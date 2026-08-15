# Version IV Gibbs-Fisher Geometry Gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Summary

Derives the Gibbs-Fisher geometry and canonical radial measure for the
normalized heat-state family and compares carrier stiffness.

## Result

For the normalized heat-state family `p_n(r) = Z(r)^-1 d_n e^(-mu_n/r^2)`
with `x = log r`, the score is `partial_x log p_n = 2(mu_n - <mu>)/r^2`.
The Fisher metric and Jeffreys measure follow exactly:

```
I_x = 4 Var(mu) / r^4,   d mu_J = sqrt(I_x) dx
```

The stationary-point invariant stiffness is `H_F = r*^2 f''(r*)/I_x(r*)`.
Numerically `H_F(S^4) = 0.00588026822269...` and
`H_F(S^2 x S^2) = 0.00456099125215...`. Both minima are stable; `S^4` has
lower density and higher stiffness in its own statistical units.

## Links

- [[version4-gibbs-free-energy-carrier-gate]] — Gibbs free energy carrier.
- [[version4-spectral-gibbs-equivalence-gate]] — spectral/Gibbs equivalence.

## Source Notes

- Gate: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex`.
