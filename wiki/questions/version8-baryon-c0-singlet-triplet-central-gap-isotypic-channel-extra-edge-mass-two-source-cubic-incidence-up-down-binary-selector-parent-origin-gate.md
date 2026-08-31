# Parent-origin бинарного u/d-селектора incidence

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Может ли существующий parent выбрать между финальными назначениями
`B->u,M->Y` и `B->d,M->Y` без нового ориентированного параметра?

## Search for solution

- Сопоставлены размерности и индексы `SU(2)`, `SU(3)` и `U(1)`.
- Проверены чётные и нечётные гиперзарядные моменты на Real-удвоении.
- Проверено, является ли incidence-проектор динамической переменной.
- Построен минимальный центрированный различитель `S_ud`.

## Expected result

Полный проход требовал inherited typed-члена с фиксированным знаком либо
единого динамического пространства, содержащего обе incidence-ветви.

## Compliance check

- Размерность и не абелевы индексы дают ничью.
- Квадратичные `U(1)`-индексы равны `25/3` и `4/3`; положительный условный
  score предпочитает `d`.
- Нечётные Real-моменты и вектороподобные аномалии сокращаются.
- `Tr((P_u-P_d)^2)=12`, а непрерывная касательная между двумя фиксированными
  диаграммами имеет размерность ноль.
- `S_ud=Y²-(29/18)I` имеет собственные значения `±7/6`, норму `49/3` и
  спаривание `Tr(A_ud S_ud)=14`.
- Typed-связь, её знак и межгеометрическая мера не наследованы.
- Exact representation `8/8`, conditional discriminator `5/5`,
  parent-origin `0/7`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-assignment-selector-gate]]
- [[up-down-incidence-selector-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_parent_origin_gate_results.json`