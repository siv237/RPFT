#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate",
        "exact_matching": {
            "required_mu_spec_over_Lambda43": "exp(-32*pi^2/3)/42",
            "direct_required_g_squared_at_beta_2": "-4*pi^2/log(42)",
            "direct_required_beta_at_g_squared_3_over_8": "-64*pi^2/(3*log(42))",
            "reverse_required_g_squared_at_beta_2": "4*pi^2/log(42)",
            "reverse_required_beta_at_g_squared_3_over_8": "64*pi^2/(3*log(42))",
        },
        "audit": {"branches": 5, "criteria": 6, "rank": 5, "complete_passes": 0},
        "scale_audit": {
            "unanchored_rank_nullity": "2/2",
            "after_c_anchor_rank_nullity": "3/1",
            "after_independent_Lambda43_anchor": "4/0",
            "residual_kernel_after_c": [int(x) for x in c.speed_anchored_kernel],
        },
        "status": {
            "conditional_architecture": "8/8",
            "matching_branches": "0/5",
            "physical_origin": "0/5",
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
            "a_conditional_relative_scale_bridge_exists": True,
            "direct_matching_preserves_positive_inherited_parameters": False,
            "reverse_matching_preserves_inherited_rg_data": False,
            "the_required_bridge_has_an_internal_origin": False,
            "absolute_birth_tick_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()