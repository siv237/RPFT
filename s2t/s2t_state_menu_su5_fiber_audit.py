import json
import math
from pathlib import Path

import numpy as np


def main():
    # Minimal-rank requirement: rank(SU3 x SU2 x U1)=4.
    rank_four_simple_groups = {
        "SU(5) / A4": 24,
        "SO(8) / D4": 28,
        "SO(9) / B4": 36,
        "Sp(8) / C4": 36,
        "F4": 52,
    }
    minimal_group = min(rank_four_simple_groups, key=rank_four_simple_groups.get)

    # Order-two SU(5) holonomy supplied by the Z2 torsion branch.
    parity = np.array([1, 1, 1, -1, -1], dtype=int)
    holonomy = np.diag(parity).astype(complex)
    holonomy_order_two_error = float(np.linalg.norm(holonomy @ holonomy - np.eye(5)))
    holonomy_determinant = complex(np.linalg.det(holonomy))

    # Complexified sl(5) basis count commuting with P.
    commuting_off_diagonal = 0
    broken_off_diagonal = 0
    for row in range(5):
        for column in range(5):
            if row == column:
                continue
            if parity[row] == parity[column]:
                commuting_off_diagonal += 1
            else:
                broken_off_diagonal += 1
    commuting_diagonal_traceless = 4
    centralizer_dimension = commuting_off_diagonal + commuting_diagonal_traceless
    broken_dimension = broken_off_diagonal

    # Hypercharge generator and one-generation SU(5) branching.
    hypercharge_fundamental = [-1.0 / 3.0] * 3 + [1.0 / 2.0] * 2
    hypercharge_trace = sum(hypercharge_fundamental)

    ten_states = []
    for first in range(5):
        for second in range(first + 1, 5):
            sectors = (
                "color" if first < 3 else "weak",
                "color" if second < 3 else "weak",
            )
            if sectors == ("color", "color"):
                label = "u_c: (bar3,1)"
            elif sectors == ("weak", "weak"):
                label = "e_c: (1,1)"
            else:
                label = "Q: (3,2)"
            ten_states.append(
                {
                    "label": label,
                    "Y": hypercharge_fundamental[first]
                    + hypercharge_fundamental[second],
                    "Z2_parity": int(parity[first] * parity[second]),
                }
            )

    five_bar_states = []
    for index in range(5):
        if index < 3:
            label = "d_c: (bar3,1)"
        else:
            label = "L: (1,2)"
        five_bar_states.append(
            {
                "label": label,
                "Y": -hypercharge_fundamental[index],
                "Z2_parity": int(parity[index]),
            }
        )

    def multiplicity(rows, label):
        return sum(row["label"] == label for row in rows)

    branching = {
        "10": {
            "Q_(3,2)_1/6": multiplicity(ten_states, "Q: (3,2)"),
            "u_c_(bar3,1)_-2/3": multiplicity(ten_states, "u_c: (bar3,1)"),
            "e_c_(1,1)_1": multiplicity(ten_states, "e_c: (1,1)"),
        },
        "bar5": {
            "d_c_(bar3,1)_1/3": multiplicity(
                five_bar_states, "d_c: (bar3,1)"
            ),
            "L_(1,2)_-1/2": multiplicity(five_bar_states, "L: (1,2)"),
        },
    }

    all_states = ten_states + five_bar_states
    weak_doublet_parities = {
        row["Z2_parity"]
        for row in all_states
        if row["label"] in {"Q: (3,2)", "L: (1,2)"}
    }
    weak_singlet_parities = {
        row["Z2_parity"]
        for row in all_states
        if row["label"] not in {"Q: (3,2)", "L: (1,2)"}
    }

    # Standard anomaly checks for one SM generation in left-handed notation.
    su5_cubic_anomaly_10 = 5 - 4
    su5_cubic_anomaly_bar5 = -1
    su5_total_anomaly = su5_cubic_anomaly_10 + su5_cubic_anomaly_bar5

    gravitational_u1 = sum(row["Y"] for row in all_states)
    u1_cubic = sum(row["Y"] ** 3 for row in all_states)
    su3_squared_u1 = (
        2.0 * 0.5 * (1.0 / 6.0)
        + 0.5 * (-2.0 / 3.0)
        + 0.5 * (1.0 / 3.0)
    )
    su2_squared_u1 = 3.0 * 0.5 * (1.0 / 6.0) + 0.5 * (-1.0 / 2.0)

    # Tempting generation count: four spin structures minus one reference sector.
    spin_structure_count = 4
    nonreference_count = spin_structure_count - 1

    gates = {
        "single_simple_fiber": {
            "passes": True,
            "finding": (
                "SU(5) is the smallest-dimensional compact simple rank-four group in the "
                "standard Lie-family census and can contain the full SM-rank subgroup."
            ),
        },
        "z2_breaking_to_sm": {
            "passes": True,
            "finding": (
                "P=diag(1,1,1,-1,-1) is an order-two SU(5) element with centralizer "
                "S(U3 x U2)=(SU3 x SU2 x U1)/Z6."
            ),
        },
        "one_generation_branching": {
            "passes": True,
            "finding": (
                "The anomaly-free chiral package 10 + bar5 branches into exactly Q, u_c, "
                "e_c, d_c and L with standard hypercharges."
            ),
        },
        "weak_doublet_parity_selector": {
            "passes": True,
            "finding": (
                "The same torsion holonomy makes Q and L odd while every weak singlet is even."
            ),
        },
        "three_generations": {
            "passes": False,
            "finding": (
                "Four spin structures minus one chosen reference gives three, but spin structures "
                "form a torsor with no canonical zero. Selecting the excluded sector requires an "
                "independent geometric or dynamical rule."
            ),
        },
        "masses_and_yukawa": {
            "passes": False,
            "finding": (
                "The construction fixes representation content and parity, not Yukawa matrices, "
                "symmetry-breaking scales or observed masses."
            ),
        },
    }

    results = {
        "status": "minimal_SU5_fiber_passes_SM_group_and_one_generation_gate_generation_count_and_masses_open",
        "date": "2026-08-04",
        "input_menu": {
            "base": "two-circle flat-character menu over K=RP3 x S1",
            "torsion_generator": "Z2",
            "fiber_requirement": "one compact connected simple group containing SM rank four",
        },
        "minimality": {
            "SM_rank": 4,
            "rank_four_simple_group_dimensions": rank_four_simple_groups,
            "minimal_group": minimal_group,
            "interpretation": (
                "Rank below four cannot contain SU3 x SU2 x U1. In the rank-four census, "
                "SU(5) has the smallest Lie-algebra dimension."
            ),
        },
        "z2_holonomy": {
            "P": "diag(1,1,1,-1,-1)",
            "determinant": [holonomy_determinant.real, holonomy_determinant.imag],
            "order_two_error": holonomy_order_two_error,
            "centralizer": "S(U3 x U2)=(SU3 x SU2 x U1)/Z6",
            "centralizer_dimension": centralizer_dimension,
            "unbroken_dimension_check": "8+3+1=12",
            "broken_dimension": broken_dimension,
            "SU5_dimension": 24,
        },
        "hypercharge": {
            "Y_fundamental": hypercharge_fundamental,
            "trace": hypercharge_trace,
        },
        "one_generation": {
            "representation": "10 + bar5",
            "branching_multiplicities": branching,
            "weak_doublet_parities": sorted(weak_doublet_parities),
            "weak_singlet_parities": sorted(weak_singlet_parities),
            "interpretation": (
                "All weak doublet states are Z2-odd and all weak singlets are Z2-even under P."
            ),
        },
        "anomaly_checks": {
            "SU5_cubic_A10": su5_cubic_anomaly_10,
            "SU5_cubic_Abar5": su5_cubic_anomaly_bar5,
            "SU5_total": su5_total_anomaly,
            "gravitational_U1": gravitational_u1,
            "U1_cubic": u1_cubic,
            "SU3_squared_U1": su3_squared_u1,
            "SU2_squared_U1": su2_squared_u1,
        },
        "generation_temptation": {
            "spin_structure_count": spin_structure_count,
            "nonreference_count": nonreference_count,
            "status": "numerically_tempting_but_not_canonical",
            "obstruction": (
                "The set of spin structures is affine; no reference element is preferred without "
                "extra data. The equation 4-1=3 is therefore not yet a derivation."
            ),
        },
        "gates": gates,
        "scientific_verdict": {
            "new_positive_result": (
                "A single minimal SU(5) fiber plus the existing Z2 torsion branch produces the "
                "SM gauge subgroup, one anomaly-free chiral generation, and a clean weak-doublet "
                "parity split without separate SU3/SU2 sector choices."
            ),
            "remaining_gaps": (
                "The choice 10+bar5 is not yet derived from the menu, three generations are not "
                "canonically selected, and no masses or Yukawa couplings follow."
            ),
            "next_gate": (
                "Search for a geometric invariant of the four spin structures that uniquely "
                "selects one reference sector and leaves three equivalent nonreference sectors, "
                "without using the observed generation count."
            ),
        },
    }

    assert minimal_group == "SU(5) / A4"
    assert holonomy_order_two_error < 1e-14
    assert abs(holonomy_determinant - 1.0) < 1e-14
    assert centralizer_dimension == 12
    assert broken_dimension == 12
    assert branching["10"] == {
        "Q_(3,2)_1/6": 6,
        "u_c_(bar3,1)_-2/3": 3,
        "e_c_(1,1)_1": 1,
    }
    assert branching["bar5"] == {
        "d_c_(bar3,1)_1/3": 3,
        "L_(1,2)_-1/2": 2,
    }
    assert weak_doublet_parities == {-1}
    assert weak_singlet_parities == {1}
    assert abs(su5_total_anomaly) < 1e-14
    assert abs(gravitational_u1) < 1e-14
    assert abs(u1_cubic) < 1e-14
    assert abs(su3_squared_u1) < 1e-14
    assert abs(su2_squared_u1) < 1e-14

    Path("s2t_state_menu_su5_fiber_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "minimal_group": minimal_group,
                "centralizer_dimension": centralizer_dimension,
                "branching": branching,
                "anomalies": results["anomaly_checks"],
                "doublet_parity": sorted(weak_doublet_parities),
                "singlet_parity": sorted(weak_singlet_parities),
                "three_generation_status": results["generation_temptation"]["status"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()