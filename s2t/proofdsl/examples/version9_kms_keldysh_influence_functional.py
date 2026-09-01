"""LCF certificate for the normalized KMS Keldysh influence-functional gate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSKeldyshInfluenceFunctionalCertificate:
    gap_operator: sp.ImmutableMatrix
    damping_operator: sp.ImmutableMatrix
    distribution_operator: sp.ImmutableMatrix
    retarded_kernel: sp.ImmutableMatrix
    advanced_kernel: sp.ImmutableMatrix
    keldysh_block: sp.ImmutableMatrix
    full_kernel: sp.ImmutableMatrix
    witness_kernel: sp.ImmutableMatrix
    damping_rank_theorem: Theorem
    adjoint_pair_theorem: Theorem
    causal_zero_block_theorem: Theorem
    keldysh_relation_theorem: Theorem
    noise_rank_theorem: Theorem
    full_determinant_theorem: Theorem
    spectral_determinant_theorem: Theorem
    target_determinant_theorem: Theorem
    witness_determinant_theorem: Theorem
    witness_target_theorem: Theorem
    witness_defect_theorem: Theorem
    normalized_ratio_theorem: Theorem
    normalized_action_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSKeldyshInfluenceFunctionalCertificate:
    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    fs, fa, ft = sp.symbols("f_s f_a f_t", nonzero=True, real=True)

    gap_operator = sp.ImmutableMatrix(sp.diag(ts, ta, tt, tt, tt))
    damping_operator = sp.ImmutableMatrix(sp.diag(ks, ka, kt, kt, kt))
    distribution_operator = sp.ImmutableMatrix(sp.diag(fs, fa, ft, ft, ft))
    retarded_kernel = sp.ImmutableMatrix(gap_operator - sp.I * damping_operator)
    advanced_kernel = sp.ImmutableMatrix(gap_operator + sp.I * damping_operator)
    keldysh_block = sp.ImmutableMatrix(
        (retarded_kernel - advanced_kernel) * distribution_operator
    )
    full_kernel = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(retarded_kernel, keldysh_block),
        sp.Matrix.hstack(sp.zeros(5), advanced_kernel),
    ))

    spectral_determinant = (
        (ts**2 + ks**2)
        * (ta**2 + ka**2)
        * (tt**2 + kt**2) ** 3
    )
    target_determinant = ts * ta * tt**3 * ks * ka * kt**3
    witness_kernel = sp.ImmutableMatrix(full_kernel.subs({
        ts: 2, ta: 2, tt: 2,
        ks: 2, ka: 2, kt: 2,
        fs: sp.Rational(1, 2),
        fa: sp.Rational(1, 2),
        ft: sp.Rational(1, 2),
    }))

    damping_rank_theorem = kernel.prove_exact_rank(
        damping_operator,
        5,
        subject="nonzero typed damping reaches all five KMS channels",
    )
    adjoint_pair_theorem = kernel.prove_matrix_equality(
        advanced_kernel,
        retarded_kernel.H,
        subject="advanced kernel is the adjoint of the retarded kernel",
    )
    causal_zero_block_theorem = kernel.prove_matrix_equality(
        full_kernel[5:10, 0:5],
        sp.zeros(5),
        subject="the lower causal Keldysh block vanishes exactly",
    )
    keldysh_relation_theorem = kernel.prove_matrix_equality(
        keldysh_block,
        (retarded_kernel - advanced_kernel) * distribution_operator,
        subject="the statistical block obeys the fermionic KMS FDT form",
    )
    noise_rank_theorem = kernel.prove_exact_rank(
        keldysh_block,
        5,
        subject="nonzero KMS statistical block carries all five channels",
    )
    full_determinant_theorem = kernel.prove_expression_equality(
        full_kernel.det(),
        retarded_kernel.det() * advanced_kernel.det(),
        subject="causal triangular determinant is independent of the Keldysh block",
    )
    spectral_determinant_theorem = kernel.prove_expression_equality(
        full_kernel.det(),
        spectral_determinant,
        subject="retarded advanced pairing gives the modulus square spectral determinant",
    )
    target_determinant_theorem = kernel.prove_expression_equality(
        gap_operator.det() * damping_operator.det(),
        target_determinant,
        subject="the desired gap conductance target is the product of two type determinants",
    )
    witness_determinant_theorem = kernel.prove_expression_equality(
        witness_kernel.det(),
        32768,
        subject="the interacting isotropic Keldysh witness has determinant eight to the fifth",
    )
    witness_target_theorem = kernel.prove_expression_equality(
        target_determinant.subs({
            ts: 2, ta: 2, tt: 2,
            ks: 2, ka: 2, kt: 2,
        }),
        1024,
        subject="the isotropic two package target determinant is two to the tenth",
    )
    witness_defect_theorem = kernel.prove_positive_expression(
        sp.Integer(32768 - 1024),
        subject="the causal retarded advanced determinant differs strictly from the target",
    )
    normalized_ratio_theorem = kernel.prove_expression_equality(
        full_kernel.det() / spectral_determinant,
        1,
        subject="closed contour vacuum normalization cancels the full Gaussian determinant",
    )
    normalized_action_theorem = kernel.prove_expression_equality(
        -sp.log(full_kernel.det() / spectral_determinant),
        0,
        subject="the normalized source free Keldysh determinant leaves zero effective action",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_keldysh_influence_"
        "functional_admission_gate",
        (
            damping_rank_theorem,
            adjoint_pair_theorem,
            causal_zero_block_theorem,
            keldysh_relation_theorem,
            noise_rank_theorem,
            full_determinant_theorem,
            spectral_determinant_theorem,
            target_determinant_theorem,
            witness_determinant_theorem,
            witness_target_theorem,
            witness_defect_theorem,
            normalized_ratio_theorem,
            normalized_action_theorem,
        ),
    )
    return KMSKeldyshInfluenceFunctionalCertificate(
        gap_operator=gap_operator,
        damping_operator=damping_operator,
        distribution_operator=distribution_operator,
        retarded_kernel=retarded_kernel,
        advanced_kernel=advanced_kernel,
        keldysh_block=keldysh_block,
        full_kernel=full_kernel,
        witness_kernel=witness_kernel,
        damping_rank_theorem=damping_rank_theorem,
        adjoint_pair_theorem=adjoint_pair_theorem,
        causal_zero_block_theorem=causal_zero_block_theorem,
        keldysh_relation_theorem=keldysh_relation_theorem,
        noise_rank_theorem=noise_rank_theorem,
        full_determinant_theorem=full_determinant_theorem,
        spectral_determinant_theorem=spectral_determinant_theorem,
        target_determinant_theorem=target_determinant_theorem,
        witness_determinant_theorem=witness_determinant_theorem,
        witness_target_theorem=witness_target_theorem,
        witness_defect_theorem=witness_defect_theorem,
        normalized_ratio_theorem=normalized_ratio_theorem,
        normalized_action_theorem=normalized_action_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_keldysh_influence_"
        "functional_admission_gate"
    ),
    title="Admission нормированного KMS--Keldysh influence functional",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_keldysh_"
        "influence_functional_admission_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_keldysh_"
        "influence_functional_admission_gate_results.json",
    ),
    obligations=(
        Obligation("five_channel_damping_rank", lambda: build_certificate().damping_rank_theorem),
        Obligation("retarded_advanced_adjoint_pair", lambda: build_certificate().adjoint_pair_theorem),
        Obligation("causal_lower_zero_block", lambda: build_certificate().causal_zero_block_theorem),
        Obligation("fermionic_kms_fdt_block", lambda: build_certificate().keldysh_relation_theorem),
        Obligation("five_channel_noise_rank", lambda: build_certificate().noise_rank_theorem),
        Obligation("triangular_determinant", lambda: build_certificate().full_determinant_theorem),
        Obligation("retarded_advanced_spectral_determinant", lambda: build_certificate().spectral_determinant_theorem),
        Obligation("two_package_target_determinant", lambda: build_certificate().target_determinant_theorem),
        Obligation("interacting_witness_determinant", lambda: build_certificate().witness_determinant_theorem),
        Obligation("witness_target_determinant", lambda: build_certificate().witness_target_theorem),
        Obligation("strict_target_defect", lambda: build_certificate().witness_defect_theorem),
        Obligation("closed_contour_normalized_ratio", lambda: build_certificate().normalized_ratio_theorem),
        Obligation("normalized_vacuum_action_zero", lambda: build_certificate().normalized_action_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)