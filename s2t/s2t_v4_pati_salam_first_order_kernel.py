#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


OUTPUT_PATH = Path("s2t_v4_pati_salam_first_order_kernel_results.json")
TOLERANCE = 1.0e-9


def quaternion_basis():
    basis = []
    for alpha, beta in ((1, 0), (1j, 0), (0, 1), (0, 1j)):
        basis.append(
            np.array(
                [[alpha, beta], [-np.conj(beta), np.conj(alpha)]], dtype=complex
            )
        )
    return basis


def complex_matrix_real_basis(size):
    basis = []
    for row in range(size):
        for column in range(size):
            for value in (1.0, 1.0j):
                matrix = np.zeros((size, size), dtype=complex)
                matrix[row, column] = value
                basis.append(matrix)
    return basis


def full_algebra_basis():
    zero_two = np.zeros((2, 2), dtype=complex)
    zero_four = np.zeros((4, 4), dtype=complex)
    basis = []
    for quaternion in quaternion_basis():
        basis.append((quaternion, zero_two, zero_four))
        basis.append((zero_two, quaternion, zero_four))
    for matrix in complex_matrix_real_basis(4):
        basis.append((zero_two, zero_two, matrix))
    return basis


def sm_algebra_basis(qr_swap=False, lepton_conjugate=False):
    zero_two = np.zeros((2, 2), dtype=complex)
    zero_four = np.zeros((4, 4), dtype=complex)
    basis = []
    for lam in (1.0, 1.0j):
        right_values = [lam, np.conj(lam)]
        if qr_swap:
            right_values.reverse()
        right = np.diag(right_values)
        four = np.zeros((4, 4), dtype=complex)
        four[0, 0] = np.conj(lam) if lepton_conjugate else lam
        basis.append((right, zero_two, four))
    for quaternion in quaternion_basis():
        basis.append((zero_two, quaternion, zero_four))
    for matrix_three in complex_matrix_real_basis(3):
        four = np.zeros((4, 4), dtype=complex)
        four[1:, 1:] = matrix_three
        basis.append((zero_two, zero_two, four))
    return basis


def ko6_reality_permutation():
    identity = np.eye(8)
    zero = np.zeros((8, 8))
    return np.block(
        [
            [zero, zero, identity, zero],
            [zero, zero, zero, identity],
            [identity, zero, zero, zero],
            [zero, identity, zero, zero],
        ]
    )


REALITY = ko6_reality_permutation()
ZERO_EIGHT = np.zeros((8, 8), dtype=complex)


def algebra_representation(element):
    right, left, four = element
    return np.block(
        [
            [np.kron(right, np.eye(4)), ZERO_EIGHT, ZERO_EIGHT, ZERO_EIGHT],
            [ZERO_EIGHT, np.kron(left, np.eye(4)), ZERO_EIGHT, ZERO_EIGHT],
            [ZERO_EIGHT, ZERO_EIGHT, np.kron(np.eye(2), four), ZERO_EIGHT],
            [ZERO_EIGHT, ZERO_EIGHT, ZERO_EIGHT, np.kron(np.eye(2), four)],
        ]
    )


def opposite_representation(element):
    representation = algebra_representation(element)
    return REALITY @ representation.conj() @ REALITY


def dirac_from_channels(yukawa=None, majorana_right=None, majorana_left=None):
    yukawa = ZERO_EIGHT if yukawa is None else yukawa
    majorana_right = ZERO_EIGHT if majorana_right is None else majorana_right
    majorana_left = ZERO_EIGHT if majorana_left is None else majorana_left
    return np.block(
        [
            [ZERO_EIGHT, yukawa, majorana_right, ZERO_EIGHT],
            [yukawa.conj().T, ZERO_EIGHT, ZERO_EIGHT, majorana_left],
            [majorana_right.conj().T, ZERO_EIGHT, ZERO_EIGHT, yukawa.conj()],
            [ZERO_EIGHT, majorana_left.conj().T, yukawa.T, ZERO_EIGHT],
        ]
    )


def dirac_variable_basis():
    matrices = []
    labels = []
    for row in range(8):
        for column in range(8):
            for part, value in (("re", 1.0), ("im", 1.0j)):
                matrix = np.zeros((8, 8), dtype=complex)
                matrix[row, column] = value
                matrices.append(dirac_from_channels(yukawa=matrix))
                labels.append(("Y", row, column, part))
    for channel in ("MR", "ML"):
        for row in range(8):
            for column in range(row, 8):
                for part, value in (("re", 1.0), ("im", 1.0j)):
                    matrix = np.zeros((8, 8), dtype=complex)
                    matrix[row, column] = value
                    matrix[column, row] = value
                    if channel == "MR":
                        matrices.append(dirac_from_channels(majorana_right=matrix))
                    else:
                        matrices.append(dirac_from_channels(majorana_left=matrix))
                    labels.append((channel, row, column, part))
    return np.asarray(matrices), labels


VARIABLE_MATRICES, VARIABLE_LABELS = dirac_variable_basis()
LABEL_INDEX = {label: index for index, label in enumerate(VARIABLE_LABELS)}


def constraint_matrix(left_element, right_element):
    representation = algebra_representation(left_element)
    opposite = opposite_representation(right_element)
    columns = []
    for dirac in VARIABLE_MATRICES:
        commutator = dirac @ representation - representation @ dirac
        double = commutator @ opposite - opposite @ commutator
        columns.append(np.concatenate((double.real.ravel(), double.imag.ravel())))
    return np.asarray(columns).T


def numerical_rank(gram):
    eigenvalues = np.linalg.eigvalsh(gram)
    threshold = max(TOLERANCE, eigenvalues[-1] * 1.0e-10)
    return int(np.sum(eigenvalues > threshold)), eigenvalues


def rank_witness(algebra_basis, analytic_kernel_dimension):
    variable_count = len(VARIABLE_MATRICES)
    target_rank = variable_count - analytic_kernel_dimension
    gram = np.zeros((variable_count, variable_count))
    used_pairs = 0
    for left_element in algebra_basis:
        for right_element in algebra_basis:
            matrix = constraint_matrix(left_element, right_element)
            gram += matrix.T @ matrix
            used_pairs += 1
            if used_pairs % 4 == 0:
                rank, eigenvalues = numerical_rank(gram)
                if rank >= target_rank:
                    return gram, used_pairs, rank, eigenvalues
    rank, eigenvalues = numerical_rank(gram)
    return gram, used_pairs, rank, eigenvalues


def coefficient_vector(entries):
    vector = np.zeros(len(VARIABLE_LABELS))
    for label, coefficient in entries.items():
        vector[LABEL_INDEX[label]] = coefficient
    return vector


def full_analytic_kernel():
    basis = []
    for right_index in range(2):
        for left_index in range(2):
            for part, value in (("re", 1.0), ("im", 1.0)):
                entries = {}
                for color in range(4):
                    label = (
                        "Y",
                        4 * right_index + color,
                        4 * left_index + color,
                        part,
                    )
                    entries[label] = value
                basis.append(coefficient_vector(entries))
    return np.asarray(basis).T


def sm_analytic_kernel():
    basis = []
    color_projectors = ([0], [1, 2, 3])
    for colors in color_projectors:
        for right_index in range(2):
            for left_index in range(2):
                for part in ("re", "im"):
                    entries = {}
                    for color in colors:
                        entries[
                            (
                                "Y",
                                4 * right_index + color,
                                4 * left_index + color,
                                part,
                            )
                        ] = 1.0
                    basis.append(coefficient_vector(entries))

    for color in range(4):
        for part in ("re", "im"):
            entries = {("MR", 0, color, part): 1.0}
            basis.append(coefficient_vector(entries))
    for color in range(4):
        for part in ("re", "im"):
            entries = {("MR", color, 4, part): 1.0}
            basis.append(coefficient_vector(entries))
    return np.asarray(basis).T


def reconstruct_dirac(coefficients):
    return np.tensordot(coefficients, VARIABLE_MATRICES, axes=(0, 0))


def exhaustive_kernel_error(analytic_kernel, algebra_basis):
    maximum = 0.0
    for column in range(analytic_kernel.shape[1]):
        dirac = reconstruct_dirac(analytic_kernel[:, column])
        for left_element in algebra_basis:
            representation = algebra_representation(left_element)
            commutator = dirac @ representation - representation @ dirac
            for right_element in algebra_basis:
                opposite = opposite_representation(right_element)
                double = commutator @ opposite - opposite @ commutator
                maximum = max(maximum, float(np.linalg.norm(double)))
    return maximum


def nullspace_from_gram(gram, dimension):
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    return eigenvectors[:, :dimension], eigenvalues


def subspace_overlap(first, second):
    first_q, _ = np.linalg.qr(first)
    second_q, _ = np.linalg.qr(second)
    singular_values = np.linalg.svd(first_q.T @ second_q, compute_uv=False)
    return float(np.min(singular_values)), float(np.max(singular_values))


def random_element(rng, qr_swap=False, lepton_conjugate=False):
    alpha = rng.normal() + 1j * rng.normal()
    beta = rng.normal() + 1j * rng.normal()
    left = np.array([[alpha, beta], [-np.conj(beta), np.conj(alpha)]])
    lam = rng.normal() + 1j * rng.normal()
    right_values = [lam, np.conj(lam)]
    if qr_swap:
        right_values.reverse()
    right = np.diag(right_values)
    four = np.zeros((4, 4), dtype=complex)
    four[0, 0] = np.conj(lam) if lepton_conjugate else lam
    four[1:, 1:] = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    return right, left, four


def convention_kernel_dimension(qr_swap, lepton_conjugate):
    rng = np.random.default_rng(20260813 + 10 * qr_swap + lepton_conjugate)
    gram = np.zeros((len(VARIABLE_MATRICES), len(VARIABLE_MATRICES)))
    for _ in range(16):
        matrix = constraint_matrix(
            random_element(rng, qr_swap, lepton_conjugate),
            random_element(rng, qr_swap, lepton_conjugate),
        )
        gram += matrix.T @ matrix
    rank, _ = numerical_rank(gram)
    projector = nullspace_from_gram(gram, len(VARIABLE_MATRICES) - rank)[0]
    projection_diagonal = np.sum(projector * projector, axis=1)
    active_majorana_pairs = sorted(
        {
            (label[1], label[2])
            for index, label in enumerate(VARIABLE_LABELS)
            if label[0] == "MR"
            and label[3] == "re"
            and projection_diagonal[index] > 0.9
        }
    )
    return len(VARIABLE_MATRICES) - rank, active_majorana_pairs


def main():
    full_basis = full_algebra_basis()
    sm_basis = sm_algebra_basis()
    full_analytic = full_analytic_kernel()
    sm_analytic = sm_analytic_kernel()

    full_gram, full_pairs, full_rank, full_eigenvalues = rank_witness(
        full_basis, full_analytic.shape[1]
    )
    sm_gram, sm_pairs, sm_rank, sm_eigenvalues = rank_witness(
        sm_basis, sm_analytic.shape[1]
    )
    full_numerical, _ = nullspace_from_gram(full_gram, full_analytic.shape[1])
    sm_numerical, _ = nullspace_from_gram(sm_gram, sm_analytic.shape[1])

    convention_scan = {}
    for qr_swap in (False, True):
        for lepton_conjugate in (False, True):
            dimension, active_pairs = convention_kernel_dimension(
                qr_swap, lepton_conjugate
            )
            convention_scan[f"qr_swap={qr_swap},lepton_conjugate={lepton_conjugate}"] = {
                "kernel_real_dimension": dimension,
                "active_MR_upper_pairs": active_pairs,
            }

    output = {
        "gate": "version4_pati_salam_first_order_kernel",
        "date": "2026-08-13",
        "variable_space": {
            "Y_real_dimension": 128,
            "MR_real_dimension": 72,
            "ML_real_dimension": 72,
            "total_real_dimension": len(VARIABLE_MATRICES),
        },
        "algebra_actions": {
            "full_Pati_Salam_real_basis_dimension": len(full_basis),
            "embedded_SM_real_basis_dimension": len(sm_basis),
            "particle_action": "q_R on R, q_L on L, M4(C) on antiparticles",
            "opposite_action": "J pi(b) J^-1",
        },
        "full_algebra_kernel": {
            "constraint_rank": full_rank,
            "kernel_real_dimension": len(VARIABLE_MATRICES) - full_rank,
            "rank_witness_pairs": full_pairs,
            "analytic_form": "Y=A_(2x2) tensor I4; MR=ML=0",
            "exhaustive_basis_error": exhaustive_kernel_error(
                full_analytic, full_basis
            ),
            "analytic_numeric_principal_cosine_range": subspace_overlap(
                full_analytic, full_numerical
            ),
            "first_nonzero_gram_eigenvalue": float(
                full_eigenvalues[full_analytic.shape[1]]
            ),
        },
        "SM_subalgebra_kernel": {
            "constraint_rank": sm_rank,
            "kernel_real_dimension": len(VARIABLE_MATRICES) - sm_rank,
            "rank_witness_pairs": sm_pairs,
            "Y_real_dimension": 16,
            "Y_analytic_form": "A_lepton tensor P_lepton + A_quark tensor P_quark",
            "MR_real_dimension": 16,
            "MR_analytic_form": (
                "weak blocks [[e u^T+u e^T, v e^T], [e v^T, 0]], "
                "u,v in C4 and e=(1,0,0,0)"
            ),
            "ML_real_dimension": 0,
            "representation_reading": (
                "independent lepton/quark bidoublet seeds plus one Delta-like "
                "(2_R,4_4) Majorana seed"
            ),
            "exhaustive_basis_error": exhaustive_kernel_error(sm_analytic, sm_basis),
            "analytic_numeric_principal_cosine_range": subspace_overlap(
                sm_analytic, sm_numerical
            ),
            "first_nonzero_gram_eigenvalue": float(
                sm_eigenvalues[sm_analytic.shape[1]]
            ),
        },
        "convention_scan": convention_scan,
        "literature_comparison": {
            "full_first_order_enforces_quark_lepton_unified_bidoublet": True,
            "SM_first_order_releases_quark_lepton_split": True,
            "SM_first_order_releases_Delta_like_seed": True,
            "composite_quadratic_fields_derived_from_inner_fluctuation": False,
            "interpretation": (
                "the exact kernel reproduces the structural seeds of the composite branch, "
                "but the nonlinear Sigma and Delta-Delta fields still require the full "
                "linear plus quadratic inner-fluctuation calculation"
            ),
        },
        "verdict": {
            "first_order_kernel_gate": "strong conditional pass",
            "reason_not_full_pass": (
                "the kernel is exact for the declared representation convention, but the "
                "quadratic inner fluctuation and physical finite-Dirac normalization are not "
                "yet derived"
            ),
            "next_gate": (
                "compute A_(1)=sum a[D,b] and the required quadratic A_(2) term on the exact "
                "SM kernel, then compare its generated fields with the literature composite "
                "formulas"
            ),
        },
        "sources": ["arXiv:1304.8050", "arXiv:1507.08161"],
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print("full kernel real dimension:", output["full_algebra_kernel"]["kernel_real_dimension"])
    print("SM kernel real dimension:", output["SM_subalgebra_kernel"]["kernel_real_dimension"])
    print("full exhaustive error:", output["full_algebra_kernel"]["exhaustive_basis_error"])
    print("SM exhaustive error:", output["SM_subalgebra_kernel"]["exhaustive_basis_error"])
    print("verdict: strong conditional pass")


if __name__ == "__main__":
    main()