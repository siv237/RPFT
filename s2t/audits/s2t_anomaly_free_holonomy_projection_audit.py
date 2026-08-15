import json
from pathlib import Path

import numpy as np


I = 1j
TOLERANCE = 1.0e-12


def quarter_phase(six_hypercharge):
    return I ** (six_hypercharge % 4)


def phase_label(value):
    labels = {
        (1.0, 0.0): "+1",
        (-1.0, 0.0): "-1",
        (0.0, 1.0): "+i",
        (0.0, -1.0): "-i",
    }
    key = (round(value.real, 12), round(value.imag, 12))
    return labels.get(key, str(value))


h_fundamental = np.diag([-1.0, -1.0, -1.0, -I, -I]).astype(complex)
p5_fundamental = np.linalg.matrix_power(h_fundamental, 2)

components = [
    {
        "parent": "10+10bar",
        "name": "U",
        "six_Y": -4,
        "P5": +1,
        "flat_twist": +1,
        "copies": 1,
        "kind": "vectorlike_Dirac",
        "beta": [16.0 / 9.0, 0.0, 2.0 / 3.0],
    },
    {
        "parent": "10+10bar",
        "name": "Q",
        "six_Y": +1,
        "P5": -1,
        "flat_twist": +1,
        "copies": 1,
        "kind": "vectorlike_Dirac",
        "beta": [2.0 / 9.0, 2.0, 4.0 / 3.0],
    },
    {
        "parent": "10+10bar",
        "name": "E",
        "six_Y": +6,
        "P5": +1,
        "flat_twist": +1,
        "copies": 1,
        "kind": "vectorlike_Dirac",
        "beta": [4.0 / 3.0, 0.0, 0.0],
    },
    {
        "parent": "2 x (5+5bar)",
        "name": "D",
        "six_Y": +2,
        "P5": +1,
        "flat_twist": -1,
        "copies": 2,
        "kind": "vectorlike_Dirac",
        "beta": [4.0 / 9.0, 0.0, 2.0 / 3.0],
    },
    {
        "parent": "2 x (5+5bar)",
        "name": "L",
        "six_Y": -3,
        "P5": -1,
        "flat_twist": -1,
        "copies": 2,
        "kind": "vectorlike_Dirac",
        "beta": [2.0 / 3.0, 2.0 / 3.0, 0.0],
    },
    {
        "parent": "5_H",
        "name": "H",
        "six_Y": +3,
        "P5": -1,
        "flat_twist": -I,
        "copies": 1,
        "kind": "complex_scalar",
        "beta": [1.0 / 6.0, 1.0 / 6.0, 0.0],
    },
    {
        "parent": "5_H",
        "name": "T_H",
        "six_Y": -2,
        "P5": +1,
        "flat_twist": -I,
        "copies": 1,
        "kind": "complex_scalar",
        "beta": [1.0 / 9.0, 0.0, 1.0 / 6.0],
    },
]

phase_table = []
surviving_beta = np.zeros(3)
survivors = []
projected = []
for component in components:
    z4_phase = quarter_phase(component["six_Y"])
    total_phase = component["P5"] * z4_phase * component["flat_twist"]
    survives = abs(total_phase - 1.0) < TOLERANCE
    if survives:
        survivors.extend([component["name"]] * component["copies"])
        surviving_beta += component["copies"] * np.array(component["beta"])
    else:
        projected.extend([component["name"]] * component["copies"])
    phase_table.append(
        {
            **component,
            "flat_twist": phase_label(complex(component["flat_twist"])),
            "Z4_hypercharge_phase": phase_label(z4_phase),
            "total_phase": phase_label(total_phase),
            "periodic_zero_mode": survives,
        }
    )

su5_parent_anomaly_terms = {
    "10": +1,
    "10bar": -1,
    "two_5": +2,
    "two_5bar": -2,
}
su5_parent_anomaly = sum(su5_parent_anomaly_terms.values())
target_beta = np.array([17.0 / 6.0, 1.0 / 6.0, 2.0])

removed_phase_determinants = {
    row["name"]: {
        "phase": row["total_phase"],
        "circle_shift_beta": {
            "+i": 0.25,
            "-1": 0.5,
            "-i": 0.75,
        }.get(row["total_phase"]),
    }
    for row in phase_table
    if not row["periodic_zero_mode"]
}

results = {
    "status": "anomaly_free_SU5_parent_Z2_Z4_projection_yields_U_2D_H_zero_sector_tower_sum_open",
    "date": "2026-08-04",
    "parent": {
        "fermions": "(10+10bar) + 2 x (5+5bar)",
        "scalar": "5_H",
        "reason": "vectorlike conjugate pairs cancel parent and low-energy chiral gauge anomalies",
        "SU5_cubic_anomaly_terms": su5_parent_anomaly_terms,
        "SU5_cubic_anomaly_sum": su5_parent_anomaly,
    },
    "holonomies": {
        "Z4_element": "h=exp(i 3 pi Y)=diag(-1,-1,-1,-i,-i) in the SU5 fundamental",
        "Z2_element": "P5=h^2=diag(+1,+1,+1,-1,-1)",
        "det_h": [
            float(np.linalg.det(h_fundamental).real),
            float(np.linalg.det(h_fundamental).imag),
        ],
        "h_fourth_power_identity_error": float(
            np.max(np.abs(np.linalg.matrix_power(h_fundamental, 4) - np.eye(5)))
        ),
        "P5_equals_h_squared_error": float(
            np.max(
                np.abs(
                    p5_fundamental - np.diag([1, 1, 1, -1, -1])
                )
            )
        ),
        "multiplet_flat_characters": {
            "10+10bar": "+1",
            "5+5bar_D_copies": "-1",
            "5_H": "-i with conjugate +i",
        },
        "geometric_interpretation": (
            "P5 is assigned to the RP3 Z2 cycle, h to the quarter S1 branch, and the remaining factors are existing flat-line characters"
        ),
    },
    "phase_table": phase_table,
    "zero_mode_content": {
        "survivors_with_copies": survivors,
        "projected_with_copies": projected,
        "surviving_content": "one vectorlike U, two vectorlike D, one complex H doublet",
        "beta_vector_Y_2_3": surviving_beta.tolist(),
        "target_beta_vector_Y_2_3": target_beta.tolist(),
        "beta_vector_error": float(np.max(np.abs(surviving_beta - target_beta))),
    },
    "anomaly_gate": {
        "parent_SU5_anomaly": su5_parent_anomaly,
        "low_energy_fermions": "vectorlike U and D pairs",
        "low_energy_gauge_anomalies": "zero pairwise",
        "scalar_H_anomaly": "none",
        "status": "passed_for_the_constructed_parent_content",
    },
    "first_tower_data": {
        "projected_component_circle_shifts": removed_phase_determinants,
        "interpretation": (
            "Q and L occupy quarter-shifted branches, E a half-shifted branch, and the color triplet a quarter-shifted branch"
        ),
        "remaining_gate": (
            "compute the regulated RP3 x S1 KK determinant difference between the surviving periodic branches and these fixed shifted partners"
        ),
    },
    "caveats": [
        "The different flat characters must be derived from S2T sector attribution rather than declared ad hoc.",
        "The construction closes representation content and anomaly consistency, not threshold magnitude.",
        "Localized anomalies require a separate check if the projection is realized by boundaries rather than smooth flat bundles.",
    ],
    "verdict": (
        "An anomaly-free parent realization of the inverse U+2D+H hint exists. The combined RP3 Z2 parity, quarter hypercharge holonomy and conjugate flat characters retain exactly the desired vectorlike zero sector while projecting Q, L, E and the colored Higgs triplet. This upgrades the split ray from a bare representation guess to a consistent projection candidate. It is not yet a successful gauge prediction: the multiplet character assignment and the finite KK determinant sum remain to be derived."
    ),
}

assert abs(np.linalg.det(h_fundamental) - 1.0) < TOLERANCE
assert results["holonomies"]["h_fourth_power_identity_error"] < TOLERANCE
assert results["holonomies"]["P5_equals_h_squared_error"] < TOLERANCE
assert survivors == ["U", "D", "D", "H"]
assert su5_parent_anomaly == 0
assert results["zero_mode_content"]["beta_vector_error"] < TOLERANCE

Path("s2t_anomaly_free_holonomy_projection_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "survivors": survivors,
            "projected": projected,
            "parent_anomaly": su5_parent_anomaly,
            "beta_vector": surviving_beta.tolist(),
            "next_gate": results["first_tower_data"]["remaining_gate"],
        },
        indent=2,
        ensure_ascii=False,
    )
)