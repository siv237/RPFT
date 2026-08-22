#!/usr/bin/env python3
"""Полный высокоугловой хвост калиброванного тензорного вихря."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.linalg import eigh


ROOT = Path(__file__).resolve().parents[2]
CALIBRATION_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate.py"
CALIBRATION_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_high_angular_coercivity_gate_results.json"


def algebraic_block_minimum(module, model, prepared, character, label):
    row = module["block_spectrum"](
        model, prepared, character, label, eigen_count=1
    )
    assembly = module["LAST_ASSEMBLY"]
    hessian = assembly["hessian"].toarray()
    metric = assembly["metric"].toarray()
    values = eigh(
        hessian, metric, subset_by_index=[0, 1],
        eigvals_only=True, check_finite=False, driver="gvx",
    )
    return {
        "lowest_algebraic_eigenvalue": float(values[0]),
        "second_algebraic_eigenvalue": float(values[1]),
        "hermiticity_residual": row["hermiticity_residual"],
    }


def analytic_row_polynomials(module, model, prepared, epsilon):
    z_value, g_value = module["Z"], module["G"]
    polynomials = []
    hermiticity_residual = 0.0

    for character in [-1, 0, 1]:
        matter_basis, _ = module["sector_basis"](
            model["representation"][0], character
        )
        gauge_basis, gauge_weights = module["sector_basis"](
            model["adjoint"][0], character
        )
        gauge_weight = int(gauge_weights[0])
        gauge_direction = gauge_basis[:, 0]
        r_zero = (
            matter_basis.conj().T
            @ model["representation"][0]
            @ matter_basis
        )
        gauge_generator = sum(
            gauge_direction[index] * model["representation"][index]
            for index in range(3)
        )
        gauge_matrix = sum(
            gauge_direction[index] * model["h"][index]
            for index in range(3)
        )
        bracket = (
            gauge_matrix.conj().T @ gauge_matrix
            - gauge_matrix @ gauge_matrix.conj().T
        )
        bracket_coefficient = (
            np.einsum("ij,ij->", model["h"][0], bracket)
            / np.einsum("ij,ij->", model["h"][0], model["h"][0])
        )

        def lower_matrix(data, signed_label):
            radius = data["middle"]
            k_value, kp = data["k"], data["kp"]
            point, point_prime = data["point"], data["point_prime"]
            orbit = matter_basis.conj().T @ (gauge_generator @ point)
            radial_cross = (
                matter_basis.conj().T
                @ gauge_generator.conj().T
                @ point_prime
            )
            angular_background = (
                (1.0 - k_value)
                * model["representation"][0]
                @ point / radius
            )
            angular_cross = (
                matter_basis.conj().T
                @ gauge_generator.conj().T
                @ angular_background
            )
            mu = signed_label - gauge_weight / 3.0
            angular_operator = (
                1j * mu * np.eye(4) + (1.0 - k_value) * r_zero
            )
            coefficients = np.zeros((4, 6), dtype=complex)
            coefficients[:, :4] = angular_operator
            coefficients[:, 5] = radius * orbit
            matrix = (
                (z_value / radius)
                * coefficients.conj().T @ coefficients
            )
            potential_sector = (
                matter_basis.conj().T
                @ data["potential_hessian"]
                @ matter_basis
            )
            matrix[:4, :4] += radius * potential_sector
            matrix[:4, 4] += z_value * radius * radial_cross
            matrix[4, :4] += z_value * radius * radial_cross.conj()
            matrix[:4, 5] += z_value * radius * angular_cross
            matrix[5, :4] += z_value * radius * angular_cross.conj()

            # Полярная тождественная оценка Ходжа даёт для двух компонент
            # связности барьер (|j|-1)^2/r. Половина сохраняется, а источник
            # фоновой калибровки ограничивается неравенством Юнга.
            vector_barrier = (
                epsilon * g_value
                * (abs(signed_label) - 1.0) ** 2 / radius
            )
            matrix[4, 4] += vector_barrier
            matrix[5, 5] += vector_barrier
            source = np.zeros(6, dtype=complex)
            source[:4] = (z_value / g_value) * orbit.conj()
            matrix -= (
                epsilon / (1.0 - epsilon) * g_value * radius
                * np.outer(source.conj(), source)
            )

            gauge_cross = g_value * (-kp) * bracket_coefficient
            matrix[4, 5] += gauge_cross
            matrix[5, 4] += gauge_cross.conjugate()
            normalization = np.diag(
                1.0 / np.sqrt(
                    np.array([z_value] * 4 + [g_value, g_value]) * radius
                )
            )
            normalized = normalization @ matrix @ normalization
            nonlocal hermiticity_residual
            hermiticity_residual = max(
                hermiticity_residual,
                float(np.linalg.norm(normalized - normalized.conj().T)),
            )
            return normalized

        for sign in [-1, 1]:
            for data in prepared[1]:
                constant_matrix = lower_matrix(data, 0)
                value_one = lower_matrix(data, sign)
                value_two = lower_matrix(data, 2 * sign)
                quadratic_matrix = (
                    value_two - 2.0 * value_one + constant_matrix
                ) / 2.0
                linear_matrix = value_one - constant_matrix - quadratic_matrix
                for row in range(6):
                    off_diagonal = [
                        column for column in range(6) if column != row
                    ]
                    quadratic = float(
                        np.real(quadratic_matrix[row, row])
                        - sum(
                            abs(quadratic_matrix[row, column])
                            for column in off_diagonal
                        )
                    )
                    linear = float(
                        np.real(linear_matrix[row, row])
                        - sum(
                            abs(linear_matrix[row, column])
                            for column in off_diagonal
                        )
                    )
                    constant = float(
                        np.real(constant_matrix[row, row])
                        - sum(
                            abs(constant_matrix[row, column])
                            for column in off_diagonal
                        )
                    )
                    polynomials.append({
                        "quadratic": quadratic,
                        "linear": linear,
                        "constant": constant,
                        "character": character,
                        "sign": sign,
                        "row": row,
                        "radius": float(data["middle"]),
                    })
    return polynomials, hermiticity_residual


def polynomial_margin(polynomials, absolute_label):
    return min(
        row["quadratic"] * absolute_label**2
        + row["linear"] * absolute_label
        + row["constant"]
        for row in polynomials
    )


def polynomial_derivative(polynomials, absolute_label):
    return min(
        2.0 * row["quadratic"] * absolute_label + row["linear"]
        for row in polynomials
    )


def main() -> None:
    calibration_module = runpy.run_path(str(CALIBRATION_AUDIT))
    module = calibration_module["load_calibrated_module"]()
    model = module["setup_model"]()
    calibration = json.loads(CALIBRATION_RESULT.read_text(encoding="utf-8"))

    bridge_node_count = 80
    analytic_threshold = 140
    bridge_absolute_labels = list(range(4, analytic_threshold))
    bridge_labels = (
        list(range(-analytic_threshold + 1, -3))
        + bridge_absolute_labels
    )
    bridge_prepared = module["prepare_grid"](model, bridge_node_count)
    low_window = {
        str(label): {
            str(character): algebraic_block_minimum(
                module, model, bridge_prepared, character, label
            )
            for character in [-1, 0, 1]
        }
        for label in range(-3, 4)
    }
    direct_bridge = {}
    for label in bridge_labels:
        direct_bridge[str(label)] = {
            str(character): algebraic_block_minimum(
                module, model, bridge_prepared, character, label
            )
            for character in [-1, 0, 1]
        }

    minimum_by_absolute_label = {}
    for absolute_label in bridge_absolute_labels:
        rows = []
        for label in [-absolute_label, absolute_label]:
            for character in [-1, 0, 1]:
                rows.append(
                    direct_bridge[str(label)][str(character)][
                        "lowest_algebraic_eigenvalue"
                    ]
                )
        minimum_by_absolute_label[str(absolute_label)] = float(min(rows))
    bridge_values = np.array(list(minimum_by_absolute_label.values()))
    all_bridge_levels = [
        row["lowest_algebraic_eigenvalue"]
        for label in direct_bridge.values() for row in label.values()
    ]
    maximum_bridge_hermiticity = max(
        row["hermiticity_residual"]
        for label in direct_bridge.values() for row in label.values()
    )
    low_levels = [
        (row["lowest_algebraic_eigenvalue"], int(character), int(label))
        for label, characters in low_window.items()
        for character, row in characters.items()
    ]
    low_internal_levels = [
        item for item in low_levels
        if not (item[1] == 0 and abs(item[2]) == 1)
    ]

    analytic_node_count = 1600
    analytic_prepared = module["prepare_grid"](model, analytic_node_count)
    epsilon = 0.5
    polynomials, lower_hermiticity = analytic_row_polynomials(
        module, model, analytic_prepared, epsilon
    )
    minimum_quadratic = min(row["quadratic"] for row in polynomials)
    threshold_margin = polynomial_margin(polynomials, analytic_threshold)
    threshold_derivative = polynomial_derivative(
        polynomials, analytic_threshold
    )
    first_positive_threshold = next(
        label for label in range(4, analytic_threshold + 1)
        if polynomial_margin(polynomials, label) > 0.0
        and polynomial_derivative(polynomials, label) > 0.0
    )

    checked_window_minimum = calibration["continuum_diagnostics"][
        "minimum_checked_near_zero_level_at_N140"
    ]
    result = {
        "gate": "version6_bosonic_defect_full_tensor_high_angular_coercivity_gate",
        "calibrated_parent": {
            "gate": calibration["gate"],
            "checked_integer_label_window": [-3, 3],
            "translation_eigenvalue_limit": calibration[
                "continuum_diagnostics"
            ]["translation_eigenvalue_limit"],
            "minimum_near_zero_level_at_N140": checked_window_minimum,
        },
        "dense_low_window": {
            "radial_node_count": bridge_node_count,
            "integer_labels": [-3, 3],
            "characters": [-1, 0, 1],
            "spectra": low_window,
            "negative_mode_count": int(
                sum(value < -1.0e-8 for value, _, _ in low_levels)
            ),
            "translation_pair_levels": sorted(
                value for value, character, label in low_levels
                if character == 0 and abs(label) == 1
            ),
            "lowest_internal_level_after_translation_removal": {
                "value": float(min(low_internal_levels)[0]),
                "character": int(min(low_internal_levels)[1]),
                "integer_label": int(min(low_internal_levels)[2]),
            },
        },
        "direct_bridge": {
            "radial_node_count": bridge_node_count,
            "characters": [-1, 0, 1],
            "signed_integer_labels": [bridge_labels[0], bridge_labels[-1]],
            "absolute_integer_labels": [
                bridge_absolute_labels[0], bridge_absolute_labels[-1]
            ],
            "solver": "dense generalized Hermitian eigensolver for the algebraically lowest levels",
            "spectra": direct_bridge,
            "minimum_by_absolute_label": minimum_by_absolute_label,
            "global_minimum": float(min(all_bridge_levels)),
            "global_minimum_absolute_label": int(
                min(
                    minimum_by_absolute_label,
                    key=minimum_by_absolute_label.get,
                )
            ),
            "negative_mode_count": int(
                sum(value < -1.0e-8 for value in all_bridge_levels)
            ),
            "minimum_strictly_increases_with_absolute_label": bool(
                np.all(np.diff(bridge_values) > 0.0)
            ),
            "maximum_hermiticity_residual": float(maximum_bridge_hermiticity),
        },
        "analytic_tail": {
            "method": "metric-normalized six-row Gershgorin polynomials after a polar Hodge split and Young bound",
            "radial_element_count": len(analytic_prepared[1]),
            "characters": [-1, 0, 1],
            "signed_directions": [-1, 1],
            "epsilon": epsilon,
            "certified_threshold_absolute_integer_label": analytic_threshold,
            "first_sampled_positive_threshold": int(first_positive_threshold),
            "minimum_quadratic_coefficient": float(minimum_quadratic),
            "threshold_margin": float(threshold_margin),
            "threshold_margin_derivative": float(threshold_derivative),
            "maximum_lower_matrix_hermiticity_residual": float(lower_hermiticity),
            "all_integer_labels_at_or_above_threshold_coercive": True,
        },
        "global_full_tensor_operator": {
            "all_three_twisted_characters_covered": True,
            "all_integer_angular_labels_covered": True,
            "translation_pair_removed_from_internal_spectrum": True,
            "negative_internal_mode_found": False,
            "global_internal_gap_upper_identification": (
                "the calibrated low-window minimum is the translation discretization level; "
                "the positive internal gap requires removing that pair"
            ),
        },
        "verdict": {
            "full_tensor_high_angular_tail_closed": True,
            "straight_stationary_vortex_linearly_nonnegative": True,
            "strict_internal_gap_value_closed": False,
            "closed_loop_stability_checked": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_internal_gap_gate",
        },
    }

    assert result["direct_bridge"]["negative_mode_count"] == 0
    assert result["dense_low_window"]["negative_mode_count"] == 0
    assert result["dense_low_window"][
        "lowest_internal_level_after_translation_removal"
    ]["value"] > 3.0
    assert result["direct_bridge"][
        "minimum_strictly_increases_with_absolute_label"
    ]
    assert result["direct_bridge"]["global_minimum"] > 3.0
    assert minimum_quadratic > 0.0
    assert threshold_margin > 0.5
    assert threshold_derivative > 0.0
    assert lower_hermiticity < 1.0e-8
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()