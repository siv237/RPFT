# Version IV: full-field carrier counterterm gate

> Status: cross-topology determinant underdetermined before finite couplings
> Updated: 2026-08-11

## Problem

The negative-space audit identified the missing scalar-vector-ghost-Dirac
determinant on `S4` and `S2 x S2`. Before evaluating the spectra, this gate
tests whether their difference is renormalization-scheme independent.

## Unit-volume ledger

Equal volume cancels the cosmological term but not the other local invariants:

```text
Delta integral R       = 11.2969093903
Delta integral R^2     = 128 pi^2
Delta integral Ric^2   = 32 pi^2
Delta integral Riem^2  = -64 pi^2
Delta integral W^2     = -256 pi^2/3
Delta integral E4      = -64 pi^2
Delta Euler chi        = -2
```

Here `Delta` means `S4 - S2 x S2`.

## Obstruction

A finite counterterm `c_W integral W^2` shifts the carrier difference by
`-256 pi^2 c_W/3`. An Euler term shifts it by `-64 pi^2 c_E`. Either can
reverse any finite nonlocal determinant ordering until its coefficient is
fixed independently.

The Euler term is especially decisive: it does not alter local equations on
a fixed topology but directly changes relative weights between topologies.

## Consequence

Minimal subtraction can define a computational number, but not a physical
carrier selector. The parent theory must first fix Newton, Weyl-squared,
Euler/topology and scalar-curvature couplings.

The massive-vector ledger also requires an explicit Proca/Stueckelberg/Higgs
completion because none of the three listed physical scalars is its
Goldstone mode.

## Next step

After those coefficients are frozen, compute the nonlocal determinant
residual and the joint geometry Hessian. Before that, a large spectral sum
would merely encode a chosen topology measure.

The follow-up [[version4-gaussian-bare-spectral-topology-gate]] provides one
concrete conditional freezing mechanism: take the Gaussian spectral action
as the fundamental bare Wilsonian boundary at the cutoff.

## Sources

- `s2t/gates/version4_full_field_carrier_counterterm_gate.tex`
- `s2t/audits/s2t_v4_full_field_carrier_counterterm_gate.py`
- `s2t/results/s2t_v4_full_field_carrier_counterterm_gate_results.json`
- Vassilevich, *Heat kernel expansion: user's manual*, arXiv:hep-th/0306138