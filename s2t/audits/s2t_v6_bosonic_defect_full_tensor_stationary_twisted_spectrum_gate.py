#!/usr/bin/env python3
"""Скрученный спектр полного Q+T+B гессиана на стационарном фоне."""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[2]
COUPLED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate.py"
T_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py"
Q_AUDIT = ROOT / "s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py"
STATIONARY_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_full_tensor_stationary_background_gate.py"
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate_results.json"

Z = 1.0 / 3.0
G = 2.0 / 27.0


def residue(weight: int) -> int:
    value = weight % 3
    return -1 if value == 2 else value


def setup_model():
    coupled = runpy.run_path(str(COUPLED_AUDIT))
    t_module = runpy.run_path(str(T_AUDIT))
    q_module = runpy.run_path(str(Q_AUDIT))
    stationary = runpy.run_path(str(STATIONARY_AUDIT))
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]
    reduced = stationary["setup_reduction"]()
    solution, _, _ = stationary["solve_full_profile"](reduced)

    q_basis = coupled["symmetric_traceless_basis"]()
    t_basis, _ = t_module["symmetrized_traceless_rank_three_basis"]()
    axes = coupled["tetrahedral_axes"]()
    director = axes[0]
    identity = np.eye(3)
    transverse_one = np.array([1.0, -1.0, 0.0]) / np.sqrt(2.0)
    transverse_two = np.cross(director, transverse_one)
    frame = np.array([director, transverse_one, transverse_two])

    def cross_generator(vector):
        x, y, z = vector
        return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])

    h = np.array([cross_generator(vector) / 3.0 for vector in frame])

    def q_action(generator, value):
        return generator @ value - value @ generator

    def representation_matrix(generator):
        q_part = np.array([
            [np.sum(left * q_action(generator, right)) for right in q_basis]
            for left in q_basis
        ])
        t_part = np.array([
            [np.sum(left * t_module["act_on_rank_three"](generator, right)) for right in t_basis]
            for left in t_basis
        ])
        result = np.zeros((12, 12))
        result[:5, :5] = q_part
        result[5:, 5:] = t_part
        return result

    representation = np.array([representation_matrix(generator) for generator in h])
    gram = np.einsum("aij,bij->ab", h, h)
    adjoint = np.zeros((3, 3, 3))
    for a in range(3):
        for b in range(3):
            bracket = h[a] @ h[b] - h[b] @ h[a]
            adjoint[a, :, b] = np.linalg.solve(gram, np.einsum("cij,ij->c", h, bracket))

    beta = float(thermal["critical_inverse_temperature"])
    ordered_spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    gap = float(ordered_spectrum[0] - ordered_spectrum[1])
    q_vacuum = gap * (np.outer(director, director) - identity / 3.0)
    t_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    v_t_squared = float(np.sum(t_vacuum**2))
    alignment_scale = (8.0 / 9.0) ** 2
    ordered_free_energy = q_module["free_energy"](identity / 3.0 + q_vacuum, beta)

    def unpack(value):
        q_value = np.einsum("a,aij->ij", value[:5], q_basis)
        t_value = np.einsum("a,aijk->ijk", value[5:], t_basis)
        return q_value, t_value

    def full_potential(value):
        q_value, t_value = unpack(value)
        density = identity / 3.0 + q_value
        q_potential = q_module["free_energy"](density, beta) - ordered_free_energy
        moment = np.einsum("ikl,jkl->ij", t_value, t_value)
        curvature_t = moment - v_t_squared * identity / 3.0
        projective_readout = identity / 3.0 + q_value / gap
        contraction = np.einsum("ijk,jk->i", t_value, projective_readout)
        curvature_qt = np.outer(contraction, contraction) - alignment_scale * projective_readout
        return float(q_potential + np.sum(curvature_t**2) / 3.0 + np.sum(curvature_qt**2) / 3.0)

    return {
        "coupled": coupled,
        "representation": representation,
        "adjoint": adjoint,
        "h": h,
        "solution": solution,
        "q_coefficients": reduced["q_coefficients"],
        "t_zero": reduced["t_zero"],
        "t_three": reduced["t_three"],
        "full_potential": full_potential,
    }


def sector_basis(generator, character):
    values, vectors = np.linalg.eigh(-1j * generator)
    weights = np.rint(3.0 * values).astype(int)
    chosen = [index for index, weight in enumerate(weights) if residue(int(weight)) == character]
    return vectors[:, chosen], weights[chosen]


def add_local(matrix, indices, local):
    for row, global_row in enumerate(indices):
        for column, global_column in enumerate(indices):
            value = local[row, column]
            if value != 0.0:
                matrix[global_row, global_column] += value


def add_square(matrix, indices, coefficients, weight):
    add_local(matrix, indices, weight * coefficients.conj().T @ coefficients)


def prepare_grid(model, node_count):
    coordinate = np.linspace(0.0, 1.0, node_count)
    radius = 1.0e-4 + (20.0 - 1.0e-4) * coordinate**1.35
    elements = []
    for element in range(node_count - 1):
        left, right = radius[element], radius[element + 1]
        width = right - left
        middle = 0.5 * (left + right)
        value = model["solution"].sol(middle)
        derivative = model["solution"].sol(middle, 1)
        k, kp, a, ap, b, bp, q, qp = value
        point = np.concatenate([
            q * model["q_coefficients"],
            b * model["t_zero"] + a * model["t_three"],
        ])
        point_prime = np.concatenate([
            qp * model["q_coefficients"],
            bp * model["t_zero"] + ap * model["t_three"],
        ])
        potential_hessian = model["coupled"]["finite_hessian"](
            model["full_potential"], point, step=4.0e-5
        )
        elements.append({
            "element": element, "middle": middle, "width": width,
            "k": k, "kp": kp, "point": point, "point_prime": point_prime,
            "potential_hessian": potential_hessian,
        })
    return radius, elements


def block_spectrum(model, prepared, character, integer_label, eigen_count=4):
    radius, elements = prepared
    node_count = len(radius)
    matter_basis, matter_weights = sector_basis(model["representation"][0], character)
    gauge_basis, gauge_weights = sector_basis(model["adjoint"][0], character)
    gauge_weight = int(gauge_weights[0])
    mu = integer_label - gauge_weight / 3.0
    harmonics = np.rint(integer_label + (matter_weights - gauge_weight) / 3.0).astype(int)
    r0 = matter_basis.conj().T @ model["representation"][0] @ matter_basis
    c0 = complex((gauge_basis.conj().T @ model["adjoint"][0] @ gauge_basis)[0, 0])
    gauge_direction = gauge_basis[:, 0]
    gauge_generator = sum(gauge_direction[a] * model["representation"][a] for a in range(3))
    gauge_matrix = sum(gauge_direction[a] * model["h"][a] for a in range(3))
    bracket = gauge_matrix.conj().T @ gauge_matrix - gauge_matrix @ gauge_matrix.conj().T
    bracket_coefficient = np.einsum("ij,ij->", model["h"][0], bracket) / np.einsum(
        "ij,ij->", model["h"][0], model["h"][0]
    )

    dimension = 6 * node_count
    hessian = lil_matrix((dimension, dimension), dtype=complex)
    metric = lil_matrix((dimension, dimension), dtype=complex)
    for data in elements:
        element = data["element"]
        middle, width = data["middle"], data["width"]
        k, kp = data["k"], data["kp"]
        point, point_prime = data["point"], data["point_prime"]
        average = np.array([0.5, 0.5])
        derivative = np.array([-1.0 / width, 1.0 / width])
        mass = width * np.array([[2.0, 1.0], [1.0, 2.0]]) / 6.0
        radial_mass = middle * mass
        local_indices = []
        for field in range(6):
            local_indices.extend([field * node_count + element, field * node_count + element + 1])

        orbit = gauge_generator @ point
        orbit_sector = matter_basis.conj().T @ orbit
        radial = np.zeros((4, 12), dtype=complex)
        angular = np.zeros((4, 12), dtype=complex)
        angular_operator = (1j * mu * np.eye(4) + (1.0 - k) * r0) / middle
        for component in range(4):
            radial[component, 2 * component:2 * component + 2] = derivative
            angular[:, 2 * component:2 * component + 2] = np.outer(
                angular_operator[:, component], average
            )
        radial[:, 8:10] = np.outer(orbit_sector, average)
        angular[:, 10:12] = np.outer(orbit_sector, average)
        add_square(hessian, local_indices, radial, Z * middle * width)
        add_square(hessian, local_indices, angular, Z * middle * width)

        radial_cross = matter_basis.conj().T @ gauge_generator.conj().T @ point_prime
        angular_background = (1.0 - k) * model["representation"][0] @ point / middle
        angular_cross = matter_basis.conj().T @ gauge_generator.conj().T @ angular_background
        cross = np.zeros((12, 12), dtype=complex)
        for component in range(4):
            block = Z * middle * mass * radial_cross[component]
            cross[2 * component:2 * component + 2, 8:10] += block
            cross[8:10, 2 * component:2 * component + 2] += block.conj().T
            block = Z * middle * mass * angular_cross[component]
            cross[2 * component:2 * component + 2, 10:12] += block
            cross[10:12, 2 * component:2 * component + 2] += block.conj().T
        add_local(hessian, local_indices, cross)

        potential_sector = matter_basis.conj().T @ data["potential_hessian"] @ matter_basis
        potential_local = np.zeros((12, 12), dtype=complex)
        for first in range(4):
            for second in range(4):
                potential_local[2 * first:2 * first + 2, 2 * second:2 * second + 2] = (
                    potential_sector[first, second] * radial_mass
                )
        add_local(hessian, local_indices, potential_local)

        gamma = 1j * mu + (1.0 - k) * c0
        curvature = np.zeros((1, 12), dtype=complex)
        curvature[0, 8:10] = -gamma * average / middle
        curvature[0, 10:12] = derivative + average / middle
        add_square(hessian, local_indices, curvature, G * middle * width)

        gauge_fixing = np.zeros((1, 12), dtype=complex)
        for component in range(4):
            gauge_fixing[0, 2 * component:2 * component + 2] = (
                -(Z / G) * orbit_sector[component].conjugate() * average
            )
        gauge_fixing[0, 8:10] = derivative + average / middle
        gauge_fixing[0, 10:12] = gamma * average / middle
        add_square(hessian, local_indices, gauge_fixing, G * middle * width)

        gauge_cross = G * (-kp / middle) * bracket_coefficient * middle * mass
        nonabelian = np.zeros((12, 12), dtype=complex)
        nonabelian[8:10, 10:12] = gauge_cross
        nonabelian[10:12, 8:10] = gauge_cross.conj().T
        add_local(hessian, local_indices, nonabelian)

        for field, coefficient in enumerate([Z, Z, Z, Z, G, G]):
            indices = [field * node_count + element, field * node_count + element + 1]
            add_local(metric, indices, coefficient * radial_mass)

    fixed = {(field + 1) * node_count - 1 for field in range(6)}
    eliminated = set()
    relations = {}
    for component, harmonic in enumerate(harmonics):
        if harmonic != 0:
            fixed.add(component * node_count)
    core_p, core_q = 4 * node_count, 5 * node_count
    if integer_label == 0:
        fixed.update([core_p, core_q])
    elif abs(integer_label) == 1:
        eliminated.add(core_q)
        relations[core_p] = [(core_p, 1.0), (core_q, 1j * np.sign(integer_label))]
    else:
        fixed.update([core_p, core_q])

    independent = [index for index in range(dimension) if index not in fixed and index not in eliminated]
    transformation = lil_matrix((dimension, len(independent)), dtype=complex)
    for column, index in enumerate(independent):
        if index in relations:
            for target, value in relations[index]:
                transformation[target, column] = value
        else:
            transformation[index, column] = 1.0
    transformation = transformation.tocsr()
    hessian = transformation.conj().T @ hessian.tocsr() @ transformation
    metric = transformation.conj().T @ metric.tocsr() @ transformation
    hermiticity = float(np.linalg.norm((hessian - hessian.conj().T).data))
    values = eigsh(
        hessian, k=eigen_count, M=metric, which="SA", tol=5.0e-7,
        maxiter=15000, ncv=max(36, 6 * eigen_count + 1), return_eigenvectors=False,
    )
    return {
        "eigenvalues": np.sort(np.real(values)).tolist(),
        "matter_weights": matter_weights.tolist(),
        "gauge_weight": gauge_weight,
        "laboratory_harmonics": harmonics.tolist(),
        "common_corotating_exponent": mu,
        "hermiticity_residual": hermiticity,
    }


def main() -> None:
    model = setup_model()
    node_counts = [70, 100, 140]
    characters = [-1, 0, 1]
    integer_labels = list(range(-3, 4))
    convergence = {}
    for nodes in node_counts:
        prepared = prepare_grid(model, nodes)
        convergence[str(nodes)] = {
            str(character): {
                str(label): block_spectrum(model, prepared, character, label)
                for label in integer_labels
            }
            for character in characters
        }

    refinement = {}
    refinement_blocks = [(1, -1), (1, -2), (0, 1), (0, 0)]
    for nodes in [200, 280]:
        prepared = prepare_grid(model, nodes)
        refinement[str(nodes)] = {
            f"{character}:{label}": block_spectrum(
                model, prepared, character, label
            )
            for character, label in refinement_blocks
        }

    finest = convergence[str(node_counts[-1])]
    levels = sorted(
        (finest[str(character)][str(label)]["eigenvalues"][0], character, label)
        for character in characters for label in integer_labels
    )
    translation = {
        str(nodes): convergence[str(nodes)]["0"]["1"]["eigenvalues"][0]
        for nodes in node_counts
    }
    conjugation_residual = max(
        abs(
            finest["1"][str(label)]["eigenvalues"][index]
            - finest["-1"][str(-label)]["eigenvalues"][index]
        )
        for label in integer_labels for index in range(4)
    )
    nontranslation = [row for row in levels if not (row[1] == 0 and abs(row[2]) == 1)]
    negative = [row for row in levels if row[0] < -1.0e-5]
    fit_nodes = np.array([140.0, 200.0, 280.0])
    inverse_square = 1.0 / (fit_nodes - 1.0) ** 2
    primary_values = np.array([
        convergence["140"]["1"]["-1"]["eigenvalues"][0],
        refinement["200"]["1:-1"]["eigenvalues"][0],
        refinement["280"]["1:-1"]["eigenvalues"][0],
    ])
    secondary_values = np.array([
        convergence["140"]["1"]["-2"]["eigenvalues"][0],
        refinement["200"]["1:-2"]["eigenvalues"][0],
        refinement["280"]["1:-2"]["eigenvalues"][0],
    ])
    translation_values = np.array([
        convergence["140"]["0"]["1"]["eigenvalues"][0],
        refinement["200"]["0:1"]["eigenvalues"][0],
        refinement["280"]["0:1"]["eigenvalues"][0],
    ])
    primary_limit = float(np.polyfit(inverse_square, primary_values, 1)[1])
    secondary_limit = float(np.polyfit(inverse_square, secondary_values, 1)[1])
    translation_limit = float(np.polyfit(inverse_square, translation_values, 1)[1])
    result = {
        "gate": "version6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate",
        "operator": {
            "stationary_four_profile_background": True,
            "characters": characters,
            "integer_labels": integer_labels,
            "complex_fields_per_block": 6,
            "background_gauge_fixing_included": True,
            "nonabelian_curvature_cross_term_included": True,
            "twisted_core_regularity_included": True,
        },
        "convergence": convergence,
        "targeted_refinement": refinement,
        "translation_candidate_character_0_label_1": translation,
        "finest_global_levels": [
            {"value": value, "character": character, "integer_label": label}
            for value, character, label in levels[:12]
        ],
        "finest_nontranslation_minimum": {
            "value": nontranslation[0][0],
            "character": nontranslation[0][1],
            "integer_label": nontranslation[0][2],
        },
        "symmetry_checks": {
            "maximum_conjugate_sector_eigenvalue_residual": conjugation_residual,
            "maximum_hermiticity_residual": max(
                row["hermiticity_residual"]
                for nodes in convergence.values() for character in nodes.values() for row in character.values()
            ),
        },
        "continuum_diagnostics": {
            "fit_node_counts": fit_nodes.astype(int).tolist(),
            "fit_variable": "1/(N-1)^2",
            "primary_twisted_candidate_limit": primary_limit,
            "secondary_twisted_candidate_limit": secondary_limit,
            "translation_candidate_limit": translation_limit,
            "primary_drift_200_to_280": float(abs(primary_values[-1] - primary_values[-2])),
            "secondary_drift_200_to_280": float(abs(secondary_values[-1] - secondary_values[-2])),
            "translation_drift_200_to_280": float(abs(translation_values[-1] - translation_values[-2])),
        },
        "verdict": {
            "negative_mode_count_in_checked_window": len(negative),
            "negative_mode_found_in_checked_window": bool(negative),
            "translation_pair_resolved": False,
            "negative_candidate_survives_targeted_refinement": bool(primary_values[-1] < -0.02),
            "physical_negative_mode_certified": False,
            "certification_blocker": "the same discretization still lifts the exact translation pair to a positive level",
            "full_checked_window_stable": not negative,
            "full_angular_tail_closed": False,
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_translation_calibration_gate",
        },
    }
    assert conjugation_residual < 1.0e-8
    assert result["symmetry_checks"]["maximum_hermiticity_residual"] < 1.0e-10
    assert primary_values[-1] < -0.02
    assert secondary_values[-1] < -0.01
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()