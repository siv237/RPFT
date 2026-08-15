# Version III Gauge--Ghost and KK Completion Gate

> Status: specification gap isolated
> Date: 2026-08-10

## Result

The heat-kernel-normalized finite block contributes the fixed numerator
`40`. A stable massive abelian vector together with its Goldstone and ghost
completion contributes `3 c_A^2`, so the gauge completion is nonnegative
once a unitary broken branch is specified.

The current parent action does not yet select the physical gauge quotient,
the canonically normalized coupling, or the BV/BRST zero-mode prescription.
It therefore does not determine `c_A`.

## KK Obstruction

The factor module used in Version III is a zero-spectator projection, not a
full local field space on `RP3 x S1`. Consequently, the scalar, spinor,
coexact and ghost towers studied in Tome II cannot be assigned to the new
finite modes without deriving a full fluctuated product operator.

The honest ledger is

```text
B_full = (40 + 3 c_A^2 + c_sigma^2 + Delta N_KK)/(64 pi^2).
```

Only `40` is presently fixed. The sign of the regulated KK correction is
not determined.

## Milestone

This is narrower than the Tome II obstruction. The finite parent block,
its vacuum, kinetic normalization and positive finite Coleman--Weinberg
seed are now derived. The remaining task is a unique local lift into one
gauge-fixed product theory, not another search for numerical sector rules.

## Next Gate

Construct the complete fluctuated product spectral triple and BV complex,
then derive all scalar, vector, ghost and fermion Hessians and their common
finite-part prescription before testing `B_full > 0`.