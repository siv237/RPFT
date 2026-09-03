#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate_results.json"

def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC); c = build_certificate()
    assert c.charge_cross_defect == sp.zeros(60)
    assert c.partial_isometry.rank() == 30
    assert c.conditional_amplifier.rank() == 2
    assert c.inherited_amplifier.rank() == 0
    assert c.algebra_gram.rank() == 16
    assert c.determinant_curvature == -60
    result = {
        "date": "2026-09-02", "gate": SPEC.identifier, "predecessor": predecessor["gate"],
        "conditional_embedding": {"carrier": "C2_spin tensor C2_twist tensor H15", "complex_dimension": 60, "M4_algebra_rank": 16, "positive_twist_rank": 30, "negative_twist_rank": 30, "cross_partial_isometry_rank": 30, "charge_commutator_rank": 0, "uniform_H15_amplifier_rank": 2, "uniform_amplifier_gram": "15 I2", "fermion_determinant_curvature": -60},
        "inheritance": {"dimension_data": True, "spatial_twist_Clifford_split": True, "abstract_equal_charge_cell_algebra": True, "sector_identification": False, "uniform_H15_amplifier": False, "inherited_amplifier_rank": 0},
        "status": {"conditional_architecture": "16/16", "inherited_data": "3/5", "strict_typed_embedding_origin": "0/3", "physical_origin": "0/3"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "obligations": [n for n, _ in verified.obligations], "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {"Callias_M4_embedding_exists_conditionally": True, "cross_operator_is_equal_charge": True, "full_M4_algebra_is_embedded": True, "uniform_H15_amplification_is_inherited": False},
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate", "floating_point_values": 0,
    }
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUT.write_text(text); print(OUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__ == "__main__": main()