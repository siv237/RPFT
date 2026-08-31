# Происхождение горизонтальной плоской моды

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Плоская мода разложена по двум изотипическим фазам: трём стрелкам
`up`-блока и семи остальным стрелкам. Метрика фазовой плоскости равна
`diag(6,20)`, её связь с калибровочной орбитой имеет единственную строку
`(-6,8)`, поэтому горизонтальная комбинация фиксирована как `4:3`.

Для фазового семейства `A(z)=diag(z^4 I_3,z^3 I_7)A0` оба грамовых конца
не меняются точно. Значит, любой родитель из `AA*`, `A*A` и следовых слов
слеп к этой фазе на всех порядках.

Обычный determinant отсутствует: максимальные миноры матрицы `10x11`
образуют 11-мерный ковектор. Фазочувствительный скаляр потребовал бы новой
свёртки или ориентации; ручной массовый член не допускается.

## Следующий вопрос

Проверить, существует ли каноническая determinant-line свёртка из уже
имеющихся Real, градуировочных и инцидентных данных.

## Связи

- [[version8-gauge-invariant-vacuum-hessian-reconstruction-gate]]
- [[version4-determinant-line-inflow-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Исходники

- `s2t/gates/version8_horizontal_flat_direction_parent_lift_gate.tex`
- `s2t/audits/s2t_v8_horizontal_flat_direction_parent_lift_gate.py`
- `s2t/results/s2t_v8_horizontal_flat_direction_parent_lift_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_flat_direction_parent_lift.py`