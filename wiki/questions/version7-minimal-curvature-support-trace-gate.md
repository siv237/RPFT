# Version VII: минимальная опора кривизны и след

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, даёт ли сжатие к минимальной концевой опоре единственный общий
след рёберной и связывающей кривизн.

## Search for Solution

Сжатие `42 -> 21` сохраняет след. Коммутант связывающего семейства
одномерен, поэтому оно порождает `M21(C)`. Диагональный рёберный суррогат
порождает `C^54`. Общая алгебра имеет центр размерности `55` и `54`
свободных параметра верного нормированного следа.

Даже в физической факторной модели `M22(C) direct_sum M21(C)` остаётся один
центральный относительный вес. Простой `M75` потребовал бы нового
внедиагонального блока комплексной размерности `1134`, а простой `M43` —
`462`.

## Expected Result

- Минимальная опора не выводит единственный общий след.
- Поточечная ранговая нормировка закрыта из-за скачка опорного проектора.
- Качественные сигнатуры `(7,0,20)` и `(0,0,27)` сохраняются.
- Количественный массовый спектр зависит от центрального веса.
- Следующий гейт фиксирует строгую качественную часть и запрещает
  преждевременные массовые предсказания.

## Links

- [[version7-affine-defect-bicomplex-completion-gate]]
- [[version7-common-chain-number-hodge-relative-trace-gate]]
- [[version7-common-irreducible-trace-multiplicity-gate]]
- [[finite-factor-trace-multiplicity-literature-2026]]
- [[version7-minimal-support-trace-project-intuition-search]]
- [[version7-qualitative-parent-mass-metric-freeze-gate]]

## Source Notes

- `s2t/gates/version7_minimal_curvature_support_trace_gate.tex`
- `s2t/audits/s2t_v7_minimal_curvature_support_trace_gate.py`
- `s2t/results/s2t_v7_minimal_curvature_support_trace_gate_results.json`