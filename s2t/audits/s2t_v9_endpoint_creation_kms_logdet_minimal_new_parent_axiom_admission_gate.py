#!/usr/bin/env python3
"""Exact ProofDSL audit of the minimal new KMS logdet parent axiom."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from s2t.proofdsl.examples.version9_kms_minimal_new_parent_axiom import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT=Path(__file__).resolve().parents[2]
STEM="endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate"
OUTPUT=ROOT/f"s2t/results/s2t_v9_{STEM}_results.json"


def main() -> None:
    predecessor=json.loads((ROOT/"s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate_results.json").read_text())
    gate=f"version9_{STEM}"
    assert predecessor["next_gate"]==gate and SPEC.identifier==gate
    c=build_certificate(); verified=verify_gate(SPEC)
    result={
        "date":"2026-09-01","gate":gate,"predecessor":predecessor["gate"],
        "axiom":{
            "formula":"B_lambda=-lambda(log det R_theta+log det R_kappa)",
            "domain":"positive type operators with weighted trace five",
            "required_sign":"lambda>0","functional_package_count":1,
            "new_continuous_stiffness":"lambda",
        },
        "exact_selection":{
            "stationary_shape":[1,1,1,1],"shape_rank":4,
            "hessian_determinant":"9 lambda^4/25",
            "unit_spectrum":[["3/5",2],[1,2]],
            "zero_lambda_rank":0,
            "minimum_independent_of_positive_lambda":True,
            "fluctuation_stiffness_independent_of_lambda":False,
        },
        "sign_witness":{
            "shape":["1/2",1,"7/6"],"weighted_trace":5,
            "one_package_determinant":"343/432",
            "determinant_defect":"89/432",
            "two_package_determinant":"117649/186624",
            "wrong_sign_is_unbounded_at_boundary":True,
        },
        "proofdsl":{
            "status":"lcf-checked","obligation_count":len(verified.obligations),
            "obligations":[name for name,_ in verified.obligations],
            "certificate_sha256":verified.sha256,"floating_point_values":0,
        },
        "ledgers":{
            "minimal_functional_axiom_admission_satisfied":1,"minimal_functional_axiom_admission_tested":1,
            "relative_shape_selection_satisfied":4,"relative_shape_selection_tested":4,
            "positive_sign_required_satisfied":1,"positive_sign_required_tested":1,
            "stiffness_parent_origin_satisfied":0,"stiffness_parent_origin_tested":1,
            "physical_logdet_derivation_satisfied":0,"physical_logdet_derivation_tested":1,
        },
        "verdict":{
            "minimal_new_axiom_admitted":True,
            "axiom_is_derived_from_old_parent":False,
            "one_term_controls_all_shapes":True,
            "positive_coefficient_changes_selected_shape":False,
            "positive_coefficient_changes_fluctuations":True,
            "physical_four_slot_parent_closed":False,
        },
        "next_gate":"version9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate",
        "floating_point_values":0,
    }
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)


if __name__=="__main__": main()