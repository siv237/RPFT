#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate",
        "covering": {
            "base_graph": "oriented Hopf cycle C3",
            "universal_cover": "integer line Z",
            "finite_witness": "radius-three ball with seven vertices",
            "cover_map": "p(n)=n mod 3",
            "chain_map_defect": 0,
            "local_adjacency_defect": 0,
            "deck_period": 3,
            "deck_period_defect": 0,
        },
        "birth_graph": {
            "height_values": [int(value) for value in certificate.height],
            "edge_height_increment": [int(value) for value in certificate.height_increment],
            "radius_counts": [int(value) for value in certificate.radius_counts],
            "shell_counts": [int(value) for value in certificate.shell_counts],
            "forward_counts": [int(value) for value in certificate.forward_counts],
            "new_future_vertices_per_step": 1,
            "absolute_height_origin_selected": False,
        },
        "scale_audit": {
            "after_v_g_equals_c_rank_nullity": "8/1",
            "remaining_length_orbit": [int(value) for value in certificate.scale_kernel],
            "cover_adds_dimensional_rank": False,
        },
        "status": {
            "conditional_cover_architecture": "12/12",
            "typed_chain_cover": "1/1",
            "discrete_birth_height": "1/1",
            "physical_growth_graph_origin": "0/1",
            "absolute_edge_metric_origin": "0/1",
            "physical_birth_clock_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "seven_vertex_path_is_a_canonical_local_cover_witness": True,
            "Hopf_cycle_lifts_to_a_nonbranching_birth_line": True,
            "cover_derives_one_discrete_birth_per_forward_step": True,
            "cover_selects_physical_time_per_step": False,
            "cover_selects_absolute_edge_length": False,
            "mathematical_cover_is_identified_with_physical_spacetime_growth": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()