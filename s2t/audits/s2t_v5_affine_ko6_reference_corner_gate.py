#!/usr/bin/env python3
"""Аффинный 4->3->3 KO6-бимодуль и канонический физический угол M300."""

import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_affine_ko6_reference_corner_gate_results.json"
TOL = 1.0e-10

affine = json.loads(
    (ROOT / "s2t/results/s2t_affine_spin_menu_triplet_results.json").read_text(
        encoding="utf-8"
    )
)
ko6 = json.loads(
    (
        ROOT
        / "s2t/results/s2t_v4_family_defect_ko6_quiver_embedding_gate_results.json"
    ).read_text(encoding="utf-8")
)
coordinate_gate = json.loads(
    (
        ROOT
        / "s2t/results/s2t_v5_m300_coordinate_algebra_wellposedness_gate_results.json"
    ).read_text(encoding="utf-8")
)
assert affine["canonical_decomposition"]["triplet_rank"] == 3
assert ko6["status"]["KO6_representation_embedding"] == "pass"
assert coordinate_gate["verdict"]["M300_as_coordinate_algebra_on_C300"] == "fail"


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def permutation_matrix(permutation):
    matrix = np.zeros((4, 4))
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


permutations = list(itertools.permutations(range(4)))
permutation_matrices = [permutation_matrix(item) for item in permutations]
P1 = sum(permutation_matrices) / len(permutation_matrices)
P3 = np.eye(4) - P1

projector_residuals = {
    "P1_idempotence": float(np.linalg.norm(P1 @ P1 - P1)),
    "P3_idempotence": float(np.linalg.norm(P3 @ P3 - P3)),
    "orthogonality": float(np.linalg.norm(P1 @ P3)),
    "sum_identity": float(np.linalg.norm(P1 + P3 - np.eye(4))),
    "S4_invariance": max(
        float(np.linalg.norm(matrix @ P3 - P3 @ matrix))
        for matrix in permutation_matrices
    ),
}
assert max(projector_residuals.values()) < TOL
assert np.linalg.matrix_rank(P1, tol=TOL) == 1
assert np.linalg.matrix_rank(P3, tol=TOL) == 3

# Канонический коизометрический кадр sum-zero триплета.
V = np.array(
    [
        [1.0, -1.0, 0.0, 0.0],
        [1.0, 1.0, -2.0, 0.0],
        [1.0, 1.0, 1.0, -3.0],
    ]
)
V /= np.linalg.norm(V, axis=1)[:, None]
frame_residuals = {
    "VVt_identity": float(np.linalg.norm(V @ V.T - np.eye(3))),
    "VtV_P3": float(np.linalg.norm(V.T @ V - P3)),
    "uniform_kernel": float(np.linalg.norm(V @ np.ones(4))),
}
assert max(frame_residuals.values()) < TOL

# Каждая перестановка S4 индуцирует ортогональное действие на триплете,
# относительно которого V является точным сплетающим оператором.
intertwiner_residuals = []
orientation_determinants = []
for permutation in permutation_matrices:
    triplet_action = V @ permutation @ V.T
    orientation_determinants.append(round(float(np.linalg.det(triplet_action))))
    intertwiner_residuals.append(
        float(np.linalg.norm(triplet_action @ V - V @ permutation))
    )
    assert np.linalg.norm(triplet_action @ triplet_action.T - np.eye(3)) < TOL
assert max(intertwiner_residuals) < TOL


def algebra_representation(matrix_part, scalar_zero, scalar_two):
    identity3 = np.eye(3)
    identity4 = np.eye(4)
    return block_diagonal(
        [
            scalar_zero * identity4,
            matrix_part,
            matrix_part,
            np.conj(scalar_zero) * identity4,
            np.conj(scalar_zero) * identity3,
            np.conj(scalar_two) * identity3,
        ]
    )


def algebra_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            matrix = np.zeros((3, 3))
            matrix[row, column] = 1.0
            basis.append((matrix, 0.0, 0.0))
    basis.extend(
        [
            (np.zeros((3, 3)), 1.0, 0.0),
            (np.zeros((3, 3)), 0.0, 1.0),
            (np.zeros((3, 3)), 0.0, 1.0j),
        ]
    )
    return basis


identity3 = np.eye(3)
zero3 = np.zeros((3, 3), dtype=complex)
zero4 = np.zeros((4, 4), dtype=complex)
zero43 = np.zeros((4, 3), dtype=complex)
zero34 = np.zeros((3, 4), dtype=complex)

rho = 0.83
phi = 0.61 + 0.20j
X = rho * V
Y = phi * identity3

particle_dirac = np.block(
    [
        [zero4, X.T, zero43],
        [X, zero3, Y.conj().T],
        [zero34, Y, zero3],
    ]
)
dirac = block_diagonal([particle_dirac, particle_dirac.conj()])

particle_grading = block_diagonal([np.eye(4), -identity3, identity3])
grading = block_diagonal([particle_grading, -particle_grading])

particle_height = block_diagonal([-P3, zero3, identity3])
height = block_diagonal([particle_height, -particle_height])

zero10 = np.zeros((10, 10))
J_matrix = np.block([[zero10, np.eye(10)], [np.eye(10), zero10]])

representations = [algebra_representation(*item) for item in algebra_basis()]
opposites = [J_matrix @ item.conj() @ J_matrix for item in representations]

ko6_residuals = {
    "selfadjoint_D": float(np.linalg.norm(dirac - dirac.conj().T)),
    "odd_D": float(np.linalg.norm(dirac @ grading + grading @ dirac)),
    "JD_equals_DJ": float(
        np.linalg.norm(J_matrix @ dirac.conj() @ J_matrix - dirac)
    ),
    "Jgamma_plus_gammaJ": float(
        np.linalg.norm(J_matrix @ grading.conj() @ J_matrix + grading)
    ),
    "Jh_plus_hJ": float(
        np.linalg.norm(J_matrix @ height.conj() @ J_matrix + height)
    ),
    "order_zero": max(
        float(np.linalg.norm(left @ right - right @ left))
        for left in representations
        for right in opposites
    ),
    "first_order": max(
        float(
            np.linalg.norm(
                (dirac @ left - left @ dirac) @ right
                - right @ (dirac @ left - left @ dirac)
            )
        )
        for left in representations
        for right in opposites
    ),
}
assert max(ko6_residuals.values()) < TOL

# Ориентированный дифференциал: на сопряжённой половине направление
# обращено вещественной структурой.
particle_differential = np.block(
    [
        [zero4, zero43, zero43],
        [X, zero3, zero3],
        [zero34, Y, zero3],
    ]
)
differential = block_diagonal(
    [particle_differential, particle_differential.T]
)
differential_residuals = {
    "D_reconstruction": float(
        np.linalg.norm(dirac - differential - differential.conj().T)
    ),
    "unit_frequency": float(
        np.linalg.norm(height @ differential - differential @ height - differential)
    ),
    "J_reverses_orientation": float(
        np.linalg.norm(
            J_matrix @ differential.conj() @ J_matrix
            - differential.conj().T
        )
    ),
}
assert max(differential_residuals.values()) < TOL

# Канонический опорный угол и его физическое дополнение.
reference_particle = block_diagonal([P1, zero3, zero3])
reference_projector = block_diagonal([reference_particle, reference_particle])
physical_projector = np.eye(20) - reference_projector
reference_residuals = {
    "idempotence": float(
        np.linalg.norm(reference_projector @ reference_projector - reference_projector)
    ),
    "J_invariance": float(
        np.linalg.norm(
            J_matrix @ reference_projector.conj() @ J_matrix
            - reference_projector
        )
    ),
    "grading_commutator": float(
        np.linalg.norm(reference_projector @ grading - grading @ reference_projector)
    ),
    "height_commutator": float(
        np.linalg.norm(reference_projector @ height - height @ reference_projector)
    ),
    "algebra_commutator": max(
        float(np.linalg.norm(reference_projector @ item - item @ reference_projector))
        for item in representations + opposites
    ),
    "vacuum_D_commutator": float(
        np.linalg.norm(reference_projector @ dirac - dirac @ reference_projector)
    ),
}
assert max(reference_residuals.values()) < TOL

base_kernel_dimension = 20 - int(np.linalg.matrix_rank(dirac, tol=TOL))
physical_dirac = physical_projector @ dirac @ physical_projector
physical_rank = int(np.linalg.matrix_rank(physical_projector, tol=TOL))
physical_kernel_dimension = physical_rank - int(
    np.linalg.matrix_rank(physical_dirac, tol=TOL)
)
assert base_kernel_dimension == 8
assert physical_rank == 18
assert physical_kernel_dimension == 6

# Полная кривизна и точная нормировка следа M300.
rng = np.random.default_rng(20260816)
curvature_residuals = []
trace_residuals = []
for _ in range(32):
    random_X = rng.normal(size=(3, 4)) @ P3
    random_phi = rng.normal() + 1.0j * rng.normal()
    random_Y = random_phi * identity3
    random_particle_d = np.block(
        [
            [zero4, zero43, zero43],
            [random_X, zero3, zero3],
            [zero34, random_Y, zero3],
        ]
    )
    random_d = block_diagonal([random_particle_d, random_particle_d.T])
    curvature = (
        random_d @ random_d.conj().T
        - random_d.conj().T @ random_d
        - height
    )
    expected_particle = block_diagonal(
        [
            P3 - random_X.T @ random_X,
            random_X @ random_X.T - abs(random_phi) ** 2 * identity3,
            (abs(random_phi) ** 2 - 1.0) * identity3,
        ]
    )
    curvature_residuals.append(
        np.linalg.norm(curvature[:10, :10] - expected_particle)
    )
    parent_trace = float(np.trace(curvature @ curvature).real / 20.0)
    expected_parent_trace = float(
        np.trace(expected_particle @ expected_particle).real / 10.0
    )
    trace_residuals.append(abs(parent_trace - expected_parent_trace))
assert max(curvature_residuals + trace_residuals) < TOL

# Точный 14-мерный гессиан прямоугольного ребра X и комплексного Phi.
variables = sp.symbols("z0:14", real=True)
X_symbolic = sp.Matrix(3, 4, variables[:12])
phi_real, phi_imaginary = variables[12], variables[13]
radius_squared = phi_real**2 + phi_imaginary**2
P3_symbolic = sp.eye(4) - sp.ones(4, 4) / 4
left = P3_symbolic - X_symbolic.T * X_symbolic
middle = X_symbolic * X_symbolic.T - radius_squared * sp.eye(3)
right = (radius_squared - 1) * sp.eye(3)
reduced_potential = sp.expand(
    (sp.trace(left**2) + sp.trace(middle**2) + sp.trace(right**2)) / 3
)

V_symbolic = sp.Matrix(
    [
        [1 / sp.sqrt(2), -1 / sp.sqrt(2), 0, 0],
        [1 / sp.sqrt(6), 1 / sp.sqrt(6), -2 / sp.sqrt(6), 0],
        [
            1 / sp.sqrt(12),
            1 / sp.sqrt(12),
            1 / sp.sqrt(12),
            -3 / sp.sqrt(12),
        ],
    ]
)
vacuum_point = list(V_symbolic) + [sp.Integer(1), sp.Integer(0)]
vacuum_substitution = dict(zip(variables, vacuum_point))
vacuum_hessian = sp.hessian(reduced_potential, variables).subs(
    vacuum_substitution
)
vacuum_eigenvalues = vacuum_hessian.eigenvals()
expected_vacuum_eigenvalues = {
    sp.Integer(0): 4,
    sp.Rational(4, 3): 3,
    sp.Rational(16, 3): 5,
    (sp.Integer(32) - 8 * sp.sqrt(7)) / 3: 1,
    (sp.Integer(32) + 8 * sp.sqrt(7)) / 3: 1,
}
assert vacuum_eigenvalues == expected_vacuum_eigenvalues

# Полный нормированный след M300 равен 3/10 сокращённого потенциала.
parent_trace_scale_relative_to_reduced = sp.Rational(3, 10)
parent_trace_hessian_eigenvalues = {
    sp.simplify(parent_trace_scale_relative_to_reduced * value): multiplicity
    for value, multiplicity in vacuum_eigenvalues.items()
}

result = {
    "date": "2026-08-16",
    "gate": "version5_affine_ko6_reference_corner_gate",
    "recovered_project_ingredients": {
        "affine_menu": "C4=1_uniform+3_sum_zero",
        "family_coordinate_algebra": "R0+M3(R)_G+C2",
        "observed_multiplicity": "10+bar5 of dimension 15",
        "KO6_doubling": True,
    },
    "dimension_identity": {
        "particle_base_nodes": [4, 3, 3],
        "particle_base_dimension": 10,
        "observed_package_dimension": 15,
        "KO6_factor": 2,
        "parent_dimension": 2 * 10 * 15,
        "formula": "2*(4+3+3)*15=300",
        "reference_full_rank": 2 * 1 * 15,
        "physical_full_rank": 2 * 9 * 15,
    },
    "affine_projectors": {
        "S4_element_count": len(permutations),
        "P1_rank": int(np.linalg.matrix_rank(P1, tol=TOL)),
        "P3_rank": int(np.linalg.matrix_rank(P3, tol=TOL)),
        "projector_residuals": projector_residuals,
        "frame_residuals": frame_residuals,
        "maximum_S4_intertwiner_residual": max(intertwiner_residuals),
        "triplet_orientation_determinants": sorted(set(orientation_determinants)),
    },
    "family_KO6_bimodule": {
        "particle_chain": "(0,0)^4 -> (G,0) -> (G,2)",
        "coordinate_algebra": "R0+M3(R)_G+C2",
        "base_complex_dimension": 20,
        "KO6_residuals": ko6_residuals,
        "differential_residuals": differential_residuals,
        "height": "diag(-P3,0_3,+I3) plus J-reversed conjugate",
    },
    "canonical_reference_corner": {
        "reference_projector": "P1 on the first node and its J-conjugate",
        "reference_residuals": reference_residuals,
        "full_base_kernel_before_corner": base_kernel_dimension,
        "physical_base_rank_after_corner": physical_rank,
        "physical_base_kernel_after_corner": physical_kernel_dimension,
        "full_physical_kernel_after_SU5_multiplicity": (
            physical_kernel_dimension * 15
        ),
        "physical_particle_count": physical_kernel_dimension * 15 // 2,
        "conditional_parent_trace_weight": "270/300=9/10",
    },
    "Hodge_curvature": {
        "particle_blocks": [
            "P3-X*X",
            "XX*-|Phi|^2 I3",
            "(|Phi|^2-1)I3",
        ],
        "maximum_block_residual": max(curvature_residuals),
        "maximum_parent_trace_residual": max(trace_residuals),
        "tau300_formula": "tau300(F^2)=Tr_particle(F^2)/10",
        "reduced_tau3_formula": "V_reduced=Tr_particle(F^2)/3",
        "tau300_over_reduced_factor": "3/10",
    },
    "vacuum_Hessian": {
        "variables": "12 real components of X plus 2 real components of Phi",
        "reduced_exact_spectrum": {
            "0": 4,
            "4/3": 3,
            "16/3": 5,
            "(32-8sqrt7)/3": 1,
            "(32+8sqrt7)/3": 1,
        },
        "parent_trace_exact_spectrum": {
            str(value): multiplicity
            for value, multiplicity in parent_trace_hessian_eigenvalues.items()
        },
        "signature": [10, 4, 0],
        "reference_chain_mixing_modes": 3,
        "reference_chain_mixing_eigenvalue_reduced": "4/3",
        "reference_chain_mixing_eigenvalue_tau300": "2/5",
    },
    "remaining_boundaries": {
        "reference_corner_is_dynamic_mass_removal": False,
        "reference_corner_is_canonical_affine_reduction": True,
        "SM_or_SU5_associative_coordinate_algebra_integrated": False,
        "naive_tensor_product_allowed": False,
        "kinetic_normalization_from_same_full_product_action": False,
        "unit_momentum_vacuum_revalidated_with_full_normalization": False,
        "full_BV_BRST_complex": False,
        "priority_combined_architecture": {
            "coordinate_algebra": "A_SM=C+H+M3(C)",
            "family_placement": "graded correspondence in pi(A_SM)'",
            "avoids_naive_M3_tensor_M3_to_M9": True,
            "differential_calculus_verified": False,
        },
    },
    "verdict": {
        "forgotten_affine_KO6_bimodule_recovered": "pass",
        "exact_M300_dimension_without_ad_hoc_reference_sum": "pass",
        "canonical_physical_45_particle_corner": "pass",
        "reference_chain_scalar_mixing_stabilized": "pass",
        "complete_coordinate_parent": False,
        "physical_closure": False,
        "status": "affine_family_coordinate_skeleton_pass_observed_algebra_open",
    },
    "next_gate": (
        "Keep A_SM=C+H+M3(C) as the coordinate algebra and test whether the affine "
        "family KO6 chain can be realized as a graded correspondence inside its "
        "commutant on the same 300-state module. Compute the resulting one-forms, "
        "gauge group and scalar kinetic normalization before repeating the "
        "unit-momentum test."
    ),
}

OUTPUT.write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))