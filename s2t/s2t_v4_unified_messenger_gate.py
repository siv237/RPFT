import json
from fractions import Fraction


sm_components = {
    "Q": {"dimension": 6, "Y2_trace": Fraction(1, 6), "SU2_trace": Fraction(3, 2), "SU3_trace": Fraction(1, 1), "SU5_piece": "10"},
    "u_c": {"dimension": 3, "Y2_trace": Fraction(4, 3), "SU2_trace": Fraction(0, 1), "SU3_trace": Fraction(1, 2), "SU5_piece": "10"},
    "e_c": {"dimension": 1, "Y2_trace": Fraction(1, 1), "SU2_trace": Fraction(0, 1), "SU3_trace": Fraction(0, 1), "SU5_piece": "10"},
    "d_c": {"dimension": 3, "Y2_trace": Fraction(1, 3), "SU2_trace": Fraction(0, 1), "SU3_trace": Fraction(1, 2), "SU5_piece": "bar5"},
    "L": {"dimension": 2, "Y2_trace": Fraction(1, 2), "SU2_trace": Fraction(1, 2), "SU3_trace": Fraction(0, 1), "SU5_piece": "bar5"},
    "nu_c": {"dimension": 1, "Y2_trace": Fraction(0, 1), "SU2_trace": Fraction(0, 1), "SU3_trace": Fraction(0, 1), "SU5_piece": "1"},
}


def traces(component_names):
    c_y = sum(sm_components[name]["Y2_trace"] for name in component_names)
    return {
        "C_Y": c_y,
        "C_1_GUT": Fraction(3, 5) * c_y,
        "C_2": sum(sm_components[name]["SU2_trace"] for name in component_names),
        "C_3": sum(sm_components[name]["SU3_trace"] for name in component_names),
    }


pieces = {
    "10": [name for name, item in sm_components.items() if item["SU5_piece"] == "10"],
    "bar5": [name for name, item in sm_components.items() if item["SU5_piece"] == "bar5"],
    "1": [name for name, item in sm_components.items() if item["SU5_piece"] == "1"],
    "16": list(sm_components),
}

piece_traces = {name: traces(components) for name, components in pieces.items()}
piece_beta_weyl = {
    name: {key: Fraction(2, 3) * value for key, value in values.items() if key != "C_Y"}
    for name, values in piece_traces.items()
}
vectorlike_16_beta = {
    key: 2 * value for key, value in piece_beta_weyl["16"].items()
}

su5_packages = {
    "10_plus_bar10": ["u_R", "e_R", "Q_L"],
    "5_plus_bar5": ["d_R", "L_L"],
    "1_plus_1": ["nu_R"],
}

result = {
    "gate": "version4_unified_messenger",
    "sm_components_of_so10_spinor_16": {
        component: {
            name: str(value) if isinstance(value, Fraction) else value
            for name, value in data.items()
        }
        for component, data in sm_components.items()
    },
    "su5_decomposition": "16 = 10 + bar5 + 1",
    "piece_traces": {
        piece: {name: str(value) for name, value in values.items()}
        for piece, values in piece_traces.items()
    },
    "piece_beta_contributions_one_weyl_multiplet": {
        piece: {name: str(value) for name, value in values.items()}
        for piece, values in piece_beta_weyl.items()
    },
    "vectorlike_16_plus_bar16_beta_shift": {
        name: str(value) for name, value in vectorlike_16_beta.items()
    },
    "vectorlike_16_beta_shifts_equal": len(set(vectorlike_16_beta.values())) == 1,
    "su5_packages_needed_without_so10": su5_packages,
    "su5_representation_types_needed": len(su5_packages),
    "single_so10_representation_type_covers_all_sectors": True,
    "one_vectorlike_16_pair_weyl_state_count": 32,
    "neutral_plus_hidden_charged_chain_weyl_state_count": 64,
    "degenerate_complete_multiplet_changes_beta_differences": False,
    "pairwise_crossing_scales_change_at_one_loop": False,
    "threshold_repair_requirement": "split Standard Model components inside complete SU5 pieces or add incomplete multiplets",
    "status": "SO10-type vectorlike messengers solve representation coverage but not the one-loop gauge mismatch when complete components are degenerate",
}

with open("s2t_v4_unified_messenger_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))