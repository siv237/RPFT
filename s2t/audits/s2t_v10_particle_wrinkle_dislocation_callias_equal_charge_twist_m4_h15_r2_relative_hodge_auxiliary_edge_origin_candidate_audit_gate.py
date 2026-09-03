#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate_results.json"
def main():
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate_results.json").read_text())
    assert predecessor["next_gate"]==SPEC.identifier
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.diagonal_relative_image==sp.zeros(16,8) and c.independent_relative_image.rank()==8
    assert c.candidate_matrix.shape==(12,6) and c.candidate_matrix.rank()==6 and c.pass_vector==sp.zeros(12,1)
    names=["fixed_point_curvature","reuse_physical_Sigma","cotangent_copy","BV_antifield","KO6_conjugate","superconnection_suspension","mapping_cone_cylinder","de_Rham_one_form_copy","Callias_normal_copy","Hubbard_Stratonovich_copy","fermionic_Nambu_doubling","target_loaded_copy"]
    result={"date":"2026-09-03","gate":SPEC.identifier,"predecessor":predecessor["gate"],"reuse_no_go":{"diagonal_embedding_rank":8,"relative_image_rank":0,"independent_copy_relative_image_rank":8},"candidate_audit":{"criteria":["exact_weights","independent_boson","odd_grading","Real_Hodge_edge","positive_metric","inherited_origin"],"names":names,"matrix":[list(map(int,c.candidate_matrix.row(i))) for i in range(12)],"rank":6,"scores":list(map(int,c.score_vector)),"passes":list(map(int,c.pass_vector)),"passing_candidates":0},"best_candidates":[{"name":"superconnection_suspension","score":"5/6","failed":"inherited_origin"},{"name":"mapping_cone_cylinder","score":"5/6","failed":"inherited_origin"}],"status":{"physical_origin":"5/6","remaining_slot":"inherited independent auxiliary copy"},"proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},"verdict":{"reuse_physical_Sigma":False,"candidate_passes_all":False,"best_route_identified":True,"physical_parent_found":False},"next_gate":"version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate","floating_point_values":0}
    output=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUT.write_text(output); print(OUT); print(hashlib.sha256(output.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()