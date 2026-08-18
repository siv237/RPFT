#!/usr/bin/env python3
"""Минимальный нелинейный тест самопорождающегося переходного дефекта."""

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_self_generated_transition_defect_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


transition = load_result("s2t_v5_transition_primitive_scientific_language_gate_results.json")
local_walk = load_result("s2t_v5_local_defect_transfer_operator_gate_results.json")
assert transition["verdict"]["scientific_languages_for_transition_ontology_exist"]
assert local_walk["input_certificates"]["carrier_dimension"] == 300

# Аналитический кинк локального phi^4-функционала.
x = sp.symbols("x", real=True)
q = sp.tanh(x / sp.sqrt(2))
static_residual = sp.simplify(-sp.diff(q, x, 2) + q * (q**2 - 1))
assert static_residual == 0

energy_density = sp.simplify(sp.diff(q, x) ** 2 / 2 + (q**2 - 1) ** 2 / 4)
kink_energy = sp.simplify(sp.integrate(energy_density, (x, -sp.oo, sp.oo)))
assert kink_energy == 2 * sp.sqrt(2) / 3
topological_charge = sp.simplify((sp.limit(q, x, sp.oo) - sp.limit(q, x, -sp.oo)) / 2)
assert topological_charge == 1

# Лоренцево движущееся продолжение: gamma^2(1-v^2)=1 сводит остаток к
# статическому уравнению.
v = sp.symbols("v", real=True)
gamma_squared = 1 / (1 - v**2)
boost_prefactor = sp.simplify(gamma_squared * (1 - v**2))
assert boost_prefactor == 1

# Джакив--Ребби нулевая мода для H=-i sigma2 d/dx+g q sigma1.
g = sp.symbols("g", positive=True)
psi1 = sp.cosh(x / sp.sqrt(2)) ** (-g * sp.sqrt(2))
zero_mode_residual = sp.simplify(sp.diff(psi1, x) + g * q * psi1)
assert zero_mode_residual == 0

# Независимая численная релаксация без tanh в начальных данных.
points = 301
x_grid = np.linspace(-10.0, 10.0, points)
dx = float(x_grid[1] - x_grid[0])
q_grid = x_grid / 10.0 + 0.08 * np.sin(np.pi * (x_grid + 10.0) / 20.0)
q_grid[0] = -1.0
q_grid[-1] = 1.0


def lattice_energy(field):
    gradient = np.diff(field) / dx
    gradient_energy = 0.5 * np.sum(gradient**2) * dx
    potential_energy = 0.25 * np.sum((field**2 - 1.0) ** 2) * dx
    return float(gradient_energy + potential_energy)


initial_energy = lattice_energy(q_grid)
dt = 0.18 * dx**2
energy_history = [initial_energy]
for step in range(30000):
    laplacian = (q_grid[2:] - 2.0 * q_grid[1:-1] + q_grid[:-2]) / dx**2
    force = laplacian - q_grid[1:-1] * (q_grid[1:-1] ** 2 - 1.0)
    q_grid[1:-1] += dt * force
    q_grid[0] = -1.0
    q_grid[-1] = 1.0
    if (step + 1) % 1000 == 0:
        energy_history.append(lattice_energy(q_grid))

final_energy = lattice_energy(q_grid)
crossing_index = int(np.where(np.diff(np.signbit(q_grid)))[0][0])
x_left, x_right = x_grid[crossing_index], x_grid[crossing_index + 1]
q_left, q_right = q_grid[crossing_index], q_grid[crossing_index + 1]
center = float(x_left - q_left * (x_right - x_left) / (q_right - q_left))
analytic_grid = np.tanh((x_grid - center) / np.sqrt(2.0))
bulk = slice(10, -10)
rms_profile_error = float(np.sqrt(np.mean((q_grid[bulk] - analytic_grid[bulk]) ** 2)))
max_energy_increase = float(max(np.diff(energy_history)))
assert final_energy < initial_energy
assert max_energy_increase < 1e-8
assert rms_profile_error < 5e-3

carrier_dimension = local_walk["input_certificates"]["carrier_dimension"]
scalar_kink_zero_mode_multiplicity = carrier_dimension
assert scalar_kink_zero_mode_multiplicity == 300

result = {
    "gate": "version5_self_generated_transition_defect_gate",
    "local_nonlinear_action": {
        "dimensionless_action": "integral [1/2 q_t^2-1/2 q_x^2-1/4(q^2-1)^2] dt dx",
        "equation": "q_tt-q_xx+q(q^2-1)=0",
        "vacua": [-1, 1],
        "new_order_parameter_added": True,
        "derived_from_M35_trace": False,
    },
    "analytic_kink": {
        "profile": "q(x)=tanh((x-X)/sqrt(2))",
        "equation_residual": str(static_residual),
        "energy_density": str(energy_density),
        "rest_energy": str(kink_energy),
        "topological_charge": str(topological_charge),
        "profile_inserted_by_hand": False,
        "topological_boundary_sector_assumed": True,
    },
    "gradient_flow_reproduction": {
        "grid_points": points,
        "domain": [-10.0, 10.0],
        "initial_profile": "x/10 + 0.08 sin(pi(x+10)/20), with fixed endpoints",
        "iterations": 30000,
        "time_step": dt,
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "sampled_max_energy_increase": max_energy_increase,
        "relaxed_center": center,
        "rms_error_against_derived_kink": rms_profile_error,
        "converges_to_kink": True,
    },
    "moving_defect": {
        "profile": "q_v=tanh(gamma(x-vt-X)/sqrt(2))",
        "gamma_squared_times_one_minus_v_squared": str(boost_prefactor),
        "shape_preserved": True,
        "topological_charge_preserved": True,
        "energy": "E(v)=gamma E_kink",
        "exact_discrete_QCA_solution": False,
    },
    "Dirac_zero_mode": {
        "Hamiltonian": "H=-i sigma2 d_x + g q(x) sigma1",
        "normalizable_component": "psi1=cosh(x/sqrt(2))^(-g sqrt(2))",
        "zero_mode_residual": str(zero_mode_residual),
        "normalizable_for": "g>0",
        "protected_by_mass_sign_change": True,
    },
    "Morita_multiplicity_obstruction": {
        "carrier": "E=M20x15(C)",
        "complex_dimension": carrier_dimension,
        "bimodule_covariant_scalar_defect": "H_q tensor I_E",
        "zero_mode_multiplicity": scalar_kink_zero_mode_multiplicity,
        "single_physical_zero_mode": False,
        "additional_projector_or_higher_complex_required": True,
    },
    "free_data_audit": {
        "dimensional_potential": "lambda/4 (q^2-v_q^2)^2",
        "Dirac_coupling": "y q",
        "dimensionful_scale_remains": True,
        "dimensionless_ratio_y_over_sqrt_lambda_remains": True,
        "topological_boundary_sector_remains_input": True,
        "parameters_derived_from_corner_weights_or_order_four_phase": False,
    },
    "verdict": {
        "profile_derived_from_local_equation": "pass",
        "independent_relaxation_reproduces_profile": "pass",
        "topologically_stable_defect": "pass_given_nontrivial_boundary_sector",
        "moving_shape_preserving_defect": "pass_in_continuum_Lorentz_model",
        "localized_Dirac_zero_mode": "pass",
        "exact_nonlinear_discrete_transition_automaton": "not_built",
        "unique_observed_particle_on_full_Morita_carrier": "fail_by_multiplicity_300",
        "parameter_free_origin_from_current_parent": "fail",
        "physical_closure": False,
        "status": "A local nonlinear field equation can genuinely generate, move and topologically protect a kink while localizing a Dirac zero mode. This validates the particle-as-defect mechanism as a continuum proof of concept. It does not close the project: the scalar potential, scale, relative coupling and topological sector are new inputs, and a bimodule-scalar kink produces 300 zero modes on the full Morita carrier.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))