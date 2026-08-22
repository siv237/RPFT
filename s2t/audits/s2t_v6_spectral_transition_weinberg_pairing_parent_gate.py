#!/usr/bin/env python3
"""Аудит родительского происхождения паринга Вайнберга."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_weinberg_pairing_parent_gate_results.json"


def symmetric_basis() -> list[np.ndarray]:
    out = []
    for i in range(3):
        for j in range(i, 3):
            m = np.zeros((3, 3), dtype=complex)
            m[i, j] = 1.0
            m[j, i] = 1.0
            out.append(m)
    return out


def main() -> None:
    line = json.loads((RESULTS / "s2t_v6_spectral_transition_neutrino_line_parent_gate_results.json").read_text())
    pairing = json.loads((RESULTS / "s2t_v5_h15_majorana_pairing_correspondence_gate_results.json").read_text())
    measure = json.loads((RESULTS / "s2t_v5_h15_fermionic_spectral_weinberg_measure_gate_results.json").read_text())

    c3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    basis = symmetric_basis()
    constraint = np.column_stack([(c3.T @ b @ c3 - b).reshape(-1) for b in basis])
    _, singular, vh = np.linalg.svd(constraint)
    nullity = int(np.sum(singular < 1e-10))
    invariant_coefficients = vh.conj().T[:, -nullity:]
    invariant_matrices = [sum(coeff[k] * basis[k] for k in range(6)) for coeff in invariant_coefficients.T]

    p0 = (np.eye(3) + c3 + c3 @ c3) / 3
    compressed = np.column_stack([(p0 @ m @ p0).reshape(-1) for m in invariant_matrices])
    compressed_dimension = int(np.linalg.matrix_rank(compressed, tol=1e-10))
    compression_residual = max(
        float(np.linalg.norm(p0 @ m @ p0 - np.trace(p0 @ m) * p0))
        for m in invariant_matrices
    )

    z = np.linspace(-8.0, 8.0, 200001)
    kernel = np.exp(-z**2)
    denom = float(np.trapezoid(kernel**2, z))
    rows = []
    odd_reference = None
    odd_residual = 0.0
    for alpha in (0.0, 1.0, 2.0):
        g = z * kernel + alpha * kernel
        gm = (-z) * kernel + alpha * kernel
        even = (g + gm) / 2
        odd = (g - gm) / 2
        if odd_reference is None:
            odd_reference = odd
        odd_residual = max(odd_residual, float(np.linalg.norm(odd - odd_reference) / np.sqrt(len(z))))
        even_coefficient = float(np.trapezoid(even * kernel, z) / denom)
        rows.append({
            "alpha": alpha,
            "odd_kinetic_norm": float(np.trapezoid(np.abs(odd) ** 2, z)),
            "even_Weinberg_coefficient": even_coefficient,
        })

    weights = [1 / 7, 2 / 7, 1.0]
    zpsi = 1.7
    mu = 0.03
    normalized_masses = [float((w * mu) / (w * zpsi)) for w in weights]

    charged_controls = [np.diag([1.0, 4.0, 9.0]), np.diag([2.0, 2.0, 2.0])]
    kappas = [float(np.trace(p0 @ k).real) for k in charged_controls]
    family_compression_residuals = [
        float(np.linalg.norm(p0 @ k @ p0 - kap * p0))
        for k, kap in zip(charged_controls, kappas)
    ]

    result = {
        "gate": "version6_spectral_transition_weinberg_pairing_parent_gate",
        "input_certificates": {
            "regular_weak_support": line["verdict"]["polynomial_neutrino_transition_support_exists"],
            "normalized_line_parent_closed": line["verdict"]["normalized_neutrino_line_parent_closed"],
            "V5_family_direction": pairing["verdict"]["canonical_zero_branch_family_direction"],
            "V5_parameter_free_amplitude": measure["verdict"]["parameter_free_Weinberg_amplitude"],
        },
        "operator_type": {
            "H15_has_right_handed_neutrino": False,
            "lowest_neutrino_mass_route": "dimension-five Weinberg pairing",
            "weak_support": "B_nu(H)=tilde(H) tilde(H)^T",
            "weak_contraction_dimension": 1,
            "lepton_number_change": 2,
            "operator_type_admissible": True,
        },
        "family_tensor_audit": {
            "unconstrained_complex_symmetric_dimension": 6,
            "C3_invariant_symmetric_dimension": nullity,
            "general_C3_form": "x P0 + y (I-P0)",
            "dimension_after_P0_compression": compressed_dimension,
            "compression_to_scalar_P0_residual": compression_residual,
            "family_direction_after_zero_branch_compression": "P0",
            "overall_complex_amplitude_fixed": False,
        },
        "spectral_measure_no_go": {
            "counterfamily": "g_alpha(z)=z exp(-z^2)+alpha exp(-z^2)",
            "rows": rows,
            "odd_part_common_residual": odd_residual,
            "kinetic_normalization_fixes_even_coefficient": False,
            "even_coefficient_can_vanish_or_vary_continuously": True,
        },
        "trace_weight_audit": {
            "tested_common_weights": weights,
            "canonical_masses_after_field_normalization": normalized_masses,
            "mass_spread": float(np.ptp(normalized_masses)),
            "one_seventh_is_channel_weight_not_mass": True,
        },
        "charged_lepton_factor_boundary": {
            "identity": "P0 K_e P0=kappa_e P0",
            "sample_kappas": kappas,
            "compression_residuals": family_compression_residuals,
            "direction_fixed": True,
            "kappa_e_fixed_by_parent": False,
        },
        "remaining_amplitude": {
            "schematic": "m_nu ~ r_tau kappa_e v_H^2/Lambda",
            "independent_underived_inputs": [
                "even/odd spectral-moment ratio r_tau",
                "charged-lepton contraction kappa_e",
                "suppression scale Lambda",
                "absolute Higgs scale v_H",
            ],
            "underived_input_count_at_least": 4,
            "localized_rank_change_profile_derived": False,
        },
        "verdict": {
            "Weinberg_operator_type_parent_admissible": True,
            "weak_direction_fixed": True,
            "family_zero_branch_direction_fixed": True,
            "full_family_tensor_fixed_without_compression": False,
            "coefficient_and_scale_parent_derived": False,
            "parameter_free_neutrino_mass": False,
            "current_parent_closes_Weinberg_pairing": False,
            "physical_closure": False,
            "status": "the parent fixes the weak support and one compressed family channel, but an explicit counterfamily leaves the even spectral coefficient free; the 1/7 trace weight cancels and the mass scale remains external",
        },
        "next_gate": "version6_spectral_transition_rank_change_localization_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()