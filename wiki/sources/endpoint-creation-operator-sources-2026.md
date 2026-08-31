# Источники typed creation-оператора endpoint-геометрии

> Status: working
> Type: source
> Updated: 2026-08-31

## Summary

GKSL-форма позволяет задавать полностью положительную trace-preserving
creation dynamics через homogeneous jump frame. Ковариантность требует
суммировать charged creators по полному family multiplet, а не выбирать одну
ось вручную.

## Key Points

- Пять creators образуют два singlet и один triplet channel block.
- Равные triplet rates сохраняют family covariance.
- Реальная структура добавляет conjugate charged frame.
- Математическая creation architecture не выводит source и rates.

## Links

- [[version9-endpoint-finite-geometry-creation-operator-architecture-gate]]
- [[version9-endpoint-finite-geometry-configuration-space-admission-gate]]
- [[version8-linking-dirichlet-quantum-markov-semigroup-gate]]

## Source Notes

- G. Lindblad, *On the Generators of Quantum Dynamical Semigroups*,
  Commun. Math. Phys. 48 (1976), 119--130.
- R. Balu, *Covariant Ergodic Quantum Markov Semigroups via Systems of
  Imprimitivity*, arXiv:2102.09984.
- `s2t/gates/version9_endpoint_finite_geometry_creation_operator_architecture_gate.tex`