#!/usr/bin/env python3
"""Касательная геометрия ранга один и факторизация двух форм по мусору."""

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_rank_one_tangent_junk_gate_results.json"
TOL = 1.0e-9


def commutator(left, right):
    return left @ right - right @ left


def orthonormal_span(columns, tolerance=TOL):
    if columns.shape[1] == 0:
        return np.zeros((columns.shape[0], 0), dtype=columns.dtype)
    left, singular_values, _ = np.linalg.svd(columns, full_matrices=False)
    return left[:, singular_values > tolerance]


def nullspace(columns, tolerance=TOL):
    _, singular_values, right = np.linalg.svd(columns, full_matrices=True)
    rank = int(np.sum(singular_values > tolerance))
    return right[rank:].conj().T


def span_residual(columns, span_basis):
    if columns.shape[1] == 0:
        return 0.0
    residual = columns - span_basis @ (span_basis.conj().T @ columns)
    return float(np.linalg.norm(residual))


def vector_residual(matrix, span_basis):
    vector = matrix.reshape(-1)
    residual = vector - span_basis @ (span_basis.conj().T @ vector)
    return float(np.linalg.norm(residual))


def matrix_units(indices):
    units = []
    for row in indices:
        for column in indices:
            unit = np.zeros((3, 3), dtype=complex)
            unit[row, column] = 1.0
            units.append(unit)
    return units


rho = np.diag([1.0, 0.0, 0.0]).astype(complex)
Q = np.eye(3, dtype=complex) - rho
algebra_basis = [rho] + matrix_units([1, 2])
off_diagonal_basis = []
for index in [1, 2]:
    upper = np.zeros((3, 3), dtype=complex)
    upper[0, index] = 1.0
    lower = np.zeros((3, 3), dtype=complex)
    lower[index, 0] = 1.0
    off_diagonal_basis.extend([upper, lower])
diagonal_basis = [rho] + matrix_units([1, 2])
q_block_basis = matrix_units([1, 2])


def stack(matrices):
    return np.stack([matrix.reshape(-1) for matrix in matrices], axis=1)


off_diagonal_span = orthonormal_span(stack(off_diagonal_basis))
diagonal_span = orthonormal_span(stack(diagonal_basis))
q_block_span = orthonormal_span(stack(q_block_basis))
rho_span = orthonormal_span(rho.reshape(-1, 1))


def determinantal_tangent_audit():
    """Линеаризация всех миноров 2x2 в точке rho."""
    equations = []
    for rows in combinations(range(3), 2):
        for columns in combinations(range(3), 2):
            r0, r1 = rows
            c0, c1 = columns
            derivative = np.zeros((3, 3), dtype=complex)
            derivative[r0, c0] += rho[r1, c1]
            derivative[r1, c1] += rho[r0, c0]
            derivative[r0, c1] -= rho[r1, c0]
            derivative[r1, c0] -= rho[r0, c1]
            equations.append(derivative.reshape(-1))
    jacobian = np.stack(equations, axis=0)
    tangent = nullspace(jacobian)
    anchored = orthonormal_span(stack([rho] + off_diagonal_basis))
    return {
        "minor_count": len(equations),
        "Jacobian_rank": int(np.linalg.matrix_rank(jacobian, tol=TOL)),
        "tangent_complex_dimension": int(tangent.shape[1]),
        "anchored_module_complex_dimension": int(anchored.shape[1]),
        "tangent_outside_anchored_module": span_residual(tangent, anchored),
        "anchored_module_outside_tangent": span_residual(anchored, tangent),
    }


def represented_calculus(connector):
    vector = np.asarray(connector, dtype=complex).reshape(2, 1)
    dirac = np.block(
        [
            [np.zeros((1, 1), dtype=complex), vector.conj().T],
            [vector, np.zeros((2, 2), dtype=complex)],
        ]
    )
    commutators = [commutator(dirac, element) for element in algebra_basis]

    one_generators = []
    differentials = []
    for first, second in product(range(len(algebra_basis)), repeat=2):
        one_generators.append(algebra_basis[first] @ commutators[second])
        differentials.append(commutators[first] @ commutators[second])
    one_matrix = stack(one_generators)
    one_kernel = nullspace(one_matrix)

    junk_generators = []
    for kernel_index in range(one_kernel.shape[1]):
        junk_generators.append(
            sum(
                one_kernel[index, kernel_index] * differentials[index]
                for index in range(len(differentials))
            )
        )
    junk_matrix = stack(junk_generators)

    two_generators = []
    for first, second, third in product(range(len(algebra_basis)), repeat=3):
        two_generators.append(
            algebra_basis[first] @ commutators[second] @ commutators[third]
        )
    two_matrix = stack(two_generators)

    one_basis = orthonormal_span(one_matrix)
    junk_basis = orthonormal_span(junk_matrix)
    two_basis = orthonormal_span(two_matrix)
    quotient_candidates = two_basis - junk_basis @ (junk_basis.conj().T @ two_basis)
    quotient_basis = orthonormal_span(quotient_candidates)

    raising = np.zeros((3, 3), dtype=complex)
    raising[1:, 0] = vector.reshape(2)
    oriented_curvature = commutator(raising, raising.conj().T)
    metric_curvature = dirac @ dirac
    connector_norm_squared = float(np.vdot(vector, vector).real)
    oriented_coefficient = complex(np.vdot(rho.reshape(-1), oriented_curvature.reshape(-1)))
    metric_coefficient = complex(np.vdot(rho.reshape(-1), metric_curvature.reshape(-1)))

    return {
        "connector": [[float(value.real), float(value.imag)] for value in vector.reshape(2)],
        "connector_norm_squared": connector_norm_squared,
        "represented_one_rank": int(one_basis.shape[1]),
        "one_form_kernel_dimension": int(one_kernel.shape[1]),
        "represented_two_rank": int(two_basis.shape[1]),
        "degree_two_junk_rank": int(junk_basis.shape[1]),
        "quotient_rank": int(quotient_basis.shape[1]),
        "one_forms_outside_off_diagonal_tangent": span_residual(one_basis, off_diagonal_span),
        "off_diagonal_tangent_outside_one_forms": span_residual(off_diagonal_span, one_basis),
        "two_forms_outside_diagonal_algebra": span_residual(two_basis, diagonal_span),
        "diagonal_algebra_outside_two_forms": span_residual(diagonal_span, two_basis),
        "junk_outside_QM2Q": span_residual(junk_basis, q_block_span),
        "QM2Q_outside_junk": span_residual(q_block_span, junk_basis),
        "quotient_outside_rho": span_residual(quotient_basis, rho_span),
        "rho_outside_quotient": span_residual(rho_span, quotient_basis),
        "Q_block_norm_after_quotient": vector_residual(Q, junk_basis),
        "oriented_curvature_quotient_coefficient": [
            float(oriented_coefficient.real),
            float(oriented_coefficient.imag),
        ],
        "metric_curvature_quotient_coefficient": [
            float(metric_coefficient.real),
            float(metric_coefficient.imag),
        ],
        "expected_oriented_coefficient": -connector_norm_squared,
        "expected_metric_coefficient": connector_norm_squared,
        "quotient_norm_squares_equal": bool(
            abs(abs(oriented_coefficient) ** 2 - abs(metric_coefficient) ** 2) < TOL
        ),
        "surviving_self_adjoint_direction": "rho",
    }


previous = json.loads(
    (ROOT / "s2t/results/s2t_v5_sm_linking_corner_gate_results.json").read_text(
        encoding="utf-8"
    )
)
assert previous["state_anchored_projection_reaudit"][
    "valid_interpretation"
] == "orthogonal projection onto an off-diagonal operator bimodule"

connectors = [
    [1.0, 0.0],
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 1.0j],
    [1.0 + 1.0j, 2.0 - 1.0j],
]
samples = [represented_calculus(connector) for connector in connectors]

for sample in samples:
    assert sample["represented_one_rank"] == 4
    assert sample["represented_two_rank"] == 5
    assert sample["degree_two_junk_rank"] == 4
    assert sample["quotient_rank"] == 1
    for key, value in sample.items():
        if key.endswith(("outside_one_forms", "outside_off_diagonal_tangent")):
            assert value < TOL
        if key.endswith(("outside_two_forms", "outside_diagonal_algebra")):
            assert value < TOL
        if key in {
            "junk_outside_QM2Q",
            "QM2Q_outside_junk",
            "quotient_outside_rho",
            "rho_outside_quotient",
        }:
            assert value < TOL
    assert sample["Q_block_norm_after_quotient"] < TOL
    assert abs(
        sample["oriented_curvature_quotient_coefficient"][0]
        - sample["expected_oriented_coefficient"]
    ) < TOL
    assert abs(
        sample["metric_curvature_quotient_coefficient"][0]
        - sample["expected_metric_coefficient"]
    ) < TOL
    assert sample["quotient_norm_squares_equal"]

tangent = determinantal_tangent_audit()
assert tangent["Jacobian_rank"] == 4
assert tangent["tangent_complex_dimension"] == 5
assert tangent["anchored_module_complex_dimension"] == 5
assert tangent["tangent_outside_anchored_module"] < TOL
assert tangent["anchored_module_outside_tangent"] < TOL

result = {
    "gate": "version5_rank_one_tangent_junk_gate",
    "zero_degree_algebra": {
        "formula": "A_rho=C rho + Q M3(C) Q isomorphic to C+M2(C)",
        "complex_dimension": 5,
        "projector_rank": 1,
    },
    "rank_one_determinantal_tangent": tangent,
    "generic_connector_samples": samples,
    "structural_result": {
        "represented_one_forms": "rho M3 Q + Q M3 rho",
        "represented_one_forms_complex_dimension": 4,
        "missing_cone_direction": "C rho (radial amplitude belongs to degree zero)",
        "represented_two_forms": "C rho + Q M3 Q",
        "degree_two_junk": "Q M3 Q",
        "degree_two_quotient": "C rho",
        "quotient_complex_dimension": 1,
        "orientation_after_quotient": (
            "[d,d*] and D^2 survive with opposite scalar signs but equal squared norm"
        ),
        "middle_shape_curvature_survives": False,
    },
    "verdict": {
        "support_condition_from_rank_one_geometry": "pass",
        "off_diagonal_linking_corner_as_one_forms": "pass",
        "stable_degree_two_quotient": "pass",
        "full_moment_map_shape_from_quotient": "fail",
        "orientation_selected_by_squared_curvature": "fail",
        "radial_anchor_curvature": "conditional_pass",
        "physical_closure": False,
        "status": (
            "rank_one geometry canonically yields the linking tangent, but junk removes "
            "the Q-block curvature and leaves only the anchor scalar"
        ),
    },
    "next_gate": (
        "Tensor the surviving anchor line with the already established observed-sector "
        "commuting square and test whether the missing Q-block moment map is supplied by "
        "a relative bimodule curvature rather than by the ordinary Connes quotient."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))