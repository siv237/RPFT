# Tau Operator Projection Candidate

> Status: working
> Research status: constructive post-audit candidate
> Type: question
> Updated: 2026-08-04

## Gram Origin of the Seed

Define a direct-sum geometric tangent

```text
Xi_tau=(1_RP3,1_S1,P_perp n).
```

Its canonical squared norm is

```text
||Xi_tau||^2=Vol(RP3)+Vol(S1)+<sin^2 theta>_S2
            =pi^2+2pi+2/3.
```

Among primitive integer vectors with all three channels present, unit coefficients give the unique minimum up to eight independent sign choices. This supplies an exact operator-norm realization of the previously postulated `rho0`. The remaining issue is to derive why this direct-sum tangent is the charged-lepton transition vertex.

## Traceless Quotient Trace

The Tome states that the relative lepton projection retains a traceless component. The already existing first ambient strain space has

```text
Sym^2_0(R4), rank=9.
```

Combining this rank with the quotient volume ratio `Vol(RP3)/Vol(S3)=1/2` gives the zero-parameter candidate

```text
J_RP3=(1/2) Tr(P_traceless)=9/2.
```

Using the explicitly evaluated compact Bessel sum gives

```text
c_tau=(9/2)|I|/pi=0.27763622,
m_tau/m_mu=rho0-c_tau alpha,
m_tau=1776.90237 MeV.
```

This is `-0.31 sigma` relative to the current control, better than the exact `1/3` formula's `-0.78 sigma`.

## Warning

This candidate was recognized after the missing Jacobian was measured, so it is not blind evidence. More importantly, a quotient field normalized per mode may cancel the volume factor or divide by rank. The full ambient lepton loop must decide whether the correct trace is `J=1`, `1/2`, `9/2`, or another fixed value.

## Next Gate

Construct the charged-lepton superconnection and calculate its projected one-loop trace before looking again at the tau mass. Only that calculation can promote this candidate.

## Gate Result

The minimal normalized ambient calculation is negative. The even-sector quotient projector has trace `9`, not `9/2`, because the image term restores the second half. Canonical normalization of one collective rank-nine field then gives loop trace `1`; nine independent fields give `9`. See [[tau-ambient-trace-normalization]].