# Four-slot origin KMS source-covectors

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, выводятся ли `j_theta,j_kappa` из четырёх slots: общего
gap-scale `E_*`, общего conductance-scale `chi²E_*/hbar`, endpoint types и
transport orientation.

## Search for solution

- Построена rank-two карта `(E_*,chi)` в два общих масштаба.
- Каждый трёхкомпонентный covector разложен на scale и двумерную shape.
- Проверено, что endpoint types лишь маркируют `1+1+3` каналы.
- Две transport orientations сохраняют type-метрику и shape-rank.
- Построены точные положительные witnesses с одинаковыми scales и разными
  source-covectors.

## Expected result

Общие масштабы должны наследоваться из four-slot package, но четыре
относительных отношения должны оставаться свободными до отдельного
selector.

## Compliance check

- Scale-map rank/determinant `2/2`.
- Full package Jacobian rank/determinant `6/(50/9)`.
- Common scale links `2/2`, channel labels `3/3`.
- Relative-ratio origin `0/4`, source-covector origin `0/2`.
- Следующий гейт:
  `version9_endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate`.

## Links

- [[version9-endpoint-creation-kms-source-vector-common-parent-architecture-gate]]
- [[version9-endpoint-creation-kms-gap-conductance-parent-origin-gate]]
- [[tome9-opening-contract]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_source_covector_four_slot_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_source_covector_four_slot_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_source_covector_four_slot_parent_origin_gate_results.json`