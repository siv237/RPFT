# Минимальный selector относительных KMS-shapes

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Построить минимальный bounded selector четырёх относительных величин,
оставшихся после выделения общих gap- и conductance-scales.

## Search for solution

- Две weighted-simplex параметризованы четырьмя глобальными log-ratios.
- Для каждой shape построен log-partition functional с linear source.
- Доказаны strict convexity, coercivity и единственность минимума.
- Selector связан с KMS source-parent через completed squares.
- Проверены минимальность размерности и точный несимметричный witness.

## Expected result

Один четырёхмерный selector должен условно выбирать все четыре relative
shapes без нарушения положительности и без добавления нового scale.

## Compliance check

- Shape chart rank `4`, минимальная размерность `4`.
- Selector architecture `10/10`, conditional selection `4/4`.
- Selector Hessian rank/determinant `4/(9/25)`.
- Common Hessian rank/determinant `12/(5184/25)`.
- Selector-source origin `0/4`.
- Следующий гейт:
  `version9_endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-source-covector-four-slot-parent-origin-gate]]
- [[version9-endpoint-creation-kms-source-vector-common-parent-architecture-gate]]
- [[kms-relative-shape-selector-sources-2026]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate_results.json`