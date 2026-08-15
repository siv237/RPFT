# Version IV: TOE-native S4 carrier candidate gate

> Status: working
> Research status: conditional candidate
> Type: question
> Updated: 2026-08-11

## Problem

The fixed carrier `K=RP3 x S1` is exhausted as a minimal vacuum theory, and
the source audit shows that it was not derived by the primary TOE
correlation operator. A replacement must avoid another fitted geometric
score and must keep spacetime, finite Standard Model geometry and flavour
data conceptually separate.

## Search for solution

- Replaced a weighted score by a lexicographic structural gate.
- Compared `S4`, equal-radius `S2 x S2`, `S3 x S1`, `RP3 x S1`, `T4`, K3
  and `CP2`.
- Required compact connected spin dimension four, homogeneous positive
  Einstein geometry, no unit-volume shape modulus, then maximal continuous
  isometry.
- Rebuilt the parent as an almost-commutative geometry over the surviving
  spacetime candidate.

## Result

Only round `S4` and equal-radius `S2 x S2` survive the first three filters.
The continuous isometry dimensions are respectively `10` and `6`; round
`S4` saturates the four-dimensional upper bound.

The proposed parent is

```text
A = C-infinity(S4) tensor (C + H + M3(C)),
H = L2(S4,S) tensor H_F,
D = D_S4 tensor 1 + gamma5 tensor D_F,
Chat = exp(-sigma^2 D^2).
```

This removes the free circle/sphere radius ratio, the periodic/AP spin
branch choice and the non-Einstein product background. Flavour hierarchy
and CP are no longer assigned to spacetime spin structure.

## Expected result

The next preregistered calculation compares round `S4` with equal-radius
`S2 x S2` using one normalized Gaussian-correlation functional at equal
volume, then tests the second variation and absolute-radius gate.

## Compliance check

- No weighted score or fitted coefficient was introduced.
- `S4` is recorded as a minimal conditional candidate, not a derived TOE
  vacuum.
- Absolute scale remains open.
- Global uniqueness beyond the declared comparison class is not claimed.

## Links

- [[zero-prompt-toe-carrier-trace-2026-08-11]]
- [[version4-spin-branch-mass-stationarity-gate]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex`
- `s2t/results/s2t_v4_toe_native_s4_carrier_candidate_gate_results.json`