#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_spectral_pole_parent_origin_gate",
        "required_mass_squared_cell": "exp(-64*pi^2/3)",
        "criteria": ["mass_squared_type", "internal_carrier", "nonzero_IR", "selected_parent", "exact_target_exponent", "non_target_loaded"],
        "candidates": [
            "explicit_bare_mass_counterterm", "Higgs_Yukawa_condensate", "asymptotically_free_condensate",
            "KMS_thermal_mass", "bath_Lamb_shift", "curvature_coupling", "finite_volume_cell_gap",
            "throughflow_self_energy", "portal_eigenvalue_splitting", "observed_pole_fit", "formal_target_mass_term",
        ],
        "candidate_matrix": [list(map(int, certificate.candidate_matrix.row(i))) for i in range(certificate.candidate_matrix.rows)],
        "matrix_rank": int(certificate.candidate_matrix.rank()),
        "score_vector": [int(x) for x in certificate.score_vector],
        "pass_vector": [int(x) for x in certificate.pass_vector],
        "conditional_asymptotic_freedom": {
            "required_beta": "-2", "inherited_beta": "2", "g_squared": "3/8",
            "scale_ratio": "exp(-32*pi^2/3)", "mass_squared_ratio": "exp(-64*pi^2/3)",
            "exact_target_match": True, "present_in_current_carrier": False,
        },
        "status": {"audit_coverage": "11/11", "candidate_passes": "0/11", "physical_origin": "0/3"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {
            "current_IR_mass_origin_found": False,
            "thermal_or_finite_volume_terms_have_exact_exponent": False,
            "formal_and_observed_mass_terms_are_non_circular": False,
            "asymptotic_freedom_would_generate_exact_inverse_exponent": True,
            "required_beta_sign_is_inherited": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()