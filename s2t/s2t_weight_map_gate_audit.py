#!/usr/bin/env python3
import json
import math
from pathlib import Path


def close(left, right, tolerance=1e-12):
    return abs(left - right) <= tolerance


def main():
    tau_target = math.pi**2 + 2.0 * math.pi + 2.0 / 3.0
    neutrino_target = 23.0 + 1.0 / math.pi

    canonical_components = {
        "tau_RP3_zero_form": 1.0,
        "tau_S1_zero_form": 1.0,
        "tau_internal_average": 2.0 / 3.0,
        "neutrino_heavy_rank": 23.0,
        "neutrino_cycle_one_form": 1.0,
    }

    c0_canonical = {
        "reference_metric": "canonical_component_metric",
        "weight": 1.0,
        "tau": sum(
            canonical_components[name]
            for name in (
                "tau_RP3_zero_form",
                "tau_S1_zero_form",
                "tau_internal_average",
            )
        ),
        "neutrino": (
            canonical_components["neutrino_heavy_rank"]
            + canonical_components["neutrino_cycle_one_form"]
        ),
    }
    c0_canonical["passes_tau"] = close(c0_canonical["tau"], tau_target)
    c0_canonical["passes_neutrino"] = close(
        c0_canonical["neutrino"], neutrino_target
    )

    c0_raw_claim = {
        "classification": "not_a_second_C0_rule_under_the_frozen_reference_metric",
        "reason": (
            "Replacing canonical component norms by factor volumes changes the base "
            "inner product. It is not the same constant weight map W=1."
        ),
        "illustrative_tau": tau_target,
        "illustrative_neutrino_if_all_heavy_zero_modes_receive_pi": (
            23.0 * math.pi + 1.0 / math.pi
        ),
    }

    c1_period_rule = {
        "statement": "degree-zero amplitudes have unit weight; integral degree-one cycle has pi^-1",
        "tau": 1.0 + 1.0 + 2.0 / 3.0,
        "neutrino": 23.0 + 1.0 / math.pi,
    }
    c1_period_rule["passes_tau"] = close(c1_period_rule["tau"], tau_target)
    c1_period_rule["passes_neutrino"] = close(
        c1_period_rule["neutrino"], neutrino_target
    )

    c1_raw_claim = {
        "classification": "misclassified_as_C1",
        "reason": (
            "A raw zero-form norm is pi^2 on RP3, 2pi on S1 and another value "
            "on a different factor. Therefore raw normalization already depends on "
            "the manifold factor and belongs to C2, not degree-only C1."
        ),
    }

    c2_cell_weights = {
        "RP3_degree0": math.pi**2,
        "S1_degree0": 2.0 * math.pi,
        "finite_internal_degree0": 1.0,
        "S1_integral_degree1": 1.0 / math.pi,
    }
    c2_tau = (
        c2_cell_weights["RP3_degree0"]
        + c2_cell_weights["S1_degree0"]
        + c2_cell_weights["finite_internal_degree0"] * 2.0 / 3.0
    )
    c2_neutrino = (
        c2_cell_weights["finite_internal_degree0"] * 23.0
        + c2_cell_weights["S1_integral_degree1"]
    )
    c2 = {
        "cell_weights": c2_cell_weights,
        "tau": c2_tau,
        "neutrino": c2_neutrino,
        "passes_tau": close(c2_tau, tau_target),
        "passes_neutrino": close(c2_neutrino, neutrino_target),
        "sector_identity_used": False,
        "action_or_symmetry_derivation_present": False,
        "field_redefinition_covariance_law_present": False,
        "predictive_status": "lookup_pass_action_fail",
        "finding": (
            "C2 separates the components into enough geometric cells to reproduce both "
            "aggregates. This is a consistent metric assignment, but without an action "
            "or covariance law it is not yet a prediction of one physical measure."
        ),
    }

    results = {
        "status": "W_gate_C0_C1_fail_C2_lookup_pass_but_parent_measure_not_derived",
        "date": "2026-08-07",
        "frozen_reference_metric": {
            "name": "canonical_component_metric",
            "reason": (
                "A weight map is meaningful only relative to one fixed base inner "
                "product. Raw and canonical norms cannot be compared as two C0 weights."
            ),
            "components": canonical_components,
        },
        "targets": {
            "charged_lepton_seed": tau_target,
            "neutrino_stiffness": neutrino_target,
        },
        "class_tests": {
            "C0_canonical_constant": c0_canonical,
            "C0_raw_claim": c0_raw_claim,
            "C1_degree_and_period": c1_period_rule,
            "C1_raw_claim": c1_raw_claim,
            "C2_factor_degree_period_cells": c2,
            "C3_sector_identity": {
                "admissible": False,
                "reason": "Sector-labelled weights are a prohibited special readout.",
            },
        },
        "covariance_gate": {
            "required": (
                "Under a field-coordinate rescaling x'=a x, the metric and couplings "
                "must transform together so that physical quadratic forms and vertices "
                "are invariant."
            ),
            "provided_by_C2_table": False,
            "passes": False,
        },
        "logical_scope": {
            "simple_universal_weight_rules_rejected": True,
            "C2_numerical_assignment_exists": True,
            "one_parent_principle_rejected": False,
            "independence_of_all_remaining_gaps_proved": False,
            "reason": (
                "Failure of C0-C1 and underivation of C2 show that the common measure is "
                "not presently derived. They do not prove that no deeper action can "
                "generate C2 or that measure, CP, vacuum and threshold gaps are logically "
                "independent."
            ),
        },
        "scientific_verdict": {
            "algebraic_gate": "C2_passes",
            "operator_gate": "fails",
            "two_sector_predictive_gate": "fails",
            "closed_physical_predictions_added": 0,
            "next_gate": (
                "Derive the C2 cell metric as the Hessian or boundary symplectic form of "
                "one preregistered action, including its field-redefinition covariance, "
                "then test an independent EM or rotor observable."
            ),
        },
    }

    assert close(c0_canonical["tau"], 8.0 / 3.0)
    assert close(c0_canonical["neutrino"], 24.0)
    assert c0_canonical["passes_tau"] is False
    assert c0_canonical["passes_neutrino"] is False
    assert c1_period_rule["passes_tau"] is False
    assert c1_period_rule["passes_neutrino"] is True
    assert c2["passes_tau"] is True
    assert c2["passes_neutrino"] is True
    assert results["covariance_gate"]["passes"] is False
    assert results["logical_scope"]["independence_of_all_remaining_gaps_proved"] is False
    assert results["scientific_verdict"]["closed_physical_predictions_added"] == 0

    Path("s2t_weight_map_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()