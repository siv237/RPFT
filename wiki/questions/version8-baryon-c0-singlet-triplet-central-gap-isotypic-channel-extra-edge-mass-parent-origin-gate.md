# Parent-origin масс трёх дополнительных рёбер

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Порождает ли одна суперсвязность положительные массы полей `Z_L-Y_R`,
`Z_L-u_R`, `Z_L-d_R`, и фиксирует ли общий след их отношения?

## Search for solution

- Построены три точных самосопряжённых off-diagonal блока.
- Вычислен физический полуслед их квадрата.
- Классифицировано центральное семейство положительных trace-метрик.
- Проверены попарные gauge-интертвинеры.
- Вычислена матрица `U(1)`, `SU(2)`, `SU(3)` индексов и её ранг.
- Архитектура сопоставлена с первичными работами по spectral action и
  конечным спектральным тройкам.

## Expected result

Строгий проход требовал единственного положительного trace-state, который
фиксирует две относительные массы, и внутреннего источника общего масштаба.
Условный проход должен был хотя бы вывести три квадратичные нормы из одного
оператора.

## Compliance check

- Полуслед даёт `2|z_Y|²+3|z_u|²+3|z_d|²`.
- Незавешенный кандидат имеет отношение масс `2:3:3`.
- Центр трёх неэквивалентных блоков трёхмерен; веса `p_Y,p_u,p_d>0`
  меняют коэффициенты на `(2p_Y,3p_u,3p_d)`.
- Два верных свидетеля дают непропорциональные векторы `(2,3,3)` и
  `(2,6,3)`.
- Gauge-index matrix имеет определитель `-7/4` и ранг `3`, поэтому не
  накладывает массового соотношения.
- Trace-shape ledger закрыт `5/5`; relative origin `0/5`; scale origin
  `0/2`.

## Boundary

Форма стабилизатора выведена условно, но незавешенный trace не выбран
внутренне. Абсолютный spectral/cutoff масштаб также остаётся новым входом.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-full-graph-aligned-parent-embedding-gate]]
- [[extra-edge-mass-parent-origin-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_parent_origin_gate_results.json`