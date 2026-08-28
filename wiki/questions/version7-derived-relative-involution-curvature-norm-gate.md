# Version VII: производная относительная инволюция или общая норма кривизны

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Обычный тепловой суперслед одной нечётной Real-суперсвязности сокращается до
индекса и не воспроизводит формальный локальный потенциал. Ручная вставка
`K_role=diag(-1,-1,+1)` запрещена.

## Search for Solution

Построена положительная сумма выведенной рёберной Hodge-нормы и относительной
Gram-кривизны физического incidence-блока `10x11`. Проверен полный гессиан
на семи корневых и двадцати тяжёлых направлениях как функция единственного
отношения `beta`.

## Result

- тяжёлые моды положительны точно при `0 <= beta < 8/15`;
- `beta=1/2` даёт нулевую сигнатуру `(7,0,20)`;
- тяжёлая щель равна `0.4`;
- целевой вакуум имеет `(0,0,27)` и минимальную моду `5.6`;
- равный вес `beta=1` не проходит;
- происхождение `beta=1/2` остаётся открытым.

## Compliance Check

Обе матрицы гессиана получены аналитической линеаризацией Gram-кривизн;
критическая граница уточнена численно и совпала с точным `8/15`.

## Links

- [[version7-real-superconnection-common-trace-origin-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-common-carrier-root-stationarity-gate]]
- [[version7-real-half-trace-curvature-weight-gate]]
- [[superconnection-curvature-norm-normalization-literature-2026]]

## Source Notes

- `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex`
- `s2t/audits/s2t_v7_derived_relative_involution_curvature_norm_gate.py`
- `s2t/results/s2t_v7_derived_relative_involution_curvature_norm_gate_results.json`