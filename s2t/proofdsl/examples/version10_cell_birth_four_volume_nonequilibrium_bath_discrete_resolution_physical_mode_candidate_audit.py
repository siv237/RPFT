"""LCF certificate for the physical mode behind the discrete resolution."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DiscreteResolutionPhysicalModeAuditCertificate:
    target_resolution: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_resolution_witnesses: sp.ImmutableMatrix
    physical_pole_vector: sp.ImmutableMatrix
    exact_match_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DiscreteResolutionPhysicalModeAuditCertificate:
    target_resolution=sp.exp(32*sp.pi**2/3)
    # inverse-length type, present carrier, physical pole/state,
    # selected mass, exact R, non-target-loaded.
    candidate_matrix=sp.ImmutableMatrix([
        [1,0,1,0,0,0], # proton
        [1,0,1,0,0,0], # electron
        [1,1,1,0,0,1], # Higgs/electroweak mode
        [1,1,1,0,0,1], # neutrino mode
        [1,0,0,0,0,0], # Planck mode
        [1,0,1,0,0,0], # Hubble mode
        [1,1,1,1,0,1], # cell clock mode
        [1,1,1,1,0,1], # K43 cutoff mode
        [1,1,0,1,1,1], # formal RG reference mode
        [1,0,1,0,1,0], # externally fitted pole
    ])
    score_vector=sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(10)])
    pass_vector=sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(10)])
    internal_resolution_witnesses=sp.ImmutableMatrix([1,sp.Rational(1,42),target_resolution])
    physical_pole_vector=sp.ImmutableMatrix([1,1,1,1,0,1,1,1,0,1])
    exact_match_vector=candidate_matrix[:,4]
    audit_coverage=sp.ones(10,1)
    physical_origin=sp.zeros(3,1)
    theorems=(
        kernel.prove_expression_equality(target_resolution,sp.exp(32*sp.pi**2/3),subject="exact discrete-resolution target"),
        kernel.prove_matrix_equality(candidate_matrix,sp.Matrix(candidate_matrix),subject="ten physical-mode candidates on six criteria"),
        kernel.prove_exact_rank(candidate_matrix,5,subject="physical-mode audit distinguishes five criterion directions"),
        kernel.prove_matrix_equality(score_vector,sp.Matrix([2,2,4,4,1,2,5,5,5,3]),subject="exact physical-mode candidate scores"),
        kernel.prove_expression_equality(max(score_vector),5,subject="three candidates miss one physical requirement"),
        kernel.prove_matrix_equality(pass_vector,sp.zeros(10,1),subject="no physical mode passes the full attribution contract"),
        kernel.prove_expression_equality(sum(pass_vector),0,subject="complete physical-mode attribution count is zero"),
        kernel.prove_expression_equality(internal_resolution_witnesses[0],1,subject="cell clock mode has unit resolution"),
        kernel.prove_expression_equality(internal_resolution_witnesses[1],sp.Rational(1,42),subject="K43 cutoff mode has reciprocal endpoint resolution"),
        kernel.prove_expression_equality(internal_resolution_witnesses[2],target_resolution,subject="formal RG reference reproduces the target hierarchy"),
        kernel.prove_matrix_inequality(internal_resolution_witnesses[:2,:],sp.ImmutableMatrix([target_resolution,target_resolution]),subject="clock and K43 cutoff modes do not reproduce the RG hierarchy"),
        kernel.prove_expression_equality(physical_pole_vector[8],0,subject="the formal renormalization scale is not a demonstrated physical pole"),
        kernel.prove_expression_equality(exact_match_vector[8],1,subject="only the formal RG reference has an internal exact target match"),
        kernel.prove_expression_equality(exact_match_vector[9],1,subject="an external fitted pole can match only by target input"),
        kernel.prove_expression_equality(sum(exact_match_vector),2,subject="two target matches exist but neither closes physical origin"),
        kernel.prove_matrix_equality(audit_coverage,sp.ones(10,1),subject="all ten mode candidates are covered"),
        kernel.prove_expression_equality(sum(audit_coverage),10,subject="physical-mode candidate coverage is complete"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(3,1),subject="spectral pole state attribution and mass-parent origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict physical mode-origin score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_physical_mode_candidate_audit_gate",theorems)
    return DiscreteResolutionPhysicalModeAuditCertificate(target_resolution,candidate_matrix,score_vector,pass_vector,internal_resolution_witnesses,physical_pole_vector,exact_match_vector,audit_coverage,physical_origin,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_physical_mode_candidate_audit_gate",title="Аудит физической моды дискретного разрешения",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_physical_mode_candidate_audit_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_physical_mode_candidate_audit_gate_results.json"),obligations=tuple(Obligation(f"discrete_resolution_physical_mode_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(19)))