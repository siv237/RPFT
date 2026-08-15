import itertools
import json

import sympy as sp


points = [(0, 0), (0, 1), (1, 0), (1, 1)]
point_index = {point: index for index, point in enumerate(points)}


def det_mod2(matrix):
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 2


def image(matrix, point):
    return (
        (matrix[0][0] * point[0] + matrix[0][1] * point[1]) % 2,
        (matrix[1][0] * point[0] + matrix[1][1] * point[1]) % 2,
    )


def permutation_matrix(mapping):
    P = sp.zeros(4)
    for source, target in enumerate(mapping):
        P[target, source] = 1
    return P


gl2 = []
for entries in itertools.product(range(2), repeat=4):
    matrix = ((entries[0], entries[1]), (entries[2], entries[3]))
    if det_mod2(matrix) == 1:
        gl2.append(matrix)

# In H^1(K;F2), y is the unique nonzero square-zero class. A ring
# automorphism must fix y. The remaining image of x is x or x+y.
ring_automorphisms = []
for matrix in gl2:
    image_y = (matrix[0][1], matrix[1][1])
    if image_y == (0, 1):
        ring_automorphisms.append(matrix)

identity = ((1, 0), (0, 1))
shear = ((1, 0), (1, 1))
assert set(ring_automorphisms) == {identity, shear}

S_mapping = tuple(point_index[image(shear, point)] for point in points)
S = permutation_matrix(S_mapping)
I = sp.eye(4)
J = sp.ones(4)
P3 = I - J / 4
P_minus = (I - S) / 2

triplet_basis = sp.Matrix.hstack(
    sp.Matrix([1, 1, -1, -1]) / 2,
    sp.Matrix([1, -1, 1, -1]) / 2,
    sp.Matrix([1, -1, -1, 1]) / 2,
)
S_triplet = sp.simplify(triplet_basis.T * S * triplet_basis)
P_minus_triplet = sp.simplify(triplet_basis.T * P_minus * triplet_basis)


def translation(shift):
    mapping = tuple(
        point_index[((point[0] + shift[0]) % 2, (point[1] + shift[1]) % 2)]
        for point in points
    )
    return permutation_matrix(mapping)


T_p = translation((1, 0))
T_q = translation((0, 1))
T_p_triplet = sp.simplify(triplet_basis.T * T_p * triplet_basis)
T_q_triplet = sp.simplify(triplet_basis.T * T_q * triplet_basis)

result = {
    "gate": "version4_rank_one_breaking",
    "gl2_order": len(gl2),
    "cohomology_ring_automorphism_order": len(ring_automorphisms),
    "unique_nontrivial_ring_automorphism": str(shear),
    "shear_permutation": list(S_mapping),
    "shear_full_eigenvalues": {str(key): value for key, value in S.eigenvals().items()},
    "shear_triplet_eigenvalues": {str(key): value for key, value in S_triplet.eigenvals().items()},
    "odd_projector_rank_full": P_minus.rank(),
    "odd_projector_rank_triplet": P_minus_triplet.rank(),
    "odd_projector_triplet_eigenvalues": {str(key): value for key, value in P_minus_triplet.eigenvals().items()},
    "odd_projector_lies_in_triplet": P3 * P_minus == P_minus and P_minus * P3 == P_minus,
    "factor_translations_commute": T_p * T_q == T_q * T_p,
    "triplet_translation_p": str(T_p_triplet),
    "triplet_translation_q": str(T_q_triplet),
    "simultaneous_diagonal_family_algebra": T_p_triplet * T_q_triplet == T_q_triplet * T_p_triplet,
    "leading_texture": "one heavy family and two massless families",
    "mixing_verdict": "operators built only from the two factor translations share an eigenbasis and cannot predict nontrivial CKM",
    "next_requirement": "derive a sector-dependent noncommuting incidence operator before looking at CKM data",
}

with open("s2t_v4_rank_one_breaking_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))