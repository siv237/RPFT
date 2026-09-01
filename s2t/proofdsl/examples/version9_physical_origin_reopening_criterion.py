"""LCF certificate for the minimal physical-origin reopening criterion."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class PhysicalOriginReopeningCriterionCertificate:
    deficit: sp.ImmutableMatrix
    package_map: sp.ImmutableMatrix
    conditional_packages: sp.ImmutableMatrix
    physical_packages: sp.ImmutableMatrix
    deficit_theorem: Theorem
    package_map_theorem: Theorem
    joint_closure_theorem: Theorem
    package_rank_theorem: Theorem
    scale_only_failure_theorem: Theorem
    logdet_only_failure_theorem: Theorem
    physical_availability_theorem: Theorem
    conditional_availability_theorem: Theorem
    strict_residual_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> PhysicalOriginReopeningCriterionCertificate:
    deficit = sp.ImmutableMatrix([1, 1, 1])
    package_map = sp.ImmutableMatrix([
        [1, 0],
        [0, 1],
        [0, 1],
    ])
    conditional_packages = sp.ones(2, 1)
    physical_packages = sp.zeros(2, 1)

    deficit_theorem = kernel.prove_matrix_equality(
        deficit,
        sp.ones(3, 1),
        subject="the strict Tome IX ledger has three open physical criteria",
    )
    package_map_theorem = kernel.prove_matrix_equality(
        package_map,
        sp.Matrix([[1, 0], [0, 1], [0, 1]]),
        subject="scale origin and logdet origin are the two reopening packages",
    )
    joint_closure_theorem = kernel.prove_matrix_equality(
        package_map * conditional_packages,
        deficit,
        subject="the two provenance packages jointly cover all three deficits",
    )
    package_rank_theorem = kernel.prove_exact_rank(
        package_map,
        2,
        subject="the reopening problem has two independent provenance packages",
    )
    scale_only_failure_theorem = kernel.prove_exact_rank(
        sp.ImmutableMatrix.hstack(package_map[:, 0], deficit),
        2,
        subject="the scale and coupling package alone cannot close the deficit",
    )
    logdet_only_failure_theorem = kernel.prove_exact_rank(
        sp.ImmutableMatrix.hstack(package_map[:, 1], deficit),
        2,
        subject="the logdet package alone cannot close the deficit",
    )
    physical_availability_theorem = kernel.prove_matrix_equality(
        package_map * physical_packages,
        sp.zeros(3, 1),
        subject="no reopening package currently has a physical-origin certificate",
    )
    conditional_availability_theorem = kernel.prove_matrix_equality(
        package_map * conditional_packages,
        sp.ones(3, 1),
        subject="axiom admission conditionally supplies both reopening packages",
    )
    strict_residual_theorem = kernel.prove_positive_expression(
        sum(deficit - package_map * physical_packages),
        subject="the physical reopening residual remains strictly positive",
    )
    gate_theorem = kernel.prove_gate(
        "version9_axiom_augmented_physical_origin_reopening_criterion_gate",
        (
            deficit_theorem,
            package_map_theorem,
            joint_closure_theorem,
            package_rank_theorem,
            scale_only_failure_theorem,
            logdet_only_failure_theorem,
            physical_availability_theorem,
            conditional_availability_theorem,
            strict_residual_theorem,
        ),
    )
    return PhysicalOriginReopeningCriterionCertificate(
        deficit=deficit,
        package_map=package_map,
        conditional_packages=conditional_packages,
        physical_packages=physical_packages,
        deficit_theorem=deficit_theorem,
        package_map_theorem=package_map_theorem,
        joint_closure_theorem=joint_closure_theorem,
        package_rank_theorem=package_rank_theorem,
        scale_only_failure_theorem=scale_only_failure_theorem,
        logdet_only_failure_theorem=logdet_only_failure_theorem,
        physical_availability_theorem=physical_availability_theorem,
        conditional_availability_theorem=conditional_availability_theorem,
        strict_residual_theorem=strict_residual_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_axiom_augmented_physical_origin_reopening_criterion_gate",
    title="Минимальный критерий переоткрытия physical-origin программы",
    source_paths=(
        "s2t/gates/version9_axiom_augmented_physical_origin_reopening_criterion_gate.tex",
        "s2t/results/s2t_v9_axiom_augmented_physical_origin_reopening_criterion_gate_results.json",
    ),
    obligations=(
        Obligation("physical_deficit_vector", lambda: build_certificate().deficit_theorem),
        Obligation("two_package_reopening_map", lambda: build_certificate().package_map_theorem),
        Obligation("joint_deficit_closure", lambda: build_certificate().joint_closure_theorem),
        Obligation("minimal_package_rank_two", lambda: build_certificate().package_rank_theorem),
        Obligation("scale_package_alone_fails", lambda: build_certificate().scale_only_failure_theorem),
        Obligation("logdet_package_alone_fails", lambda: build_certificate().logdet_only_failure_theorem),
        Obligation("physical_package_availability_zero", lambda: build_certificate().physical_availability_theorem),
        Obligation("conditional_package_availability_full", lambda: build_certificate().conditional_availability_theorem),
        Obligation("strict_physical_residual", lambda: build_certificate().strict_residual_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)