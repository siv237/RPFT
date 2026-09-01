# Admission нормированного KMS--Keldysh influence functional

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Проверить, превращает ли causal Schwinger--Keldysh doubling минимальную
fermion-bath architecture в physical origin одновременно conductance и
target barrier `-log det R_theta-log det R_kappa`.

## Search for solution

- Построены `K_R=R_theta-iR_kappa`, `K_A=K_R^dagger` и
  `K_K=(K_R-K_A)F` на type-space `1+1+3`.
- Проверены causal zero block и ranks damping/noise `5/5`.
- Вычислены causal determinant и target determinant.
- Closed-contour normalization реализована как exact normalized Gaussian ratio.
- Algebraic core сертифицирован ProofDSL без floating point.

## Expected result

Nonzero dissipative kernel должен удовлетворять causality и KMS/FDT, а
после normalization оставлять target logdet как source-free parent term.

## Compliance check

- Causal R/A/K architecture `5/5`, KMS/FDT `1/1`.
- `det K_SK=product_alpha(theta_alpha^2+kappa_alpha^2)^m_alpha`, а не target.
- Witness: determinant `32768`, target `1024`, defect `31744`, ratio `32`.
- Normalized ratio `1`, normalized vacuum action `0`.
- Target logdet до/после normalization `0/1`, reservoir origin `0/1`.
- ProofDSL `13/13`, registry `58/468`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-minimal-fermion-bath-architecture-gate]]
- [[kms-keldysh-influence-functional-sources-2026]]
- [[kms-keldysh-next-gate-reconnaissance-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_keldysh_influence_functional.py`