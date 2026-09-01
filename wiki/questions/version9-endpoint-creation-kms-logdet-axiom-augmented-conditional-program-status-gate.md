# Conditional program status axiom-augmented KMS parent

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Разделить conditional completion augmented model и строгий physical status.

## Search for solution

- Шесть критериев Тома IX сведены в conditional, physical и
  axiom-dependency vectors.
- Проверены exact decomposition, scores и dependency rank.
- Algebraic core сертифицирован ProofDSL.

## Expected result

Conditional `6/6` не должен скрывать критерии, закрытые только новой axiom.

## Compliance check

- Conditional vector `(1,1,1,1,1,1)`, score `6/6`.
- Physical vector `(1,0,1,1,0,0)`, score `3/6`.
- Axiom dependency `(0,1,0,0,1,1)`, rank `3`.
- Physical four-slot parent `0/1`.
- ProofDSL `8/8`, registry `64/529`.
- Следующий гейт:
  `version9_axiom_augmented_physical_origin_reopening_criterion_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-axiom-augmented-blind-dimensionless-prediction-gate]]
- [[kms-conditional-program-status-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate.tex`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_axiom_augmented_conditional_program_status_gate_results.json`