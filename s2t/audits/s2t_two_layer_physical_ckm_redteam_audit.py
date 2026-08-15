#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution


def matrix_unit(row, column):
    result = np.zeros((3, 3), dtype=complex)
    result[row, column] = 1.0
    return result


def phased_edge(edge, phase):
    target, source = edge
    unit = matrix_unit(target, source)
    return np.exp(1j * phase) * unit + np.exp(-1j * phase) * unit.conj().T


def jarlskog(matrix):
    return float(
        np.imag(
            matrix[0, 0]
            * matrix[1, 1]
            * np.conj(matrix[0, 1])
            * np.conj(matrix[1, 0])
        )
    )


def standard_parameters(mixing):
    absolute = np.abs(mixing)
    sine_13 = float(np.clip(absolute[0, 2], 0.0, 1.0))
    cosine_13 = math.sqrt(max(1.0 - sine_13**2, 1e-16))
    sine_12 = float(np.clip(absolute[0, 1] / cosine_13, 0.0, 1.0))
    sine_23 = float(np.clip(absolute[1, 2] / cosine_13, 0.0, 1.0))
    cosine_12 = math.sqrt(max(1.0 - sine_12**2, 1e-16))
    cosine_23 = math.sqrt(max(1.0 - sine_23**2, 1e-16))
    invariant = jarlskog(mixing)
    denominator = (
        sine_12
        * sine_23
        * sine_13
        * cosine_12
        * cosine_23
        * cosine_13**2
    )
    sine_delta = float(np.clip(invariant / denominator, -1.0, 1.0))
    cosine_delta = float(
        np.clip(
            (
                absolute[1, 0] ** 2
                - sine_12**2 * cosine_23**2
                - cosine_12**2 * sine_23**2 * sine_13**2
            )
            / (
                2.0
                * sine_12
                * cosine_12
                * sine_23
                * cosine_23
                * sine_13
            ),
            -1.0,
            1.0,
        )
    )
    delta = math.atan2(sine_delta, cosine_delta)
    if delta < 0.0:
        delta += 2.0 * math.pi
    return {
        "absolute_mixing": absolute.tolist(),
        "Jarlskog": invariant,
        "sin_theta_12": sine_12,
        "sin_theta_23": sine_23,
        "sin_theta_13": sine_13,
        "theta_12_degrees": math.degrees(math.asin(sine_12)),
        "theta_23_degrees": math.degrees(math.asin(sine_23)),
        "theta_13_degrees": math.degrees(math.asin(sine_13)),
        "delta_radians": delta,
        "delta_degrees": math.degrees(delta),
    }


def build_matrices(odd_weight, chord_weight, flux):
    level_operator = np.diag([1.0, 2.0, 3.0]).astype(complex)
    upper = level_operator + chord_weight * phased_edge((2, 0), -flux)
    lower = (
        level_operator
        + odd_weight * phased_edge((1, 0), 0.0)
        + odd_weight * phased_edge((2, 1), 0.0)
    )
    return upper, lower


def physical_readout(odd_weight, chord_weight, flux):
    upper, lower = build_matrices(odd_weight, chord_weight, flux)
    upper_squared = upper @ upper.conj().T
    lower_squared = lower @ lower.conj().T
    upper_mass_squared, upper_vectors = np.linalg.eigh(upper_squared)
    lower_mass_squared, lower_vectors = np.linalg.eigh(lower_squared)
    mixing = upper_vectors.conj().T @ lower_vectors
    commutator = upper_squared @ lower_squared - lower_squared @ upper_squared
    trace_cube = np.trace(commutator @ commutator @ commutator)
    upper_vandermonde = np.prod(
        [
            upper_mass_squared[first] - upper_mass_squared[second]
            for first in range(3)
            for second in range(first + 1, 3)
        ]
    )
    lower_vandermonde = np.prod(
        [
            lower_mass_squared[first] - lower_mass_squared[second]
            for first in range(3)
            for second in range(first + 1, 3)
        ]
    )
    parameters = standard_parameters(mixing)
    identity_rhs = (
        6j
        * parameters["Jarlskog"]
        * upper_vandermonde
        * lower_vandermonde
    )
    return {
        "upper_mass_squared": upper_mass_squared.tolist(),
        "lower_mass_squared": lower_mass_squared.tolist(),
        "upper_singular_values": np.sqrt(np.maximum(upper_mass_squared, 0.0)).tolist(),
        "lower_singular_values": np.sqrt(np.maximum(lower_mass_squared, 0.0)).tolist(),
        "trace_squared_mass_commutator_cube": {
            "real": float(np.real(trace_cube)),
            "imaginary": float(np.imag(trace_cube)),
        },
        "jarlskog_identity_rhs": {
            "real": float(np.real(identity_rhs)),
            "imaginary": float(np.imag(identity_rhs)),
        },
        "jarlskog_identity_absolute_error": float(abs(trace_cube - identity_rhs)),
        **parameters,
    }


def exact_invariants():
    odd_weight, chord_weight, flux = sp.symbols("p q Phi", real=True)
    imaginary_unit = sp.I
    level_operator = sp.diag(1, 2, 3)

    def exact_unit(row, column):
        return sp.eye(3)[:, row] * sp.eye(3)[column, :]

    def exact_edge(edge, phase):
        target, source = edge
        unit = exact_unit(target, source)
        return (
            sp.exp(imaginary_unit * phase) * unit
            + sp.exp(-imaginary_unit * phase) * unit.conjugate().T
        )

    upper = level_operator + chord_weight * exact_edge((2, 0), -flux)
    lower = (
        level_operator
        + odd_weight * exact_edge((1, 0), 0)
        + odd_weight * exact_edge((2, 1), 0)
    )
    auxiliary_commutator = upper * lower - lower * upper
    auxiliary_trace = sp.factor(
        sp.expand_complex(sp.trace(auxiliary_commutator**3))
    )
    upper_squared = upper * upper.conjugate().T
    lower_squared = lower * lower.conjugate().T
    physical_commutator = upper_squared * lower_squared - lower_squared * upper_squared
    physical_trace = sp.factor(
        sp.expand_complex(sp.trace(physical_commutator**3))
    )
    auxiliary_expected = (
        12
        * imaginary_unit
        * odd_weight**2
        * chord_weight
        * (chord_weight**2 + 1)
        * sp.sin(flux)
    )
    physical_expected = (
        192
        * imaginary_unit
        * odd_weight**2
        * chord_weight
        * (2 * odd_weight**2 - 15)
        * (chord_weight**2 - 15)
        * (chord_weight**2 + 1)
        * sp.sin(flux)
    )
    assert sp.simplify(auxiliary_trace - auxiliary_expected) == 0
    assert sp.simplify(physical_trace - physical_expected) == 0
    return {
        "auxiliary_mass_commutator": "12*i*p^2*q*(q^2+1)*sin(Phi)",
        "physical_squared_mass_commutator": "192*i*p^2*q*(2*p^2-15)*(q^2-15)*(q^2+1)*sin(Phi)",
        "physical_degeneracy_zeros": ["p^2=15/2", "q^2=15"],
    }


def grading_checks():
    grading = np.diag([1.0, -1.0, 1.0]).astype(complex)
    odd_chain = phased_edge((1, 0), 0.0) + phased_edge((2, 1), 0.0)
    even_chord = phased_edge((2, 0), 0.0)
    return {
        "odd_chain_anticommutator_norm": float(
            np.linalg.norm(grading @ odd_chain + odd_chain @ grading)
        ),
        "even_chord_commutator_norm": float(
            np.linalg.norm(grading @ even_chord - even_chord @ grading)
        ),
        "even_chord_anticommutator_norm": float(
            np.linalg.norm(grading @ even_chord + even_chord @ grading)
        ),
        "interpretation": "The chain is grading-odd, while the chord is grading-even. The chord is not a zero-form odd Higgs component of a Quillen superconnection on this unchanged grading.",
    }


def rephasing_check(odd_weight, chord_weight, flux):
    upper, lower = build_matrices(odd_weight, chord_weight, flux)
    phases = np.array([0.17, -0.31, 0.73])
    rephasing = np.diag(np.exp(1j * phases))
    transformed_upper = rephasing @ upper @ rephasing.conj().T
    transformed_lower = rephasing @ lower @ rephasing.conj().T

    def read_matrices(first, second):
        first_squared = first @ first.conj().T
        second_squared = second @ second.conj().T
        _, first_vectors = np.linalg.eigh(first_squared)
        _, second_vectors = np.linalg.eigh(second_squared)
        return standard_parameters(first_vectors.conj().T @ second_vectors)

    original = read_matrices(upper, lower)
    transformed = read_matrices(transformed_upper, transformed_lower)
    return {
        "absolute_mixing_invariant": bool(
            np.allclose(
                original["absolute_mixing"],
                transformed["absolute_mixing"],
                atol=1e-12,
            )
        ),
        "Jarlskog_invariant": abs(original["Jarlskog"] - transformed["Jarlskog"])
        < 1e-12,
    }


def svd_eigendecomposition_check(odd_weight, chord_weight, flux):
    upper, lower = build_matrices(odd_weight, chord_weight, flux)
    upper_squared = upper @ upper.conj().T
    lower_squared = lower @ lower.conj().T
    _, upper_eigenvectors = np.linalg.eigh(upper_squared)
    _, lower_eigenvectors = np.linalg.eigh(lower_squared)
    eigen_mixing = upper_eigenvectors.conj().T @ lower_eigenvectors

    upper_left, upper_singular, _ = np.linalg.svd(upper)
    lower_left, lower_singular, _ = np.linalg.svd(lower)
    upper_order = np.argsort(upper_singular)
    lower_order = np.argsort(lower_singular)
    svd_mixing = (
        upper_left[:, upper_order].conj().T @ lower_left[:, lower_order]
    )
    eigen_parameters = standard_parameters(eigen_mixing)
    svd_parameters = standard_parameters(svd_mixing)
    return {
        "absolute_mixing_max_error": float(
            np.max(
                np.abs(
                    np.asarray(eigen_parameters["absolute_mixing"])
                    - np.asarray(svd_parameters["absolute_mixing"])
                )
            )
        ),
        "Jarlskog_absolute_error": abs(
            eigen_parameters["Jarlskog"] - svd_parameters["Jarlskog"]
        ),
    }


def random_exact_formula_check(sample_count=25):
    generator = np.random.default_rng(20260806)
    maximum_error = 0.0
    for _ in range(sample_count):
        odd_weight = float(generator.uniform(0.2, 2.5))
        chord_weight = float(generator.uniform(0.2, 3.0))
        flux = float(generator.uniform(0.1, math.pi - 0.1))
        upper, lower = build_matrices(odd_weight, chord_weight, flux)
        upper_squared = upper @ upper.conj().T
        lower_squared = lower @ lower.conj().T
        commutator = upper_squared @ lower_squared - lower_squared @ upper_squared
        direct = np.trace(commutator @ commutator @ commutator)
        expected = (
            192j
            * odd_weight**2
            * chord_weight
            * (2 * odd_weight**2 - 15)
            * (chord_weight**2 - 15)
            * (chord_weight**2 + 1)
            * math.sin(flux)
        )
        maximum_error = max(maximum_error, float(abs(direct - expected)))
    return {
        "seed": 20260806,
        "sample_count": sample_count,
        "maximum_absolute_error": maximum_error,
    }


def main():
    continuous = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    target_cosine = float(continuous["continuous_two_sector_solution"]["cos_theta_numeric"])
    target_flux = math.acos(target_cosine)
    curvature_c = float(continuous["gap_action"]["curvature_at_target"])
    curvature_flux = curvature_c * (1.0 - target_cosine**2)

    prediction = physical_readout(1.0, 2.0, target_flux)
    conjugate = physical_readout(1.0, 2.0, -target_flux)
    exact = exact_invariants()
    grading = grading_checks()
    rephasing = rephasing_check(1.0, 2.0, target_flux)
    svd_check = svd_eigendecomposition_check(1.0, 2.0, target_flux)
    random_formula_check = random_exact_formula_check()

    control_sines = np.array([0.22501, 0.04183, 0.003732])
    control_angles = np.degrees(np.arcsin(control_sines))

    def objective(log_weights):
        odd_weight, chord_weight = np.exp(log_weights)
        row = physical_readout(odd_weight, chord_weight, target_flux)
        predicted_angles = np.array(
            [
                row["theta_12_degrees"],
                row["theta_23_degrees"],
                row["theta_13_degrees"],
            ]
        )
        return float(np.sum(np.radians(predicted_angles - control_angles) ** 2))

    optimization = differential_evolution(
        objective,
        [(-8.0, 2.0), (-8.0, 2.0)],
        seed=1,
        tol=1e-12,
        polish=True,
    )
    best_odd_weight, best_chord_weight = np.exp(optimization.x)
    best_fit = physical_readout(best_odd_weight, best_chord_weight, target_flux)

    results = {
        "status": "redteam_correction_confirms_the_texture_failure_but_replaces_the_auxiliary_mass_commutator_by_the_physical_squared_mass_invariant_and_rejects_the_superconnection_overclaim",
        "date": "2026-08-06",
        "blind_stage": {
            "CKM_control_loaded": False,
            "odd_weight": 1.0,
            "chord_weight": 2.0,
            "cos_flux": target_cosine,
            "flux_radians": target_flux,
            "gap_transfer_status": "conditional hypothesis, not a parent-action derivation",
            "curvature_in_flux": curvature_flux,
            "prediction": prediction,
        },
        "physical_invariant_gate": {
            **exact,
            "standard_object": "H_u=M_u M_u^dagger and H_d=M_d M_d^dagger",
            "numerical_Jarlskog_identity_error": prediction[
                "jarlskog_identity_absolute_error"
            ],
            "finding": "The earlier trace of [M_u,M_d]^3 is only an auxiliary Hermitian-matrix invariant. The physical CKM test uses the squared-mass commutator; it remains nonzero for p=1,q=2 but has additional degeneracy zeros.",
        },
        "grading_and_superconnection_gate": grading,
        "basis_rephasing_gate": rephasing,
        "independent_diagonalization_gate": svd_check,
        "random_exact_formula_gate": random_formula_check,
        "CP_conjugation_gate": {
            "absolute_mixing_equal": bool(
                np.allclose(
                    prediction["absolute_mixing"],
                    conjugate["absolute_mixing"],
                    atol=1e-12,
                )
            ),
            "Jarlskog_sign_reversed": abs(
                prediction["Jarlskog"] + conjugate["Jarlskog"]
            )
            < 1e-12,
        },
        "post_blind_PDG_2024_control": {
            "source": "Particle Data Group 2024 CKM review, Eqs. (12.27)-(12.28)",
            "sin_theta_12": control_sines[0],
            "sin_theta_23": control_sines[1],
            "sin_theta_13": control_sines[2],
            "delta_radians": 1.147,
            "Jarlskog": 3.12e-5,
            "control_angles_degrees": control_angles.tolist(),
            "prediction_angles_degrees": [
                prediction["theta_12_degrees"],
                prediction["theta_23_degrees"],
                prediction["theta_13_degrees"],
            ],
            "finding": "The corrected physical diagonalization still predicts large, non-hierarchical mixing and a Jarlskog invariant over three orders of magnitude too large.",
        },
        "equal_odd_edge_diagnostic": {
            "fit_performed_only_after_blind_prediction": True,
            "best_odd_weight": best_odd_weight,
            "best_chord_weight": best_chord_weight,
            "best_angles_degrees": [
                best_fit["theta_12_degrees"],
                best_fit["theta_23_degrees"],
                best_fit["theta_13_degrees"],
            ],
            "objective_radians_squared": float(optimization.fun),
            "finding": "A common odd-edge weight cannot separate theta_12 and theta_23; edge asymmetry remains necessary.",
        },
        "scientific_verdict": {
            "survives": "The A3 tree no-go, the need for a cycle, the existence of CP-conjugate flux choices, and the failure of symmetric odd-edge weights all survive the red-team audit.",
            "corrected": "The physical invariant is Tr([H_u,H_d]^3), not merely Tr([M_u,M_d]^3). The even chord is not by itself a standard odd Higgs zero-form in a Quillen superconnection.",
            "status": "physical_CP_mechanism_exists_but_superconnection_parent_action_and_CKM_texture_both_fail",
            "next_gate": "Enlarge the graded space or derive an even curvature layer and unequal odd-edge metrics from the RP3 and S1 factors before any further CKM comparison.",
        },
    }

    assert curvature_flux > 0.0
    assert prediction["jarlskog_identity_absolute_error"] < 1e-8
    assert grading["odd_chain_anticommutator_norm"] < 1e-12
    assert grading["even_chord_commutator_norm"] < 1e-12
    assert grading["even_chord_anticommutator_norm"] > 1.0
    assert rephasing["absolute_mixing_invariant"]
    assert rephasing["Jarlskog_invariant"]
    assert svd_check["absolute_mixing_max_error"] < 1e-12
    assert svd_check["Jarlskog_absolute_error"] < 1e-12
    assert random_formula_check["maximum_absolute_error"] < 1e-7
    assert results["CP_conjugation_gate"]["absolute_mixing_equal"]
    assert results["CP_conjugation_gate"]["Jarlskog_sign_reversed"]
    assert prediction["theta_12_degrees"] > 20.0
    assert prediction["theta_23_degrees"] > 40.0
    assert prediction["theta_13_degrees"] > 30.0
    assert abs(best_fit["theta_12_degrees"] - best_fit["theta_23_degrees"]) < 0.01

    Path("s2t_two_layer_physical_ckm_redteam_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "physical_invariant": exact["physical_squared_mass_commutator"],
                "prediction_angles": results["post_blind_PDG_2024_control"][
                    "prediction_angles_degrees"
                ],
                "prediction_Jarlskog": prediction["Jarlskog"],
                "PDG_2024_Jarlskog": results["post_blind_PDG_2024_control"][
                    "Jarlskog"
                ],
                "superconnection_overclaim_rejected": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()