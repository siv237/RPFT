#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_common_parent_reopening import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_common_parent_reopening_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate",
        "reopened_sources": [
            "version5_topological_closure_deficit_gate",
            "version5_local_defect_transfer_operator_gate",
            "version6_projective_order_parameter_field_spectrum_gate",
            "version6_spatial_projective_defect_energy_spectrum_gate",
            "version6_bosonic_defect_curved_string_effective_action_gate",
        ],
        "topological_dislocation": {
            "fredholm_domain_dimension": 90,
            "fredholm_codomain_dimension": 105,
            "kernel_dimension": 0,
            "cokernel_dimension": 15,
            "index": -15,
            "normalized_closure_deficit": "1/7",
        },
        "conditional_wrinkle": {
            "energy": "E(L)=L+1/L",
            "stationary_radius": 1,
            "stationary_energy": 2,
            "radial_curvature": 2,
        },
        "common_parent": {
            "inherited_hessian": [[2, 0], [0, 0]],
            "inherited_rank": int(certificate.inherited_parent_hessian.rank()),
            "inherited_nullity": 1,
            "mixed_block": 0,
            "conditional_hessian": [[2, 1], [1, 1]],
            "conditional_determinant": 1,
        },
        "status": {
            "joint_requirements_consistent": "8/8",
            "topological_defect_exact": "7/7",
            "conditional_wrinkle_stationary": "3/3",
            "physical_common_parent_origin": "0/3",
            "strict_particle_closure": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "wrinkle_and_dislocation_are_compatible": True,
            "wrinkle_and_dislocation_share_an_inherited_parent": False,
            "index_defect_is_localized_by_the_wrinkle": False,
            "profile_energy_equals_a_derived_spectral_pole": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()