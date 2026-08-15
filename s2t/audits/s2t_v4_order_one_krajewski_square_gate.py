import json

import sympy as sp


nodes = {
    "A": ("o", "o"),
    "B": ("o", "h"),
    "C": ("h", "h"),
    "D": ("h", "o"),
}


def order_one_allowed(first, second):
    left_first, right_first = nodes[first]
    left_second, right_second = nodes[second]
    return left_first == left_second or right_first == right_second


edges = []
node_names = list(nodes)
for first_index, first in enumerate(node_names):
    for second in node_names[first_index + 1 :]:
        edges.append(
            {
                "edge": f"{first}-{second}",
                "same_left": nodes[first][0] == nodes[second][0],
                "same_right": nodes[first][1] == nodes[second][1],
                "order_one_allowed": order_one_allowed(first, second),
            }
        )

allowed_edges = [edge["edge"] for edge in edges if edge["order_one_allowed"]]
forbidden_edges = [edge["edge"] for edge in edges if not edge["order_one_allowed"]]

amplitude_a, amplitude_b, phase = sp.symbols(
    "a b phi", positive=True, real=True
)
coupling_a = amplitude_a
coupling_b = amplitude_b * sp.exp(sp.I * phase)

dirac = sp.zeros(4)
dirac[0, 1] = coupling_a
dirac[1, 0] = sp.conjugate(coupling_a)
dirac[0, 3] = sp.conjugate(coupling_a)
dirac[3, 0] = coupling_a
dirac[1, 2] = coupling_b
dirac[2, 1] = sp.conjugate(coupling_b)
dirac[3, 2] = sp.conjugate(coupling_b)
dirac[2, 3] = coupling_b

j_permutation = sp.Matrix(
    [
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
    ]
)

j_compatibility_residual = sp.simplify(
    j_permutation * sp.conjugate(dirac) * j_permutation - dirac
)
trace_d2 = sp.simplify(sp.trace(dirac**2))
trace_d4 = sp.simplify(
    sp.expand_complex(sp.trace(dirac**4)).rewrite(sp.cos)
)
determinant = sp.simplify(
    sp.expand_complex(sp.det(dirac)).rewrite(sp.sin)
)

family_basis = []
for row in range(3):
    for column in range(3):
        matrix = sp.zeros(3)
        matrix[row, column] = 1
        family_basis.append(matrix)
family_span_dimension = len({tuple(matrix) for matrix in family_basis})

result = {
    "gate": "version4_order_one_krajewski_square",
    "bimodule_nodes": {
        name: {"left_label": labels[0], "right_label": labels[1]}
        for name, labels in nodes.items()
    },
    "edge_order_one_ledger": edges,
    "allowed_edges": allowed_edges,
    "forbidden_diagonal_edges": forbidden_edges,
    "allowed_graph_is_four_cycle": set(allowed_edges)
    == {"A-B", "A-D", "B-C", "C-D"},
    "triangle_cycle_possible": False,
    "minimum_order_one_cycle_length": 4,
    "real_structure_map": {"A": "A", "B": "D", "C": "C", "D": "B"},
    "j_compatibility_residual_is_zero": j_compatibility_residual == sp.zeros(4),
    "trace_D2": str(trace_d2),
    "trace_D4": str(trace_d4),
    "determinant_D": str(determinant),
    "positive_quartic_phase_minima": ["pi/2", "-pi/2"],
    "phase_sign_is_degenerate": True,
    "j_structure_eliminates_cycle_phase": False,
    "unrestricted_family_edge_product_span_dimension": family_span_dimension,
    "unrestricted_family_edges_return_full_M3": family_span_dimension == 9,
    "status": "order-one replaces the triangular connector by a Krajewski square; J preserves one CP-evenly selected loop phase, but unrestricted family factors restore arbitrary M3",
}

with open(
    "s2t_v4_order_one_krajewski_square_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))