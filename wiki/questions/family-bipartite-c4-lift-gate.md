# Family Bipartite C4 Lift Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Minimal Graph Result

Keeping the labelled path `0-1-2`, requiring every edge to be odd under
`Gamma4=diag(1,-1,1,-1)`, and adding the smallest connected cycle gives one
minimal graph:

`0-1-2-3-0`.

It is a bipartite four-cycle with one gauge-invariant flux. Eliminating
coordinate vertex 3 produces an energy-dependent Schur complement and ties
the induced `0-2` chord to diagonal endpoint shifts.

## Canonical Triplet Obstruction

The canonical three-family space is not the coordinate span of vertices
`0,1,2`. It is the sum-zero subspace orthogonal to
`u=(1,1,1,1)/2`.

For the unit-edge flux adjacency,
`||(I-u u^dagger) A_C4(Phi) u||^2 = (1-cos(Phi))(3+cos(Phi))/4`.

The leakage vanishes only at trivial flux. At the conditionally inherited
Wilson flux its value is `0.9905101417`, so the affine singlet and triplet are
almost maximally mixed.

The vertex grading also fails to preserve the affine decomposition:
`||[Gamma4,u u^dagger]||_F^2=2`.

Finally, coordinate vector `e3` contains singlet probability `1/4` and
triplet probability `3/4`. Its Schur elimination is therefore not
elimination of the canonical affine singlet.

## Spectral Obstruction

The canonical four-mode factor Laplacian has spectrum
`(0,1/pi,2/pi,3/pi)`. The uniform singlet is the zero mode, not a derived
heavy state. A static Schur reduction at zero spectral parameter requires an
additional singlet mass operator and its normalization.

## Verdict

The square repairs coordinate bipartiteness but does not preserve the existing
`1+3` generation mechanism. The branch can reopen only by constructing a
larger graded space where singlet and triplet are invariant, or by abandoning
the affine `1+3` mechanism and independently deriving generation counting.

## Evidence

- `s2t/audits/s2t_family_bipartite_c4_lift_audit.py`
- `s2t/results/s2t_family_bipartite_c4_lift_results.json`
- `s2t/gates/family_bipartite_c4_lift_gate.tex`
