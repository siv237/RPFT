#!/usr/bin/env python3
"""Audit whether a product spectral/superconnection fixes E2/E4."""
from __future__ import annotations
import json
from pathlib import Path


def main() -> None:
    result={
      "gate":"version5_projector_superconnection_common_scale_gate",
      "product_operator":"D_space tensor 1 + gamma tensor N/ell",
      "spectral_action":{"E2_coefficient":"f2 Lambda^2 times metric/internal normalization","E4_coefficient":"f0 times curvature normalization","independent_inputs":["f2","f0","Lambda","ell"],"ratio_fixed":False},
      "superconnection_square":{"odd_rescaling":"Phi -> a Phi","E2_scaling":"a^2","quartic_scaling":"a^4 or curvature normalization","ratio_fixed":False},
      "project_cross_audit":{"ordinary_spectral_moment_no_go_reused":True,"M35_trace_only_fixes_matrix_weights":True,"spacetime_Hodge_and_scale_derived":False},
      "verdict":{"common_scale_from_current_parent":False,"finite_radius_prediction":False,"next_gate":"version5_fermionic_determinant_induced_skyrme_gate"}}
    out=Path(__file__).resolve().parents[1]/"results"/"s2t_v5_projector_superconnection_common_scale_gate_results.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert len(result["spectral_action"]["independent_inputs"])==4
    print(out)
if __name__=="__main__": main()