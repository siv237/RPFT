#!/usr/bin/env python3
"""Проверка меры фермионного спектрального оператора Вайнберга на H15."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_h15_fermionic_spectral_weinberg_measure_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


pairing = load_result("s2t_v5_h15_majorana_pairing_correspondence_gate_results.json")
carrier = load_result("s2t_v5_carrier_measure_freeze_gate_results.json")
oneforms = load_result("s2t_v5_h15_physical_oneform_bimodule_gate_results.json")
torsion = load_result("s2t_v5_h15_spectral_torsion_selector_gate_results.json")

assert pairing["zero_branch_spectral_compression"]["M35_zero_line_trace_weight"] == "1/7"
assert pairing["zero_branch_spectral_compression"]["compressed_family_direction_dimension"] == 1
assert not carrier["requirements"]["carrier_prior_measure_defined"]["pass"]
assert not carrier["requirements"]["field_ghost_BV_measure_frozen"]["pass"]
assert oneforms["verdict"]["Grassmann_connection_uniquely_fixes_u_d_e_connection"] == "fail"
assert torsion["verdict"]["Morita_oneform_route_to_unique_Yukawa_operator"] == "closed"

# Чётная и нечётная части одной функции могут изменяться независимо.
# Семейство Шварца g_alpha(z)=z exp(-z^2)+alpha exp(-z^2) сохраняет
# нечётную часть и непрерывно меняет чётную.
z, alpha = sp.symbols("z alpha", real=True)
g_alpha = z * sp.exp(-(z**2)) + alpha * sp.exp(-(z**2))
g_minus = g_alpha.subs(z, -z)
even_part = sp.simplify((g_alpha + g_minus) / 2)
odd_part = sp.simplify((g_alpha - g_minus) / 2)
assert even_part == alpha * sp.exp(-(z**2))
assert odd_part == z * sp.exp(-(z**2))
assert sp.diff(odd_part, alpha) == 0
assert sp.diff(even_part, alpha) == sp.exp(-(z**2))

# Проектор нулевой линии сжимает любой положительный семейный коэффициент
# K=Y_e Y_e^* до одного числа <v0,Kv0>, но не определяет это число.
C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
P0 = sp.simplify((sp.eye(3) + C3 + C3**2) / 3)
d1, d2, d3 = sp.symbols("d1 d2 d3", nonnegative=True, real=True)
K_diag = sp.diag(d1, d2, d3)
kappa_e = sp.simplify((d1 + d2 + d3) / 3)
assert sp.simplify(P0 * K_diag * P0 - kappa_e * P0) == sp.zeros(3)

# Общий следовой вес одинаково умножает кинетику и массовый член.
# После канонической нормировки он сокращается.
w, Z_psi, mu = sp.symbols("w Z_psi mu", positive=True, real=True)
canonical_mass = sp.simplify((w * mu) / (w * Z_psi))
assert canonical_mass == mu / Z_psi
assert sp.diff(canonical_mass, w) == 0

# Схематическая физическая амплитуда зависит минимум от трёх независимых
# величин: отношения спектральных моментов, charged-lepton contraction и
# обратного масштаба отсечения.
r_tau, Lambda = sp.symbols("r_tau Lambda", positive=True, real=True)
v_higgs = sp.symbols("v_H", positive=True, real=True)
m_nu = sp.simplify(r_tau * kappa_e * v_higgs**2 / Lambda)

counterfamily = []
for label, alpha_value in (("zero_even_part", 0), ("unit_even_part", 1), ("double_even_part", 2)):
    counterfamily.append(
        {
            "label": label,
            "alpha": alpha_value,
            "odd_kinetic_function": "z*exp(-z^2)",
            "even_weinberg_function": f"{alpha_value}*exp(-z^2)",
            "same_kinetic_normalization": True,
            "relative_Weinberg_coefficient": alpha_value,
        }
    )

result = {
    "gate": "version5_h15_fermionic_spectral_weinberg_measure_gate",
    "input_certificates": {
        "H15_zero_branch_family_direction": "P0 fixed",
        "M35_zero_line_trace_weight": "1/7",
        "right_handed_neutrino_present": False,
        "charged_Yukawa_operator_uniquely_derived": False,
        "parent_measure_frozen": False,
    },
    "fermionic_spectral_action_structure": {
        "full_function_decomposition": "g(z)=f(z^2)+z h(z^2)",
        "even_part_role": "next-order nonscalar term containing the Higgs-quadratic Majorana/Weinberg operator",
        "odd_part_role": "ordinary fermionic dynamics and its kinetic normalization",
        "even_and_odd_parts_related_by_current_axioms": False,
        "counterfamily": {
            "formula": "g_alpha(z)=z exp(-z^2)+alpha exp(-z^2)",
            "even_part": str(even_part),
            "odd_part": str(odd_part),
            "rows": counterfamily,
            "finding": "The kinetic odd part is identical for every alpha, while the Weinberg even coefficient ranges continuously and can vanish.",
        },
    },
    "family_compression_of_charged_lepton_factor": {
        "literature_factor": "K_e=Y_e Y_e^dagger",
        "diagonal_control": "diag(d1,d2,d3)",
        "compression_identity": "P0 K_e P0=kappa_e P0",
        "kappa_e": str(kappa_e),
        "family_direction_fixed": True,
        "scalar_amplitude_fixed": False,
        "reason": "The project has not derived the three charged-edge amplitudes or their invariant quadratic norm.",
    },
    "trace_weight_cancellation": {
        "zero_line_weight": "w0=1/7",
        "unnormalized_action": "w0 [Z_psi psi^dagger D psi + mu psi^T C psi]",
        "canonical_field_rescaling": "psi_c=sqrt(w0 Z_psi) psi",
        "canonical_mass": str(canonical_mass),
        "depends_on_w0": False,
        "finding": "The common trace weight selects and counts the channel but cannot set its physical mass because it cancels between kinetic and mass terms.",
    },
    "remaining_amplitude": {
        "schematic_formula": str(m_nu),
        "independent_inputs": [
            "r_tau: ratio of the nonscalar even spectral moment to the odd kinetic moment",
            "kappa_e=<v0,Y_e Y_e^dagger v0>: charged-lepton quadratic contraction",
            "Lambda: the dimensionful cutoff or parent suppression scale",
        ],
        "independent_input_count_at_least": 3,
        "fixed_by_C3": False,
        "fixed_by_M35_trace": False,
        "fixed_by_current_parent_measure": False,
    },
    "literature_boundary": {
        "reference": "Sakellariadou-Sitarz, arXiv:1903.09149",
        "paper_explicitly_leaves_classification_of_nonscalar_functions_open": True,
        "paper_mass_depends_on_cutoff_coefficients_scale_Higgs_vev_and_charged_lepton_masses": True,
        "paper_requires_further_nondiagonal_tau_data_for_neutrino_mixing": True,
        "paper_does_not_supply_defect_localization": True,
    },
    "verdict": {
        "operator_type_on_H15": "retained",
        "canonical_family_projector": "retained",
        "trace_weight_one_seventh": "retained_as_channel_weight_not_mass",
        "parameter_free_Weinberg_amplitude": "fail",
        "common_measure_derivation": "fail",
        "localized_defect_profile": "not_derived",
        "physical_closure": False,
        "status": "The nonscalar fermionic spectral action supplies a viable H15 operator type, but the current parent does not relate its even spectral moment to the odd kinetic moment. The M35 weight 1/7 cancels after canonical normalization, and the remaining coefficient also contains an underived charged-lepton contraction and cutoff scale.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))