# Допуск determinant-line свёртки горизонтальной фазы

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Кофакторный вектор максимальных миноров точно равен
`(0,0,0,0,0,0,-1,0,0,1,0)` и порождает ядро инцидентности. На
горизонтальной фазовой окружности он преобразуется как `z^33`, поэтому
determinant-line действительно видит плоскую моду.

Но канонической скалярной свёртки нет. Determinant-гиперзаряды источника и
цели оба равны `-2`, после их сокращения носитель миноров эквивалентен
11-мерному источнику, а `dim Hom_G(E_s,C)=0`. Real-пара оставляет только
постоянный модуль `2`. Свёртка с фиксированным ядром вакуума была бы новым
фон-зависимым выбором.

## Следующий вопрос

Проверить, закрывают ли уже найденные тяжёлые стрелки фазочувствительный
калибровочный цикл без добавления нового концевого состояния.

## Связи

- [[version8-horizontal-flat-direction-parent-lift-gate]]
- [[version8-bimodule-multiplicity-separator-gate]]
- [[version4-determinant-line-inflow-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_determinant_line_admission_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_determinant_line_admission_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_determinant_line_admission_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_determinant_line_admission.py`