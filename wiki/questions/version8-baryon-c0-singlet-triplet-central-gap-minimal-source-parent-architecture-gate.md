# Минимальная source-parent архитектура центральной щели

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Общий квадратичный многочлен имеет единственный ненулевой глобальный
минимум только при наличии положительного квадратичного и ненулевого
линейного членов. Поэтому минимальная форма равна
`V=m² lambda²/2-j lambda`, а её вакуум — `lambda*=j/m²`.

Операторное поднятие на центральную прямую `R Q` совместимо с семейным
`SO(3)`, градуировкой и Real-структурой. Отражение `lambda -> -lambda` не
является обязательной симметрией: singlet- и triplet-проекторы имеют ранги
один и три.

Архитектура условно проходит `7/7`, но происхождение параметров имеет
реестр `0/2`. Луч `(m²,j)->(a m²,a j)` сохраняет вакуум и меняет гессиан;
для восстановления обоих коэффициентов нужен независимый двухточечный
отклик.

## Связи

- [[version8-baryon-c0-singlet-triplet-central-gap-coefficient-selector-gate]]
- [[version8-baryon-c0-singlet-triplet-central-gap-parent-action-origin-gate]]
- [[version8-baryon-c0-singlet-triplet-central-weight-minimal-hamiltonian-data-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate_results.json`