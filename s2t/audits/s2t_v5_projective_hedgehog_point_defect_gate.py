#!/usr/bin/env python3
"""Коразмерность, энергия и индекс проекторного семейного ежа."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_projective_hedgehog_point_defect_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


self_defect = load_result("s2t_v5_self_generated_transition_defect_gate_results.json")
projector_gate = load_result("s2t_v5_holonomy_projector_defect_multiplicity_gate_results.json")
root_menu = load_result("s2t_majorana_root_source_menu_results.json")
assert self_defect["analytic_kink"]["topological_charge"] == "1"
assert projector_gate["conditional_neutrino_rank_chain"]["combined_complex_rank"] == 1
assert root_menu["exhaustive_gate"]["existing_mandatory_root_sources"] == 0

theta, phi = sp.symbols("theta phi", real=True)
n = sp.Matrix(
    [
        sp.sin(theta) * sp.cos(phi),
        sp.sin(theta) * sp.sin(phi),
        sp.cos(theta),
    ]
)
assert sp.simplify((n.T * n)[0]) == 1

# Степень ориентированного подъёма ежа.
degree_density = sp.simplify(n.dot(sp.diff(n, theta).cross(sp.diff(n, phi))))
hedgehog_degree = sp.simplify(
    sp.integrate(
        sp.integrate(degree_density / (4 * sp.pi), (phi, 0, 2 * sp.pi)),
        (theta, 0, sp.pi),
    )
)
assert degree_density == sp.sin(theta)
assert hedgehog_degree == 1

# Ранг-один проектор P=n n^T и энергия глобального ежа.
P = sp.simplify(n * n.T)
assert sp.simplify(P**2 - P) == sp.zeros(3)
assert P.rank() == 1
angular_gradient = sp.simplify(
    sp.trace(sp.diff(P, theta).T * sp.diff(P, theta))
    + sp.trace(sp.diff(P, phi).T * sp.diff(P, phi)) / sp.sin(theta) ** 2
)
shell_energy_coefficient = sp.simplify(
    sp.integrate(
        sp.integrate(angular_gradient * sp.sin(theta) / 2, (phi, 0, 2 * sp.pi)),
        (theta, 0, sp.pi),
    )
)
assert angular_gradient == 4
assert shell_energy_coefficient == 8 * sp.pi

# Проекторная массовая матрица имеет сигнатуру (1,2), но её положительное
# собственное расслоение имеет нулевой Chern integrand.
Q_vector = sp.simplify(3 * P - sp.eye(3))
assert Q_vector.eigenvals() == {2: 1, -1: 2}
vector_chern_density = sp.simplify(
    sp.trace(P * (sp.diff(P, theta) * sp.diff(P, phi) - sp.diff(P, phi) * sp.diff(P, theta)))
)
assert vector_chern_density == 0
vector_chern_number = 0

# Спинорный подъём n.sigma имеет Hopf eigenline с c1=1.
sigma1 = sp.Matrix([[0, 1], [1, 0]])
sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sigma3 = sp.Matrix([[1, 0], [0, -1]])
Q_spinor = sp.simplify(n[0] * sigma1 + n[1] * sigma2 + n[2] * sigma3)
assert sp.simplify(Q_spinor**2 - sp.eye(2)) == sp.zeros(2)
P_plus = sp.simplify((sp.eye(2) + Q_spinor) / 2)
assert P_plus.rank() == 1
assert sp.simplify(P_plus**2 - P_plus) == sp.zeros(2)
spinor_chern_density = sp.simplify(
    sp.trace(
        P_plus
        * (
            sp.diff(P_plus, theta) * sp.diff(P_plus, phi)
            - sp.diff(P_plus, phi) * sp.diff(P_plus, theta)
        )
    )
)
spinor_chern_number = sp.simplify(
    sp.integrate(
        sp.integrate(spinor_chern_density / (2 * sp.pi * sp.I), (phi, 0, 2 * sp.pi)),
        (theta, 0, sp.pi),
    )
)
assert spinor_chern_density == sp.I * sp.sin(theta) / 2
assert spinor_chern_number == 1

# P теряет знак n, тогда как спинорная масса его сохраняет.
P_sign_defect = sp.simplify((-n) * (-n).T - P)
spinor_sign_sum = sp.simplify((-Q_spinor) + Q_spinor)
assert P_sign_defect == sp.zeros(3)
assert spinor_sign_sum == sp.zeros(2)

result = {
    "gate": "version5_projective_hedgehog_point_defect_gate",
    "codimension_audit": {
        "scalar_Z2_kink_in_one_space_dimension": "localized point",
        "same_Z2_defect_in_three_space_dimensions": "codimension-one domain wall",
        "point_particle_from_scalar_kink_in_3_plus_1": False,
        "minimal_SM_Higgs_vacuum_homotopy_type": "S3",
        "minimal_SM_Higgs_pi2": 0,
        "Higgs_alone_supplies_point_defect_topology": False,
    },
    "projective_hedgehog": {
        "order_parameter": "P=n n^T with n~-n",
        "vacuum_manifold": "RP2",
        "pi2": "Z",
        "representative": "n(x)=x/|x|, P(x)=x x^T/|x|^2",
        "oriented_lift_degree_density": str(degree_density),
        "oriented_lift_degree": str(hedgehog_degree),
        "point_defect_topological_charge": 1,
    },
    "global_energy_audit": {
        "angular_gradient_coefficient": str(angular_gradient),
        "energy_density_asymptotic": "4/r^2 inside Tr(dP dP)",
        "shell_energy_per_dr": str(shell_energy_coefficient),
        "total_energy_behavior": "8 pi integral dr, linearly divergent",
        "finite_energy_without_spatial_gauge_connection": False,
        "spatial_SO3_connection_or_other_stabilizer_required": True,
    },
    "vector_projector_mass": {
        "mass_matrix": "Q_P=3P-I3",
        "eigenvalues": [2, -1, -1],
        "positive_eigenprojector": "P",
        "Chern_density": str(vector_chern_density),
        "first_Chern_number": vector_chern_number,
        "nonzero_complex_Callias_index_from_this_representation": False,
    },
    "spinor_lift_mass": {
        "mass_matrix": "Q_1/2=n.sigma",
        "square": "I2",
        "positive_projector": "(I+n.sigma)/2",
        "Chern_density": str(spinor_chern_density),
        "first_Chern_number": str(spinor_chern_number),
        "unit_index_bundle_available": True,
        "well_defined_as_function_of_P_alone": False,
        "reason": "P(n)=P(-n) but n.sigma changes sign",
    },
    "order_four_root_bridge": {
        "root_phase_candidates": ["-i", "+i"],
        "square": "-1",
        "fourth_power": "1",
        "can_encode_double_cover_sign_in_principle": True,
        "mandatory_root_assigned_to_H15": False,
        "functorial_lift_constructed": False,
    },
    "required_parent_extension": {
        "operator_order_parameter": "spatially varying family projector P(x)",
        "finite_energy_completion": "spatial family gauge connection or alternative stabilizing higher-gradient structure",
        "fermion_index_completion": "oriented spinor/root lift P -> n.sigma",
        "weak_neutrino_readout": "Higgs-dressed projector after the point defect and spinor lift exist",
        "all_from_one_normalized_functional": False,
    },
    "verdict": {
        "projective_order_parameter_has_correct_point_defect_codimension": "pass",
        "ungauged_projective_hedgehog_finite_energy": "fail_linear_divergence",
        "vector_projector_representation_unit_fermion_index": "fail_Chern_zero",
        "spinor_lift_representation_unit_index": "pass",
        "spinor_lift_derived_from_projector_alone": "fail_sign_lost",
        "order_four_root_is_possible_missing_lift_data": "conditional_not_assigned",
        "physical_closure": False,
        "status": "The rank-one family projector has the right RP2 topology for a point defect, unlike the scalar kink. But an ungauged hedgehog has linearly divergent energy and the direct vector-projector mass has zero Chern/Callias index. A unit index appears only after an oriented spinor lift n.sigma, which cannot be reconstructed from P=n n^T without additional double-cover/root data.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))