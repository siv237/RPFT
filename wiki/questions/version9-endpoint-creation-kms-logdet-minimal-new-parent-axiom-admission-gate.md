# Admission минимальной новой аксиомы KMS logdet parent

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Определить минимальное честное расширение parent после исчерпания
унаследованных origin-механизмов.

## Search for solution

- Введён один term `B_lambda=-lambda(log det R_theta+log det R_kappa)`.
- Проверены stationary point, Hessian rank/determinant и sign witness.
- Разделены shape selection и fluctuation stiffness.
- Algebraic core сертифицирован ProofDSL.

## Expected result

Один positive invariant term должен контролировать четыре shape-directions,
не объявляя axiom физически выведенной.

## Compliance check

- Shape rank `4`, Hessian determinant `9 lambda^4/25`.
- Unit spectrum `{(3/5)^2,1^2}`; при `lambda=0` rank `0`.
- Minimum isotropic для любого `lambda>0`.
- Axiom admission `1/1`, shape selection `4/4`.
- Stiffness origin и physical derivation `0/1`.
- ProofDSL `11/11`, registry `61/503`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_axiom_augmented_common_parent_closure_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-reservoir-measure-anomaly-parent-origin-gate]]
- [[kms-minimal-new-parent-axiom-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_new_parent_axiom_admission_gate_results.json`