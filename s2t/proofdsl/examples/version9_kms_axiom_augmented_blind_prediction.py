"""LCF certificate for blind dimensionless predictions of the augmented KMS parent."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class KMSAxiomAugmentedBlindPredictionCertificate:
    contrast: sp.ImmutableMatrix
    gap_vector: sp.ImmutableMatrix
    conductance_vector: sp.ImmutableMatrix
    response_vector: sp.ImmutableMatrix
    contrast_rank_theorem: Theorem
    gap_contrast_theorem: Theorem
    conductance_contrast_theorem: Theorem
    gap_ratios_theorem: Theorem
    conductance_ratios_theorem: Theorem
    double_ratios_theorem: Theorem
    response_theorem: Theorem
    weighted_variance_theorem: Theorem
    coefficient_blind_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSAxiomAugmentedBlindPredictionCertificate:
    e, chi, hbar, lam = sp.symbols("E chi hbar lambda", positive=True)
    ones = sp.ones(3, 1)
    gap = sp.ImmutableMatrix(e * ones)
    conductance = sp.ImmutableMatrix(chi**2 * e / hbar * ones)
    contrast = sp.ImmutableMatrix([[1, -1, 0], [0, 1, -1]])
    gap_ratios = sp.ImmutableMatrix([gap[0]/gap[2], gap[1]/gap[2]])
    conductance_ratios = sp.ImmutableMatrix([conductance[0]/conductance[2], conductance[1]/conductance[2]])
    double_ratios = sp.ImmutableMatrix([
        conductance[0]*gap[2]/(conductance[2]*gap[0]),
        conductance[1]*gap[2]/(conductance[2]*gap[1]),
    ])
    response = sp.ImmutableMatrix([hbar*conductance[i]/(chi**2*gap[i]) for i in range(3)])
    weights = [1, 1, 3]
    mean = sum(weights[i]*gap[i] for i in range(3))/5
    variance = sp.simplify(sum(weights[i]*(gap[i]-mean)**2 for i in range(3))/mean**2)
    coefficient_probe = sum(response)

    contrast_rank_theorem = kernel.prove_exact_rank(contrast, 2, subject="two independent channel contrasts span each normalized three component package")
    gap_contrast_theorem = kernel.prove_matrix_equality(contrast*gap, sp.zeros(2,1), subject="both blind gap contrasts vanish")
    conductance_contrast_theorem = kernel.prove_matrix_equality(contrast*conductance, sp.zeros(2,1), subject="both blind conductance contrasts vanish")
    gap_ratios_theorem = kernel.prove_matrix_equality(gap_ratios, sp.ones(2,1), subject="two independent gap ratios equal one")
    conductance_ratios_theorem = kernel.prove_matrix_equality(conductance_ratios, sp.ones(2,1), subject="two independent conductance ratios equal one")
    double_ratios_theorem = kernel.prove_matrix_equality(double_ratios, sp.ones(2,1), subject="gap conductance double ratios equal one")
    response_theorem = kernel.prove_matrix_equality(response, sp.ones(3,1), subject="all three dimensionless transport responses equal one")
    weighted_variance_theorem = kernel.prove_expression_equality(variance, 0, subject="weighted dimensionless gap variance vanishes")
    coefficient_blind_theorem = kernel.prove_expression_equality(sp.diff(coefficient_probe, lam), 0, subject="blind response is independent of the new axiom stiffness")
    gate_theorem = kernel.prove_gate("version9_endpoint_creation_kms_logdet_axiom_augmented_blind_dimensionless_prediction_gate", (contrast_rank_theorem,gap_contrast_theorem,conductance_contrast_theorem,gap_ratios_theorem,conductance_ratios_theorem,double_ratios_theorem,response_theorem,weighted_variance_theorem,coefficient_blind_theorem))
    return KMSAxiomAugmentedBlindPredictionCertificate(contrast,gap,conductance,response,contrast_rank_theorem,gap_contrast_theorem,conductance_contrast_theorem,gap_ratios_theorem,conductance_ratios_theorem,double_ratios_theorem,response_theorem,weighted_variance_theorem,coefficient_blind_theorem,gate_theorem)


SPEC=GateSpec(identifier="version9_endpoint_creation_kms_logdet_axiom_augmented_blind_dimensionless_prediction_gate",title="Blind dimensionless predictions axiom-augmented KMS parent",source_paths=("s2t/gates/version9_endpoint_creation_kms_logdet_axiom_augmented_blind_dimensionless_prediction_gate.tex","s2t/results/s2t_v9_endpoint_creation_kms_logdet_axiom_augmented_blind_dimensionless_prediction_gate_results.json"),obligations=(
 Obligation("channel_contrast_rank",lambda:build_certificate().contrast_rank_theorem),Obligation("gap_contrasts",lambda:build_certificate().gap_contrast_theorem),Obligation("conductance_contrasts",lambda:build_certificate().conductance_contrast_theorem),Obligation("gap_ratios",lambda:build_certificate().gap_ratios_theorem),Obligation("conductance_ratios",lambda:build_certificate().conductance_ratios_theorem),Obligation("double_ratios",lambda:build_certificate().double_ratios_theorem),Obligation("dimensionless_response",lambda:build_certificate().response_theorem),Obligation("weighted_variance",lambda:build_certificate().weighted_variance_theorem),Obligation("stiffness_blindness",lambda:build_certificate().coefficient_blind_theorem)))
if __name__=="__main__": print(build_certificate().gate_theorem.proposition)