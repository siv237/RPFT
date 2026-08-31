#!/usr/bin/env python3
"""Exact audit of permutation-covariant three-particle noise lifts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_three_particle_lift_normalization_gate_results.json"


def kron3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def exact(expr: sp.Expr) -> str:
    return str(sp.factor(sp.cancel(expr)))


def main() -> None:
    x = sp.symbols("x", positive=True)
    c = sp.symbols("c", real=True)
    identity2 = sp.eye(2)
    pauli = [
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.Matrix([[1, 0], [0, -1]]) / 2,
    ]

    total_generators = []
    for generator in pauli:
        total_generators.append(
            kron3(generator, identity2, identity2)
            + kron3(identity2, generator, identity2)
            + kron3(identity2, identity2, generator)
        )
    isospin_square = sp.simplify(
        sum((generator * generator for generator in total_generators), sp.zeros(8, 8))
    )
    projector_symmetric = sp.simplify((isospin_square - sp.Rational(3, 4) * sp.eye(8)) / 3)
    projector_mixed = sp.eye(8) - projector_symmetric

    symmetric_projector_exact = sp.simplify(
        projector_symmetric**2 - projector_symmetric
    ) == sp.zeros(8, 8)
    mixed_projector_exact = sp.simplify(projector_mixed**2 - projector_mixed) == sp.zeros(8, 8)
    decomposition_exact = sp.simplify(
        isospin_square
        - sp.Rational(15, 4) * projector_symmetric
        - sp.Rational(3, 4) * projector_mixed
    ) == sp.zeros(8, 8)

    # Copy-space covariance of a permutation-invariant three-particle lift.
    copy_covariance = (1 - c) * sp.eye(3) + c * sp.ones(3, 3)
    copy_eigenvalues = [1 - c, 1 - c, 1 + 2 * c]

    a = 1 / (11 + 10 * x)
    b = x / (11 + 10 * x)
    ab = sp.factor(a + b)
    kappa2 = sp.factor(1 / ((5 * a + b) / 2))
    transfer_scalar = sp.factor(x / (2 * ab) + x / (13 * ab))
    kappa1 = sp.factor(1 / ((13 * a + 25 * b) / 6))

    # Additive transfer losses are fixed.  Correlated weak noise contributes
    # c times the off-diagonal part of the total isospin Casimir.
    additive_weak = sp.Rational(9, 4) * kappa2
    weak_cross = sp.simplify(isospin_square - sp.Rational(9, 4) * sp.eye(8))
    mass_operator = sp.simplify(
        (3 * transfer_scalar + additive_weak + kappa1 / 4) * sp.eye(8)
        + c * kappa2 * weak_cross
    )
    symmetric_level = sp.factor(
        3 * transfer_scalar + additive_weak + kappa1 / 4 + sp.Rational(3, 2) * c * kappa2
    )
    mixed_level = sp.factor(
        3 * transfer_scalar + additive_weak + kappa1 / 4 - sp.Rational(3, 2) * c * kappa2
    )
    level_decomposition_exact = sp.simplify(
        mass_operator
        - symmetric_level * projector_symmetric
        - mixed_level * projector_mixed
    ) == sp.zeros(8, 8)
    split3 = sp.factor(symmetric_level - mixed_level)
    split2 = sp.factor(2 * c * kappa2)

    r1 = sp.factor(
        transfer_scalar
        + sp.Rational(4, 3) / ab
        + sp.Rational(3, 2) / (5 * a + b)
        + sp.Rational(1, 6) / (13 * a + 25 * b)
    )
    discriminator = sp.factor(split3 / (3 * r1))
    collective_discriminator = sp.factor(discriminator.subs(c, 1))
    target = sp.Rational(977, 3490)
    target_gap = sp.factor(target - collective_discriminator)
    target_gap_numerator = sp.together(target_gap).as_numer_denom()[0]
    gap_lower_certificate = sp.factor(
        358774 - sp.Rational(711068, 49)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_three_particle_lift_normalization_gate",
        "field": "Q(x,c), x=exp(-2)",
        "isospin_decomposition": {
            "symmetric_projector_rank": int(projector_symmetric.rank()),
            "mixed_projector_rank": int(projector_mixed.rank()),
            "symmetric_projector_exact": symmetric_projector_exact,
            "mixed_projector_exact": mixed_projector_exact,
            "casimir_decomposition_exact": decomposition_exact,
            "symmetric_isospin_square": "15/4",
            "mixed_isospin_square": "3/4",
        },
        "copy_covariance": {
            "matrix": str(copy_covariance),
            "eigenvalues": [exact(value) for value in copy_eigenvalues],
            "complete_positivity_interval": "-1/2 <= c <= 1",
            "independent_lift": "c=0",
            "collective_lift": "c=1",
            "same_one_particle_generator": True,
        },
        "three_particle_operator": {
            "transfer_scalar_per_particle": exact(transfer_scalar),
            "kappa_SU2": exact(kappa2),
            "symmetric_level": exact(symmetric_level),
            "mixed_level": exact(mixed_level),
            "level_decomposition_exact": level_decomposition_exact,
            "split3": exact(split3),
            "split2": exact(split2),
            "split3_over_split2": exact(sp.factor(split3 / split2)),
            "additive_three_over_one": "3",
        },
        "discriminator_family": {
            "value": exact(discriminator),
            "collective_value": exact(collective_discriminator),
            "collective_display_at_exp_minus_2": format(
                float(sp.N(collective_discriminator.subs(x, sp.exp(-2)), 17)), ".15g"
            ),
            "target": "977/3490",
            "target_minus_collective": exact(target_gap),
            "gap_numerator": exact(target_gap_numerator),
            "positive_lower_certificate_for_0_x_lt_1_over_7": exact(gap_lower_certificate),
            "target_above_all_cp_lifts_at_exp_minus_2_exact": True,
        },
        "status_boundary": {
            "additive_tensor_factor_three_exact": True,
            "three_over_two_split_ratio_exact": True,
            "one_particle_qms_selects_copy_correlation": False,
            "permutation_symmetry_selects_copy_correlation": False,
            "collective_lift_is_additional_assumption": True,
            "physical_mass_theorem": False,
        },
        "verdict": {
            "unique_three_particle_lift": False,
            "correlation_parameter_interval": "[-1/2,1]",
            "next_gate": "version8_baryon_common_environment_correlation_origin_gate",
        },
    }

    assert symmetric_projector_exact and mixed_projector_exact
    assert projector_symmetric.rank() == projector_mixed.rank() == 4
    assert decomposition_exact and level_decomposition_exact
    assert sp.factor(split3 / split2) == sp.Rational(3, 2)
    assert sp.factor(split3.subs(c, 1) - 3 * kappa2) == 0
    assert gap_lower_certificate > 0
    # For 0<x<1/7 the positive terms of the numerator can be dropped and
    # -711068*x^2 > -711068/49, leaving a strictly positive lower bound.
    assert target_gap_numerator == 366375 * x**3 - 711068 * x**2 + 203619 * x + 358774

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()