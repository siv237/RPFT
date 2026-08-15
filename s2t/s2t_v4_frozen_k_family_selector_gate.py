import json
from fractions import Fraction


cellular_boundaries_rp3 = {
    "d1": [[0]],
    "d2": [[2]],
    "d3": [[0]],
}

product_chain_ranks = {"C0": 1, "C1": 2, "C2": 2, "C3": 2, "C4": 1}
product_boundary_smith_diagonals = {
    "d1": [],
    "d2": [2],
    "d3": [2],
    "d4": [],
}

homology = {
    "H0": "Z",
    "H1": "Z + Z2",
    "H2": "Z2",
    "H3": "Z",
    "H4": "Z",
}
cohomology = {
    "H^0": "Z",
    "H^1": "Z",
    "H^2": "Z2",
    "H^3": "Z + Z2",
    "H^4": "Z",
}

canonical_counts = {
    "sum_free_betti_numbers": 4,
    "number_of_spin_structures": 4,
    "torsion_flat_character_branches": 2,
    "fundamental_group_minimal_generators": 2,
    "integral_cohomology_torsion_generators": 2,
    "flat_twisted_dirac_zero_modes": 0,
    "euler_characteristic": 0,
}

radius = 1
scalar_curvature = Fraction(6, radius**2)
lichnerowicz_gap = scalar_curvature / 4

result = {
    "gate": "version4_frozen_k_family_selector",
    "space": "RP3 x S1",
    "cellular_boundaries_rp3": cellular_boundaries_rp3,
    "product_chain_ranks": product_chain_ranks,
    "product_boundary_smith_diagonals": product_boundary_smith_diagonals,
    "homology": homology,
    "cohomology": cohomology,
    "fundamental_group": "Z2 x Z",
    "spin_structure_group": "H^1(K;Z2)=Z2 x Z2",
    "flat_u1_character_space": "{+1,-1} x U(1)",
    "unit_radius_scalar_curvature": str(scalar_curvature),
    "lichnerowicz_gap_R_over_4": str(lichnerowicz_gap),
    "canonical_counts": canonical_counts,
    "any_declared_count_equals_three": any(value == 3 for value in canonical_counts.values()),
    "status": "no canonical three-family selector in the declared frozen-K invariant menu",
    "scope": "does not exclude a new family algebra, non-flat bundle, defect, or additional index problem",
}

with open("s2t_v4_frozen_k_family_selector_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))