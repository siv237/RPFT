"""LCF certificate for the KMS reservoir spectral-density origin gate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSReservoirSpectralDensityOriginCertificate:
    evaluation_map: sp.ImmutableMatrix
    kernel_profile_coefficients: sp.ImmutableMatrix
    baseline_rates: sp.ImmutableMatrix
    perturbed_rates: sp.ImmutableMatrix
    normalization_map: sp.ImmutableMatrix
    evaluation_rank_theorem: Theorem
    kernel_profile_theorem: Theorem
    equal_rates_theorem: Theorem
    baseline_moment_theorem: Theorem
    perturbed_moment_theorem: Theorem
    moment_defect_theorem: Theorem
    baseline_first_moment_theorem: Theorem
    perturbed_first_moment_theorem: Theorem
    first_moment_defect_theorem: Theorem
    normalization_rank_theorem: Theorem
    rate_difference_theorem: Theorem
    offshell_difference_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSReservoirSpectralDensityOriginCertificate:
    w = sp.symbols("omega", real=True)
    basis = sp.Matrix([w**degree for degree in range(7)])
    evaluation_map = sp.ImmutableMatrix([
        [sp.Integer(delta) ** degree for degree in range(7)]
        for delta in (1, 2, 3)
    ])
    q = sp.expand((w - 1) ** 2 * (w - 2) ** 2 * (w - 3) ** 2)
    kernel_profile_coefficients = sp.ImmutableMatrix([
        sp.expand(q).coeff(w, degree) for degree in range(7)
    ])
    baseline = sp.Integer(1)
    perturbed = sp.Integer(1) + q / 16
    baseline_rates = sp.ImmutableMatrix([baseline.subs(w, d) for d in (1, 2, 3)])
    perturbed_rates = sp.ImmutableMatrix([perturbed.subs(w, d) for d in (1, 2, 3)])
    baseline_moment = sp.integrate(baseline, (w, 0, 4))
    perturbed_moment = sp.integrate(perturbed, (w, 0, 4))
    baseline_first_moment = sp.integrate(w * baseline, (w, 0, 4))
    perturbed_first_moment = sp.integrate(w * perturbed, (w, 0, 4))
    normalization_map = sp.ImmutableMatrix([[1, 1, 3]])
    z = sp.symbols("z", nonzero=True)
    baseline_asymptotic = baseline_moment / z + baseline_first_moment / z**2
    perturbed_asymptotic = perturbed_moment / z + perturbed_first_moment / z**2

    evaluation_rank_theorem = kernel.prove_exact_rank(
        evaluation_map,
        3,
        subject="three on shell gaps constrain only three polynomial spectral coordinates",
    )
    kernel_profile_theorem = kernel.prove_matrix_equality(
        evaluation_map * kernel_profile_coefficients,
        sp.zeros(3, 1),
        subject="the squared three gap polynomial is invisible to all on shell rates",
    )
    equal_rates_theorem = kernel.prove_matrix_equality(
        perturbed_rates,
        baseline_rates,
        subject="positive off shell deformation preserves the three conductances",
    )
    baseline_moment_theorem = kernel.prove_expression_equality(
        baseline_moment,
        4,
        subject="zeroth moment of the flat spectral profile",
    )
    perturbed_moment_theorem = kernel.prove_expression_equality(
        perturbed_moment,
        sp.Rational(527, 105),
        subject="zeroth moment of the deformed spectral profile",
    )
    moment_defect_theorem = kernel.prove_positive_expression(
        perturbed_moment - baseline_moment,
        subject="equal on shell rates admit a strict zeroth spectral moment defect",
    )
    baseline_first_moment_theorem = kernel.prove_expression_equality(
        baseline_first_moment,
        8,
        subject="first moment of the flat spectral profile",
    )
    perturbed_first_moment_theorem = kernel.prove_expression_equality(
        perturbed_first_moment,
        sp.Rational(1054, 105),
        subject="first moment of the deformed spectral profile",
    )
    first_moment_defect_theorem = kernel.prove_positive_expression(
        perturbed_first_moment - baseline_first_moment,
        subject="equal on shell rates admit a strict first spectral moment defect",
    )
    normalization_rank_theorem = kernel.prove_exact_rank(
        normalization_map,
        1,
        subject="one weighted rate normalization leaves two relative type strengths",
    )
    rate_difference_theorem = kernel.prove_matrix_equality(
        perturbed_rates - baseline_rates,
        sp.zeros(3, 1),
        subject="the exact rate vector cannot see the off shell profile deformation",
    )
    offshell_difference_theorem = kernel.prove_expression_nonconstant(
        sp.simplify(perturbed_asymptotic - baseline_asymptotic),
        z,
        subject="the off shell self energy asymptotics changes despite equal rates",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_reservoir_spectral_"
        "density_parent_origin_gate",
        (
            evaluation_rank_theorem,
            kernel_profile_theorem,
            equal_rates_theorem,
            baseline_moment_theorem,
            perturbed_moment_theorem,
            moment_defect_theorem,
            baseline_first_moment_theorem,
            perturbed_first_moment_theorem,
            first_moment_defect_theorem,
            normalization_rank_theorem,
            rate_difference_theorem,
            offshell_difference_theorem,
        ),
    )
    return KMSReservoirSpectralDensityOriginCertificate(
        evaluation_map=evaluation_map,
        kernel_profile_coefficients=kernel_profile_coefficients,
        baseline_rates=baseline_rates,
        perturbed_rates=perturbed_rates,
        normalization_map=normalization_map,
        evaluation_rank_theorem=evaluation_rank_theorem,
        kernel_profile_theorem=kernel_profile_theorem,
        equal_rates_theorem=equal_rates_theorem,
        baseline_moment_theorem=baseline_moment_theorem,
        perturbed_moment_theorem=perturbed_moment_theorem,
        moment_defect_theorem=moment_defect_theorem,
        baseline_first_moment_theorem=baseline_first_moment_theorem,
        perturbed_first_moment_theorem=perturbed_first_moment_theorem,
        first_moment_defect_theorem=first_moment_defect_theorem,
        normalization_rank_theorem=normalization_rank_theorem,
        rate_difference_theorem=rate_difference_theorem,
        offshell_difference_theorem=offshell_difference_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_reservoir_spectral_"
        "density_parent_origin_gate"
    ),
    title="Parent-origin reservoir spectral density для KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_reservoir_"
        "spectral_density_parent_origin_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_"
        "spectral_density_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("on_shell_evaluation_rank_three", lambda: build_certificate().evaluation_rank_theorem),
        Obligation("off_shell_kernel_profile", lambda: build_certificate().kernel_profile_theorem),
        Obligation("equal_on_shell_rates", lambda: build_certificate().equal_rates_theorem),
        Obligation("flat_zeroth_moment", lambda: build_certificate().baseline_moment_theorem),
        Obligation("deformed_zeroth_moment", lambda: build_certificate().perturbed_moment_theorem),
        Obligation("positive_zeroth_moment_defect", lambda: build_certificate().moment_defect_theorem),
        Obligation("flat_first_moment", lambda: build_certificate().baseline_first_moment_theorem),
        Obligation("deformed_first_moment", lambda: build_certificate().perturbed_first_moment_theorem),
        Obligation("positive_first_moment_defect", lambda: build_certificate().first_moment_defect_theorem),
        Obligation("rate_normalization_rank_one", lambda: build_certificate().normalization_rank_theorem),
        Obligation("rate_vector_blindness", lambda: build_certificate().rate_difference_theorem),
        Obligation("offshell_self_energy_difference", lambda: build_certificate().offshell_difference_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)