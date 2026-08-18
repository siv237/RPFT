#!/usr/bin/env python3
"""Коммутантное размещение семейной цепи и обычное исчисление одноформ."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_sm_family_commutant_calculus_gate_results.json"
TOL = 1.0e-10

affine = json.loads(
    (ROOT / "s2t/results/s2t_v5_affine_ko6_reference_corner_gate_results.json")
    .read_text(encoding="utf-8")
)
algebra_menu = json.loads(
    (ROOT / "s2t/results/s2t_v4_finite_algebra_menu_gate_results.json")
    .read_text(encoding="utf-8")
)
multiplicity = json.loads(
    (ROOT / "s2t/results/s2t_v4_bimodule_multiplicity_gate_results.json")
    .read_text(encoding="utf-8")
)

assert affine["verdict"]["forgotten_affine_KO6_bimodule_recovered"] == "pass"
assert algebra_menu["selected_baseline"] == ["C", "H", "M3C"]
assert (
    multiplicity["no_right_neutrino_branch"]["minimal_dimension"] == 15
)


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def matrix_units(size):
    units = []
    for row in range(size):
        for column in range(size):
            unit = np.zeros((size, size), dtype=complex)
            unit[row, column] = 1.0
            units.append(unit)
    return units


def complex_span_rank(matrices):
    if not matrices:
        return 0
    columns = np.column_stack([matrix.reshape(-1) for matrix in matrices])
    return int(np.linalg.matrix_rank(columns, tol=TOL))


# Контрольное верное представление конечномерной полупростой алгебры на C^15.
# Оно не подменяет стандарт-модельный бимодуль: проверяемое ниже тождество
# справедливо для любого представления и любого наблюдаемого оператора Дирака.
observed_basis = []
for unit in matrix_units(2):
    observed_basis.append(block_diagonal([unit, np.zeros((3, 3)), np.zeros((10, 10))]))
for unit in matrix_units(3):
    observed_basis.append(block_diagonal([np.zeros((2, 2)), unit, np.zeros((10, 10))]))
observed_basis.append(block_diagonal([np.zeros((2, 2)), np.zeros((3, 3)), np.eye(10)]))

rng = np.random.default_rng(20260816)
raw_observed = rng.normal(size=(15, 15)) + 1j * rng.normal(size=(15, 15))
D_observed = raw_observed + raw_observed.conj().T

# Частичная семейная цепь 4 -> 3 -> 3 из предыдущего сертификата.
V = np.array(
    [
        [1.0, -1.0, 0.0, 0.0],
        [1.0, 1.0, -2.0, 0.0],
        [1.0, 1.0, 1.0, -3.0],
    ]
)
V /= np.linalg.norm(V, axis=1)[:, None]
zero4 = np.zeros((4, 4), dtype=complex)
zero3 = np.zeros((3, 3), dtype=complex)
zero43 = np.zeros((4, 3), dtype=complex)
zero34 = np.zeros((3, 4), dtype=complex)


def family_dirac(rho, phi):
    X = rho * V
    Y = phi * np.eye(3)
    return np.block(
        [
            [zero4, X.T, zero43],
            [X, zero3, Y.conj().T],
            [zero34, Y, zero3],
        ]
    )


D_family_1 = family_dirac(0.83, 0.61 + 0.20j)
D_family_2 = family_dirac(1.17, -0.28 + 0.49j)
I_family = np.eye(10)
I_observed = np.eye(15)

represented = [np.kron(I_family, item) for item in observed_basis]
D_total_1 = np.kron(D_family_1, I_observed) + np.kron(I_family, D_observed)
D_total_2 = np.kron(D_family_2, I_observed) + np.kron(I_family, D_observed)

family_commutator_residual = max(
    np.linalg.norm(
        np.kron(D_family_1, I_observed) @ item
        - item @ np.kron(D_family_1, I_observed)
    )
    for item in represented
)
factorization_residual = max(
    np.linalg.norm(
        D_total_1 @ total_a
        - total_a @ D_total_1
        - np.kron(I_family, D_observed @ a - a @ D_observed)
    )
    for total_a, a in zip(represented, observed_basis)
)
family_change_residual = max(
    np.linalg.norm(
        (D_total_1 @ item - item @ D_total_1)
        - (D_total_2 @ item - item @ D_total_2)
    )
    for item in represented
)
assert max(
    family_commutator_residual,
    factorization_residual,
    family_change_residual,
) < TOL

observed_one_forms = []
total_one_forms = []
for a in observed_basis:
    for b in observed_basis:
        one_form = a @ (D_observed @ b - b @ D_observed)
        observed_one_forms.append(one_form)
        total_one_forms.append(np.kron(I_family, one_form))

observed_one_form_rank = complex_span_rank(observed_one_forms)
total_one_form_rank = complex_span_rank(total_one_forms)
assert observed_one_form_rank == total_one_form_rank

# Калибровочные направления не размножаются при представлении I_K tensor g.
observed_algebra_rank = complex_span_rank(observed_basis)
replicated_algebra_rank = complex_span_rank(represented)
assert observed_algebra_rank == replicated_algebra_rank == 14

# Две альтернативы, которые необходимо исключить до введения нового языка.
direct_sum_central_product_norm = float(
    np.linalg.norm(
        np.block(
            [
                [np.eye(2), np.zeros((2, 3))],
                [np.zeros((3, 2)), np.zeros((3, 3))],
            ]
        )
        @ np.block(
            [
                [np.zeros((2, 2)), np.zeros((2, 3))],
                [np.zeros((3, 2)), np.eye(3)],
            ]
        )
    )
)
assert direct_sum_central_product_norm < TOL

separate_family_color_lie_dimension = 3 + 9  # so(3) + u(3)
tensor_family_color_lie_dimension = 9**2  # u(9)
tensor_extra_generators = (
    tensor_family_color_lie_dimension - separate_family_color_lie_dimension
)
assert tensor_extra_generators == 69

result = {
    "gate": "version5_sm_family_commutant_calculus_gate",
    "inputs": {
        "coordinate_algebra": "A_SM=C+H+M3(C)",
        "observed_particle_multiplicity": 15,
        "family_particle_dimension": 10,
        "full_KO6_product_dimension": 300,
        "standard_model_gauge_lie_dimension_after_unimodularity": 12,
        "control_representation": "M2(C)+M3(C)+C on C^15",
        "control_is_not_claimed_as_the_SM_bimodule": True,
    },
    "commutant_placement": {
        "representation": "pi(a)=I_10 tensor pi_SM(a)",
        "dirac": "D=D_fam tensor I_15 + I_10 tensor D_SM",
        "family_commutator_residual": float(family_commutator_residual),
        "commutator_factorization_residual": float(factorization_residual),
        "family_change_sensitivity_residual": float(family_change_residual),
        "gauge_algebra_dimension_preserved": True,
        "observed_control_algebra_span_rank": observed_algebra_rank,
        "replicated_control_algebra_span_rank": replicated_algebra_rank,
    },
    "ordinary_one_form_calculus": {
        "identity": "[D,pi(a)]=I_10 tensor [D_SM,pi_SM(a)]",
        "observed_control_one_form_span_rank": observed_one_form_rank,
        "total_control_one_form_span_rank": total_one_form_rank,
        "family_dirac_changes_one_forms": False,
        "family_chain_visible_to_ordinary_inner_fluctuations": False,
    },
    "architecture_trilemma": {
        "direct_sum": {
            "central_idempotent_product_norm": direct_sum_central_product_norm,
            "jointly_charged_irreducible_sector": False,
            "verdict": "fail_by_central_decomposition",
        },
        "naive_tensor_product": {
            "witness": "M3(R) tensor_R M3(C) is M9(C)",
            "separate_so3_plus_u3_lie_dimension": separate_family_color_lie_dimension,
            "tensor_u9_lie_dimension": tensor_family_color_lie_dimension,
            "extra_generators": tensor_extra_generators,
            "verdict": "fail_by_gauge_enlargement",
        },
        "commutant": {
            "standard_model_gauge_algebra_preserved": True,
            "ordinary_family_one_forms_generated": False,
            "verdict": "kinematic_pass_differential_origin_fail",
        },
    },
    "surviving_route": {
        "type": "graded correspondence or superconnection over A_SM",
        "family_differential_must_be_additional_morphism_data": True,
        "ordinary_single_spectral_triple_already_obtained": False,
        "required_next_checks": [
            "graded Leibniz rule",
            "KO6 reality and grading",
            "gauge covariance",
            "one common positive trace on C300",
            "scalar kinetic normalization",
            "BV/BRST complex",
        ],
    },
    "verdict": {
        "SM_coordinate_algebra_with_family_in_commutant": "kinematic_pass",
        "ordinary_Connes_calculus_produces_family_chain": "fail",
        "direct_sum_solution": "fail",
        "naive_tensor_product_solution": "fail",
        "graded_correspondence_branch": "open",
        "physical_closure": False,
        "status": "commutant_preserves_gauge_but_is_invisible_to_ordinary_one_forms",
    },
    "next_gate": (
        "Define the affine family chain as a graded correspondence connection over "
        "A_SM and test its Leibniz rule, KO6 covariance, common tau300 curvature, "
        "scalar kinetic normalization and BV/BRST complex."
    ),
}

OUTPUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))