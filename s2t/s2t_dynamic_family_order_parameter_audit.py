#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np


def cross_matrix(vector):
    x, y, z = vector
    return np.array(
        [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float
    )


def main():
    characters = np.array(
        [
            [1, 1, 1],
            [-1, 1, -1],
            [1, -1, -1],
            [-1, -1, 1],
        ],
        dtype=int,
    )

    antisymmetric_basis = [
        cross_matrix(np.array([1.0, 0.0, 0.0])),
        cross_matrix(np.array([0.0, 1.0, 0.0])),
        cross_matrix(np.array([0.0, 0.0, 1.0])),
    ]
    invariant_constant_forms = []
    for basis_matrix in antisymmetric_basis:
        invariant = True
        for signs in characters:
            representation = np.diag(signs)
            if not np.allclose(
                representation @ basis_matrix @ representation.T,
                basis_matrix,
            ):
                invariant = False
        invariant_constant_forms.append(invariant)

    dynamic_terms_invariant = []
    for i, j, k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        dynamic_terms_invariant.append(
            all(signs[i] * signs[j] * signs[k] == 1 for signs in characters)
        )

    sigma = np.array([1.0, 2.0, 4.0])
    family_operator = cross_matrix(sigma)

    inverse_square_weights = (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2))
    w3, w1 = inverse_square_weights
    factor_eigenvalues = np.array([2.0 * w3, 2.0 * w1, 2.0 * (w3 + w1)])

    mu1, mu2, mu3 = 3.0, 1.0, 4.0
    cubic_coupling = 0.5
    axis_amplitude = 2.0
    transverse_hessian = np.array(
        [
            [2.0 * (mu1 - mu2), cubic_coupling * axis_amplitude],
            [cubic_coupling * axis_amplitude, 2.0 * (mu3 - mu2)],
        ]
    )

    results = {
        "status": "dynamic_selector_algebra_pass_condensation_coefficients_open",
        "date": "2026-08-08",
        "representation_gate": {
            "constant_antisymmetric_invariant_dimension": int(
                sum(invariant_constant_forms)
            ),
            "dynamic_epsilon_terms_all_invariant": all(dynamic_terms_invariant),
            "finding": (
                "Lambda^2(V) has no invariant vector, but V tensor Lambda^2(V) "
                "contains the invariant epsilon_ijk Sigma_k chi_i chi_j."
            ),
        },
        "rank_gate": {
            "sample_sigma": sigma.tolist(),
            "rank_A_sigma": int(np.linalg.matrix_rank(family_operator)),
            "kernel_residual": float(np.linalg.norm(family_operator @ sigma)),
        },
        "isotropic_potential": {
            "potential": "m2*|Sigma|^2+(u/4)*|Sigma|^4+v*Sigma1*Sigma2*Sigma3",
            "favored_diagonal_stationarity": "3*u*s^2-|v|*s+2*m2=0",
            "spinodal_condition": "m2 <= v^2/(24*u)",
            "degenerate_first_order_transition": "m2 = v^2/(27*u)",
            "nonzero_global_minimum_condition": "m2 < v^2/(27*u)",
            "favored_orientation_count": 4,
            "correction": (
                "The cubic invariant changes the radial minimum. There are four "
                "favored sign orientations, not eight minima, and condensation can "
                "occur for positive m2 through a first-order transition."
            ),
        },
        "factor_mass_selector": {
            "quadratic_operator": "M2=m0^2*I+kappa*L(w3,w1)",
            "inverse_square_eigenvalues": factor_eigenvalues.tolist(),
            "unique_lowest_character_index": int(np.argmin(factor_eigenvalues)),
            "finding": (
                "The existing product-factor Laplacian gives a canonical anisotropic "
                "quadratic term and selects the S1 character as the first instability "
                "for positive kappa in the inverse-square branch."
            ),
        },
        "fermion_gate": {
            "zero_temperature_pair_energy_if_parity_branches_available": "Delta E=-|g Sigma|/2",
            "finite_temperature_free_energy": "-(1/beta) log(2 cosh(beta*g*|Sigma|/2))",
            "small_field_quadratic_shift": "-beta*g^2*|Sigma|^2/8",
            "unconditional_condensation": False,
            "parity_completion_required": True,
            "cubic_generated_by_core_pair": False,
            "finding": (
                "The cusp requires access to the lower parity branch. Fixed global "
                "fermion parity and the completion of an odd local Majorana system "
                "must be specified before claiming unconditional condensation."
            ),
        },
        "bulk_core_gate": {
            "projected_core_epsilon_bilinear_nonzero": True,
            "bulk_lorentz_scalar_antisymmetric_family_bilinear_nonzero": False,
            "finding": (
                "The antisymmetric family operator is valid after core projection, "
                "but a scalar bulk Weyl/Majorana bilinear is flavor symmetric. Its "
                "epsilon contraction vanishes, so a connection or derivative origin "
                "must be derived."
            ),
        },
        "axis_stability_gate": {
            "condition": "mu1>mu2, mu3>mu2, 4*(mu1-mu2)*(mu3-mu2)>v^2*s^2",
            "sample_transverse_hessian": transverse_hessian.tolist(),
            "sample_eigenvalues": np.linalg.eigvalsh(transverse_hessian).tolist(),
            "sample_stable": bool(np.all(np.linalg.eigvalsh(transverse_hessian) > 0.0)),
        },
        "full_bdg_gate": {
            "projected_core_kernel_dimension": 1,
            "full_spectrum_kernel_dimension_proved": False,
            "required_argument": "bulk gap control or Feshbach-Schur reduction",
        },
        "next_gate": (
            "Derive the antisymmetric core operator from an allowed bulk action, fix "
            "global fermion parity completion, derive all Sigma coefficients, verify "
            "the transverse Hessian, and prove the full BdG gap."
        ),
    }

    assert results["representation_gate"]["constant_antisymmetric_invariant_dimension"] == 0
    assert results["representation_gate"]["dynamic_epsilon_terms_all_invariant"]
    assert results["rank_gate"]["rank_A_sigma"] == 2
    assert results["rank_gate"]["kernel_residual"] < 1e-12
    assert results["axis_stability_gate"]["sample_stable"]
    Path("s2t_dynamic_family_order_parameter_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()