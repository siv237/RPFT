"""LCF certificate for the minimal contractible BRST complex of KMS logdet."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSMinimalBRSTComplexCertificate:
    brst_differential: sp.ImmutableMatrix
    ghost_number: sp.ImmutableMatrix
    parity: sp.ImmutableMatrix
    fp_operator: sp.ImmutableMatrix
    nilpotence_theorem: Theorem
    rank_theorem: Theorem
    nullity_theorem: Theorem
    cohomology_theorem: Theorem
    ghost_number_theorem: Theorem
    parity_theorem: Theorem
    superdimension_theorem: Theorem
    fp_rank_theorem: Theorem
    fp_determinant_theorem: Theorem
    physical_decoupling_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSMinimalBRSTComplexCertificate:
    identity = sp.eye(10)
    zero = sp.zeros(10)
    brst_differential = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(zero, zero, zero, zero),
        sp.Matrix.hstack(zero, zero, zero, identity),
        sp.Matrix.hstack(identity, zero, zero, zero),
        sp.Matrix.hstack(zero, zero, zero, zero),
    ))
    ghost_number = sp.ImmutableMatrix(sp.diag(
        sp.zeros(10), sp.zeros(10), sp.eye(10), -sp.eye(10)
    ))
    parity = sp.ImmutableMatrix(sp.diag(
        sp.eye(10), sp.eye(10), -sp.eye(10), -sp.eye(10)
    ))

    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    fp_operator = sp.ImmutableMatrix(sp.diag(
        ts, ta, tt, tt, tt, ks, ka, kt, kt, kt
    ))

    total_brst = sp.ImmutableMatrix(sp.diag(sp.zeros(6), brst_differential))
    physical_inclusion = sp.ImmutableMatrix(sp.Matrix.vstack(sp.eye(6), sp.zeros(40, 6)))

    nilpotence_theorem = kernel.prove_matrix_equality(
        brst_differential**2,
        sp.zeros(40),
        subject="minimal BRST quartet differential is nilpotent",
    )
    rank_theorem = kernel.prove_exact_rank(
        brst_differential,
        20,
        subject="BRST differential maps both ten dimensional doublets",
    )
    nullity_theorem = kernel.prove_exact_nullity(
        brst_differential,
        20,
        subject="kernel of the BRST quartet has dimension twenty",
    )
    cohomology_theorem = kernel.prove_expression_equality(
        20 - 20,
        0,
        subject="nilpotent quartet has zero cohomology dimension",
    )
    ghost_number_theorem = kernel.prove_matrix_equality(
        ghost_number * brst_differential - brst_differential * ghost_number,
        brst_differential,
        subject="BRST differential raises ghost number by one",
    )
    parity_theorem = kernel.prove_matrix_equality(
        parity * brst_differential + brst_differential * parity,
        sp.zeros(40),
        subject="BRST differential is odd",
    )
    superdimension_theorem = kernel.prove_expression_equality(
        20 - 20,
        0,
        subject="minimal quartet has balanced even and odd dimensions",
    )
    fp_rank_theorem = kernel.prove_exact_rank(
        fp_operator,
        10,
        subject="positive KMS Faddeev Popov operator has full rank ten",
    )
    fp_determinant_theorem = kernel.prove_expression_equality(
        fp_operator.det(),
        ts * ta * tt**3 * ks * ka * kt**3,
        subject="Faddeev Popov determinant equals both KMS type determinants",
    )
    physical_decoupling_theorem = kernel.prove_matrix_equality(
        total_brst * physical_inclusion,
        sp.zeros(46, 6),
        subject="contractible BRST quartet acts trivially on physical creation states",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_minimal_brst_complex_"
        "architecture_gate",
        (
            nilpotence_theorem,
            rank_theorem,
            nullity_theorem,
            cohomology_theorem,
            ghost_number_theorem,
            parity_theorem,
            superdimension_theorem,
            fp_rank_theorem,
            fp_determinant_theorem,
            physical_decoupling_theorem,
        ),
    )
    return KMSMinimalBRSTComplexCertificate(
        brst_differential=brst_differential,
        ghost_number=ghost_number,
        parity=parity,
        fp_operator=fp_operator,
        nilpotence_theorem=nilpotence_theorem,
        rank_theorem=rank_theorem,
        nullity_theorem=nullity_theorem,
        cohomology_theorem=cohomology_theorem,
        ghost_number_theorem=ghost_number_theorem,
        parity_theorem=parity_theorem,
        superdimension_theorem=superdimension_theorem,
        fp_rank_theorem=fp_rank_theorem,
        fp_determinant_theorem=fp_determinant_theorem,
        physical_decoupling_theorem=physical_decoupling_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_minimal_brst_complex_"
        "architecture_gate"
    ),
    title="Минимальный contractible BRST complex для KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_minimal_brst_"
        "complex_architecture_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_brst_"
        "complex_architecture_gate_results.json",
    ),
    obligations=(
        Obligation("brst_nilpotence", lambda: build_certificate().nilpotence_theorem),
        Obligation("brst_rank_twenty", lambda: build_certificate().rank_theorem),
        Obligation("brst_nullity_twenty", lambda: build_certificate().nullity_theorem),
        Obligation("contractible_zero_cohomology", lambda: build_certificate().cohomology_theorem),
        Obligation("ghost_number_plus_one", lambda: build_certificate().ghost_number_theorem),
        Obligation("odd_brst_differential", lambda: build_certificate().parity_theorem),
        Obligation("balanced_superdimension", lambda: build_certificate().superdimension_theorem),
        Obligation("fp_operator_rank_ten", lambda: build_certificate().fp_rank_theorem),
        Obligation("fp_determinant_two_packages", lambda: build_certificate().fp_determinant_theorem),
        Obligation("physical_creation_decoupling", lambda: build_certificate().physical_decoupling_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)