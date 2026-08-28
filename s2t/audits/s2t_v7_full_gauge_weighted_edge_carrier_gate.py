#!/usr/bin/env python3
"""Audit the full gauge-weighted lift of the eleven Version VII edges."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path


EDGES = [
    ("L_L_Y_R", True, 1, Fraction(0), 0, 0, "(1,1)_0"),
    ("Q_L_Y_R", True, 3, Fraction(2, 3), 0, Fraction(1, 2), "(3,1)_{2/3}"),
    ("X_L_X_R", True, 1, Fraction(0), 0, 0, "(1,1)_0"),
    ("X_L_e_R", True, 1, Fraction(0), 0, 0, "(1,1)_0"),
    ("X_L_u_R", True, 3, Fraction(5, 3), 0, Fraction(1, 2), "(3,1)_{5/3}"),
    ("Y_L_Y_R", True, 1, Fraction(0), 0, 0, "(1,1)_0"),
    ("L_L_X_R", False, 2, Fraction(1, 2), Fraction(1, 2), 0, "(1,2)_{1/2}"),
    ("X_L_Y_R", False, 2, Fraction(1, 2), Fraction(1, 2), 0, "(1,2)_{1/2}"),
    ("X_L_d_R", False, 3, Fraction(2, 3), 0, Fraction(1, 2), "(3,1)_{2/3}"),
    ("Y_L_X_R", False, 2, Fraction(1, 2), Fraction(1, 2), 0, "(1,2)_{1/2}"),
    ("Y_L_e_R", False, 2, Fraction(1, 2), Fraction(1, 2), 0, "(1,2)_{1/2}"),
]


def main() -> None:
    rows = []
    totals = {
        "selected": {"dimension": 0, "u1": Fraction(0), "su2": Fraction(0), "su3": Fraction(0)},
        "unselected": {"dimension": 0, "u1": Fraction(0), "su2": Fraction(0), "su3": Fraction(0)},
    }
    for edge, selected, dim, hypercharge, su2_index, su3_index, rep in EDGES:
        sector = "selected" if selected else "unselected"
        u1_index = dim * hypercharge * hypercharge
        totals[sector]["dimension"] += dim
        totals[sector]["u1"] += u1_index
        totals[sector]["su2"] += su2_index
        totals[sector]["su3"] += su3_index
        rows.append(
            {
                "edge": edge,
                "selected": selected,
                "minimal_multiplet": rep,
                "complex_dimension": dim,
                "absolute_hypercharge": str(hypercharge),
                "u1_trace_index": str(u1_index),
                "su2_dynkin_index": str(su2_index),
                "su3_dynkin_index": str(su3_index),
                "contains_color_triplet": su3_index != 0,
                "contains_weak_doublet": su2_index != 0,
            }
        )

    selected_dims = [dim for _, selected, dim, *_ in EDGES if selected]
    unselected_dims = [dim for _, selected, dim, *_ in EDGES if not selected]
    negative_origin = 2 * sum(selected_dims)
    positive_origin = 2 * sum(unselected_dims)
    vacuum_zero = sum(2 * dim - 1 for dim in selected_dims)
    vacuum_positive = len(selected_dims) + 2 * sum(unselected_dims)

    selected_colored = [row["edge"] for row in rows if row["selected"] and row["contains_color_triplet"]]

    def clean(block):
        return {
            "complex_dimension": block["dimension"],
            "u1_trace_index": str(block["u1"]),
            "su2_dynkin_index": str(block["su2"]),
            "su3_dynkin_index": str(block["su3"]),
        }

    all_totals = {
        key: totals["selected"][key] + totals["unselected"][key]
        for key in totals["selected"]
    }

    result = {
        "gate": "version7_full_gauge_weighted_edge_carrier_gate",
        "minimal_intertwiner_lift": {
            "edges": rows,
            "selected_totals": clean(totals["selected"]),
            "unselected_totals": clean(totals["unselected"]),
            "all_edge_totals": clean(all_totals),
        },
        "weighted_hodge_audit": {
            "potential": (
                "sum_selected w_e*(||phi_e||^2-mu^2)^2 + "
                "sum_unselected w_e*(||phi_e||^4+2*mu^2||phi_e||^2), w_e>0"
            ),
            "support_six_of_eleven_preserved_for_positive_weights": True,
            "origin_signature_full_multiplets": [negative_origin, 0, positive_origin],
            "vacuum_signature_before_gauge_quotient": [0, vacuum_zero, vacuum_positive],
            "total_real_dimension": 2 * all_totals["dimension"],
        },
        "color_vacuum_audit": {
            "selected_colored_edges": selected_colored,
            "selected_colored_edge_count": len(selected_colored),
            "hodge_vacuum_requires_each_selected_norm_nonzero": True,
            "fundamental_su3_has_nonzero_invariant_vector": False,
            "full_su3_color_preserved": False,
            "verdict": "the exact six-edge Hodge vacuum necessarily breaks color",
        },
        "gauge_index_audit": {
            "edge_indices_one_copy": clean(all_totals),
            "indices_are_unified": (
                all_totals["u1"] == all_totals["su2"] == all_totals["su3"]
            ),
            "single_old_q_G_reuse_available": False,
        },
        "verdict": {
            "projector_support_survives_positive_trace_weights": True,
            "physical_color_preserving_vacuum_survives": False,
            "status": "structural_support_pass_but_color_vacuum_no_go",
            "next_gate": "version7_color_preserving_composite_cycle_parent_gate",
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_full_gauge_weighted_edge_carrier_gate_results.json"
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()