# Источники minimal selector относительных KMS-shapes

> Status: mature
> Type: source
> Updated: 2026-08-31

## Summary

Log-ratio coordinates дают глобальную параметризацию внутренности simplex,
а log-partition functional обеспечивает строго выпуклую dual-архитектуру.
В гейте эти методы применены к двум weighted-simplex с весами `1+1+3`.

## Key Points

- J. Aitchison (1982) вводит log-ratio анализ compositional data.
- Внутренняя точка трёхкомпонентного simplex имеет две независимые
  log-ratio координаты.
- Два KMS-пакета поэтому требуют четыре координаты.
- Конкретный weighted log-partition parent и его exact Hessian выведены
  непосредственно в гейте, а не заимствованы как физический selector.
- Maximum entropy выбирает isotropic representative только после принятия
  дополнительного inference-принципа; это не доказывает происхождение
  соответствующего parent-term.

## Links

- [[version9-endpoint-creation-kms-relative-shape-minimal-selector-architecture-gate]]
- [[version9-endpoint-creation-kms-source-covector-four-slot-parent-origin-gate]]

## Source Notes

- J. Aitchison, “The Statistical Analysis of Compositional Data,” Journal
  of the Royal Statistical Society, Series B 44 (1982), 139–177.
- E. T. Jaynes, “Information Theory and Statistical Mechanics,” Physical
  Review 106 (1957), 620–630.
- `s2t/gates/version9_endpoint_creation_kms_relative_shape_minimal_selector_architecture_gate.tex`
- `s2t/gates/version9_endpoint_creation_kms_relative_shape_selector_source_parent_origin_gate.tex`