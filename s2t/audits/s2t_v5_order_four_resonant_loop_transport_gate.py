#!/usr/bin/env python3
"""Унитарный внешний канал с внутренней четырёхтактной петлёй."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_order_four_resonant_loop_transport_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


transport = load_result("s2t_v5_local_defect_transfer_operator_gate_results.json")
root_menu = load_result("s2t_majorana_root_source_menu_results.json")

assert transport["continuum_limit"]["common_light_cone"]
assert transport["verdict"]["local_unitary_transfer_exists"] == "pass"
assert root_menu["exhaustive_gate"]["existing_mandatory_root_sources"] == 0
assert root_menu["candidate_menu"][1]["phases"] == ["-i", "+i"]

# Корневая фаза порядка четыре: после двух тактов возникает знак Мёбиуса,
# после четырёх состояние возвращается полностью.
h = sp.I
assert h**2 == -1
assert h**4 == 1
phase_history = [sp.simplify(h**n) for n in range(5)]

# Потеребезопасный однопортовый кольцевой резонатор. Реальный r — амплитуда
# остаться в петле после обхода, t=sqrt(1-r^2) — связь с внешним каналом.
r, q = sp.symbols("r q", real=True)
t_squared = sp.simplify(1 - r**2)
S = sp.simplify((r - q) / (1 - r * q))
S_conjugate_on_unit_circle = sp.simplify((r - 1 / q) / (1 - r / q))
unitarity_residual = sp.simplify(S * S_conjugate_on_unit_circle - 1)
assert unitarity_residual == 0

# Четыре внутренних такта дают q=exp(i theta), theta=4 omega.
theta, omega = sp.symbols("theta omega", real=True)
L = sp.Integer(4)
delay = sp.simplify(L * (1 - r**2) / (1 + r**2 - 2 * r * sp.cos(theta)))
resonant_delay = sp.simplify(delay.subs(theta, 0))
assert sp.simplify(sp.together(resonant_delay - 4 * (1 + r) / (1 - r))) == 0
assert sp.simplify(resonant_delay.subs(r, 0)) == 4

controls = []
for r_value in (sp.Rational(0), sp.Rational(1, 2), sp.Rational(9, 10)):
    controls.append(
        {
            "r": str(r_value),
            "external_internal_coupling_t": float(sp.sqrt(1 - r_value**2)),
            "resonant_group_delay_steps": float(resonant_delay.subs(r, r_value)),
            "survival_probability_per_roundtrip": float(r_value**2),
            "finite_lifetime_for_nonzero_coupling": bool(r_value < 1),
        }
    )

# После выключения входа внутренняя вероятность после n обходов равна
# r^(2n). Бесконечная устойчивость требует r=1, но тогда t=0.
n = sp.symbols("n", integer=True, nonnegative=True)
survival_probability = r ** (2 * n)
stable_condition = "r=1"
nonzero_coupling_condition = "0<=r<1"

# Четырёхсостояний внутренний сдвиг. При связи через один узел все четыре
# собственные моды видны порту. При симметричной связи три моды темны, но
# именно поэтому не могут входить и выходить через тот же порт.
U4 = sp.Matrix(
    [
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
)
assert U4**4 == sp.eye(4)

fourier_modes = []
site_port = sp.Matrix([1, 0, 0, 0])
symmetric_port = sp.ones(4, 1) / 2
site_dark_count = 0
symmetric_dark_count = 0
for k in range(4):
    mode = sp.Matrix([sp.exp(2 * sp.pi * sp.I * k * j / 4) / 2 for j in range(4)])
    site_overlap = sp.simplify((site_port.T.conjugate() * mode)[0])
    symmetric_overlap = sp.simplify((symmetric_port.T.conjugate() * mode)[0])
    if site_overlap == 0:
        site_dark_count += 1
    if symmetric_overlap == 0:
        symmetric_dark_count += 1
    fourier_modes.append(
        {
            "k": k,
            "eigenvalue": str(sp.simplify((U4 * mode)[0] / mode[0])),
            "site_port_overlap_squared": str(sp.simplify(sp.conjugate(site_overlap) * site_overlap)),
            "symmetric_port_overlap_squared": str(
                sp.simplify(sp.conjugate(symmetric_overlap) * symmetric_overlap)
            ),
        }
    )

assert site_dark_count == 0
assert symmetric_dark_count == 3

result = {
    "gate": "version5_order_four_resonant_loop_transport_gate",
    "early_hypothesis_reconstruction": {
        "matter_image": "light delayed by a four-stage twisted closed route rather than locally propagating below c",
        "order_four_phase_history": [str(value) for value in phase_history],
        "Mobius_sign_after_two_steps": str(h**2),
        "full_return_after_four_steps": str(h**4),
        "literal_c_over_four_local_speed_claimed": False,
        "effective_delay_interpretation": True,
    },
    "minimal_unitary_resonator": {
        "junction_parameters": "r real, t=sqrt(1-r^2)",
        "four_step_loop_factor": "q=exp(4 i omega)",
        "through_scattering_amplitude": str(S),
        "unitarity_residual_on_abs_q_equal_one": str(unitarity_residual),
        "group_delay": str(delay),
        "resonant_group_delay": str(resonant_delay),
        "controls": controls,
    },
    "exact_factor_four_case": {
        "condition": "r=0, t=1",
        "scattering": "S=-q",
        "delay_steps": 4,
        "interpretation": "the incoming wave is fully routed through one four-stage internal cycle and then re-emitted",
        "permanent_localization": False,
    },
    "stability_coupling_trilemma": {
        "survival_probability_after_n_roundtrips": str(survival_probability),
        "infinite_stability_requires": stable_condition,
        "nonzero_entry_exit_requires": nonzero_coupling_condition,
        "at_infinite_stability_coupling_t": 0,
        "stable_and_open_single_port_solution": False,
        "finding": "For every nonzero coupling the stored amplitude has a finite lifetime. The infinite-lifetime limit disconnects the loop from the same external port.",
    },
    "dark_state_audit": {
        "internal_shift_order": 4,
        "modes": fourier_modes,
        "single_site_port_dark_mode_count": site_dark_count,
        "symmetric_port_dark_mode_count": symmetric_dark_count,
        "dark_state_entry_exit_through_same_port": False,
        "finding": "Destructive interference can create exact dark states only by making their port overlap zero; reciprocity then prevents free excitation and emission through that port.",
    },
    "moving_defect_boundary": {
        "translated_attachment_points_are_isospectral": True,
        "static_model_selects_attachment_position": False,
        "law_transporting_the_attachment_point": "not derived",
        "particle_motion_from_static_resonator": False,
    },
    "project_compatibility": {
        "local_unitary_transport": "compatible",
        "common_light_cone": "compatible because local propagation remains at the base step speed",
        "order_four_root_phase_algebraically_present": True,
        "order_four_root_assigned_mandatorily_to_H15": False,
        "new_topological_sector_required": True,
    },
    "verdict": {
        "four_stage_unitary_delay": "pass",
        "exact_effective_factor_four": "pass_only_for_full_one_cycle_routing_r_equal_zero",
        "free_entry_and_exit": "pass_for_nonzero_coupling",
        "infinite_local_stability_with_same_port": "fail",
        "topologically_protected_dark_state": "conditional_but_decoupled",
        "moving_particle_law": "not_derived",
        "parameter_free_physical_particle": "fail",
        "physical_closure": False,
        "status": "The early light-in-a-twisted-loop idea has a precise unitary realization as an order-four delay resonator. It explains an effective four-step delay without reducing the local light cone, but a single reciprocal port cannot simultaneously provide free entry/exit and infinite localization. The order-four root is also not mandatory in the current H15 parent.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))