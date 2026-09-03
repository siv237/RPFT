#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin import SPEC,build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate_results.json"
def main():
 p=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate_results.json").read_text()); assert p["next_gate"]==SPEC.identifier
 v=verify_gate(SPEC); c=build_certificate()
 result={"date":"2026-09-02","gate":SPEC.identifier,"predecessor":p["gate"],"hopf_affinity":{"cycle":"3*log(2)","edges":["log(2)"]*3},"reservoir_affinity":{"hot":"log(2)","cold":"2*log(2)","difference":"log(2)","typed_match":True},"current_match":{"J_two_bath":"1/66","J_edge":"kappa/3","kappa_times_step":"1/22"},"residual_orbits":{"affinity_rank_nullity":"2/1","affinity_kernel":[1,1,0],"rate_clock_rank_nullity":"1/1","rate_clock_kernel":[1,-1]},"status":{"conditional_origin":"8/8","affinity_difference_origin":"1/1","common_affinity_offset_origin":"0/1","absolute_clock_origin":"0/1","absolute_scale":"0/1"},"proofdsl":{"status":"lcf-checked","obligation_count":len(v.obligations),"obligations":[n for n,_ in v.obligations],"certificate_sha256":v.sha256,"floating_point_values":0},"verdict":{"Hopf_cycle_derives_affinity_difference":True,"Hopf_cycle_derives_both_bath_temperatures":False,"current_matching_derives_absolute_rate":False},"next_gate":"version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate","floating_point_values":0}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n";OUT.write_text(text);print(OUT);print(hashlib.sha256(text.encode()).hexdigest());print(v.sha256)
if __name__=="__main__":main()