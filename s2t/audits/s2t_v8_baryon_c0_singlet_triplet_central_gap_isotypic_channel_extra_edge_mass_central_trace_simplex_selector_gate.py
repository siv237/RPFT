#!/usr/bin/env python3
"""Exact selector audit for the three-component central trace simplex."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate"
    assert previous["next_gate"] == gate

    # Order: Y, u, d.  The Real-completed block dimensions are twice the
    # complex representation dimensions.
    d = sp.Matrix([2, 3, 3])
    n = 2 * d
    p_y, p_u, p_d = sp.symbols("p_Y p_u p_d", positive=True)
    p = sp.Matrix([p_y, p_u, p_d])
    mu = sp.diag(*d) * p

    counting = sp.Matrix([sp.Rational(1, 3)] * 3)
    equal_mass = sp.Matrix([sp.Rational(3, 7), sp.Rational(2, 7), sp.Rational(2, 7)])
    assert sum(counting) == 1 and sum(equal_mass) == 1
    mu_counting = sp.diag(*d) * counting
    mu_equal_mass = sp.diag(*d) * equal_mass
    assert mu_counting == sp.Matrix([sp.Rational(2, 3), 1, 1])
    assert mu_equal_mass == sp.Matrix([sp.Rational(6, 7)] * 3)
    assert mu_counting.cross(mu_equal_mass) != sp.zeros(3, 1)

    # Maximum von Neumann entropy of a central density on the 4+6+6 carrier
    # gives equal microscopic eigenvalues, hence equal central density.
    rho_y, rho_u, rho_d = sp.symbols("rho_Y rho_u rho_d", positive=True)
    rho = sp.Matrix([rho_y, rho_u, rho_d])
    entropy = -sum(n[i] * rho[i] * sp.log(rho[i]) for i in range(3))
    rho_star = sp.Matrix([sp.Rational(1, 16)] * 3)
    assert (n.dot(rho_star)) == 1
    entropy_hessian = sp.hessian(entropy, (rho_y, rho_u, rho_d)).subs(dict(zip(rho, rho_star)))
    assert entropy_hessian == sp.diag(-64, -96, -96)
    assert all(value < 0 for value in entropy_hessian.diagonal())

    # Type-preserving symmetry acts trivially on the three central rays.
    representation_signatures = ("(1,2)_{1/2}", "(3,1)_{5/3}", "(3,1)_{2/3}")
    assert len(set(representation_signatures)) == 3
    center_fixed_dimension = 3

    # Unimodularity removes one phase direction on the 4+6+6 carrier but is
    # independent of the positive trace weights.
    unimodularity_row = sp.Matrix([[4, 6, 6]])
    assert unimodularity_row.rank() == 1
    assert len(unimodularity_row.nullspace()) == 2
    assert all(sp.diff(entry, variable) == 0 for entry in unimodularity_row for variable in p)

    gauge_indices = sp.Matrix([
        [sp.Rational(1, 2), sp.Rational(25, 3), sp.Rational(4, 3)],
        [sp.Rational(1, 2), 0, 0],
        [0, sp.Rational(1, 2), sp.Rational(1, 2)],
    ])
    assert gauge_indices.det() == -sp.Rational(7, 4)
    gauge_counting = gauge_indices * counting
    gauge_equal_mass = gauge_indices * equal_mass
    assert gauge_counting == sp.Matrix([sp.Rational(61, 18), sp.Rational(1, 6), sp.Rational(1, 3)])
    assert gauge_equal_mass == sp.Matrix([sp.Rational(125, 42), sp.Rational(3, 14), sp.Rational(2, 7)])

    # Every positive central density is a Gibbs density for two independent
    # energy gaps.  The equal-mass witness needs two equal nonzero gaps.
    beta = sp.symbols("beta", positive=True)
    gap_u = sp.log(sp.Rational(3, 2)) / beta
    gap_d = sp.log(sp.Rational(3, 2)) / beta
    assert sp.simplify(sp.exp(-beta * gap_u) - sp.Rational(2, 3)) == 0
    assert sp.simplify(sp.exp(-beta * gap_d) - sp.Rational(2, 3)) == 0

    # At the physical z=0 vacuum the trace weights are exactly flat.
    x_y, y_y, x_u, y_u, x_d, y_d = sp.symbols("x_Y y_Y x_u y_u x_d y_d", real=True)
    amplitudes = sp.Matrix([
        d[0] * (x_y**2 + y_y**2),
        d[1] * (x_u**2 + y_u**2),
        d[2] * (x_d**2 + y_d**2),
    ])
    trace_action = sp.expand(p.dot(amplitudes))
    vacuum = {x_y: 0, y_y: 0, x_u: 0, y_u: 0, x_d: 0, y_d: 0}
    weight_gradient = sp.Matrix([sp.diff(trace_action, variable) for variable in p]).subs(vacuum)
    weight_hessian = sp.hessian(trace_action, (p_y, p_u, p_d)).subs(vacuum)
    assert weight_gradient == sp.zeros(3, 1)
    assert weight_hessian == sp.zeros(3)

    exact_objects = [
        d, n, p, mu, counting, equal_mass, mu_counting, mu_equal_mass,
        entropy, rho_star, entropy_hessian, unimodularity_row, gauge_indices,
        gauge_counting, gauge_equal_mass, gap_u, gap_d, trace_action,
        weight_gradient, weight_hessian,
    ]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "central_simplex": {
            "normalized_coordinates": "p_Y+p_u+p_d=1",
            "mass_vector": [str(value) for value in mu],
            "projective_dimension": 2,
            "center_fixed_dimension_under_type_preserving_symmetry": center_fixed_dimension,
        },
        "competing_conventions": {
            "equal_microscopic_trace_density": {
                "weights": [str(value) for value in counting],
                "mass_coefficients": [str(value) for value in mu_counting],
                "ratio": "2:3:3",
            },
            "equal_edge_mass": {
                "weights": [str(value) for value in equal_mass],
                "mass_coefficients": [str(value) for value in mu_equal_mass],
                "ratio": "1:1:1",
            },
            "vectors_proportional": False,
        },
        "maximum_entropy_test": {
            "real_completed_dimensions": [int(value) for value in n],
            "maximizer_eigenvalue_density": [str(value) for value in rho_star],
            "hessian_diagonal": [str(value) for value in entropy_hessian.diagonal()],
            "selects_equal_microscopic_density_conditionally": True,
            "entropy_principle_present_in_parent": False,
        },
        "unimodularity_test": {
            "phase_constraint": "4 theta_Y + 6 theta_u + 6 theta_d = 0",
            "constraint_rank": unimodularity_row.rank(),
            "phase_nullity": len(unimodularity_row.nullspace()),
            "depends_on_positive_trace_weights": False,
        },
        "gauge_matching_test": {
            "index_matrix_determinant": str(gauge_indices.det()),
            "index_matrix_rank": gauge_indices.rank(),
            "counting_trace_image": [str(value) for value in gauge_counting],
            "equal_mass_trace_image": [str(value) for value in gauge_equal_mass],
            "requires_external_gauge_target": True,
            "intrinsic_selector": False,
        },
        "gibbs_test": {
            "independent_dimensionless_gaps": 2,
            "equal_mass_witness_gaps": ["log(3/2)/beta", "log(3/2)/beta"],
            "realizes_whole_positive_simplex": True,
            "gap_parent_origin_present": False,
        },
        "stationarity_test": {
            "vacuum_weight_gradient": [str(value) for value in weight_gradient],
            "vacuum_weight_hessian_rank": weight_hessian.rank(),
            "vacuum_selects_trace_point": False,
        },
        "ledgers": {
            "conditional_trace_conventions_satisfied": 2,
            "conditional_trace_conventions_tested": 2,
            "intrinsic_simplex_selectors_satisfied": 0,
            "intrinsic_simplex_selectors_tested": 8,
            "minimal_new_relative_parameters": 2,
        },
        "verdict": {
            "counting_trace_is_a_valid_candidate": True,
            "maximum_entropy_reproduces_counting_trace": True,
            "equal_edge_mass_is_another_valid_candidate": True,
            "gauge_symmetry_selects_weights": False,
            "unimodularity_selects_weights": False,
            "gauge_matching_is_blind": False,
            "kms_selects_weights_without_gaps": False,
            "vacuum_stationarity_selects_weights": False,
            "central_trace_simplex_closed": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()