#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate",
        "beta_convention": "beta_g=b*g^3/(16*pi^2)",
        "required_beta": "-2",
        "inherited_beta": "2",
        "conditional_exact_carriers": [
            {"gauge_algebra": "su2", "C_A": 2, "Dirac_fundamentals": 8, "complex_scalar_fundamentals": 0, "beta": "-2", "anomaly_free": True},
            {"gauge_algebra": "su3", "C_A": 3, "Dirac_fundamentals": 13, "complex_scalar_fundamentals": 2, "beta": "-2", "anomaly_free": True},
        ],
        "false_friend": {"carrier": "su3_plus_27_chiral_Weyl_fundamentals", "beta": "-2", "anomaly_free": False, "K43_BV_27_is_typed_as_this_multiplicity": False},
        "beta_constraint": {"equation": "-22*C_A+4*n_D+n_s=-12", "rank": 1, "nullity": 2, "parent_hessian_rank": 1},
        "criteria": ["typed_gauge_beta", "internal_carrier", "negative_sign", "exact_minus_two", "anomaly_free", "independently_parent_selected"],
        "candidate_matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(c.candidate_matrix.rows)],
        "score_vector": [int(x) for x in c.score_vector],
        "pass_vector": [int(x) for x in c.pass_vector],
        "status": {"conditional_exact_carriers": "2/2", "candidate_passes": "0/9", "physical_origin": "0/4"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {
            "negative_beta_is_algebraically_possible": True,
            "exact_minus_two_is_algebraically_possible": True,
            "beta_equation_selects_unique_field_content": False,
            "current_relative_U1_is_asymptotically_free": False,
            "current_K43_carrier_derives_an_AF_sector": False,
            "physical_AF_parent_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_anomaly_free_carrier_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()