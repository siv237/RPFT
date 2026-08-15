import itertools
import json
import math

import numpy as np


def permutation_matrix(permutation):
    size = len(permutation)
    matrix = np.zeros((size, size))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def standard_triplet_basis():
    seed = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [-1.0, -1.0, -1.0],
        ]
    )
    basis, _ = np.linalg.qr(seed)
    return basis[:, :3]


def cycle_type(permutation):
    visited = [False] * len(permutation)
    lengths = []
    for start in range(len(permutation)):
        if visited[start]:
            continue
        current = start
        length = 0
        while not visited[current]:
            visited[current] = True
            current = permutation[current]
            length += 1
        lengths.append(length)
    return "+".join(str(length) for length in sorted(lengths, reverse=True))


def canonical_axis(rotation):
    values, vectors = np.linalg.eig(rotation)
    index = int(np.argmin(np.abs(values - 1.0)))
    axis = np.real(vectors[:, index])
    axis /= np.linalg.norm(axis)
    first_nonzero = np.flatnonzero(np.abs(axis) > 1.0e-10)
    if first_nonzero.size and axis[first_nonzero[0]] < 0:
        axis = -axis
    return axis


def unique_axes(axes):
    result = []
    for axis in axes:
        if not any(abs(np.dot(axis, existing)) > 1.0 - 1.0e-9 for existing in result):
            result.append(axis)
    return result


basis = standard_triplet_basis()
three_cycle_rows = []
three_cycle_axes = []
orientation_ledger = {}
for permutation in itertools.permutations(range(4)):
    kind = cycle_type(permutation)
    full = permutation_matrix(permutation)
    restricted = basis.T @ full @ basis
    determinant = round(float(np.linalg.det(restricted)))
    orientation_ledger.setdefault(kind, {"count": 0, "determinants": set()})
    orientation_ledger[kind]["count"] += 1
    orientation_ledger[kind]["determinants"].add(determinant)
    if kind == "3+1":
        axis = canonical_axis(restricted)
        three_cycle_axes.append(axis)
        three_cycle_rows.append(
            {
                "permutation": list(permutation),
                "determinant": determinant,
                "axis": axis.tolist(),
            }
        )

axes = unique_axes(three_cycle_axes)
with open(
    "s2t_family_wilson_majorana_core_selector_results.json",
    encoding="utf-8",
) as source:
    wilson = json.load(source)

wilson_axes = [np.asarray(row["axis"], dtype=float) for row in wilson["rows"]]
alignment_rows = []
for wilson_index, wilson_axis in enumerate(wilson_axes):
    dots = [abs(float(np.dot(wilson_axis, axis))) for axis in axes]
    best_index = int(np.argmax(dots))
    alignment_rows.append(
        {
            "wilson_axis_index": wilson_index,
            "nearest_three_cycle_axis_index": best_index,
            "absolute_dot": dots[best_index],
            "misalignment_angle": math.acos(min(1.0, dots[best_index])),
            "exact_alignment": dots[best_index] > 1.0 - 1.0e-9,
        }
    )

theta_star = float(wilson["input"]["wilson_angle"])
three_cycle_angle = 2.0 * math.pi / 3.0

result = {
    "gate": "version4_old_problem_rotation_audit",
    "orientation_filter": {
        kind: {
            "count": entry["count"],
            "restricted_triplet_determinants": sorted(entry["determinants"]),
        }
        for kind, entry in sorted(orientation_ledger.items())
    },
    "family_defect_cross_clue": {
        "outside_D8_full_M3_candidates": 12,
        "continuous_SO3_compatible_candidates": 8,
        "compatible_cycle_type": "3+1",
        "unique_unoriented_three_cycle_axes": len(axes),
        "three_cycle_axes": [axis.tolist() for axis in axes],
        "wilson_axis_alignment": alignment_rows,
        "wilson_angle": theta_star,
        "three_cycle_angle": three_cycle_angle,
        "angle_difference": abs(theta_star - three_cycle_angle),
        "verdict": (
            "The SO(3) requirement removes transposition candidates and leaves "
            "the eight three-cycles, but neither selected Wilson axis is exactly "
            "a tetrahedral three-cycle axis and theta_star is not 2pi/3. The "
            "Wilson-defect bridge narrows the family selector but does not derive "
            "a discrete affine incidence operator."
        ),
    },
    "problem_ledger": [
        {
            "branch": "family_defect_boundary_superconnection",
            "readiness": 4,
            "independent_blockers_addressed": 2,
            "known_positive": [
                "exact-one tubular BdG kernel",
                "rank-two SO3 core generator",
                "twelve affine full-M3 candidates narrowed to eight three-cycles",
            ],
            "blocking_input": (
                "derive root sector, condensate and family-axis holonomy from one "
                "boundary action"
            ),
            "priority": 1,
        },
        {
            "branch": "full_field_carrier_comparison",
            "readiness": 2,
            "independent_blockers_addressed": 1,
            "known_positive": [
                "field multiplicity ledger",
                "fixed-volume curvature invariant difference",
            ],
            "blocking_input": (
                "parent derivation of Newton, Weyl-squared, Euler, nonminimal "
                "scalar and vector-mass data"
            ),
            "priority": 2,
        },
        {
            "branch": "standalone_affine_family_selector",
            "readiness": 2,
            "independent_blockers_addressed": 1,
            "known_positive": [
                "canonical S4 triplet",
                "full M3 exists for twelve outside-D8 incidences",
            ],
            "blocking_input": (
                "no intrinsic selector, sector assignment or relative weight"
            ),
            "priority": 3,
        },
    ],
    "recommended_next_gate": (
        "construct the minimal boundary superconnection whose holonomy acts on "
        "the family triplet and the sterile root line simultaneously; test "
        "whether its equations select a three-cycle axis and a condensed "
        "charge-two vortex without target-dependent coefficients"
    ),
}

with open(
    "s2t_v4_old_problem_rotation_audit_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))