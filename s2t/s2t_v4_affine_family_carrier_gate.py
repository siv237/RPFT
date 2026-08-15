import itertools
import json

import sympy as sp


points = [(0, 0), (0, 1), (1, 0), (1, 1)]
point_index = {point: index for index, point in enumerate(points)}


def det_mod2(matrix):
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 2


gl2 = []
for entries in itertools.product(range(2), repeat=4):
    matrix = ((entries[0], entries[1]), (entries[2], entries[3]))
    if det_mod2(matrix) == 1:
        gl2.append(matrix)


def affine_image(matrix, shift, point):
    return (
        (matrix[0][0] * point[0] + matrix[0][1] * point[1] + shift[0]) % 2,
        (matrix[1][0] * point[0] + matrix[1][1] * point[1] + shift[1]) % 2,
    )


permutation_matrices = []
permutations = []
for matrix in gl2:
    for shift in points:
        permutation = tuple(point_index[affine_image(matrix, shift, point)] for point in points)
        P = sp.zeros(4)
        for source, target in enumerate(permutation):
            P[target, source] = 1
        permutations.append(permutation)
        permutation_matrices.append(P)

unique_permutations = sorted(set(permutations))

x = sp.symbols("x0:16")
X = sp.Matrix(4, 4, x)
equations = []
for P in permutation_matrices:
    equations.extend(list(X * P - P * X))
coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, x)
commutant_basis_vectors = coefficient_matrix.nullspace()
commutant_basis = [sp.Matrix(4, 4, vector) for vector in commutant_basis_vectors]

I = sp.eye(4)
J = sp.ones(4)
P1 = J / 4
P3 = I - P1
L = 4 * I - J

average_group_matrix = sp.zeros(4)
for P in permutation_matrices:
    average_group_matrix += P
average_group_matrix /= len(permutation_matrices)

result = {
    "gate": "version4_affine_family_carrier",
    "torsor": "F2^2",
    "gl2_order": len(gl2),
    "affine_group_order": len(unique_permutations),
    "is_full_s4_permutation_group": len(unique_permutations) == 24,
    "commutant_dimension": len(commutant_basis),
    "commutant_is_span_I_J": len(commutant_basis) == 2,
    "group_average_equals_J_over_4": average_group_matrix == P1,
    "uniform_projector_rank": P1.rank(),
    "triplet_projector_rank": P3.rank(),
    "triplet_projector_idempotent": P3 * P3 == P3,
    "complete_graph_laplacian_eigenvalues": {str(key): value for key, value in L.eigenvals().items()},
    "singlet_mass_eigenvalues": {str(key): value for key, value in J.eigenvals().items()},
    "triplet_irreducibility_test": "the full commutant restricts to scalars on im(P3)",
    "physical_status": "conditional on promoting the full affine torsor symmetry to a family symmetry",
    "open_items": [
        "derive the affine symmetry from a parent action",
        "break exact triplet degeneracy without a free Yukawa matrix",
        "connect the triplet to the observed-sector finite algebra",
    ],
}

with open("s2t_v4_affine_family_carrier_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))