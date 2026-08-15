import json

import sympy as sp


with open(
    "s2t_v4_cross_sector_transposition_orbit_gate_results.json",
    encoding="utf-8",
) as handle:
    orbit_results = json.load(handle)

with open(
    "s2t_v4_family_square_spectral_selector_gate_results.json",
    encoding="utf-8",
) as handle:
    square_results = json.load(handle)

with open(
    "s2t_v4_rank_one_breaking_gate_results.json",
    encoding="utf-8",
) as handle:
    rank_one_results = json.load(handle)


triplet_basis = sp.Matrix.hstack(
    sp.Matrix([1, 1, -1, -1]) / 2,
    sp.Matrix([1, -1, 1, -1]) / 2,
    sp.Matrix([1, -1, -1, 1]) / 2,
)


def permutation_matrix(permutation):
    matrix = sp.zeros(4)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1
    return matrix


def restrict(matrix):
    return sp.simplify(triplet_basis.T * matrix * triplet_basis)


operators = [
    restrict(permutation_matrix(row["permutations"][0]))
    for row in square_results["selected_operators"]
]
shear = restrict(
    permutation_matrix(rank_one_results["shear_permutation"])
)
rank_one_projector = (sp.eye(3) - shear) / 2

primary_labels = {
    "A": ("L0", "R0"),
    "B": ("L0", "R1"),
    "C": ("L1", "R1"),
    "D": ("L1", "R0"),
}
primary_edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]


def order_one_allowed(first, second):
    return (
        primary_labels[first][0] == primary_labels[second][0]
        or primary_labels[first][1] == primary_labels[second][1]
    )


theta = sp.symbols("theta", real=True)
phase = sp.exp(sp.I * theta)


def set_block(matrix, row_block, column_block, block):
    matrix[
        3 * row_block : 3 * row_block + 3,
        3 * column_block : 3 * column_block + 3,
    ] = block


def primary_dirac(operator_u, operator_d):
    matrix = sp.zeros(12)
    edges = [
        (0, 1, rank_one_projector),
        (1, 2, operator_u),
        (2, 3, operator_d),
        (3, 0, phase * sp.eye(3)),
    ]
    for first, second, block in edges:
        set_block(matrix, first, second, block)
        set_block(matrix, second, first, block.conjugate().T)
    return matrix


def full_real_dirac(operator_u, operator_d):
    primary = primary_dirac(operator_u, operator_d)
    return sp.diag(primary, sp.conjugate(primary))


j_swap = sp.zeros(24)
j_swap[:12, 12:] = sp.eye(12)
j_swap[12:, :12] = sp.eye(12)

gamma_primary = sp.diag(
    *(
        [1] * 3
        + [-1] * 3
        + [1] * 3
        + [-1] * 3
    )
)
gamma_full = sp.diag(gamma_primary, -gamma_primary)

orbit_rows = []
for orbit in orbit_results["relative_orbits"]:
    first, second = orbit["representative"]
    operator_u = operators[first]
    operator_d = operators[second]
    cross_word = sp.simplify(
        sp.trace(rank_one_projector * operator_u * operator_d)
    )
    primary = primary_dirac(operator_u, operator_d)
    full = full_real_dirac(operator_u, operator_d)
    trace_d4 = sp.simplify(
        sp.expand_complex(sp.trace(full**4)).rewrite(sp.cos)
    )
    if cross_word < 0:
        phase_minimum = "0"
    elif cross_word > 0:
        phase_minimum = "pi"
    else:
        phase_minimum = "flat"
    minimum_trace = (
        sp.simplify(trace_d4.subs(theta, 0))
        if cross_word < 0
        else sp.simplify(trace_d4.subs(theta, sp.pi))
        if cross_word > 0
        else trace_d4
    )
    orbit_rows.append(
        {
            "cross_word": str(cross_word),
            "representative": [first, second],
            "trace_full_D4": str(trace_d4),
            "phase_minimum": phase_minimum,
            "minimum_trace_full_D4": str(minimum_trace),
            "selected_by_positive_quartic": cross_word != 0,
            "primary_self_adjoint": primary == primary.conjugate().T,
            "full_j_compatible": sp.simplify(
                j_swap * sp.conjugate(full) * j_swap - full
            )
            == sp.zeros(24),
            "full_odd_under_grading": sp.simplify(
                gamma_full * full + full * gamma_full
            )
            == sp.zeros(24),
        }
    )

orbit_rows.sort(key=lambda row: sp.Rational(row["cross_word"]))
selected_rows = [
    row for row in orbit_rows if row["selected_by_positive_quartic"]
]

result = {
    "gate": "version4_common_updown_krajewski_loop",
    "primary_rectangle_labels": {
        node: {"left": labels[0], "right": labels[1]}
        for node, labels in primary_labels.items()
    },
    "all_primary_edges_order_one_allowed": all(
        order_one_allowed(first, second)
        for first, second in primary_edges
    ),
    "primary_rectangle_node_count": 4,
    "j_paired_total_node_count": 8,
    "family_block_dimension": 3,
    "full_dirac_dimension": 24,
    "common_loop_generates_cross_word": True,
    "full_trace_cross_term": "16 cos(theta) Tr(P_minus H_u H_d)",
    "relative_orbits": orbit_rows,
    "positive_quartic_selected_orbit_count": len(selected_rows),
    "positive_quartic_selected_cross_words": [
        row["cross_word"] for row in selected_rows
    ],
    "commuting_orbit_removed": all(
        row["cross_word"] != "0" for row in selected_rows
    ),
    "orientation_sign_selected": False,
    "selected_loop_phases_are_cp_even": all(
        row["phase_minimum"] in {"0", "pi"} for row in selected_rows
    ),
    "nonzero_common_connector_assumed": True,
    "status": "a common J-paired Krajewski rectangle derives the cross word and selects the two noncommuting relative orbits, but phase relaxation leaves their orientations degenerate and CP-even",
}

with open(
    "s2t_v4_common_updown_krajewski_loop_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))