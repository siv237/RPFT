#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_particle_wrinkle_dislocation_common_parent_reopening_gate",
        "criteria": [
            "typed_common_carrier",
            "nonzero_mixed_block",
            "index_preservation",
            "finite_localization",
            "same_operator_spectral_pole",
            "inherited_and_not_target_loaded",
        ],
        "candidates": [
            "inherited_direct_sum",
            "scalar_trace_product",
            "projector_curvature_pairing",
            "toeplitz_spatial_boundary_product",
            "graded_morita_two_step_connector",
            "hopf_chern_pairing",
            "callias_mass_profile",
            "K43_cell_incidence",
            "bath_covariance_response",
            "inherited_higgs_rank_change_portal",
            "target_loaded_pole_match",
        ],
        "scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": int(certificate.candidate_matrix.rank()),
        "strict_pass_count": int(sum(certificate.pass_vector)),
        "inherited_pass_count": int(sum(certificate.inherited_pass_vector)),
        "best_structural_candidate": {
            "name": "callias_mass_profile",
            "score": 5,
            "localized_channel_rank": int(certificate.callias_localization_projector.rank()),
            "conditional_hessian_determinant": int(certificate.conditional_callias_hessian.det()),
            "missing_criterion": "inherited_and_not_target_loaded",
        },
        "closed_routes": {
            "graded_product_mixed_block": "zero",
            "centered_morita_mixed_block": "zero",
            "inherited_hessian_rank_nullity": "1/1",
        },
        "status": {
            "audit_coverage": "11/11",
            "strict_candidate_pass": "0/11",
            "inherited_candidate_pass": "0/11",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "existing_mixed_bridge_closes_particle": False,
            "callias_profile_is_structurally_complete": True,
            "callias_profile_is_inherited": False,
            "target_loaded_match_is_admissible": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()