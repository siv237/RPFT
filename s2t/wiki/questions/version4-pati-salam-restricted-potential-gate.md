# Version IV: restricted Pati–Salam potential gate

> Status: current spectral field menu closed negatively
> Updated: 2026-08-13

## Representation correction

The general spectral field called `Sigma` transforms as
`(2_R,2_L,1+15_4)`, not `(1_R,1_L,1+15_4)`. A nonzero high-scale VEV
therefore breaks `SU(2)_L` and produces large left-right Dirac masses.

The required independent four-color breaking field is a genuine weak
singlet `(1_R,1_L,15_4)`. It is absent from the general fundamental branch
but present conditionally in the composite first-order branch.

## Hessian result

- Required Goldstones: `9`.
- Additional unwanted massless scalars: `6`.
- Total massless modes at the candidate point: at least `15`.
- Other scalar directions have negative mass squared.
- Verdict: local maximum, not a symmetry-breaking vacuum.

Adding two general quartic invariants of the existing breaking field does
not lift the degeneracy: the required leptoquark Goldstone and the unwanted
antisymmetric mode couple identically to the VEV.

## Corrected next step

The Casimir sensitivity clue survives, but the candidate must come from a
project finite-geometry construction that either derives the composite
`(1,1,15)` legitimately or generates connected diagonal fields and the
missing multi-trace invariants without unacceptable fermion masses.

## Sources

- Karimi Khozani, arXiv:1905.04533, especially equations (3), (6), and (7).
- `version4_pati_salam_restricted_potential_no_go.tex`
- `s2t_v4_pati_salam_restricted_potential_gate.py`