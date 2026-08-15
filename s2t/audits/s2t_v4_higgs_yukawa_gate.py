import itertools
import json
from fractions import Fraction


left_fields = {
    "Q_L": {"color": "3", "weak": "2", "Y": Fraction(1, 6)},
    "L_L": {"color": "1", "weak": "2", "Y": Fraction(-1, 2)},
}
right_fields = {
    "u_R": {"color": "3", "weak": "1", "Y": Fraction(2, 3)},
    "d_R": {"color": "3", "weak": "1", "Y": Fraction(-1, 3)},
    "e_R": {"color": "1", "weak": "1", "Y": Fraction(-1, 1)},
    "nu_R": {"color": "1", "weak": "1", "Y": Fraction(0, 1)},
}
scalars = {
    "H": {"weak": "2", "Y": Fraction(1, 2)},
    "tilde_H": {"weak": "2", "Y": Fraction(-1, 2)},
}


def color_singlet(left, right):
    return left["color"] == right["color"]


def weak_singlet(left, scalar, right):
    return left["weak"] == "2" and scalar["weak"] == "2" and right["weak"] == "1"


rows = []
allowed_vertices = []
for left_name, right_name, scalar_name in itertools.product(left_fields, right_fields, scalars):
    left = left_fields[left_name]
    right = right_fields[right_name]
    scalar = scalars[scalar_name]
    hypercharge_sum = -left["Y"] + scalar["Y"] + right["Y"]
    allowed = color_singlet(left, right) and weak_singlet(left, scalar, right) and hypercharge_sum == 0
    row = {
        "left": left_name,
        "scalar": scalar_name,
        "right": right_name,
        "hypercharge_sum": str(hypercharge_sum),
        "color_singlet": color_singlet(left, right),
        "weak_singlet": weak_singlet(left, scalar, right),
        "allowed": allowed,
    }
    rows.append(row)
    if allowed:
        allowed_vertices.append(f"bar({left_name}) {scalar_name} {right_name}")

generation_count = 3
dirac_yukawa_matrices = 4
dirac_real_parameters_before_basis_quotient = dirac_yukawa_matrices * 2 * generation_count**2
majorana_real_parameters_before_basis_quotient = 2 * generation_count * (generation_count + 1) // 2

result = {
    "gate": "version4_higgs_yukawa",
    "tested_left_scalar_right_combinations": len(rows),
    "allowed_renormalizable_yukawa_vertices": allowed_vertices,
    "allowed_vertex_count": len(allowed_vertices),
    "rows": rows,
    "single_doublet_scalar_invariants_dimension_le_4": [
        "H^dagger H",
        "(H^dagger H)^2",
    ],
    "renormalizable_scalar_potential": "V(H)=-mu^2 H^dagger H + lambda (H^dagger H)^2 + constant",
    "physical_scalar_count_after_electroweak_breaking": 1,
    "goldstone_count": 3,
    "right_neutrino_majorana_term_allowed": True,
    "weinberg_operator_dimension": 5,
    "generation_count_for_parameter_count": generation_count,
    "dirac_yukawa_real_parameters_before_basis_quotient": dirac_real_parameters_before_basis_quotient,
    "majorana_real_parameters_before_basis_quotient": majorana_real_parameters_before_basis_quotient,
    "spectral_yukawa_invariants": {
        "a": "Tr(Ye^dagger Ye + Ynu^dagger Ynu + 3 Yu^dagger Yu + 3 Yd^dagger Yd)",
        "b": "Tr((Ye^dagger Ye)^2 + (Ynu^dagger Ynu)^2 + 3 (Yu^dagger Yu)^2 + 3 (Yd^dagger Yd)^2)",
    },
    "predictive_status": "the representation fixes the graph and scalar invariant menu, but not Yukawa matrices, mu^2, lambda, or the electroweak scale",
    "minimal_hidden_portal": {
        "operator": "(H^dagger H) Sigma_h",
        "gauge_allowed": True,
        "coefficient_fixed_by_observed_finite_algebra": False,
        "direct_sum_value": 0,
    },
}

with open("s2t_v4_higgs_yukawa_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))