import itertools
import json

import numpy as np


corner_dimensions = {
    "rho_rho": 1,
    "rho_Q": 2,
    "Q_rho": 2,
    "Q_Q": 4,
}


def star_closed(corners):
    return ("rho_Q" in corners) == ("Q_rho" in corners)


rows = []
corner_names = tuple(corner_dimensions)
for mask in itertools.product((False, True), repeat=len(corner_names)):
    corners = {
        name for name, included in zip(corner_names, mask) if included
    }
    rows.append(
        {
            "corners": sorted(corners),
            "dimension": sum(corner_dimensions[name] for name in corners),
            "star_closed": star_closed(corners),
            "contains_anchor_self_edge": "rho_rho" in corners,
            "connects_anchor_to_complement": (
                "rho_Q" in corners and "Q_rho" in corners
            ),
            "excludes_complement_internal_edge": "Q_Q" not in corners,
        }
    )

admissible = [
    row
    for row in rows
    if row["star_closed"]
    and row["contains_anchor_self_edge"]
    and row["connects_anchor_to_complement"]
    and row["excludes_complement_internal_edge"]
]

rho = np.diag([1.0, 0.0, 0.0])
complement = np.eye(3) - rho


def projection(matrix):
    return matrix - complement @ matrix @ complement


matrix_units = []
allowed_support = []
for row in range(3):
    for column in range(3):
        matrix = np.zeros((3, 3))
        matrix[row, column] = 1
        matrix_units.append(matrix)
        if row == 0 or column == 0:
            allowed_support.append(matrix)

projection_span = np.column_stack(
    [projection(matrix).reshape(-1) for matrix in matrix_units]
)
star_span = np.column_stack(
    [matrix.reshape(-1) for matrix in allowed_support]
)
same_span = bool(
    np.linalg.matrix_rank(
        np.column_stack([projection_span, star_span]), tol=1e-12
    )
    == np.linalg.matrix_rank(projection_span, tol=1e-12)
    == np.linalg.matrix_rank(star_span, tol=1e-12)
)

rng = np.random.default_rng(20260811)
test_matrix = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
inclusion_exclusion_error = np.linalg.norm(
    projection(test_matrix)
    - (
        rho @ test_matrix
        + test_matrix @ rho
        - rho @ test_matrix @ rho
    )
)

sector_assignments = {
    "u": "up_type_tilde_H",
    "nu": "up_type_tilde_H",
    "d": "down_type_H",
    "e": "down_type_H",
}
distinct_family_textures = len(set(sector_assignments.values()))

base_operator = np.array(
    [
        [13.5, -2.0, 1.5],
        [-2.0, 17.5, -2.5],
        [1.5, -2.5, 17.0],
    ]
)
base_ground = np.linalg.eigh(base_operator)[1][:, 0]
weighted_ground_errors = {}
for sector, multiplicity in {"quark": 3.0, "lepton": 1.0}.items():
    ground = np.linalg.eigh(multiplicity * base_operator)[1][:, 0]
    weighted_ground_errors[sector] = float(
        min(
            np.linalg.norm(ground - base_ground),
            np.linalg.norm(ground + base_ground),
        )
    )

result = {
    "gate": "version4_relative_krajewski_star",
    "corner_decomposition": corner_dimensions,
    "star_closed_bimodule_count": sum(row["star_closed"] for row in rows),
    "minimality_requirements": [
        "contains rho M rho",
        "contains rho M Q and Q M rho",
        "excludes Q M Q",
    ],
    "admissible_module_count": len(admissible),
    "unique_admissible_module": admissible[0] if len(admissible) == 1 else None,
    "relative_star_support": "matrix entries with row=anchor or column=anchor",
    "relative_star_dimension": len(allowed_support),
    "relative_star_equals_M_rho": same_span,
    "projection_is_endpoint_inclusion_exclusion": bool(
        inclusion_exclusion_error < 1e-12
    ),
    "inclusion_exclusion_error": float(inclusion_exclusion_error),
    "sector_assignments": sector_assignments,
    "distinct_family_texture_count": distinct_family_textures,
    "color_lepton_multiplicity_ground_state_errors": weighted_ground_errors,
    "positive_multiplicity_changes_state": False,
    "support_axiom_derived_conditionally": bool(
        len(admissible) == 1 and same_span
    ),
    "four_sector_map_derived": False,
    "status": (
        "the support module is the unique minimal relative Krajewski star, "
        "but factorized gauge labels produce only two family textures for "
        "the four Yukawa sectors"
    ),
}

assert result["admissible_module_count"] == 1
assert result["unique_admissible_module"]["dimension"] == 5
assert result["relative_star_equals_M_rho"]
assert result["projection_is_endpoint_inclusion_exclusion"]
assert result["distinct_family_texture_count"] == 2
assert max(weighted_ground_errors.values()) < 1e-12

with open(
    "s2t_v4_relative_krajewski_star_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))