#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def partial_traces(rho):
    tensor = rho.reshape(2, 2, 2, 2)
    rho_rp3 = np.trace(tensor, axis1=0, axis2=2)
    rho_s1 = np.trace(tensor, axis1=1, axis2=3)
    return rho_rp3, rho_s1


def entropy(rho):
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-15]
    return float(-np.sum(eigenvalues * np.log(eigenvalues)))


def partial_transpose(rho):
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def jarlskog(unitary):
    return float(
        np.imag(
            unitary[0, 0]
            * unitary[1, 1]
            * np.conjugate(unitary[0, 1])
            * np.conjugate(unitary[1, 0])
        )
    )


def cross_matrix(axis):
    x_value, y_value, z_value = axis
    return np.array(
        [
            [0.0, -z_value, y_value],
            [z_value, 0.0, -x_value],
            [-y_value, x_value, 0.0],
        ]
    )


def main():
    wilson = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    cosine = wilson["continuous_two_sector_solution"]["cos_theta_numeric"]
    axes = wilson["factor_axis_selector"]["summary"]["inverse_length"][
        "selected_axes"
    ]

    basis = triplet_basis()
    identity2 = np.eye(2, dtype=int)
    translate_rp3 = permutation_matrix(
        affine_permutation(identity2, (1, 0))
    )
    translate_s1 = permutation_matrix(
        affine_permutation(identity2, (0, 1))
    )
    restricted_rp3 = restrict(translate_rp3, basis)
    restricted_s1 = restrict(translate_s1, basis)
    triplet_projector = basis @ basis.T
    singlet_projector = np.eye(4) - triplet_projector

    kernels = {
        "inverse_length": (1.0 / math.pi, 1.0 / (2.0 * math.pi)),
        "inverse_square": (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2)),
        "tunneling": (math.exp(-math.pi), math.exp(-2.0 * math.pi)),
    }

    rows = []
    spectral_readout_commutators = []
    cross_sector_rows = []
    for kernel_name, (weight_rp3, weight_s1) in kernels.items():
        factor_operator = (
            weight_rp3 * (np.eye(3) - restricted_rp3)
            + weight_s1 * (np.eye(3) - restricted_s1)
        )
        sector_eigenvectors = {}
        for sign in [1, -1]:
            for axis_index, axis_values in enumerate(axes):
                axis = np.array(axis_values)
                incidence = cosine * np.eye(3) + (1.0 - cosine) * np.outer(
                    axis, axis
                )
                triplet_hamiltonian = factor_operator + sign * incidence
                hamiltonian = basis @ triplet_hamiltonian @ basis.T
                rho = expm(-hamiltonian)
                rho /= np.trace(rho)

                rho_rp3, rho_s1 = partial_traces(rho)
                product_state = np.kron(rho_s1, rho_rp3)
                factorization_error = float(np.linalg.norm(rho - product_state))
                mutual_information = float(
                    entropy(rho_rp3) + entropy(rho_s1) - entropy(rho)
                )
                pt_eigenvalues = np.linalg.eigvalsh(partial_transpose(rho))
                negativity = float(-np.sum(pt_eigenvalues[pt_eigenvalues < 0]))

                eigenvalues, eigenvectors = np.linalg.eigh(rho)
                minimum_gap = float(np.min(np.diff(eigenvalues)))
                triplet_probability = float(
                    np.real(np.trace(triplet_projector @ rho))
                )
                modular_triplet_error = float(
                    np.linalg.norm(rho @ triplet_projector - triplet_projector @ rho)
                )

                test_operator = np.arange(16, dtype=float).reshape(4, 4)
                test_operator = test_operator + test_operator.T
                block_expectation = (
                    triplet_projector @ test_operator @ triplet_projector
                    + singlet_projector @ test_operator @ singlet_projector
                )
                state_preservation_error = float(
                    abs(
                        np.trace(rho @ block_expectation)
                        - np.trace(rho @ test_operator)
                    )
                )

                readout_commutators = []
                for excluded in range(4):
                    isometry = np.delete(eigenvectors, excluded, axis=1)
                    compressed_rp3 = (
                        isometry.conjugate().T @ translate_rp3 @ isometry
                    )
                    compressed_s1 = (
                        isometry.conjugate().T @ translate_s1 @ isometry
                    )
                    commutator_norm = float(
                        np.linalg.norm(
                            compressed_rp3 @ compressed_s1
                            - compressed_s1 @ compressed_rp3
                        )
                    )
                    readout_commutators.append(commutator_norm)
                    spectral_readout_commutators.append(commutator_norm)

                rows.append(
                    {
                        "kernel": kernel_name,
                        "wilson_sign": sign,
                        "axis_index": axis_index,
                        "rho_eigenvalues": eigenvalues.tolist(),
                        "faithful": bool(eigenvalues[0] > 0),
                        "minimum_spectral_gap": minimum_gap,
                        "factorization_error": factorization_error,
                        "mutual_information": mutual_information,
                        "PPT_negativity": negativity,
                        "entangled": negativity > 1e-12,
                        "triplet_probability": triplet_probability,
                        "discarded_singlet_probability": 1.0
                        - triplet_probability,
                        "modular_triplet_projector_error": modular_triplet_error,
                        "block_expectation_state_preservation_error": (
                            state_preservation_error
                        ),
                        "rank3_spectral_readout_commutators": readout_commutators,
                    }
                )
                sector_eigenvectors[(sign, axis_index)] = np.linalg.eigh(
                    triplet_hamiltonian
                )[1]

            overlap = (
                sector_eigenvectors[(sign, 0)].conjugate().T
                @ sector_eigenvectors[(sign, 1)]
            )
            cross_sector_rows.append(
                {
                    "kernel": kernel_name,
                    "wilson_sign": sign,
                    "absolute_overlap": np.abs(overlap).tolist(),
                    "zero_entries": int(np.sum(np.abs(overlap) < 1e-10)),
                    "unit_entries": int(
                        np.sum(np.abs(np.abs(overlap) - 1.0) < 1e-10)
                    ),
                    "Jarlskog": jarlskog(overlap),
                }
            )

    axis_equivalence = []
    for kernel_name in kernels:
        for sign in [1, -1]:
            pair = [
                row
                for row in rows
                if row["kernel"] == kernel_name and row["wilson_sign"] == sign
            ]
            axis_equivalence.append(
                {
                    "kernel": kernel_name,
                    "wilson_sign": sign,
                    "eigenvalue_difference": float(
                        np.linalg.norm(
                            np.array(pair[0]["rho_eigenvalues"])
                            - np.array(pair[1]["rho_eigenvalues"])
                        )
                    ),
                    "mutual_information_difference": abs(
                        pair[0]["mutual_information"]
                        - pair[1]["mutual_information"]
                    ),
                    "negativity_difference": abs(
                        pair[0]["PPT_negativity"] - pair[1]["PPT_negativity"]
                    ),
                }
            )

    angle = math.acos(cosine)
    oriented_rows = []
    for mode in ["modular_generator", "full_Wilson_Hermitian_part"]:
        for kernel_name, (weight_rp3, weight_s1) in kernels.items():
            factor_operator = (
                weight_rp3 * (np.eye(3) - restricted_rp3)
                + weight_s1 * (np.eye(3) - restricted_s1)
            )
            for orientation_up in [1, -1]:
                for orientation_down in [1, -1]:
                    sector_vectors = []
                    for axis_values, orientation in zip(
                        axes, [orientation_up, orientation_down]
                    ):
                        axis = np.array(axis_values)
                        generator = 1j * cross_matrix(axis)
                        incidence = cosine * np.eye(3) + (
                            1.0 - cosine
                        ) * np.outer(axis, axis)
                        if mode == "modular_generator":
                            hamiltonian = (
                                factor_operator
                                + orientation * angle * generator
                            )
                        else:
                            hamiltonian = (
                                factor_operator
                                + incidence
                                + orientation
                                * math.sin(angle)
                                * generator
                            )
                        sector_vectors.append(np.linalg.eigh(hamiltonian)[1])
                    overlap = (
                        sector_vectors[0].conjugate().T @ sector_vectors[1]
                    )
                    oriented_rows.append(
                        {
                            "mode": mode,
                            "kernel": kernel_name,
                            "orientation_up": orientation_up,
                            "orientation_down": orientation_down,
                            "absolute_overlap": np.abs(overlap).tolist(),
                            "minimum_absolute_entry": float(
                                np.min(np.abs(overlap))
                            ),
                            "zero_entries": int(
                                np.sum(np.abs(overlap) < 1e-10)
                            ),
                            "Jarlskog": jarlskog(overlap),
                        }
                    )

    unique_state_classes = {
        (row["kernel"], row["wilson_sign"]) for row in rows
    }
    results = {
        "status": "minimal_Wilson_Gibbs_states_are_correlated_but_do_not_select_a_unique_modular_readout_or_full_flavour_mixing",
        "date": "2026-08-06",
        "state_ansatz": {
            "formula": "rho=exp(-H)/Tr exp(-H), H=B[L_kernel+s A_n]B^T",
            "beta": 1,
            "singlet_energy": 0,
            "declared_class": {
                "kernels": list(kernels),
                "Wilson_signs": [1, -1],
                "residual_axis_representatives": 2,
            },
            "warning": (
                "The Wilson saddle fixes angle and axis orbit, but not this "
                "Gibbs ansatz, sign, beta, or singlet energy."
            ),
        },
        "state_rows": rows,
        "axis_orbit_equivalence": axis_equivalence,
        "factorization_gate": {
            "all_states_nonfactorizing": all(
                row["factorization_error"] > 1e-10 for row in rows
            ),
            "factorization_error_range": [
                min(row["factorization_error"] for row in rows),
                max(row["factorization_error"] for row in rows),
            ],
            "mutual_information_range": [
                min(row["mutual_information"] for row in rows),
                max(row["mutual_information"] for row in rows),
            ],
            "positive_sign_entangled_count": sum(
                row["entangled"] for row in rows if row["wilson_sign"] == 1
            ),
            "negative_sign_entangled_count": sum(
                row["entangled"] for row in rows if row["wilson_sign"] == -1
            ),
            "finding": (
                "Nonfactorization is robust, but quantum entanglement is sign "
                "dependent. The undeclared Wilson sign blocks inevitability."
            ),
        },
        "modular_subalgebra_gate": {
            "all_states_faithful_and_nondegenerate": all(
                row["faithful"] and row["minimum_spectral_gap"] > 1e-10
                for row in rows
            ),
            "canonical_M3_plus_C_modular_invariant": all(
                row["modular_triplet_projector_error"] < 1e-12 for row in rows
            ),
            "state_preserving_block_expectation": all(
                row["block_expectation_state_preservation_error"] < 1e-11
                for row in rows
            ),
            "canonical_block_algebra": "P3 M4 P3 direct_sum C P1",
            "canonical_block_partition_count_for_nondegenerate_state": 15,
            "rank3_plus_rank1_spectral_partitions": 4,
            "discarded_singlet_probability_range": [
                min(row["discarded_singlet_probability"] for row in rows),
                max(row["discarded_singlet_probability"] for row in rows),
            ],
            "finding": (
                "The state preserves M3 plus C but does not remove the singlet. "
                "A pure M3 world needs nonlinear conditioning and discards finite "
                "probability. Multiple modular block partitions remain."
            ),
        },
        "spectral_rank3_readout_gate": {
            "tested_readouts": len(spectral_readout_commutators),
            "maximum_factor_commutator_norm": max(
                spectral_readout_commutators
            ),
            "noncommuting_readouts": sum(
                value > 1e-10 for value in spectral_readout_commutators
            ),
            "finding": (
                "Every rank-three spectral complement selected by the minimal "
                "state preserves factor commutativity. State selection alone "
                "does not create CKM."
            ),
        },
        "relative_sector_gate": {
            "rows": cross_sector_rows,
            "all_CP_conserving": all(
                abs(row["Jarlskog"]) < 1e-12 for row in cross_sector_rows
            ),
            "all_have_spectator_direction": all(
                row["unit_entries"] >= 1 and row["zero_entries"] >= 4
                for row in cross_sector_rows
            ),
            "finding": (
                "The two residual-axis states give one real two-family rotation "
                "with a spectator direction, not full CKM."
            ),
        },
        "oriented_Wilson_phase_gate": {
            "tested_pairs": len(oriented_rows),
            "rows": oriented_rows,
            "full_support_pairs": sum(
                row["zero_entries"] == 0 for row in oriented_rows
            ),
            "nonzero_CP_pairs": sum(
                abs(row["Jarlskog"]) > 1e-12 for row in oriented_rows
            ),
            "maximum_absolute_Jarlskog": max(
                abs(row["Jarlskog"]) for row in oriented_rows
            ),
            "finding": (
                "Restoring the oriented Hermitian Wilson generator removes the "
                "spectator zeros and gives full three-family overlap, but every "
                "declared pair remains CP conserving. A complex matrix is not "
                "enough; the two sectors require a relative modular cocycle not "
                "removable by their common real structure."
            ),
        },
        "identifiability": {
            "state_classes_after_axis_quotient": len(unique_state_classes),
            "unfixed_choices": [
                "factor kernel",
                "Wilson insertion sign",
                "Gibbs-state derivation and beta",
                "singlet energy or conditioning rule",
                "relative up/down state assignment",
            ],
        },
        "scientific_verdict": {
            "positive": (
                "Wilson angle plus factor geometry naturally creates a "
                "nonfactorizing state, and one sign branch is entangled."
            ),
            "negative": (
                "Entanglement is sign dependent, the observable algebra is not "
                "unique, pure triplet readout requires conditioning, and all "
                "minimal spectral readouts retain commuting factors. Oriented "
                "Wilson generators create full mixing but still give zero CP."
            ),
            "next_gate": (
                "Derive sign, beta and singlet energy from one parent action, "
                "then construct a relative modular cocycle for the two sectors "
                "and test whether it breaks the common antiunitary symmetry."
            ),
        },
    }

    assert len(rows) == 12
    assert len(unique_state_classes) == 6
    assert all(
        row["eigenvalue_difference"] < 1e-12
        and row["mutual_information_difference"] < 1e-12
        and row["negativity_difference"] < 1e-12
        for row in axis_equivalence
    )
    assert results["factorization_gate"]["all_states_nonfactorizing"]
    assert results["factorization_gate"]["positive_sign_entangled_count"] == 0
    assert results["factorization_gate"]["negative_sign_entangled_count"] == 6
    assert results["spectral_rank3_readout_gate"]["tested_readouts"] == 48
    assert results["spectral_rank3_readout_gate"]["noncommuting_readouts"] == 0
    assert results["relative_sector_gate"]["all_CP_conserving"]
    assert len(oriented_rows) == 24
    assert results["oriented_Wilson_phase_gate"]["full_support_pairs"] == 24
    assert results["oriented_Wilson_phase_gate"]["nonzero_CP_pairs"] == 0

    Path("s2t_wilson_modular_state_readout_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "state_classes": len(unique_state_classes),
                "nonfactorizing_states": len(rows),
                "entangled_positive_sign": 0,
                "entangled_negative_sign": 6,
                "spectral_rank3_readouts": 48,
                "noncommuting_spectral_readouts": 0,
                "full_CKM_from_relative_states": False,
                "oriented_full_support_pairs": 24,
                "oriented_nonzero_CP_pairs": 0,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()