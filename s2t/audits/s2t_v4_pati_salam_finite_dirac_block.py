#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


OUTPUT_PATH = Path("s2t_v4_pati_salam_finite_dirac_block_results.json")


def symmetric_random(rng, size):
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    return 0.5 * (matrix + matrix.T)


def build_dirac_block(yukawa, majorana_right, majorana_left):
    size = yukawa.shape[0]
    zero = np.zeros((size, size), dtype=complex)
    return np.block(
        [
            [zero, yukawa, majorana_right, zero],
            [yukawa.conj().T, zero, zero, majorana_left],
            [majorana_right.conj().T, zero, zero, yukawa.conj()],
            [zero, majorana_left.conj().T, yukawa.T, zero],
        ]
    )


def ko6_operators(size):
    identity = np.eye(size)
    zero = np.zeros((size, size))
    reality_permutation = np.block(
        [
            [zero, zero, identity, zero],
            [zero, zero, zero, identity],
            [identity, zero, zero, zero],
            [zero, identity, zero, zero],
        ]
    )
    grading = np.block(
        [
            [identity, zero, zero, zero],
            [zero, -identity, zero, zero],
            [zero, zero, -identity, zero],
            [zero, zero, zero, identity],
        ]
    )
    return reality_permutation, grading


def composite_fields(rng):
    phi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    sigma = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    sigma -= np.trace(sigma) * np.eye(4) / 4.0
    delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))

    sigma_two = np.array([[0.0, -1j], [1j, 0.0]])
    phi_tilde = sigma_two @ phi.conj() @ sigma_two
    couplings = {"nu": 0.7, "e": 0.2, "u": 1.1, "d": 0.4, "nu_R": 0.9}

    lepton_weak = couplings["nu"] * phi + couplings["e"] * phi_tilde
    quark_weak = couplings["u"] * phi + couplings["d"] * phi_tilde
    identity_four = np.eye(4)
    yukawa = np.kron(lepton_weak, sigma) + np.kron(
        quark_weak, identity_four - sigma
    )

    majorana_right = np.zeros((8, 8), dtype=complex)
    for right_a in range(2):
        for color_i in range(4):
            row = 4 * right_a + color_i
            for right_b in range(2):
                for color_j in range(4):
                    column = 4 * right_b + color_j
                    majorana_right[row, column] = (
                        np.conj(couplings["nu_R"])
                        * delta[right_a, color_j]
                        * delta[right_b, color_i]
                    )
    return phi, sigma, delta, yukawa, majorana_right


def main():
    rng = np.random.default_rng(20260813)
    one_chiral_dimension = 2 * 4
    yukawa = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    majorana_right = symmetric_random(rng, 8)
    majorana_left = symmetric_random(rng, 8)
    dirac = build_dirac_block(yukawa, majorana_right, majorana_left)
    reality, grading = ko6_operators(8)

    phi, sigma, delta, composite_yukawa, composite_majorana = composite_fields(rng)

    checks = {
        "self_adjoint_error": float(np.linalg.norm(dirac - dirac.conj().T)),
        "odd_grading_error": float(np.linalg.norm(grading @ dirac + dirac @ grading)),
        "reality_error": float(np.linalg.norm(dirac @ reality - reality @ dirac.conj())),
        "J_gamma_anticommutator_error": float(
            np.linalg.norm(reality @ grading + grading @ reality)
        ),
        "right_majorana_symmetry_error": float(
            np.linalg.norm(majorana_right - majorana_right.T)
        ),
        "left_majorana_symmetry_error": float(
            np.linalg.norm(majorana_left - majorana_left.T)
        ),
        "composite_right_majorana_symmetry_error": float(
            np.linalg.norm(composite_majorana - composite_majorana.T)
        ),
    }

    output = {
        "gate": "version4_pati_salam_finite_dirac_block",
        "date": "2026-08-13",
        "finite_algebra_target": "H_R direct_sum H_L direct_sum M4(C)",
        "one_generation_particle_modules": {
            "R": "(2_R,1_L,4_4)",
            "L": "(1_R,2_L,4_4)",
            "complex_dimension_R": one_chiral_dimension,
            "complex_dimension_L": one_chiral_dimension,
            "particle_dimension": 16,
            "KO6_particle_antiparticle_dimension": 32,
        },
        "grading_order": ["R:+", "L:-", "R^c:-", "L^c:+"],
        "dirac_channels": {
            "Y_LR": {
                "matrix_shape": [8, 8],
                "complex_components": 64,
                "representation": "(2_R,2_L,1_4+15_4)",
            },
            "M_R": {
                "matrix_shape": [8, 8],
                "symmetric": True,
                "complex_components": 36,
                "representation": "(3_R,1_L,10_4)+(1_R,1_L,6_4)",
            },
            "M_L": {
                "matrix_shape": [8, 8],
                "symmetric": True,
                "complex_components": 36,
                "representation": "(1_R,3_L,10_4)+(1_R,1_L,6_4)",
            },
            "total_general_complex_components": 136,
        },
        "matrix_checks": checks,
        "composite_first_order_ansatz": {
            "fundamental_fields": {
                "phi": {"shape": list(phi.shape), "complex_components": 4},
                "Delta": {"shape": list(delta.shape), "complex_components": 8},
                "Sigma_4_traceless": {
                    "shape": list(sigma.shape),
                    "complexified_components": 15,
                    "Hermitian_reality_components": 15,
                },
            },
            "complexified_input_components_before_gauge_quotient": 27,
            "real_components_if_Sigma4_is_Hermitian": 39,
            "general_active_Y_plus_MR_complex_components": 100,
            "Y_formula": (
                "(k_nu phi+k_e phi_tilde) tensor Sigma_4 + "
                "(k_u phi+k_d phi_tilde) tensor (I4-Sigma_4)"
            ),
            "MR_formula": "k_nuR^* Delta_(a,J) Delta_(b,I)",
            "Y_shape": list(composite_yukawa.shape),
            "MR_shape": list(composite_majorana.shape),
            "MR_symmetric": checks["composite_right_majorana_symmetry_error"]
            < 1.0e-12,
            "is_nonlinear_restriction_of_general_block": True,
            "is_derived_from_project_first_order_double_commutator": False,
        },
        "verdict": {
            "explicit_KO6_target_matrix_constructed": True,
            "literature_field_representations_reproduced": True,
            "project_spectral_triple_completed": False,
            "missing_checks": [
                "explicit left and opposite algebra representations",
                "full first-order double commutator",
                "orientability and unimodularity",
                "inner-fluctuation derivation of the composite formulas",
                "spectral potential and physical half-trace",
            ],
            "next_gate": (
                "implement the algebra and opposite-algebra matrices and compute the exact "
                "first-order double-commutator kernel for the full and SM-restricted algebras"
            ),
        },
        "sources": ["arXiv:1507.08161", "arXiv:1304.8050"],
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    for name, value in checks.items():
        print(name, f"{value:.3e}")
    print("general complex components: 136")
    print("composite complexified inputs: 27")
    print("composite real inputs with Hermitian Sigma4: 39")


if __name__ == "__main__":
    main()