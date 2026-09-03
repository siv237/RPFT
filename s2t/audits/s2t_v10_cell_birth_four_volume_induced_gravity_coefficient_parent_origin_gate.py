#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.throughflow_constraint_map.rank()==2
    assert c.throughflow_constraint_map.nullspace()==[sp.Matrix([-1,1,1])]
    assert sum(c.architecture)==9 and sum(c.conditional_origin)==4 and sum(c.physical_ledger)==0
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "stationary_throughflow":{"incoming":"J","outgoing":"J","net_cell_change":0,"activity":"2*J","affinity":"F>0","entropy_production":"sigma=F*J>0"},
    "geometric_order_parent":{"functional":"lambda*(x^2-g*sigma/lambda)^2/4","maintained_amplitude":"x_*^2=g*sigma/lambda","maintained_hessian":"2*g*sigma>0","collapsed_hessian":"-g*sigma<0","zero_flow_parent":"lambda*x^4/4"},
    "conditional_induced_gravity":{"seed":"m=x_*^2=g*sigma/lambda","A":"alpha*m^2","B":"beta*m","selected_invariant":"q*m=beta/(2*alpha)"},
    "scale_obstruction":{"constraint_rank":2,"constraint_nullity":1,"kernel":"(1,-1,-1) in (q,m,sigma)","absolute_affinity_current_scale_derived":False},
    "status":{"architecture":"9/9","conditional_origin":"4/4","physical_affinity_origin":"0/1","absolute_gravitational_scale":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"balanced_throughflow_can_maintain_nonzero_geometry":True,"turning_off_flow_removes_broken_branch":True,"throughflow_alone_derives_absolute_scale":False},
    "next_gate":"version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()