# Parent-origin четырёх relative-shape sources

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, выводятся ли четыре linear source-компоненты minimal KMS shape
selector из inherited parent, types, endpoint-defects, KMS и transport.

## Search for solution

- Проверен source-free log-partition parent и его boundary infimum.
- Вычислены ranks scale-, swap-, cross-lock- и combined constraints.
- Endpoint-defects продолжены до positive one-parameter family.
- Maximum entropy отделён от физического parent-origin.
- Построены два admissible source-пакета с разными shapes.

## Expected result

Каждый кандидат должен либо единственно выбрать четыре sources, либо дать
точный witness остаточной свободы без скрытого inference postulate.

## Compliance check

- Source-free interior minimum отсутствует.
- Candidate origin `0/8`; combined swap/lock nullity `1`.
- Conditional maximum-entropy representative `1/1`, physical origin `0/4`.
- Selector-source и relative-shape origin остаются `0/4`.
- Следующий гейт:
  `version9_endpoint_creation_kms_relative_shape_selector_source_minimal_invariant_parent_architecture_gate`.

## Links

- [[version9-endpoint-creation-kms-relative-shape-minimal-selector-architecture-gate]]
- [[version9-endpoint-creation-kms-source-covector-four-slot-parent-origin-gate]]
- [[kms-relative-shape-selector-sources-2026]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate_results.json`