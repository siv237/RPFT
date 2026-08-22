#!/usr/bin/env python3
"""Solve the radial Euler--Lagrange equation and audit radial stability."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_euler_lagrange_stability_gate_results.json"
GAP = 0.8682499004685158


def analytic_densities(radius: np.ndarray, value: np.ndarray, derivative: np.ndarray):
    derivative_density = (
        (2.0 / 3.0) * GAP**2 * derivative**2
        + 4.0 * GAP**2 * value**2 * (1.0 - value**2) ** 2 / radius**2
    )
    curvature_density = (
        16.0 * value**2 * derivative**2 / radius**2
        + 2.0 * value**4 * (value**2 - 2.0) ** 2 / radius**4
    )
    potential_density = GAP**4 * (1.0 - value**2) ** 2
    return derivative_density, curvature_density, potential_density


def trial_radius_and_energy(coefficients: tuple[float, float, float], integrals: tuple[float, float, float]):
    c_d, c_f, c_v = coefficients
    i_d, i_f, i_v = integrals
    roots = np.roots([3.0 * c_v * i_v, c_d * i_d, -c_f * i_f])
    positive_y = max(root.real for root in roots if abs(root.imag) < 1e-12 and root.real > 0)
    radius = float(np.sqrt(positive_y))
    energy = float(c_d * i_d * radius + c_f * i_f / radius + c_v * i_v * radius**3)
    return radius, energy


def sturm_negative_count(diagonal: np.ndarray, off_diagonal: np.ndarray) -> int:
    """Number of negative eigenvalues from the Sturm pivot recurrence."""
    pivots = np.empty_like(diagonal)
    pivots[0] = diagonal[0]
    negative = int(pivots[0] < 0.0)
    for index in range(1, len(diagonal)):
        previous = pivots[index - 1]
        if abs(previous) < 1e-14:
            previous = -1e-14 if previous < 0.0 else 1e-14
        pivots[index] = diagonal[index] - off_diagonal[index - 1] ** 2 / previous
        negative += int(pivots[index] < 0.0)
    return negative


def main() -> None:
    radius_symbol, value_symbol = sp.symbols("r u", positive=True)
    c_d_symbol, c_f_symbol, c_v_symbol = sp.symbols("c_D c_F c_V", positive=True)
    kinetic_coefficient = (
        c_d_symbol * sp.Rational(2, 3) * GAP**2 * radius_symbol**2
        + 16 * c_f_symbol * value_symbol**2
    )
    potential = (
        4 * c_d_symbol * GAP**2 * value_symbol**2 * (1 - value_symbol**2) ** 2
        + 2 * c_f_symbol * value_symbol**4 * (value_symbol**2 - 2) ** 2 / radius_symbol**2
        + c_v_symbol * GAP**4 * radius_symbol**2 * (1 - value_symbol**2) ** 2
    )
    potential_u = sp.lambdify(
        (radius_symbol, value_symbol, c_d_symbol, c_f_symbol, c_v_symbol),
        sp.diff(potential, value_symbol),
        "numpy",
    )
    potential_uu = sp.lambdify(
        (radius_symbol, value_symbol, c_d_symbol, c_f_symbol, c_v_symbol),
        sp.diff(potential, value_symbol, 2),
        "numpy",
    )

    previous = json.loads(
        (ROOT / "s2t/results/s2t_v6_gauged_projective_spin_cover_parent_gate_results.json")
        .read_text(encoding="utf-8")
    )
    finite = previous["finite_energy_test_unit_coefficients"]
    trial_integrals = (
        float(finite["integral_DQ_squared"]),
        float(finite["integral_F_squared"]),
        float(finite["integral_bulk_potential"]),
    )

    # Independent Cartesian check of the reduced radial densities.
    audit_path = ROOT / "s2t/audits/s2t_v6_gauged_projective_spin_cover_parent_gate.py"
    specification = importlib.util.spec_from_file_location("composite_connection_audit", audit_path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    density_residuals = []
    for radius in [0.1, 0.3, 1.0, 3.0, 10.0]:
        value = radius**2 / (radius**2 + 1.0)
        derivative = 2.0 * radius / (radius**2 + 1.0) ** 2
        analytic = analytic_densities(
            np.array([radius]), np.array([value]), np.array([derivative])
        )
        cartesian = module.densities(radius, GAP)[:3]
        density_residuals.extend(
            abs(float(analytic[index][0]) - float(cartesian[index])) for index in range(3)
        )

    coefficient_cases = {
        "unit": (1.0, 1.0, 1.0),
        "small_D": (0.25, 1.0, 1.0),
        "large_D": (4.0, 1.0, 1.0),
        "small_F": (1.0, 0.25, 1.0),
        "large_F": (1.0, 4.0, 1.0),
        "small_V": (1.0, 1.0, 0.25),
        "large_V": (1.0, 1.0, 4.0),
    }
    case_results = {}
    epsilon = 1.0e-4
    outer_radius = 50.0

    for name, coefficients in coefficient_cases.items():
        c_d, c_f, c_v = coefficients
        mesh = np.geomspace(epsilon, outer_radius, 1100)
        trial_radius, trial_energy = trial_radius_and_energy(coefficients, trial_integrals)
        initial = mesh**2 / (mesh**2 + trial_radius**2)
        initial_derivative = 2.0 * mesh * trial_radius**2 / (mesh**2 + trial_radius**2) ** 2

        def equation(radius: np.ndarray, field: np.ndarray) -> np.ndarray:
            value, derivative = field
            coefficient = c_d * (2.0 / 3.0) * GAP**2 * radius**2 + 16.0 * c_f * value**2
            coefficient_r = c_d * (4.0 / 3.0) * GAP**2 * radius
            coefficient_u = 32.0 * c_f * value
            second = (
                potential_u(radius, value, c_d, c_f, c_v)
                - coefficient_u * derivative**2
                - 2.0 * coefficient_r * derivative
            ) / (2.0 * coefficient)
            return np.vstack((derivative, second))

        solution = solve_bvp(
            equation,
            lambda left, right: np.array([left[0], right[0] - 1.0]),
            mesh,
            np.vstack((initial, initial_derivative)),
            tol=2.0e-7,
            max_nodes=50000,
        )

        integration_radius = np.geomspace(epsilon, outer_radius, 30000)
        value, derivative = solution.sol(integration_radius)
        derivative_density, curvature_density, potential_density = analytic_densities(
            integration_radius, value, derivative
        )
        measure = 4.0 * np.pi * integration_radius**2
        energy_parts = [
            float(np.trapezoid(measure * c_d * derivative_density, integration_radius)),
            float(np.trapezoid(measure * c_f * curvature_density, integration_radius)),
            float(np.trapezoid(measure * c_v * potential_density, integration_radius)),
        ]
        curvature_tail = 8.0 * np.pi * c_f / outer_radius
        corrected_parts = [energy_parts[0], energy_parts[1] + curvature_tail, energy_parts[2]]
        corrected_energy = float(sum(corrected_parts))
        virial_residual = float(corrected_parts[0] - corrected_parts[1] + 3.0 * corrected_parts[2])

        evaluation_radius = np.linspace(epsilon, outer_radius, 900)
        evaluation_value, evaluation_derivative = solution.sol(evaluation_radius)
        coefficient = (
            c_d * (2.0 / 3.0) * GAP**2 * evaluation_radius**2
            + 16.0 * c_f * evaluation_value**2
        )
        coefficient_r = c_d * (4.0 / 3.0) * GAP**2 * evaluation_radius
        coefficient_u = 32.0 * c_f * evaluation_value
        second_derivative = (
            potential_u(evaluation_radius, evaluation_value, c_d, c_f, c_v)
            - coefficient_u * evaluation_derivative**2
            - 2.0 * coefficient_r * evaluation_derivative
        ) / (2.0 * coefficient)
        hessian_potential = (
            potential_uu(evaluation_radius, evaluation_value, c_d, c_f, c_v)
            - 32.0 * c_f * evaluation_derivative**2
            - 64.0 * c_f * evaluation_value * second_derivative
        )
        principal = 2.0 * coefficient
        spacing = evaluation_radius[1] - evaluation_radius[0]
        midpoint = 0.5 * (principal[:-1] + principal[1:])
        diagonal = (
            (midpoint[:-1] + midpoint[1:]) / spacing**2
            + hessian_potential[1:-1]
        )
        off_diagonal = -midpoint[1:-1] / spacing**2
        lowest_discrete = eigh_tridiagonal(
            diagonal, off_diagonal, select="i", select_range=(0, 2)
        )[0]
        negative_count = sturm_negative_count(diagonal, off_diagonal)

        case_results[name] = {
            "coefficients": list(coefficients),
            "bvp_status": int(solution.status),
            "maximum_rms_ode_residual": float(np.max(solution.rms_residuals)),
            "boundary_residual": float(
                max(abs(solution.y[0, 0]), abs(solution.y[0, -1] - 1.0))
            ),
            "monotonicity_minimum_difference": float(np.min(np.diff(value))),
            "half_height_radius": float(np.interp(0.5, value, integration_radius)),
            "energy_parts_with_tail_correction": corrected_parts,
            "corrected_total_energy": corrected_energy,
            "best_scaled_trial_radius": trial_radius,
            "best_scaled_trial_energy": trial_energy,
            "energy_below_trial_family": corrected_energy < trial_energy,
            "corrected_virial_residual": virial_residual,
            "radial_hessian_negative_eigenvalue_count": negative_count,
            "lowest_three_finite_box_eigenvalues": lowest_discrete.tolist(),
        }

    result = {
        "gate": "version6_bosonic_defect_full_euler_lagrange_stability_gate",
        "radial_reduction": {
            "field": "Q=Delta*u(r)*(P-I/3)",
            "composite_connection": "A=u(r)^2[P,dP]",
            "DQ_density": "(2/3)Delta^2 u'^2+4 Delta^2 u^2(1-u^2)^2/r^2",
            "F_density": "16 u^2 u'^2/r^2+2 u^4(u^2-2)^2/r^4",
            "V_density": "Delta^4(1-u^2)^2",
            "cartesian_reduction_maximum_residual": max(density_residuals),
        },
        "boundary_value_problem": {
            "boundary_conditions": ["u(0)=0", "u(infinity)=1"],
            "outer_radius": outer_radius,
            "curvature_tail_correction": "8 pi c_F/R_max",
            "cases": case_results,
        },
        "verdict": {
            "unit_case_solution_exists": case_results["unit"]["bvp_status"] == 0,
            "all_tested_positive_coefficient_cases_converged": all(
                case["bvp_status"] == 0 for case in case_results.values()
            ),
            "all_solutions_monotone": all(
                case["monotonicity_minimum_difference"] > -1e-10
                for case in case_results.values()
            ),
            "all_exact_energies_below_scaled_trial_family": all(
                case["energy_below_trial_family"] for case in case_results.values()
            ),
            "radial_negative_mode_found": any(
                case["radial_hessian_negative_eigenvalue_count"] > 0
                for case in case_results.values()
            ),
            "full_nonradial_stability_derived": False,
            "status": "radial_solution_exists_and_is_radially_stable_in_tested_positive_coefficient_window",
            "next_gate": "version6_bosonic_defect_nonradial_stability_gate",
        },
    }

    assert max(density_residuals) < 1e-9
    assert result["verdict"]["all_tested_positive_coefficient_cases_converged"]
    assert result["verdict"]["all_solutions_monotone"]
    assert result["verdict"]["all_exact_energies_below_scaled_trial_family"]
    assert not result["verdict"]["radial_negative_mode_found"]
    assert max(abs(case["corrected_virial_residual"]) for case in case_results.values()) < 2e-3

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()