# Parent-origin нечётной статистики auxiliary fermion module

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, выводится ли all-odd grading auxiliary KMS carrier из physical
channel-grading, package labels, Real/KMS/transport structures.

## Search for solution

- Physical type grading равна `diag(+1,-1,+1,+1,+1)`.
- Перебраны четыре tensor-product grading с uniform package signs.
- Получены exact odd ranks `2,5,5,8`; target требует `10`.
- Package-swap сохраняет только equal-sign choices с ranks `2,8`.
- Ближайший candidate имеет rank-two defect на `theta_a,kappa_a`.
- Проверена paired Berezin covariance:
  `det(S)det(S^-1)=1`.

## Expected result

Либо inherited grading должна единственно дать `-I10`, либо missing
statistics datum должен быть локализован без ложной дополнительной свободы
measure orientation.

## Compliance check

- Statistics origin candidates `0/6`.
- Conditional all-odd grading `1/1`, но это внешний seed.
- Paired measure covariance `1/1`; normalization даёт только additive
  constant, independent orientation freedom `0`.
- Неразрешённый datum сокращён до одного: Grassmann statistics.
- ProofDSL `10/10`, registry `52/402`.
- Physical logdet parent остаётся `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-module-admission-gate]]
- [[kms-auxiliary-fermion-statistics-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_auxiliary_fermion_statistics_origin.py`