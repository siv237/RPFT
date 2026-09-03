#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin import SPEC,build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate_results.json"
def main():
 v=verify_gate(SPEC); c=build_certificate()
 r={"date":"2026-09-02","gate":SPEC.identifier,"predecessor":"version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate","conditional_parent":{"stationary_ratio":"exp(-32*pi^2/3)/42","hessian":[[2,1,1],[1,2,1],[1,1,1]],"rank":3,"determinant":1},"inherited_parent":{"hessian":"diag(1,1,0)","rank_nullity":"2/1","mixed_blocks":"0/2"},"scale_audit":{"rank_nullity":"2/2"},"status":{"conditional_architecture":"9/9","inherited_factor_parents":"2/2","physical_origin":"0/4","absolute_birth_tick_origin":"0/1"},"proofdsl":{"status":"lcf-checked","obligation_count":len(v.obligations),"certificate_sha256":v.sha256,"floating_point_values":0},"verdict":{"a_strict_conditional_common_parent_exists":True,"the_common_parent_is_inherited":False,"absolute_birth_tick_is_derived":False},"next_gate":"version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate","floating_point_values":0}
 t=json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUT.write_text(t); print(OUT); print(hashlib.sha256(t.encode()).hexdigest()); print(v.sha256)
if __name__=="__main__": main()