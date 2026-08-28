# Version VII: инцидентный передаточный и марковский вес

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Размерностное отношение `11/21` лежит в допустимом окне и даёт правильный
гессиан, но обычный след source-проектора не масштабирует всю физическую
кривизну и проваливается с сигнатурой `(8,0,19)`.

## Search for Solution

Полярная часть фонового оператора типа `10 x 11` выделяет согласованные
десятимерные углы и один индексный дефект. Проверены source-only кривизна,
однократная UCP-карта

`T_U(X,Y)=(U X U*+Y)/2`

и полное сохраняющее след условное ожидание, дублирующее общий угол.

## Expected Result

Число `11/21` не является фундаментальным весом. Операторное разложение имеет
вид `21=10+10+1`. Однократное quotient-чтение точно даёт половину исходного
физического гессиана, сигнатуру `(7,0,20)`, тяжёлую щель `2/5` и устойчивый
вакуум. Полное сохраняющее след ожидание считает согласованный угол дважды,
возвращает `(21,0,6)` и проваливается. Поэтому получен локальный UCP-проход,
но физическое происхождение редуцированного quotient ещё не доказано.

## Links

- [[version7-common-irreducible-trace-multiplicity-gate]]
- [[version7-real-superconnection-common-trace-origin-gate]]
- [[vertex-edge-hodge-dirac-literature-2026]]
- [[polar-transfer-linking-expectation-literature-2026]]
- [[version7-index-defect-reduced-linking-quotient-gate]]

## Source Notes

- `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex`
- `s2t/audits/s2t_v7_incidence_transfer_markov_weight_gate.py`
- `s2t/results/s2t_v7_incidence_transfer_markov_weight_gate_results.json`