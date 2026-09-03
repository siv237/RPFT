#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate",
        "inherited_rg": {
            "beta_coefficient": "2",
            "boundary_coupling_squared": "3/8",
            "log_Lambda_L_over_mu_spec": "32*pi^2/3",
            "log_m_DT_over_mu_spec_squared": "64*pi^2/3",
        },
        "tick_candidate": {
            "omega_DT": "c*mu_spec*exp(32*pi^2/3)",
            "tau_DT": "exp(-32*pi^2/3)/(c*mu_spec)",
            "tau_DT_c_mu_spec": "exp(-32*pi^2/3)",
        },
        "k43_compatibility": {
            "established_tau_birth_c_Lambda43": "42",
            "naive_identification": "mu_spec=Lambda43",
            "compatible": False,
            "mismatch_factor": "42*exp(32*pi^2/3)",
        },
        "parent": {
            "invariant_coordinates": 3,
            "hessian": "I3",
            "rank": 3,
            "determinant": 1,
        },
        "scale_audit": {
            "unanchored_rank_nullity": "3/2",
            "after_c_anchor_rank_nullity": "4/1",
            "after_independent_mu_spec_anchor": "5/0",
            "residual_kernel_after_c": [int(value) for value in certificate.speed_anchored_kernel],
        },
        "status": {
            "conditional_architecture": "9/9",
            "historical_rg_data": "2/2",
            "typed_rg_transfer_to_bath": "0/1",
            "physical_origin": "0/4",
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
            "dimensional_transmutation_defines_a_relative_tick": True,
            "dimensional_transmutation_fixes_mu_spec": False,
            "naive_k43_identification_is_compatible": False,
            "absolute_birth_tick_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_k43_rg_boundary_matching_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()