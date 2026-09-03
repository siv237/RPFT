#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate",
        "common_parent": {
            "invariants": [
                "v_cell/ell_cell^4=1",
                "E_C ell_cell/(hbar c)=1",
                "k_BZ ell_cell=pi",
                "omega_UV ell_cell/v_g=2 sqrt(3)",
                "Lambda_43 ell_cell=42",
                "v_g Delta_t/ell_edge=1",
                "ell_edge/ell_cell=1",
            ],
            "hessian": "I_7",
            "rank": 7,
            "determinant": 1,
            "derived_uv_phase_per_edge_step": "2 sqrt(3)",
        },
        "scale_audit": {
            "variable_order": ["v_cell", "E_C", "k_BZ", "omega_UV", "Lambda_43", "Delta_t", "v_g", "ell_cell", "ell_edge"],
            "rank_nullity": "7/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
            "after_v_g_equals_c_anchor": "8/1",
            "remaining_length_orbit": [int(value) for value in certificate.velocity_anchored_kernel],
            "after_independent_length_anchor": "9/0",
        },
        "status": {
            "conditional_common_parent": "11/11",
            "relative_edge_cell_identification": "1/1",
            "global_growth_complex_origin": "0/1",
            "absolute_edge_length_origin": "0/1",
            "damping_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "one_positive_parent_unifies_all_relative_edge_relations": True,
            "causal_speed_anchor_selects_absolute_edge_length": False,
            "four_volume_selects_absolute_edge_length": False,
            "spectral_cutoffs_select_absolute_edge_length": False,
            "independent_length_anchor_is_still_required": True,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()