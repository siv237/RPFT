# Version VI: составный оператор Каллиаса

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Естественная масса `Q/Delta` делает составной дефект фредгольмовым, но её
индекс равен нулю. Ненулевой индекс возникает только на spin-cover
носителе.

## Results

- `Q/Delta` имеет асимптотический спектр `(2/3,-1/3,-1/3)` и обратим;
- положительная линия порождена вещественным директором `n`, поэтому
  `c1=0` и индекс Каллиаса равен нулю;
- spinor-масса `n dot sigma` имеет хопфову положительную линию с `c1=1`;
- коэффициентный ранг 15 даёт индексы `+15/-15`;
- прямой нечётный угол `15 -> 20` оставляет пять асимптотических нулей и
  не удовлетворяет условию Каллиаса;
- составная связность не меняет ранги внутренних носителей;
- Toeplitz boundary Тома V независимо имеет индексы `-15/+15`.

## Boundary at This Gate

Совпадение числа `15` очень сильное, но пока стабильное: Toeplitz-оператор
живёт на пространстве Харди, а Callias-кандидат — на пространстве дефекта.
Без общего KK-класса или явного intertwiner оно не доказывает
пространственную локализацию пятнадцати фермионных мод.

## Subsequent Result

[[version6-callias-toeplitz-index-comparison-gate]] построил явное
сравнение: clutching-функция хопфовой линии равна `z`, а после умножения
на `q0` она дословно совпадает с `V+` Real-Toeplitz символа. Граничный
`K`-мост закрыт; открытым остался вывод rank-two spin-cover носителя из
конечного родителя.

## Links

- [[version6-gauged-projective-spin-cover-parent-gate]]
- [[callias-fredholm-spin-cover-literature-2026]]
- [[version6-callias-toeplitz-index-comparison-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[version5-hopf-pair-odd-core-extension-gate]]
- [[version5-spin-cover-defect-sphere-bridge-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_composite_connection_callias_fredholm_gate.tex`
- `s2t/audits/s2t_v6_composite_connection_callias_fredholm_gate.py`
- `s2t/results/s2t_v6_composite_connection_callias_fredholm_gate_results.json`