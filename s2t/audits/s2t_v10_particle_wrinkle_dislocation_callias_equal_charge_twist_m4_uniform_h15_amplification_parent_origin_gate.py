#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate_results.json"
def main():
    predecessor=json.loads((ROOT/"s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate_results.json").read_text()); assert predecessor["next_gate"]==SPEC.identifier
    verified=verify_gate(SPEC); c=build_certificate()
    assert c.existing_laplacian.rank()==3 and len(c.existing_laplacian.nullspace())==2
    assert c.augmented_laplacian.rank()==4 and len(c.augmented_laplacian.nullspace())==1
    assert c.uniform_channel_vector==sp.ones(15,1) and c.inherited_bridge.rank()==0
    result={"date":"2026-09-02","gate":SPEC.identifier,"predecessor":predecessor["gate"],"H15_type_graph":{"blocks":["Q_L(6)","L_L(2)","u_R(3)","d_R(3)","e_R(1)"],"inherited_edges":["Q_L-u_R","Q_L-d_R","L_L-e_R"],"incidence_rank":3,"laplacian_rank":3,"kernel_dimension":2,"component_channel_multiplicities":[12,3]},"conditional_bridge":{"edge":"Q_L-L_L","augmented_incidence_rank":4,"augmented_laplacian_rank":4,"kernel_dimension":1,"kernel":"(1,1,1,1,1)","lifted_channel_vector":"ones(15)","twist_amplifier_rank":2,"twist_amplifier_gram":"15 I2"},"inheritance":{"quark_lepton_bridge_rank":0,"relative_uniformity_selected":False,"absolute_amplitude_selected":False},"status":{"conditional_architecture":"12/12","inherited_component_amplitudes":"2","conditional_uniform_relative_amplitude":"1","physical_origin":"0/3"},"proofdsl":{"status":"lcf-checked","obligation_count":len(verified.obligations),"obligations":[n for n,_ in verified.obligations],"certificate_sha256":verified.sha256,"floating_point_values":0},"verdict":{"existing_H15_parent_selects_uniform_amplification":False,"one_cross_component_edge_is_conditionally_sufficient":True,"quark_lepton_bridge_is_inherited":False},"next_gate":"version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUT.write_text(text); print(OUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)
if __name__=="__main__": main()