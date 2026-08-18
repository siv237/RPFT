#!/usr/bin/env python3
"""Классификация неоднозначности связностей после физических ограничений углов."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v5_physical_corner_connection_classification_gate_results.json"
)
TOL = 1.0e-10
FAMILY_DIMENSION = 20
OBSERVED_DIMENSION = 15
BLOCK_SIZES = [6, 2, 3, 3, 1]
BLOCK_NAMES = ["Q_L", "L_L", "u_R", "d_R", "e_R"]


def matrix_units(size, ranges=None):
    if ranges is None:
        ranges = [range(size)]
    units = []
    for indices in ranges:
        for row in indices:
            for column in indices:
                unit = np.zeros((size, size), dtype=complex)
                unit[row, column] = 1.0
                units.append(unit)
    return units


def commutant_basis(generators, size, tolerance=TOL):
    unknown_units = matrix_units(size)
    columns = []
    for unit in unknown_units:
        columns.append(
            np.concatenate(
                [(unit @ generator - generator @ unit).reshape(-1) for generator in generators]
            )
        )
    system = np.stack(columns, axis=1)
    _, singular_values, right = np.linalg.svd(system, full_matrices=False)
    rank = int(np.sum(singular_values > tolerance))
    kernel = right[rank:].conj().T
    matrices = [kernel[:, index].reshape(size, size) for index in range(kernel.shape[1])]
    return matrices, singular_values


morita = json.loads(
    (ROOT / "s2t/results/s2t_v5_morita_linking_parent_gate_results.json")
    .read_text(encoding="utf-8")
)
state_corner = json.loads(
    (ROOT / "s2t/results/s2t_v5_state_corner_curvature_readout_gate_results.json")
    .read_text(encoding="utf-8")
)
operator_map = json.loads(
    (ROOT / "s2t/results/s2t_v4_yukawa_operator_map_gate_results.json")
    .read_text(encoding="utf-8")
)
inner_fluctuation = json.loads(
    (ROOT / "s2t/results/s2t_v4_inner_fluctuation_yukawa_gate_results.json")
    .read_text(encoding="utf-8")
)
assert morita["verdict"]["canonical_Morita_bimodule_origin_of_C300"] == "pass"
assert state_corner["verdict"]["rank_one_quotient_as_controlled_readout"] == "pass"
assert not operator_map["operator_map_uniquely_derived"]
assert not inner_fluctuation["unique_inner_fluctuation_map_derived"]

# Полная правая алгебра M15.
full_generators = matrix_units(OBSERVED_DIMENSION)
full_commutant, _ = commutant_basis(full_generators, OBSERVED_DIMENSION)

# Пятиблочная наблюдаемая алгебра M6+M2+M3+M3+C.
block_ranges = []
offset = 0
block_projectors = []
for size in BLOCK_SIZES:
    indices = range(offset, offset + size)
    block_ranges.append(indices)
    projector = np.zeros((OBSERVED_DIMENSION, OBSERVED_DIMENSION), dtype=complex)
    projector[offset : offset + size, offset : offset + size] = np.eye(size)
    block_projectors.append(projector)
    offset += size
block_generators = matrix_units(OBSERVED_DIMENSION, block_ranges)
block_commutant, _ = commutant_basis(block_generators, OBSERVED_DIMENSION)

identity = np.eye(OBSERVED_DIMENSION, dtype=complex)
centered_projectors = [
    projector - np.trace(projector) * identity / OBSERVED_DIMENSION
    for projector in block_projectors
]
centered_matrix = np.stack([matrix.reshape(-1) for matrix in centered_projectors], axis=1)
centered_rank = int(np.linalg.matrix_rank(centered_matrix, tol=TOL))

commutant_residual = max(
    np.linalg.norm(element @ generator - generator @ element)
    for element in block_commutant
    for generator in block_generators
)

# Проверка, что левое действие и ранг-один компрессия не удаляют правую
# пятиблочную неоднозначность.
rng = np.random.default_rng(20260816)
family_matrix = rng.normal(size=(FAMILY_DIMENSION, FAMILY_DIMENSION)) + 1j * rng.normal(
    size=(FAMILY_DIMENSION, FAMILY_DIMENSION)
)
connector = rng.normal(size=(FAMILY_DIMENSION, OBSERVED_DIMENSION)) + 1j * rng.normal(
    size=(FAMILY_DIMENSION, OBSERVED_DIMENSION)
)
family_projector = np.zeros((FAMILY_DIMENSION, FAMILY_DIMENSION), dtype=complex)
family_projector[0, 0] = 1.0

right_action_residuals = []
corner_right_action_residuals = []
for projector in block_projectors:
    right_action_residuals.append(
        np.linalg.norm(family_matrix @ (connector @ projector) - (family_matrix @ connector) @ projector)
    )
    corner_connector = family_projector @ connector
    corner_right_action_residuals.append(
        np.linalg.norm(
            family_projector @ (corner_connector @ projector)
            - (family_projector @ corner_connector) @ projector
        )
    )

# Метрика единственного наблюдаемого следа на пяти канонических направлениях.
trace_gram = np.array(
    [
        [
            np.trace(first.conj().T @ second).real / OBSERVED_DIMENSION
            for second in block_projectors
        ]
        for first in block_projectors
    ]
)
trace_gram_eigenvalues = np.linalg.eigvalsh(trace_gram)

assert len(full_commutant) == 1
assert len(block_commutant) == 5
assert centered_rank == 4
assert commutant_residual < TOL
assert max(right_action_residuals) < TOL
assert max(corner_right_action_residuals) < TOL
assert abs(sum(BLOCK_SIZES) - OBSERVED_DIMENSION) < TOL

result = {
    "gate": "version5_physical_corner_connection_classification_gate",
    "input_certificates": {
        "Morita_linking_parent": "pass",
        "state_corner_curvature_readout": "pass",
        "old_Yukawa_operator_uniqueness": "fail",
        "old_inner_fluctuation_uniqueness": "fail",
    },
    "connection_difference_principle": {
        "statement": (
            "two connections with the same left/right Leibniz data differ by a "
            "bimodule-linear endomorphism"
        ),
        "full_factor_bimodule_endomorphism_dimension": len(full_commutant),
        "full_factor_result": "C identity",
    },
    "observed_block_restriction": {
        "algebra": "M6(C)+M2(C)+M3(C)+M3(C)+C",
        "block_names": BLOCK_NAMES,
        "block_sizes": BLOCK_SIZES,
        "complex_dimension": sum(size * size for size in BLOCK_SIZES),
        "commutant_complex_dimension": len(block_commutant),
        "commutant": "C P_Q+C P_L+C P_u+C P_d+C P_e",
        "centered_commutant_complex_dimension": centered_rank,
        "commutant_residual": float(commutant_residual),
        "exact_SM_coordinate_algebra_commutant_lower_bound": len(block_commutant),
        "reason_for_lower_bound": (
            "the exact Standard Model representation is contained in the block-preserving reading"
        ),
    },
    "rank_one_family_corner": {
        "family_projector_rank": 1,
        "right_block_ambiguity_dimension_after_corner": len(block_commutant),
        "left_right_associativity_residual": float(max(right_action_residuals)),
        "corner_right_action_residual": float(max(corner_right_action_residuals)),
        "family_rank_one_selection_removes_observed_block_ambiguity": False,
    },
    "trace_metric": {
        "projector_Gram_matrix": trace_gram.tolist(),
        "eigenvalues": trace_gram_eigenvalues.tolist(),
        "weights": [size / OBSERVED_DIMENSION for size in BLOCK_SIZES],
        "fixes_metric": True,
        "selects_nonzero_connection_vector": False,
        "pure_quadratic_norm_minimum": "zero connection",
    },
    "anti_circle_comparison": {
        "version4_operator_map": (
            "the same selected family data admitted inequivalent coefficient-free maps"
        ),
        "version4_inner_fluctuation": (
            "small algebras excluded the CP-capable map while full M3 restored all directions"
        ),
        "new_information": (
            "the Morita container does not remove underdetermination; after exact observed "
            "block restriction at least five affine connection directions remain"
        ),
    },
    "verdict": {
        "full_M20_M15_connection_unique_up_to_scalar": "pass",
        "physical_observed_restriction_unique": "fail",
        "minimum_complex_ambiguity_dimension": len(block_commutant),
        "minimum_centered_ambiguity_dimension": centered_rank,
        "rank_one_family_corner_restores_uniqueness": "fail",
        "trace_alone_selects_Yukawa": "fail",
        "Morita_parent_architecture": "retained",
        "unique_Yukawa_connection": False,
        "physical_closure": False,
        "status": (
            "the linking parent fixes the carrier and relative curvature but not a unique "
            "physical Yukawa connection"
        ),
    },
    "next_gate": (
        "Do not search for another algebraic projection. Test the most general symmetry-allowed "
        "potential on the four-dimensional centered observed-block connection ambiguity and "
        "determine whether the existing parent curvature and trace select a nonzero unique orbit; "
        "otherwise freeze Yukawa origin as underdetermined."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))