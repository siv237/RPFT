#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_thom_multiplet_common_parent_origin_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.odd_pairing.T == -c.odd_pairing and c.odd_pairing.rank() == 16
    assert c.candidate_matrix.shape == (12, 7) and c.candidate_matrix.rank() == 7
    assert c.pass_vector == sp.zeros(12, 1)
    names = [
        "carrier_Z2_grading", "physical_Callias_fermions",
        "charge_conjugate_Nambu_pair", "inherited_M4_cross_bilinear",
        "differential_form_parity", "BV_antifields_of_Sigma",
        "existing_Faddeev_Popov_ghosts", "imported_KMS_BRST_quartet",
        "Sigma_shift_BRST_quartet", "AKSZ_mapping_space_extension",
        "formal_Mathai_Quillen_odd_fibers", "target_loaded_Grassmann_pair",
    ]
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "required_odd_pair": {
            "fields": ["psi_Sigma", "chi_Sigma"],
            "real_odd_dimension": 16,
            "target_odd_rank": 16,
            "antisymmetric_pairing_rank": c.odd_pairing.rank(),
            "pairing_determinant": int(c.odd_pairing.det()),
            "pfaffian_magnitude": 3969,
            "required_shift_generator_rank": c.required_shift_generator.rank(),
            "inherited_translational_gauge_rank_at_Sigma_zero": c.inherited_gauge_shift_at_origin.rank(),
            "shift_generator_deficit": 8,
        },
        "candidate_audit": {
            "criteria": ["exact_typed_pair", "Grassmann_statistics", "Thom_differential", "exact_Q_pairing", "paired_Berezin_measure", "acyclic_auxiliary_sector", "inherited_parent_origin"],
            "names": names,
            "matrix": [list(map(int, c.candidate_matrix.row(i))) for i in range(12)],
            "rank": c.candidate_matrix.rank(),
            "scores": list(map(int, c.score_vector)),
            "passes": list(map(int, c.pass_vector)),
            "passing_candidates": 0,
        },
        "best_candidates": [
            {"name": "Sigma_shift_BRST_quartet", "score": "6/7", "failed": "inherited_parent_origin"},
            {"name": "formal_Mathai_Quillen_odd_fibers", "score": "6/7", "failed": "inherited_parent_origin"},
            {"name": "physical_Callias_fermions", "score": "4/7", "failed": ["Thom_differential", "exact_Q_pairing", "acyclic_auxiliary_sector"]},
        ],
        "no_go": {
            "carrier_grading_is_field_statistics": False,
            "physical_fermions_are_contractible_auxiliaries": False,
            "existing_gauge_symmetry_supplies_required_shift": False,
            "formal_BRST_or_MQ_extension_is_inherited": False,
        },
        "status": {
            "conditional_best": "6/7",
            "inherited_best": "4/7",
            "remaining_slot": "origin of an eight-generator Sigma shift symmetry",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "candidate_passes_all_criteria": False,
            "conditional_shift_BRST_closure": True,
            "physical_odd_pair_parent_found": False,
            "best_next_discriminator_identified": True,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()