# Version VII: общий цепно-Hodge relative trace

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Объединить рёберный Hodge-момент и относительную полярную кривизну одним
следом и проверить, остаётся ли нормировка препятствием для селектора.

## Search for Solution

Построен общий самосопряжённый носитель размерности `54+42=96`:

```text
F_common = diag(M_E, i delta_N(Q²-Q0²)).
```

Единый незавешенный след даёт

```text
1/2 Tr_96(F_common²) = S_E + ||R_U||² + constant.
```

Real-удвоение имеет размерность `192`, а физический полуслед точно
восстанавливает исходное действие. Проверен также широкий набор
положительных относительных Hodge-весов.

## Expected Result

- Один общий след существует.
- В нуле получается `(7,0,20)` со щелью `18/5`.
- В вакууме получается `(0,0,27)` с минимумом `4.2355904499...`.
- Эти сигнатуры сохраняются при любом положительном весе linking-блока.
- Ручная нормировка больше не влияет на качественный селектор.
- Отношения масс остаются открыты: блоки `54` и `42` не связаны обменной
  симметрией, поэтому единственность Hodge-метрики не доказана.

## Links

- [[version7-linking-chain-degree-two-curvature-quotient-gate]]
- [[version7-bicomplex-total-degree-hodge-metric-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[polar-transfer-linking-expectation-literature-2026]]

## Source Notes

- `s2t/gates/version7_common_chain_number_hodge_relative_trace_gate.tex`
- `s2t/audits/s2t_v7_common_chain_number_hodge_relative_trace_gate.py`
- `s2t/results/s2t_v7_common_chain_number_hodge_relative_trace_gate_results.json`