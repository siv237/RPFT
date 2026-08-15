# Finite Threshold Sign Cone

> Status: working
> Research status: negative for the minimal `XY/H3/Sigma8/Sigma3` basis
> Type: question
> Updated: 2026-08-04

## Corrected Target

Starting from the alpha-anchored gauge-only two-loop SM result, use the measured `M_W` with frozen `v_S2T`, preserve `alpha_em`, and use measured `alpha_s`. The required finite inverse-coupling shift is

```text
Delta alpha^-1_(Y,2,3)=(+0.368015,-0.368015,-2.459153)
                      proportional to (+1,-1,-6.6822).
```

Even this target cannot close both weak masses by gauge couplings alone: the resulting `M_Z=90.6969 GeV` remains low by `0.54%`.

## Threshold Cone

For `x_J=-log(M_J/Lambda)>=0`, the declared extended SU(5)-like basis has columns

```text
XY:     (22,12,21)/(12pi),
H3:     (2/5,0,-1)/(12pi),
Sigma8: (0,0,-1/2)/(12pi),
Sigma3: (0,-1/3,0)/(12pi).
```

The unrestricted nonnegative cone contains the target, but its least extreme exact solution requires

```text
x_XY=0,
x_H3=34.68,
x_Sigma8=116.05,
x_Sigma3=41.62.
```

These masses lie far below `M_Z`. Requiring every threshold mass to stay in the physical interval `M_Z <= M <= Lambda_S2T`, corresponding to `x<=29.92`, makes the exact system infeasible.

## Best Physical Approximation

The constrained least-squares solution saturates `H3`, `Sigma8` and `Sigma3` at the lower endpoint and still leaves `50.7%` of the target vector unresolved in relative L2 norm. Even allowing masses on both sides of `Lambda` requires `max |log(M/Lambda)|=56.30`, nearly twice the entire available RG interval.

## Verdict

The minimal logarithmic finite-threshold basis is algebraically capable but physically incapable of repairing EW and QCD simultaneously. The gauge branch now requires genuinely nonlogarithmic finite matching with independently fixed coefficients. Otherwise it should be frozen in favor of sectors with stronger independent evidence.