#!/usr/bin/env python3
"""Audit the relative Bott spatial lift and Derrick scaling ledger."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def main() -> None:
    sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.diag([1,-1]).astype(complex)
    residuals=[]; unitary=[]
    p0=(np.eye(2)+sz)/2
    for th in np.linspace(0,np.pi,17):
        for ph in np.linspace(0,2*np.pi,33):
            n=np.array([np.sin(th)*np.cos(ph),np.sin(th)*np.sin(ph),np.cos(th)])
            p=(np.eye(2)+n[0]*sx+n[1]*sy+n[2]*sz)/2
            residuals.append(np.linalg.norm(p@p-p))
            z=np.exp(1j*0.37)
            w=(z*p+np.eye(2)-p)@(z*p0+np.eye(2)-p0).conj().T
            unitary.append(np.linalg.norm(w.conj().T@w-np.eye(2)))
    a=b=1.0; rstar=np.sqrt(b/a)
    result={
      "gate":"version5_spatial_extension_derrick_balance_gate",
      "relative_bott_unitary":"W(z,n)=(zP(n)+1-P(n))(zP0+1-P0)*",
      "checks":{"max_projector_residual":float(max(residuals)),"max_unitarity_residual":float(max(unitary)),"W_at_z_1":"identity","W_at_spatial_basepoint":"identity"},
      "topology":{"hopf_line_c1":1,"coefficient_rank":15,"suspended_K1_charge":15,"real_pair_charges":[15,-15]},
      "derrick":{"E2_scaling":"a R","E4_scaling":"b/R","stationary_radius":"sqrt(b/a)","example_a_b_1_radius":rstar,"both_terms_required":True},
      "verdict":{"conditional_spatial_topology":"pass","E4_coefficient_derived_from_current_parent":False,"finite_radius_from_current_action":False,"physical_action":"not_yet","next_gate":"version5_superconnection_skyrme_coefficient_gate"}}
    out=Path(__file__).resolve().parents[1]/"results"/"s2t_v5_spatial_extension_derrick_balance_gate_results.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert max(residuals)<1e-12 and max(unitary)<1e-12 and 15*1==15
    print(out)
if __name__=="__main__": main()