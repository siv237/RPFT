# Version IV: correlation-cell free-energy density gate

> Status: working
> Research status: conditional scale-ratio selection
> Type: question
> Updated: 2026-08-11

## Problem

Total Gibbs free energy decompactifies and the positive spectral action
collapses. A finite radius requires a constraint or intensive principle that
does not introduce a fitted relative coefficient.

## Search for solution

- Constructed the dimensionless Gibbs free energy per four-dimensional
  correlation cell:
  `f_cell=tau^3 F/V=-tau^2 log(Z)/V`.
- Varied the round `S4` radius through `r=a/sigma`.
- Derived the exact stationarity and Hessian formulas.
- Independently optimized equal-radius `S2 x S2`.
- Compared the two optimized densities rather than fixing a common volume.

## Stationarity

For `S4`,

```text
f_cell(r)=-log Z(r)/(v4 r^4),
<mu>/r^2=2 log Z
```

at a stationary point. The unique audited minimum is

```text
a/sigma = 1.35139219568654,
f_cell  = -0.00549336084715081,
Hessian = 0.0245770874529649.
```

The condition is equivalent to the vacuum equation of state `p=-epsilon`.

## Competitor audit

For equal-radius `S2 x S2`,

```text
b/sigma = 0.950165770265542,
f_cell  = -0.00447647528318466,
Hessian = 0.0440183779452763.
```

The optimized `S4` density is lower, so the spherical carrier remains
preferred after each topology chooses its own correlation-scale ratio.

## Result

The intensive completion selects

```text
M*=S4,
a*=1.35139219568654 sigma,
R sigma^2=6.57080279149.
```

This reopens the radius gate at the dimensionless level without an
additional relative weight.

## Expected result

Derive the absolute normalization of `sigma` from the corrected
gravitational sector and test it blindly. Until that is done, the result is
a correlation-length ratio, not a prediction in metres or GeV.

## Compliance check

- No observed radius or coupling entered the minimization.
- Both candidate scales were optimized independently.
- The radial Hessians are positive.
- Minimization per correlation cell is a new explicit completion, not a
  claim already present in primary TOE.

## Links

- [[version4-s4-radius-boundary-no-go]]
- [[version4-spectral-gibbs-equivalence-gate]]
- [[version4-gibbs-free-energy-carrier-gate]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/gates/version4_correlation_cell_free_energy_density_gate.tex`
- `s2t/audits/s2t_v4_correlation_cell_free_energy_density_gate.py`
- `s2t/results/s2t_v4_correlation_cell_free_energy_density_gate_results.json`