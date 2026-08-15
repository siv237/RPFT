# Split Defect Saddle Gate

> Status: working
> Research status: conditional fixed-background derivation; dynamical-radius no-go
> Type: question
> Updated: 2026-08-04

## Explicit Functional

On a degree-one wrapped copy of the unit carrier and a unit-period real form on its systolic core, consider

```text
S[X,a] = Vol(X) + (1/2) integral_gamma a wedge star a,
deg(X)=1,
integral_gamma a=1.
```

The volume form calibrates the degree-one wrapping, so the identity carrier saturates the lower bound `Vol(RP3)=pi^2`. Writing `a=f(s) ds` on a cycle of length `L=pi`, Cauchy--Schwarz gives

```text
integral f^2 ds >= 1/L,
```

with equality only for `f=1/L`. Therefore the unique cycle saddle is `a=ds/pi`, and

```text
S_on-shell = pi^2 + 1/(2pi).
```

Random Fourier perturbations confirm the exact positive quadratic remainder.

## Important No-Go

If the carrier radius is varied rather than frozen, the same action becomes

```text
S(R)=pi^2 R^3 + 1/(2pi R).
```

Its derivative at `R=1` is `29.4497`, not zero. Its actual stationary point is `R=0.27077`, so the two-term action does not select the unit carrier geometry.

## Verdict

The geometric split action has an explicit and stable constrained saddle on the already fixed unit carrier. This is a real mathematical upgrade over a bare numerical combination. The two-loop audit has separately rejected its interpretation as an ordinary gauge-running threshold. It is not yet a derivation from the full theory because the common unit normalization is not produced by a parent action and the action cannot stabilize the overall radius.

## Next Gate

Derive both terms from one S2T superconnection trace or identify an independently mandatory radius-stabilizing sector. Do not tune the cycle coefficient: hitting the reconstructed exponent exactly would require `kappa=1.22397` instead of the canonical value `1`.