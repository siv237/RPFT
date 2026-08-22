#!/usr/bin/env python3
"""Полный стационарный четырёхпрофильный фон вихря Q+T+B."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parents[2]
COUPLED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate.py"
T_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py"
Q_AUDIT = ROOT / "s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py"
CORRECTED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py"
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_stationary_background_gate_results.json"

Z = 1.0 / 3.0
G = 2.0 / 27.0


def setup_reduction():
    coupled = runpy.run_path(str(COUPLED_AUDIT))
    t_module = runpy.run_path(str(T_AUDIT))
    q_module = runpy.run_path(str(Q_AUDIT))
    corrected = runpy.run_path(str(CORRECTED_AUDIT))
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]

    q_basis = coupled["symmetric_traceless_basis"]()
    t_basis, _ = t_module["symmetrized_traceless_rank_three_basis"]()
    axes = coupled["tetrahedral_axes"]()
    director = axes[0]
    identity = np.eye(3)
    gap = float(thermal["coexistence_ordered_spectrum"][0] - thermal["coexistence_ordered_spectrum"][1])
    beta = float(thermal["critical_inverse_temperature"])
    q_vacuum = gap * (np.outer(director, director) - identity / 3.0)
    t_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    q_coefficients = np.einsum("aij,ij->a", q_basis, q_vacuum)
    t_coefficients = np.einsum("aijk,ijk->a", t_basis, t_vacuum)

    generator = np.array([
        [0.0, -director[2], director[1]],
        [director[2], 0.0, -director[0]],
        [-director[1], director[0], 0.0],
    ]) / 3.0
    t_generator = np.array([
        [np.sum(left * t_module["act_on_rank_three"](generator, right)) for right in t_basis]
        for left in t_basis
    ])
    values, vectors = np.linalg.eigh(-1j * t_generator)
    zero_vectors = vectors[:, np.abs(values) < 1.0e-10]
    projector_zero = zero_vectors @ zero_vectors.conj().T
    t_zero = np.real_if_close(projector_zero @ t_coefficients).real
    t_three = t_coefficients - t_zero

    A = Z * float(np.dot(t_three, t_three))
    B = Z * float(np.dot(t_zero, t_zero))
    D = Z * float(np.dot(q_coefficients, q_coefficients))
    v_t_squared = float(np.sum(t_vacuum**2))
    alignment_scale = (8.0 / 9.0) ** 2
    ordered_free_energy = q_module["free_energy"](identity / 3.0 + q_vacuum, beta)

    # Полиномиальная часть полного потенциала вдоль (q,a,b).
    qs, aa, bb = sp.symbols("q a b", real=True)
    q_matrix = sp.Matrix(identity / 3.0) + qs * sp.Matrix(q_vacuum / gap)
    t_tensor = np.empty((3, 3, 3), dtype=object)
    t_zero_tensor = np.einsum("a,aijk->ijk", t_zero, t_basis)
    t_three_tensor = np.einsum("a,aijk->ijk", t_three, t_basis)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                t_tensor[i, j, k] = sp.Float(t_zero_tensor[i, j, k]) * bb + sp.Float(t_three_tensor[i, j, k]) * aa

    moment = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            moment[i, j] = sum(t_tensor[i, k, l] * t_tensor[j, k, l] for k in range(3) for l in range(3))
    curvature_t = moment - sp.Float(v_t_squared / 3.0) * sp.eye(3)
    t_potential = sum(curvature_t[i, j] ** 2 for i in range(3) for j in range(3)) / 3

    contraction = sp.Matrix([
        sum(t_tensor[i, j, k] * q_matrix[j, k] for j in range(3) for k in range(3))
        for i in range(3)
    ])
    curvature_qt = contraction * contraction.T - sp.Float(alignment_scale) * q_matrix
    mixed_potential = sum(curvature_qt[i, j] ** 2 for i in range(3) for j in range(3)) / 3
    polynomial = sp.expand(t_potential + mixed_potential)
    poly_value = sp.lambdify((qs, aa, bb), polynomial, "numpy")
    poly_dq = sp.lambdify((qs, aa, bb), sp.diff(polynomial, qs), "numpy")
    poly_da = sp.lambdify((qs, aa, bb), sp.diff(polynomial, aa), "numpy")
    poly_db = sp.lambdify((qs, aa, bb), sp.diff(polynomial, bb), "numpy")

    def q_free_energy(q):
        l1 = 1.0 / 3.0 + 2.0 * gap * q / 3.0
        l2 = 1.0 / 3.0 - gap * q / 3.0
        second = l1**2 + 2.0 * l2**2
        third = l1**3 + 2.0 * l2**3
        entropy = l1 * np.log(l1) + 2.0 * l2 * np.log(l2)
        return entropy + beta * ((2.0 / 7.0) * (1.0 - second**2 / third) + 1.0 - second) - ordered_free_energy

    def q_free_derivative(q):
        l1 = 1.0 / 3.0 + 2.0 * gap * q / 3.0
        l2 = 1.0 / 3.0 - gap * q / 3.0
        dl1, dl2 = 2.0 * gap / 3.0, -gap / 3.0
        second = l1**2 + 2.0 * l2**2
        third = l1**3 + 2.0 * l2**3
        dsecond = 2.0 * l1 * dl1 + 4.0 * l2 * dl2
        dthird = 3.0 * l1**2 * dl1 + 6.0 * l2**2 * dl2
        dentropy = dl1 * (np.log(l1) + 1.0) + 2.0 * dl2 * (np.log(l2) + 1.0)
        dradial = -(2.0 / 7.0) * (2.0 * second * dsecond * third - second**2 * dthird) / third**2
        return dentropy + beta * (dradial - dsecond)

    def potential(q, a, b):
        return q_free_energy(q) + poly_value(q, a, b)

    def derivatives(q, a, b):
        return q_free_derivative(q) + poly_dq(q, a, b), poly_da(q, a, b), poly_db(q, a, b)

    old_solution, _, _ = corrected["corrected_profile"]()
    return {
        "A": A, "B": B, "D": D, "G": G,
        "potential": potential, "derivatives": derivatives,
        "old_solution": old_solution, "q_coefficients": q_coefficients,
        "t_zero": t_zero, "t_three": t_three,
        "polynomial": str(polynomial), "gap": gap,
    }


def solve_full_profile(model, tolerance=2.0e-7):
    A, B, D, Gc = model["A"], model["B"], model["D"], model["G"]

    def equations(radius, value):
        k, kp, a, ap, b, bp, q, qp = value
        dq, da, db = model["derivatives"](q, a, b)
        return np.vstack([
            kp,
            kp / radius - (A / Gc) * a**2 * (1.0 - k),
            ap,
            -ap / radius + (1.0 - k) ** 2 * a / radius**2 + da / A,
            bp,
            -bp / radius + db / B,
            qp,
            -qp / radius + dq / D,
        ])

    def boundary(left, right):
        return np.array([
            left[0], left[2], left[5], left[7],
            right[0] - 1.0, right[2] - 1.0, right[4] - 1.0, right[6] - 1.0,
        ])

    radius = np.linspace(1.0e-5, 20.0, 900)
    old = model["old_solution"].sol(radius)
    q = 1.0 - 0.12 * np.exp(-radius**2)
    initial = np.vstack([old[:6], q, np.gradient(q, radius)])
    solution = solve_bvp(equations, boundary, radius, initial, tol=tolerance, max_nodes=80000, verbose=0)
    return solution, equations, boundary


def main() -> None:
    model = setup_reduction()
    solution, equations, boundary = solve_full_profile(model)
    radius = np.linspace(1.0e-5, 20.0, 30000)
    k, kp, a, ap, b, bp, q, qp = solution.sol(radius)
    A, B, D, Gc = model["A"], model["B"], model["D"], model["G"]
    densities = {
        "radial_T3": 0.5 * A * ap**2,
        "radial_T0": 0.5 * B * bp**2,
        "radial_Q": 0.5 * D * qp**2,
        "angular_T3": 0.5 * A * a**2 * (1.0 - k) ** 2 / radius**2,
        "gauge_curvature": 0.5 * Gc * kp**2 / radius**2,
        "potential": model["potential"](q, a, b),
    }
    parts = {
        name: float(2.0 * np.pi * np.trapezoid(value * radius, radius))
        for name, value in densities.items()
    }
    tension = sum(parts.values())
    virial = abs(parts["gauge_curvature"] - parts["potential"])
    equation_residual = solution.sol(radius, 1) - equations(radius, solution.sol(radius))
    old_q_residual = abs(float(model["derivatives"](1.0, 0.0, float(model["old_solution"].sol(1.0e-5)[4]))[0] / model["D"]))

    sample_radii = np.array([1.0e-5, 0.05, 0.1, 0.3, 0.7, 1.5, 3.0, 6.0, 12.0])
    sample = solution.sol(sample_radii)
    result = {
        "gate": "version6_bosonic_defect_full_tensor_stationary_background_gate",
        "reduced_action": {
            "profiles": ["K", "a", "b", "q"],
            "Q_ansatz": "Q(r)=q(r) Q_vacuum",
            "kinetic_coefficients": {"A_T3": A, "B_T0": B, "D_Q": D, "G_connection": Gc},
            "new_free_parameter_count": 0,
        },
        "boundary_value_problem": {
            "solver_status": int(solution.status),
            "solver_message": solution.message,
            "mesh_nodes": int(solution.x.size),
            "maximum_relative_residual": float(np.max(solution.rms_residuals)),
            "boundary_residual": float(np.linalg.norm(boundary(solution.y[:, 0], solution.y[:, -1]))),
            "maximum_first_order_system_residual": float(np.max(np.abs(equation_residual))),
        },
        "profile": {
            "core_values": {"b": float(b[0]), "q": float(q[0]), "a_slope": float(ap[0])},
            "dimensionless_tension": tension,
            "energy_parts": parts,
            "relative_virial_residual": virial / tension,
            "samples": {
                "r": sample_radii.tolist(), "K": sample[0].tolist(), "a": sample[2].tolist(),
                "b": sample[4].tolist(), "q": sample[6].tolist(),
            },
        },
        "stationarity": {
            "old_frozen_Q_equation_residual_scale": old_q_residual,
            "full_four_profile_background_stationary": bool(solution.status == 0 and np.max(solution.rms_residuals) < 3.0e-7),
            "Q_profile_deviation_from_vacuum_at_core": float(1.0 - q[0]),
        },
        "verdict": {
            "single_additional_Q_amplitude_suffices": True,
            "full_stationary_background_constructed": bool(solution.status == 0),
            "candidate_twisted_negative_mode_retest_required": True,
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate",
        },
    }
    assert solution.status == 0
    assert result["boundary_value_problem"]["maximum_relative_residual"] < 3.0e-7
    assert result["boundary_value_problem"]["boundary_residual"] < 1.0e-8
    assert 0.0 < q[0] < 1.0
    assert result["profile"]["relative_virial_residual"] < 2.0e-6
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()