import json
from fractions import Fraction


right_sectors = {
    "u_R": {"SU3": "3", "SU2": "1", "Y": Fraction(2, 3)},
    "d_R": {"SU3": "3", "SU2": "1", "Y": Fraction(-1, 3)},
    "e_R": {"SU3": "1", "SU2": "1", "Y": Fraction(-1, 1)},
    "nu_R": {"SU3": "1", "SU2": "1", "Y": Fraction(0, 1)},
}

hidden_charge = {
    "observed_fermions": 0,
    "H": 0,
    "X0_L": 0,
    "X0_R": 0,
    "Xq_L": 1,
    "Xq_R": 1,
    "Omega": -1,
    "phi_h": 1,
}

vertex_hidden_charge_sums = {
    "bar(F_L) H X0_R": -hidden_charge["observed_fermions"] + hidden_charge["H"] + hidden_charge["X0_R"],
    "bar(X0_L) Omega Xq_R": -hidden_charge["X0_L"] + hidden_charge["Omega"] + hidden_charge["Xq_R"],
    "bar(Xq_L) phi_h f_R": -hidden_charge["Xq_L"] + hidden_charge["phi_h"] + hidden_charge["observed_fermions"],
}


def cycle_rank(vertices, edges, connected_components=1):
    return edges - vertices + connected_components


single_chain_graph = {
    "vertices": 4,
    "edges": 3,
    "connected_components": 1,
}
single_chain_graph["cycle_rank"] = cycle_rank(**single_chain_graph)

two_path_graph = {
    "vertices": 5,
    "edges": 5,
    "connected_components": 1,
}
two_path_graph["cycle_rank"] = cycle_rank(**two_path_graph)

unique_observed_representations = {
    (values["SU3"], values["SU2"], str(values["Y"]))
    for values in right_sectors.values()
}

result = {
    "gate": "version4_vectorlike_messenger_chain",
    "normalized_hidden_charge_ledger": hidden_charge,
    "vertex_hidden_charge_sums": vertex_hidden_charge_sums,
    "all_three_chain_vertices_hidden_gauge_invariant": all(value == 0 for value in vertex_hidden_charge_sums.values()),
    "vectorlike_anomaly_cancellation": {
        "continuous_gauge_anomalies": "left and right messenger contributions cancel representation by representation",
        "mixed_gravitational_hidden": "q-q=0",
        "hidden_cubic": "q^3-q^3=0",
        "status": True,
    },
    "single_chain_graph": single_chain_graph,
    "single_chain_physical_phase_count": single_chain_graph["cycle_rank"],
    "two_path_graph": two_path_graph,
    "two_path_physical_phase_count": two_path_graph["cycle_rank"],
    "two_path_phase_invariant": "arg(y_Omega_a y_phi_a y_Omega_b^* y_phi_b^*)",
    "effective_operator": "bar(F_L) H Omega phi_h f_R /(M0 Mq)",
    "effective_operator_dimension": 6,
    "right_sector_representations": {
        name: {key: str(value) for key, value in values.items()}
        for name, values in right_sectors.items()
    },
    "distinct_messenger_representation_types_for_all_dirac_sectors": len(unique_observed_representations),
    "single_sm_representation_covers_all_dirac_sectors": len(unique_observed_representations) == 1,
    "status": "one sector admits an anomaly-safe chain; physical CP needs two paths; the full four-sector graph needs four SM messenger representation types or a new unified multiplet",
}

with open("s2t_v4_vectorlike_messenger_chain_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))