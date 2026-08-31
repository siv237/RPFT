#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUTPUT=ROOT/"s2t/results/s2t_v8_full_noise_repeated_interaction_hamiltonian_gate_results.json"; sys.path.insert(0,str(ROOT))
from s2t.proofdsl.examples.version8_full_noise_repeated_interaction import build_certificate  # noqa:E402
from s2t.proofdsl.verify import verify_all  # noqa:E402
def main()->None:
 c=build_certificate(); assert (c.system_dimension,c.jump_dimension,c.environment_dimension,c.ambient_dimension)==(21,42,43,903); assert c.closure_theorem.proposition.data["closure_checks"]==504
 r=verify_all(); g=next(x for x in r["gates"] if x["identifier"]=="version8_full_noise_repeated_interaction_hamiltonian_gate"); assert len(g["obligations"])==6
 result={"date":"2026-08-30","gate":g["identifier"],"dimensions":{"system":21,"jumps":42,"environment":43,"ambient":903},"proof":{"gauge_closure_checks":504,"self_adjoint":True,"vacuum_second_moment":"sum_a F_a^2","gksl_tangent":True,"collision_limit":"operator_norm","fixed_algebra":"C I_21","minimal_environment":True},"boundary":{"fresh_ancilla_source":False,"physical_time_scale":False},"registry":{"gate_count":r["gate_count"],"obligation_count":r["obligation_count"],"certificate_sha256":r["certificate_sha256"][g["identifier"]]},"next_gate":"autonomous_fresh_ancilla_chain_dilation_gate"}
 text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=="__main__": main()