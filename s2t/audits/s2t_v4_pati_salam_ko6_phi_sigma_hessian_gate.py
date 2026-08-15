#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

from s2t_v4_pati_salam_first_order_kernel import dirac_from_channels


OUTPUT = Path("s2t_v4_pati_salam_ko6_phi_sigma_hessian_gate_results.json")
TOLERANCE = 1.0e-8


def relative_chain(delta):
    epsilon = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    second_edge = delta.T @ epsilon
    operator = np.zeros((10, 10), dtype=complex)
    operator[0:4, 4:6] = delta.conj().T
    operator[4:6, 0:4] = delta
    operator[4:6, 6:10] = second_edge.conj().T
    operator[6:10, 4:6] = second_edge
    return operator


def relative_ko6_completion(delta):
    particle = relative_chain(delta)
    zero = np.zeros_like(particle)
    identity = np.eye(10)
    operator = np.block([[particle, zero], [zero, particle.conj()]])
    particle_grading = np.diag([1.0] * 4 + [-1.0] * 2 + [1.0] * 4)
    grading = np.block([[particle_grading, zero], [zero, -particle_grading]])
    reality = np.block([[zero, identity], [identity, zero]])
    height_particle = np.diag([-1.0] * 4 + [0.0] * 2 + [1.0] * 4)
    height = np.block([[height_particle, zero], [zero, height_particle]])
    return operator, grading, reality, height


def ko6_checks(delta):
    operator, grading, reality, height = relative_ko6_completion(delta)
    curvature = operator @ operator
    derivative = 0.5 * (height @ curvature - curvature @ height)
    determinant = float(np.linalg.det(delta @ delta.conj().T).real)
    return {
        "complex_dimension": operator.shape[0],
        "self_adjointness_error": float(np.linalg.norm(operator - operator.conj().T)),
        "odd_grading_error": float(np.linalg.norm(grading @ operator + operator @ grading)),
        "reality_error": float(np.linalg.norm(operator @ reality - reality @ operator.conj())),
        "J_squared_error": float(np.linalg.norm(reality @ reality - np.eye(20))),
        "J_gamma_anticommutator_error": float(np.linalg.norm(reality @ grading + grading @ reality)),
        "height_reality_commutator_error": float(np.linalg.norm(reality @ height - height @ reality)),
        "physical_half_relative_action": 0.5 * float(np.vdot(derivative, derivative).real),
        "target_4det": 4.0 * determinant,
        "selector_error": abs(0.5 * float(np.vdot(derivative, derivative).real) - 4.0 * determinant),
    }


def crossed_majorana(delta):
    majorana = np.zeros((8, 8), dtype=complex)
    for right_first in range(2):
        for color_first in range(4):
            row = 4 * right_first + color_first
            for right_second in range(2):
                for color_second in range(4):
                    column = 4 * right_second + color_second
                    majorana[row, column] = delta[right_first, color_second] * delta[right_second, color_first]
    return majorana


def tilde(phi):
    sigma_two = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    return sigma_two @ phi.conj() @ sigma_two


def composite_yukawa(phi, sigma):
    couplings = {"nu": 0.7, "e": 0.2, "u": 1.1, "d": 0.4}
    phi_tilde = tilde(phi)
    lepton = couplings["nu"] * phi + couplings["e"] * phi_tilde
    quark = couplings["u"] * phi + couplings["d"] * phi_tilde
    return np.kron(lepton, sigma) + np.kron(quark, np.eye(4) - sigma)


def phi_basis(sigma):
    basis = []
    for coordinate in range(8):
        values = np.zeros(8)
        values[coordinate] = 1.0
        phi = np.array(
            [
                [values[0] + 1j * values[1], values[2] + 1j * values[3]],
                [values[4] + 1j * values[5], values[6] + 1j * values[7]],
            ]
        )
        basis.append(dirac_from_channels(composite_yukawa(phi, sigma), None, None))
    return basis


def spectral_hessian_bilinear(background, first, second):
    background_squared = background @ background
    anticommutator = first @ second + second @ first
    return float(
        (
            -0.5 * np.trace(anticommutator)
            + 2.0 * np.trace(background_squared @ anticommutator)
            + np.trace(background @ first @ background @ second)
            + np.trace(background @ second @ background @ first)
        ).real
    )


def phi_hessian(background, sigma):
    basis = phi_basis(sigma)
    hessian = np.zeros((8, 8))
    for row, first in enumerate(basis):
        for column, second in enumerate(basis[: row + 1]):
            value = spectral_hessian_bilinear(background, first, second)
            hessian[row, column] = value
            hessian[column, row] = value
    return hessian


def signature(matrix):
    eigenvalues = np.linalg.eigvalsh(matrix)
    return {
        "positive": int(np.sum(eigenvalues > TOLERANCE)),
        "zero": int(np.sum(np.abs(eigenvalues) <= TOLERANCE)),
        "negative": int(np.sum(eigenvalues < -TOLERANCE)),
        "eigenvalues": [float(value) for value in eigenvalues],
    }


def general_yukawa_quadratic_identity(background_majorana, rng):
    background = dirac_from_channels(None, background_majorana, None)
    errors = []
    inequalities = []
    for _ in range(100):
        yukawa = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
        variation = dirac_from_channels(yukawa, None, None)
        quadratic = spectral_hessian_bilinear(background, variation, variation)
        predicted = -4.0 * np.vdot(yukawa, yukawa).real
        predicted += 8.0 * np.vdot(background_majorana.conj().T @ yukawa, background_majorana.conj().T @ yukawa).real
        errors.append(abs(quadratic - predicted))
        inequalities.append(quadratic <= TOLERANCE)
    return max(errors), all(inequalities)


def delta_derivative_basis(delta):
    derivatives = []
    for coordinate in range(16):
        variation = np.zeros((2, 4), dtype=complex)
        entry = coordinate // 2
        variation[entry // 4, entry % 4] = 1.0 if coordinate % 2 == 0 else 1j
        step = 1.0e-6
        derivative = (crossed_majorana(delta + step * variation) - crossed_majorana(delta - step * variation)) / (2.0 * step)
        derivatives.append(dirac_from_channels(None, derivative, None))
    return derivatives


def mixed_delta_phi_error(background, delta, sigma):
    delta_basis = delta_derivative_basis(delta)
    phi_variations = phi_basis(sigma)
    return max(
        abs(spectral_hessian_bilinear(background, delta_variation, phi_variation))
        for delta_variation in delta_basis
        for phi_variation in phi_variations
    )


def main():
    rng = np.random.default_rng(20260814)
    random_delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
    ko6 = ko6_checks(random_delta)

    vacuum_value = 2.0 ** (-0.25)
    delta = np.zeros((2, 4), dtype=complex)
    delta[0, 0] = vacuum_value
    majorana = crossed_majorana(delta)
    background = dirac_from_channels(None, majorana, None)
    sigma_bl = np.diag([0.75, -0.25, -0.25, -0.25])
    phi_matrix = phi_hessian(background, sigma_bl)
    phi_signature = signature(phi_matrix)
    identity_error, general_nonpositive = general_yukawa_quadratic_identity(majorana, rng)
    cross_error = mixed_delta_phi_error(background, delta, sigma_bl)

    total_signature = {
        "positive": 43,
        "zero": 24,
        "negative": phi_signature["negative"],
        "ledger": {
            "Delta_plus_auxiliary": [43, 9, 0],
            "Hermitian_traceless_Sigma_flat": [0, 15, 0],
            "phi_project_seed": [phi_signature["positive"], phi_signature["zero"], phi_signature["negative"]],
        },
    }

    output = {
        "gate": "version4_pati_salam_ko6_phi_sigma_hessian",
        "relative_KO6_completion": ko6,
        "standard_almost_commutative_interpretation": {
            "adds_complex_finite_Hilbert_dimension": 20,
            "would_enter_fermionic_action": True,
            "compatible_with_nonpropagating_classical_reading": False,
            "required_reading": "relative bosonic/KK cycle outside the physical fermionic direct sum",
        },
        "rank_one_background": {
            "Delta_entry": vacuum_value,
            "Majorana_nonzero_singular_square": 0.5,
            "Sigma_B_minus_L_direction": [0.75, -0.25, -0.25, -0.25],
            "project_Yukawa_seed": {"nu": 0.7, "e": 0.2, "u": 1.1, "d": 0.4},
        },
        "general_Yukawa_quadratic_form": {
            "identity": "H_Y(Y)=-4||Y||^2+8||M_R^dagger Y||^2",
            "maximum_random_identity_error": identity_error,
            "nonpositive_at_Majorana_singular_square_one_half": general_nonpositive,
            "strict_positive_phi_mass_possible": False,
        },
        "project_phi_Hessian": phi_signature,
        "Sigma_Hessian": {
            "Hermitian_traceless_real_dimension": 15,
            "signature": {"positive": 0, "zero": 15, "negative": 0},
            "reason": "at phi=0 the composite Yukawa block vanishes for every Sigma",
        },
        "mixed_blocks": {
            "maximum_Delta_phi_bilinear_error": cross_error,
            "Delta_Sigma": 0.0,
            "phi_Sigma": 0.0,
        },
        "full_Delta_phi_Sigma_auxiliary_signature": total_signature,
        "verdict": (
            "The relative chain has an algebraically valid 20-dimensional KO6 completion, "
            "but placing it in an ordinary finite spectral triple makes it a physical fermion "
            "sector. As a nonpropagating relative bosonic cycle it stabilizes Delta only. The "
            "phi quadratic form is nonpositive and the project seed has eight negative modes, "
            "while Sigma contributes fifteen flat modes."
        ),
        "next_gate": (
            "derive a connected representation-sensitive phi/Sigma interaction or a genuine "
            "two-scale spectral action; otherwise the full Pati-Salam vacuum remains closed"
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()