#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_topological_quantum_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_topological_quantum_candidate_audit_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_spectral_counting_measure_origin_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.candidate_matrix.shape==(8,5) and c.candidate_matrix.rank()==2
    assert c.pass_vector==sp.zeros(8,1)
    assert c.multiplicity_parent_hessian.rank()==1
    assert c.multiplicity_parent_hessian.nullspace()==[sp.Matrix([0,1])]
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "candidates":["Euler_characteristic","signature","Pontryagin_number","Dirac_index","winding_number","simplicial_cell_count","GNVW_index","K43_dimension"],
    "criteria":["protected_integer","internal","length_four_dimension","typed_volume_map","breaks_scale_orbit"],
    "candidate_matrix":[list(map(int,c.candidate_matrix.row(i))) for i in range(8)],"candidate_matrix_rank":2,"passing_candidates":0,"maximum_score":"3/5",
    "dimensional_boundary":{"all_length_four_entries":0,"all_orbit_break_entries":0,"quantized_form":"V=n*v0","scale_orbit":"v0->s^4*v0","topological_density":"rho_top=n/V -> rho_top/s^4"},
    "multiplicity_parent":{"hessian":[[1,0],[0,0]],"rank":1,"nullity":1,"kernel":"elementary volume v0"},
    "status":{"candidate_coverage":"8/8","topological_origin":"2/4","physical_volume_quantum":"0/1","absolute_clock_energy":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"topology_selects_integer_multiplicity":True,"topology_selects_elementary_four_volume":False,"topology_breaks_physical_scale_orbit":False},
    "next_gate":"version10_cell_birth_four_volume_curvature_density_parent_origin_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n";OUTPUT.write_text(text);print(OUTPUT);print(hashlib.sha256(text.encode()).hexdigest());print(verified.sha256)
if __name__=="__main__":main()