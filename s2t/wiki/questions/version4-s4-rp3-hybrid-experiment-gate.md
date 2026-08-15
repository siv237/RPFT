# Version IV: S4/RP3 hybrid experiment

> Status: metric hybrid closed; discrete topological core survives
> Updated: 2026-08-11

## Problem

The original `K=RP3 x S1` had a useful exact ledger of volumes, systoles,
parity spectra and `Z2` holonomy. The new `S4` carrier is cleaner but should
be tested for whether it can inherit that structure through a separate
internal `RP3` sector.

## Search for solution

- Minimized scalar correlation-cell density on metric `RP3`.
- Compared the selected radius with the exact `b=2 sigma` values.
- Built the honest tensor-product density on `S4 x RP3`.
- Audited trivial and twisted scalar KK thresholds.
- Tested a sum over the two flat-character sectors.

## Separate RP3 result

The trivial scalar sector has a strict minimum at

```text
b/sigma = 1.99760832726935,
Vol/sigma^3 = 78.6739154398455,
systole/sigma = 6.27567164569920.
```

This is close to `b=2 sigma`, `Vol=8 pi^2 sigma^3` and
`systole=2 pi sigma`, but it is not exact. Rounding the minimum to two would
be a new numerical substitution.

## Product failure

For the honest seven-dimensional product,

```text
f_7 = -(log Z_S4 + log Z_RP3)/(v4 v3 r^4 s^3).
```

At fixed `S4` radius, `f_7 -> -infinity` as the `RP3` radius tends to zero.
The joint product therefore has no finite vacuum even though each separate
density has one.

## KK price

At the separate `RP3` minimum,

```text
m_KK(trivial)/Lambda_corr = 1.41591,
m_KK(twisted)/Lambda_corr = 0.86706.
```

Metric `RP3` is not a finite internal geometry at the correlation cutoff.
Summing both flat-character sectors changes the preferred radius and again
requires a spin/character measure absent from the current theory.

## Result

The hybrid options form a trilemma:

1. metric `RP3` retains the geometric pi-ledger but introduces KK towers and
   product instability;
2. a topological `Z2` sector avoids KK modes but retains only torsion,
   holonomy and linking data, not metric pi-values;
3. finite spectral truncation requires an arbitrary mode cutoff.

The best current hybrid is therefore `S4` spacetime plus a non-metric
discrete `Z2` topological core. The full exact baggage of `K` is not inherited
for free.

## Expected result

Construct a genuine finite or topological `Z2` sector whose measure fixes
its relative weight and test whether it contributes to two independent
normalization-sensitive observables without reintroducing KK modes.

## Compliance check

- Near-equalities are not promoted to exact identities.
- The tensor-product functional, not a manually separated sum, was tested.
- KK thresholds are recorded explicitly.
- Only the genuinely topological part of `RP3` is retained unconditionally.

## Links

- [[version4-correlation-cell-free-energy-density-gate]]
- [[version4-absolute-scale-eft-validity-gate]]
- [[version4-spin-sum-measure-gate]]
- [[version4-observed-reconstruction-roadmap]]

## Sources

- `version4_s4_rp3_hybrid_experiment_gate.tex`
- `s2t_v4_s4_rp3_hybrid_experiment.py`
- `s2t_v4_s4_rp3_hybrid_experiment_results.json`