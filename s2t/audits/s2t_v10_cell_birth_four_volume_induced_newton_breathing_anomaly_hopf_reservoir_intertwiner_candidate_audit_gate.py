#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.intertwiner_constraint.rank() == 2
    assert len(certificate.intertwiner_constraint.nullspace()) == 2
    assert certificate.candidate_matrix.rank() == 6
    assert certificate.pass_vector == sp.zeros(10, 1)
    assert certificate.inherited_pass_vector == sp.zeros(10, 1)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "intertwiner_space": {
            "constraint_rank_nullity": "2/2",
            "kernel": "all_diagonal_2x2_maps",
            "real_orthogonal_phase_choices": 4,
            "permutation_assignment_unique": True,
            "full_intertwiner_unique": False,
        },
        "criteria": [
            "correct_Hom_type",
            "inherited_and_not_target_loaded",
            "nonzero_map",
            "orientation_compatible",
            "phase_and_coefficient_selected",
            "appears_as_parent_mixed_block",
        ],
        "candidates": [
            "inherited_zero_mixed_block",
            "spectral_projector_matching",
            "basis_identity",
            "relative_sign_intertwiner",
            "KMS_modular_swap",
            "Hopf_incidence_restriction",
            "modular_conjugation",
            "bath_current_covariance",
            "minimal_portal_Pauli_block",
            "target_loaded_coupling_parent",
        ],
        "candidate_scores": list(map(int, certificate.score_vector)),
        "candidate_matrix_rank": 6,
        "strict_pass_count": 0,
        "inherited_pass_count": 0,
        "best_candidate": {
            "name": "target_loaded_coupling_parent",
            "score": "5/6",
            "missing_criterion": "inherited_and_not_target_loaded",
            "mixed_hessian_rank_nullity": "2/2",
        },
        "closed_routes": {
            "spectral_projectors_fix_level_matching_but_not_phases": True,
            "orientation_equation_fixes_off_diagonal_entries_only": True,
            "inherited_parent_mixed_block": "zero",
        },
        "status": {
            "audit_coverage": "10/10",
            "criterion_rank": "6/6",
            "strict_candidate_pass": "0/10",
            "intertwiner_phase_origin": "0/1",
            "mixed_parent_block_origin": "0/1",
            "physical_temperature_origin": "0/1",
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
            "orientation_selects_unique_permutation": True,
            "orientation_selects_unique_intertwiner": False,
            "existing_candidate_generates_physical_mixed_parent": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()