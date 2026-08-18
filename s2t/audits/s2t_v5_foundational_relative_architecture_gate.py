#!/usr/bin/env python3
"""Audit the relative/categorical clue behind the Version V architecture."""

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_foundational_relative_architecture_gate_results.json"


required_sources = {
    "tome1": "s2t/docs/main.tex",
    "pairing_diagnosis": "wiki/syntheses/kinematics-dynamics-pairing-diagnosis-2026-08-07.md",
    "relative_determinant": "wiki/questions/relative-holonomy-determinant.md",
    "mapping_cone_priority": "wiki/questions/version4-mapping-cone-spectral-priority-audit.md",
    "relative_pati_salam": "wiki/questions/pati-salam-relative-parent-action-gate.md",
    "determinant_line": "wiki/questions/version4-determinant-line-inflow-gate.md",
    "carrier_measure_fail": "wiki/questions/version5-carrier-measure-freeze-gate.md",
}
source_presence = {key: (ROOT / path).exists() for key, path in required_sources.items()}
assert all(source_presence.values())


# Exact additive coboundary test on the reduction triangle g -> s -> c -> g.
gamma = {("g", "s"): 2, ("s", "c"): -1, ("c", "g"): 3}
vertex_potential = {"g": 5, "s": -2, "c": 7}


def shift(edge, value):
    source, target = edge
    return value + vertex_potential[target] - vertex_potential[source]


gamma_shifted = {edge: shift(edge, value) for edge, value in gamma.items()}
loop_before = sum(gamma.values())
loop_after = sum(gamma_shifted.values())
open_path_before = gamma[("g", "s")] + gamma[("s", "c")]
open_path_after = gamma_shifted[("g", "s")] + gamma_shifted[("s", "c")]

assert loop_before == loop_after
assert open_path_after - open_path_before == vertex_potential["c"] - vertex_potential["g"]


# Exact multiplicative normalization test with rational weights.
ratio = {("g", "s"): Fraction(2), ("s", "c"): Fraction(3), ("c", "g"): Fraction(5)}
normalization = {"g": Fraction(7), "s": Fraction(11), "c": Fraction(13)}
ratio_shifted = {
    edge: normalization[edge[1]] / normalization[edge[0]] * value
    for edge, value in ratio.items()
}
product_before = ratio[("g", "s")] * ratio[("s", "c")] * ratio[("c", "g")]
product_after = (
    ratio_shifted[("g", "s")]
    * ratio_shifted[("s", "c")]
    * ratio_shifted[("c", "g")]
)
assert product_before == product_after


project_pattern = {
    "relative_successes": [
        "scheme-safe twisted/untwisted determinant ratios",
        "holonomy and transition functions",
        "mapping-cone response",
        "Pati-Salam relative quotient norm",
        "determinant/Pfaffian line bookkeeping",
        "defect index stability",
        "gauge-family diagonal locking",
        "exact three-cycle residual bundle",
    ],
    "absolute_failures": [
        "cross-topology determinant with free finite counterterms",
        "unique fixed-carrier selection",
        "ordinary one-trace relative quartic sign",
        "standalone Pfaffian branch orientation",
        "absolute scale from uncontrolled local expansion",
        "one common sector normalization measure",
        "derived topology/spin sum weights",
        "lifting numerical formulas to one parent action",
    ],
}

triangle_status = {
    "T_gs_geometry_to_spectrum": {
        "status": "partial",
        "reason": "Dirac/Laplace spectra are constructed for declared carriers but not uniquely across all sectors",
    },
    "T_sc_spectrum_to_correlation": {
        "status": "pass",
        "reason": "C=exp(-tau H) and H=-tau^-1 log C form an exact dictionary on the support",
    },
    "T_cg_correlation_to_geometry": {
        "status": "missing",
        "reason": "no canonical reconstruction of geometry, topology prior or counterterm trivialization",
    },
    "triangle_cocycle": {
        "status": "undefined",
        "reason": "Omega_gsc cannot be evaluated before T_cg exists",
    },
}

result = {
    "date": "2026-08-15",
    "gate": "version5_foundational_relative_architecture_gate",
    "source_presence": source_presence,
    "philosophical_clue": {
        "primary_not_object_but_admissible_transition_law": True,
        "tome1_explicitly_allows_category_of_reductions": True,
        "correlation_assembly_rule_was_never_fully_formalized": True,
    },
    "project_pattern": project_pattern,
    "additive_coboundary_test": {
        "edge_values": {f"{a}->{b}": value for (a, b), value in gamma.items()},
        "vertex_potential": vertex_potential,
        "shifted_edges": {f"{a}->{b}": value for (a, b), value in gamma_shifted.items()},
        "open_path_before": open_path_before,
        "open_path_after": open_path_after,
        "open_path_shift": open_path_after - open_path_before,
        "loop_before": loop_before,
        "loop_after": loop_after,
        "loop_invariant": loop_before == loop_after,
    },
    "multiplicative_normalization_test": {
        "loop_product_before": str(product_before),
        "loop_product_after": str(product_after),
        "loop_product_invariant": product_before == product_after,
    },
    "reduction_triangle": triangle_status,
    "verdict": {
        "relative_category_hypothesis": "admitted_as_bounded_research_direction",
        "mathematical_architecture_pass": False,
        "physical_closure": False,
        "main_missing_datum": "T_cg correlation-to-geometry reconstruction morphism",
        "interpretation": (
            "relative successes and absolute failures are consistent with a cocycle/coboundary architecture, "
            "but the project-specific reduction triangle is not yet instantiated"
        ),
    },
    "next_gate": {
        "name": "version5_reduction_triangle_cocycle_gate",
        "obligations": [
            "freeze concrete geometric, spectral and correlation objects",
            "define domains and codomains of T_gs and T_sc",
            "classify coefficient-free T_cg candidates",
            "check functorial composition and determinant-line anomalies",
            "compute or prove undefined the closed-loop defect Omega_gsc",
            "reject any T_cg requiring observed data, arbitrary topology prior or free counterterm trivialization",
        ],
    },
    "boundary_control_status": "reserved_until_reduction_triangle_verdict",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))