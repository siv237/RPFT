# Admission минимального auxiliary fermion module

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, можно ли канонически построить минимальный нечётный carrier,
реализующий два KMS logdet-блока, не добавляя физические endpoint-states.

## Search for solution

- Использован inherited type-space
  `V_type=C_s direct_sum C_a direct sum C_t^3`, dimension `5`.
- Две KMS copies образуют package-space `P_KMS=C_theta direct sum C_kappa`.
- Построен functorial carrier
  `G_aux=Pi(V_type tensor P_KMS)`, complex dimension `10`.
- Quadratic operator `D_aux=R_theta direct sum R_kappa` сохраняет family
  covariance и package exchange.
- Complex Berezin completion содержит `10` pairs, или `20` независимых
  odd coordinates, и имеет rank `20`.
- Direct-sum embedding отделяет auxiliary block от physical creation-cell.

## Expected result

Minimal auxiliary architecture должна быть symmetry-compatible и не менять
physical QMS, а происхождение Grassmann statistics должно остаться отдельным
origin-вопросом.

## Compliance check

- Auxiliary module architecture `10/10`.
- Functorial ungraded carrier origin `2/2`.
- Physical state increment `0`; QMS dimension остаётся `6`.
- ProofDSL `10/10`, registry `51/392`.
- Odd statistics origin `0/1`; Berezin orientation origin `0/1`.
- Physical logdet parent остаётся `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-relative-shape-logdet-parent-measure-origin-gate]]
- [[kms-auxiliary-fermion-module-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_auxiliary_fermion_module_admission.py`