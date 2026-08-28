# Version VII: Real- и аномальный допуск минимальной зеркальной пары

> Status: mature
> Type: question
> Updated: 2026-08-27

## Summary

Двухвершинная зеркальная пара проходит строгий первый порядок и формально
замыкается Real-структурой, но физический admission провален.

## Exact Result

Кандидат `X_L=(C,C,L)`, `Y_R=(H,C,R)` замыкает шестикромочный цикл. В
каноническом зеркальном чтении это левый заряженный синглет и правый слабый
дублет. Их добавочные коэффициенты равны `A_221=1/2`, `A_111=-3/4`, а число
новых слабых дублетов нечётно.

При произвольных гиперзарядах локальные уравнения вынуждают оба заряда стать
нулевыми, но глобальное mod-2 препятствие остаётся. Real-удвоение не является
новым независимым физическим Weyl-сектором и не исправляет аномалии.

## Physical Obstruction

Разрешённые блоки `X_L-e_R` и `L_L-Y_R` при общей невырожденной массе
спаривают исходные лептоны. Поэтому минимальная пара одновременно не
аномально безопасна и не сохраняет лёгкий хиральный `H15` без ручной
настройки ранга.

## Verdict

Две вершины недостаточны. Консервативный аномально безопасный ремонт требует
добавить также `X_R` и `Y_L`, то есть перейти минимум к четырём новым
физическим хиральным вершинам. Это новый кандидат, а не полученный результат.

## Subsequent Result

[[version7-four-vertex-vectorlike-selector-gate]] показал, что ремонт
действительно безаномален и сохраняет хиральный индекс `H15`. Он условно
допущен как носитель, но разрешает пять лишних рёбер и не выбирает
ориентацию лёгкого ядра.

## Links

- [[version7-r2-minimal-architecture-branch-gate]]
- [[version7-r2-generalized-fluctuation-seed-origin-gate]]
- [[version7-rank-change-parent-program]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[mixed-connector-extension-architecture-literature-2026]]
- [[mixed-connector-krajewski-leptoquark-literature-2026]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_minimal_mirror_pair_real_anomaly_gate.tex`
- `s2t/audits/s2t_v7_minimal_mirror_pair_real_anomaly_gate.py`
- `s2t/results/s2t_v7_minimal_mirror_pair_real_anomaly_gate_results.json`