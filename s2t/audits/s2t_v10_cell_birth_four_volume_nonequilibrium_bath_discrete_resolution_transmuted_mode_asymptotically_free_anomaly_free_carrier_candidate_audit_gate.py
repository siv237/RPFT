#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate",
        "required_beta": "-2",
        "existing_nonabelian_betas": {"SM_SU2": "-19/6", "SM_SU3": "-7"},
        "restricted_fundamental_solutions": [
            {"SU_N": int(row[0]), "Dirac_fundamentals": int(row[1]), "complex_scalar_fundamentals": int(row[2]), "complexity": int(row[3]), "beta": "-2"}
            for row in c.fundamental_solution_table.tolist()
        ],
        "restricted_minimal_candidate": {"carrier": "SU2_plus_8_Dirac_fundamentals", "Weyl_doublets": 16, "Witten_parity": 0, "anomaly_free": True, "typed_in_K43": False, "coupled_to_pole_mode": False},
        "criteria": ["nonabelian_gauge_carrier", "anomaly_free", "internally_typed", "exact_beta_minus_two", "typed_pole_coupling", "parent_selected_content"],
        "candidate_matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
        "matrix_rank": int(c.candidate_matrix.rank()),
        "score_vector": [int(x) for x in c.score_vector],
        "pass_vector": [int(x) for x in c.pass_vector],
        "status": {"restricted_minimality": "1/1", "candidate_passes": "0/11", "physical_origin": "0/3"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {
            "existing_SM_nonabelian_sector_has_exact_beta": False,
            "restricted_minimal_anomaly_free_candidate_exists": True,
            "minimal_candidate_is_in_current_K43_carrier": False,
            "minimal_candidate_is_typed_to_transmuted_pole": False,
            "physical_AF_carrier_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()