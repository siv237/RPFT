# Допуск тяжёлых стрелочных циклов горизонтальной фазы

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Полный девятивершинный граф бимодульной опоры связен, имеет 11 рёбер и
цикл-ранг `3`. Инцидентностные семь рёбер образуют лес, тогда как проекция
четырёх тяжёлых рёбер на цикл-пространство имеет ранг `3`: тяжёлые стрелки
действительно создают все независимые циклы.

Однако фазовую моду они не видят. Единственная стрелка в `u_R`, где
горизонтальный вес равен `4`, является листом и отсутствует во всех циклах.
Для точного базиса `C` имеем `qC=(0,0,0)`, где
`q=(4,3,3,3,3,3,3,3,3,3,3)`. Любой обычный след голономии чередует поле и
его сопряжение, поэтому целевая фаза сокращается.

## Следующий вопрос

Проверить, превращает ли Real-структура сопряжённые стрелки в допустимую
независимую ориентированную голоморфную свёртку. Простое переименование
`A*` новым полем не допускается.

## Связи

- [[version8-horizontal-phase-determinant-line-admission-gate]]
- [[version8-bimodule-multiplicity-separator-gate]]
- [[version7-baseline-rooted-primitive-cycle-admission-gate]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_heavy_arrow_cycle_admission_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_heavy_arrow_cycle_admission_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_heavy_arrow_cycle_admission_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_heavy_arrow_cycle_admission.py`