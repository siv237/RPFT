# Хиральный Fredholm-индекс и ориентация прямоугольного оператора

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Fredholm-индекс прямоугольного оператора различает число непарных нулевых
мод оператора и его сопряжения. Смена направления меняет знак индекса.
В градуированном описании тот же знак фиксирует, в каком хиральном блоке
остаётся непарная нулевая мода.

## Key Points

- `ind U=dim ker U-dim ker U*`.
- Для коизометрии `C11 -> C10` индекс равен `+1`.
- У сопряжённого направления индекс равен `-1`.
- Сам индекс не задаёт скорость; в проектном гейте он используется вместе
  с уже зарегистрированным знаком Hodge-функционала.

## Links

- [[version8-chain-orientation-index-defect-selector-gate]] — применение к
  цепному KMS-процессу.
- [[version7-chiral-hodge-index-instability-gate]] — непарная ядерная линия.
- [[version8-modular-bohr-parent-origin-gate]] — две исходные ориентации.

## Source Notes

- F. Gesztesy et al., “The index formula and the spectral shift function
  for relatively trace class perturbations”, arXiv:1004.1582.
- F. Finster, “The Chiral Index of the Fermionic Signature Operator”,
  arXiv:1404.6625.