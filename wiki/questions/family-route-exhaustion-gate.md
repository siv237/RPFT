# Family Route Exhaustion Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Scope

This gate exhausts two minimal continuations of the declared four-state menu:
all affine incidence extensions inside `AGL(2,2)` and all flux-only projective
carriers of dimension `2m`.

## Affine Incidence Scan

The current translation-plus-shear subgroup has order eight and leaves a
reducible `1+2` triplet algebra. There are sixteen affine elements outside it:

- four transposition-type candidates; all generate full `M3`;
- eight three-cycle candidates; all generate full `M3`;
- four four-cycle candidates; all remain reducible.

Thus twelve single incidence operators can support full family mixing. None is
selected by the current geometry. Averaging a candidate over the geometric
order-eight group restores the `1+2` algebra.

## Projective Carrier Scan

The nontrivial flux algebra is `M2 tensor I_m`, with commutant
`I2 tensor M_m`. In four dimensions every flux-only eigenvalue is doubly
degenerate, so spectral projectors have ranks `0,2,4`, never `1` or `3`.

Using a six-dimensional carrier with multiplicity three merely relocates all
family masses and mixing into an unconstrained `M3` commutant. The flux does
not select them.

## Cohomology and Metric Selector

The mod-two cohomology ring has only the identity and `a -> a+b, b -> b` as
linear ring automorphisms. Its three nonzero classes therefore retain a `1+2`
orbit split.

The square indicator, free-S1 component and product-metric lengths distinguish
all three labels, but their operators are simultaneously diagonal. Intrinsic
topology can label generations and support hierarchy; it still predicts
identity mixing. A localized systolic defect adds the missing incidence datum
only by choosing a noncanonical S1 point or phase.

## Surviving Condition

The only live minimal route is a prior boundary, discrete-Dirac, or geometric
principle selecting one of the twelve outside-D8 incidence directions and
fixing its sector map and relative normalization before CKM data are used.

## Evidence

- `s2t/audits/s2t_family_affine_incidence_exhaustive_audit.py`
- `s2t/results/s2t_family_affine_incidence_exhaustive_results.json`
- `s2t/audits/s2t_even_projective_carrier_exhaustive_audit.py`
- `s2t/results/s2t_even_projective_carrier_exhaustive_results.json`
- `s2t/audits/s2t_topological_family_selector_audit.py`
- `s2t/results/s2t_topological_family_selector_results.json`
- `s2t/gates/family_route_exhaustion_gate.tex`