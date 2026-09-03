#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate_results.json"


def main()->None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate_results.json").read_text())
    gate="version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.embedding.shape==(258,3) and c.embedding.T*c.embedding==sp.eye(3)
    assert c.projector.rank()==3 and c.product_generator.rank()==2
    assert c.product_generator*c.stationary_state==sp.zeros(258,1)
    assert c.rate_clock_map.nullspace()==[sp.Matrix([-1,-1,1])]
    result={"date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
    "product_carrier":{"cell_dimension":43,"KMS_dimension":6,"product_dimension":258,"cycle_vertices":["vacuum_x_source","hypercharge_x_source","vacuum_x_singlet"],"embedding_isometry":True,"projector_rank":3},
    "typed_cycle":{"hypercharge_compression":[0,1,0],"KMS_singlet_compression":[0,0,1],"compressed_cycle_exact":True,"product_generator_rank":2,"probability_conserving":True,"negative_offdiagonal_rates":0,"stationary_state_normalized":True},
    "throughflow":{"edge_current":"kappa/3","cycle_affinity":"3*log(2)","entropy_production":"kappa*log(2)"},
    "remaining_scale_orbit":{"transformation":"kappa->c*kappa, t->t/c","map_rank":2,"map_nullity":1,"absolute_rate_derived":False},
    "status":{"architecture":"10/10","typed_origin":"5/7","canonical_Markov_embedding":"1/1","absolute_conductance":"0/1","common_parent_origin":"0/1"},
    "proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},
    "verdict":{"K43_KMS_product_supplies_canonical_cycle_vertices":True,"canonical_product_cycle_is_Markov_positive":True,"product_embedding_derives_absolute_rate":False},
    "next_gate":"version10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()