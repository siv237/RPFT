# Parent-origin measure anomaly reservoir KMS logdet

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Может ли Jacobian reservoir fermion measure породить target logdet.

## Search for solution

- Проверены paired и same-direction Berezin transformations.
- Сопоставлены type-, package- и product-gradings с target coefficients.
- Проверена target-dependent isotropic rescaling.
- Algebraic core сертифицирован ProofDSL.

## Expected result

Inherited symmetry должна дать positive coefficient vector
`(1,1,3,1,1,3)` без вставки `D_aux` в transformation.

## Compliance check

- Paired Jacobian `1`.
- Inherited anomaly rank `3`; rank после target `4`.
- Isotropic traces `6,0,0`, target trace `10`.
- Target получается только при `S=r^-1/2 I10`, то есть target-loaded.
- Physical anomaly/logdet origin `0/1`.
- ProofDSL `12/12`, registry `60/492`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-reservoir-spectral-density-parent-origin-gate]]
- [[kms-reservoir-measure-anomaly-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate_results.json`