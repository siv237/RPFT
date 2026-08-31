#!/usr/bin/env python3
"""Точный аудит полной главной кинетической суперметрики поля."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v8_full_field_kinetic_supermetric_assembly_gate_results.json"
sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_field_kinetic_supermetric_assembly import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main():
    c=build_certificate(); assert c.scalar_principal_symbol.shape==(120,120); assert c.gauge_principal_symbol.shape==(48,48); assert c.ungauged_supermetric.shape==(168,168); assert c.gauge_fixed_supermetric.shape==(168,168); assert c.sector_mixing_block==sp.zeros(120,48); assert c.ungauged_rank_theorem.proposition.kind=="expression_equality"; assert c.ungauged_nullity_theorem.proposition.kind=="expression_equality"; assert c.gauge_fixed_rank_theorem.proposition.kind=="expression_equality"; assert not c.gauge_fixed_supermetric.atoms(sp.Float)
    registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_full_field_kinetic_supermetric_assembly_gate"); assert len(gate["obligations"])==9
    result={"date":"2026-08-30","gate":gate["identifier"],"carrier":{"transfer_channels":30,"gauge_channels":12,"spacetime_components":4,"total_principal_dimension":168},"principal_symbol":{"scalar_rank":120,"gauge_transverse_rank":36,"ungauged_rank":156,"ungauged_nullity":12,"mixed_block_rank":0},"gauge_fixing":{"fixed_rank":168,"factorized_inverse_verified":True,"transverse_observable_block_gauge_parameter_independent":True},"verdict":{"principal_supermetric_assembled":True,"lower_order_scalar_vector_mixing_classified":False,"relative_sector_weight_derived":False,"absolute_time_scale_derived":False},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"version8_full_field_kinetic_relative_weight_parent_origin_gate"}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()