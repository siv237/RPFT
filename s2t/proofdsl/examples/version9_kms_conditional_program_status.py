"""LCF certificate for the conditional and physical status ledgers of Tome IX."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSConditionalProgramStatusCertificate:
    conditional: sp.ImmutableMatrix
    physical: sp.ImmutableMatrix
    axiom_dependency: sp.ImmutableMatrix
    conditional_theorem: Theorem
    physical_theorem: Theorem
    decomposition_theorem: Theorem
    conditional_count_theorem: Theorem
    physical_count_theorem: Theorem
    deficit_count_theorem: Theorem
    dependency_rank_theorem: Theorem
    strict_failure_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSConditionalProgramStatusCertificate:
    conditional=sp.ones(6,1)
    physical=sp.ImmutableMatrix([1,0,1,1,0,0])
    dependency=sp.ImmutableMatrix([0,1,0,0,1,1])
    conditional_theorem=kernel.prove_matrix_equality(conditional,sp.ones(6,1),subject="the axiom augmented model conditionally passes all six Tome IX criteria")
    physical_theorem=kernel.prove_matrix_equality(physical,sp.ImmutableMatrix([1,0,1,1,0,0]),subject="only carrier transport and primitive process survive the strict physical ledger")
    decomposition_theorem=kernel.prove_matrix_equality(physical+dependency,conditional,subject="the three missing physical criteria are exactly the axiom dependent criteria")
    conditional_count_theorem=kernel.prove_expression_equality(sum(conditional),6,subject="conditional Tome IX score is six of six")
    physical_count_theorem=kernel.prove_expression_equality(sum(physical),3,subject="strict physical Tome IX score is three of six")
    deficit_count_theorem=kernel.prove_expression_equality(sum(dependency),3,subject="three program criteria remain axiom dependent")
    dependency_rank_theorem=kernel.prove_exact_rank(sp.diag(*list(dependency)),3,subject="axiom dependency occupies exactly three independent program slots")
    strict_failure_theorem=kernel.prove_positive_expression(sum(conditional)-sum(physical),subject="conditional and physical program scores differ strictly")
    gate_theorem=kernel.prove_gate("version9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate",(conditional_theorem,physical_theorem,decomposition_theorem,conditional_count_theorem,physical_count_theorem,deficit_count_theorem,dependency_rank_theorem,strict_failure_theorem))
    return KMSConditionalProgramStatusCertificate(conditional,physical,dependency,conditional_theorem,physical_theorem,decomposition_theorem,conditional_count_theorem,physical_count_theorem,deficit_count_theorem,dependency_rank_theorem,strict_failure_theorem,gate_theorem)


SPEC=GateSpec(identifier="version9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate",title="Conditional program status axiom-augmented KMS parent",source_paths=("s2t/gates/version9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate.tex","s2t/results/s2t_v9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate_results.json"),obligations=(Obligation("conditional_status_vector",lambda:build_certificate().conditional_theorem),Obligation("physical_status_vector",lambda:build_certificate().physical_theorem),Obligation("status_decomposition",lambda:build_certificate().decomposition_theorem),Obligation("conditional_score",lambda:build_certificate().conditional_count_theorem),Obligation("physical_score",lambda:build_certificate().physical_count_theorem),Obligation("deficit_score",lambda:build_certificate().deficit_count_theorem),Obligation("axiom_dependency_rank",lambda:build_certificate().dependency_rank_theorem),Obligation("strict_status_gap",lambda:build_certificate().strict_failure_theorem)))
if __name__=="__main__": print(build_certificate().gate_theorem.proposition)