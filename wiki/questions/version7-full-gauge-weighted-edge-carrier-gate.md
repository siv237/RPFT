# Version VII: полный калибровочно-взвешенный носитель рёбер

> Status: mature
> Type: question
> Updated: 2026-08-27

## Problem

Незавешенный Hodge-след по одиннадцати меткам рёбер не совпадает с
физическим gauge-следом по полным представлениям. Нужно проверить,
сохраняются ли селектор `6 из 11`, единый Hodge-потенциал и его гессиан
после раскрытия цветовых, слабых, гиперзарядовых, семейных и Real-кратностей.

## Search for Solution

Для всех одиннадцати рёбер построен минимальный multiplet-подъём с
тождественным стягиванием общего фактора концов. Выбранная часть имеет
комплексную размерность 10, конкурирующая — 11. При любых положительных
trace-весах прежний селектор сохраняет опору, а полный 42-мерный
вещественный гессиан имеет сигнатуры `(20,0,22)` в нуле и `(0,14,28)` в
вакууме до gauge-quotient.

Однако среди шести обязательных ненулевых блоков находятся
`Q_L-Y_R ~ (3,1)_(2/3)` и `X_L-u_R ~ (3,1)_(5/3)`. Фундаментальная тройка
не имеет ненулевого `SU(3)`-инвариантного вектора, поэтому их нормы
`mu>0` неизбежно нарушают цвет.

## Expected Result

Получен смешанный, но физически отрицательный результат. Структурная опора
`6 из 11` устойчива к полным положительным весам, однако её фундаментальный
ненулевой вакуум разрушает `SU(3)_c`. Цветные рёбра могут оставаться
возбуждениями либо входить в составной цветосинглетный циклический оператор,
но не быть самостоятельными вакуумными конденсатами.

## Links

- [[version7-common-gauge-f0-anchor-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-rooted-cycle-isotypic-edge-projector-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version7-color-preserving-composite-cycle-parent-gate]]

## Source Notes

- `s2t/gates/version7_common_gauge_f0_anchor_gate.tex`
- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`
- `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex`
- `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex`
- `s2t/results/s2t_v7_full_gauge_weighted_edge_carrier_gate_results.json`