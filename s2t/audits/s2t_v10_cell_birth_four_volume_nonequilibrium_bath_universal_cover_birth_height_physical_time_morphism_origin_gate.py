#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate",
        "affine_time_readout": {
            "law": "t_n=t_0+n tau_birth",
            "normalized_height_values": [int(value) for value in certificate.height],
            "readout_rank": 2,
            "edge_difference_rank_nullity": "1/1",
            "origin_edge_effect": [int(value) for value in certificate.origin_edge_effect],
            "tick_edge_effect": [int(value) for value in certificate.tick_edge_effect],
            "additive_time_origin_is_gauge": True,
        },
        "clock_metric_parent": {
            "relations": [
                "E_C tau_birth/hbar=1",
                "c tau_birth/ell_edge=1",
                "E_C ell_edge/(hbar c)=1",
            ],
            "third_relation_is_dependent": True,
            "invariant_hessian": "I_3",
            "invariant_rank": 3,
            "dimensional_rank_nullity": "2/2",
            "after_c_anchor": "3/1",
            "after_c_and_length_anchors": "4/0",
        },
        "status": {
            "conditional_affine_time_morphism": "10/10",
            "relative_tick_compatibility": "3/3",
            "additive_origin_gauge_identified": "1/1",
            "physical_time_readout_origin": "0/1",
            "absolute_birth_tick_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "cover_height_admits_a_typed_affine_time_readout": True,
            "time_intervals_are_independent_of_additive_origin": True,
            "clock_and_edge_relations_are_mutually_compatible": True,
            "relations_select_absolute_tick_duration": False,
            "relations_select_absolute_clock_energy": False,
            "physical_identification_of_height_with_time_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()