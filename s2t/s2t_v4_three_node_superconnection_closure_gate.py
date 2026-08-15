#!/usr/bin/env python3
import itertools
import json
from pathlib import Path

import sympy as sp


def admissible_architectures(node_count):
    rows = []
    nodes = range(node_count)
    for parities in itertools.product((0, 1), repeat=node_count):
        for charges in itertools.product((0, 1), repeat=node_count):
            for source in nodes:
                for scalar_target in nodes:
                    for oneform_target in nodes:
                        if len({source, scalar_target, oneform_target}) < 3:
                            continue
                        scalar_charge = charges[scalar_target] - charges[source]
                        oneform_charge = charges[oneform_target] - charges[source]
                        scalar_internal_parity = (
                            parities[scalar_target] - parities[source]
                        ) % 2
                        oneform_internal_parity = (
                            parities[oneform_target] - parities[source]
                        ) % 2
                        scalar_total_parity = scalar_internal_parity
                        oneform_total_parity = (oneform_internal_parity + 1) % 2
                        if (
                            abs(scalar_charge) == 1
                            and abs(oneform_charge) == 1
                            and scalar_total_parity == 1
                            and oneform_total_parity == 1
                        ):
                            rows.append(
                                {
                                    "parities": list(parities),
                                    "charges": list(charges),
                                    "source": source,
                                    "scalar_target": scalar_target,
                                    "oneform_target": oneform_target,
                                }
                            )
    return rows


def main():
    two_node = admissible_architectures(2)
    three_node = admissible_architectures(3)

    c = sp.symbols("c", real=True)
    inertia = 1 - c
    nonlinear = sp.Rational(8, 1) / inertia + sp.Rational(8, 3) * sp.log(
        inertia
    )
    canonical_plaquette = 1 - c
    periodic_primitive = sp.Rational(1, 45) * c
    full_candidate = sp.simplify(
        nonlinear + canonical_plaquette + periodic_primitive
    )
    target_up_to_constant = sp.simplify(
        nonlinear - sp.Rational(44, 45) * c
    )

    chosen = {
        "nodes": ["E0_plus", "E1_minus", "E2_plus"],
        "parities": [0, 1, 0],
        "root_charges": [0, 1, 1],
        "zero_form_edge": "E0_plus -> E1_minus",
        "one_form_edge": "E0_plus -> E2_plus",
    }

    results = {
        "status": "minimal_three_node_graded_superconnection_embeds_the_exact_reduced_Wilson_complex_at_quadratic_order",
        "date": "2026-08-12",
        "minimality_scan": {
            "two_node_survivors": len(two_node),
            "three_node_survivors": len(three_node),
            "minimum_nodes": 3 if three_node and not two_node else None,
            "reason": (
                "A charged zero-form needs an odd internal map, while a charged one-form of total "
                "odd degree needs an even internal map. Distinct targets are therefore required."
            ),
        },
        "chosen_architecture": chosen,
        "quadratic_trace_Hodge_gate": {
            "zero_form_module": "Omega0 Hom(E0,E1) tensor End_0(V1)",
            "one_form_module": "Omega1 Hom(E0,E2) tensor End_0(V1)",
            "same_root_charge": 1,
            "same_Wilson_chord_operator": "K_theta=(2-U-U^dagger)/2=1-c",
            "cross_term": 0,
            "cross_term_reason": "different form degree and orthogonal target summands E1,E2",
            "canonical_relative_metric_parameter": False,
            "generic_spectral_Hessian_may_split_grades": True,
        },
        "reduced_effective_action": {
            "nonlinear_pair": str(nonlinear),
            "canonical_plaquette": str(canonical_plaquette),
            "periodic_primitive": str(periodic_primitive),
            "combined": str(full_candidate),
            "target_up_to_constant": str(target_up_to_constant),
            "difference_is_constant": sp.simplify(
                sp.diff(full_candidate - target_up_to_constant, c)
            )
            == 0,
            "constant_difference": str(
                sp.simplify(full_candidate - target_up_to_constant)
            ),
        },
        "scientific_verdict": {
            "positive": (
                "A minimal three-node Z2-graded bundle removes the parity/charge obstruction. "
                "The canonical trace-Hodge metric makes the charged zero-form and charged one-form "
                "orthogonal and exposes the same Wilson chord operator on both grades. Adding the "
                "canonical plaquette and the already known periodic primitive reproduces the full "
                "gap shape up to an irrelevant constant."
            ),
            "negative": (
                "This is a quadratic configuration-metric embedding, not yet a derivation from a "
                "specific local curvature or spectral action. Generic spectral Hessians can weight "
                "the two grades differently, and the compact radial constraint, gauge fixing, "
                "interaction Jacobian, and periodic primitive must still be computed in one model."
            ),
            "next_gate": (
                "Choose the minimal three-node superconnection curvature action, expand it through "
                "quartic order, and verify that gauge/BV reduction preserves the fixed-charge sector, "
                "the 16-mode determinant, and the linear primitive without a new polarization."
            ),
        },
    }
    Path("s2t_v4_three_node_superconnection_closure_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "two_node_survivors": len(two_node),
                "three_node_survivors": len(three_node),
                "minimum_nodes": results["minimality_scan"]["minimum_nodes"],
                "quadratic_cross_term": 0,
                "full_shape_exact_up_to_constant": results[
                    "reduced_effective_action"
                ]["difference_is_constant"],
                "remaining": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()