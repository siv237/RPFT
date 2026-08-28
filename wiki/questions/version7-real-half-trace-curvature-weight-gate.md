# Version VII: происхождение половинного веса кривизны

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Положительная сумма рёберной и физической относительной Hodge-норм проходит
оба гессиана при `beta=1/2`, но равный вес `beta=1` проваливается.

## Search for Solution

Оба действия приведены к форме `1/2 Tr(m^2)`. Полное Real-удвоение умножает
каждый след на два, а один общий физический полуслед делит оба на два.
Относительное отношение поэтому остаётся `beta=1`.

## Expected Result

Гипотеза закрыта отрицательно. Равный вес даёт нулевую сигнатуру `(21,0,6)`,
а нужная `(7,0,20)` возникает только после дополнительной секторной половины.
Такая операция является свободным центральным весом. Следующий допустимый
источник различия — заранее представленная степень формы или клиффордов след.

## Links

- [[version7-derived-relative-involution-curvature-norm-gate]]
- [[version7-real-superconnection-common-trace-origin-gate]]
- [[superconnection-curvature-norm-normalization-literature-2026]]
- [[version7-clifford-form-degree-weight-origin-gate]]

## Source Notes

- `s2t/gates/version7_real_half_trace_curvature_weight_gate.tex`
- `s2t/audits/s2t_v7_real_half_trace_curvature_weight_gate.py`
- `s2t/results/s2t_v7_real_half_trace_curvature_weight_gate_results.json`