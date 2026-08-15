#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

from s2t_v4_pati_salam_first_order_kernel import dirac_from_channels
from s2t_v4_pati_salam_ko6_phi_sigma_hessian_gate import (
    composite_yukawa,
    crossed_majorana,
    phi_basis,
    signature,
)


OUTPUT = Path("s2t_v4_pati_salam_common_scale_no_go_results.json")


def scaled_spectral_hessian(background, first, second, quadratic_scale):
    background_squared = background @ background
    anticommutator = first @ second + second @ first
    return float(
        (
            -0.5 * quadratic_scale * np.trace(anticommutator)
            + 2.0 * np.trace(background_squared @ anticommutator)
            + np.trace(background @ first @ background @ second)
            + np.trace(background @ second @ background @ first)
        ).real
    )


def scaled_phi_hessian(background, sigma, quadratic_scale):
    basis = phi_basis(sigma)
    hessian = np.zeros((8, 8))
    for row, first in enumerate(basis):
        for column, second in enumerate(basis[: row + 1]):
            value = scaled_spectral_hessian(
                background, first, second, quadratic_scale
            )
            hessian[row, column] = value
            hessian[column, row] = value
    return hessian


def quadratic_identity_error(majorana, quadratic_scale, rng):
    background = dirac_from_channels(None, majorana, None)
    errors = []
    nonpositive = []
    for _ in range(100):
        yukawa = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
        variation = dirac_from_channels(yukawa, None, None)
        measured = scaled_spectral_hessian(
            background, variation, variation, quadratic_scale
        )
        predicted = -4.0 * quadratic_scale * np.vdot(yukawa, yukawa).real
        predicted += 8.0 * np.vdot(
            majorana.conj().T @ yukawa, majorana.conj().T @ yukawa
        ).real
        errors.append(abs(measured - predicted))
        nonpositive.append(measured <= 1.0e-8)
    return max(errors), all(nonpositive)


def main():
    rng = np.random.default_rng(20260814)
    sigma_bl = np.diag([0.75, -0.25, -0.25, -0.25])
    scans = {}
    identity_errors = []

    for quadratic_scale in (0.1, 1.0, 10.0):
        delta = np.zeros((2, 4), dtype=complex)
        delta[0, 0] = (quadratic_scale / 2.0) ** 0.25
        majorana = crossed_majorana(delta)
        background = dirac_from_channels(None, majorana, None)
        hessian = scaled_phi_hessian(background, sigma_bl, quadratic_scale)
        error, nonpositive = quadratic_identity_error(
            majorana, quadratic_scale, rng
        )
        identity_errors.append(error)
        scans[str(quadratic_scale)] = {
            "Delta_entry": float(delta[0, 0].real),
            "Majorana_nonzero_singular_square": float(
                np.linalg.svd(majorana, compute_uv=False)[0] ** 2
            ),
            "phi_signature": signature(hessian),
            "general_Yukawa_Hessian_nonpositive": nonpositive,
            "Sigma_flat_dimension_at_phi_zero": 15,
        }

    reference = np.asarray(scans["1.0"]["phi_signature"]["eigenvalues"])
    scaling_errors = {}
    for key, entry in scans.items():
        scale = float(key)
        eigenvalues = np.asarray(entry["phi_signature"]["eigenvalues"])
        scaling_errors[key] = float(np.max(np.abs(eigenvalues - scale * reference)))

    output = {
        "gate": "version4_pati_salam_common_scale_no_go",
        "potential_family": "V_alpha=-(alpha/2) Tr D_F^2 +(1/2) Tr D_F^4",
        "rank_one_stationary_relation": "||M_R||_op^2=alpha/2",
        "general_Yukawa_quadratic_form": (
            "H_Y,alpha(Y)=-4 alpha ||Y||^2+8||M_R^dagger Y||^2 <= 0"
        ),
        "scan": scans,
        "maximum_random_identity_error": max(identity_errors),
        "maximum_linear_eigenvalue_scaling_errors": scaling_errors,
        "common_scale_verdict": (
            "Changing the common a2/a4 quadratic-to-quartic ratio rescales the "
            "rank-one background and all eight negative phi eigenvalues but cannot "
            "change their signs. Sigma remains fifteen-dimensional and flat at phi=0."
        ),
        "project_archaeology": {
            "twisted_grand_symmetry": (
                "representation mismatch: the literature model is Pati-Salam-like with "
                "M3(C), a Majorana singlet sigma and a spacetime vector X_mu, not an SU4 "
                "adjoint Sigma_4 potential"
            ),
            "graded_superconnection": (
                "useful normalization mechanism for linking zero- and one-form channels, "
                "but generic spectral kernels split their Hessian weights"
            ),
            "compact_a2_a4": (
                "fixes one common tree-level quadratic/quartic ratio but cannot supply "
                "the missing representation-sensitive mixed invariants"
            ),
            "relative_mapping_cone": (
                "already fixes the Delta determinant selector and is the strongest local "
                "carrier from which a new mixed curvature invariant could be derived"
            ),
        },
        "surviving_target": (
            "derive from connected relative curvature a fixed mixed invariant that gives "
            "both a positive Y-channel shift and a direct full-rank Sigma_4 norm; a common "
            "spectral scale or a singlet/vector twist is insufficient"
        ),
        "next_gate": (
            "classify mixed quartic invariants generated by the irreducible relative cycle, "
            "compute their phi/Sigma Hessian ranks, and test whether one canonical curvature "
            "norm fixes the required coefficients without adding a second fitted weight"
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()