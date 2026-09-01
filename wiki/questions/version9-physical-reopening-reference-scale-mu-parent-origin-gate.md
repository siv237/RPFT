# Parent-origin физического reference scale mu

> Status: mature
> Type: question
> Updated: 2026-09-01

## Summary

Восемь доступных кандидатов проверены по пяти условиям physical origin.
Ни один не имеет одновременно внутреннего selector, typed map к Gaussian
carrier и разрыва общего scale-orbit без target input.

## Key Points

- Candidate matrix имеет shape `8x5` и rank `4`.
- Pass vector равен `(0,0,0,0,0,0,0,0)`.
- Relative-scale map имеет rank/nullity `7/1`.
- KMS temperature, clock energy, cutoff и inverse radius дают отношения,
  но не абсолютную единицу.
- Observed mass target-loaded.
- Dimensional transmutation — ближайший кандидат `3/5`, но beta-function,
  boundary coupling и typed map не выведены.

## Answer

Физический reference scale `mu` в текущем корпусе отсутствует. Любая сеть
relative calibrations сохраняет одну common scaling zero mode. Physical
origin равен `0/1`, оба reopening packages остаются `0/2`; Том IX готов к
финальной отрицательной фиксации.

## Links

- [[version9-physical-reopening-gaussian-reference-state-parent-origin-gate]] — predecessor.
- [[reference-scale-mu-parent-origin-sources-2026]] — scale-anchor evidence.
- [[live-formulas-gates-version9-36]] — формулы гейта.
- [[current-status-and-next-vectors]] — актуальный фронтир.

## Source Notes

- `s2t/gates/version9_physical_reopening_reference_scale_mu_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_physical_reopening_reference_scale_mu_parent_origin_gate.py`
- `s2t/results/s2t_v9_physical_reopening_reference_scale_mu_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_reference_scale_mu_parent_origin.py`