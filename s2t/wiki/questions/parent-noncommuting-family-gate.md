# Parent Noncommuting Family Gate

## Canonical Commutator

The existing translation and shear operators define the coefficient-free
Hermitian candidate `K=(i/2)[T_RP3,S]`. It has spectrum `(-1,0,1)` and rank two.
However, its translation and full affine orbit averages vanish exactly, so it
is a symmetry-breaking spurion rather than an invariant action term.

`K tensor P_SU5` is allowed only after the SU5 holonomy has reduced the group to
the SM centralizer. The unique matrix trace normalizes this term if written but
does not fix its coefficient relative to the other invariant terms. A single
`K` also mixes only one family plane.

## Projective Flux

The nontrivial Z2 cocycle gives magnetic translations satisfying
`U^2=V^2=I` and `UV=-VU`. This is an exact coefficient-free source of
noncommutativity.

It cannot act on the three-family triplet: anticommuting invertible operators
have no odd-dimensional representation. In the explicit four-state model the
flux mixes the uniform reference state with the triplet. Compressing back to
three dimensions breaks the projective relation and leaves a reducible `1+2`
algebra.

## Fork

- Preserve the `1+3` generation mechanism and seek a richer discrete
  incidence/Dirac operator fixing at least two spurions.
- Or retain projective flux and rebuild generation counting on an
  even-dimensional carrier.

These mechanisms cannot presently be combined without a new scale.

## Evidence

- `s2t_parent_noncommuting_family_insertion_audit.py`
- `s2t_parent_noncommuting_family_insertion_results.json`
- `s2t_projective_family_flux_audit.py`
- `s2t_projective_family_flux_results.json`
- `parent_noncommuting_family_gate.tex`