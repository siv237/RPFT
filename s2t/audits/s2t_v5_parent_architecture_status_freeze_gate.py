#!/usr/bin/env python3
"""Freeze the Version V parent-architecture status from all machine results."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUTPUT = RESULTS / "s2t_v5_parent_architecture_status_freeze_gate_results.json"

EXPECTED = [
    "architecture_selection_gate",
    "carrier_measure_freeze_gate",
    "foundational_relative_architecture_gate",
    "reduction_triangle_cocycle_gate",
    "boundary_parent_trace_freeze_gate",
    "finite_geometry_complexity_bound_gate",
    "real_selector_leaf_ko6_gate",
    "family_algebra_rectangle_gate",
    "ordinary_spectral_moment_map_no_go",
    "nonordinary_architecture_fork_gate",
    "oriented_height_hodge_ko6_gate",
    "twisted_family_automorphism_gate",
    "minimal_twist_doubling_budget_gate",
    "real_scalar_flip_twisted_ko6_gate",
    "flip_twisted_trace_positivity_gate",
    "derived_moment_map_minimal_data_gate",
]


def load(topic):
    path = RESULTS / f"s2t_v5_{topic}_results.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["gate"] == f"version5_{topic}"
    return data


records = {topic: load(topic) for topic in EXPECTED}
assert len(records) == 16

selection = records["architecture_selection_gate"]
carrier = records["carrier_measure_freeze_gate"]
relative = records["foundational_relative_architecture_gate"]
triangle = records["reduction_triangle_cocycle_gate"]
boundary = records["boundary_parent_trace_freeze_gate"]
complexity = records["finite_geometry_complexity_bound_gate"]
leaf = records["real_selector_leaf_ko6_gate"]
rectangle = records["family_algebra_rectangle_gate"]
ordinary = records["ordinary_spectral_moment_map_no_go"]
fork = records["nonordinary_architecture_fork_gate"]
height = records["oriented_height_hodge_ko6_gate"]
twist = records["twisted_family_automorphism_gate"]
doubling = records["minimal_twist_doubling_budget_gate"]
twisted_ko6 = records["real_scalar_flip_twisted_ko6_gate"]
twisted_trace = records["flip_twisted_trace_positivity_gate"]
derived = records["derived_moment_map_minimal_data_gate"]

# Procedural V.0 passes.
assert selection["protocol"]["observed_inputs_used"] is False
assert selection["protocol"]["selection_is_architecture_pass"] is False
assert selection["global_status"]["phenomenology_authorized"] is False

# Carrier/relative class.
assert carrier["verdict"]["state_normalization"] == "pass"
assert carrier["verdict"]["parent_measure"] == "fail"
assert relative["verdict"]["mathematical_architecture_pass"] is False
assert triangle["verdict"]["categorical_architecture_pass"] is False

# Boundary class.
assert boundary["verdict"]["one_parent_trace"] is False
assert boundary["verdict"]["mathematical_parent_architecture_pass"] is False

# Finite, twisted and derived class.
assert complexity["verdict"]["graph_enumeration"] is True
assert complexity["verdict"]["finite_geometry_exists"] is False
assert leaf["verdict"]["selector_leaf"] == "fail"
assert rectangle["verdict"]["standard_finite_geometry_budget_route"] == "closed"
assert ordinary["verdict"]["spectral_blindness_theorem"] is True
assert ordinary["verdict"]["ordinary_one_trace_moment_map_origin"] == "closed"
assert fork["verdict"]["algebraic_orientation_selector"] == "pass"
assert fork["verdict"]["parent_architecture"] == "not_passed"
assert height["verdict"]["height_hodge_algebraic_identity"] == "pass"
assert height["verdict"]["height_uniqueness"] == "fail"
assert twist["verdict"]["coefficient_free_current_algebra_twisted_family_route"] == "closed"
assert doubling["verdict"]["twisted_parent_action"] == "not_passed"
assert twisted_ko6["verdict"]["faithful_twisted_KO6_representation"] == "pass"
assert twisted_ko6["verdict"]["ordinary_spectral_moment_map_sign"] == "fail"
assert twisted_trace["verdict"]["finite_real_scalar_twisted_route"] == "closed"
assert derived["verdict"]["exact_preprojective_target"] == "pass"
assert derived["verdict"]["positive_star_canonicity"] == "fail"
assert derived["verdict"]["physical_SO3_moment_map"] == "fail"

# Every explicit physical-closure field in the ledger is false or zero.
physical_fields = []


def collect_physical_fields(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}" if path else key
            if key in {"physical_closure", "physical_closures"}:
                physical_fields.append((child, item))
            collect_physical_fields(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            collect_physical_fields(item, f"{path}[{index}]")


for topic, record in records.items():
    collect_physical_fields(record, topic)

assert physical_fields
assert all(value is False or value == 0 for _, value in physical_fields)

positive_results = [
    "fixed-carrier Gibbs state normalization",
    "bounded finite-graph enumeration",
    "order-one active-family rectangle and scalar commutant",
    "ordinary spectral-blindness theorem for the oriented Gram difference",
    "exact height-Hodge moment-map identity and full-trace normalization",
    "faithful real-scalar twisted KO6 representation and twisted first order",
    "no-go theorem for a faithful finite twisted trace or modular flip",
    "exact preprojective middle relation",
    "positive-star orientation obstruction",
    "strict SO(3) trace-pairing obstruction",
]

result = {
    "date": "2026-08-16",
    "gate": "version5_parent_architecture_status_freeze_gate",
    "source_ledger": {
        "machine_result_count": len(records),
        "topics": EXPECTED,
        "explicit_physical_closure_fields": len(physical_fields),
        "all_explicit_physical_closures_false_or_zero": True,
    },
    "architecture_classes": {
        "joint_state_carrier": {
            "state_normalization": "pass",
            "parent_measure": "fail",
            "reduction_triangle": "fail",
            "status": "closed_in_current_realization",
        },
        "boundary_source": {
            "local_modules": "partial_pass",
            "one_parent_trace": "fail",
            "joint_charge_condensate_axis_majorana_origin": "fail",
            "status": "closed_in_current_realization",
        },
        "finite_twisted_derived": {
            "bounded_enumeration": "pass",
            "ordinary_spectral_origin": "closed",
            "height_origin": "closed",
            "finite_twisted_origin": "closed",
            "minimal_preprojective_origin": "closed",
            "status": "closed_within_frozen_finite_positive_KO6_axioms",
        },
    },
    "definition_of_done": {
        "prephenomenological_selection": True,
        "observed_inputs_avoided": True,
        "one_frozen_parent_functional": False,
        "measure_covering_all_auxiliary_sectors": False,
        "full_physical_hessian_and_BV_factor": False,
        "single_trace_two_sector_normalization": False,
        "threshold_flow_without_target_derived_masses": False,
        "two_independent_blind_tests": False,
    },
    "positive_mathematical_legacy": positive_results,
    "status": {
        "early_stop_triggered": True,
        "version5_mathematical_parent_architectures": 0,
        "version5_intersector_closures": 0,
        "version5_physical_closures": 0,
        "phenomenology_authorized": False,
        "inherited_R_sci": "4/10",
        "R_sci_recalculated": False,
        "tome5": "frozen_as_obstruction_classification_under_current_axioms",
    },
    "reentry_conditions": [
        "declare a genuinely new parent object rather than rename a closed implementation",
        "derive orientation or polarization before writing the moment-map square",
        "derive the physical real form and any gauge-group enlargement",
        "produce one positive measure and one trace for at least two sectors",
        "compute the complete BV/BRST quotient and physical Hessian before phenomenology",
    ],
    "candidate_new_architectures_not_opened_here": [
        "complex symplectic or indefinite parent with a derived positive physical sector",
        "type-III modular parent with a concrete finite-sector reduction",
        "irreducible boundary Hilbert space with derived off-diagonal connectors",
    ],
    "verdict": {
        "version5_definition_of_done": False,
        "parent_architecture_achieved": False,
        "current_version5_search_menu_exhausted": True,
        "new_axiomatics_logically_possible": True,
        "physical_closure": False,
    },
    "next_gate": None,
    "next_action": "explicit_user_decision_required_before_opening_a_new_version_or_axiomatic_class",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))