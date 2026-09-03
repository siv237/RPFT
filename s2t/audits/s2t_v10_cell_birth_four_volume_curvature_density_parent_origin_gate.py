#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_curvature_density_parent_origin import SPEC,build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_curvature_density_parent_origin_gate_results.json"
def main()->None:
 p=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_topological_quantum_candidate_audit_gate_results.json").read_text());gate="version10_cell_birth_four_volume_curvature_density_parent_origin_gate";assert p["next_gate"]==gate and SPEC.identifier==gate
 v=verify_gate(SPEC);c=build_certificate();assert c.curvature_constraint_map.rank()==2;assert c.curvature_constraint_map.nullspace()==[sp.Matrix([-2,-1,1])];assert sum(c.architecture)==8 and sum(c.conditional_origin)==3 and sum(c.physical_ledger)==0
 result={"date":"2026-09-01","gate":gate,"predecessor":p["gate"],"constant_curvature_cell":{"volume":"ell^4","scalar_curvature":"12/ell^2","einstein_integral":"12*ell^2","curvature_square_integral":144,"curvature_square_scale_invariant":True},"conditional_parent":{"functional":"A*q^2-B*q+B^2/(4*A)=A*(q-B/(2*A))^2","q":"ell^2","selected_q":"B/(2*A)","radial_hessian":"2*A>0"},"coefficient_scale_orbit":{"transformation":"(q,A,B)->(s^2*q,A/s^4,B/s^2)","constraint_rank":2,"constraint_nullity":1,"kernel":"(-2,-1,1)","absolute_scale_selected":False},"status":{"architecture":"8/8","conditional_origin":"3/3","curvature_coefficient_origin":"0/1","absolute_cell_scale":"0/1"},"proofdsl":{"status":"lcf-checked","obligation_count":len(v.obligations),"obligations":[n for n,_ in v.obligations],"certificate_sha256":v.sha256,"floating_point_values":0},"verdict":{"curvature_square_selects_scale":False,"competing_volume_and_einstein_terms_select_scale_conditionally":True,"coefficient_ratio_physically_derived":False},"next_gate":"version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate","floating_point_values":0}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n";OUTPUT.write_text(text);print(OUTPUT);print(hashlib.sha256(text.encode()).hexdigest());print(v.sha256)
if __name__=="__main__":main()