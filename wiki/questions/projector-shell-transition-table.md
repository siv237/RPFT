# Projector Shell Transition Table

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Which scalar `RP^3` even shells can be reached by the projector Green-chain operators `L_A` and `L_AB`?

## Plain-Language Summary

This page is the first leakage map for the projector Green chains. It does not compute matrix coefficients. It answers a simpler but decisive question: if a scalar mode starts in shell `ell`, which other scalar shells can the ambient-strain operators send it to? The answer shows that higher shells are generically allowed unless an additional same-scheme cancellation, locality argument, or representation-specific vanishing is proven.

## Inputs

From [[projector-ambient-substitution-gate]],

```text
L_A f = 2 S_A^{ij} nabla_i nabla_j f - 6 a_A^k nabla_k f,
L_AB f = -p_AB^{ij} Hess_ij(f) + b_AB^k nabla_k f.
```

The ambient objects have scalar/tensor degree content:

| Object | Expected Scalar Degree Content | Reason |
|---|---|---|
| `A` / `q_A=<x,Ax>` | `0 + 2` | `Sym^2(R4)=1+9` on `S^3/RP^3` |
| `a_A=(Ax)^T` | degree-2-derived vector | gradient of `q_A` up to factor |
| `S_A=P_TAP_T` | degree `0+2` tensor coefficient | tangent projection of ambient symmetric tensor |
| `p_AB` | degrees `0+2+4` generically | quadratic in `A,B` minus mixed metric term |
| `w_AB`, `b_AB` | degrees `0+2+4` generically | built from `AB+BA`, `A_T a_B`, `B_T a_A` |

## Selection Rules

For scalar harmonics on `S^3`, multiplying/coupling by a degree-`d` coefficient can connect

```text
ell -> ell-d, ell-d+2, ..., ell+d
```

with parity preserved. Since `RP^3` keeps only even scalar `ell`, all transitions below stay in the even sector.

### First Variation `L_A`

`L_A` has degree `0+2` coefficients and two/one derivatives. Derivatives do not change the parity class of the representation; the degree-2 coefficient gives the main shell spread.

Expected transition window:

```text
L_A: ell -> ell-2, ell, ell+2
```

with negative shells omitted.

| Input `ell` | Possible Output Shells | Comment |
|---:|---|---|
| `0` | `0,2` | zero mode is not inverted by `G`, but deformation trace can feed formulas outside `G` bookkeeping |
| `2` | `0,2,4` | first nonzero Green shell can leak to `ell=4` |
| `4` | `2,4,6` | higher shells couple back down and upward |
| `6` | `4,6,8` | no natural finite closure at `ell=2` |
| `8` | `6,8,10` | tower continues |

### Mixed Second Variation `L_AB`

`L_AB` contains `p_AB` and `b_AB`, which are generically quadratic in the ambient strains. Their scalar degree content can include `0+2+4`.

Expected transition window:

```text
L_AB: ell -> ell-4, ell-2, ell, ell+2, ell+4
```

with negative shells omitted.

| Input `ell` | Possible Output Shells | Comment |
|---:|---|---|
| `0` | `0,2,4` | mixed second variation can create `ell=4` even from trace-like input |
| `2` | `0,2,4,6` | first nonzero shell can leak to `ell=4,6` |
| `4` | `0,2,4,6,8` | higher shell mixing is generic |
| `6` | `2,4,6,8,10` | tower continues |
| `8` | `4,6,8,10,12` | no finite rank-10 closure by selection alone |

## Consequence For Green Chains

The Green chains contain repeated insertions:

```text
G L_A G,
G L_A G L_B G,
G L_AB G.
```

Since `G` sums over nonzero even shells `ell=2,4,6,...`, the selection rules imply:

- `G L_A G` can connect `ell=2` to `ell=4`.
- `G L_A G L_B G` can reach at least `ell=6` from `ell=2` through two degree-2 insertions.
- `G L_AB G` can reach `ell=4` or `ell=6` directly from `ell=2` if the degree-4 component is nonzero.

Therefore the projector Green-chain route does **not** close to the `ell=0,2` rank-10 window by representation selection alone.

## Pass/Fail Result

| Test | Result | Meaning |
|---|---|---|
| Even parity preservation | pass | `RP^3` quotient keeps the calculation inside even scalar shells |
| Natural `ell<=2` closure | fail/generic | `L_A` and especially `L_AB` can reach higher even shells |
| Manual rank-10 cutoff | forbidden | would assume the conclusion |
| Need locality/subtraction proof | yes | higher-shell finite parts must be removed by a same-scheme rule or retained |
| Need explicit Green-chain moments | yes | coefficients may vanish in special contractions, but this must be computed |

## Plain-Language Verdict

The projector does not automatically stay in the small `1+9` box. The door can swing into higher floors. If C6 is rescued, it must be because those higher-floor contributions are local, subtracted, compensated, or vanish after explicit quotient moments — not because representation theory alone keeps them out.

The explicit nonzero `ell=4` witness is tracked in [[projector-higher-shell-witness]].

## Next Computation

Compute the first nontrivial coefficient tests:

```text
<ell=4 | L_A | ell=2>,
<ell=4 | L_AB | ell=0 or 2>,
<ell=6 | L_A G L_B | ell=2>.
```

If any of these are generically nonzero in the relevant contractions, the projector Green-chain contribution must include higher-shell sums or a same-scheme subtraction theorem.

## Links

- [[projector-green-chain-reduction-gate]] — parent Green-chain protocol.
- [[projector-higher-shell-witness]] — explicit `ell=4` leakage witness.
- [[projector-coefficient-test-protocol]] — concrete coefficient tests for leakage survival.
- [[projector-ambient-substitution-gate]] — ambient formulas for `L_A` and `L_AB`.
- [[delta2-projector-expansion-gate]] — projector formula containing the Green chains.
- [[projector-hilbert-rescue-sprint]] — computation-facing sprint.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `s2t/results/s2t_integer10_origin_results.json`, `s2t/results/s2t_determinant_casmix_results.json`, `s2t/results/s2t_c6_l21_metric_strain_tensor_results.json`, `wiki/questions/projector-green-chain-reduction-gate.md`, `wiki/questions/projector-ambient-substitution-gate.md`.
- This page is a selection-rule audit. It does not evaluate Clebsch coefficients or quotient moment integrals.