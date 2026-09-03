#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.laplacian.eigenvals() == {0: 1, 2: 1}
    assert certificate.reversed_laplacian == certificate.laplacian
    assert certificate.stable_schur_complement == sp.Rational(3, 2)
    assert certificate.supercritical_schur_complement == -2
    assert certificate.fermion_vacuum_curvature == -2
    assert certificate.candidate_matrix.rank() == 6
    assert certificate.pass_vector == sp.zeros(12, 1)
    assert certificate.inherited_derived_negative_seed == sp.zeros(12, 1)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "sign_theorem": {
            "incidence_laplacian_spectrum": [0, 2],
            "orientation_reversal_changes_laplacian": False,
            "positive_weight_laplacian_spectrum": [0, 6],
            "stable_auxiliary_schur_complement": "3/2",
            "supercritical_auxiliary_schur_complement": -2,
            "supercritical_parent_determinant": -2,
            "fermion_determinant_quadratic_curvature": -2,
        },
        "criteria": [
            "correct_relative_incidence_type",
            "inherited_carrier_and_operator",
            "actual_negative_mode",
            "bounded_nonlinear_completion",
            "parent_derived_coefficient_without_target_loading",
            "phase_and_orientation_compatibility",
        ],
        "candidates": [
            "positive_incidence_stiffness",
            "orientation_reversal",
            "positive_edge_reweighting",
            "adjacency_quadratic_form",
            "antisymmetric_boundary_form",
            "stable_auxiliary_schur_complement",
            "supercritical_auxiliary_mixing",
            "fermionic_determinant_susceptibility",
            "Callias_sign_changing_profile",
            "real_Higgs_rank_change_portal",
            "negative_common_mode_wrong_type",
            "target_loaded_minus_laplacian",
        ],
        "candidate_scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": 6,
        "strict_pass_count": 0,
        "inherited_parent_derived_negative_seed_count": 0,
        "closest_routes": [
            {
                "name": "positive_incidence_stiffness",
                "score": "5/6",
                "missing": "actual_negative_mode",
            },
            {
                "name": "adjacency_quadratic_form",
                "score": "5/6",
                "missing": "parent_derived_coefficient_without_target_loading",
            },
            {
                "name": "fermionic_determinant_susceptibility",
                "score": "5/6",
                "missing": "inherited_carrier_and_operator",
            },
            {
                "name": "Callias_sign_changing_profile",
                "score": "5/6",
                "missing": "inherited_carrier_and_operator",
            },
        ],
        "status": {
            "audit_coverage": "12/12",
            "criterion_rank": "6/6",
            "strict_candidate_pass": "0/12",
            "inherited_parent_derived_negative_seed": "0/12",
            "stable_bosonic_incidence_tachyonic_sign": "0/1",
            "conditional_fermionic_sign": "1/1",
            "physical_origin": "0/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "orientation_can_reverse_incidence_stiffness": False,
            "stable_positive_bosonic_parent_can_generate_tachyonic_schur_complement": False,
            "supercritical_bosonic_parent_only_relocates_preexisting_instability": True,
            "fermionic_determinant_supplies_canonical_negative_susceptibility": True,
            "fermionic_carrier_is_inherited": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()