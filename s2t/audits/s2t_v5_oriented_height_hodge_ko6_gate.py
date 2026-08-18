#!/usr/bin/env python3
"""Full-KO6 canonicity audit for the oriented height--Hodge action."""

import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_oriented_height_hodge_ko6_gate_results.json"
TOL = 1.0e-10


def block_diag(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        result[offset : offset + width, offset : offset + width] = block
        offset += width
    return result


def particle_dirac(X, phi):
    zero = np.zeros((3, 3), dtype=complex)
    Y = phi * np.eye(3)
    return np.block(
        [[zero, X.conj().T, zero], [X, zero, Y.conj().T], [zero, Y, zero]]
    )


def full_height(levels):
    particle = block_diag([value * np.eye(3) for value in levels])
    return block_diag([particle, -particle])


def algebra_representation(A, left, right):
    identity = np.eye(3)
    return block_diag(
        [
            left * identity,
            A,
            A,
            np.conj(left) * identity,
            np.conj(left) * identity,
            np.conj(right) * identity,
        ]
    )


def algebra_basis():
    basis = []
    for row in range(3):
        for column in range(3):
            A = np.zeros((3, 3))
            A[row, column] = 1.0
            basis.append((A, 0.0, 0.0))
    basis.extend(
        [
            (np.zeros((3, 3)), 1.0, 0.0),
            (np.zeros((3, 3)), 0.0, 1.0),
            (np.zeros((3, 3)), 0.0, 1.0j),
        ]
    )
    return basis


rng = np.random.default_rng(20260815)
X = rng.normal(size=(3, 3))
phi = 0.41 + 0.23j
Dp = particle_dirac(X, phi)
D = block_diag([Dp, Dp.conj()])

identity9 = np.eye(9)
zero9 = np.zeros((9, 9))
J_matrix = np.block([[zero9, identity9], [identity9, zero9]])
gamma_p = block_diag([np.eye(3), -np.eye(3), np.eye(3)])
gamma = block_diag([gamma_p, -gamma_p])

representations = [algebra_representation(*item) for item in algebra_basis()]
opposites = [J_matrix @ rep.conj() @ J_matrix for rep in representations]

candidates = {
    "coherent_chain": (-1, 0, 1),
    "middle_sink": (-1, 0, -1),
}

candidate_rows = {}
for name, levels in candidates.items():
    h = full_height(levels)
    P = np.eye(18) - h @ h
    ad_h_D = h @ D - D @ h
    oriented = 0.5 * (D + ad_h_D)
    curvature = oriented @ oriented.conj().T - oriented.conj().T @ oriented
    particle_middle = curvature[3:6, 3:6]
    selected_full_trace = float(np.trace(P @ curvature @ curvature).real)

    left_commutators = [np.linalg.norm(h @ rep - rep @ h) for rep in representations]
    right_commutators = [np.linalg.norm(h @ rep - rep @ h) for rep in opposites]
    proposed_first_order = []
    for left in representations:
        first = h @ left - left @ h
        for right in opposites:
            proposed_first_order.append(np.linalg.norm(first @ right - right @ first))

    target_difference = X @ X.T - abs(phi) ** 2 * np.eye(3)
    target_sum = X @ X.T + abs(phi) ** 2 * np.eye(3)
    expected = target_difference if name == "coherent_chain" else target_sum

    row = {
        "particle_levels": list(levels),
        "J_odd_residual": float(np.linalg.norm(J_matrix @ h.conj() @ J_matrix + h)),
        "grading_commutator_residual": float(np.linalg.norm(h @ gamma - gamma @ h)),
        "left_algebra_commutator_residual": max(left_commutators),
        "opposite_algebra_commutator_residual": max(right_commutators),
        "proposed_height_first_order_residual": max(proposed_first_order),
        "unit_gap_D_residual": float(np.linalg.norm(h @ ad_h_D - ad_h_D @ h - D)),
        "middle_projector_rank": int(np.linalg.matrix_rank(P, tol=TOL)),
        "middle_curvature_residual": float(np.linalg.norm(particle_middle - expected)),
        "middle_curvature_type": "A-B" if name == "coherent_chain" else "A+B",
        "selected_full_trace": selected_full_trace,
        "normalized_full_trace": selected_full_trace / 6.0,
        "expected_normalized_trace": float(np.trace(expected @ expected).real / 3.0),
    }
    for key, value in row.items():
        if key.endswith("residual"):
            assert value < TOL, (name, key, value)
    assert row["middle_projector_rank"] == 6
    assert abs(row["normalized_full_trace"] - row["expected_normalized_trace"]) < TOL
    candidate_rows[name] = row

assert not np.allclose(
    full_height(candidates["coherent_chain"]),
    full_height(candidates["middle_sink"]),
)
assert not np.allclose(
    full_height(candidates["coherent_chain"]),
    -full_height(candidates["middle_sink"]),
)

discrete_heights = []
for left, middle, right in itertools.product((-1, 0, 1), repeat=3):
    levels = (left, middle, right)
    if middle != 0 or abs(left) != 1 or abs(right) != 1:
        continue
    if abs(middle - left) != 1 or abs(right - middle) != 1:
        continue
    discrete_heights.append(levels)
assert len(discrete_heights) == 4

orbits = []
unused = set(discrete_heights)
while unused:
    item = unused.pop()
    orbit = {item, tuple(-value for value in item)}
    unused -= orbit
    orbits.append(sorted(orbit))
assert len(orbits) == 2

result = {
    "date": "2026-08-15",
    "gate": "version5_oriented_height_hodge_ko6_gate",
    "KO6_signs": {"J_squared": 1, "JD": "+DJ", "J_gamma": "-gamma_J"},
    "candidate_heights": candidate_rows,
    "height_classification": {
        "discrete_unit_gap_heights": [list(item) for item in discrete_heights],
        "global_sign_orbits": [[list(item) for item in orbit] for orbit in orbits],
        "inequivalent_orbit_count": len(orbits),
        "coherent_and_sink_both_survive": True,
    },
    "corrections_to_review": {
        "direct_sum_block_center_can_distinguish_nodes": True,
        "height_first_order_condition_is_trivial_for_block_scalar_h": True,
        "J_squared_plus_one_in_project_KO6": True,
        "nakajima_analogy_requires_oriented_quiver_as_input": True,
    },
    "trace_normalization": {
        "KO6_conjugate_copy_factor": 2,
        "full_middle_dimension": 6,
        "normalized_trace_matches_tau3": True,
        "independent_relative_weight_introduced": False,
    },
    "verdict": {
        "height_hodge_algebraic_identity": "pass",
        "coherent_height_KO6_compatibility": "pass",
        "full_trace_normalization": "pass",
        "height_uniqueness": "fail",
        "orientation_from_existing_KO6_data": "closed",
        "physical_closure": False,
    },
    "next_gate": "version5_twisted_family_automorphism_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))