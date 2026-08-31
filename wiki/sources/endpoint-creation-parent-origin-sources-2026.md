# Источники parent-origin endpoint creation-frame

> Status: working
> Type: source
> Updated: 2026-08-31

## Summary

Уникальный constant mode connected phase graph поставляет configuration
source. Теория стационарных состояний QMS и KMS detailed balance показывает,
почему outward-only jumps не определяют единственную equilibrium state и не
фиксируют forward rates без reverse sector и energy gaps.

## Key Points

- Source-projector есть normalized kernel projector фазового Laplacian.
- Physical channel commutant разбивается как `1+1+3` и имеет dimension `3`.
- Trace isotropy является представителем, а не следствием symmetry.
- Outward-only stationary corner равен `M5(C)`.

## Links

- [[version9-endpoint-finite-geometry-creation-operator-parent-origin-gate]]
- [[version9-endpoint-finite-geometry-creation-operator-architecture-gate]]
- [[endpoint-creation-operator-sources-2026]]

## Source Notes

- A. Frigerio, *Stationary States of Quantum Dynamical Semigroups*,
  Commun. Math. Phys. 63 (1978), 269--276.
- Z. Ding, B. Li, L. Lin, *Efficient quantum Gibbs samplers with
  Kubo--Martin--Schwinger detailed balance condition*, arXiv:2404.05998.
- `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex`
- `s2t/gates/version9_endpoint_finite_geometry_creation_operator_parent_origin_gate.tex`