#!/usr/bin/env python3
"""Проверка совместного вакуума квадрупольного и тетраэдрического порядков."""

from __future__ import annotations

import itertools
import json
import runpy
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate_results.json"
Q_AUDIT = ROOT / "s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py"
T_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py"
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
IDENTITY = np.eye(3)


def symmetric_traceless_basis() -> np.ndarray:
    xy = np.zeros((3, 3))
    xy[0, 1] = xy[1, 0] = 1.0 / np.sqrt(2.0)
    xz = np.zeros((3, 3))
    xz[0, 2] = xz[2, 0] = 1.0 / np.sqrt(2.0)
    yz = np.zeros((3, 3))
    yz[1, 2] = yz[2, 1] = 1.0 / np.sqrt(2.0)
    return np.array(
        [
            np.diag([2.0, -1.0, -1.0]) / np.sqrt(6.0),
            np.diag([0.0, 1.0, -1.0]) / np.sqrt(2.0),
            xy,
            xz,
            yz,
        ]
    )


def tetrahedral_axes() -> np.ndarray:
    return np.array(
        [[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]]
    ) / np.sqrt(3.0)


def finite_hessian(function, point: np.ndarray, step: float = 5.0e-5) -> np.ndarray:
    dimension = len(point)
    hessian = np.zeros((dimension, dimension))
    centre = function(point)
    for first in range(dimension):
        unit_first = np.zeros(dimension)
        unit_first[first] = step
        hessian[first, first] = (
            function(point + unit_first) + function(point - unit_first) - 2.0 * centre
        ) / step**2
        for second in range(first + 1, dimension):
            unit_second = np.zeros(dimension)
            unit_second[second] = step
            value = (
                function(point + unit_first + unit_second)
                - function(point + unit_first - unit_second)
                - function(point - unit_first + unit_second)
                + function(point - unit_first - unit_second)
            ) / (4.0 * step**2)
            hessian[first, second] = value
            hessian[second, first] = value
    return hessian


def main() -> None:
    q_module = runpy.run_path(str(Q_AUDIT))
    t_module = runpy.run_path(str(T_AUDIT))
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]

    beta = float(thermal["critical_inverse_temperature"])
    ordered_spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    gap = float(ordered_spectrum[0] - ordered_spectrum[1])
    q_basis = symmetric_traceless_basis()
    t_basis, _ = t_module["symmetrized_traceless_rank_three_basis"]()
    axes = tetrahedral_axes()
    director = axes[0]
    projector_vacuum = np.outer(director, director)
    q_vacuum = gap * (projector_vacuum - IDENTITY / 3.0)
    t_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    q_coefficients = np.einsum("aij,ij->a", q_basis, q_vacuum)
    t_coefficients = np.einsum("aijk,ijk->a", t_basis, t_vacuum)
    point = np.concatenate([q_coefficients, t_coefficients])
    v_t_squared = float(np.sum(t_vacuum**2))
    alignment_scale = (8.0 / 9.0) ** 2

    ordered_matrix = IDENTITY / 3.0 + q_vacuum
    ordered_free_energy = q_module["free_energy"](ordered_matrix, beta)

    def unpack(value: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        q_value = np.einsum("a,aij->ij", value[:5], q_basis)
        t_value = np.einsum("a,aijk->ijk", value[5:], t_basis)
        return q_value, t_value

    def components(value: np.ndarray) -> tuple[float, float, float]:
        q_value, t_value = unpack(value)
        density = IDENTITY / 3.0 + q_value
        q_potential = q_module["free_energy"](density, beta) - ordered_free_energy
        moment = np.einsum("ikl,jkl->ij", t_value, t_value)
        tetrahedral_curvature = moment - v_t_squared * IDENTITY / 3.0
        t_potential = float(np.sum(tetrahedral_curvature**2) / 3.0)

        # P_Q is the projective readout of the ordered Q field.  Since T is
        # traceless, w_i=T_ijk P_jk also equals T_ijk Q_jk/Delta.
        projective_readout = IDENTITY / 3.0 + q_value / gap
        contraction = np.einsum("ijk,jk->i", t_value, projective_readout)
        mixed_curvature = np.outer(contraction, contraction) - alignment_scale * projective_readout
        mixed_potential = float(np.sum(mixed_curvature**2) / 3.0)
        return q_potential, t_potential, mixed_potential

    def total_potential(value: np.ndarray) -> float:
        return float(sum(components(value)))

    def uncoupled_potential(value: np.ndarray) -> float:
        q_value, t_value, _ = components(value)
        return float(q_value + t_value)

    vacuum_components = components(point)
    hessian = finite_hessian(total_potential, point)
    uncoupled_hessian = finite_hessian(uncoupled_potential, point)

    generators = t_module["so3_generators"]()
    gauge_tangents = []
    for generator in generators:
        q_variation = generator @ q_vacuum - q_vacuum @ generator
        t_variation = t_module["act_on_rank_three"](generator, t_vacuum)
        gauge_tangents.append(
            np.concatenate(
                [
                    np.einsum("aij,ij->a", q_basis, q_variation),
                    np.einsum("aijk,ijk->a", t_basis, t_variation),
                ]
            )
        )
    gauge_tangents = np.array(gauge_tangents).T
    gauge_rank = int(np.linalg.matrix_rank(gauge_tangents, tol=1.0e-10))
    complete_basis, _ = np.linalg.qr(gauge_tangents, mode="complete")
    physical_basis = complete_basis[:, gauge_rank:]
    physical_hessian = physical_basis.T @ hessian @ physical_basis
    physical_eigenvalues = np.linalg.eigvalsh(physical_hessian)
    full_eigenvalues = np.linalg.eigvalsh(hessian)
    uncoupled_eigenvalues = np.linalg.eigvalsh(uncoupled_hessian)
    normalized_gauge_tangents = complete_basis[:, :gauge_rank]

    q_variations = gauge_tangents[:5]
    t_variations = gauge_tangents[5:]
    q_mass = q_variations.T @ q_variations
    t_mass = t_variations.T @ t_variations
    combined_mass = q_mass + t_mass

    signed_axes = np.array(list(itertools.product([-1.0, 1.0], repeat=3))) / np.sqrt(3.0)
    alignment_zero_residuals = []
    for axis in signed_axes:
        projector = np.outer(axis, axis)
        contraction = np.einsum("ijk,jk->i", t_vacuum, projector)
        curvature = np.outer(contraction, contraction) - alignment_scale * projector
        alignment_zero_residuals.append(float(np.linalg.norm(curvature)))

    proper_rotations = []
    residual_rotations = []
    for permutation in itertools.permutations(range(4)):
        permutation_matrix = np.eye(4)[:, permutation]
        rotation = 0.75 * axes.T @ permutation_matrix @ axes
        if np.linalg.det(rotation) > 0.0:
            proper_rotations.append(rotation)
            if np.linalg.norm(rotation @ projector_vacuum @ rotation.T - projector_vacuum) < 1.0e-12:
                residual_rotations.append(rotation)

    isotropic_point = point.copy()
    isotropic_point[:5] = 0.0
    isotropic_components = components(isotropic_point)
    mixed_block_norm = float(np.linalg.norm(hessian[:5, 5:]))

    result = {
        "gate": "version6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate",
        "canonical_input": {
            "critical_inverse_temperature": beta,
            "ordered_density_spectrum": ordered_spectrum.tolist(),
            "projective_gap_Delta": gap,
            "tetrahedral_norm_squared": v_t_squared,
            "single_family_connection": True,
        },
        "mixed_parent_curvature": {
            "projective_readout": "P_Q=I3/3+Q/Delta",
            "composed_arrow": "w_i=T_ijk(P_Q)_jk=(T:Q)_i/Delta",
            "curvature": "F_QT=w w^T-(64/81)P_Q",
            "potential": "V_QT=Tr(F_QT^2)/3",
            "tetrahedral_contraction_residual": float(
                np.linalg.norm(np.einsum("ijk,jk->i", t_vacuum, projector_vacuum) - (8.0 / 9.0) * director)
            ),
            "vacuum_curvature_norm": float(np.sqrt(3.0 * vacuum_components[2])),
            "new_relative_weight_parameter_count": 0,
            "fixed_scale_origin": "(8/9)^2 from the canonical tetrahedral contraction",
            "mixed_hessian_block_frobenius_norm": mixed_block_norm,
        },
        "vacuum_selection": {
            "ordered_aligned_potential_components_Q_T_QT": list(vacuum_components),
            "ordered_aligned_total_potential": total_potential(point),
            "isotropic_Q_with_tetrahedral_T_components_Q_T_QT": list(isotropic_components),
            "isotropic_Q_with_tetrahedral_T_total_potential": total_potential(isotropic_point),
            "exact_isotropic_alignment_penalty": 4096.0 / 59049.0,
            "oriented_tetrahedral_axis_count": len(signed_axes),
            "projective_tetrahedral_axis_count": len(signed_axes) // 2,
            "maximum_enumerated_axis_curvature_residual": max(alignment_zero_residuals),
            "zero_locus_statement": "for canonical T, F_QT=0 implies |n1|=|n2|=|n3|=1/sqrt(3)",
        },
        "full_mixed_hessian": {
            "field_dimension": len(point),
            "uncoupled_eigenvalues": uncoupled_eigenvalues.tolist(),
            "uncoupled_zero_mode_count_tolerance_1e-5": int(np.sum(np.abs(uncoupled_eigenvalues) < 1.0e-5)),
            "coupled_eigenvalues": full_eigenvalues.tolist(),
            "coupled_zero_mode_count_tolerance_1e-5": int(np.sum(np.abs(full_eigenvalues) < 1.0e-5)),
            "gauge_orbit_rank": gauge_rank,
            "hessian_on_normalized_gauge_orbit_residual": float(np.linalg.norm(hessian @ normalized_gauge_tangents)),
            "physical_dimension_after_gauge_quotient": physical_hessian.shape[0],
            "physical_eigenvalues": physical_eigenvalues.tolist(),
            "physical_negative_mode_count_tolerance_1e-5": int(np.sum(physical_eigenvalues < -1.0e-5)),
            "physical_zero_mode_count_tolerance_1e-5": int(np.sum(np.abs(physical_eigenvalues) < 1.0e-5)),
            "physical_positive_mode_count_tolerance_1e-5": int(np.sum(physical_eigenvalues > 1.0e-5)),
        },
        "family_gauge_sector": {
            "Q_only_mass_eigenvalues": np.linalg.eigvalsh(q_mass).tolist(),
            "T_only_mass_eigenvalues": np.linalg.eigvalsh(t_mass).tolist(),
            "combined_mass_eigenvalues": np.linalg.eigvalsh(combined_mass).tolist(),
            "continuous_stabilizer_dimension": 3 - int(np.linalg.matrix_rank(combined_mass, tol=1.0e-10)),
            "tetrahedral_proper_rotation_count": len(proper_rotations),
            "aligned_residual_rotation_count": len(residual_rotations),
            "aligned_residual_discrete_group": "Z3",
            "vacuum_orbit": "SO(3)/Z3",
        },
        "literature_boundary": {
            "rank_two_and_rank_three_coupled_order_is_standard_in_general_landau_theory": True,
            "SO3_to_A4_by_spin_three_is_known": True,
            "specific_coefficient_free_mixed_curvature_is_project_construction": True,
            "observed_standard_model_matter_derived": False,
        },
        "verdict": {
            "coefficient_free_mixed_parent_square_passes": True,
            "ordered_Q_axis_is_locked_to_one_of_four_tetrahedral_projective_axes": True,
            "relative_orientation_zero_modes_lifted": True,
            "only_common_SO3_gauge_orbit_remains_zero": True,
            "full_physical_hessian_positive": bool(np.min(physical_eigenvalues) > 1.0e-5),
            "all_family_gauge_bosons_massive": bool(np.min(np.linalg.eigvalsh(combined_mass)) > 0.0),
            "residual_group_is_Z3": len(residual_rotations) == 3,
            "matter_birth_closed": False,
            "status": "coupled_Q_T_vacuum_Z3_and_physical_hessian_pass",
            "next_gate": "version6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate",
        },
    }

    assert max(abs(value) for value in vacuum_components) < 1.0e-12
    assert abs(total_potential(isotropic_point) - 4096.0 / 59049.0) < 1.0e-12
    assert result["full_mixed_hessian"]["uncoupled_zero_mode_count_tolerance_1e-5"] == 5
    assert result["full_mixed_hessian"]["coupled_zero_mode_count_tolerance_1e-5"] == 3
    assert result["full_mixed_hessian"]["physical_negative_mode_count_tolerance_1e-5"] == 0
    assert result["full_mixed_hessian"]["physical_zero_mode_count_tolerance_1e-5"] == 0
    assert result["full_mixed_hessian"]["physical_positive_mode_count_tolerance_1e-5"] == 9
    assert mixed_block_norm > 0.1
    assert max(alignment_zero_residuals) < 1.0e-12
    assert len(proper_rotations) == 12
    assert len(residual_rotations) == 3
    assert np.min(np.linalg.eigvalsh(combined_mass)) > 10.0

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()