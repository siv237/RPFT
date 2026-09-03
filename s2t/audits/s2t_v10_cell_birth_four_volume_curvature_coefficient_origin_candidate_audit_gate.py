#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_curvature_density_parent_origin_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_curvature_coefficient_origin_candidate_audit_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.candidate_matrix.shape==(8,6) and c.candidate_matrix.rank()==3
    assert c.pass_vector==sp.zeros(8,1)
    assert c.coefficient_constraint_map.rank()==2
    assert c.coefficient_constraint_map.nullspace()==[sp.Matrix([-2,-1,1])]
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "candidates":["cosmological_curvature","spectral_cutoff","clock_energy","inverse_cell_length","cell_curvature","KMS_temperature","topological_density","induced_matter_loop"],
    "criteria":["paired_dimensions","internal","target_independent","derived_by_common_parent","typed_into_A_B","breaks_scale_orbit"],
    "candidate_matrix":[list(map(int,c.candidate_matrix.row(i))) for i in range(8)],"candidate_matrix_rank":3,"passing_candidates":0,"maximum_score":"4/6","closest_candidates":["spectral_cutoff","induced_matter_loop"],
    "generic_scale_seed":{"seed_dimension":"L^-2","coefficients":{"A":"alpha*m^2","B":"beta*m"},"dimensionless_ratio":"B^2/A=beta^2/alpha","selected_scale":"q*=beta/(2*alpha*m)","selected_invariant":"q* m=beta/(2*alpha)","scale_orbit":"(q,m)->(s^2*q,m/s^2)"},
    "coefficient_constraint":{"rank":2,"nullity":1,"kernel":"(-2,-1,1)","parent_origin_column":0,"orbit_break_column":0},
    "status":{"candidate_coverage":"8/8","origin_ledger":"3/5","physical_coefficient_pair":"0/1","absolute_cell_scale":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"current_candidate_derives_A_and_B":False,"dimensionally_covariant_pair_breaks_scale_orbit":False,"induced_matter_loop_requires_dedicated_origin_test":True},
    "next_gate":"version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()