#!/usr/bin/env python3
"""Точный аудит масштабной свободы поперечной мобильности."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v8_transverse_noise_mobility_environment_origin_gate_results.json"
sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_transverse_noise_mobility_environment_origin import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main():
    c=build_certificate(); assert c.canonical_covariance.rank()==12; assert c.canonical_transverse_mobility.rank()==36; assert c.rescaled_transverse_mobility==4*c.canonical_transverse_mobility; assert not c.canonical_transverse_mobility.atoms(sp.Float)
    registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_transverse_noise_mobility_environment_origin_gate"); assert len(gate["obligations"])==7
    result={"date":"2026-08-30","gate":gate["identifier"],"environment_covariance":{"canonical":"C_1=K_gauge^-1","rescaled":"C_2=4 K_gauge^-1","rank":12,"normalized_shape_equal":True},"transverse_mobility":{"rank":36,"nullity":12,"rescaling":"M_2=4 M_1","longitudinal_kernel_preserved":True},"scale_orbit":{"coupling":"g -> 2g","rate":"Gamma -> 4 Gamma","time":"t -> t/4","semigroup_parameter_invariant":True},"verdict":{"internal_shape_obtained":True,"absolute_mobility_scale_derived":False,"rejoins_physical_time_scale_no_go":True},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"version8_full_field_kinetic_supermetric_assembly_gate"}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()