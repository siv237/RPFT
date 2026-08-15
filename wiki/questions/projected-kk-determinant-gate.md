# Projected KK Determinant Gate

> Status: working
> Research status: negative for the common-spectrum determinant
> Type: question
> Updated: 2026-08-04

## Computation

For every positive `RP3` mass parameter use the finite shifted/periodic circle ratio

```text
L_beta(rho)=log[(cosh(2pi rho)-cos(2pi beta))/(cosh(2pi rho)-1)].
```

The projected partners from the anomaly-free phase table are

```text
quarter: Q + 2L + T_H = (5/3,10/3,3/2),
half:    E              = (4/3,0,0).
```

Thus every common mass shell has direction

```text
A(5/3,10/3,3/2)+B(4/3,0,0),  A,B>0.
```

After normalization to `SU(2)`, its color component is always `9/20=0.45`. The required scorecard ratio is `11.014`. No normalization, cutoff or positive sum over common shells can bridge this gap.

## Verdict

The finite holonomy determinant of the projected `Q,L,E,T_H` partners fails the gauge-correction direction. The anomaly-free projection is algebraically consistent but does not solve the threshold problem through its shifted partners alone.

## Former Intermediate-Running Route

The inverse residual is approximately aligned with the periodic `U+2D+H` beta vector and formerly suggested

```text
log(Lambda_S2T/M_split)=10.065,
M_split approximately 3.8e10 GeV
```

for the existing `T_EW`. The residual directional error remains below `5.6%`.

This interpretation is now closed. Correct downward running adds `+(Delta b/2pi) log(Lambda/M_split)` to inverse couplings, while the reconstructed repair required the opposite sign.

## Geometric Follow-Up

The parameter-free candidate `S_split=pi^2+1/(2pi)` still defines a conditional defect saddle, but it does not repair the gauge rows through ordinary running. See [[geometric-split-mass-action]] and [[two-loop-split-stress-test]].