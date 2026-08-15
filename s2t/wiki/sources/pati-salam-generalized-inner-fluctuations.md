# Pati-Salam Generalized Inner Fluctuations

> Status: mature
> Type: source
> Updated: 2026-08-13

## Summary

The generalized inner fluctuation without the first-order condition is
controlled by the normalized self-adjoint perturbation semigroup `Pert(A)`.
Its quadratic term is constrained by the same perturbation tensor as the
linear term; independent double commutators must not be counted as independent
physical fields.

## Key Points

- `D' = D + A_(1) + tilde(A_(1)) + A_(2)` with
  `A_(2) = sum_j hat(a_j)[A_(1),hat(b_j)]`.
- Valid perturbations satisfy `sum_j a_j b_j = 1` and self-adjointness in
  `A tensor A^op`.
- Unitary perturbations embed as `u tensor (u*)^op` and reproduce exact gauge
  conjugation.
- On the project's physical Standard-Model seed, the linear ranks are `8`
  for the bidoublet and `16` for the Delta field.
- Every sampled full Yukawa block has weak/color reshuffle rank `2` and a
  tilde-invariant weak subspace.
- Every sampled right-Majorana block has crossed reshuffle rank `1`, verifying
  `H_(aI,bJ) = k Delta_(aJ) Delta_(bI)`.

## Links

- [[pati-salam-generalized-inner-fluctuation-gate]] — project computation and verdict.
- [[version4-observed-reconstruction-roadmap]] — wider Tome IV reconstruction route.
- [[project-success-tree-2026-08-11]] — global evidence-status tree.

## Source Notes

- Chamseddine, Connes, van Suijlekom, arXiv:1304.7583.
- Chamseddine, Connes, van Suijlekom, arXiv:1304.8050.
- Chamseddine, Connes, van Suijlekom, arXiv:1507.08161.
- Project derivation: `version4_pati_salam_generalized_inner_fluctuation_gate.tex`.
- Reproduction code: `s2t_v4_pati_salam_generalized_inner_fluctuation.py`.