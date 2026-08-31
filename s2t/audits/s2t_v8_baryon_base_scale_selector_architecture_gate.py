#!/usr/bin/env python3
"""Exact classical no-go and conditional quantum scale-selector audit."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v8_baryon_base_scale_selector_architecture_gate_results.json"
def main():
    a,c,c0,B,mu2=sp.symbols("a c c0 B mu2", positive=True)
    classical=sp.expand(a**2*(c-c0)**2)
    Hc=sp.hessian(classical,(a,c)).subs(c,c0)
    assert Hc==sp.diag(0,2*a**2)
    quantum=B*a**2*(sp.log(a/mu2)-sp.Rational(1,2))+a**2*(c-c0)**2
    grad=[sp.simplify(sp.diff(quantum,x).subs({a:mu2,c:c0})) for x in (a,c)]
    Hq=sp.simplify(sp.hessian(quantum,(a,c)).subs({a:mu2,c:c0}))
    assert grad==[0,0]
    assert Hq==sp.diag(2*B,2*mu2**2)
    assert not any(x.is_Float for obj in [classical,*Hc,quantum,*Hq] for x in sp.preorder_traversal(obj))
    result={"date":"2026-08-30","gate":"version8_baryon_base_scale_selector_architecture_gate","field":"Q(a,c,c0,B,mu2,log(a/mu2))","classical":{"potential":"a^2(c-c0)^2","vacuum":"c=c0, arbitrary a>0","hessian":[["0","0"],["0","2*a^2"]],"scale_selected":False,"map_selected_conditionally":True},"quantum":{"potential":"B*a^2(log(a/mu2)-1/2)+a^2(c-c0)^2","stationary_point":"(mu2,c0)","gradient":["0","0"],"hessian":[["2*B","0"],["0","2*mu2^2"]],"strict_minimum_if_B_positive":True},"verdict":{"classical_scale_invariant_parent_selects_a":False,"quantum_architecture_conditionally_selects_a_and_c":True,"mu2_derived":False,"c0_derived":False,"full_internal_selector_realized":False},"next_gate":"version8_baryon_dimensional_transmutation_input_origin_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8")
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()