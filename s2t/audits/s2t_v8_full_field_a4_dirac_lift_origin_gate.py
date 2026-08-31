#!/usr/bin/env python3
"""Точный аудит неединственности product-Dirac подъёма."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]; OUTPUT=ROOT/"s2t/results/s2t_v8_full_field_a4_dirac_lift_origin_gate_results.json"; sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_field_a4_dirac_lift_origin import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main():
 c=build_certificate(); assert c.internal_check_count==42; assert c.external_symbol_one**2==sp.eye(4); assert c.external_symbol_two**2==4*sp.eye(4); assert not c.external_symbol_two.atoms(sp.Float)
 registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_full_field_a4_dirac_lift_origin_gate"); assert len(gate["obligations"])==7
 result={"date":"2026-08-30","gate":gate["identifier"],"product_lifts":{"spin_dimension":4,"internal_dimension":21,"internal_frame_checks":42,"scales":[1,2],"principal_symbol_squares":[1,4],"same_internal_calculus":True},"verdict":{"relative_a4_weight_three_to_one_stable":True,"external_metric_scale_selected":False,"product_dirac_lift_derived_from_finite_parent":False},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"version8_spacetime_base_geometry_selector_gate"}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()