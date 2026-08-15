import itertools
import json


blocks = {
    "C": (2, (), 1, False, False),
    "H": (4, ("su2",), 0, True, False),
    "M2C": (8, ("su2",), 1, False, False),
    "M3C": (18, ("su3",), 1, False, True),
    "M3R": (9, ("so3",), 0, False, False),
}


def summarize(candidate):
    real_dimension = sum(blocks[name][0] for name in candidate)
    factors = sorted(factor for name in candidate for factor in blocks[name][1])
    center_rank = sum(blocks[name][2] for name in candidate)
    return {
        "blocks": list(candidate),
        "real_dimension": real_dimension,
        "simple_lie_factors": factors,
        "central_u1_rank_before_unimodularity": center_rank,
        "central_u1_rank_after_one_constraint": max(center_rank - 1, 0),
        "has_quaternionic_weak_block": any(blocks[name][3] for name in candidate),
        "has_complex_color_block": any(blocks[name][4] for name in candidate),
    }


candidates = []
for size in range(1, 4):
    for candidate in itertools.combinations(blocks, size):
        item = summarize(candidate)
        item["passes_lie_target"] = "su2" in item["simple_lie_factors"] and "su3" in item["simple_lie_factors"]
        item["passes_one_surviving_u1"] = item["central_u1_rank_after_one_constraint"] >= 1
        item["passes_quaternionic_branch"] = (
            item["passes_lie_target"]
            and item["passes_one_surviving_u1"]
            and item["has_quaternionic_weak_block"]
            and item["has_complex_color_block"]
        )
        candidates.append(item)

lie_and_center = [item for item in candidates if item["passes_lie_target"] and item["passes_one_surviving_u1"]]
quaternionic = [item for item in candidates if item["passes_quaternionic_branch"]]
minimum_dimension = min(item["real_dimension"] for item in quaternionic)
minimal_quaternionic = [item for item in quaternionic if item["real_dimension"] == minimum_dimension]

bimodule_target = {
    "Q_L": ("H", "M3C", 6),
    "L_L": ("H", "C", 2),
    "u_R": ("C", "M3C", 3),
    "d_R": ("conjugate-C", "M3C", 3),
    "nu_R": ("C", "C", 1),
    "e_R": ("conjugate-C", "C", 1),
}

result = {
    "gate": "version4_finite_algebra_menu",
    "all_lie_and_center_candidates": lie_and_center,
    "minimal_quaternionic_candidates": minimal_quaternionic,
    "selected_baseline": ["C", "H", "M3C"],
    "unitary_lie_algebra_before_unimodularity": "u1 + su2 + su3 + u1",
    "unitary_lie_algebra_after_one_nontrivial_central_constraint": "su3 + su2 + u1",
    "bimodule_target": {
        name: {"left": values[0], "right": values[1], "complex_dimension": values[2]}
        for name, values in bimodule_target.items()
    },
    "one_generation_complex_dimension_without_antiparticles": sum(values[2] for values in bimodule_target.values()),
    "uniqueness_status": "unique minimum only inside the quaternionic weak-block branch and declared menu",
}

with open("s2t_v4_finite_algebra_menu_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))