#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_noise_trace_frame_metric_gate_results.json"
sys.path.insert(0, str(ROOT))
from s2t.proofdsl.examples.version8_full_noise_trace_frame import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402

def main() -> None:
    c = build_certificate()
    assert c.orbit_dimensions == (1, 4, 5, 5)
    assert (c.transfer_complex_dimension, c.transfer_real_dimension, c.gauge_real_dimension, c.full_frame_dimension) == (15, 30, 12, 42)
    assert (c.added_linking_directions, c.added_internal_directions) == (9, 8)
    registry = verify_all(); gate = next(x for x in registry["gates"] if x["identifier"] == "version8_full_noise_trace_frame_metric_gate")
    assert len(gate["obligations"]) == 7
    result = {
      "date":"2026-08-30", "gate":gate["identifier"],
      "frame":{"linking_orbit_dimensions":[1,4,5,5],"linking_complex":5,"heavy_complex":10,"transfer_real":30,"gauge_real":12,"full_real":42,"added_linking_real":9,"added_internal_real":8},
      "metric":{"definition":"K_ab=Tr(F_a^* F_b)","rank":42,"transfer_gauge_block":"0","dual":"R=K^-1","inverse_residual":"0"},
      "boundary":{"riesz_principle_derived":False,"physical_time_derived":False,"fresh_ancilla_source_derived":False},
      "registry":{"gate_count":registry["gate_count"],"obligation_count":registry["obligation_count"],"certificate_sha256":registry["certificate_sha256"][gate["identifier"]]},
      "next_gate":"full_42_jump_gksl_fixed_algebra_gate"
    }
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text,encoding="utf-8"); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__ == "__main__": main()