# Version III Base-K Spectral Renormalization Gate

> Status: no parameter-free subtraction prescription found
> Date: 2026-08-10

## Zeta Ambiguity

Changing the determinant scale mu to exp(t) mu shifts the one-loop
potential by -2 B t chi^4. This is exactly absorbed by the finite quartic
counterterm lambda4 -> lambda4 + 2 B t.

The nonzero stationary point obeys

    log(chi^2/mu^2) = c - 1/2 - lambda4/B.

Thus even the dimensionless ratio chi/mu depends on the finite subtraction.

## Tested Prescriptions

- Zeta-minimal is a valid computational convention but is not selected by
  the spectrum.
- Choosing mu=1/R introduces no new dimensional input, but still leaves
  lambda4 and the global homothety scale open.
- A spectral cutoff can impose boundary conditions, but Lambda, f0 and f2
  become continuous model inputs.

## Verdict

The base-K path is a renormalizable four-dimensional effective parent
action with derived relative coefficients. Its absolute vacuum scale is a
renormalization datum, not yet a prediction.

## Next Choice

Either use one explicit scale-setting observable as training input and
reserve dimensionless quantities for blind tests, or derive a new symmetry,
fixed point or anomaly condition that fixes lambda4/B.