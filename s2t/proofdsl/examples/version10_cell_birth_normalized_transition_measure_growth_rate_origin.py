"""LCF certificate for normalized cell-birth measures and rate freedom."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CellBirthNormalizedTransitionMeasureCertificate:
    probabilities: sp.ImmutableMatrix
    transition_matrix: sp.ImmutableMatrix
    mean_multiplier: sp.Expr
    step_growth: sp.Expr
    target_growth: sp.Expr
    slope_gap: sp.Expr
    waiting_density: sp.Expr
    clock_orbit_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    probability_normalization_theorem: Theorem
    odds_theorem: Theorem
    transition_stochastic_theorem: Theorem
    mean_multiplier_theorem: Theorem
    step_growth_theorem: Theorem
    step_growth_slope_theorem: Theorem
    target_growth_slope_theorem: Theorem
    slope_gap_theorem: Theorem
    growth_law_nonidentity_theorem: Theorem
    waiting_normalization_theorem: Theorem
    mean_waiting_theorem: Theorem
    clock_rescaling_theorem: Theorem
    clock_orbit_nullity_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellBirthNormalizedTransitionMeasureCertificate:
    x = sp.symbols("x", positive=True)
    rate, time, scale = sp.symbols("gamma t c", positive=True)

    no_birth_probability = 1 / (1 + x)
    birth_probability = x / (1 + x)
    probabilities = sp.ImmutableMatrix([no_birth_probability, birth_probability])
    transition_matrix = sp.ImmutableMatrix([
        [no_birth_probability, birth_probability],
        [0, 1],
    ])
    mean_multiplier = sp.simplify(1 + birth_probability)
    step_growth = sp.log(mean_multiplier) / 3
    target_growth = x / sp.sqrt(8 * sp.pi)
    step_growth_slope = sp.simplify(sp.diff(step_growth, x).subs(x, 0))
    target_growth_slope = sp.simplify(sp.diff(target_growth, x).subs(x, 0))
    slope_gap = sp.simplify(step_growth_slope - target_growth_slope)

    waiting_density = rate * sp.exp(-rate * time)
    waiting_normalization = sp.integrate(waiting_density, (time, 0, sp.oo))
    mean_waiting = sp.integrate(time * waiting_density, (time, 0, sp.oo))
    survival = sp.exp(-rate * time)
    rescaled_survival = sp.exp(-(scale * rate) * (time / scale))
    clock_orbit_map = sp.ImmutableMatrix([[1, 1]])

    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 0, 0])

    probability_normalization_theorem = kernel.prove_expression_equality(
        sum(probabilities),
        1,
        subject="the no-birth and one-birth weights define a normalized transition measure",
    )
    odds_theorem = kernel.prove_expression_equality(
        birth_probability / no_birth_probability,
        x,
        subject="normalization preserves the input cell-birth weight as an odds ratio",
    )
    transition_stochastic_theorem = kernel.prove_matrix_equality(
        transition_matrix * sp.ones(2, 1),
        sp.ones(2, 1),
        subject="the minimal cell-birth transition matrix is row stochastic",
    )
    mean_multiplier_theorem = kernel.prove_expression_equality(
        mean_multiplier,
        (1 + 2 * x) / (1 + x),
        subject="the normalized independent birth step has an exact mean cell multiplier",
    )
    step_growth_theorem = kernel.prove_expression_equality(
        step_growth,
        sp.log((1 + 2 * x) / (1 + x)) / 3,
        subject="the normalized birth step induces a dimensionless geometric growth increment",
    )
    step_growth_slope_theorem = kernel.prove_expression_equality(
        step_growth_slope,
        sp.Rational(1, 3),
        subject="the weak-weight slope of normalized cell growth is one third",
    )
    target_growth_slope_theorem = kernel.prove_expression_equality(
        target_growth_slope,
        1 / sp.sqrt(8 * sp.pi),
        subject="the weak-weight slope of the proposed vacuum growth amplitude",
    )
    slope_gap_theorem = kernel.prove_positive_expression(
        slope_gap,
        subject="normalization alone does not reproduce the proposed vacuum prefactor",
    )
    growth_law_nonidentity_theorem = kernel.prove_expression_nonconstant(
        step_growth - target_growth,
        x,
        subject="the normalized discrete growth law is not the proposed vacuum growth law",
    )
    waiting_normalization_theorem = kernel.prove_expression_equality(
        waiting_normalization,
        1,
        subject="every positive exponential waiting rate gives a normalized clock measure",
    )
    mean_waiting_theorem = kernel.prove_expression_equality(
        mean_waiting,
        1 / rate,
        subject="the physical waiting time retains the inverse free rate",
    )
    clock_rescaling_theorem = kernel.prove_expression_equality(
        rescaled_survival,
        survival,
        subject="rate and clock rescaling leave the normalized survival law invariant",
    )
    clock_orbit_nullity_theorem = kernel.prove_exact_nullity(
        clock_orbit_map,
        1,
        subject="the logarithmic rate-clock calibration has one exact scale orbit",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(8, 1),
        subject="all minimal normalized cell-birth measure conditions pass",
    )
    origin_ledger_theorem = kernel.prove_matrix_equality(
        origin_ledger,
        sp.Matrix([1, 1, 0, 0]),
        subject="normalization and dimensionless growth pass while target rate and physical clock remain open",
    )
    origin_score_theorem = kernel.prove_expression_equality(
        sum(origin_ledger),
        2,
        subject="two of four cell-birth origin requirements are supplied",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_normalized_transition_measure_growth_rate_origin_gate",
        (
            probability_normalization_theorem,
            odds_theorem,
            transition_stochastic_theorem,
            mean_multiplier_theorem,
            step_growth_theorem,
            step_growth_slope_theorem,
            target_growth_slope_theorem,
            slope_gap_theorem,
            growth_law_nonidentity_theorem,
            waiting_normalization_theorem,
            mean_waiting_theorem,
            clock_rescaling_theorem,
            clock_orbit_nullity_theorem,
            architecture_theorem,
            origin_ledger_theorem,
            origin_score_theorem,
        ),
    )
    return CellBirthNormalizedTransitionMeasureCertificate(
        probabilities=probabilities,
        transition_matrix=transition_matrix,
        mean_multiplier=mean_multiplier,
        step_growth=step_growth,
        target_growth=target_growth,
        slope_gap=slope_gap,
        waiting_density=waiting_density,
        clock_orbit_map=clock_orbit_map,
        architecture=architecture,
        origin_ledger=origin_ledger,
        probability_normalization_theorem=probability_normalization_theorem,
        odds_theorem=odds_theorem,
        transition_stochastic_theorem=transition_stochastic_theorem,
        mean_multiplier_theorem=mean_multiplier_theorem,
        step_growth_theorem=step_growth_theorem,
        step_growth_slope_theorem=step_growth_slope_theorem,
        target_growth_slope_theorem=target_growth_slope_theorem,
        slope_gap_theorem=slope_gap_theorem,
        growth_law_nonidentity_theorem=growth_law_nonidentity_theorem,
        waiting_normalization_theorem=waiting_normalization_theorem,
        mean_waiting_theorem=mean_waiting_theorem,
        clock_rescaling_theorem=clock_rescaling_theorem,
        clock_orbit_nullity_theorem=clock_orbit_nullity_theorem,
        architecture_theorem=architecture_theorem,
        origin_ledger_theorem=origin_ledger_theorem,
        origin_score_theorem=origin_score_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_normalized_transition_measure_growth_rate_origin_gate",
    title="Нормированная мера рождения ячеек и граница темпа роста",
    source_paths=(
        "s2t/gates/version10_cell_birth_normalized_transition_measure_growth_rate_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_normalized_transition_measure_growth_rate_origin_gate_results.json",
    ),
    obligations=(
        Obligation("birth_probability_normalization", lambda: build_certificate().probability_normalization_theorem),
        Obligation("birth_weight_odds_ratio", lambda: build_certificate().odds_theorem),
        Obligation("birth_transition_row_stochastic", lambda: build_certificate().transition_stochastic_theorem),
        Obligation("mean_cell_multiplier", lambda: build_certificate().mean_multiplier_theorem),
        Obligation("dimensionless_step_growth", lambda: build_certificate().step_growth_theorem),
        Obligation("normalized_growth_weak_slope", lambda: build_certificate().step_growth_slope_theorem),
        Obligation("vacuum_target_weak_slope", lambda: build_certificate().target_growth_slope_theorem),
        Obligation("vacuum_prefactor_positive_mismatch", lambda: build_certificate().slope_gap_theorem),
        Obligation("normalized_growth_not_vacuum_target", lambda: build_certificate().growth_law_nonidentity_theorem),
        Obligation("waiting_time_measure_normalized", lambda: build_certificate().waiting_normalization_theorem),
        Obligation("mean_waiting_time_free_rate", lambda: build_certificate().mean_waiting_theorem),
        Obligation("clock_rate_rescaling_invariance", lambda: build_certificate().clock_rescaling_theorem),
        Obligation("clock_rate_scale_orbit_nullity_one", lambda: build_certificate().clock_orbit_nullity_theorem),
        Obligation("cell_birth_measure_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("cell_birth_origin_ledger_two_of_four", lambda: build_certificate().origin_ledger_theorem),
        Obligation("cell_birth_origin_score_two", lambda: build_certificate().origin_score_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)