#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate_results.json"

def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.candidate_matrix.rank() == 6
    assert c.pass_vector == sp.zeros(12, 1)
    assert c.ko_charge_defect.rank() == 4
    assert c.equal_charge_defect == sp.zeros(4)
    assert c.odd_rank_defect.rank() == 2
    result = {
        "date": "2026-09-02", "gate": SPEC.identifier, "predecessor": predecessor["gate"],
        "criteria": ["correct_M4_cross_type", "inherited_operator", "odd_statistics_and_measure", "negative_determinant_susceptibility", "gauge_and_KMS_compatibility", "independent_non_target_loaded_coupling"],
        "candidates": ["inherited_block_diagonal_physical_fermions", "formal_M4_cross_involution", "KO6_particle_conjugate_bilinear", "Callias_equal_charge_twist", "KMS_auxiliary_fermion_module", "BRST_ghost_pair", "physical_SM_Yukawa_bilinear", "fermionic_bath_pseudomode", "reduced_Pfaffian_representative", "Schwinger_Keldysh_doubling", "abstract_cell_equal_charge_twist", "target_loaded_cross_Grassmann_pair"],
        "candidate_scores": list(map(int, c.score_vector)), "candidate_matrix_rank": 6, "strict_pass_count": 0,
        "exact_obstructions": {"KO6_charge_commutator_rank": 4, "equal_charge_twist_commutator_rank": 0, "inherited_odd_rank": 2, "required_odd_rank": 4, "odd_rank_defect": 2, "Callias_to_M4_embedding_rank": 0, "reduced_Pfaffian_phases": [-1, 1], "full_KO6_phases": [1, 1]},
        "closest_routes": [{"name": "KO6_particle_conjugate_bilinear", "score": "5/6", "missing": "gauge_and_KMS_compatibility"}, {"name": "Callias_equal_charge_twist", "score": "5/6", "missing": "inherited_operator"}, {"name": "reduced_Pfaffian_representative", "score": "5/6", "missing": "gauge_and_KMS_compatibility"}],
        "status": {"audit_coverage": "12/12", "criterion_rank": "6/6", "strict_candidate_pass": "0/12", "physical_origin": "0/4"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "obligations": [n for n, _ in verified.obligations], "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {"KO6_cross_is_gauge_compatible": False, "full_KO6_Pfaffian_retains_relative_sign": False, "Callias_equal_charge_route_is_conditionally_compatible": True, "Callias_to_M4_embedding_is_inherited": False},
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate", "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text); print(OUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)

if __name__ == "__main__": main()