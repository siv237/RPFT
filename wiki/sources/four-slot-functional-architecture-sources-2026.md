# Источники архитектуры four-slot functional

> Status: working
> Type: source
> Updated: 2026-08-31

## Summary

Узел использует общий carrier предыдущего гейта и стандартные точные факты
о минимумах quartic polynomial, вогнутых функциях на симплексе и boundary
selection на отрезке. Конкретные коэффициенты вводятся только как witness
архитектуры и не считаются физически выведенными.

## Key Points

- Quartic completion обеспечивает boundedness и положительный Hessian.
- Вогнутая endpoint-часть минимизируется в вершине симплекса.
- Вогнутая transport-часть выбирает одну из двух границ.
- Четыре coefficient packages являются следующим parent-origin bottleneck.

## Links

- [[version9-four-slot-common-parent-functional-architecture-gate]]
- [[version9-four-slot-common-carrier-architecture-gate]]
- [[tome9-opening-contract]]

## Source Notes

- `s2t/gates/version9_four_slot_common_parent_functional_architecture_gate.tex`
- `s2t/results/s2t_v9_four_slot_common_parent_functional_architecture_gate_results.json`