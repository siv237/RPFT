#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_throughflow_scale_parent_admission_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_spectral_coefficient_origin_candidate_audit_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (12, 6)
    assert certificate.candidate_matrix.rank() == 6
    assert certificate.pass_vector == sp.zeros(12, 1)
    assert certificate.score_vector == sp.ImmutableMatrix([4, 4, 3, 4, 4, 3, 3, 4, 4, 5, 5, 4])
    assert certificate.component_assignment.rank() == 3
    assert certificate.component_pass_vector == sp.zeros(3, 1)
    assert certificate.package_dependency.rank() == 3
    assert certificate.package_availability == sp.zeros(3, 1)
    assert certificate.scale_map.rank() == 3
    assert certificate.scale_map * certificate.scale_vector == sp.zeros(3, 1)
    assert certificate.externally_anchored_map.rank() == 4

    candidates = [
        "epsilon_from_K43_oriented_trace_magnitude",
        "epsilon_from_induced_curvature_alpha",
        "epsilon_from_relative_U1_beta_two",
        "epsilon_from_cycle_entropy_log2",
        "b_A_from_K43_unit_geometric_beta",
        "b_A_from_relative_U1_beta_two",
        "b_A_from_heat_kernel_a4_log_coefficient",
        "b_A_from_KMS_logdet_measure_exponent",
        "mu_from_symbolic_mu_spec",
        "mu_from_finite_cell_spectral_cutoff",
        "mu_from_clock_KMS_energy",
        "mu_from_observed_inverse_Planck_length",
    ]
    result = {
        "date": "2026-09-02",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "components": ["epsilon", "b_A", "mu_spec"],
        "candidates": candidates,
        "criteria": [
            "correct_target_type",
            "exact_source_relation",
            "typed_current_carrier",
            "target_independent",
            "admitted_into_breathing_parent",
            "breaks_absolute_scale_orbit",
        ],
        "candidate_matrix": [
            list(map(int, certificate.candidate_matrix.row(index)))
            for index in range(certificate.candidate_matrix.rows)
        ],
        "candidate_scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": 6,
        "passing_candidates": 0,
        "maximum_score": "5/6",
        "component_audit": {
            "candidate_counts": {"epsilon": 4, "b_A": 4, "mu_spec": 4},
            "component_dependency_rank": 3,
            "complete_component_origins": "0/3",
            "complete_package_available": False,
        },
        "exact_partial_data": {
            "K43_oriented_trace_response": "A(1,0)=-1/6",
            "positive_trace_magnitude": "-A(1,0)=1/6",
            "K43_incoming_geometric_beta": "d exp(zeta)/dzeta at zeta=0 equals 1",
            "finite_cell_cutoff_relation": "Lambda*ell_cell=42",
        },
        "closest_routes": {
            "epsilon": "K43 trace magnitude is exact and typed, but no positive output-density morphism enters the breathing parent",
            "b_A": "K43 unit geometric beta is exact, but zeta is not typed as log(m/mu_spec^2)",
            "mu_spec": "spectral cutoff and clock energy score 5/6, but both preserve the absolute scale orbit",
        },
        "scale_orbit": {
            "variables": ["m", "mu_spec^2", "v_cell", "density/Theta"],
            "rank": 3,
            "nullity": 1,
            "kernel": [-1, -1, 2, -2],
            "external_reference_scale_row_rank": 4,
        },
        "status": {
            "candidate_coverage": "12/12",
            "criterion_rank": "6/6",
            "component_origins": "0/3",
            "complete_spectral_package": "0/1",
            "absolute_scale": "0/1",
            "origin_ledger": "3/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "existing_spectral_data_contain_partial_coefficients": True,
            "epsilon_origin_derived": False,
            "b_A_origin_derived": False,
            "mu_spec_origin_derived": False,
            "absolute_breathing_scale_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_output_density_morphism_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()