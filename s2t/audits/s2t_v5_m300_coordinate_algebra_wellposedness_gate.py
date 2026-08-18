#!/usr/bin/env python3
"""Проверка корректности постановки комплекса одноформ на носителе M300."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "s2t/results/s2t_v5_m300_coordinate_algebra_wellposedness_gate_results.json"
)
TOL = 1.0e-10

hessian = json.loads(
    (
        ROOT
        / "s2t/results/s2t_v5_m300_hodge_curvature_hessian_gate_results.json"
    ).read_text(encoding="utf-8")
)
assert hessian["verdict"]["one_trace_Hodge_curvature_action_candidate"] == "pass"


def matrix_units(size):
    units = []
    for row in range(size):
        for column in range(size):
            unit = np.zeros((size, size), dtype=complex)
            unit[row, column] = 1.0
            units.append(unit)
    return units


def complex_span_rank(matrices):
    columns = np.stack([matrix.reshape(-1) for matrix in matrices], axis=1)
    return int(np.linalg.matrix_rank(columns, tol=TOL))


def represented_one_forms(algebra_basis, dirac):
    forms = []
    for left in algebra_basis:
        for right in algebra_basis:
            forms.append(left @ (dirac @ right - right @ dirac))
    return forms


def projected_span_rank(matrices, mask):
    projected = [matrix[mask].reshape(-1) for matrix in matrices]
    columns = np.stack(projected, axis=1)
    return int(np.linalg.matrix_rank(columns, tol=TOL))


# Минимальный аналог амальгамированного частичного носителя:
# одна опорная вершина и цепь L--G--R. Оператор Дирака не связывает опору
# с цепью, как в текущей конструкции M300.
size = 4
dirac = np.array(
    [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.83, 0.0],
        [0.0, 0.83, 0.0, 0.61],
        [0.0, 0.0, 0.61, 0.0],
    ],
    dtype=complex,
)

# Завершение A: диагональная координатная алгебра C^4.
diagonal_basis = []
for index in range(size):
    projector = np.zeros((size, size), dtype=complex)
    projector[index, index] = 1.0
    diagonal_basis.append(projector)
diagonal_forms = represented_one_forms(diagonal_basis, dirac)

# Завершение B: полная координатная алгебра M4(C).
full_basis = matrix_units(size)
full_forms = represented_one_forms(full_basis, dirac)

reference_chain_mask = np.zeros((size, size), dtype=bool)
reference_chain_mask[0, 1:] = True
reference_chain_mask[1:, 0] = True

diagonal_one_rank = complex_span_rank(diagonal_forms)
full_one_rank = complex_span_rank(full_forms)
diagonal_reference_chain_rank = projected_span_rank(
    diagonal_forms, reference_chain_mask
)
full_reference_chain_rank = projected_span_rank(full_forms, reference_chain_mask)

assert diagonal_one_rank == 4
assert full_one_rank == size**2
assert diagonal_reference_chain_rank == 0
assert full_reference_chain_rank == 2 * (size - 1)

# Коммутант определяющего представления M4(C): решаем линейную систему
# [Z,E_ij]=0. Его комплексная размерность должна быть один.
constraints = []
for unit in full_basis:
    columns = []
    for variable in full_basis:
        columns.append((variable @ unit - unit @ variable).reshape(-1))
    constraints.append(np.stack(columns, axis=1))
constraint_matrix = np.concatenate(constraints, axis=0)
commutant_dimension = size**2 - int(
    np.linalg.matrix_rank(constraint_matrix, tol=TOL)
)
assert commutant_dimension == 1

# Точные размерностные следствия для n=300.
n = 300
full_m300_one_form_complex_rank = n**2
full_m300_selfadjoint_real_dimension = n**2
full_m300_projective_gauge_lie_dimension = n**2 - 1
minimal_faithful_m300_bimodule_complex_dimension = n**2
current_carrier_complex_dimension = n

result = {
    "date": "2026-08-16",
    "gate": "version5_m300_coordinate_algebra_wellposedness_gate",
    "input_certificate": {
        "M300_chain_action_and_connector_Hessian": "pass",
    },
    "wellposedness_issue": {
        "carrier_algebra": "B(H_parent)=M300(C)",
        "coordinate_algebra_specified": False,
        "representation_pi_specified_on_all_300_states": False,
        "opposite_representation_specified_on_all_300_states": False,
        "full_Dirac_seed_on_reference_chain_blocks_specified": False,
        "finding": (
            "A trace carrier does not by itself define represented one-forms. "
            "Omega_D^1 requires a coordinate algebra, its representation and D."
        ),
    },
    "full_matrix_coordinate_interpretation": {
        "coordinate_algebra": "M300(C) in its defining representation on C300",
        "commutant_dimension": 1,
        "faithful_noncommutative_opposite_action_possible": False,
        "represented_one_form_complex_rank_for_nonscalar_D": (
            full_m300_one_form_complex_rank
        ),
        "selfadjoint_fluctuation_real_dimension": (
            full_m300_selfadjoint_real_dimension
        ),
        "projective_gauge_lie_dimension": (
            full_m300_projective_gauge_lie_dimension
        ),
        "minimal_faithful_left_right_bimodule_complex_dimension": (
            minimal_faithful_m300_bimodule_complex_dimension
        ),
        "current_carrier_complex_dimension": current_carrier_complex_dimension,
        "verdict": "fails_real_spectral_triple_and_minimal_field_content",
    },
    "same_trace_same_D_two_calculi_witness": {
        "toy_carrier": "C4 with one reference node and an A3 chain",
        "same_normalized_matrix_trace": True,
        "same_Dirac_operator": True,
        "diagonal_coordinate_algebra": {
            "algebra": "C^4",
            "represented_one_form_complex_rank": diagonal_one_rank,
            "reference_chain_mixing_rank": diagonal_reference_chain_rank,
        },
        "full_coordinate_algebra": {
            "algebra": "M4(C)",
            "represented_one_form_complex_rank": full_one_rank,
            "reference_chain_mixing_rank": full_reference_chain_rank,
        },
        "conclusion": (
            "The normalized carrier trace and the same D do not determine the "
            "differential calculus or reference-chain mixing fields."
        ),
    },
    "status_of_previous_action": {
        "chain_sector_identity": "retained",
        "connector_Hessian": "retained_conditionally_on_the_restricted_calculus",
        "claim_of_full_M300_one_form_Hessian": "not_well_posed_yet",
    },
    "verdict": {
        "M300_as_unique_trace_carrier": "pass",
        "M300_as_coordinate_algebra_on_C300": "fail",
        "full_one_form_classification_from_existing_data": False,
        "physical_closure": False,
        "status": "coordinate_algebra_and_bimodule_data_missing",
    },
    "next_gate": (
        "Specify the minimal coordinate algebra A_coord, its faithful left/right "
        "bimodule representation, J, grading and full Dirac support on H300. Then "
        "compute Omega_D^1(A_coord), degree-two junk and the BV/BRST quotient."
    ),
}

OUTPUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))