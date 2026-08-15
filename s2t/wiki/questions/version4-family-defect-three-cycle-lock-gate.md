# Version IV family-defect three-cycle lock gate

> Status: conditional positive
> Date: 2026-08-14

## Question

Can one coefficient-free boundary functional use the unit vortex winding to
select one of the eight orientation-preserving affine family candidates while
preserving the exact-one Majorana core kernel?

## Result

On the standard `S4` triplet, the cubic invariant
`I3(x)=sum_a x_a^3` obeys `|I3|<=1/sqrt(3)`. Equality occurs only at the
eight oriented tetrahedral vertices. The triplet character of an `SO(3)`
rotation is `1+2 cos(theta)` and vanishes uniquely at `theta=2 pi/3`.

The nonnegative functional

`V_nu=(r^2-1)^2+r^2(1+2 cos theta)^2+r^2(1-sqrt(3) nu I3)`

has exactly four minima for each unit winding `nu`. The two winding sectors
therefore reproduce all eight `S4` three-cycles. Every selected generator has
rank two and leaves one real Majorana family mode.

## Status boundary

This is an exact invariant and zero-locus theorem, not yet a parent-action
closure. The full functional must still be derived as the supertrace of one
graded boundary-superconnection curvature. The radial unit scale and the sign
map between vortex winding and the cubic invariant cannot be inserted by hand.

## Evidence

- `version4_family_defect_three_cycle_lock_gate.tex`
- `s2t_v4_family_defect_three_cycle_lock_gate.py`
- `s2t_v4_family_defect_three_cycle_lock_gate_results.json`

## Next gate

Construct the smallest graded bundle whose curvature square produces the
radial, zero-character and cubic-orientation terms with one trace
normalization.