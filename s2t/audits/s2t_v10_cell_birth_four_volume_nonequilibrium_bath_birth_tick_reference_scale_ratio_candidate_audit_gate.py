#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    names = [
        "formal_Landau_times_K43_product", "K43_inverse_endpoint",
        "Landau_suppression", "Brillouin_K43_ratio", "bath_profile_ratio",
        "KMS_Boltzmann_ratio", "trace_anomaly_fraction",
        "normalized_birth_probability", "free_symbolic_bridge",
        "observed_matching_ratio", "external_renormalization_condition",
    ]
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate",
        "required_ratio": "exp(-32*pi^2/3)/42",
        "factorization": {
            "Landau_factor": "exp(-32*pi^2/3)",
            "K43_factor": "1/42",
            "formal_product_is_exact": True,
            "composition_parent_rank_nullity": "1/2",
        },
        "candidates": [
            {"name": name, "score": int(c.score_vector[i]), "pass": bool(c.pass_vector[i])}
            for i, name in enumerate(names)
        ],
        "audit": {"matrix_shape": "11x6", "rank": 5, "complete_passes": 0, "maximum_score": 5},
        "scale_audit": {"rank_nullity": "2/2", "kernel_columns": [[int(c.scale_kernel[i, j]) for i in range(4)] for j in range(2)]},
        "status": {
            "candidate_coverage": "11/11", "complete_candidates": "0/11",
            "origin_ledger": "3/6", "common_parent_origin": "0/1",
            "absolute_birth_tick_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked", "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256, "floating_point_values": 0,
        },
        "verdict": {
            "the_required_ratio_factorizes_exactly": True,
            "factorization_is_an_independent_origin": False,
            "an_internal_candidate_selects_the_full_ratio": False,
            "absolute_birth_tick_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()