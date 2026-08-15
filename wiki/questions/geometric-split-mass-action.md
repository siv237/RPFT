# Geometric Split Mass Action

> Status: working
> Research status: geometric saddle retained; gauge interpretation rejected
> Type: question
> Updated: 2026-08-04

## Minimal Hypothesis

Use only invariants already present before the gauge repair:

```text
Vol(RP3)=pi^2,
||e1||^2=1/pi,
S_split=Vol(RP3)+(1/2)||e1||^2=pi^2+1/(2pi).
```

With `M_split=Lambda_S2T exp(-S_split)`, this gives

```text
S_split=10.0287593442,
M_split=3.9674e10 GeV.
```

The scale reconstructed from the gauge residuals was `3.8285e10 GeV`; the geometric candidate differs by `3.63%`.

## Invalidated Legacy Gauge Test

The earlier shortcut gave

```text
M_W     =80.2826 GeV   (-0.108%),
M_Z     =91.0795 GeV   (-0.119%),
sin2_OS =0.223035       (-0.078%),
alpha_s =0.120257       (+1.91%).
```

This apparent improvement is invalid. The shortcut used the opposite sign from downward RG running and changed the electromagnetic train anchor to `alpha_em^-1=132.2454`.

## Evidence Warning

The action was proposed after the required split exponent was known. More importantly, the two-loop stress test shows that ordinary `U+2D+H` running moves the inverse couplings in the wrong direction.

The even closer expression `pi^2+1/(2pi)+alpha*pi^2/2` is excluded from the evidence ledger because the `alpha/2` dressing coefficient was not independently present in the action.

## Next Gate

Retain the action only as a mathematical defect candidate. A gauge application now requires a separately derived finite threshold of the required negative sign; ordinary intermediate running is closed.

## 2026-08-04 Saddle Update

The action is now the exact minimum of a degree-one wrapped-carrier plus unit-period cycle functional on the frozen unit geometry. The cycle mode is uniquely `a=ds/pi` and has a positive Hessian. However, varying the common radius gives `S'(1) != 0`; the two-term action does not stabilize the unit carrier. See [[split-defect-saddle-gate]].

## 2026-08-04 Two-Loop Verdict

With the correct RG sign and the `alpha_em` anchor preserved, the split sector gives `M_W=82.0226 GeV`, `M_Z=92.0616 GeV`, `sin2=0.206203` and `alpha_s=0.080177`. The gauge interpretation is rejected. See [[two-loop-split-stress-test]].