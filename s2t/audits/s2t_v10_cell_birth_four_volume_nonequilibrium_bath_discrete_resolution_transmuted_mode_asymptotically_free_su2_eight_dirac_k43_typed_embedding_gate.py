#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate",
        "K43_decomposition": {"active_SU2_doublet_sector": 32, "Weyl_doublets": 16, "Dirac_doublets": 8, "singlet_complement": 11},
        "representation": {"Casimir": "3/4", "trace_gram": "8*I3", "fermion_Dynkin_index": 8, "commutant_dimension": 377},
        "renormalization": {"gauge_contribution": "-22/3", "fermion_contribution": "16/3", "beta": "-2"},
        "anomalies": {"local_cubic_tensor": "0_27", "Witten_parity": 0},
        "pole_compatibility": {
            "active_rank_one_pole_gauge_defect": 1,
            "singlet_rank_one_pole_gauge_defect": 0,
            "singlet_rank_one_pole_active_overlap_rank": 0,
            "minimal_invariant_active_projector_rank": 2,
        },
        "status": {"conditional_embedding_architecture": "12/12", "exact_beta": "1/1", "anomaly_checks": "2/2", "active_invariant_rank_one_pole": "0/1", "physical_origin": "0/3"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {
            "SU2_eight_Dirac_embeds_in_K43": True,
            "embedding_has_exact_beta_minus_two": True,
            "embedding_is_anomaly_free": True,
            "active_rank_one_pole_is_gauge_invariant": False,
            "gauge_invariant_rank_one_pole_is_AF_active": False,
            "physical_embedding_is_parent_selected": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()