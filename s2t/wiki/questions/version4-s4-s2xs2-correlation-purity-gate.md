# Version IV: S4 versus S2 x S2 correlation-purity gate

> Status: positive ordering, conditional selection
> Updated: 2026-08-11

## Problem

The post-`K` shortlist leaves round `S4` and equal-radius `S2 x S2` as the
two compact spin homogeneous positive-Einstein candidates without a
unit-volume shape modulus. Maximal symmetry favours `S4`, but an independent
operator criterion is required.

## Search for solution

- Fixed the four-volume of both backgrounds to one.
- Used the same scalar Gaussian operator `C_tau=exp(-tau Delta0)`.
- Normalized it to a density operator and compared Rényi-2 entropy
  `S2=2 log Z(tau)-log Z(2 tau)`.
- Derived the small- and large-`tau` signs analytically.
- Audited the middle profile with adaptive spectral cutoffs and log-sum-exp.

## Result

At small correlation time,

```text
Delta S2 = S2(S4)-S2(S2 x S2)
         = (16 pi^2/15) tau^2 + O(tau^3) > 0.
```

At large correlation time the first positive gaps are

```text
S4:       lambda1=20.52079728, degeneracy=5,
S2 x S2: lambda1=25.13274123, degeneracy=6,
```

so `S4` again has larger entropy. A 3001-point logarithmic grid on
`1e-5 <= tau <= 2` finds no crossing. The maximal difference is

```text
tau=0.1133942342,
Delta S2=0.1810734171.
```

Thus the normalized Gaussian state on `S4` retains greater effective mode
diversity and has lower purity across the audited profile.

## Expected result

Derive the sign of the TOE vacuum principle from the definition of the
correlation state. If the vacuum maximizes correlation entropy at fixed
volume, `S4` becomes the selected carrier. If the sign is opposite, the
ordering selects `S2 x S2` instead.

## Compliance check

- The same operator and unit-volume normalization were used for both
  candidates.
- No finite-sector multiplicity or fitted coefficient entered the test.
- Both asymptotic signs are analytic; the middle interval is numerical.
- The result is recorded as spectral ordering, not yet a dynamic vacuum
  theorem.

## Links

- [[version4-toe-native-s4-carrier-candidate-gate]]
- [[zero-prompt-toe-carrier-trace-2026-08-11]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `version4_s4_s2xs2_correlation_purity_gate.tex`
- `s2t_v4_s4_s2xs2_correlation_purity_gate.py`
- `s2t_v4_s4_s2xs2_correlation_purity_gate_results.json`