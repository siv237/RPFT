#!/usr/bin/env python3
"""Audit three possible origins of the missing Skyrme coefficient."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def main() -> None:
    sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.diag([1,-1]).astype(complex)
    p=(np.eye(2)+sz)/2
    dpx=sx/2; dpy=sy/2
    curvature=p@(dpx@dpy-dpy@dpx)@p
    result={
      "gate":"version5_superconnection_skyrme_coefficient_gate",
      "candidates":{
        "maurer_cartan":{"connection":"L=V^-1 dV","curvature":"dL+L^2=0","produces_E4":False},
        "grassmann_connection":{"connection":"A=P dP","curvature":"F=P(dP)^2","sample_curvature_norm":float(np.linalg.norm(curvature)),"produces_E4":True,"requires_spatial_projector":True},
        "higher_dimensional_YM":{"produces_E2_and_E4":True,"requires_extra_profile_or_dimension":True,"coefficient_ratio_internal":False}},
      "coefficient_ledger":{"E2_source":"tau([N,V]*[N,V])","E4_source":"tau(F_P*F_P)","same_parent_derivation":False,"relative_dimensionful_scale_fixed":False},
      "verdict":{"pure_superconnection_closes_action":False,"projector_curvature_is_candidate":True,"current_version_physical_radius":"not_derived","next_gate":"version5_projector_superconnection_common_scale_gate"}}
    out=Path(__file__).resolve().parents[1]/"results"/"s2t_v5_superconnection_skyrme_coefficient_gate_results.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert np.linalg.norm(curvature)>0
    print(out)
if __name__=="__main__": main()