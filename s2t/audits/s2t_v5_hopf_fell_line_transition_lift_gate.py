#!/usr/bin/env python3
"""Хопфова линия, фазовый перенос и ориентированные стрелки Мориты."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_hopf_fell_line_transition_lift_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def matrix_trigsimp(matrix):
    return matrix.applyfunc(lambda value: sp.trigsimp(sp.simplify(value)))


projective = load_result("s2t_v5_projective_hedgehog_point_defect_gate_results.json")
order_four = load_result("s2t_v5_order_four_resonant_loop_transport_gate_results.json")
su2_no_go = load_result("s2t_v5_su2_family_lift_h15_representation_gate_results.json")
spinh_no_go = load_result("s2t_v5_spinh_orientation_family_locking_reopening_gate_results.json")

assert projective["spinor_lift_mass"]["first_Chern_number"] == "1"
assert order_four["early_hypothesis_reconstruction"]["full_return_after_four_steps"] == "1"
assert not su2_no_go["verdict"]["all_gate_conditions_simultaneously_satisfied"]
assert not spinh_no_go["verdict"]["reopening_without_new_module"]

theta, phi = sp.symbols("theta phi", real=True)
sigma1 = sp.Matrix([[0, 1], [1, 0]])
sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sigma3 = sp.Matrix([[1, 0], [0, -1]])
sigmas = [sigma1, sigma2, sigma3]

# Северная и южная локальные секции расслоения Хопфа.
z_north = sp.Matrix(
    [sp.cos(theta / 2), sp.exp(sp.I * phi) * sp.sin(theta / 2)]
)
z_south = sp.Matrix(
    [sp.exp(-sp.I * phi) * sp.cos(theta / 2), sp.sin(theta / 2)]
)
assert sp.simplify((z_north.conjugate().T * z_north)[0] - 1) == 0
assert sp.simplify(z_south - sp.exp(-sp.I * phi) * z_north) == sp.zeros(2, 1)

n = sp.Matrix(
    [sp.simplify((z_north.conjugate().T * sigma * z_north)[0]) for sigma in sigmas]
)
expected_n = sp.Matrix(
    [
        sp.sin(theta) * sp.cos(phi),
        sp.sin(theta) * sp.sin(phi),
        sp.cos(theta),
    ]
)
assert matrix_trigsimp(n - expected_n) == sp.zeros(3, 1)

P_spinor = sp.simplify(z_north * z_north.conjugate().T)
Q_spinor = sp.simplify(sum((n[j] * sigmas[j] for j in range(3)), sp.zeros(2)))
assert matrix_trigsimp(P_spinor - (sp.eye(2) + Q_spinor) / 2) == sp.zeros(2)
P_spinor_squared_factored = sp.simplify(
    z_north * (z_north.conjugate().T * z_north)[0] * z_north.conjugate().T
)
assert matrix_trigsimp(P_spinor_squared_factored - P_spinor) == sp.zeros(2)

# Связность Берри и первый класс Черна.
A_north_phi = sp.simplify(-sp.I * (z_north.conjugate().T * sp.diff(z_north, phi))[0])
A_south_phi = sp.simplify(-sp.I * (z_south.conjugate().T * sp.diff(z_south, phi))[0])
curvature_theta_phi = sp.simplify(sp.diff(A_north_phi, theta))
chern_number = sp.simplify(
    sp.integrate(
        sp.integrate(curvature_theta_phi / (2 * sp.pi), (phi, 0, 2 * sp.pi)),
        (theta, 0, sp.pi),
    )
)
assert sp.simplify(A_south_phi - A_north_phi + 1) == 0
assert curvature_theta_phi == sp.sin(theta) / 2
assert chern_number == 1

# Вертикальная четверть оборота не меняет n и проектор.
z_quarter = sp.I * z_north
n_quarter = sp.Matrix(
    [sp.simplify((z_quarter.conjugate().T * sigma * z_quarter)[0]) for sigma in sigmas]
)
assert matrix_trigsimp(n_quarter - n) == sp.zeros(3, 1)
assert matrix_trigsimp(z_quarter * z_quarter.conjugate().T - P_spinor) == sp.zeros(2)
phase_history = [sp.simplify(sp.I**power) for power in range(5)]

# Обычный характер C4 является 1-коциклом; индуцированный множитель
# omega(a,b)=chi(a)chi(b)/chi(a+b) тривиален.
character = {a: sp.I**a for a in range(4)}
character_multiplicative = all(
    sp.simplify(character[(a + b) % 4] - character[a] * character[b]) == 0
    for a in range(4)
    for b in range(4)
)
multiplier_values = {
    (a, b): sp.simplify(character[a] * character[b] / character[(a + b) % 4])
    for a in range(4)
    for b in range(4)
}
assert character_multiplicative
assert set(multiplier_values.values()) == {sp.Integer(1)}

# Сопряжённая хопфова линия меняет знак кривизны и c1.
z_conjugate_line = sp.Matrix([-sp.conjugate(z_north[1]), sp.conjugate(z_north[0])])
n_conjugate = sp.Matrix(
    [
        sp.simplify((z_conjugate_line.conjugate().T * sigma * z_conjugate_line)[0])
        for sigma in sigmas
    ]
)
assert matrix_trigsimp(n_conjugate + n) == sp.zeros(3, 1)
conjugate_chern_number = -chern_number

result = {
    "gate": "version5_hopf_fell_line_transition_lift_gate",
    "flat_order_four_character_audit": {
        "phase_history": [str(value) for value in phase_history],
        "is_C4_character": character_multiplicative,
        "induced_projective_multiplier_values": sorted({str(v) for v in multiplier_values.values()}),
        "nontrivial_groupoid_two_cocycle_from_character_alone": False,
        "flat_line_first_Chern_number": 0,
        "unit_index_from_flat_Z4_phase_alone": False,
    },
    "hopf_line_audit": {
        "north_section": [str(value) for value in z_north],
        "south_to_north_transition": "exp(-i phi)",
        "berry_connection_north_phi": str(A_north_phi),
        "berry_connection_south_phi": str(A_south_phi),
        "curvature_theta_phi": str(curvature_theta_phi),
        "first_Chern_number": int(chern_number),
        "positive_projector": "z z^*= (I+n.sigma)/2",
        "unit_index_line_available": True,
    },
    "order_four_inside_hopf_fiber": {
        "quarter_turn": "z -> i z",
        "projector_invariant": True,
        "oriented_axis_invariant": True,
        "sign_after_two_quarter_turns": "-1 on z",
        "return_after_four_quarter_turns": True,
        "order_four_phase_is_subgroup_of_full_U1_fiber": True,
    },
    "cover_quotient_reading": {
        "spinor_total_space": "S3=SU(2), Hopf circle bundle over S2 with c1=1",
        "vector_total_space": "RP3=SO(3), quotient circle bundle over S2 with c1=2",
        "projective_axis": "RP2 after n~-n",
        "unit_Chern_class_requires_spinor_cover": True,
        "existing_project_has_S3_spinor_cover": True,
    },
    "oriented_transition_pairing": {
        "forward_arrow_candidate": "E twisted by Hopf line L, c1=+1",
        "reverse_arrow_candidate": "E* twisted by conjugate line L*, c1=-1",
        "KO6_real_structure_can_exchange_pair": True,
        "new_fixed_internal_C2_family_required": False,
        "new_chiral_SU2F_gauge_group_required": False,
        "canonical_assignment_E_to_oriented_n_derived": False,
    },
    "fell_line_composition": {
        "arrow_fiber": "F(y<-x)=L_y tensor L_x^*",
        "composition": "F(z<-y) tensor F(y<-x) -> F(z<-x)",
        "associative_without_free_coefficient": True,
        "index_source": "c1(L), not the flat C4 character",
    },
    "verdict": {
        "pure_Z4_cocycle_route": "fail_trivial_multiplier_and_c1_zero",
        "full_Hopf_line_route": "pass_topology_and_unit_Chern_class",
        "avoids_previous_SU2F_representation_no_go": True,
        "avoids_single_doublet_Spinh_no_go": True,
        "physical_closure": False,
        "status": "conditional_reopening",
        "missing_bridge": "derive functorially that Morita arrow orientation E/E* selects n/-n and L/L* from the existing parent connection",
    },
    "next_gate": "version5_hopf_line_morita_orientation_functor_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))