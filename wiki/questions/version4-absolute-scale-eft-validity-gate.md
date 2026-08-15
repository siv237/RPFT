# Version IV: absolute-scale EFT-validity gate

> Status: working
> Research status: absolute matching closed as uncontrolled
> Type: question
> Updated: 2026-08-11

## Problem

The correlation-cell gate fixes `a/sigma`, but an absolute prediction still
requires normalization of `sigma`. Primary TOE relates the gravitational
coupling to the spectral moment `f2` and cutoff `Lambda=1/sigma`.

## Search for solution

- Used the primary matching
  `1/(8 pi G)=f2 Lambda^2/(96 pi^2)`.
- Evaluated the Gaussian profile with `f2=1`.
- Converted the selected radius to Planck units.
- Tested the large-cutoff conditions required by the local
  Seeley-DeWitt expansion.
- Quantified the hierarchy needed for a separate EFT cutoff.

## Formal absolute values

For `f(u)=exp(-u)`,

```text
sigma/l_P = 0.162867503967640,
a/l_P     = 0.220097873792816,
R l_P^2   = 247.713429335233.
```

These numbers follow algebraically from the stated gravitational matching.

## Self-consistency failure

The same selected vacuum has

```text
a Lambda       = 1.35139219568654,
R/Lambda^2     = 6.57080279149122,
sqrt(R)/Lambda = 2.56335771820696.
```

The local spectral expansion requires `a Lambda >> 1` and
`R/Lambda^2 << 1`. Both fail. This obstruction is independent of `f2`
because `R/Lambda^2=R sigma^2` is already fixed by the correlation-cell
minimum.

## Result

The formal sub-Planck radius is not a controlled physical prediction. The
dimensionless ratio `a/sigma` survives, while absolute matching through the
local `a2` coefficient is demoted to conditional status.

## Expected result

Either derive a hierarchy `Lambda_EFT sigma >> 1` from the theory or compute
the exact nonlocal spectral response without truncating to local
Seeley-DeWitt terms.

## Compliance check

- No measured value other than the definition of Planck units was fitted.
- The expansion parameter was tested on the resulting vacuum.
- Changing the cutoff moment cannot remove the obstruction.
- The invalid asymptotic matching is not used as a prediction.

## Links

- [[version4-correlation-cell-free-energy-density-gate]]
- [[version4-spectral-gibbs-equivalence-gate]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/17705966/TOE.pdf`, gravitational matching on page 2
- `s2t/gates/version4_absolute_scale_eft_validity_gate.tex`
- `s2t/audits/s2t_v4_absolute_scale_eft_validity_gate.py`
- `s2t/results/s2t_v4_absolute_scale_eft_validity_gate_results.json`