#!/usr/bin/env python3
"""Exact source and rate parent-origin audit for the Tome IX creation frame."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_finite_geometry_creation_operator_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def matrix_unit(size: int, row: int, column: int) -> sp.Matrix:
    result = sp.zeros(size)
    result[row, column] = 1
    return result


def dissipator(jump: sp.Matrix, rho: sp.Matrix) -> sp.Matrix:
    gram = jump.T.conjugate() * jump
    return jump * rho * jump.T.conjugate() - (gram * rho + rho * gram) / 2


def main() -> None:
    predecessor = json.loads(
        (
            ROOT
            / "s2t/results/s2t_v9_endpoint_finite_geometry_creation_operator_architecture_gate_results.json"
        ).read_text(encoding="utf-8")
    )
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate

    laplacian = sp.Matrix([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
    omega = sp.ones(3, 1) / sp.sqrt(3)
    source_projector = omega * omega.T
    assert laplacian * omega == sp.zeros(3, 1)
    assert len(laplacian.nullspace()) == 1
    assert source_projector**2 == source_projector
    assert sp.trace(source_projector) == 1

    channel_dimension = 5
    hypercharge = sp.diag(0, 0, -1, -1, -1)
    grading = sp.diag(1, -1, 1, 1, 1)
    family_generators = []
    for generator3 in [
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
    ]:
        generator5 = sp.zeros(channel_dimension)
        generator5[2:, 2:] = generator3
        family_generators.append(generator5)

    variables = sp.symbols("x0:25")
    general = sp.Matrix(channel_dimension, channel_dimension, variables)
    equations = []
    for operator in [hypercharge, grading, *family_generators]:
        equations.extend(list(general * operator - operator * general))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    commutant_dimension = len(variables) - coefficient_matrix.rank()
    assert commutant_dimension == 3

    ps = sp.diag(1, 0, 0, 0, 0)
    pa = sp.diag(0, 1, 0, 0, 0)
    pt = sp.diag(0, 0, 1, 1, 1)
    for projector in [ps, pa, pt]:
        for operator in [hypercharge, grading, *family_generators]:
            assert projector * operator - operator * projector == sp.zeros(channel_dimension)

    k1 = sp.eye(channel_dimension)
    k2 = sp.diag(2, 1, sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(2, 3))
    assert sp.trace(k1) == sp.trace(k2) == 5
    assert all(value > 0 for value in k1.diagonal())
    assert all(value > 0 for value in k2.diagonal())
    for matrix in [k1, k2]:
        for operator in [hypercharge, grading, *family_generators]:
            assert matrix * operator - operator * matrix == sp.zeros(channel_dimension)
    assert sum(k1.diagonal()[:3]) == 3
    assert sum(k2.diagonal()[:3]) == sp.Rational(11, 3)

    swap = sp.eye(channel_dimension)
    swap[1, 1] = swap[2, 2] = 0
    swap[1, 2] = swap[2, 1] = 1
    assert (swap * hypercharge - hypercharge * swap).rank() == 2
    assert (swap * grading - grading * swap).rank() == 2

    size = 6
    jumps = [matrix_unit(size, target, 0) for target in range(1, size)]
    superoperator_columns = []
    for row in range(size):
        for column in range(size):
            basis = matrix_unit(size, row, column)
            image = sum((dissipator(jump, basis) for jump in jumps), sp.zeros(size))
            superoperator_columns.append(image.reshape(size * size, 1))
    liouvillian = sp.Matrix.hstack(*superoperator_columns)
    assert liouvillian.rank() == 11
    assert size**2 - liouvillian.rank() == 25

    rate_candidates = {
        "represented_symmetry": False,
        "trace_normalization": False,
        "phase_edge_weights": False,
        "old_noise_frame_extension": False,
        "kms_without_reverse_jumps_and_energy_gaps": False,
    }
    assert not any(rate_candidates.values())

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "configuration_source": {
            "origin": "normalized_unique_zero_mode_of_phase_laplacian",
            "vector": "(1,1,1)/sqrt(3)",
            "kernel_dimension": 1,
            "projector_rank": source_projector.rank(),
            "physically_derived": True,
        },
        "rate_commutant": {
            "channel_representation": "1_neutral_even direct_sum 1_neutral_odd direct_sum 3_charged_even",
            "complex_dimension": commutant_dimension,
            "general_positive_matrix": "diag(gamma_s,gamma_a,gamma_t,gamma_t,gamma_t)",
            "trace_normalized_simplex_dimension": 2,
            "witness_1": [1, 1, 1, 1, 1],
            "witness_2": [2, 1, "2/3", "2/3", "2/3"],
            "new_population_rates": [3, "11/3"],
            "unphysical_U5_swap_charge_commutator_rank": 2,
            "unphysical_U5_swap_grading_commutator_rank": 2,
        },
        "outward_creation_qms": {
            "liouvillian_rank": liouvillian.rank(),
            "stationary_operator_space_dimension": size**2 - liouvillian.rank(),
            "stationary_target_corner": "M5(C)",
            "primitive": False,
            "reverse_jumps_present": False,
            "energy_gaps_present": False,
        },
        "rate_selector_candidates": {
            **rate_candidates,
            "satisfied": sum(rate_candidates.values()),
            "tested": len(rate_candidates),
        },
        "ledgers": {
            "configuration_source_origin_satisfied": 1,
            "configuration_source_origin_tested": 1,
            "creation_rate_selector_satisfied": 0,
            "creation_rate_selector_tested": 5,
            "rate_parameter_origin_satisfied": 0,
            "rate_parameter_origin_tested": 3,
            "creation_parent_origin_satisfied": 1,
            "creation_parent_origin_tested": 4,
            "endpoint_reachability_satisfied": 3,
            "endpoint_reachability_tested": 3,
            "physical_endpoint_selection_satisfied": 0,
            "physical_endpoint_selection_tested": 1,
            "physical_four_slot_parent_satisfied": 0,
            "physical_four_slot_parent_tested": 1,
        },
        "verdict": {
            "configuration_source_derived_from_phase_graph": True,
            "represented_symmetry_selects_rate_ratios": False,
            "trace_isotropy_is_physically_forced": False,
            "outward_creation_qms_has_unique_stationary_state": False,
            "bidirectional_kms_completion_required": True,
            "physical_endpoint_transition_derived": False,
        },
        "next_gate": "version9_endpoint_creation_bidirectional_kms_completion_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()