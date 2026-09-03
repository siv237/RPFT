#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.candidate_matrix.shape==(8,6) and c.candidate_matrix.rank()==4
    assert c.pass_vector==sp.zeros(8,1)
    assert c.cycle_generator.rank()==2 and c.cycle_generator.nullspace()==[sp.Matrix([1,1,1])]
    assert c.rate_clock_map.nullspace()==[sp.Matrix([-1,-1,1])]
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "candidates":["KMS_rate_ratio","reciprocal_K43_orientation","normalized_cell_birth_measure","clock_resonance","spectral_gap","Hopf_winding","physical_matter_bath","cosmological_flow"],
    "criteria":["force_relation_fixed","absolute_conductance_fixed","closed_cycle_carrier","positive_entropy","internal_typed","breaks_clock_orbit"],
    "candidate_matrix":[list(map(int,c.candidate_matrix.row(i))) for i in range(8)],"candidate_matrix_rank":4,"passing_candidates":0,"maximum_score":"4/6","closest_candidate":"KMS_rate_ratio",
    "oriented_cycle":{"generator":"kappa*[[-3,1,2],[2,-3,1],[1,2,-3]]","stationary_state":"(1,1,1)/3","rank":2,"nullity":1,"edge_current":"kappa/3","cycle_affinity":"3*log(2)","entropy_production":"kappa*log(2)"},
    "clock_scale_obstruction":{"transformation":"kappa->c*kappa, t->t/c","affinity_invariant":True,"current_scales":"J->c*J","map_rank":2,"map_nullity":1,"absolute_conductance_derived":False},
    "status":{"candidate_coverage":"8/8","origin_ledger":"3/5","absolute_channel_conductance":"0/1","physical_clock_scale":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"oriented_cycle_supports_stationary_current":True,"KMS_ratio_fixes_affinity":True,"KMS_ratio_fixes_absolute_rate":False,"current_derives_absolute_scale":False},
    "next_gate":"version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()