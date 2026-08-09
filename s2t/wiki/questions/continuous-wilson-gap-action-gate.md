# Continuous Wilson Gap-Action Gate

## Result

The continuous `SO3` Wilson class contains eight axes that simultaneously
produce full family `M3` and exact tensor response `H=pi^4`.

The required angle satisfies

`11 c^2-52 c-49=0`, `c=(26-9 sqrt(15))/11`.

## Stable Spectral Saddle

Define

`V_gap(c)=(8/3)(3/(1-c)+log(1-c))-(44/45)c`.

Then `V_gap'(c)=R(c)-1`, where

`R(c)=1/45+8(2+c)/(3(1-c)^2)`.

At the exact angle, `V_gap''=1.901648596...>0`. The solution is therefore a
stable local minimum of an explicit spectral primitive, not merely an
isolated numerical point.

## Axis Reduction

Applying the existing factor Laplacian to the eight joint axes reduces them
to two transposition axes for all three previously declared kernels: inverse
length, inverse square and tunneling.

## Remaining Gates

- Derive unit tree stiffness rather than assuming `kappa=1`.
- Derive the resolvent-plus-log potential from local BV/BRST field content.
- Derive the factor-axis coupling from the same action.
- Check whether the remaining two axes are symmetry-equivalent vacua.
- Derive source normalization.

## Evidence

- `s2t_continuous_wilson_gap_action_audit.py`
- `s2t_continuous_wilson_gap_action_results.json`
- `continuous_wilson_gap_action_gate.tex`