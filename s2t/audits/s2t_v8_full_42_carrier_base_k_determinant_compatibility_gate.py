#!/usr/bin/env python3
"""Точный аудит переноса base-K ledger на полный 42-мерный носитель."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]; OUTPUT=ROOT/"s2t/results/s2t_v8_full_42_carrier_base_k_determinant_compatibility_gate_results.json"; sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_42_carrier_base_k_determinant_compatibility import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main():
 c=build_certificate(); assert c.scalar_hessian.rank()==28; assert c.gauge_mass_gram.rank()==3; assert c.bosonic_fourth_moment==sp.Rational(4659176,3249); assert c.finite_fermion_fourth_moment==46; assert not c.scalar_hessian.atoms(sp.Float)
 registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_full_42_carrier_base_k_determinant_compatibility_gate"); assert len(gate["obligations"])==9
 result={"date":"2026-08-30","gate":gate["identifier"],"vacuum_bosonic_blocks":{"transfer_rank":28,"transfer_nullity":2,"gauge_mass_rank":3,"unbroken_gauge_nullity":9},"normalized_fourth_moments":{"scalar":"23053/18","gauge":"36897/722","bosonic_numerator":"4659176/3249"},"finite_fermion":{"raw_fourth_moment":46,"physical_determinant_multiplicity_derived":False},"verdict":{"early_67_numerator_reusable":False,"full_bosonic_ledger_derived":True,"full_supertrace_B_derived":False,"bv_vacuum_quotient_required":True},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"version8_full_42_carrier_bv_vacuum_quotient_gate"}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()