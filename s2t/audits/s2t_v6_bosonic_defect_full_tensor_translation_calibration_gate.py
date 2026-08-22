#!/usr/bin/env python3
"""Переносная калибровка полного скрученного гессиана Q+T+B.

Предыдущий аудит сохраняется как исторический. Здесь его оператор загружается
с одной явно контролируемой заменой: знак материальной части фоновой
калибровки согласуется со знаком переменной связности.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import eigsh, lsqr


ROOT = Path(__file__).resolve().parents[2]
PARENT_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate.py"
PARENT_RESULT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate_results.json"

OLD_GAUGE_TERM = "-(Z / G) * orbit_sector[component].conjugate() * average"
NEW_GAUGE_TERM = "+(Z / G) * orbit_sector[component].conjugate() * average"


def load_calibrated_module():
    source = PARENT_AUDIT.read_text(encoding="utf-8")
    assert source.count(OLD_GAUGE_TERM) == 1
    source = source.replace(OLD_GAUGE_TERM, NEW_GAUGE_TERM)
    marker = "    values = eigsh(\n"
    assert source.count(marker) == 1
    exposure = (
        "    globals()['LAST_ASSEMBLY'] = {"
        "'hessian': hessian, 'metric': metric, "
        "'transformation': transformation, 'radius': radius, "
        "'matter_basis': matter_basis, 'matter_weights': matter_weights, "
        "'harmonics': harmonics}\n"
    )
    source = source.replace(marker, exposure + marker)
    source = source.replace(
        'M=metric, which="SA", tol=5.0e-7,',
        'M=metric, sigma=0.0, which="LM", tol=2.0e-9,',
    )
    source = source.rsplit('if __name__ == "__main__":', 1)[0]
    namespace = {"__file__": str(PARENT_AUDIT), "__name__": "calibrated_parent"}
    exec(compile(source, str(PARENT_AUDIT), "exec"), namespace)
    return namespace


def translation_tangent(module, model, prepared, node_count):
    module["block_spectrum"](model, prepared, 0, 1, eigen_count=2)
    assembly = module["LAST_ASSEMBLY"]
    hessian = assembly["hessian"]
    metric = assembly["metric"]
    transformation = assembly["transformation"]
    radius = assembly["radius"]
    matter_basis = assembly["matter_basis"]
    harmonics = assembly["harmonics"]

    representation_zero = model["representation"][0]
    solution = model["solution"]
    q_coefficients = model["q_coefficients"]
    t_zero = model["t_zero"]
    t_three = model["t_three"]
    full = np.zeros(6 * node_count, dtype=complex)
    matter = full[:4 * node_count].reshape(4, node_count)

    for index, radial_coordinate in enumerate(radius):
        k, kp, a, ap, b, bp, q, qp = solution.sol(radial_coordinate)
        point = np.concatenate([
            q * q_coefficients,
            b * t_zero + a * t_three,
        ])
        point_prime = np.concatenate([
            qp * q_coefficients,
            bp * t_zero + ap * t_three,
        ])
        angular_derivative = (
            (1.0 - k) * representation_zero @ point / radial_coordinate
        )
        matter[:, index] = matter_basis.conj().T @ (
            point_prime + 1j * angular_derivative
        )

        # В родительском операторе переменная связности имеет знак,
        # противоположный физической delta A. Для F_{r theta}=-K'/r:
        # p=i K'/r, q=-K'/r, поэтому q=i p в регулярном m=1 канале.
        full[4 * node_count + index] = 1j * kp / radial_coordinate
        full[5 * node_count + index] = -kp / radial_coordinate

    for field in range(6):
        full[(field + 1) * node_count - 1] = 0.0
    for component, harmonic in enumerate(harmonics):
        if harmonic != 0:
            full[component * node_count] = 0.0
    full[5 * node_count] = 1j * full[4 * node_count]

    reduced = lsqr(
        transformation, full, atol=1.0e-13, btol=1.0e-13,
        iter_lim=10000,
    )[0]
    tangent_projection_residual = float(
        np.linalg.norm(transformation @ reduced - full)
        / max(np.linalg.norm(full), 1.0e-30)
    )
    h_tangent = hessian @ reduced
    m_tangent = metric @ reduced
    rayleigh = float(np.real(
        np.vdot(reduced, h_tangent) / np.vdot(reduced, m_tangent)
    ))
    generalized_residual = float(
        np.linalg.norm(h_tangent - rayleigh * m_tangent)
        / max(np.linalg.norm(m_tangent), 1.0e-30)
    )
    values, vectors = eigsh(
        hessian, k=1, M=metric, sigma=0.0, which="LM",
        tol=2.0e-10, maxiter=15000,
    )
    vector = vectors[:, 0]
    overlap = float(
        abs(np.vdot(vector, metric @ reduced))
        / np.sqrt(max(np.real(np.vdot(reduced, metric @ reduced)), 1.0e-30))
    )
    return {
        "lowest_eigenvalue": float(values[0]),
        "analytic_tangent_rayleigh_quotient": rayleigh,
        "analytic_tangent_generalized_residual": generalized_residual,
        "analytic_tangent_overlap_with_lowest_mode": overlap,
        "domain_projection_residual": tangent_projection_residual,
    }


def main() -> None:
    parent = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    module = load_calibrated_module()
    model = module["setup_model"]()
    base_nodes = [70, 100, 140]
    refinement_nodes = [200, 280]
    characters = [-1, 0, 1]
    labels = list(range(-3, 4))

    convergence = {}
    translation = {}
    for nodes in base_nodes:
        prepared = module["prepare_grid"](model, nodes)
        convergence[str(nodes)] = {
            str(character): {
                str(label): module["block_spectrum"](
                    model, prepared, character, label, eigen_count=2
                )
                for label in labels
            }
            for character in characters
        }
        translation[str(nodes)] = translation_tangent(
            module, model, prepared, nodes
        )

    refinement = {}
    for nodes in refinement_nodes:
        prepared = module["prepare_grid"](model, nodes)
        refinement[str(nodes)] = {
            "0:1": module["block_spectrum"](
                model, prepared, 0, 1, eigen_count=2
            ),
            "1:-1": module["block_spectrum"](
                model, prepared, 1, -1, eigen_count=2
            ),
            "1:-2": module["block_spectrum"](
                model, prepared, 1, -2, eigen_count=2
            ),
        }
        translation[str(nodes)] = translation_tangent(
            module, model, prepared, nodes
        )

    finest = convergence[str(base_nodes[-1])]
    conjugation_residual = max(
        abs(
            finest["1"][str(label)]["eigenvalues"][index]
            - finest["-1"][str(-label)]["eigenvalues"][index]
        )
        for label in labels for index in range(2)
    )
    all_nodes = base_nodes + refinement_nodes
    lowest_by_nodes = np.array([
        translation[str(nodes)]["lowest_eigenvalue"] for nodes in all_nodes
    ])
    tangent_rayleigh = np.array([
        translation[str(nodes)]["analytic_tangent_rayleigh_quotient"]
        for nodes in all_nodes
    ])
    fit_nodes = np.array([140.0, 200.0, 280.0])
    fit_variable = 1.0 / (fit_nodes - 1.0) ** 2
    zero_limit = float(np.polyfit(fit_variable, lowest_by_nodes[-3:], 1)[1])
    rayleigh_limit = float(np.polyfit(fit_variable, tangent_rayleigh[-3:], 1)[1])
    primary = np.array([
        convergence["140"]["1"]["-1"]["eigenvalues"][0],
        refinement["200"]["1:-1"]["eigenvalues"][0],
        refinement["280"]["1:-1"]["eigenvalues"][0],
    ])
    secondary = np.array([
        convergence["140"]["1"]["-2"]["eigenvalues"][0],
        refinement["200"]["1:-2"]["eigenvalues"][0],
        refinement["280"]["1:-2"]["eigenvalues"][0],
    ])
    primary_limit = float(np.polyfit(fit_variable, primary, 1)[1])
    secondary_limit = float(np.polyfit(fit_variable, secondary, 1)[1])
    checked_near_zero_levels = [
        row["eigenvalues"][0]
        for character in finest.values() for row in character.values()
    ]

    result = {
        "gate": "version6_bosonic_defect_full_tensor_translation_calibration_gate",
        "identified_sign_error": {
            "location": "matter term of the polar background-gauge square",
            "parent_expression": OLD_GAUGE_TERM,
            "calibrated_expression": NEW_GAUGE_TERM,
            "connection_variable_is_minus_physical_delta_A": True,
            "number_of_operator_source_replacements": 1,
        },
        "operator": {
            "stationary_four_profile_background": True,
            "characters": characters,
            "integer_labels": labels,
            "base_node_counts": base_nodes,
            "refinement_node_counts": refinement_nodes,
            "near_zero_shift_invert_used": True,
        },
        "corrected_convergence": convergence,
        "targeted_refinement": refinement,
        "translation_calibration": translation,
        "continuum_diagnostics": {
            "fit_variable": "1/(N-1)^2",
            "translation_eigenvalue_limit": zero_limit,
            "analytic_tangent_rayleigh_limit": rayleigh_limit,
            "former_primary_negative_block_limit": primary_limit,
            "former_secondary_negative_block_limit": secondary_limit,
            "maximum_conjugate_sector_residual": conjugation_residual,
            "minimum_checked_near_zero_level_at_N140": float(min(checked_near_zero_levels)),
        },
        "comparison_with_parent": {
            "parent_primary_candidate_limit": parent["continuum_diagnostics"]["primary_twisted_candidate_limit"],
            "parent_secondary_candidate_limit": parent["continuum_diagnostics"]["secondary_twisted_candidate_limit"],
            "parent_translation_candidate_limit": parent["continuum_diagnostics"]["translation_candidate_limit"],
            "parent_negative_candidates_survive_calibration": False,
        },
        "verdict": {
            "translation_zero_mode_resolved": bool(
                abs(zero_limit) < 8.0e-5 and abs(rayleigh_limit) < 2.0e-4
            ),
            "former_negative_pair_is_gauge_fixing_sign_artifact": bool(
                primary_limit > 3.0 and secondary_limit > 3.0
            ),
            "checked_window_has_negative_near_zero_level": bool(
                min(checked_near_zero_levels) < -1.0e-5
            ),
            "full_angular_tail_closed_for_full_tensor_operator": False,
            "straight_vortex_full_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_high_angular_coercivity_gate",
        },
    }
    assert conjugation_residual < 1.0e-8
    assert result["verdict"]["translation_zero_mode_resolved"]
    assert result["verdict"]["former_negative_pair_is_gauge_fixing_sign_artifact"]
    assert not result["verdict"]["checked_window_has_negative_near_zero_level"]
    assert max(
        row["domain_projection_residual"] for row in translation.values()
    ) < 1.0e-12
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()