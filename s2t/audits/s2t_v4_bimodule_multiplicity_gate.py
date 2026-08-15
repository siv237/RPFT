import itertools
import json
from fractions import Fraction


fields = {
    "Q_L": {"dimension": 6, "su3_index": 2, "su2_y": Fraction(1, 2), "grav_y": 1, "cubic_y": Fraction(1, 36)},
    "u_R": {"dimension": 3, "su3_index": -1, "su2_y": 0, "grav_y": -2, "cubic_y": Fraction(-8, 9)},
    "d_R": {"dimension": 3, "su3_index": -1, "su2_y": 0, "grav_y": 1, "cubic_y": Fraction(1, 9)},
    "L_L": {"dimension": 2, "su3_index": 0, "su2_y": Fraction(-1, 2), "grav_y": -1, "cubic_y": Fraction(-1, 4)},
    "e_R": {"dimension": 1, "su3_index": 0, "su2_y": 0, "grav_y": 1, "cubic_y": 1},
    "nu_R": {"dimension": 1, "su3_index": 0, "su2_y": 0, "grav_y": 0, "cubic_y": 0},
}


def ledger(vector):
    multiplicities = dict(zip(fields, vector))
    return {
        "multiplicities": multiplicities,
        "complex_dimension": sum(multiplicities[name] * data["dimension"] for name, data in fields.items()),
        "su3_cubed": sum(multiplicities[name] * data["su3_index"] for name, data in fields.items()),
        "su2_squared_u1": sum(multiplicities[name] * data["su2_y"] for name, data in fields.items()),
        "gravity_squared_u1": sum(multiplicities[name] * data["grav_y"] for name, data in fields.items()),
        "u1_cubed": sum(multiplicities[name] * data["cubic_y"] for name, data in fields.items()),
        "weak_doublets_mod2": (3 * multiplicities["Q_L"] + multiplicities["L_L"]) % 2,
    }


def complete_dirac_yukawa(m):
    return (
        m["u_R"] == m["Q_L"]
        and m["d_R"] == m["Q_L"]
        and m["e_R"] == m["L_L"]
        and m["nu_R"] == m["L_L"]
    )


def complete_charged_yukawa(m):
    return (
        m["u_R"] == m["Q_L"]
        and m["d_R"] == m["Q_L"]
        and m["e_R"] == m["L_L"]
        and m["nu_R"] == 0
    )


def anomaly_free(item):
    return (
        item["su3_cubed"] == 0
        and item["su2_squared_u1"] == 0
        and item["gravity_squared_u1"] == 0
        and item["u1_cubed"] == 0
        and item["weak_doublets_mod2"] == 0
    )


all_ledgers = [ledger(vector) for vector in itertools.product(range(5), repeat=6)]

dirac_solutions = [
    item
    for item in all_ledgers
    if item["multiplicities"]["Q_L"] > 0
    and item["multiplicities"]["L_L"] > 0
    and complete_dirac_yukawa(item["multiplicities"])
    and anomaly_free(item)
]
charged_solutions = [
    item
    for item in all_ledgers
    if item["multiplicities"]["Q_L"] > 0
    and item["multiplicities"]["L_L"] > 0
    and complete_charged_yukawa(item["multiplicities"])
    and anomaly_free(item)
]

minimum_dirac_dimension = min(item["complex_dimension"] for item in dirac_solutions)
minimum_charged_dimension = min(item["complex_dimension"] for item in charged_solutions)
minimal_dirac = [item for item in dirac_solutions if item["complex_dimension"] == minimum_dirac_dimension]
minimal_charged = [item for item in charged_solutions if item["complex_dimension"] == minimum_charged_dimension]


def serialize(item):
    return {
        **item,
        "su2_squared_u1": str(item["su2_squared_u1"]),
        "u1_cubed": str(item["u1_cubed"]),
    }


result = {
    "gate": "version4_bimodule_multiplicity",
    "search_range_per_multiplicity": [0, 4],
    "tested_vectors": len(all_ledgers),
    "dirac_neutrino_branch": {
        "solution_count_in_range": len(dirac_solutions),
        "minimal_dimension": minimum_dirac_dimension,
        "minimal_solutions": [serialize(item) for item in minimal_dirac],
        "solution_vectors": [item["multiplicities"] for item in dirac_solutions],
    },
    "no_right_neutrino_branch": {
        "solution_count_in_range": len(charged_solutions),
        "minimal_dimension": minimum_charged_dimension,
        "minimal_solutions": [serialize(item) for item in minimal_charged],
        "solution_vectors": [item["multiplicities"] for item in charged_solutions],
    },
    "structural_result": "all nonzero solutions are generation copies with a common multiplicity g",
    "generation_count_status": "unfixed positive integer",
}

with open("s2t_v4_bimodule_multiplicity_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))