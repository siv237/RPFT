#!/usr/bin/env python3
"""Identify the full defect connection with the existing family SO(3) bundle."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_family_connection_parent_identification_gate_results.json"
GAP = 0.8682499004685158


def load_nonradial_module():
    path = ROOT / "s2t/audits/s2t_v6_bosonic_defect_nonradial_stability_gate.py"
    specification = importlib.util.spec_from_file_location("nonradial", path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def so3_generators() -> list[np.ndarray]:
    generators = []
    for first, second in [(1, 2), (2, 0), (0, 1)]:
        generator = np.zeros((3, 3))
        generator[first, second] = -1.0
        generator[second, first] = 1.0
        generators.append(generator)
    return generators


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def induced_spin_two_representation(module, generators):
    basis = module.TENSOR_BASIS
    matrices = []
    reconstruction_residuals = []
    for generator in generators:
        matrix = np.array(
            [
                [
                    np.sum(left * commutator(generator, right))
                    for right in basis
                ]
                for left in basis
            ]
        )
        matrices.append(matrix)

    rng = np.random.default_rng(20260820)
    for _ in range(12):
        coefficients = rng.normal(size=5)
        connection = sum(value * generator for value, generator in zip(rng.normal(size=3), generators))
        order = np.einsum("a,amn->mn", coefficients, basis)
        direct = commutator(connection, order)
        connection_coefficients = np.array(
            [-0.5 * np.trace(generator @ connection) for generator in generators]
        )
        representation = sum(
            value * matrix for value, matrix in zip(connection_coefficients, matrices)
        )
        represented_coefficients = representation @ coefficients
        reconstructed = np.einsum("a,amn->mn", represented_coefficients, basis)
        reconstruction_residuals.append(float(np.linalg.norm(direct - reconstructed)))

    casimir = -sum(matrix @ matrix for matrix in matrices)
    return {
        "generator_matrices": [matrix.tolist() for matrix in matrices],
        "casimir_eigenvalues": np.linalg.eigvalsh(casimir).tolist(),
        "maximum_induced_connection_residual": max(reconstruction_residuals),
        "representation_dimension": 5,
        "spin": 2,
    }


def trace_normalization(generators):
    coefficients = np.array([0.37, -0.51, 0.29])
    curvature = sum(value * generator for value, generator in zip(coefficients, generators))
    curvature_square = curvature.T @ curvature
    trace_triplet = np.trace(curvature_square) / 3.0
    trace_h45 = np.trace(np.kron(curvature_square, np.eye(15))) / 45.0
    trace_doubled_h90 = np.trace(
        np.block(
            [
                [np.kron(curvature_square, np.eye(15)), np.zeros((45, 45))],
                [np.zeros((45, 45)), np.kron(curvature_square, np.eye(15))],
            ]
        )
    ) / 90.0
    return {
        "normalized_triplet_trace": float(trace_triplet),
        "normalized_H45_trace": float(trace_h45),
        "normalized_real_doubled_H90_trace": float(trace_doubled_h90),
        "H45_residual": float(abs(trace_h45 - trace_triplet)),
        "H90_residual": float(abs(trace_doubled_h90 - trace_triplet)),
        "independent_relative_weight_required": False,
    }


def anomaly_audit(generators):
    hermitian = [-1.0j * generator for generator in generators]
    cubic_residuals = []
    for first, second, third in itertools.product(range(3), repeat=3):
        value = np.trace(
            hermitian[first]
            @ (
                hermitian[second] @ hermitian[third]
                + hermitian[third] @ hermitian[second]
            )
        )
        cubic_residuals.append(abs(value))

    hypercharges = (
        [1.0 / 6.0] * 6
        + [-2.0 / 3.0] * 3
        + [1.0 / 3.0] * 3
        + [-1.0 / 2.0] * 2
        + [1.0]
    )
    hypercharge_sum = float(sum(hypercharges))
    conventional_twice_dynkin_index_j1 = 4
    global_parity = (15 * conventional_twice_dynkin_index_j1) % 2
    return {
        "left_handed_SM_channel_count": 15,
        "family_representation": "real SO(3) triplet, integer isospin j=1",
        "maximum_local_SO3_cubic_anomaly_residual": float(max(cubic_residuals)),
        "mixed_SO3_squared_U1_hypercharge_sum": hypercharge_sum,
        "mixed_SO3_squared_U1_anomaly": 2.0 * hypercharge_sum,
        "mixed_single_SO3_generator_anomalies": 0.0,
        "witten_mod_two_index": int(global_parity),
        "old_SU2_global_anomaly_present": bool(global_parity),
        "new_SU2_anomaly_applicable": False,
        "reason_new_anomaly_absent": "all family fermions have integer isospin j=1",
        "anomaly_audit_passes": max(cubic_residuals) < 1.0e-14 and abs(hypercharge_sum) < 1.0e-14 and global_parity == 0,
    }


def tetrahedral_mass_map(generators):
    axes = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ]
    ) / np.sqrt(3.0)
    tensor = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    director = axes[0]
    order = GAP * (np.outer(director, director) - np.eye(3) / 3.0)

    order_variations = [commutator(generator, order) for generator in generators]

    def tensor_variation(generator):
        return (
            np.einsum("ip,pjk->ijk", generator, tensor)
            + np.einsum("jp,ipk->ijk", generator, tensor)
            + np.einsum("kp,ijp->ijk", generator, tensor)
        )

    tensor_variations = [tensor_variation(generator) for generator in generators]
    order_gram = np.array(
        [[np.sum(left * right) for right in order_variations] for left in order_variations]
    )
    tensor_gram = np.array(
        [[np.sum(left * right) for right in tensor_variations] for left in tensor_variations]
    )
    total_gram = order_gram + tensor_gram
    return {
        "tetrahedral_tensor_norm_squared": float(np.sum(tensor**2)),
        "tetrahedral_trace_residual": float(np.linalg.norm(np.einsum("iik->k", tensor))),
        "Q_only_mass_eigenvalues": np.linalg.eigvalsh(order_gram).tolist(),
        "tetrahedral_mass_eigenvalues": np.linalg.eigvalsh(tensor_gram).tolist(),
        "combined_mass_eigenvalues": np.linalg.eigvalsh(total_gram).tolist(),
        "continuous_stabilizer_dimension_after_Q_only": 1,
        "continuous_stabilizer_dimension_after_Q_and_tetrahedral_tensor": int(
            3 - np.linalg.matrix_rank(total_gram, tol=1.0e-10)
        ),
        "residual_discrete_group_for_vertex_axis": "Z3",
    }


def main() -> None:
    module = load_nonradial_module()
    generators = so3_generators()
    induced = induced_spin_two_representation(module, generators)
    trace = trace_normalization(generators)
    anomalies = anomaly_audit(generators)
    tetrahedral = tetrahedral_mass_map(generators)

    result = {
        "gate": "version6_bosonic_defect_family_connection_parent_identification_gate",
        "single_bundle_identification": {
            "family_bundle": "E_fam with real rank-three fibre",
            "fermion_carrier": "E_fam tensor H15 = H45",
            "bosonic_order_parameter": "SymmetricTracelessSquare(E_fam)",
            "one_connection_induces_both_actions": True,
            "second_independent_SO3_connection_required": False,
            "induced_spin_two_audit": induced,
        },
        "parent_trace_restriction": trace,
        "anomaly_audit": anomalies,
        "tetrahedral_stabilizer_completion": tetrahedral,
        "binding_previous_no_go_results": {
            "M300_is_coordinate_algebra": False,
            "M300_can_normalize_a_preselected_embedded_family_connection": True,
            "ordinary_SM_one_forms_generate_family_connection": False,
            "spinor_Callias_carrier_from_20x15": False,
            "tetrahedral_tensor_potential_from_same_parent_trace": False,
        },
        "verdict": {
            "connection_identity_passes": True,
            "single_trace_normalization_passes": True,
            "local_and_global_anomaly_tests_pass": anomalies["anomaly_audit_passes"],
            "continuous_massless_stabilizer_removed_if_tetrahedral_condensate_is_active": True,
            "dynamical_localization_of_family_symmetry_derived": False,
            "tetrahedral_condensate_from_same_action_derived": False,
            "matter_birth_closed": False,
            "status": "representation_trace_anomaly_pass_dynamical_origin_open",
            "next_gate": "version6_bosonic_defect_tetrahedral_gauge_mass_parent_gate",
        },
    }

    assert induced["maximum_induced_connection_residual"] < 1.0e-12
    assert np.max(np.abs(np.array(induced["casimir_eigenvalues"]) - 6.0)) < 1.0e-12
    assert trace["H45_residual"] < 1.0e-14
    assert trace["H90_residual"] < 1.0e-14
    assert anomalies["anomaly_audit_passes"]
    assert tetrahedral["continuous_stabilizer_dimension_after_Q_and_tetrahedral_tensor"] == 0
    assert min(tetrahedral["combined_mass_eigenvalues"]) > 0.0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()