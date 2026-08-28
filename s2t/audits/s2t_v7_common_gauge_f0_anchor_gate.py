#!/usr/bin/env python3
"""Audit the proposed common gauge anchor for the Version VII edge carrier."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


SELECTED = {
    "L_L_Y_R": (Fraction(-1, 2), Fraction(-1, 2)),
    "Q_L_Y_R": (Fraction(1, 6), Fraction(-1, 2)),
    "X_L_X_R": (Fraction(-1), Fraction(-1)),
    "X_L_e_R": (Fraction(-1), Fraction(-1)),
    "X_L_u_R": (Fraction(-1), Fraction(2, 3)),
    "Y_L_Y_R": (Fraction(-1, 2), Fraction(-1, 2)),
}


def main() -> None:
    edge_rows = []
    for edge, (source_y, target_y) in SELECTED.items():
        charge = target_y - source_y
        edge_rows.append(
            {
                "edge": edge,
                "source_hypercharge": str(source_y),
                "target_hypercharge": str(target_y),
                "induced_hypercharge": str(charge),
                "hypercharge_square": str(charge * charge),
                "gauge_singlet_under_u1": charge == 0,
                "hodge_block_weight": 1,
            }
        )

    q_squares = [Fraction(row["hypercharge_square"]) for row in edge_rows]
    singlets = sum(row["gauge_singlet_under_u1"] for row in edge_rows)
    charged = len(edge_rows) - singlets
    reduced_u1_index = sum(q_squares, Fraction(0))

    q_examples = [Fraction(2), Fraction(4), Fraction(8)]
    conditional = []
    for q_g in q_examples:
        # C0*q_G/3 = 1/(4 g^2), lambda_E = 1/(8 C0).
        conditional.append(
            {
                "q_G": str(q_g),
                "f0_times_g_squared_over_pi_squared": float(Fraction(6, 1) / q_g),
                "lambda_E_over_g_squared": float(q_g / 6),
            }
        )

    result = {
        "gate": "version7_common_gauge_f0_anchor_gate",
        "conditional_dictionary": {
            "common_a4_coefficient": "C0=f0/(8*pi^2)",
            "gauge_coefficient": "C0*q_G/3",
            "canonical_matching": "C0*q_G/3=1/(4*g^2)",
            "f0": "6*pi^2/(q_G*g^2)",
            "edge_quartic": "lambda_E=q_G*g^2/6",
            "old_relative_u1_if_q_G_equals_2": "lambda_E=g^2/3",
        },
        "selected_edge_hypercharge_audit": {
            "rows": edge_rows,
            "singlet_edges": singlets,
            "charged_edges": charged,
            "unweighted_reduced_u1_index": str(reduced_u1_index),
            "all_hodge_weights_equal": all(row["hodge_block_weight"] == 1 for row in edge_rows),
            "all_gauge_weights_equal": len(set(q_squares)) == 1,
        },
        "representation_trace_audit": {
            "conditional_examples": conditional,
            "lambda_depends_on_total_gauge_index": True,
            "reduced_edge_trace_determines_total_gauge_index": False,
            "reason": (
                "The 11-dimensional edge-label trace suppresses gauge multiplet dimensions "
                "and Dynkin indices; the physical curvature trace does not."
            ),
        },
        "verdict": {
            "formal_f0_cancellation_against_a_fixed_gauge_trace": True,
            "reuse_q_G_equals_2_without_full_carrier": False,
            "common_physical_gauge_anchor_admitted": False,
            "status": "conditional_formula_and_trace_mismatch_no_go",
            "next_gate": "version7_full_gauge_weighted_edge_carrier_gate",
        },
        "numerical_checks": {
            "pi_squared": math.pi**2,
            "q_G_2_lambda_over_g_squared": 1 / 3,
            "selected_reduced_u1_index": float(reduced_u1_index),
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_common_gauge_f0_anchor_gate_results.json"
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()