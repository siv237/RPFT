# Селектор центрального симплекса масс дополнительных рёбер

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Выбирают ли счётный след, максимум энтропии, калибровочная симметрия,
унимодулярность, gauge matching, KMS или стационарность единственную точку
симплекса `p_Y:p_u:p_d`?

## Search for solution

- Сопоставлены равная микроскопическая плотность и равная масса на ребро.
- Вычислены максимум и гессиан центральной энтропии на блоках `4+6+6`.
- Найден неподвижный центр type-сохраняющей группы.
- Проверено унимодулярное фазовое ограничение.
- Сравнены образы двух trace-кандидатов под gauge-index matrix.
- Построена общая Gibbs-параметризация двумя энергетическими разрывами.
- Проверена вариация trace-весов на физическом вакууме.

## Expected result

Положительный проход требовал одного внутреннего принципа, который оставляет
единственную верную точку симплекса без наблюдаемой калибровки. Отрицательный
результат должен был локализовать минимальное число новых параметров.

## Compliance check

- Счётный trace даёт отношение `2:3:3`.
- Равная edge-масса даёт `1:1:1`; два кандидата непропорциональны.
- Максимум энтропии единственен, но повторяет условный счётный trace.
- Type-сохраняющий неподвижный центр имеет размерность `3`.
- Унимодулярность имеет фазовый ранг `1`, nullity `2`, от `p` не зависит.
- Gauge-index matrix обратима и потому только реконструирует веса из внешней
  тройки коэффициентов.
- Gibbs-класс использует две независимые щели и реализует весь симплекс.
- Вакуумный гессиан по весам имеет ранг `0`.
- Conditional conventions: `2/2`; intrinsic selectors: `0/8`.

## Boundary

Точка `2:3:3` остаётся хорошим условным кандидатом, но не предсказанием.
Минимальная тепловая запись требует двух независимых безразмерных разрывов.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-parent-origin-gate]]
- [[extra-edge-mass-central-trace-simplex-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_trace_simplex_selector_gate_results.json`