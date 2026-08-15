import json

import numpy as np

from s2t_v4_pati_salam_ko6_phi_sigma_hessian_gate import (
    composite_yukawa,
    crossed_majorana,
)


TOLERANCE = 1.0e-9


def hermitian_traceless_basis(size):
    basis = []
    for index in range(size - 1):
        diagonal = np.zeros((size, size), dtype=complex)
        diagonal[index, index] = 1.0
        diagonal[index + 1, index + 1] = -1.0
        diagonal /= np.linalg.norm(diagonal)
        basis.append(diagonal)
    for row in range(size):
        for column in range(row + 1, size):
            symmetric = np.zeros((size, size), dtype=complex)
            symmetric[row, column] = 1.0 / np.sqrt(2.0)
            symmetric[column, row] = 1.0 / np.sqrt(2.0)
            basis.append(symmetric)
            antisymmetric = np.zeros((size, size), dtype=complex)
            antisymmetric[row, column] = -1j / np.sqrt(2.0)
            antisymmetric[column, row] = 1j / np.sqrt(2.0)
            basis.append(antisymmetric)
    return basis


def real_vector(matrix):
    return np.r_[matrix.real.ravel(), matrix.imag.ravel()]


def map_rank(basis, map_function):
    columns = [real_vector(map_function(element)) for element in basis]
    matrix = np.column_stack(columns)
    return int(np.linalg.matrix_rank(matrix, tol=TOLERANCE))


def stacked_map_rank(basis, map_functions):
    columns = []
    for element in basis:
        columns.append(
            np.concatenate([real_vector(map_function(element)) for map_function in map_functions])
        )
    matrix = np.column_stack(columns)
    return int(np.linalg.matrix_rank(matrix, tol=TOLERANCE))


def phi_matrix_basis(sigma):
    basis = []
    for coordinate in range(8):
        values = np.zeros(8)
        values[coordinate] = 1.0
        phi = np.array(
            [
                [values[0] + 1j * values[1], values[2] + 1j * values[3]],
                [values[4] + 1j * values[5], values[6] + 1j * values[7]],
            ]
        )
        basis.append(composite_yukawa(phi, sigma))
    return basis


def projector_rank_ledger():
    sigma_basis = hermitian_traceless_basis(4)
    ledger = []
    for projector_rank in (1, 2, 3, 4):
        projector = np.diag([1.0] * projector_rank + [0.0] * (4 - projector_rank))
        connected_maps = [
            lambda sigma, projector=projector: projector @ sigma,
            lambda sigma, projector=projector: sigma @ projector,
            lambda sigma, projector=projector: projector @ sigma - sigma @ projector,
            lambda sigma, projector=projector: projector @ sigma + sigma @ projector,
            lambda sigma, projector=projector: np.array(
                [[np.trace(projector @ sigma)]], dtype=complex
            ),
        ]
        rank = stacked_map_rank(sigma_basis, connected_maps)
        expected_kernel = max((4 - projector_rank) ** 2 - 1, 0)
        ledger.append(
            {
                "projector_rank": projector_rank,
                "connected_span_rank": rank,
                "kernel_dimension": 15 - rank,
                "expected_complement_su_kernel": expected_kernel,
            }
        )
    return ledger


delta = np.zeros((2, 4), dtype=complex)
delta[0, 0] = 2.0 ** (-0.25)
majorana = crossed_majorana(delta)
majorana_norm = np.vdot(majorana, majorana).real
left_projector = majorana @ majorana.conj().T / majorana_norm
right_projector = majorana.conj().T @ majorana / majorana_norm

sigma_bl = np.diag([0.75, -0.25, -0.25, -0.25])
phi_basis = phi_matrix_basis(sigma_bl)
phi_maps = {
    "Mdagger_Y": lambda yukawa: majorana.conj().T @ yukawa,
    "Y_Mdagger": lambda yukawa: yukawa @ majorana.conj().T,
    "left_projector_Y": lambda yukawa: left_projector @ yukawa,
    "Y_right_projector": lambda yukawa: yukawa @ right_projector,
    "commutator_Mdagger_Y": lambda yukawa: majorana.conj().T @ yukawa
    - yukawa @ majorana.conj().T,
    "anticommutator_Mdagger_Y": lambda yukawa: majorana.conj().T @ yukawa
    + yukawa @ majorana.conj().T,
}
phi_ranks = {
    name: map_rank(phi_basis, map_function)
    for name, map_function in phi_maps.items()
}
phi_stacked_rank = stacked_map_rank(phi_basis, list(phi_maps.values()))

color_projector = delta.conj().T @ delta
color_projector /= np.trace(color_projector)
sigma_basis = hermitian_traceless_basis(4)
sigma_maps = {
    "P_Sigma": lambda sigma: color_projector @ sigma,
    "Sigma_P": lambda sigma: sigma @ color_projector,
    "commutator": lambda sigma: color_projector @ sigma - sigma @ color_projector,
    "anticommutator": lambda sigma: color_projector @ sigma + sigma @ color_projector,
    "projected_trace": lambda sigma: np.array(
        [[np.trace(color_projector @ sigma)]], dtype=complex
    ),
}
sigma_ranks = {
    name: map_rank(sigma_basis, map_function)
    for name, map_function in sigma_maps.items()
}
sigma_stacked_rank = stacked_map_rank(sigma_basis, list(sigma_maps.values()))
factorized_full_rank = map_rank(sigma_basis, lambda sigma: sigma)

q_projector = np.eye(4) - color_projector
su3_kernel_basis = []
embedded_su3 = hermitian_traceless_basis(3)
for generator in embedded_su3:
    embedded = np.zeros((4, 4), dtype=complex)
    embedded[1:, 1:] = generator
    su3_kernel_basis.append(embedded)
su3_max_connected_image = max(
    np.linalg.norm(map_function(generator))
    for generator in su3_kernel_basis
    for map_function in sigma_maps.values()
)

result = {
    "gate": "version4_pati_salam_rank_one_connected_curvature_no_go",
    "rank_one_background": {
        "rank_Delta": int(np.linalg.matrix_rank(delta)),
        "rank_color_projector": int(np.linalg.matrix_rank(color_projector)),
        "rank_crossed_Majorana": int(np.linalg.matrix_rank(majorana)),
    },
    "quadratic_connected_word_basis": [
        "Tr(P Sigma^2)",
        "Tr(P Sigma P Sigma)",
        "(Tr(P Sigma))^2",
    ],
    "Sigma_map_ranks": sigma_ranks,
    "Sigma_all_connected_maps_rank": sigma_stacked_rank,
    "Sigma_common_kernel_dimension": 15 - sigma_stacked_rank,
    "Sigma_kernel_identification": "embedded su(3) adjoint in Q Sigma Q",
    "Sigma_su3_kernel_dimension": len(su3_kernel_basis),
    "Sigma_su3_max_connected_image": float(su3_max_connected_image),
    "factorized_TrP_TrSigma2_rank": factorized_full_rank,
    "projector_rank_ledger": projector_rank_ledger(),
    "phi_map_ranks": phi_ranks,
    "phi_all_connected_maps_rank": phi_stacked_rank,
    "phi_common_kernel_dimension": 8 - phi_stacked_rank,
    "structural_theorem": (
        "Any quadratic single-trace connected invariant generated by one "
        "rank-r color projector has a common su(4-r) adjoint kernel of "
        "dimension (4-r)^2-1. At the selected rank-one vacuum this is the "
        "eight-dimensional su(3) adjoint."
    ),
    "verdict": (
        "The irreducible rank-one relative cycle cannot generate a full-rank "
        "Sigma_4 Hessian through connected non-product contractions. All such "
        "contractions see at most seven of fifteen Sigma directions; the full "
        "phi connected span also retains a two-dimensional kernel. The only "
        "single-projector full-rank Sigma norm is factorized Tr(P)Tr(Sigma^2), "
        "already closed by product saturation."
    ),
    "next_gate": (
        "close Tome IV current finite geometry and require a new diagonal "
        "carrier of rank at least three, or several independently derived "
        "noncommuting color projectors, before reopening the physical branch"
    ),
}

with open(
    "s2t_v4_pati_salam_rank_one_connected_curvature_no_go_results.json",
    "w",
    encoding="utf-8",
) as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))