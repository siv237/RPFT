# Version IV: S4 absolute-radius boundary no-go

> Status: working
> Research status: closed negatively
> Type: question
> Updated: 2026-08-11

## Problem

Round `S4` is selected as a unit-volume shape candidate, but its absolute
radius was fixed by hand. The next gate releases the radius and tests both
functionals in the corrected two-stage operator architecture.

## Search for solution

- Wrote the exact scalar partition function on `S4_a`.
- Differentiated Gibbs free energy with respect to the radius.
- Differentiated a general positive decreasing spectral cutoff action.
- Checked the signs numerically for the Gaussian cutoff.
- Tested whether a simple sum can stabilize the radius without a new free
  relative normalization.

## Gibbs result

For dimensionless spherical eigenvalues `mu_l=l(l+3)`,

```text
dF/da = -2 <mu>/a^3 < 0.
```

Thus Gibbs free energy decreases monotonically and reaches its infimum only
at `a -> infinity`. Releasing the unit-volume constraint causes
decompactification.

## Spectral-action result

For a standard cutoff with `f'(y)<=0`,

```text
dS_f/da = -(2/a) sum_l d_l y_l f'(y_l) >= 0.
```

Minimizing the positive spectral action therefore drives `a -> 0`. The two
corrected readings of the same correlation operator pull toward opposite
boundaries and neither has a finite stationary radius.

## Combined-functional obstruction

A sum `alpha S_f + beta F` may have a stationary point, but its position is
set by `beta/alpha`. In the Gaussian case the condition is simply

```text
Z(a)=beta/(alpha tau).
```

Therefore an arbitrary relative weight merely encodes the desired radius.

## Expected result

Derive a volume, pressure, mean-energy or relative-weight constraint from a
single correlation-operator measure before using any physical scale. Without
such a derivation, the shape result must not be promoted to an absolute
vacuum prediction.

## Compliance check

- Both monotonicity signs are analytic.
- Numerical values reproduce the derivative identities.
- No Planck, cosmological or observed radius was used.
- The scale-setting route is frozen as closed until a derived constraint is
  supplied.

## Links

- [[version4-spectral-gibbs-equivalence-gate]]
- [[version4-gibbs-free-energy-carrier-gate]]
- [[version4-toe-native-s4-carrier-candidate-gate]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/gates/version4_s4_radius_boundary_no_go.tex`
- `s2t/audits/s2t_v4_s4_radius_boundary_no_go.py`
- `s2t/results/s2t_v4_s4_radius_boundary_no_go_results.json`