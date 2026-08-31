# Parent-origin полной портальной матрицы двух источников

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Может ли единый операторный след породить полную rank-two portal-matrix от
радиусов `T_B,T_M` к центральным направлениям `A,B`?

## Search for solution

- Проверена аддитивность моментов прямой суммы.
- Построен минимальный общий кубический блок.
- Вычислены три центральных charge-вектора.
- Перебраны девять упорядоченных incidence-назначений.
- Сравнены один общий и два независимых кубических коэффициента.

## Expected result

Условная конструкция должна была дать rank-two карту; полный parent-origin
требовал её присутствия и единственности в унаследованном действии.

## Compliance check

- Прямая сумма имеет нулевой смешанный гессиан.
- `Tr X³=d lambda³+3 lambda T` создаёт условный портал.
- Из девяти назначений шесть имеют rank `2`; determinants `±2,±3`.
- Два коэффициента дают determinants `108` или `162`.
- Один общий коэффициент оставляет шесть дискретных source-лучей.
- Inherited odd coefficients равны нулю.
- Conditional shape `7/7`; incidence selector `0/5`; parent-origin `0/4`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-existing-scalar-carrier-classification-gate]]
- [[extra-edge-mass-two-source-portal-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate_results.json`