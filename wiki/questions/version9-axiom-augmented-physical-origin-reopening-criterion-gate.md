# Критерий переоткрытия physical-origin программы Тома IX

> Status: mature
> Type: question
> Updated: 2026-09-01

## Summary

Три открытых физических критерия сжимаются в два независимых
provenance-пакета. Переоткрытие требует одновременно вывести physical
scale/coupling selector и physical origin logdet parent-term; текущая
availability равна `0/2`, поэтому заморозка статуса сохраняется.

## Key Points

- Deficit: `d_phys=(1,1,1)^T`.
- Reopening map:
  `R=[[1,0],[0,1],[0,1]]`, `rank R=2`.
- Joint dossier `(1,1)^T` покрывает deficit `3/3`.
- Ни один столбец отдельно deficit не покрывает.
- Conditional availability равна `(1,1)`, physical availability — `(0,0)`.
- Допустимы только source-free, target-independent certificates внутри
  одного bounded-below common parent.

## Answer

Минимальный reopening dossier состоит из двух independent physical-origin
certificate. Logdet-origin одновременно открывает physical Hessian и blind
следствие, поэтому число пакетов равно двум, а не трём. Однако ни один из
них пока физически не получен: physical deficit coverage `0/3`, reopening
status `0/2`.

## Links

- [[version9-endpoint-creation-kms-logdet-axiom-augmented-conditional-program-status-gate]] — predecessor.
- [[physical-origin-reopening-criterion-sources-2026]] — доказательная база.
- [[live-formulas-gates-version9-33]] — формулы гейта.
- [[current-status-and-next-vectors]] — актуальный фронтир.

## Source Notes

- `s2t/gates/version9_axiom_augmented_physical_origin_reopening_criterion_gate.tex`
- `s2t/audits/s2t_v9_axiom_augmented_physical_origin_reopening_criterion_gate.py`
- `s2t/results/s2t_v9_axiom_augmented_physical_origin_reopening_criterion_gate_results.json`
- `s2t/proofdsl/examples/version9_physical_origin_reopening_criterion.py`