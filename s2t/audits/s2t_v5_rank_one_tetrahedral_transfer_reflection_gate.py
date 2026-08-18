#!/usr/bin/env python3
"""Проверка, задают ли проектор и тетраэдрическая голономия монету переноса."""

import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import expm, null_space


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_rank_one_tetrahedral_transfer_reflection_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


transfer = load_result("s2t_v5_local_defect_transfer_operator_gate_results.json")
holonomy = load_result("s2t_v4_family_defect_holonomy_realization_gate_results.json")
assert transfer["verdict"]["unique_nonzero_mass_from_current_geometry"] == "fail"
assert holonomy["exact_checks"]["branch_count"] == 8
assert holonomy["exact_checks"]["maximum_holonomy_residual"] < 1e-12


def permutation_sign(p):
    inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


epsilon = np.zeros((4, 4, 4, 4), dtype=float)
for perm in itertools.permutations(range(4)):
    epsilon[perm] = permutation_sign(perm)

u = np.ones(4) / 2
rows = []
max_residuals = {
    "omega_square": 0.0,
    "omega_antisymmetry": 0.0,
    "householder_transverse_scalar": 0.0,
    "holonomy_transverse_reconstruction": 0.0,
}

for fixed_point in range(4):
    e = np.zeros(4)
    e[fixed_point] = 1.0
    projector = np.outer(e, e)
    h = (2 / np.sqrt(3)) * (e - np.ones(4) / 4)
    omega = np.einsum("bcde,d,e->bc", epsilon, u, h)
    transverse_projector = np.eye(4) - np.outer(u, u) - np.outer(h, h)
    transverse_basis = null_space(np.vstack([u, h]))
    omega_2 = transverse_basis.T @ omega @ transverse_basis
    householder = 2 * projector - np.eye(4)
    householder_2 = transverse_basis.T @ householder @ transverse_basis

    max_residuals["omega_square"] = max(
        max_residuals["omega_square"],
        float(np.linalg.norm(omega @ omega + transverse_projector)),
    )
    max_residuals["omega_antisymmetry"] = max(
        max_residuals["omega_antisymmetry"],
        float(np.linalg.norm(omega.T + omega)),
    )
    max_residuals["householder_transverse_scalar"] = max(
        max_residuals["householder_transverse_scalar"],
        float(np.linalg.norm(householder_2 + np.eye(2))),
    )

    for winding in (+1, -1):
        angle = winding * 2 * np.pi / 3
        hol = expm(-angle * omega)
        hol_2 = transverse_basis.T @ hol @ transverse_basis
        reconstructed = np.cos(angle) * np.eye(2) - np.sin(angle) * omega_2
        residual = float(np.linalg.norm(hol_2 - reconstructed))
        max_residuals["holonomy_transverse_reconstruction"] = max(
            max_residuals["holonomy_transverse_reconstruction"], residual
        )
        rows.append(
            {
                "fixed_point": fixed_point,
                "winding": winding,
                "omega_2": omega_2.tolist(),
                "householder_on_transverse_plane": householder_2.tolist(),
                "holonomy_2": hol_2.tolist(),
                "holonomy_eigenphases": sorted(
                    [float(np.angle(value)) for value in np.linalg.eigvals(hol_2)]
                ),
                "reconstruction_residual": residual,
            }
        )

assert max(max_residuals.values()) < 1e-12

# На ориентированной двумерной плоскости все отражения, меняющие знак
# комплексной структуры, образуют окружность R(alpha).
alpha = sp.symbols("alpha", real=True)
J = sp.Matrix([[0, -1], [1, 0]])
R_alpha = sp.Matrix(
    [
        [sp.cos(2 * alpha), sp.sin(2 * alpha)],
        [sp.sin(2 * alpha), -sp.cos(2 * alpha)],
    ]
)
assert sp.simplify(R_alpha**2) == sp.eye(2)
assert sp.simplify(R_alpha * J * R_alpha + J) == sp.zeros(2)
assert sp.simplify(R_alpha.det()) == -1

phi = 2 * sp.pi / 3
C3 = sp.cos(phi) * sp.eye(2) + sp.sin(phi) * J

# Линейная система: X должен одновременно коммутировать с C3 и менять знак J.
x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22", real=True)
X = sp.Matrix([[x11, x12], [x21, x22]])
equations = list(X * C3 - C3 * X) + list(X * J + J * X)
coefficient_matrix, rhs = sp.linear_eq_to_matrix(equations, [x11, x12, x21, x22])
intersection_rank = int(coefficient_matrix.rank())
intersection_nullity = 4 - intersection_rank
assert intersection_nullity == 0

# Три отражения стабилизатора S3 циклически переставляются трёхциклом;
# ни одно не выделено, а их среднее равно нулю.
reflection_angles = [0, sp.pi / 3, 2 * sp.pi / 3]
reflections = [sp.simplify(R_alpha.subs(alpha, value)) for value in reflection_angles]
reflection_average = sp.simplify(sum(reflections, sp.zeros(2)) / 3)
assert reflection_average == sp.zeros(2)

conjugation_residuals = []
for idx, reflection in enumerate(reflections):
    conjugated = sp.simplify(C3 * reflection * C3.T)
    distances = [sp.simplify(conjugated - candidate) for candidate in reflections]
    matching = [j for j, defect in enumerate(distances) if defect == sp.zeros(2)]
    assert len(matching) == 1
    conjugation_residuals.append({"from": idx, "to": matching[0]})

# Алгебра, порождённая проектором и ориентированной голономией, на
# поперечной плоскости имеет только I и J; она не содержит отражения.
canonical_generators = [sp.eye(2), J, C3, C3**2]
generator_columns = [sp.Matrix(generator).reshape(4, 1) for generator in canonical_generators]
canonical_algebra_rank = int(sp.Matrix.hstack(*generator_columns).rank())
assert canonical_algebra_rank == 2

# Если отражение выбрать дополнительно, локальная плотность голономии
# действительно может быть превращена в дираковскую монету, но результат
# зависит от выбранной поляризации.
a, length = sp.symbols("a L", positive=True, real=True)
theta_step = 2 * sp.pi * a / (3 * length)
mass_amplitude = sp.sin(theta_step)
propagation_amplitude = sp.cos(theta_step)
continuum_mass = sp.limit(mass_amplitude / a, a, 0)
assert continuum_mass == 2 * sp.pi / (3 * length)

result = {
    "gate": "version5_rank_one_tetrahedral_transfer_reflection_gate",
    "input_certificates": {
        "minimal_transfer_has_one_free_mass_modulus": True,
        "rank_one_projector_holonomy_exact_for_eight_branches": True,
        "holonomy_angle": "2*pi/3",
    },
    "projector_holonomy_geometry": {
        "u": u.tolist(),
        "transverse_plane": "orthogonal complement of the affine singlet u and selected axis h_a",
        "orientation_generator_identity": "Omega^2=-P_transverse",
        "maximum_residuals": max_residuals,
        "transverse_holonomy_eigenvalues": ["exp(+2*pi*i/3)", "exp(-2*pi*i/3)"],
        "projector_involution_on_transverse_plane": "(2P_a-I)|_T=-I_T",
        "projector_involution_exchanges_chiral_lines": False,
    },
    "reflection_classification": {
        "general_reflection": "R(alpha)=[[cos(2alpha),sin(2alpha)],[sin(2alpha),-cos(2alpha)]]",
        "parameter_space": "alpha modulo pi",
        "R_squared": "I",
        "R_J_R": "-J",
        "det_R": -1,
        "C3_invariant_reflection_linear_intersection_dimension": intersection_nullity,
        "stabilizer_reflection_count": 3,
        "stabilizer_reflection_angles": ["0", "pi/3", "2*pi/3"],
        "C3_conjugation_permutation": conjugation_residuals,
        "average_of_three_reflections": [[str(x) for x in row] for row in reflection_average.tolist()],
        "unique_reflection_selected": False,
    },
    "canonical_operator_algebra": {
        "generators_on_transverse_plane": ["I", "J", "C3", "C3^2"],
        "real_linear_rank": canonical_algebra_rank,
        "algebra": "span_R{I,J}",
        "all_elements_commute_with_J": True,
        "contains_chirality_exchanging_reflection": False,
    },
    "local_connection_candidate": {
        "connection_density": "2*pi/(3L)",
        "step_angle": str(theta_step),
        "candidate_if_reflection_is_added": {
            "n": str(propagation_amplitude),
            "m": str(mass_amplitude),
            "continuum_mass": str(continuum_mass),
        },
        "extra_choice": "one reflection/polarization R(alpha) identifying the transverse plane with left/right propagation",
        "functorial_from_projector_and_holonomy_alone": False,
    },
    "rows": rows,
    "verdict": {
        "projector_selects_transverse_plane": "pass",
        "winding_selects_holonomy_orientation": "pass",
        "holonomy_fixes_phase_density": "pass",
        "projector_involution_fixes_mass_reflection": "fail",
        "C3_holonomy_contains_unique_reflection": "fail",
        "unique_chiral_polarization": "fail",
        "mass_modulus_fixed_without_extra_choice": "fail",
        "minimal_dynamic_mass_route": "closed",
        "massless_holonomy_transport": "retained",
        "physical_closure": False,
        "status": "the projector and 2pi/3 holonomy canonically fix an oriented transverse complex structure and phase transport, but no reflection exchanging the two chiral directions; choosing such a reflection is an external polarization and is exactly the missing mass datum",
    },
    "next_gate": (
        "Stop using family holonomy as a mass selector. Keep the canonical massless "
        "transport and test its natural role instead: the spectrum and index of a "
        "massless triplet transported around the existing C3 holonomy. The decisive "
        "question is whether the invariant holonomy line gives one parameter-free "
        "zero mode while the conjugate branches acquire fixed one-third momentum shifts."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))