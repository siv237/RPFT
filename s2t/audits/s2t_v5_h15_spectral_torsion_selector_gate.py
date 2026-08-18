#!/usr/bin/env python3
"""Проверка спектрального кручения как селектора рёбер u,d,e на H15."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_h15_spectral_torsion_selector_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


oneforms = load_result("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
assert oneforms["verdict"]["residual_relative_connection_dimension"] == 2

# a,b,c обозначают |y_u|^2, |y_d|^2, |y_e|^2.
a, b, c, scale = sp.symbols("a b c scale", positive=True)
torsion_invariants = {
    "up_self": 3 * a**2,
    "down_lepton_self": 3 * b**2 + c**2,
    "up_down_mixed": 3 * a * b,
}

homogeneity_checks = {
    name: sp.simplify(expr.subs({a: scale**2 * a, b: scale**2 * b, c: scale**2 * c}) / expr)
    for name, expr in torsion_invariants.items()
}
assert all(value == scale**4 for value in homogeneity_checks.values())

# После удаления общей амплитуды остаются r=a/b и s=c/b. Две простые
# безмасштабные комбинации спектрального кручения чувствительны к обеим
# относительным координатам, но не предписывают их значения.
r, s = sp.symbols("r s", positive=True)
relative_observables = sp.Matrix([1 / r, 1 + s**2 / 3])
jacobian = relative_observables.jacobian([r, s])
jacobian_determinant = sp.factor(jacobian.det())
generic_rank = int(jacobian.subs({r: 2, s: 3}).rank())
assert generic_rank == 2
assert jacobian_determinant != 0

# Если превратить кручение в новый положительный потенциал без отдельного
# уровня/ограничения, однородность оставляет тривиальный минимум в начале.
positive_norm = sp.expand(sum(expr**2 for expr in torsion_invariants.values()))
gradient_at_origin = [sp.diff(positive_norm, variable).subs({a: 0, b: 0, c: 0}) for variable in (a, b, c)]
assert all(value == 0 for value in gradient_at_origin)
assert positive_norm.subs({a: 0, b: 0, c: 0}) == 0

result = {
    "gate": "version5_h15_spectral_torsion_selector_gate",
    "input_certificate": {
        "correctly_typed_H15_oneforms": "pass",
        "residual_relative_dimension": 2,
    },
    "H15_spectral_torsion_invariants": {
        name: str(expr) for name, expr in torsion_invariants.items()
    },
    "homogeneity": {
        "Yukawa_scaling": "y_s -> t y_s",
        "invariant_scaling": "I -> t^4 I",
        "checks": {name: str(value) for name, value in homogeneity_checks.items()},
        "absolute_scale_selected": False,
    },
    "relative_sensitivity": {
        "coordinates": {"r": "|y_u|^2/|y_d|^2", "s": "|y_e|^2/|y_d|^2"},
        "scale_free_observables": ["I_ud/I_u=1/r", "I_de/(3|y_d|^4)=1+s^2/3"],
        "jacobian": [[str(entry) for entry in row] for row in jacobian.tolist()],
        "jacobian_determinant": str(jacobian_determinant),
        "generic_rank": generic_rank,
        "sees_both_relative_directions": True,
        "prescribes_target_values_for_them": False,
    },
    "connection_reconstruction_literature_audit": {
        "ordinary_Connes_calculus_exact_match": False,
        "Mesland_Rennie_modified_calculus_match": True,
        "required_second_degree_idempotent_is_Hermitian": False,
        "required_second_degree_idempotent_respects_involution": False,
        "reconstructed_connection_uses_the_input_Dirac_Yukawa_data": True,
        "reconstructed_connection_derives_Yukawa_ratios": False,
    },
    "forbidden_potential_repair": {
        "candidate": "sum of squares of torsion invariants",
        "formula": str(positive_norm),
        "nonnegative": True,
        "zero_at_origin": True,
        "gradient_at_origin": [str(value) for value in gradient_at_origin],
        "nonzero_level_or_constraint_required": True,
        "allowed_as_parent_derived_selector": False,
    },
    "verdict": {
        "spectral_torsion_is_nontrivial_on_H15": "pass",
        "spectral_torsion_detects_two_relative_directions": "pass",
        "spectral_torsion_selects_unique_relative_Yukawa_ratios": "fail",
        "ordinary_involutive_second_degree_calculus_reproduces_torsion": "fail",
        "modified_calculus_is_input_independent_selector": "fail",
        "Morita_oneform_route_to_unique_Yukawa_operator": "closed",
        "Morita_parent_as_kinematic_container": "retained",
        "physical_closure": False,
        "status": "torsion measures the two remaining Yukawa directions but does not choose them; the unique-Yukawa Morita route is closed",
    },
    "next_gate": (
        "Do not add another potential on the two-dimensional plane. Freeze the "
        "Morita construction as kinematics and return to the project-wide architecture "
        "menu: only an independently derived symmetry relating inequivalent edges or a "
        "new parent principle can reopen Yukawa selection."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))