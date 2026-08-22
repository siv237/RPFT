#!/usr/bin/env python3
"""Compare the dimension and sphaleron-index maps on the H15 representation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_anomaly_to_toeplitz_product_map_gate_results.json"


def main() -> None:
    representation = {
        "SU2_fundamental_doublet_copies": 4,
        "SU2_singlet_copies": 7,
        "dimension_fundamental": 2,
        "dimension_singlet": 1,
        "sphaleron_index_fundamental": 1,
        "sphaleron_index_singlet": 0,
    }

    dimension_map = (
        representation["SU2_fundamental_doublet_copies"]
        * representation["dimension_fundamental"]
        + representation["SU2_singlet_copies"]
        * representation["dimension_singlet"]
    )
    sphaleron_index_map = (
        representation["SU2_fundamental_doublet_copies"]
        * representation["sphaleron_index_fundamental"]
        + representation["SU2_singlet_copies"]
        * representation["sphaleron_index_singlet"]
    )

    formal_product_index = 1 * dimension_map
    physical_equivariant_product_index = sphaleron_index_map

    project_component_ranks = [12, 3]
    physical_component_flows = [3, 1]
    component_rank_to_flow_ratios = [
        project_component_ranks[i] / physical_component_flows[i]
        for i in range(2)
    ]

    result = {
        "gate": "version6_spectral_transition_anomaly_to_toeplitz_product_map_gate",
        "physical_SU2_representation_of_H15": {
            "class": "4[fundamental doublet] + 7[singlet]",
            **representation,
        },
        "two_additive_maps": {
            "forgetful_dimension": dimension_map,
            "sphaleron_index_pairing": sphaleron_index_map,
            "maps_are_equal_on_H15": dimension_map == sphaleron_index_map,
        },
        "external_product_test": {
            "unit_sphaleron_flow": 1,
            "formal_nonequivariant_product_with_rank_q0": formal_product_index,
            "physical_equivariant_product": physical_equivariant_product_index,
            "formal_product_derives_q0": False,
            "formal_product_uses_q0_as_input": True,
            "gauge_representation_is_preserved_by_formal_rank_only_product": False,
        },
        "component_test": {
            "project_ranks": project_component_ranks,
            "physical_sphaleron_flows": physical_component_flows,
            "rank_to_flow_ratios": component_rank_to_flow_ratios,
            "single_common_rescaling_exists": len(set(component_rank_to_flow_ratios)) == 1,
        },
        "real_KO6_comparison": {
            "formal_decorated_pair": [-formal_product_index, formal_product_index],
            "physical_sphaleron_pair": [-physical_equivariant_product_index, physical_equivariant_product_index],
            "ordinary_sum_formal": 0,
            "ordinary_sum_physical": 0,
            "pairs_are_identical": formal_product_index == physical_equivariant_product_index,
        },
        "verdict": {
            "formal_KK_product_with_rank15_exists": True,
            "physical_sphaleron_operator_produces_rank15_class": False,
            "rank15_remains_classification_ledger": True,
            "rank15_is_sphaleron_birth_multiplicity": False,
            "physical_closure": False,
            "status": "forgetting SU(2) equivariance gives the input dimension 15, whereas the physical equivariant index pairing gives 4",
        },
        "next_gate": "version6_spectral_transition_class15_physical_role_branch_decision_gate",
    }

    assert dimension_map == 15
    assert sphaleron_index_map == 4
    assert formal_product_index == 15
    assert physical_equivariant_product_index == 4
    assert project_component_ranks == [12, 3]
    assert physical_component_flows == [3, 1]
    assert component_rank_to_flow_ratios == [4.0, 3.0]
    assert not result["component_test"]["single_common_rescaling_exists"]
    assert not result["real_KO6_comparison"]["pairs_are_identical"]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()