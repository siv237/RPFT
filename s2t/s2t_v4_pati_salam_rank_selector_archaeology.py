#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
import sympy as sp


OUTPUT_PATH = Path("s2t_v4_pati_salam_rank_selector_archaeology_results.json")
RANDOM_SEED = 20260813
RANDOM_TESTS = 200


def direct_path(delta):
    tensor = np.einsum("aI,bJ->aIbJ", delta, delta)
    return tensor.reshape(8, 8)


def crossed_path(delta):
    tensor = np.einsum("aJ,bI->aIbJ", delta, delta)
    return tensor.reshape(8, 8)


def frobenius_square(matrix):
    return float(np.vdot(matrix, matrix).real)


def symbolic_hessian():
    coordinates = sp.symbols("x0:16", real=True)
    kappa = sp.symbols("kappa", real=True)
    delta = sp.zeros(2, 4)
    for right_index in range(2):
        for color in range(4):
            coordinate = 2 * (4 * right_index + color)
            delta[right_index, color] = (
                coordinates[coordinate] + sp.I * coordinates[coordinate + 1]
            )
    gram = delta * delta.conjugate().T
    rho = sp.trace(gram)
    tau = sp.trace(gram * gram)
    determinant = sp.det(gram)
    potential = -rho**2 + tau**2 + kappa * determinant
    vacuum_value = 2 ** (-sp.Rational(1, 4))
    substitution = {coordinate: 0 for coordinate in coordinates}
    substitution[coordinates[0]] = vacuum_value
    hessian = sp.hessian(potential, coordinates).subs(substitution)
    return {
        "rank_one_hessian_eigenvalues": {
            str(eigenvalue): int(multiplicity)
            for eigenvalue, multiplicity in hessian.eigenvals().items()
        },
        "rank_one_energy": str(sp.simplify(potential.subs(substitution))),
        "rank_one_stationary": all(
            sp.simplify(sp.diff(potential, coordinate).subs(substitution)) == 0
            for coordinate in coordinates
        ),
    }


def signature_at_kappa(kappa):
    eigenvalues = [8 * np.sqrt(2)] + [0.0] * 9 + [np.sqrt(2) * (kappa - 2)] * 6
    return {
        "positive": int(sum(value > 1.0e-9 for value in eigenvalues)),
        "zero": int(sum(abs(value) <= 1.0e-9 for value in eigenvalues)),
        "negative": int(sum(value < -1.0e-9 for value in eigenvalues)),
    }


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    maximum_wedge_identity_error = 0.0
    maximum_weak_antisymmetry_error = 0.0
    maximum_color_antisymmetry_error = 0.0
    for _ in range(RANDOM_TESTS):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        direct = direct_path(delta)
        crossed = crossed_path(delta)
        raw_difference = direct - crossed
        gram = delta @ delta.conj().T
        determinant = float(np.linalg.det(gram).real)
        maximum_wedge_identity_error = max(
            maximum_wedge_identity_error,
            abs(frobenius_square(raw_difference) - 4.0 * determinant),
        )
        tensor = raw_difference.reshape(2, 4, 2, 4)
        weak_swap = np.transpose(tensor, (2, 1, 0, 3))
        color_swap = np.transpose(tensor, (0, 3, 2, 1))
        maximum_weak_antisymmetry_error = max(
            maximum_weak_antisymmetry_error,
            float(np.linalg.norm(tensor + weak_swap)),
        )
        maximum_color_antisymmetry_error = max(
            maximum_color_antisymmetry_error,
            float(np.linalg.norm(tensor + color_swap)),
        )

    symbolic = symbolic_hessian()
    results = {
        "random_seed": RANDOM_SEED,
        "random_tests": RANDOM_TESTS,
        "double_path_identity": {
            "direct": "Delta_(aI) Delta_(bJ)",
            "crossed": "Delta_(aJ) Delta_(bI)",
            "identity": "||direct-crossed||_F^2 = 4 det(Delta Delta^dagger)",
            "maximum_absolute_error": maximum_wedge_identity_error,
            "maximum_weak_antisymmetry_error": maximum_weak_antisymmetry_error,
            "maximum_color_antisymmetry_error": maximum_color_antisymmetry_error,
            "representation": "(1_R,6_4)",
        },
        "combined_casimir_cross_check": {
            "desired_3R_10": "2+9/2=13/2",
            "unwanted_1R_6": "0+5/2=5/2",
            "gap": 4,
        },
        "extended_potential": "V=-rho^2+tau^2+kappa det(Delta Delta^dagger)",
        **symbolic,
        "signatures": {
            "kappa_0_original": signature_at_kappa(0),
            "kappa_2_single_casimir_gap": signature_at_kappa(2),
            "kappa_4_double_path_or_combined_casimir": signature_at_kappa(4),
        },
        "rank_two_stationary_branch": {
            "exists_for": "kappa<4",
            "equal_singular_value_fourth_power": "(4-kappa)/8",
            "energy": "-(4-kappa)^2/16",
            "at_kappa_4": "collapses to the origin",
        },
        "project_archaeology": {
            "rank_one_projector_precedent": "version4_rank_one_breaking_gate.tex",
            "parallel_path_interference_precedent": "version4_common_updown_krajewski_loop_gate.tex",
            "endpoint_inclusion_exclusion_precedent": "version4_relative_krajewski_star_gate.tex",
            "casimir_gap_precedent": "version4_pati_salam_diagonal_connector_menu_gate.tex",
            "decorated_trace_precedent": "version4_algebra_embedding_weighted_selector_gate.tex",
            "common_superconnection_precedent": "version4_wilson_defect_parent_superconnection_gate.tex",
        },
        "verdict": (
            "exact algebraic rescue candidate found; parent derivation of the two-path "
            "relative sign or equivalent Casimir-decorated curvature term remains open"
        ),
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()