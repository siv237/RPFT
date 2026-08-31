#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v8_full_noise_42_jump_gksl_fixed_algebra_gate_results.json"
sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_noise_gksl import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402
def main()->None:
 c=build_certificate(); assert (c.jump_count,c.base_jump_count,c.added_jump_count)==(42,25,17)
 assert c.scalar_fixed_theorem.proposition.data["fixed_algebra_dimension"]==1
 registry=verify_all(); gate=next(x for x in registry["gates"] if x["identifier"]=="version8_full_noise_42_jump_gksl_fixed_algebra_gate"); assert len(gate["obligations"])==6
 result={"date":"2026-08-30","gate":gate["identifier"],"process":{"jump_count":42,"base_jump_count":25,"added_jump_count":17,"gksl":True,"trace_preserving":True,"unital":True,"endpoint_invariant":True,"fixed_algebra":"C I_21","primitive":True,"trace_dual_whitening_preserves_span":True},"boundary":{"physical_rate_metric_selected":False,"physical_time_selected":False,"fresh_ancilla_source_derived":False},"registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},"next_gate":"full_42_jump_repeated_interaction_hamiltonian_gate"}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()