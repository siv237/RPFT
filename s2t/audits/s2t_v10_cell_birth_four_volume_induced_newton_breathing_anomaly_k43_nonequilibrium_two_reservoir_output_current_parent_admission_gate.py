#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission import SPEC,build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate_results.json"
def main():
 p=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate_results.json").read_text())
 assert p["next_gate"]==SPEC.identifier
 v=verify_gate(SPEC); c=build_certificate()
 assert c.currents==sp.ImmutableMatrix([sp.Rational(1,66),-sp.Rational(1,66)])
 result={"date":"2026-09-02","gate":SPEC.identifier,"predecessor":p["gate"],"rates":{"hot":{"down":"1/6","up":"1/12","ratio":"1/2"},"cold":{"down":"1/6","up":"1/24","ratio":"1/4"}},"stationary_population":["8/11","3/11"],"currents":{"hot_to_system":"1/66","system_to_cold":"1/66","net_storage":"0"},"entropy_production":"log(2)/66","status":{"CPTP_channel":"1/1","nonzero_through_current":"1/1 conditional","architecture":"10/10","physical_bath_affinity_rate_origins":"0/3","absolute_scale":"0/1"},"proofdsl":{"status":"lcf-checked","obligation_count":len(v.obligations),"obligations":[n for n,_ in v.obligations],"certificate_sha256":v.sha256,"floating_point_values":0},"verdict":{"nonequilibrium_current_exists":True,"detailed_balance_globally_holds":False,"bath_parameters_parent_derived":False,"absolute_scale_derived":False},"next_gate":"version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate","floating_point_values":0}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUT.write_text(text); print(OUT); print(hashlib.sha256(text.encode()).hexdigest()); print(v.sha256)
if __name__=="__main__": main()