#!/usr/bin/env python3
"""Multiplicity and charge audit for electroweak sphaleron spectral flow."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_sphaleron_spectral_flow_gate_results.json"


def main() -> None:
    # Full one-generation H15 blocks and the number of independent
    # left-handed SU(2) doublet crossings carried by each block.
    blocks = {
        "Q_L": {"rank": 6, "flow": 3, "baryon_weight": Fraction(1, 3)},
        "L_L": {"rank": 2, "flow": 1, "lepton_weight": Fraction(1, 1)},
        "u_R": {"rank": 3, "flow": 0},
        "d_R": {"rank": 3, "flow": 0},
        "e_R": {"rank": 1, "flow": 0},
    }

    h15_rank = sum(block["rank"] for block in blocks.values())
    flow_one_generation = sum(block["flow"] for block in blocks.values())
    flow_three_generations = 3 * flow_one_generation

    project_quark_rank = blocks["Q_L"]["rank"] + blocks["u_R"]["rank"] + blocks["d_R"]["rank"]
    project_lepton_rank = blocks["L_L"]["rank"] + blocks["e_R"]["rank"]
    sphaleron_quark_flow = blocks["Q_L"]["flow"]
    sphaleron_lepton_flow = blocks["L_L"]["flow"]

    delta_b = blocks["Q_L"]["flow"] * blocks["Q_L"]["baryon_weight"]
    delta_l = blocks["L_L"]["flow"] * blocks["L_L"]["lepton_weight"]

    result = {
        "gate": "version6_spectral_transition_sphaleron_spectral_flow_gate",
        "chern_simons_transition": {
            "delta_N_CS": 1,
            "sphaleron_midpoint_N_CS_mod_Z": "1/2",
            "spectral_flow_per_left_SU2_doublet": 1,
        },
        "one_generation": {
            "H15_block_ranks": {name: block["rank"] for name, block in blocks.items()},
            "H15_total_rank": h15_rank,
            "left_doublet_crossings": {
                "three_colored_Q_L_copies": sphaleron_quark_flow,
                "one_L_L_copy": sphaleron_lepton_flow,
                "right_singlets": 0,
                "total": flow_one_generation,
            },
            "anomaly_charges": {
                "delta_B": str(delta_b),
                "delta_L": str(delta_l),
                "delta_B_plus_L": str(delta_b + delta_l),
                "delta_B_minus_L": str(delta_b - delta_l),
            },
        },
        "three_generations": {
            "left_doublet_crossings": flow_three_generations,
            "delta_B": str(3 * delta_b),
            "delta_L": str(3 * delta_l),
        },
        "comparison_with_project_class": {
            "project_component_ranks": [project_quark_rank, project_lepton_rank],
            "sphaleron_component_flows_per_generation": [sphaleron_quark_flow, sphaleron_lepton_flow],
            "project_total_rank": h15_rank,
            "sphaleron_flow_per_generation": flow_one_generation,
            "sphaleron_flow_three_generations": flow_three_generations,
            "flow_equals_project_rank_15": flow_one_generation == h15_rank,
            "three_generation_flow_equals_project_rank_15": flow_three_generations == h15_rank,
            "numeric_12_has_same_origin_as_project_quark_rank_12": False,
            "reason": "the sphaleron counts chiral SU(2) doublet copies, while q0 counts the full one-generation coefficient-space rank including right singlets",
        },
        "real_KO6_reading": {
            "oriented_flow": [flow_one_generation, -flow_one_generation],
            "ordinary_sum": 0,
            "matches_general_conjugate_cancellation_pattern": True,
            "identifies_toeplitz_pair_minus15_plus15": False,
        },
        "verdict": {
            "spectral_transition_language_has_physical_example": True,
            "standard_sphaleron_flow_derives_project_class_15": False,
            "explicit_operator_product_map_required": True,
            "physical_closure": False,
            "status": "the sphaleron validates transition through a zero mode, but its chiral multiplicity 4 per generation is not the rank-15 Toeplitz coefficient class",
        },
        "next_gate": "version6_spectral_transition_anomaly_to_toeplitz_product_map_gate",
    }

    assert h15_rank == 15
    assert [project_quark_rank, project_lepton_rank] == [12, 3]
    assert [sphaleron_quark_flow, sphaleron_lepton_flow] == [3, 1]
    assert flow_one_generation == 4
    assert flow_three_generations == 12
    assert delta_b == delta_l == 1
    assert delta_b - delta_l == 0
    assert result["real_KO6_reading"]["ordinary_sum"] == 0
    assert not result["comparison_with_project_class"]["flow_equals_project_rank_15"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()