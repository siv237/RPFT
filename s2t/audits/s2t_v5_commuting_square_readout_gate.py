#!/usr/bin/env python3
"""Коммутирующий квадрат семейного и наблюдаемого чтений на C^300."""

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_commuting_square_readout_gate_results.json"
TOL = 1.0e-10

old_expectation = json.loads(
    (ROOT / "s2t/results/s2t_v3_conditional_expectation_results.json")
    .read_text(encoding="utf-8")
)
affine = json.loads(
    (ROOT / "s2t/results/s2t_v5_affine_ko6_reference_corner_gate_results.json")
    .read_text(encoding="utf-8")
)
modular = json.loads(
    (ROOT / "s2t/results/s2t_v5_modular_commutant_parent_correspondence_gate_results.json")
    .read_text(encoding="utf-8")
)
assert old_expectation["module_origin_derived"] is False
assert affine["family_KO6_bimodule"]["base_complex_dimension"] == 20
assert modular["closure_ledger"]["exact_moment_map_square"] is True


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return 1 if inversions % 2 == 0 else -1


def intertwiner_nullity(left_actions, right_actions, rows, columns):
    equations = []
    for left, right in zip(left_actions, right_actions):
        for row in range(rows):
            for column in range(columns):
                coefficients = np.zeros(rows * columns)
                for i in range(rows):
                    for j in range(columns):
                        basis = np.zeros((rows, columns))
                        basis[i, j] = 1.0
                        coefficients[i * columns + j] = (
                            left @ basis - basis @ right
                        )[row, column]
                equations.append(coefficients)
    rank = np.linalg.matrix_rank(np.array(equations), tol=TOL)
    return rows * columns - int(rank)


V = np.array(
    [
        [1.0, -1.0, 0.0, 0.0],
        [1.0, 1.0, -2.0, 0.0],
        [1.0, 1.0, 1.0, -3.0],
    ]
)
V /= np.linalg.norm(V, axis=1)[:, None]
P3 = V.T @ V

permutations = list(itertools.permutations(range(4)))
U4 = [permutation_matrix(item) for item in permutations]
R3 = [V @ item @ V.T for item in U4]
full_intertwiner_dimension = intertwiner_nullity(R3, U4, 3, 4)

even_pairs = [
    (left, right)
    for permutation, left, right in zip(permutations, R3, U4)
    if permutation_sign(permutation) == 1
]
even_R3 = [pair[0] for pair in even_pairs]
even_U4 = [pair[1] for pair in even_pairs]
a4_intertwiner_dimension = intertwiner_nullity(even_R3, even_U4, 3, 4)
a4_endomorphism_dimension = intertwiner_nullity(even_R3, even_R3, 3, 3)
assert full_intertwiner_dimension == 1
assert a4_intertwiner_dimension == 1
assert a4_endomorphism_dimension == 1


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def family_curvature(rho, phi):
    X = rho * V
    radius = abs(phi) ** 2
    particle = block_diagonal(
        [
            P3 - X.conj().T @ X,
            X @ X.conj().T - radius * np.eye(3),
            (radius - 1.0) * np.eye(3),
        ]
    )
    return block_diagonal([particle, particle.conj()])


family_dimension = 20
observed_dimension = 15
total_dimension = family_dimension * observed_dimension
I_family = np.eye(family_dimension)
I_observed = np.eye(observed_dimension)


def normalized_trace(matrix):
    return np.trace(matrix) / matrix.shape[0]


def partial_trace_observed(matrix):
    reshaped = matrix.reshape(
        family_dimension,
        observed_dimension,
        family_dimension,
        observed_dimension,
    )
    return np.einsum("iaja->ij", reshaped)


def partial_trace_family(matrix):
    reshaped = matrix.reshape(
        family_dimension,
        observed_dimension,
        family_dimension,
        observed_dimension,
    )
    return np.einsum("iaib->ab", reshaped)


def expectation_family(matrix):
    return np.kron(
        partial_trace_observed(matrix) / observed_dimension,
        I_observed,
    )


def expectation_observed(matrix):
    return np.kron(
        I_family,
        partial_trace_family(matrix) / family_dimension,
    )


rng = np.random.default_rng(20260816)
raw = rng.normal(size=(total_dimension, total_dimension)) + 1j * rng.normal(
    size=(total_dimension, total_dimension)
)
test_operator = raw + raw.conj().T

expectation_residuals = {
    "family_idempotence": float(
        np.linalg.norm(
            expectation_family(expectation_family(test_operator))
            - expectation_family(test_operator)
        )
    ),
    "observed_idempotence": float(
        np.linalg.norm(
            expectation_observed(expectation_observed(test_operator))
            - expectation_observed(test_operator)
        )
    ),
    "family_trace_preservation": float(
        abs(
            normalized_trace(expectation_family(test_operator))
            - normalized_trace(test_operator)
        )
    ),
    "observed_trace_preservation": float(
        abs(
            normalized_trace(expectation_observed(test_operator))
            - normalized_trace(test_operator)
        )
    ),
    "commuting_square": float(
        np.linalg.norm(
            expectation_family(expectation_observed(test_operator))
            - expectation_observed(expectation_family(test_operator))
        )
    ),
}
assert max(expectation_residuals.values()) < TOL

family_F = family_curvature(0.83, 0.61 + 0.20j)
raw_observed = rng.normal(size=(observed_dimension, observed_dimension))
observed_F = raw_observed + raw_observed.T

family_lift = np.kron(family_F, I_observed)
observed_lift = np.kron(I_family, observed_F)
total_F = family_lift + observed_lift

family_trace = normalized_trace(family_F)
cross_term = normalized_trace(family_lift.conj().T @ observed_lift)
norm_decomposition_residual = abs(
    normalized_trace(total_F.conj().T @ total_F)
    - normalized_trace(family_F.conj().T @ family_F)
    - normalized_trace(observed_F.conj().T @ observed_F)
)
factor_norm_residuals = {
    "family": float(
        abs(
            normalized_trace(family_lift.conj().T @ family_lift)
            - normalized_trace(family_F.conj().T @ family_F)
        )
    ),
    "observed": float(
        abs(
            normalized_trace(observed_lift.conj().T @ observed_lift)
            - normalized_trace(observed_F.conj().T @ observed_F)
        )
    ),
}
assert abs(family_trace) < TOL
assert abs(cross_term) < TOL
assert norm_decomposition_residual < TOL
assert max(factor_norm_residuals.values()) < TOL

# На эквивариантном пространстве полей остаются rho и комплексное Phi.
# Радиальный потенциал получается непосредственно из трех блоков кривизны.
radial_checks = []
for _ in range(64):
    rho = float(rng.uniform(0.0, 1.8))
    phi = rng.normal() + 1j * rng.normal()
    radius = abs(phi) ** 2
    F = family_curvature(rho, phi)
    traced = normalized_trace(F.conj().T @ F).real
    formula = (
        (1.0 - rho**2) ** 2
        + (rho**2 - radius) ** 2
        + (radius - 1.0) ** 2
    ) / 10.0 * 3.0
    radial_checks.append(abs(traced - formula))
assert max(radial_checks) < TOL

result = {
    "gate": "version5_commuting_square_readout_gate",
    "recovered_architecture": {
        "ambient_parent_algebra": "B(H_fam tensor H_obs)=M300(C)",
        "ambient_is_not_coordinate_algebra": True,
        "family_factor_dimension": family_dimension,
        "observed_factor_dimension": observed_dimension,
        "total_dimension": total_dimension,
        "family_reading": "B(H_fam) tensor I15",
        "observed_reading": "I20 tensor B(H_obs)",
        "intersection": "C I300",
    },
    "conditional_expectations": {
        "E_family": "id tensor tau15",
        "E_observed": "tau20 tensor id",
        "residuals": expectation_residuals,
        "unique_trace_preserving_factor_expectations": True,
        "old_module_origin_obstruction_resolved": True,
    },
    "one_trace_orthogonality": {
        "family_curvature_trace": float(np.real(family_trace)),
        "family_observed_cross_term": float(np.real(cross_term)),
        "norm_decomposition_residual": float(norm_decomposition_residual),
        "factor_norm_residuals": factor_norm_residuals,
        "independent_relative_weight": False,
        "formula": "tau300((F_fam tensor I+I tensor F_obs)^2)=tau20(F_fam^2)+tau15(F_obs^2)",
    },
    "equivariant_field_content": {
        "Hom_S4(C4_triplet,C3_triplet)_dimension": full_intertwiner_dimension,
        "Hom_A4(C4_triplet,C3_triplet)_dimension": a4_intertwiner_dimension,
        "End_A4(C3_triplet)_dimension": a4_endomorphism_dimension,
        "left_arrow": "X=rho V",
        "right_arrow": "Y=Phi I3",
        "continuous_family_orientation_fields": 0,
        "previous_three_SO3_zero_modes_are_declared_fields": False,
        "interpretation": "global triplet rotations are presentation equivalences or violate the fixed A4/S4 intertwiner space",
    },
    "restricted_Hodge_functional": {
        "potential": "(1-rho^2)^2+(rho^2-|Phi|^2)^2+(|Phi|^2-1)^2",
        "maximum_trace_formula_residual": float(max(radial_checks)),
        "zero_momentum_vacuum": {
            "rho_squared": "1",
            "abs_Phi_squared": "1",
            "Hessian_spectrum_rho_RePhi_ImPhi": ["24", "8", "0"],
        },
        "unit_momentum_vacuum": {
            "rho_squared": "5/6",
            "abs_Phi_squared": "2/3",
            "energy": "5/6",
            "Hessian_spectrum_rho_RePhi_ImPhi": [
                "12-4sqrt(21)/3",
                "12+4sqrt(21)/3",
                "0",
            ],
        },
        "rotational_zero_modes": 0,
        "remaining_phase_zero_mode": 1,
    },
    "remaining_boundaries": {
        "observed_subalgebra_reduced_from_B15_to_exact_SM_bimodule": False,
        "family_to_Yukawa_reading_map_derived": False,
        "Phi_phase_charge_or_topological_fix_derived_in_same_square": False,
        "full_BV_BRST_complex": False,
        "blind_observables_closed": False,
    },
    "verdict": {
        "two_readings_one_parent_trace": "pass",
        "module_origin_for_old_conditional_expectation_gate": "pass",
        "no_relative_sector_weight": "pass",
        "equivariant_field_restriction_removes_fake_SO3_modes": "pass",
        "single_coordinate_algebra_required": False,
        "physical_closure": False,
        "status": "commuting_square_recovers_simple_two_reading_parent_architecture",
    },
    "next_gate": (
        "Replace the observed B(C15) control factor by the exact Standard Model "
        "bimodule algebra and test whether the existing state-anchored conditional "
        "map and Wilson/defect phase readouts arise as compatible corners of the "
        "same commuting square, without a new coefficient."
    ),
}

OUTPUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))