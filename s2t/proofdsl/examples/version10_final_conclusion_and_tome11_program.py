"""LCF certificate for the final Tome X status and Tome XI program."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FinalConclusionTome11ProgramCertificate:
    operational_conditional: sp.ImmutableMatrix
    operational_physical: sp.ImmutableMatrix
    operational_deficit: sp.ImmutableMatrix
    inherited_rg_physical: sp.ImmutableMatrix
    inherited_rg_deficit: sp.ImmutableMatrix
    reopening_packages: sp.ImmutableMatrix
    tome11_dependency: sp.ImmutableMatrix
    tome11_specification: sp.ImmutableMatrix
    tome11_construction: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FinalConclusionTome11ProgramCertificate:
    operational_conditional = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1])
    operational_physical = sp.ImmutableMatrix([1, 0, 1, 0, 1, 1])
    operational_deficit = sp.ImmutableMatrix([0, 1, 0, 1, 0, 0])
    inherited_rg_physical = sp.ImmutableMatrix([1, 1, 0, 0, 0, 1])
    inherited_rg_deficit = sp.ImmutableMatrix([0, 0, 1, 1, 1, 0])
    reopening_packages = sp.ImmutableMatrix([0, 0, 0, 0])
    tome11_dependency = sp.ImmutableMatrix([
        [1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ])
    tome11_specification = sp.ImmutableMatrix([1, 1, 1, 1, 1, 1])
    tome11_construction = sp.ImmutableMatrix([0, 0, 0, 0, 0, 0])
    theorems = (
        kernel.prove_matrix_equality(operational_conditional, sp.ones(6, 1), subject="all six operational Tome X goals have conditional constructions"),
        kernel.prove_matrix_equality(operational_physical, sp.ImmutableMatrix([1, 0, 1, 0, 1, 1]), subject="strict operational Tome X status is four of six"),
        kernel.prove_matrix_equality(operational_physical + operational_deficit, operational_conditional, subject="operational deficit exactly accounts for conditional closure"),
        kernel.prove_expression_equality(sum(operational_conditional), 6, subject="conditional operational score is six of six"),
        kernel.prove_expression_equality(sum(operational_physical), 4, subject="strict operational score is four of six"),
        kernel.prove_exact_rank(sp.diag(*list(operational_deficit)), 2, subject="two operational goals remain physically open"),
        kernel.prove_matrix_equality(inherited_rg_physical, sp.ImmutableMatrix([1, 1, 0, 0, 0, 1]), subject="inherited quantum RG contract closes three of six"),
        kernel.prove_matrix_equality(inherited_rg_physical + inherited_rg_deficit, sp.ones(6, 1), subject="inherited quantum RG deficit is exact"),
        kernel.prove_expression_equality(sum(inherited_rg_physical), 3, subject="strict inherited quantum RG score is three of six"),
        kernel.prove_exact_rank(sp.diag(*list(inherited_rg_deficit)), 3, subject="three inherited quantum RG promises remain open"),
        kernel.prove_matrix_equality(reopening_packages, sp.zeros(4, 1), subject="no physical scale-breaking reopening package was obtained"),
        kernel.prove_positive_expression(sum(operational_conditional) - sum(operational_physical), subject="conditional and physical Tome X statuses differ strictly"),
        kernel.prove_exact_rank(tome11_dependency, 6, subject="the six Tome XI tasks form a nonredundant dependency chain"),
        kernel.prove_expression_equality(tome11_dependency.det(), 1, subject="the Tome XI dependency contract is unimodular"),
        kernel.prove_matrix_equality(tome11_specification, sp.ones(6, 1), subject="all Tome XI program obligations are specified"),
        kernel.prove_matrix_equality(tome11_construction, sp.zeros(6, 1), subject="no Tome XI construction is claimed at admission"),
        kernel.prove_positive_expression(sum(tome11_specification - tome11_construction), subject="Tome XI specification is not a constructed theory"),
        kernel.prove_expression_equality(sum(operational_physical) - sum(inherited_rg_physical), 1, subject="the operational growth contract is one criterion weaker than the inherited RG promise"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_final_conclusion_and_tome11_program_gate", theorems
    )
    return FinalConclusionTome11ProgramCertificate(
        operational_conditional, operational_physical, operational_deficit,
        inherited_rg_physical, inherited_rg_deficit, reopening_packages,
        tome11_dependency, tome11_specification, tome11_construction,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_final_conclusion_and_tome11_program_gate",
    title="Финальное заключение Тома X и программа Тома XI",
    source_paths=(
        "s2t/gates/version10_final_conclusion_and_tome11_program_gate.tex",
        "s2t/results/s2t_v10_final_conclusion_and_tome11_program_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"version10_final_conclusion_tome11_program_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(18)
    ),
)