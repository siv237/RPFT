#!/usr/bin/env python3
"""Audit the KO2 product Pfaffian and its normalization."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def antisymmetric_family_carrier(state: np.ndarray) -> np.ndarray:
    """Embed fifteen family blocks and an R-independent complement in M300."""
    family = np.kron(np.eye(15), state)
    zero_family = np.zeros_like(family)
    active = np.block([[zero_family, family], [-family.T, zero_family]])

    complement_half = np.eye(105)
    zero_complement = np.zeros_like(complement_half)
    complement = np.block(
        [[zero_complement, complement_half], [-complement_half, zero_complement]]
    )

    zero_ac = np.zeros((active.shape[0], complement.shape[0]))
    return np.block([[active, zero_ac], [-zero_ac.T, complement]])


def log_abs_pfaffian(matrix: np.ndarray) -> float:
    sign, logdet = np.linalg.slogdet(matrix)
    assert sign > 0
    return 0.5 * float(logdet)


def main() -> None:
    upper = Fraction(17, 168)
    ordinary_pfaffian_weight = Fraction(15, 1)
    normalized_fk_weight = Fraction(15, 300)

    rng = np.random.default_rng(20260819)
    reference = np.eye(3) / 3.0
    reference_carrier = antisymmetric_family_carrier(reference)
    reference_logpf = log_abs_pfaffian(reference_carrier)

    samples = []
    for _ in range(20):
        raw = rng.normal(size=(3, 3))
        state = raw @ raw.T + np.eye(3)
        state /= np.trace(state)

        carrier = antisymmetric_family_carrier(state)
        assert carrier.shape == (300, 300)
        assert np.linalg.norm(carrier + carrier.T) < 1e-12

        logdet_ratio = float(np.linalg.slogdet(state)[1] - np.linalg.slogdet(reference)[1])
        logpf_ratio = log_abs_pfaffian(carrier) - reference_logpf

        scaled = carrier / 300.0
        scaled_reference = reference_carrier / 300.0
        scaled_ratio = log_abs_pfaffian(scaled) - log_abs_pfaffian(scaled_reference)

        two_mode = np.kron(np.eye(2), carrier)
        two_mode_reference = np.kron(np.eye(2), reference_carrier)
        two_mode_ratio = log_abs_pfaffian(two_mode) - log_abs_pfaffian(
            two_mode_reference
        )

        samples.append(
            {
                "logdet_R_ratio": logdet_ratio,
                "ordinary_logpf_ratio": logpf_ratio,
                "target_15_logdet_ratio": 15.0 * logdet_ratio,
                "scaled_quadratic_form_logpf_ratio": scaled_ratio,
                "two_external_mode_logpf_ratio": two_mode_ratio,
                "target_30_logdet_ratio": 30.0 * logdet_ratio,
                "normalized_FK_logpf_ratio": logpf_ratio / 300.0,
                "target_one_over_20_logdet_ratio": logdet_ratio / 20.0,
            }
        )

    residuals = {
        "ordinary": max(
            abs(row["ordinary_logpf_ratio"] - row["target_15_logdet_ratio"])
            for row in samples
        ),
        "scaled_action": max(
            abs(
                row["scaled_quadratic_form_logpf_ratio"]
                - row["target_15_logdet_ratio"]
            )
            for row in samples
        ),
        "two_external_modes": max(
            abs(row["two_external_mode_logpf_ratio"] - row["target_30_logdet_ratio"])
            for row in samples
        ),
        "normalized_fk": max(
            abs(
                row["normalized_FK_logpf_ratio"]
                - row["target_one_over_20_logdet_ratio"]
            )
            for row in samples
        ),
    }

    gaussian_lattice = sorted(
        {
            Fraction(n, 2)
            for n in range(-40, 41)
            if Fraction(n, 2) > 0
        }
    )
    minimum_positive_gaussian_weight = gaussian_lattice[0]

    result = {
        "gate": "version6_product_ko2_family_pfaffian_operator_gate",
        "ko_dimension": {
            "external": 4,
            "internal": 6,
            "sum_mod_8": (4 + 6) % 8,
            "chiral_pfaffian_allowed": True,
        },
        "carrier": {
            "total_dimension": 300,
            "active_real_pair_dimension": 90,
            "R_independent_complement_dimension": 210,
            "family_copies_in_pfaffian": 15,
        },
        "weights": {
            "ordinary_Berezin_pfaffian": str(ordinary_pfaffian_weight),
            "normalized_Fuglede_Kadison_pfaffian": str(normalized_fk_weight),
            "admissible_upper_bound": str(upper),
            "ordinary_inside_window": ordinary_pfaffian_weight < upper,
            "normalized_inside_window": normalized_fk_weight < upper,
        },
        "normalization_test": {
            "statement": "Pf(c A_R)/Pf(c A_R0) = Pf(A_R)/Pf(A_R0)",
            "quadratic_action_scale": "1/300",
            "R_dependent_exponent_after_scaling": "15",
            "normalized_log_pfaffian_requires_postprocessing": "(1/300) log|Pf A_R|",
            "samples": samples,
            "maximum_residuals": residuals,
        },
        "finite_gaussian_exponent_lattice": {
            "lattice": "(1/2) Z",
            "minimum_positive_weight": str(minimum_positive_gaussian_weight),
            "minimum_exceeds_admissible_window": minimum_positive_gaussian_weight > upper,
        },
        "verdict": {
            "product_KO2_kinematics_pass": True,
            "ordinary_fermion_integral_yields_fractional_barrier": False,
            "M210_vs_M300_denominator_selects_standard_pfaffian": False,
            "normalized_intensive_free_energy_remains_possible": True,
            "parent_measure_closed": False,
            "next_gate": "version6_common_intensive_free_energy_normalization_gate",
        },
    }

    assert result["ko_dimension"]["sum_mod_8"] == 2
    assert ordinary_pfaffian_weight == 15
    assert normalized_fk_weight == Fraction(1, 20)
    assert ordinary_pfaffian_weight > upper
    assert normalized_fk_weight < upper
    assert minimum_positive_gaussian_weight == Fraction(1, 2)
    assert minimum_positive_gaussian_weight > upper
    assert max(residuals.values()) < 1e-10
    assert math.isclose(float(normalized_fk_weight), 0.05)

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_product_ko2_family_pfaffian_operator_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()