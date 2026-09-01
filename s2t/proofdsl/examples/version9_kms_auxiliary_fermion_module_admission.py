"""LCF certificate for the minimal auxiliary KMS fermion module."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSAuxiliaryFermionModuleAdmissionCertificate:
    type_label: sp.ImmutableMatrix
    package_theta: sp.ImmutableMatrix
    package_kappa: sp.ImmutableMatrix
    odd_parity: sp.ImmutableMatrix
    auxiliary_operator: sp.ImmutableMatrix
    berezin_pairing: sp.ImmutableMatrix
    type_multiplicity_theorem: Theorem
    package_partition_theorem: Theorem
    parity_involution_theorem: Theorem
    even_operator_theorem: Theorem
    family_covariance_theorem: Theorem
    determinant_theorem: Theorem
    degree_theorem: Theorem
    package_swap_theorem: Theorem
    physical_decoupling_theorem: Theorem
    berezin_pairing_rank_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSAuxiliaryFermionModuleAdmissionCertificate:
    ts, ta, tt = sp.symbols("theta_s theta_a theta_t", positive=True)
    ks, ka, kt = sp.symbols("kappa_s kappa_a kappa_t", positive=True)
    r_theta = sp.ImmutableMatrix(sp.diag(ts, ta, tt, tt, tt))
    r_kappa = sp.ImmutableMatrix(sp.diag(ks, ka, kt, kt, kt))
    auxiliary_operator = sp.ImmutableMatrix(sp.diag(r_theta, r_kappa))

    type_label = sp.ImmutableMatrix(sp.diag(0, 1, 2, 2, 2))
    package_theta = sp.ImmutableMatrix(sp.diag(sp.eye(5), sp.zeros(5)))
    package_kappa = sp.ImmutableMatrix(sp.diag(sp.zeros(5), sp.eye(5)))
    odd_parity = sp.ImmutableMatrix(-sp.eye(10))

    family_generator_one = sp.zeros(5)
    family_generator_one[2, 3] = 1
    family_generator_one[3, 2] = -1
    family_generator_two = sp.zeros(5)
    family_generator_two[3, 4] = 1
    family_generator_two[4, 3] = -1
    family_action = sp.ImmutableMatrix(sp.diag(
        family_generator_one + 2 * family_generator_two,
        family_generator_one + 2 * family_generator_two,
    ))

    package_swap = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(5), sp.eye(5)),
        sp.Matrix.hstack(sp.eye(5), sp.zeros(5)),
    ))
    swapped_operator = sp.ImmutableMatrix(sp.diag(r_kappa, r_theta))

    total_operator = sp.ImmutableMatrix(sp.diag(sp.zeros(6), auxiliary_operator))
    physical_inclusion = sp.ImmutableMatrix(sp.Matrix.vstack(sp.eye(6), sp.zeros(10, 6)))

    berezin_pairing = sp.ImmutableMatrix(sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(10), auxiliary_operator),
        sp.Matrix.hstack(-auxiliary_operator.T, sp.zeros(10)),
    ))

    type_multiplicity_theorem = kernel.prove_exact_spectrum(
        type_label,
        {sp.Integer(0): 1, sp.Integer(1): 1, sp.Integer(2): 3},
        subject="auxiliary type carrier has multiplicities one one three",
    )
    package_partition_theorem = kernel.prove_complementary_projectors(
        package_theta,
        package_kappa,
        expected_ranks=(5, 5),
        subject="gap and conductance packages split the ten dimensional carrier",
    )
    parity_involution_theorem = kernel.prove_matrix_equality(
        odd_parity**2,
        sp.eye(10),
        subject="auxiliary carrier is purely odd with involutive grading",
    )
    even_operator_theorem = kernel.prove_matrix_equality(
        odd_parity * auxiliary_operator,
        auxiliary_operator * odd_parity,
        subject="quadratic auxiliary operator is even",
    )
    family_covariance_theorem = kernel.prove_matrix_equality(
        family_action * auxiliary_operator,
        auxiliary_operator * family_action,
        subject="triplet scalar blocks preserve family covariance",
    )
    determinant_theorem = kernel.prove_expression_equality(
        auxiliary_operator.det(),
        ts * ta * tt**3 * ks * ka * kt**3,
        subject="auxiliary determinant contains both one one three packages",
    )
    degree_theorem = kernel.prove_expression_equality(
        sp.Poly(auxiliary_operator.det(), ts, ta, tt, ks, ka, kt).total_degree(),
        10,
        subject="minimal linear determinant carrier has total degree ten",
    )
    package_swap_theorem = kernel.prove_matrix_equality(
        package_swap * auxiliary_operator * package_swap,
        swapped_operator,
        subject="package exchange swaps the two five dimensional blocks",
    )
    physical_decoupling_theorem = kernel.prove_matrix_equality(
        total_operator * physical_inclusion,
        sp.zeros(16, 6),
        subject="auxiliary quadratic operator adds no physical creation cell states",
    )
    berezin_pairing_rank_theorem = kernel.prove_exact_rank(
        berezin_pairing,
        20,
        subject="bar psi psi completion has twenty independent odd coordinates",
    )
    gate_theorem = kernel.prove_gate(
        "version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_"
        "admission_gate",
        (
            type_multiplicity_theorem,
            package_partition_theorem,
            parity_involution_theorem,
            even_operator_theorem,
            family_covariance_theorem,
            determinant_theorem,
            degree_theorem,
            package_swap_theorem,
            physical_decoupling_theorem,
            berezin_pairing_rank_theorem,
        ),
    )
    return KMSAuxiliaryFermionModuleAdmissionCertificate(
        type_label=type_label,
        package_theta=package_theta,
        package_kappa=package_kappa,
        odd_parity=odd_parity,
        auxiliary_operator=auxiliary_operator,
        berezin_pairing=berezin_pairing,
        type_multiplicity_theorem=type_multiplicity_theorem,
        package_partition_theorem=package_partition_theorem,
        parity_involution_theorem=parity_involution_theorem,
        even_operator_theorem=even_operator_theorem,
        family_covariance_theorem=family_covariance_theorem,
        determinant_theorem=determinant_theorem,
        degree_theorem=degree_theorem,
        package_swap_theorem=package_swap_theorem,
        physical_decoupling_theorem=physical_decoupling_theorem,
        berezin_pairing_rank_theorem=berezin_pairing_rank_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier=(
        "version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_"
        "admission_gate"
    ),
    title="Admission минимального auxiliary fermion module для KMS logdet",
    source_paths=(
        "s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "module_admission_gate.tex",
        "s2t/results/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_"
        "module_admission_gate_results.json",
    ),
    obligations=(
        Obligation("type_multiplicity_113", lambda: build_certificate().type_multiplicity_theorem),
        Obligation("package_partition_5_5", lambda: build_certificate().package_partition_theorem),
        Obligation("purely_odd_parity_involution", lambda: build_certificate().parity_involution_theorem),
        Obligation("quadratic_operator_is_even", lambda: build_certificate().even_operator_theorem),
        Obligation("family_triplet_covariance", lambda: build_certificate().family_covariance_theorem),
        Obligation("two_package_determinant", lambda: build_certificate().determinant_theorem),
        Obligation("minimal_total_degree_ten", lambda: build_certificate().degree_theorem),
        Obligation("package_exchange_covariance", lambda: build_certificate().package_swap_theorem),
        Obligation("physical_cell_decoupling", lambda: build_certificate().physical_decoupling_theorem),
        Obligation("berezin_pairing_rank_twenty", lambda: build_certificate().berezin_pairing_rank_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)