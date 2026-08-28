# Version VII: общий носитель и корневая стационарность

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, существует ли незамороженная корневая стационарная точка
формального общего Hodge--cycle профиля и положителен ли полный смешанный
гессиан.

## Search for Solution

Одновременно варьировались три старых заряженных и четыре новых
singlet-ребра. Их точные Hodge-тепловые вклады объединены с физическим
Gaussian при общей шкале `t=1` и единичных следовых кратностях.

Найдено решение

$$
(1.07737088,1.07737088,1.03492564,1.02768473,
1.04972668,1.00214566,1.07390997).
$$

## Expected Result

Максимальный остаток семи стационарных уравнений меньше `3e-15`. Корневой
гессиан положителен. После включения двадцати тяжёлых направлений и
ненулевого корнево-тяжёлого смешивания полный гессиан имеет сигнатуру
`(0,0,27)` и минимальное собственное значение `1.14399252085`.

Это формальный локальный вакуумный проход. Открытым остаётся происхождение
трёх следовых блоков из одной физической Real-суперсвязности:
[[version7-real-superconnection-common-trace-origin-gate]].

## Compliance Check

- Два запуска дали одинаковый SHA-256.
- Все семь корней варьировались, тяжёлые поля не замораживались в гессиане.
- Смешанный блок вычислен явно и не занулён вручную.
- Статус: `formal local vacuum pass; Real-superconnection origin open`.

## Links

- [[version7-exact-profile-hodge-cycle-unification-gate]]
- [[version7-real-superconnection-common-trace-origin-gate]]

## Source Notes

- `s2t/gates/version7_common_carrier_root_stationarity_gate.tex`
- `s2t/audits/s2t_v7_common_carrier_root_stationarity_gate.py`
- `s2t/results/s2t_v7_common_carrier_root_stationarity_gate_results.json`