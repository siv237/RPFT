# Pati-Salam Higher-Moment Saturation No-Go

> Status: working
> Type: question
> Updated: 2026-08-15

## Summary

Tests whether higher-moment polynomial spectral potentials can lift the
four threshold zero modes in the Pati-Salam composite construction.

## Result

For a rank-one radial variable `t = Tr(M_R^dag M_R)` and polynomial spectral
potential `V_rad(t) = -alpha t + P(t)`, radial stationarity fixes
`alpha = P'(t)`. The canonical graded-product quadratic auxiliary portal
gives portal `= 2n a_n t^(n-1) ||X||^2`, so the total coefficient is
`zeta(t) = 2P'(t) = 2 alpha`. The weak `phi`-Hessian after connector shift
is identically `-4 alpha + 2 zeta = 0`. Adding `D^6, D^8, ...` changes the
stationary radius but does not lift the four threshold zero modes.

## Links

- [[pati-salam-project-wide-rescue-archaeology]] — rescue archaeology context.
- [[version4-pati-salam-literature-reaudit]] — literature re-audit.

## Source Notes

- Gate: `s2t/gates/version4_pati_salam_higher_moment_saturation_no_go.tex`.
- Audit: `s2t/audits/s2t_v4_pati_salam_higher_moment_saturation_no_go.py`.
