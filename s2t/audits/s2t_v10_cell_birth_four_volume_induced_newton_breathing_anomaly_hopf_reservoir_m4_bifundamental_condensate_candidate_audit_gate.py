#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (11, 6)
    assert certificate.candidate_matrix.rank() == 6
    assert certificate.pass_vector == sp.zeros(11, 1)
    assert certificate.physical_seed_vector == sp.zeros(11, 1)
    assert certificate.incidence_laplacian.eigenvals() == {0: 1, 2: 1}

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "criteria": [
            "correct_bifundamental_type",
            "inherited_carrier_and_operator",
            "negative_quadratic_mode",
            "positive_quartic_stabilization",
            "orientation_and_phase_selector",
            "non_target_loaded_physical_normalization",
        ],
        "candidates": [
            "inherited_block_diagonal_parent",
            "spectral_inner_fluctuation",
            "KMS_modular_covariance",
            "Hopf_holonomy",
            "bath_current_susceptibility",
            "cell_incidence_boundary",
            "Callias_sign_changing_profile",
            "Higgs_rank_change_portal",
            "existing_RG_K43_portal",
            "auxiliary_bifundamental_scalar",
            "target_loaded_tachyonic_source",
        ],
        "candidate_scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": 6,
        "strict_pass_count": 0,
        "correct_inherited_negative_seed_count": int(sum(certificate.physical_seed_vector)),
        "closest_candidates": [
            {
                "name": "cell_incidence_boundary",
                "score": "5/6",
                "missing": "negative_quadratic_mode",
                "inherited_spectrum": [0, 2],
            },
            {
                "name": "Callias_sign_changing_profile",
                "score": "5/6",
                "missing": "inherited_carrier_and_operator",
            },
            {
                "name": "Higgs_rank_change_portal",
                "score": "5/6",
                "missing": "inherited_carrier_and_operator",
            },
        ],
        "incidence_sign_test": {
            "laplacian": [[1, -1], [-1, 1]],
            "spectrum": [0, 2],
            "tachyonic_sign_flip_spectrum": [-2, 0],
            "sign_flip_inherited": False,
        },
        "status": {
            "audit_coverage": "11/11",
            "criterion_rank": "6/6",
            "strict_candidate_pass": "0/11",
            "correct_inherited_negative_seed": "0/11",
            "tachyonic_sign_origin": "0/1",
            "physical_origin": "0/4",
            "origin_ledger": "3/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "existing_candidate_physically_seeds_bifundamental_condensate": False,
            "cell_incidence_supplies_correct_positive_stiffness": True,
            "cell_incidence_supplies_tachyonic_sign": False,
            "conditional_Callias_or_Higgs_route_remains_open": True,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()