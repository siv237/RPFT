#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit import SPEC,build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate_results.json"
def main():
 v=verify_gate(SPEC); c=build_certificate(); names=["direct_sum","tensor_identity","trace_product","mixed_spectral_trace","trace_anomaly","KMS_throughflow","Hopf_K43_product","explicit_bridge_portal"]
 r={"date":"2026-09-02","gate":SPEC.identifier,"predecessor":"version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_common_parent_origin_gate","candidates":[{"name":n,"score":int(c.score_vector[i]),"pass":bool(c.pass_vector[i])} for i,n in enumerate(names)],"audit":{"matrix_shape":"8x6","rank":5,"complete_passes":0,"formal_nonzero_mixed_blocks":5,"inherited_mixed_and_selected":0},"portal_stability":{"determinant":"1-lambda^2","strict_example":"lambda=1/2","boundary_zero_mode":"lambda=1"},"status":{"candidate_coverage":"8/8","complete_candidates":"0/8","physical_origin":"0/3"},"proofdsl":{"status":"lcf-checked","obligation_count":len(v.obligations),"certificate_sha256":v.sha256,"floating_point_values":0},"verdict":{"an_inherited_selected_cross_operator_exists":False,"a_conditional_stable_portal_exists":True,"absolute_birth_tick_is_derived":False},"next_gate":"version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_minimal_portal_operator_architecture_gate","floating_point_values":0}
 t=json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n";OUT.write_text(t);print(OUT);print(hashlib.sha256(t.encode()).hexdigest());print(v.sha256)
if __name__=="__main__":main()