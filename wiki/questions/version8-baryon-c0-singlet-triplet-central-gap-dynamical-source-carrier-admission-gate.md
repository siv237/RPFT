# Допуск динамического носителя источника центральной щели

> Status: mature
> Type: question
> Updated: 2026-08-31

## Итог

Одна вещественная singlet-координата `s` условно заменяет внешний источник.
Потенциал `V=M lambda²/2-g s lambda+u s⁴/4` имеет седло в нуле и два
устойчивых ненулевых вакуума:
`s*²=g²/(uM)`, `lambda*²=g⁴/(uM³)`, `j*=g s*`.

Архитектура совместима с gauge-, family-, grading- и Real-условиями и
проходит `8/8`. Однако вакуумы связаны отражением
`(s,lambda)->(-s,-lambda)`, поэтому знак не выбран. Носитель, его метрика и
коэффициенты `M,g,u` не происходят из текущего действия: origin-ledger
равен `0/4`.

## Связи

- [[version8-baryon-c0-singlet-triplet-central-gap-source-stiffness-parent-origin-gate]]
- [[version8-baryon-c0-singlet-triplet-central-gap-minimal-source-parent-architecture-gate]]
- [[version8-smooth-relative-background-order-parameter-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate_results.json`