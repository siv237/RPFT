#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (10, 6)
    assert certificate.candidate_matrix.rank() == 6
    assert certificate.pass_vector == sp.zeros(10, 1)
    assert certificate.affinity_map.rank() == 2
    assert certificate.affinity_map * certificate.affinity_kernel == sp.zeros(2, 1)
    assert certificate.temperature_map.rank() == 2
    assert certificate.temperature_map * certificate.temperature_kernel == sp.zeros(2, 1)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "candidates": [
            "Hopf_one_edge_two_edge_path_lengths",
            "chain_number_levels_one_two",
            "Gibbs_normalization",
            "equal_downward_probability_one_sixth",
            "stationary_population_vector",
            "entropy_production",
            "clock_energy",
            "spectral_cutoff",
            "conditional_dimensional_transmutation",
            "observed_thermal_datum",
        ],
        "criteria": [
            "correct_dimensionless_affinity_type",
            "internally_available",
            "typed_to_both_reservoirs",
            "selects_common_affinity_offset",
            "preserves_positive_CPTP_channel",
            "supplies_physical_energy_temperature_unit",
        ],
        "candidate_matrix": [list(map(int, certificate.candidate_matrix.row(i))) for i in range(10)],
        "candidate_scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": 6,
        "passing_candidates": 0,
        "maximum_score": "4/6",
        "closest_candidate": {
            "name": "Hopf_one_edge_two_edge_path_lengths",
            "affinities": ["log(2)", "2*log(2)"],
            "missing": ["typed_reservoir_path_assignment", "physical_energy_temperature_unit"],
        },
        "residual_orbits": {
            "common_affinity_rank_nullity": "2/1",
            "common_affinity_kernel": [1, 1, 0],
            "energy_temperature_rank_nullity": "2/1",
            "energy_temperature_kernel": [-1, -1, 1],
        },
        "status": {
            "candidate_coverage": "10/10",
            "criterion_rank": "6/6",
            "common_affinity_offset_origin": "0/1",
            "physical_temperature_origin": "0/1",
            "origin_ledger": "4/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "Hopf_path_lengths_numerically_reproduce_both_affinities": True,
            "existing_parent_types_paths_to_reservoirs": False,
            "dimensionless_affinities_determine_physical_temperatures": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()