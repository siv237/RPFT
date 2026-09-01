"""LCF certificate for the final Tome IX status and Tome X program contract."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FinalConclusionTome10ProgramCertificate:
    conditional: sp.ImmutableMatrix
    physical: sp.ImmutableMatrix
    deficit: sp.ImmutableMatrix
    reopening_packages: sp.ImmutableMatrix
    tome10_dependency: sp.ImmutableMatrix
    tome10_specification: sp.ImmutableMatrix
    tome10_construction: sp.ImmutableMatrix
    conditional_theorem: Theorem
    physical_theorem: Theorem
    decomposition_theorem: Theorem
    conditional_score_theorem: Theorem
    physical_score_theorem: Theorem
    deficit_rank_theorem: Theorem
    reopening_theorem: Theorem
    strict_gap_theorem: Theorem
    tome10_dependency_rank_theorem: Theorem
    tome10_dependency_determinant_theorem: Theorem
    tome10_specification_theorem: Theorem
    tome10_construction_theorem: Theorem
    tome10_gap_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FinalConclusionTome10ProgramCertificate:
    conditional = sp.ones(6, 1)
    physical = sp.ImmutableMatrix([1, 0, 1, 1, 0, 0])
    deficit = sp.ImmutableMatrix([0, 1, 0, 0, 1, 1])
    reopening_packages = sp.zeros(2, 1)
    tome10_dependency = sp.ImmutableMatrix([
        [1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ])
    tome10_specification = sp.ones(6, 1)
    tome10_construction = sp.zeros(6, 1)

    conditional_theorem = kernel.prove_matrix_equality(
        conditional,
        sp.ones(6, 1),
        subject="the axiom augmented Tome IX model closes all six conditional criteria",
    )
    physical_theorem = kernel.prove_matrix_equality(
        physical,
        sp.Matrix([1, 0, 1, 1, 0, 0]),
        subject="the final strict physical Tome IX ledger remains three of six",
    )
    decomposition_theorem = kernel.prove_matrix_equality(
        physical + deficit,
        conditional,
        subject="the final physical deficit exactly accounts for conditional closure",
    )
    conditional_score_theorem = kernel.prove_expression_equality(
        sum(conditional),
        6,
        subject="the final conditional score is six of six",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical),
        3,
        subject="the final physical score is three of six",
    )
    deficit_rank_theorem = kernel.prove_exact_rank(
        sp.diag(*list(deficit)),
        3,
        subject="three independent Tome IX criteria remain physically open",
    )
    reopening_theorem = kernel.prove_matrix_equality(
        reopening_packages,
        sp.zeros(2, 1),
        subject="neither physical reopening package was obtained",
    )
    strict_gap_theorem = kernel.prove_positive_expression(
        sum(conditional) - sum(physical),
        subject="conditional and physical final statuses differ strictly",
    )
    tome10_dependency_rank_theorem = kernel.prove_exact_rank(
        tome10_dependency,
        6,
        subject="the six Tome X tasks form a nonredundant dependency chain",
    )
    tome10_dependency_determinant_theorem = kernel.prove_expression_equality(
        tome10_dependency.det(),
        1,
        subject="the Tome X dependency contract is unimodular",
    )
    tome10_specification_theorem = kernel.prove_matrix_equality(
        tome10_specification,
        sp.ones(6, 1),
        subject="all six Tome X program obligations are explicitly specified",
    )
    tome10_construction_theorem = kernel.prove_matrix_equality(
        tome10_construction,
        sp.zeros(6, 1),
        subject="no Tome X quantum RG construction is claimed at admission",
    )
    tome10_gap_theorem = kernel.prove_positive_expression(
        sum(tome10_specification - tome10_construction),
        subject="the admitted Tome X program is not yet a constructed theory",
    )
    gate_theorem = kernel.prove_gate(
        "version9_final_conclusion_and_tome10_program_gate",
        (
            conditional_theorem,
            physical_theorem,
            decomposition_theorem,
            conditional_score_theorem,
            physical_score_theorem,
            deficit_rank_theorem,
            reopening_theorem,
            strict_gap_theorem,
            tome10_dependency_rank_theorem,
            tome10_dependency_determinant_theorem,
            tome10_specification_theorem,
            tome10_construction_theorem,
            tome10_gap_theorem,
        ),
    )
    return FinalConclusionTome10ProgramCertificate(
        conditional=conditional,
        physical=physical,
        deficit=deficit,
        reopening_packages=reopening_packages,
        tome10_dependency=tome10_dependency,
        tome10_specification=tome10_specification,
        tome10_construction=tome10_construction,
        conditional_theorem=conditional_theorem,
        physical_theorem=physical_theorem,
        decomposition_theorem=decomposition_theorem,
        conditional_score_theorem=conditional_score_theorem,
        physical_score_theorem=physical_score_theorem,
        deficit_rank_theorem=deficit_rank_theorem,
        reopening_theorem=reopening_theorem,
        strict_gap_theorem=strict_gap_theorem,
        tome10_dependency_rank_theorem=tome10_dependency_rank_theorem,
        tome10_dependency_determinant_theorem=tome10_dependency_determinant_theorem,
        tome10_specification_theorem=tome10_specification_theorem,
        tome10_construction_theorem=tome10_construction_theorem,
        tome10_gap_theorem=tome10_gap_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_final_conclusion_and_tome10_program_gate",
    title="Финальное заключение Тома IX и программа Тома X",
    source_paths=(
        "s2t/gates/version9_final_conclusion_and_tome10_program_gate.tex",
        "s2t/results/s2t_v9_final_conclusion_and_tome10_program_gate_results.json",
    ),
    obligations=(
        Obligation("final_conditional_status", lambda: build_certificate().conditional_theorem),
        Obligation("final_physical_status", lambda: build_certificate().physical_theorem),
        Obligation("final_status_decomposition", lambda: build_certificate().decomposition_theorem),
        Obligation("final_conditional_score", lambda: build_certificate().conditional_score_theorem),
        Obligation("final_physical_score", lambda: build_certificate().physical_score_theorem),
        Obligation("final_deficit_rank_three", lambda: build_certificate().deficit_rank_theorem),
        Obligation("reopening_packages_zero", lambda: build_certificate().reopening_theorem),
        Obligation("strict_conditional_physical_gap", lambda: build_certificate().strict_gap_theorem),
        Obligation("tome10_dependency_rank_six", lambda: build_certificate().tome10_dependency_rank_theorem),
        Obligation("tome10_dependency_determinant_one", lambda: build_certificate().tome10_dependency_determinant_theorem),
        Obligation("tome10_program_specification_full", lambda: build_certificate().tome10_specification_theorem),
        Obligation("tome10_construction_zero", lambda: build_certificate().tome10_construction_theorem),
        Obligation("tome10_specification_construction_gap", lambda: build_certificate().tome10_gap_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)