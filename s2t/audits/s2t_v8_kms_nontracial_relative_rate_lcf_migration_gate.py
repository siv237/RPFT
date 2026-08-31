#!/usr/bin/env python3
"""Migrate the nontracial KMS selector no-go to the exact LCF eDSL."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_kms_nontracial_relative_rate_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))
from s2t.proofdsl.examples.version8_kms_selector import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402

def main() -> None:
    c = build_certificate()
    assert c.transfer_traces == (13, 6, 6) and c.transfer_jump_count == 13
    assert c.central_state_theorem.proposition.data["condition"] == "a=b=1/21"
    assert c.conditional_ratio_theorem.proposition.data["uniquely_selected"] is False
    registry = verify_all()
    gate = next(x for x in registry["gates"] if x["identifier"] == "version8_kms_nontracial_relative_rate_selector_gate")
    assert len(gate["obligations"]) == 6
    result = {
        "date": "2026-08-29",
        "gate": "version8_kms_nontracial_relative_rate_lcf_migration_gate",
        "current_process_no_go": {
            "unique_stationary_state": "I21/21",
            "central_stationarity_condition": "a=b=1/21",
            "positive_transfer_traces_link_QLYR_XLdR": [13, 6, 6],
            "positive_rate_tuning_can_cancel_transfer": False,
        },
        "directed_extension": {
            "transfer_jump_count": 13,
            "opposite_bohr_frequencies": True,
            "selfadjoint_jump_is_one_nonzero_bohr_mode": False,
            "conditional_rate_ratio": "exp(-beta_Delta)",
            "beta_Delta_derived": False,
            "relative_rate_uniquely_selected": False,
        },
        "proofdsl_registry": {"status": gate["status"], "obligation_count": 6,
            "certificate_sha256": registry["certificate_sha256"]["version8_kms_nontracial_relative_rate_selector_gate"]},
        "verdict": {"status": "lcf-checked-nontracial-kms-selector-no-go",
            "next_gate": "version8_modular_bohr_parent_lcf_migration_gate"},
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__ == "__main__": main()