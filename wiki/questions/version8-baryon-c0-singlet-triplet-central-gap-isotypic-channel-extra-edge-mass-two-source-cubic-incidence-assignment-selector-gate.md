# Селектор кубического incidence-назначения двух источников

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Выбирают ли determinant, trace-метрика, обусловленность, кратности или
gauge-типы одно из шести полноранговых incidence-назначений?

## Search for solution

- Вычислены determinants и метрические площади всех шести кандидатов.
- Вычислены точные condition numbers после whitening trace-метрикой.
- Проверено совпадение кратностей `3,2` с секторами.
- Проверены ориентационный знак, gauge-неэквивалентность и equal-gap мишень.

## Expected result

Полный проход требовал единственного финалиста без наблюдаемой калибровки.

## Compliance check

- Maximum determinant и metric area оставляют четыре назначения.
- Minimum condition и dimension match оставляют `(u,Y)` и `(d,Y)`.
- `kappa_min²=(27+3sqrt(17))/(27-3sqrt(17))`.
- Два финалиста дают gap-rays `(0,-1)` и `(-1,0)`.
- Знак determinant зависит от ориентации; gauge-типы не выбирают ветвь.
- Equal-gap условие требует `c_B=0` и понижает portal-rank до одного.
- Exact classification `8/8`; intrinsic selector `0/8`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-portal-matrix-parent-origin-gate]]
- [[extra-edge-mass-cubic-incidence-selector-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_assignment_selector_gate_results.json`