# Происхождение центрального следового веса синглета и триплета

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Обычный счётный след и максимум энтропии условно дают `p=1/4`, `r=1`, но
оба требуют дополнительного принципа равной микроскопической плотности.
Центральное переопределение
`Z_p=4p P1+4(1-p)P3/3` сохраняет `SO(3)`, grading, положительность и
нормировку, реализуя любой `0<p<1`.

Нормированный grading-суперслед неположителен. Общий центральный
Gibbs-гамильтониан лишь параметризует симплекс:
`p=1/(1+3 exp(-beta Delta))`, поэтому каждый вес эквивалентен свободному
безразмерному разрыву `beta Delta=log(3p/(1-p))`. Итоговый parent-origin
ledger равен `0/6`.

## Связи

- [[version8-baryon-c0-family-triplet-singlet-relative-rate-selector-gate]]
- [[version8-baryon-c0-common-trace-embedding-normalization-gate]]
- [[version8-baryon-c0-multiplicity-environment-hamiltonian-parent-origin-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate_results.json`