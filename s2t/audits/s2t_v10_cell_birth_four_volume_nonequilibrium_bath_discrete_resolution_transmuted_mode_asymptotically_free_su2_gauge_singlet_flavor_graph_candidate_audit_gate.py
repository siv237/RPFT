#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_democratic_flavor_selector_parent_origin_gate",
        "criteria": [
            "sixteen_label_carrier",
            "unique_democratic_zero_mode",
            "non_scalar_graph_geometry",
            "inherited_edge_operator",
            "parent_selected_weight",
            "not_target_loaded",
        ],
        "candidates": [
            "zero_graph",
            "complete_K16",
            "cycle_C16",
            "path_P16",
            "hypercube_Q4",
            "complete_bipartite_K8_8",
            "K43_block_multiplicity_graph",
            "bath_covariance_graph",
            "fitted_weighted_graph",
            "target_loaded_K16",
        ],
        "scores": list(map(int, certificate.score_vector)),
        "strict_pass_count": int(sum(certificate.pass_vector)),
        "internal_origin_count": int(sum(certificate.internal_origin_vector)),
        "candidate_matrix_rank": int(certificate.candidate_matrix.rank()),
        "hypercube_Q4": {
            "vertices": 16,
            "degree": 4,
            "laplacian_spectrum": {"0": 1, "2": 4, "4": 6, "6": 4, "8": 1},
            "zero_mode_multiplicity": 1,
            "bit_flip_covariance_generators": 4,
            "missing_origin": "canonical_4_bit_labeling_and_edge_weight",
        },
        "status": {
            "audit_coverage": "10/10",
            "strict_candidate_pass": "0/10",
            "physical_origin": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "Q4_is_structurally_distinguished": True,
            "Q4_is_inherited_from_K43_multiplicity": False,
            "complete_K16_is_inherited": False,
            "strict_flavor_graph_origin_closed": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_hypercube_q4_flavor_graph_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()