#!/usr/bin/env python3
"""Точный аудит относительного кинетического веса общего a4-родителя."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v8_full_field_kinetic_relative_weight_parent_origin_gate_results.json"
sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_field_kinetic_relative_weight_parent_origin import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main():
    c=build_certificate(); assert c.scalar_coefficient==2; assert c.gauge_coefficient==-sp.Rational(2,3); assert c.scalar_to_gauge_ratio==3; assert c.gamma_five==sp.diag(1,1,-1,-1); assert not any(g.atoms(sp.Float) for g in c.gamma_matrices)
    registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_full_field_kinetic_relative_weight_parent_origin_gate"); assert len(gate["obligations"])==7
    result={"date":"2026-08-30","gate":gate["identifier"],"clifford":{"dimension":4,"relations_verified":16,"gamma5_spectrum":[1,1,-1,-1]},"heat_kernel_a4":{"scalar_coefficient":"2","antihermitian_gauge_coefficient":"-2/3","positive_gauge_coefficient":"2/3","scalar_to_gauge_ratio":"3"},"verdict":{"relative_weight_fixed_within_common_a4_lift":True,"normalized_weights":{"transfer":"1","gauge":"1/3"},"spacetime_dirac_lift_derived_from_finite_parent":False,"unconditional_parent_origin_closed":False},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"version8_full_field_a4_dirac_lift_origin_gate"}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()