"""LCF certificate for the minimal coupled KMS fermion-bath architecture."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSMinimalFermionBathCertificate:
    system_operator: sp.ImmutableMatrix
    bath_operator: sp.ImmutableMatrix
    coupling_operator: sp.ImmutableMatrix
    full_kernel: sp.ImmutableMatrix
    schur_kernel: sp.ImmutableMatrix
    stable_witness: sp.ImmutableMatrix
    carrier_rank_theorem: Theorem
    coupling_rank_theorem: Theorem
    full_determinant_theorem: Theorem
    schur_kernel_theorem: Theorem
    schur_determinant_theorem: Theorem
    target_determinant_theorem: Theorem
    determinant_ratio_theorem: Theorem
    witness_spectrum_theorem: Theorem
    witness_determinant_theorem: Theorem
    witness_target_theorem: Theorem
    witness_defect_theorem: Theorem
    decoupled_target_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSMinimalFermionBathCertificate:
    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    gs, ga, gt = sp.symbols("g_s g_a g_t", positive=True)

    system_operator = sp.ImmutableMatrix(sp.diag(ts, ta, tt, tt, tt))
    bath_operator = sp.ImmutableMatrix(sp.diag(ks, ka, kt, kt, kt))
    coupling_operator = sp.ImmutableMatrix(sp.diag(gs, ga, gt, gt, gt))
    full_kernel = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(system_operator, coupling_operator),
        sp.Matrix.hstack(coupling_operator, bath_operator),
    ))
    schur_kernel = sp.ImmutableMatrix(
        system_operator - coupling_operator * bath_operator.inv() * coupling_operator
    )

    full_determinant = (
        (ts * ks - gs**2)
        * (ta * ka - ga**2)
        * (tt * kt - gt**2) ** 3
    )
    target_determinant = (
        ts * ta * tt**3 * ks * ka * kt**3
    )
    determinant_ratio = (
        (1 - gs**2 / (ts * ks))
        * (1 - ga**2 / (ta * ka))
        * (1 - gt**2 / (tt * kt)) ** 3
    )

    stable_witness = sp.ImmutableMatrix(full_kernel.subs({
        ts: 2, ta: 2, tt: 2,
        ks: 2, ka: 2, kt: 2,
        gs: 1, ga: 1, gt: 1,
    }))
    zero_coupling_kernel = sp.ImmutableMatrix(full_kernel.subs({
        gs: 0, ga: 0, gt: 0,
    }))

    carrier_rank_theorem = kernel.prove_exact_rank(
        sp.eye(10),
        10,
        subject="one system and one bath type multiplet form a ten dimensional carrier",
    )
    coupling_rank_theorem = kernel.prove_exact_rank(
        coupling_operator,
        5,
        subject="type covariant positive coupling reaches all five channels",
    )
    full_determinant_theorem = kernel.prove_expression_equality(
        full_kernel.det(),
        full_determinant,
        subject="coupled Hermitian system bath determinant factorizes by channel type",
    )
    schur_kernel_theorem = kernel.prove_matrix_equality(
        schur_kernel,
        sp.diag(
            ts - gs**2 / ks,
            ta - ga**2 / ka,
            tt - gt**2 / kt,
            tt - gt**2 / kt,
            tt - gt**2 / kt,
        ),
        subject="integrating out the bath produces the exact Schur complement",
    )
    schur_determinant_theorem = kernel.prove_expression_equality(
        full_kernel.det(),
        bath_operator.det() * schur_kernel.det(),
        subject="full determinant equals bath determinant times system Schur determinant",
    )
    target_determinant_theorem = kernel.prove_expression_equality(
        system_operator.det() * bath_operator.det(),
        target_determinant,
        subject="decoupled system and bath blocks carry the desired two package determinant",
    )
    determinant_ratio_theorem = kernel.prove_expression_equality(
        full_kernel.det() / target_determinant,
        determinant_ratio,
        subject="nonzero Hermitian coupling multiplies the target by a Schur correction",
    )
    witness_spectrum_theorem = kernel.prove_exact_spectrum(
        stable_witness,
        {sp.Integer(1): 5, sp.Integer(3): 5},
        subject="the coupled isotropic witness is strictly positive",
    )
    witness_determinant_theorem = kernel.prove_expression_equality(
        stable_witness.det(),
        243,
        subject="stable nonzero coupling witness has determinant three to the fifth",
    )
    witness_target_theorem = kernel.prove_expression_equality(
        (sp.diag(2, 2, 2, 2, 2).det()) ** 2,
        1024,
        subject="the decoupled target determinant of the witness is four to the fifth",
    )
    witness_defect_theorem = kernel.prove_positive_expression(
        sp.Integer(1024 - 243),
        subject="the stable coupled witness differs strictly from the target determinant",
    )
    decoupled_target_theorem = kernel.prove_expression_equality(
        zero_coupling_kernel.det(),
        target_determinant,
        subject="exact target factorization is restored only on the zero coupling face",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_minimal_fermion_bath_"
        "architecture_gate",
        (
            carrier_rank_theorem,
            coupling_rank_theorem,
            full_determinant_theorem,
            schur_kernel_theorem,
            schur_determinant_theorem,
            target_determinant_theorem,
            determinant_ratio_theorem,
            witness_spectrum_theorem,
            witness_determinant_theorem,
            witness_target_theorem,
            witness_defect_theorem,
            decoupled_target_theorem,
        ),
    )
    return KMSMinimalFermionBathCertificate(
        system_operator=system_operator,
        bath_operator=bath_operator,
        coupling_operator=coupling_operator,
        full_kernel=full_kernel,
        schur_kernel=schur_kernel,
        stable_witness=stable_witness,
        carrier_rank_theorem=carrier_rank_theorem,
        coupling_rank_theorem=coupling_rank_theorem,
        full_determinant_theorem=full_determinant_theorem,
        schur_kernel_theorem=schur_kernel_theorem,
        schur_determinant_theorem=schur_determinant_theorem,
        target_determinant_theorem=target_determinant_theorem,
        determinant_ratio_theorem=determinant_ratio_theorem,
        witness_spectrum_theorem=witness_spectrum_theorem,
        witness_determinant_theorem=witness_determinant_theorem,
        witness_target_theorem=witness_target_theorem,
        witness_defect_theorem=witness_defect_theorem,
        decoupled_target_theorem=decoupled_target_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_minimal_fermion_bath_"
        "architecture_gate"
    ),
    title="Минимальная fermion-bath архитектура KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_minimal_"
        "fermion_bath_architecture_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_"
        "fermion_bath_architecture_gate_results.json",
    ),
    obligations=(
        Obligation("system_bath_carrier_rank_ten", lambda: build_certificate().carrier_rank_theorem),
        Obligation("all_channel_coupling_rank_five", lambda: build_certificate().coupling_rank_theorem),
        Obligation("coupled_kernel_determinant", lambda: build_certificate().full_determinant_theorem),
        Obligation("bath_schur_kernel", lambda: build_certificate().schur_kernel_theorem),
        Obligation("schur_determinant_factorization", lambda: build_certificate().schur_determinant_theorem),
        Obligation("decoupled_two_package_target", lambda: build_certificate().target_determinant_theorem),
        Obligation("coupling_determinant_correction", lambda: build_certificate().determinant_ratio_theorem),
        Obligation("stable_coupled_witness_spectrum", lambda: build_certificate().witness_spectrum_theorem),
        Obligation("stable_coupled_witness_determinant", lambda: build_certificate().witness_determinant_theorem),
        Obligation("witness_target_determinant", lambda: build_certificate().witness_target_theorem),
        Obligation("strict_witness_determinant_defect", lambda: build_certificate().witness_defect_theorem),
        Obligation("zero_coupling_target_factorization", lambda: build_certificate().decoupled_target_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)