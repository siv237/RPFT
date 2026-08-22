#!/usr/bin/env python3
"""Топология и канонический профиль Z3-вихря совместного вакуума Q+T+B."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate_results.json"
A = C = 128.0 / 81.0
B = 160.0 / 81.0
G = 2.0 / 27.0
POLYNOMIAL = {
    (0, 0): 31744.0 / 19683.0, (0, 2): -38912.0 / 19683.0,
    (0, 4): 5120.0 / 6561.0, (2, 0): -8192.0 / 6561.0,
    (2, 2): 8192.0 / 19683.0, (4, 0): 8192.0 / 19683.0,
}


def potential(a, b):
    return sum(value * a**i * b**j for (i, j), value in POLYNOMIAL.items())


def derivative_a(a, b):
    return sum(value * i * a ** (i - 1) * b**j for (i, j), value in POLYNOMIAL.items() if i)


def derivative_b(a, b):
    return sum(value * j * a**i * b ** (j - 1) for (i, j), value in POLYNOMIAL.items() if j)


def equations(radius, value):
    k, kp, a, ap, b, bp = value
    return np.vstack([
        kp,
        kp / radius - (C / G) * a**2 * (1.0 - k),
        ap,
        -ap / radius + (1.0 - k) ** 2 * a / radius**2 + derivative_a(a, b) / A,
        bp,
        -bp / radius + derivative_b(a, b) / B,
    ])


def boundary(left, right):
    return np.array([left[0], left[2], left[5], right[0] - 1.0, right[2] - 1.0, right[4] - 1.0])


def solve_profile(tolerance=2.0e-7):
    radius = np.linspace(1.0e-5, 20.0, 700)
    k = radius**2 / (1.0 + radius**2)
    a = np.tanh(radius)
    b = 1.0 + 0.07 * np.exp(-radius**2)
    initial = np.vstack([k, np.gradient(k, radius), a, np.gradient(a, radius), b, np.gradient(b, radius)])
    return solve_bvp(equations, boundary, radius, initial, tol=tolerance, max_nodes=50000)


def main() -> None:
    solution = solve_profile()
    radius = np.linspace(1.0e-5, 20.0, 30000)
    k, kp, a, ap, b, bp = solution.sol(radius)
    densities = {
        "radial_scalar": 0.5 * A * ap**2 + 0.5 * B * bp**2,
        "angular_scalar": 0.5 * C * a**2 * (1.0 - k) ** 2 / radius**2,
        "gauge_curvature": 0.5 * G * kp**2 / radius**2,
        "potential": potential(a, b),
    }
    parts = {name: float(2.0 * np.pi * np.trapezoid(value * radius, radius)) for name, value in densities.items()}
    tension = sum(parts.values())
    virial = abs(parts["gauge_curvature"] - parts["potential"])

    # The endpoint SO(3) rotation has angle 2pi/3; its SU(2) lift has order six.
    lift = np.array([0.5, 0.5, 0.5, 0.5])
    def multiply(x, y):
        return np.concatenate([[x[0] * y[0] - np.dot(x[1:], y[1:])], x[0] * y[1:] + y[0] * x[1:] + np.cross(x[1:], y[1:])])
    powers = [np.array([1.0, 0.0, 0.0, 0.0])]
    for _ in range(6): powers.append(multiply(powers[-1], lift))

    sample_radii = np.array([1.0e-5, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 15.0])
    sample = solution.sol(sample_radii)
    result = {
        "gate": "version6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate",
        "topology": {
            "vacuum_manifold": "SO(3)/Z3", "pi1": "Z6", "pi2": "0", "pi3": "Z",
            "SU2_lift_cube_minus_identity_residual": float(np.linalg.norm(powers[3] - np.array([-1.0, 0.0, 0.0, 0.0]))),
            "SU2_lift_sixth_identity_residual": float(np.linalg.norm(powers[6] - powers[0])),
            "isolated_RP2_hedgehog_is_full_vacuum_charge": False,
        },
        "ansatz": {
            "formula": "Q=Q*, T=b(r)T0+a(r)rho(exp(theta J/3))T3, B=-(K(r)/3)J dtheta",
            "winding_norm_squared": A, "invariant_norm_squared": B,
            "gauge_trace_norm": G,
        },
        "profile": {
            "solver_status": int(solution.status), "mesh_nodes": int(solution.x.size),
            "maximum_relative_residual": float(np.max(solution.rms_residuals)),
            "boundary_residual": float(np.linalg.norm(boundary(solution.y[:, 0], solution.y[:, -1]))),
            "core_b": float(b[0]), "core_a_slope": float(ap[0]),
            "dimensionless_tension": tension, "energy_parts": parts,
            "relative_virial_residual": virial / tension,
            "samples": {"r": sample_radii.tolist(), "K": sample[0].tolist(), "a": sample[2].tolist(), "b": sample[4].tolist()},
        },
        "boundary": {
            "absolute_scale_derived": False, "full_stability_derived": False,
            "localized_fermion_modes_derived": False,
        },
        "verdict": {
            "finite_Z6_vortex_profile_passes": True, "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate",
        },
    }
    assert solution.status == 0
    assert result["profile"]["relative_virial_residual"] < 1.0e-6
    assert 3.10 < tension < 3.12
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__": main()