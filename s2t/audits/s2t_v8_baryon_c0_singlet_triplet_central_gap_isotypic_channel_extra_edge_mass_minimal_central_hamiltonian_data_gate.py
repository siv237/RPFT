#!/usr/bin/env python3
"""Exact minimal central Hamiltonian data for the three extra-edge weights."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate_results.json").read_text(encoding="utf-8")
    )
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate"
    assert previous["next_gate"] == gate

    beta = sp.symbols("beta", positive=True)
    eps_y, eps_u, eps_d = sp.symbols("epsilon_Y epsilon_u epsilon_d", real=True)
    delta_u = eps_u - eps_y
    delta_d = eps_d - eps_y
    theta_u, theta_d = sp.symbols("theta_u theta_d", real=True)

    # Real-completed carrier projectors of ranks 4, 6, and 6.
    p_y = sp.diag(*([1] * 4 + [0] * 12))
    p_u = sp.diag(*([0] * 4 + [1] * 6 + [0] * 6))
    p_d = sp.diag(*([0] * 10 + [1] * 6))
    identity = sp.eye(16)
    h = eps_y * p_y + eps_u * p_u + eps_d * p_d
    assert h == eps_y * identity + delta_u * p_u + delta_d * p_d

    shift = sp.symbols("b", real=True)
    shifted = h + shift * identity
    boltzmann = sp.Matrix([
        sp.exp(-beta * eps_y),
        sp.exp(-beta * eps_u),
        sp.exp(-beta * eps_d),
    ])
    partition = 4 * boltzmann[0] + 6 * boltzmann[1] + 6 * boltzmann[2]
    rho = boltzmann / partition
    shifted_boltzmann = sp.exp(-beta * shift) * boltzmann
    shifted_partition = 4 * shifted_boltzmann[0] + 6 * shifted_boltzmann[1] + 6 * shifted_boltzmann[2]
    rho_shifted = shifted_boltzmann / shifted_partition
    assert sp.simplify(rho_shifted - rho) == sp.zeros(3, 1)

    # Projective central weights: common block multiplicities cancel from
    # the eigenvalue-density ratios.
    a = sp.exp(-theta_u)
    b = sp.exp(-theta_d)
    z = 1 + a + b
    weights = sp.Matrix([1 / z, a / z, b / z])
    assert sp.simplify(sum(weights) - 1) == 0
    inverse_u = sp.log(weights[0] / weights[1])
    inverse_d = sp.log(weights[0] / weights[2])
    assert sp.simplify(inverse_u - theta_u) == 0
    assert sp.simplify(inverse_d - theta_d) == 0

    jacobian = sp.simplify(sp.Matrix([weights[1], weights[2]]).jacobian([theta_u, theta_d]))
    jacobian_det = sp.factor(jacobian.det())
    assert sp.simplify(jacobian_det - weights[0] * weights[1] * weights[2]) == 0
    assert jacobian.subs({theta_u: 0, theta_d: 0}).det() == sp.Rational(1, 27)

    # Three exact witnesses in the simplex.
    counting = sp.simplify(weights.subs({theta_u: 0, theta_d: 0}))
    equal_mass = sp.simplify(weights.subs({theta_u: sp.log(sp.Rational(3, 2)), theta_d: sp.log(sp.Rational(3, 2))}))
    asymmetric = sp.simplify(weights.subs({theta_u: sp.log(sp.Rational(3, 2)), theta_d: sp.log(3)}))
    assert counting == sp.Matrix([sp.Rational(1, 3)] * 3)
    assert equal_mass == sp.Matrix([sp.Rational(3, 7), sp.Rational(2, 7), sp.Rational(2, 7)])
    assert asymmetric == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)])

    # Strict convexity of the projective Gibbs free energy.
    q_u, q_d = sp.symbols("q_u q_d", positive=True)
    q_y = 1 - q_u - q_d
    free_energy = sp.expand(theta_u * q_u + theta_d * q_d + q_y * sp.log(q_y) + q_u * sp.log(q_u) + q_d * sp.log(q_d))
    free_hessian = sp.simplify(sp.hessian(free_energy, (q_u, q_d)))
    free_det = sp.factor(free_hessian.det())
    assert sp.simplify(free_det - 1 / (q_d * q_u * q_y)) == 0
    assert free_hessian.subs({q_u: sp.Rational(1, 3), q_d: sp.Rational(1, 3)}) == sp.Matrix([[6, 3], [3, 6]])

    # Traceless gauge fixes only the additive representative, not the gaps.
    trace_constraint = sp.Matrix([[4, 6, 6]])
    assert trace_constraint.rank() == 1
    assert len(trace_constraint.nullspace()) == 2

    scale = sp.symbols("c", positive=True)
    assert sp.simplify((beta / scale) * (scale * delta_u) - beta * delta_u) == 0
    assert sp.simplify((beta / scale) * (scale * delta_d) - beta * delta_d) == 0

    alpha = sp.symbols("alpha", positive=True)
    mass_vector = sp.Matrix([2 * alpha * weights[0], 3 * alpha * weights[1], 3 * alpha * weights[2]])
    assert sp.simplify(mass_vector.subs({theta_u: 0, theta_d: 0}) - sp.Matrix([2 * alpha / 3, alpha, alpha])) == sp.zeros(3, 1)

    exact_objects = [
        p_y, p_u, p_d, identity, h, shifted, rho, weights, jacobian,
        counting, equal_mass, asymmetric, free_energy, free_hessian,
        trace_constraint, mass_vector,
    ]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "admissible_central_hamiltonian": {
            "form": "epsilon_Y P_Y + epsilon_u P_u + epsilon_d P_d",
            "shift_quotient_form": "epsilon_Y I16 + Delta_u P_u + Delta_d P_d",
            "real_completed_ranks": [4, 6, 6],
            "additive_energy_shift_relevant": False,
            "gap_dimension": 2,
        },
        "minimal_dimensionless_selector": {
            "coordinates": ["theta_u=beta Delta_u", "theta_d=beta Delta_d"],
            "weights": [str(value) for value in weights],
            "inverse": ["theta_u=log(p_Y/p_u)", "theta_d=log(p_Y/p_d)"],
            "jacobian_determinant": "p_Y p_u p_d",
            "diffeomorphism": "R^2 to interior(Delta^2)",
            "necessary_parameters": 2,
            "sufficient_parameters": 2,
        },
        "exact_witnesses": {
            "counting_trace": {"theta": [0, 0], "weights": [str(value) for value in counting]},
            "equal_edge_mass": {"theta": ["log(3/2)", "log(3/2)"], "weights": [str(value) for value in equal_mass]},
            "asymmetric_point": {"theta": ["log(3/2)", "log(3)"], "weights": [str(value) for value in asymmetric]},
        },
        "gibbs_variational_test": {
            "functional": "theta_u p_u + theta_d p_d + sum_e p_e log(p_e)",
            "hessian_determinant": "1/(p_Y p_u p_d)",
            "counting_point_hessian": [[6, 3], [3, 6]],
            "unique_minimizer_for_each_gap_pair": True,
        },
        "identifiability": {
            "equilibrium_determines_two_beta_gap_products": True,
            "beta_and_physical_gaps_separately_determined": False,
            "common_scaling_orbit": "(beta,Delta_u,Delta_d)->(beta/c,c Delta_u,c Delta_d)",
            "traceless_representative_removes_only_common_shift": True,
            "overall_stabilizing_mass_scale_alpha_determined": False,
            "relaxation_time_determined": False,
        },
        "mass_parameterization": {
            "form": [str(value) for value in mass_vector],
            "relative_weights_controlled_by_theta_pair": True,
            "overall_scale": "alpha>0",
        },
        "ledgers": {
            "minimal_hamiltonian_architecture_satisfied": 7,
            "minimal_hamiltonian_architecture_tested": 7,
            "relative_gap_origin_satisfied": 0,
            "relative_gap_origin_tested": 2,
            "energy_scale_origin_satisfied": 0,
            "energy_scale_origin_tested": 1,
            "mass_scale_origin_satisfied": 0,
            "mass_scale_origin_tested": 1,
            "relaxation_scale_origin_satisfied": 0,
            "relaxation_scale_origin_tested": 1,
        },
        "verdict": {
            "two_dimensionless_gaps_are_minimal": True,
            "two_dimensionless_gaps_are_sufficient": True,
            "counting_trace_corresponds_to_zero_gaps": True,
            "equal_mass_corresponds_to_equal_nonzero_gaps": True,
            "gap_values_derived_by_current_parent": False,
            "absolute_energy_scale_derived": False,
            "absolute_mass_scale_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()