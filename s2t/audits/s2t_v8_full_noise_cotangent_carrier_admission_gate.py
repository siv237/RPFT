#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_noise_cotangent_carrier_admission_gate_results.json"
sys.path.insert(0, str(ROOT))
from s2t.proofdsl.examples.version8_full_noise_cotangent_carrier import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402

def main() -> None:
    c = build_certificate()
    assert (c.mixed_real_dimension, c.naive_uniform_complex_real_dimension) == (42, 54)
    assert (c.current_jump_dimension, c.missing_real_directions) == (25, 17)
    registry = verify_all()
    gate = next(x for x in registry["gates"] if x["identifier"] == "version8_full_noise_cotangent_carrier_admission_gate")
    assert len(gate["obligations"]) == 5
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "typed_carrier": {"transfer_complex": 15, "transfer_real": 30, "gauge_hermitian_real": 12, "mixed_real": 42, "field_real": 42},
        "no_go": {"naive_uniform_complex_real": 54, "current_jump_real": 25, "missing_real_directions": 17, "current_qms_is_full_cotangent_frame": False},
        "registry": {"gate_count": registry["gate_count"], "obligation_count": registry["obligation_count"], "certificate_sha256": registry["certificate_sha256"][gate["identifier"]]},
        "next_gate": "full_42_real_jump_frame_trace_metric_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__ == "__main__": main()