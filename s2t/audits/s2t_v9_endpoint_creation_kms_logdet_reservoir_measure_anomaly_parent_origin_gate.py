#!/usr/bin/env python3
"""Exact ProofDSL audit of reservoir measure-anomaly origin."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from s2t.proofdsl.examples.version9_kms_reservoir_measure_anomaly_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
STEM = "endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate"
OUTPUT = ROOT / f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate_results.json").read_text())
    gate = f"version9_{STEM}"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate
    certificate = build_certificate()
    verified = verify_gate(SPEC)
    result = {
        "date": "2026-09-01", "gate": gate, "predecessor": predecessor["gate"],
        "jacobians": {
            "paired_vector_like": 1,
            "same_direction": "det(S)^-2",
            "target_loaded_isotropic_rescaling": "S=r^-1/2 I10 gives J=r^10",
        },
        "anomaly_coefficients": {
            "target": [1, 1, 3, 1, 1, 3],
            "type": [1, -1, 3, 1, -1, 3],
            "package": [1, 1, 3, -1, -1, -3],
            "product": [1, -1, 3, -1, 1, -3],
            "inherited_rank": 3, "rank_with_target": 4,
            "isotropic_traces": {"type": 6, "package": 0, "product": 0, "target": 10},
        },
        "proofdsl": {
            "status": "lcf-checked", "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256, "floating_point_values": 0,
        },
        "ledgers": {
            "paired_measure_covariance_satisfied": 1, "paired_measure_covariance_tested": 1,
            "inherited_anomaly_candidates_satisfied": 0, "inherited_anomaly_candidates_tested": 3,
            "target_loaded_rescaling_satisfied": 1, "target_loaded_rescaling_tested": 1,
            "physical_measure_anomaly_origin_satisfied": 0, "physical_measure_anomaly_origin_tested": 1,
            "physical_logdet_parent_satisfied": 0, "physical_logdet_parent_tested": 1,
        },
        "verdict": {
            "paired_measure_is_anomalous": False,
            "inherited_gradings_reproduce_target": False,
            "all_positive_target_trace_requires_identity_direction": True,
            "identity_rescaling_is_target_loaded": True,
            "physical_measure_anomaly_origin_derived": False,
        },
        "next_gate": "version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)


if __name__ == "__main__": main()