# Допуск Real-ориентированного голоморфного цикла

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Полный двуслойный колчан не имеет чисто голоморфных направленных циклов:
его повышающая матрица удовлетворяет `N²=0`. Real-структура добавляет
обратные стрелки как `N*`, а не как независимое поле. Полный оператор
`D_R=N+N*` нечётен и вдоль горизонтальной фазы меняется только подобием.

Точные моменты равны `(Tr D,Tr D³,Tr D⁵)=(0,0,0)` и
`(Tr D²,Tr D⁴,Tr D⁶)=(22,110,682)` независимо от фазы. Освобождение
обратного носителя увеличило бы размерность переноса с `40` до `80`
вещественных направлений. Формальный ориентирующий знак также несовместим с
положительной инволюцией: условия `alpha beta=-1` и
`beta=conjugate(alpha)` потребовали бы `|alpha|²=-1`.

## Следующий вопрос

Проверить, существует ли на нынешнем носителе каноническая комплексная
симплектическая форма и поляризация. Если они требуют новой меры или
независимого обратного поля, это должно быть зафиксировано как расширение
архитектуры, а не скрытый вывод Real-структуры.

## Связи

- [[version8-horizontal-phase-heavy-arrow-cycle-admission-gate]]
- [[version5-derived-moment-map-minimal-data-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version4-determinant-line-inflow-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_real_oriented_cycle_admission_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_real_oriented_cycle_admission_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_real_oriented_cycle_admission_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_real_oriented_cycle_admission.py`