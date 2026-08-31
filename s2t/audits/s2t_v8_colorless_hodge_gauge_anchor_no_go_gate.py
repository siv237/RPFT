#!/usr/bin/env python3
"""Test whether the final colorless Hodge vacuum can anchor f0 by its gauge trace."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_colorless_hodge_gauge_anchor_no_go_gate_results.json"


EDGE_KEYS = {
    "L_L--Y_R": "L_L_Y_R",
    "Q_L--Y_R": "Q_L_Y_R",
    "X_L--X_R": "X_L_X_R",
    "X_L--e_R": "X_L_e_R",
    "X_L--Y_R": "X_L_Y_R",
    "X_L--d_R": "X_L_d_R",
    "X_L--u_R": "X_L_u_R",
    "X_R--Y_L": "Y_L_X_R",
    "Y_L--e_R": "Y_L_e_R",
    "Y_L--Y_R": "Y_L_Y_R",
    "L_L--X_R": "L_L_X_R",
}


def frac(value: str | int) -> Fraction:
    return Fraction(str(value))


def sum_indices(edges, rows):
    chosen = [rows[EDGE_KEYS[edge]] for edge in edges]
    return {
        "complex_dimension": sum(int(row["complex_dimension"]) for row in chosen),
        "u1_trace_index": sum((frac(row["u1_trace_index"]) for row in chosen), Fraction()),
        "su2_dynkin_index": sum((frac(row["su2_dynkin_index"]) for row in chosen), Fraction()),
        "su3_dynkin_index": sum((frac(row["su3_dynkin_index"]) for row in chosen), Fraction()),
    }


def serialise_indices(indices):
    return {
        key: str(value) if isinstance(value, Fraction) else value
        for key, value in indices.items()
    }


def main():
    selector = json.loads((ROOT / "s2t/results/s2t_v7_color_preserving_quadratic_selector_origin_gate_results.json").read_text(encoding="utf-8"))
    carrier = json.loads((ROOT / "s2t/results/s2t_v7_full_gauge_weighted_edge_carrier_gate_results.json").read_text(encoding="utf-8"))
    anchor = json.loads((ROOT / "s2t/results/s2t_v7_common_gauge_f0_anchor_gate_results.json").read_text(encoding="utf-8"))

    rows = {row["edge"]: row for row in carrier["minimal_intertwiner_lift"]["edges"]}
    active = selector["hodge_selector"]["negative_edges"]
    spectator = selector["hodge_selector"]["positive_edges"]
    active_indices = sum_indices(active, rows)
    spectator_indices = sum_indices(spectator, rows)
    full_indices = sum_indices(active + spectator, rows)

    zero = Fraction()
    assert len(active) == 4 and len(spectator) == 7
    assert set(active).isdisjoint(spectator)
    assert all(rows[EDGE_KEYS[edge]]["minimal_multiplet"] == "(1,1)_0" for edge in active)
    assert active_indices["u1_trace_index"] == zero
    assert active_indices["su2_dynkin_index"] == zero
    assert active_indices["su3_dynkin_index"] == zero
    gauge_keys = ("u1_trace_index", "su2_dynkin_index", "su3_dynkin_index")
    assert all(spectator_indices[key] == full_indices[key] for key in gauge_keys)
    expected = carrier["gauge_index_audit"]["edge_indices_one_copy"]
    assert full_indices["complex_dimension"] == expected["complex_dimension"]
    assert full_indices["u1_trace_index"] == frac(expected["u1_trace_index"])
    assert full_indices["su2_dynkin_index"] == frac(expected["su2_dynkin_index"])
    assert full_indices["su3_dynkin_index"] == frac(expected["su3_dynkin_index"])
    assert anchor["verdict"]["common_physical_gauge_anchor_admitted"] is False

    result = {
        "gate": "version8_colorless_hodge_gauge_anchor_no_go_gate",
        "final_hodge_support": {
            "active_edges": active,
            "active_edge_count": len(active),
            "all_active_multiplets": "(1,1)_0",
            "active_indices": serialise_indices(active_indices),
            "active_scalar_potential_is_nonzero": True,
            "active_gauge_kinetic_trace_is_zero": True,
        },
        "spectator_support": {
            "edges": spectator,
            "edge_count": len(spectator),
            "indices": serialise_indices(spectator_indices),
            "carries_all_edge_carrier_gauge_index": all(
                spectator_indices[key] == full_indices[key] for key in gauge_keys
            ),
        },
        "full_edge_carrier": {
            "indices": serialise_indices(full_indices),
            "indices_are_group_dependent": True,
            "single_scalar_q_G_read_from_active_vacuum": False,
        },
        "trace_closure_test": {
            "conditional_dictionary": anchor["conditional_dictionary"],
            "active_q_G_is_zero_for_every_gauge_factor": True,
            "formula_f0_equals_6pi2_over_qGg2_is_singular_on_active_support": True,
            "adding_charged_spectators_changes_the_traced_carrier": True,
            "common_product_operator_embedding_already_derived": False,
            "same_trace_relative_hodge_metric_fixed": False,
        },
        "verdict": {
            "active_colorless_gauge_anchor_exists": False,
            "full_spectator_gauge_index_nonzero": True,
            "same_trace_f0_closure_derived": False,
            "primitive_C_current_architecture_closed": True,
            "status": "colorless_active_hodge_support_is_gauge_trace_invisible_no_go",
            "next_step": "audit_the_remaining_second_family_tensor_primitive_against_version4_no_go_results",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()