# Intertwiner чётного coherence-угла и семейного триплета

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Существует ли типизированное отображение из трёхмерного угла
`Lambda²W*` coherence-chain в активный стандартный family-triplet?

## Search for solution

- Решены intertwiner-системы для текущей product-group
  `(U(2)_{eX} x U(1)_Y) x SO(3)_fam`.
- Отдельно проверены семейный `SO(3)`, остаток `A4` и канальная группа.
- Исследована условная диагональная ветвь, где `W` повышается до
  ориентированного стандартного `R3`.
- Построен Hodge-map `Lambda²R3 -> R3`, вычислены Hom и изометрическая
  нормировка.

## Expected result

Текущий проход требовал ненулевого Hom без смешивания различных
бимодульных типов. Условный проход должен был явно перечислить цену
превращения случайной `U(3)`-симметрии нормы в физическое действие.

## Compliance check

- Текущий `SO(3)`-Hom: ранг системы `9`, nullity `0`.
- Текущий `A4`-Hom: ранг `9`, nullity `0`.
- Канальный Hom в тривиальный target: ранг `9`, nullity `0`.
- Полный current-intertwiner ledger: `0/4`.
- После условного повышения `W` система имеет ранг `8` и
  `Hom=R *`, где `*` — Hodge-map.
- `*^T*=I3`, `det(*)=1`; нормированные карты равны `+-*`.
- Требуются три новые структуры: унификация channel-бимодулей,
  диагональный `SO(3)`-lock и ориентированная метрика/знак.

## Boundary

Условный Hodge-map не принадлежит текущей теории: `W_Y` имеет иной
бимодульный тип, чем `W_e,W_X`. Portal parent-origin остаётся открытым.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-edge-coherence-radius-portal-parent-origin-gate]]
- [[version7-edge-coherence-bimodule-admission-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version8-baryon-c0-family-to-multiplicity-intertwiner-admission-gate]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate_results.json`
