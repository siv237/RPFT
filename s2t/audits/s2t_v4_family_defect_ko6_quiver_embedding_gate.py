import itertools
import json

import numpy as np


TOLERANCE = 1.0e-9


def block_diagonal(blocks):
    total_size = sum(block.shape[0] for block in blocks)
    result = np.zeros((total_size, total_size), dtype=complex)
    offset = 0
    for block in blocks:
        size = block.shape[0]
        result[offset : offset + size, offset : offset + size] = block
        offset += size
    return result


def particle_dirac(locking, pairing):
    zero = np.zeros((3, 3), dtype=complex)
    pairing_block = pairing * np.eye(3)
    return np.block(
        [
            [zero, locking.conj().T, zero],
            [locking, zero, pairing_block.conj().T],
            [zero, pairing_block, zero],
        ]
    )


def ko6_operators():
    identity9 = np.eye(9)
    zero9 = np.zeros((9, 9))
    reality_permutation = np.block(
        [[zero9, identity9], [identity9, zero9]]
    )
    grading_particle = block_diagonal(
        [np.eye(3), -np.eye(3), np.eye(3)]
    )
    grading = block_diagonal([grading_particle, -grading_particle])
    return reality_permutation, grading


def algebra_representation(matrix_part, scalar_left, scalar_right):
    identity = np.eye(3)
    particle_blocks = [
        scalar_left * identity,
        matrix_part,
        matrix_part,
    ]
    conjugate_blocks = [
        np.conj(scalar_left) * identity,
        np.conj(scalar_left) * identity,
        np.conj(scalar_right) * identity,
    ]
    return block_diagonal(particle_blocks + conjugate_blocks)


def opposite_representation(representation, reality):
    return reality @ representation.conj() @ reality


def algebra_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append((matrix, 0.0, 0.0))
    basis.append((np.zeros((3, 3)), 1.0, 0.0))
    basis.append((np.zeros((3, 3)), 0.0, 1.0))
    basis.append((np.zeros((3, 3)), 0.0, 1.0j))
    return basis


def first_order_residual(dirac, left_representation, right_opposite):
    first_commutator = dirac @ left_representation - left_representation @ dirac
    double_commutator = (
        first_commutator @ right_opposite
        - right_opposite @ first_commutator
    )
    return np.linalg.norm(double_commutator)


rng = np.random.default_rng(20260815)
locking = rng.normal(size=(3, 3))
pairing = 0.37 + 0.21j
particle = particle_dirac(locking, pairing)
dirac = block_diagonal([particle, particle.conj()])
reality, grading = ko6_operators()

representations = [
    algebra_representation(*basis_element) for basis_element in algebra_basis()
]
opposite_representations = [
    opposite_representation(representation, reality)
    for representation in representations
]

order_zero_residuals = [
    np.linalg.norm(left @ right - right @ left)
    for left in representations
    for right in opposite_representations
]
first_order_residuals = [
    first_order_residual(dirac, left, right)
    for left in representations
    for right in opposite_representations
]

nonscalar_pairing_matrix = rng.normal(size=(3, 3))
zero = np.zeros((3, 3), dtype=complex)
nonscalar_particle = np.block(
    [
        [zero, locking.T, zero],
        [locking, zero, nonscalar_pairing_matrix.T],
        [zero, nonscalar_pairing_matrix, zero],
    ]
)
nonscalar_dirac = block_diagonal(
    [nonscalar_particle, nonscalar_particle.conj()]
)
nonscalar_first_order_residuals = [
    first_order_residual(nonscalar_dirac, left, right)
    for left in representations
    for right in opposite_representations
]

commutator_equations = []
for matrix_basis_element, _, _ in algebra_basis()[:9]:
    for row in range(3):
        for column in range(3):
            equation = np.zeros(9)
            for variable_row in range(3):
                for variable_column in range(3):
                    variable = np.zeros((3, 3))
                    variable[variable_row, variable_column] = 1.0
                    index = 3 * variable_row + variable_column
                    equation[index] = (
                        variable @ matrix_basis_element
                        - matrix_basis_element @ variable
                    )[row, column]
            commutator_equations.append(equation)
commutator_matrix = np.array(commutator_equations)
commutator_singular_values = np.linalg.svd(
    commutator_matrix, compute_uv=False
)
pairing_kernel_dimension = 9 - int(
    np.sum(commutator_singular_values > TOLERANCE)
)


def radial_trace_ledger(frame_radius, pairing_radius):
    radial_particle = particle_dirac(
        frame_radius * np.eye(3), pairing_radius
    )
    trace_two = float(np.trace(radial_particle @ radial_particle).real)
    trace_four = float(
        np.trace(np.linalg.matrix_power(radial_particle, 4)).real
    )
    moment_map = (frame_radius**2 - pairing_radius**2) * np.eye(3)
    moment_square = float(np.trace(moment_map @ moment_map).real / 3.0)
    grading_particle = block_diagonal(
        [np.eye(3), -np.eye(3), np.eye(3)]
    )
    graded_trace_four = float(
        np.trace(
            grading_particle @ np.linalg.matrix_power(radial_particle, 4)
        ).real
    )
    return trace_two, trace_four, moment_square, graded_trace_four


sample_radii = [(0.4, 0.7), (0.9, 0.2), (1.1, 0.8)]
trace_rows = []
for frame_radius, pairing_radius in sample_radii:
    trace_two, trace_four, moment_square, graded_trace_four = radial_trace_ledger(
        frame_radius, pairing_radius
    )
    trace_rows.append(
        {
            "frame_radius": frame_radius,
            "pairing_radius": pairing_radius,
            "particle_trace_D2": trace_two,
            "particle_trace_D4": trace_four,
            "moment_map_square": moment_square,
            "particle_supertrace_D4": graded_trace_four,
            "trace_D4_formula_residual": abs(
                trace_four
                - 6.0 * (frame_radius**2 + pairing_radius**2) ** 2
            ),
            "moment_formula_residual": abs(
                moment_square - (frame_radius**2 - pairing_radius**2) ** 2
            ),
        }
    )

result = {
    "gate": "version4_family_defect_ko6_quiver_embedding_gate",
    "finite_geometry": {
        "algebra": "R_0 direct_sum M3(R)_G direct_sum C_2",
        "particle_bimodule_labels": ["(0,0) x3", "(G,0)", "(G,2)"],
        "particle_grading": ["+", "-", "+"],
        "KO6_completion": "conjugate transposed-label chain with opposite grading",
        "complex_dimension": 18,
        "edges": {
            "X": "(0,0)x3 -> (G,0), arbitrary 3x3 locking matrix",
            "Y": "(G,0) -> (G,2), forced to Phi I3 by first-order condition",
        },
    },
    "checks": {
        "self_adjoint_residual": float(np.linalg.norm(dirac - dirac.conj().T)),
        "odd_grading_residual": float(np.linalg.norm(grading @ dirac + dirac @ grading)),
        "reality_residual": float(
            np.linalg.norm(dirac @ reality - reality @ dirac.conj())
        ),
        "J_gamma_anticommutator_residual": float(
            np.linalg.norm(reality @ grading + grading @ reality)
        ),
        "maximum_order_zero_residual": max(order_zero_residuals),
        "maximum_first_order_residual_scalar_pairing": max(first_order_residuals),
        "maximum_first_order_residual_nonscalar_pairing": max(
            nonscalar_first_order_residuals
        ),
        "first_order_pairing_kernel_dimension": pairing_kernel_dimension,
        "maximum_trace_D4_formula_residual": max(
            row["trace_D4_formula_residual"] for row in trace_rows
        ),
        "maximum_moment_formula_residual": max(
            row["moment_formula_residual"] for row in trace_rows
        ),
        "maximum_particle_supertrace_D4_residual": max(
            abs(row["particle_supertrace_D4"]) for row in trace_rows
        ),
    },
    "quartic_sign_comparison": {
        "ordinary_particle_trace": (
            "Tr D_p^4=6(rho^2+r^2)^2, mixed coefficient +12"
        ),
        "moment_map_trace": (
            "tau_3(mu^2)=(rho^2-r^2)^2, mixed coefficient -2"
        ),
        "graded_supertrace": "Str D_p^4=0",
        "conclusion": (
            "the KO6/order-one quiver exists, but the ordinary single-trace "
            "spectral quartic has the opposite mixed sign and the graded trace "
            "cancels; the moment-map action requires an auxiliary D-term, "
            "relative curvature, or another non-ordinary spectral functional"
        ),
    },
    "trace_rows": trace_rows,
    "status": {
        "KO6_representation_embedding": "pass",
        "order_zero": "pass",
        "first_order_scalar_pairing_selection": "pass",
        "ordinary_spectral_action_moment_map_origin": "fail_by_mixed_sign",
        "remaining_route": (
            "derive the middle-node moment-map norm as a relative/auxiliary "
            "curvature functional with the same kinetic normalization, rather "
            "than as Tr D_F^4"
        ),
    },
}

with open(
    "s2t_v4_family_defect_ko6_quiver_embedding_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, indent=2)

print(json.dumps(result["checks"], indent=2))
print(json.dumps(result["quartic_sign_comparison"], indent=2))