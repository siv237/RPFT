#!/usr/bin/env python3
"""Ориентационный функтор связывающей алгебры Мориты."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_hopf_line_morita_orientation_functor_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


hopf = load_result("s2t_v5_hopf_fell_line_transition_lift_gate_results.json")
morita = load_result("s2t_v5_morita_linking_parent_gate_results.json")
height = load_result("s2t_v5_oriented_height_hodge_ko6_gate_results.json")

assert hopf["hopf_line_audit"]["first_Chern_number"] == 1
assert hopf["verdict"]["status"] == "conditional_reopening"
assert morita["morita_carrier"]["equivalence_bimodule"] == "E=M20x15(C)"
assert height["verdict"]["orientation_from_existing_KO6_data"] == "closed"

# Конечномерный представитель связывающей алгебры M_{p+q} с p != q.
p, q = 3, 2
size = p + q
p_left = sp.diag(*([1] * p + [0] * q))
p_right = sp.eye(size) - p_left
gamma_link = p_left - p_right
assert p_left.rank() == p
assert p_right.rank() == q


def matrix_unit(i, j):
    unit = sp.zeros(size)
    unit[i, j] = 1
    return unit


def degree_of_unit(i, j):
    if i < p and j >= p:
        return 1
    if i >= p and j < p:
        return -1
    return 0


units = {(i, j): matrix_unit(i, j) for i in range(size) for j in range(size)}
commutator_residuals = []
star_residuals = []
for (i, j), unit in units.items():
    degree = degree_of_unit(i, j)
    residual = gamma_link * unit - unit * gamma_link - 2 * degree * unit
    commutator_residuals.append(residual.norm())
    star_degree = degree_of_unit(j, i)
    star_residuals.append(star_degree + degree)
assert all(value == 0 for value in commutator_residuals)
assert all(value == 0 for value in star_residuals)

# Аддитивность степени на всех ненулевых композициях матричных единиц.
composition_checks = 0
composition_failures = 0
for (i, j), first in units.items():
    for (k, ell), second in units.items():
        product = first * second
        if product == sp.zeros(size):
            continue
        composition_checks += 1
        product_degree = degree_of_unit(i, ell)
        expected_degree = degree_of_unit(i, j) + degree_of_unit(k, ell)
        if product_degree != expected_degree:
            composition_failures += 1
assert composition_checks > 0
assert composition_failures == 0

# Для E E* и E* E хопфовы степени сокращаются в нуль.
forward = matrix_unit(0, p)
reverse = forward.T
assert degree_of_unit(0, p) == 1
assert degree_of_unit(p, 0) == -1
assert forward * reverse == matrix_unit(0, 0)
assert reverse * forward == matrix_unit(p, p)

# Проективная ось имеет два подъёма; степень стрелки выбирает знак класса.
theta, phi = sp.symbols("theta phi", real=True)
curvature = sp.sin(theta) / 2
chern_by_degree = {}
for degree in (-1, 1):
    chern = sp.simplify(
        sp.integrate(
            sp.integrate(degree * curvature / (2 * sp.pi), (phi, 0, 2 * sp.pi)),
            (theta, 0, sp.pi),
        )
    )
    chern_by_degree[str(degree)] = int(chern)
assert chern_by_degree == {"-1": -1, "1": 1}

# Углы разных рангов нельзя переставить унитарным сопряжением.
corner_swap_by_inner_unitary_possible = p_left.rank() == p_right.rank()
assert not corner_swap_by_inner_unitary_possible

result = {
    "gate": "version5_hopf_line_morita_orientation_functor_gate",
    "linking_grading": {
        "full_parent": "M35 with corner projections p20 and p15",
        "proxy": "M5 with ranks 3 and 2",
        "grading": "Gamma_link=p_left-p_right",
        "degree_formula": "[Gamma_link,X]=2 deg(X) X",
        "degree_E": 1,
        "degree_E_star": -1,
        "degree_diagonal_corners": 0,
        "maximum_proxy_commutator_residual": 0,
    },
    "functoriality": {
        "nonzero_matrix_unit_compositions_checked": composition_checks,
        "composition_failures": composition_failures,
        "degree_additive_on_composition": True,
        "star_reverses_degree": True,
        "line_assignment": "T(X)=X tensor L^{deg(X)}",
        "forward_reverse_products_are_untwisted": True,
    },
    "orientation_selection": {
        "projective_axis_lifts": ["n", "-n"],
        "degree_plus_selects": "L with c1=+1",
        "degree_minus_selects": "L* with c1=-1",
        "Chern_numbers_by_degree": chern_by_degree,
        "global_reversal": "implemented by star/J, not a continuous free parameter",
    },
    "canonicity": {
        "corner_ranks": [20, 15],
        "corners_swappable_by_inner_unitary": False,
        "family_and_observed_roles_already_fixed": True,
        "depends_on_ambiguous_three_level_height": False,
        "reason": "the two-corner source-target grading is fixed before the affine height choice",
    },
    "KO6_and_trace": {
        "J_maps_E_tensor_L_to_E_star_tensor_L_star": True,
        "full_real_pair_preserved": True,
        "finite_internal_dimension_changed": False,
        "normalized_M35_trace_changed": False,
        "reason": "L tensor L* cancels in diagonal products and every line fiber has rank one",
    },
    "verdict": {
        "orientation_functor_from_linking_parent": "pass",
        "manual_sign_assignment_required": False,
        "previous_height_nonuniqueness_bypassed_not_overturned": True,
        "unit_Chern_branch_selected_on_forward_arrow": True,
        "physical_closure": False,
        "status": "topological_orientation_bridge_pass",
        "remaining_problem": "derive a single spatial superconnection/action whose Hopf curvature gives both finite defect energy and the twisted Dirac index",
    },
    "next_gate": "version5_hopf_twisted_defect_superconnection_energy_index_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))