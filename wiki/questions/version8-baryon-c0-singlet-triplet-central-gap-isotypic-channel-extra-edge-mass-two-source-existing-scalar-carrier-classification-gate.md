# Классификация существующих скалярных носителей двух источников

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Есть ли в активном изотипическом parent два независимых скалярных режима,
способных нести source-компоненты `j_A,j_B`?

## Search for solution

- Классифицированы радиусы и определители полей `B,M`.
- Проверен радиальный якобиан при выровненном вакууме.
- Проверены spectator-радиусы трёх дополнительных рёбер.
- Построена общая портальная матрица между скалярами и центром `A,B`.

## Expected result

Два активных ненулевых инварианта должны иметь независимый динамический
отклик; полный проход дополнительно требовал канонической ненулевой
портальной матрицы в унаследованном действии.

## Compliance check

- `T_B=Tr(BB*)=3`, `T_M=Tr(MM*)=2`.
- Радиальный якобиан равен `diag(6,4)`, determinant `24`, rank `2`.
- Определители не добавляют нового первого порядка; spectator-rank равен `0`.
- Пространство допустимых portal-matrix равно `M2(R)` и имеет размерность `4`.
- Унаследованный смешанный гессиан равен нулю.
- Carrier-classification `6/6`; canonical pairing `0/5`; portal-origin `0/4`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-parent-architecture-gate]]
- [[extra-edge-mass-two-source-carrier-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate_results.json`