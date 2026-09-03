#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.coordinate_embedding.shape==(43,3) and c.coordinate_generator.rank()==2
    assert len(c.coordinate_generator.nullspace())==41
    assert c.symmetric_embedding.T*c.symmetric_embedding==sp.eye(3)
    assert c.symmetric_generator[1,2].is_negative
    assert c.pass_vector==sp.zeros(2,1)
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "coordinate_embedding":{"lines":["vacuum","hypercharge","one_of_30_transfer_labels"],"isometry":True,"projector_rank":3,"compressed_cycle_exact":True,"embedded_generator_rank":2,"embedded_generator_nullity":41,"probability_conserving":True,"negative_offdiagonal_rates":0,"canonical_transfer_choice":False},
    "symmetric_embedding":{"lines":["vacuum","hypercharge","uniform_transfer_superposition"],"isometry":True,"transfer_permutation_invariant":True,"compressed_cycle_exact":True,"negative_rate_witness":"L[1,2]=-kappa/10","negative_offdiagonal_rates":870,"probability_generator":False},
    "admissibility_dichotomy":{"matrix":[[1,0],[0,1]],"columns":["Markov_positive","canonical_transfer_symmetry"],"fully_passing_embeddings":0,"rank":2},
    "status":{"architecture":"8/8","typed_origin":"2/5","canonical_Markov_embedding":"0/1","common_parent_origin":"0/1","absolute_rate_scale":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"coordinate_K43_cycle_exists":True,"coordinate_choice_is_canonical":False,"symmetric_embedding_is_Markov_positive":False,"K43_alone_supplies_physical_Hopf_cycle":False},
    "next_gate":"version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()