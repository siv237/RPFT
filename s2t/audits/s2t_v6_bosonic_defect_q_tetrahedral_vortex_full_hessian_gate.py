#!/usr/bin/env python3
"""Проверка определённости полного гессиана вихря Q+T+B.

Строится максимальный однозначно доступный осесимметричный оператор всех
пяти компонент Q, семи компонент T и угловой компоненты связности. Не
выведенная родителем относительная жёсткость Q сохраняется как Z_Q и
сканируется, а не фиксируется вручную.
"""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import ArpackNoConvergence, eigsh


ROOT = Path(__file__).resolve().parents[2]
PROFILE_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_defect_profile_gate.py"
COUPLED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate.py"
Q_AUDIT = ROOT / "s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py"
T_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py"
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_vortex_full_hessian_gate_results.json"


def main() -> None:
    profile_module = runpy.run_path(str(PROFILE_AUDIT))
    coupled_module = runpy.run_path(str(COUPLED_AUDIT))
    q_module = runpy.run_path(str(Q_AUDIT))
    t_module = runpy.run_path(str(T_AUDIT))
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]

    identity = np.eye(3)
    beta = float(thermal["critical_inverse_temperature"])
    spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    gap = float(spectrum[0] - spectrum[1])
    q_basis = coupled_module["symmetric_traceless_basis"]()
    t_basis, _ = t_module["symmetrized_traceless_rank_three_basis"]()
    axes = coupled_module["tetrahedral_axes"]()
    director = axes[0]
    q_vacuum = gap * (np.outer(director, director) - identity / 3.0)
    t_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    q_coefficients = np.einsum("aij,ij->a", q_basis, q_vacuum)
    t_vacuum_coefficients = np.einsum("aijk,ijk->a", t_basis, t_vacuum)
    v_t_squared = float(np.sum(t_vacuum**2))
    alignment_scale = (8.0 / 9.0) ** 2
    ordered_free_energy = q_module["free_energy"](identity / 3.0 + q_vacuum, beta)

    generator = np.array(
        [
            [0.0, -director[2], director[1]],
            [director[2], 0.0, -director[0]],
            [-director[1], director[0], 0.0],
        ]
    )

    def q_action(matrix):
        return generator @ matrix - matrix @ generator

    q_generator = np.array(
        [[np.sum(left * q_action(right)) for right in q_basis] for left in q_basis]
    )
    t_generator = np.array(
        [
            [np.sum(left * t_module["act_on_rank_three"](generator, right)) for right in t_basis]
            for left in t_basis
        ]
    )

    q_m2, q_rotation = np.linalg.eigh(-q_generator @ q_generator)
    t_m2, t_rotation = np.linalg.eigh(-t_generator @ t_generator)
    q_generator = q_rotation.T @ q_generator @ q_rotation
    t_generator = t_rotation.T @ t_generator @ t_rotation
    representation_rotation = block_diag(q_rotation, t_rotation)

    # Разложение T*=T0+T3 получается проектированием на ядро генератора.
    t0_coefficients = t_rotation @ (
        (np.abs(t_m2) < 1.0e-10).astype(float) * (t_rotation.T @ t_vacuum_coefficients)
    )
    t3_coefficients = t_vacuum_coefficients - t0_coefficients
    decomposition = {
        "T0_norm_squared": float(np.dot(t0_coefficients, t0_coefficients)),
        "T3_norm_squared": float(np.dot(t3_coefficients, t3_coefficients)),
        "orthogonality_residual": float(abs(np.dot(t0_coefficients, t3_coefficients))),
    }

    def unpack_old(value):
        q_value = np.einsum("a,aij->ij", value[:5], q_basis)
        t_value = np.einsum("a,aijk->ijk", value[5:], t_basis)
        return q_value, t_value

    def potential_old(value):
        q_value, t_value = unpack_old(value)
        density = identity / 3.0 + q_value
        q_potential = q_module["free_energy"](density, beta) - ordered_free_energy
        moment = np.einsum("ikl,jkl->ij", t_value, t_value)
        tetrahedral_curvature = moment - v_t_squared * identity / 3.0
        t_potential = float(np.sum(tetrahedral_curvature**2) / 3.0)
        projective_readout = identity / 3.0 + q_value / gap
        contraction = np.einsum("ijk,jk->i", t_value, projective_readout)
        mixed_curvature = np.outer(contraction, contraction) - alignment_scale * projective_readout
        mixed_potential = float(np.sum(mixed_curvature**2) / 3.0)
        return q_potential + t_potential + mixed_potential

    solution = profile_module["solve_profile"]()
    G = float(profile_module["G"])
    node_count = 150
    coordinate = np.linspace(0.0, 1.0, node_count)
    radius = 1.0e-4 + (20.0 - 1.0e-4) * coordinate**1.3

    midpoint_data = []
    local_minima = []
    for element in range(node_count - 1):
        middle = 0.5 * (radius[element] + radius[element + 1])
        k, a, b = solution.sol(middle)[[0, 2, 4]]
        t_background_old = b * t0_coefficients + a * t3_coefficients
        point_old = np.concatenate([q_coefficients, t_background_old])
        potential_hessian_old = coupled_module["finite_hessian"](potential_old, point_old, step=4.0e-5)
        potential_hessian = representation_rotation.T @ potential_hessian_old @ representation_rotation
        point = representation_rotation.T @ point_old
        local_minima.append(float(np.min(np.linalg.eigvalsh(potential_hessian))))
        midpoint_data.append((middle, k, point, potential_hessian))

    def spectrum_for_q_stiffness(z_q: float):
        field_count = 13
        dimension = field_count * node_count
        hessian = lil_matrix((dimension, dimension))
        metric = lil_matrix((dimension, dimension))
        kinetic_weights = np.array([z_q] * 5 + [1.0] * 7 + [G])

        h0 = block_diag(
            z_q * (-q_generator @ q_generator),
            -t_generator @ t_generator,
        )
        for element, (middle, k, point, potential_hessian) in enumerate(midpoint_data):
            width = radius[element + 1] - radius[element]
            derivative = np.array([[1.0, -1.0], [-1.0, 1.0]]) / width
            mass = width * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
            c = (1.0 - k) / 3.0
            local = np.zeros((field_count, field_count))
            local[:12, :12] = potential_hessian + c * c * h0 / middle**2
            local[12, 12] = float(point @ h0 @ point) / (9.0 * middle**2)
            local[12, :12] = local[:12, 12] = -2.0 * c * (h0 @ point) / (3.0 * middle**2)

            for first in range(field_count):
                for second in range(field_count):
                    coefficient = middle * local[first, second]
                    if coefficient == 0.0:
                        continue
                    first_indices = [first * node_count + element, first * node_count + element + 1]
                    second_indices = [second * node_count + element, second * node_count + element + 1]
                    for i in range(2):
                        for j in range(2):
                            hessian[first_indices[i], second_indices[j]] += coefficient * mass[i, j]

            for field in range(field_count):
                indices = [field * node_count + element, field * node_count + element + 1]
                if field < 12:
                    stiffness = kinetic_weights[field] * middle
                    weight = kinetic_weights[field] * middle
                else:
                    stiffness = G / middle
                    weight = G / middle
                for i in range(2):
                    for j in range(2):
                        hessian[indices[i], indices[j]] += stiffness * derivative[i, j]
                        metric[indices[i], indices[j]] += weight * mass[i, j]

        fixed = set()
        # Внешняя граница фиксирует вакуум для всех компонент.
        for field in range(field_count):
            fixed.add((field + 1) * node_count - 1)
        # В ядре ненулевые угловые веса и вариация K обращаются в нуль.
        for field, m2 in enumerate(np.concatenate([q_m2, t_m2])):
            if m2 > 1.0e-8:
                fixed.add(field * node_count)
        fixed.add(12 * node_count)
        keep = np.array([index for index in range(dimension) if index not in fixed])
        hessian = hessian.tocsr()[keep][:, keep]
        metric = metric.tocsr()[keep][:, keep]
        try:
            values = eigsh(
                hessian, k=6, M=metric, which="SA", ncv=48,
                return_eigenvectors=False, tol=2.0e-6, maxiter=8000,
            )
        except ArpackNoConvergence as error:
            if len(error.eigenvalues) < 4:
                raise
            values = error.eigenvalues
        values = np.sort(values)
        return values

    stiffness_scan = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    spectra = {str(value): spectrum_for_q_stiffness(value).tolist() for value in stiffness_scan}
    minima = {value: rows[0] for value, rows in spectra.items()}

    result = {
        "gate": "version6_bosonic_defect_q_tetrahedral_vortex_full_hessian_gate",
        "operator_ledger": {
            "field_components": {"Q_spin2": 5, "T_spin3": 7, "angular_family_connection": 1},
            "potential_Q_T_QT_fixed": True,
            "T_spatial_kinetic_norm_fixed_by_conditioned_parent_trace": True,
            "family_curvature_coefficient_G": G,
            "Q_relative_spatial_stiffness_Z_Q_derived": False,
            "Q_relative_spatial_stiffness_symbol": "Z_Q",
            "full_time_kinetic_metric_derived": False,
        },
        "representation": {
            "Q_angular_weight_squares": q_m2.tolist(),
            "T_angular_weight_squares": t_m2.tolist(),
            "profile_decomposition": decomposition,
        },
        "local_potential": {
            "minimum_hessian_eigenvalue_on_profile": float(min(local_minima)),
            "maximum_hessian_eigenvalue_minimum_on_profile": float(max(local_minima)),
            "sample_count": len(local_minima),
        },
        "maximal_unambiguous_radial_family": {
            "node_count": node_count,
            "Q_stiffness_scan": stiffness_scan,
            "lowest_eigenvalues": spectra,
            "minimum_by_stiffness": minima,
            "negative_mode_found_in_scan": bool(any(value < -1.0e-5 for value in minima.values())),
        },
        "boundary": {
            "all_internal_Q_and_T_components_in_corotating_radial_sector_checked": True,
            "all_transverse_nonabelian_connection_components_checked": False,
            "all_nonaxisymmetric_angular_sectors_checked": False,
            "unique_full_hessian_defined_by_parent": False,
            "closed_loop_stability_checked": False,
            "hopf_identification_checked": False,
        },
        "verdict": {
            "full_hessian_gate_well_posed_without_new_weight": False,
            "reason": "the parent does not derive the relative spatial stiffness Z_Q or the complete time-kinetic metric",
            "scanned_internal_radial_family_has_negative_mode": bool(any(value < -1.0e-5 for value in minima.values())),
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_q_stiffness_parent_normalization_gate",
        },
    }

    assert abs(decomposition["T0_norm_squared"] - 160.0 / 81.0) < 1.0e-10
    assert abs(decomposition["T3_norm_squared"] - 128.0 / 81.0) < 1.0e-10
    assert decomposition["orthogonality_residual"] < 1.0e-10
    assert not result["operator_ledger"]["Q_relative_spatial_stiffness_Z_Q_derived"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()