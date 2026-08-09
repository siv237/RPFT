# Projector Hilbert Rescue Sprint

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Can the remaining coexact-projector and Hilbert/basis transport blocks explain, cancel, or properly normalize the C6 obstruction in the same quotient-normalized scheme?

## Plain-Language Summary

The connection and principal blocks have now been measured and do not cancel. The next useful move is not to invent a new sector, but to check whether the physical doorway and the measuring ruler move. In formulas: the coexact projector `Pi_coex` and the Hilbert inner product/basis both depend on the metric. If they move at second order, fixed-basis matrix traces may be misleading.

## Why This Sprint Exists

Current C6 status says:

```text
C_principal_plus_connection[1,1] != 0
```

for all `55` raw symmetric strain pairs. Therefore any rescue must come from blocks not yet evaluated in the same scheme:

- Ricci/curvature;
- coexact-projector variation;
- Hilbert/basis transport;
- local/finite compensation.

The [[finite-gap-source-audit]] ranks projector and Hilbert/basis as the best live normalization components for the small `N_need-10` gap.

## Projector Block

Known skeleton from `s2t_c6_l21_delta2_second_projector_formula_results.json`:

```text
Pi_coex = I - d Delta_0^{-1} delta
L_phys = Pi_coex Delta_1 Pi_coex
```

The explicit second-projector formula gate is now tracked in [[delta2-projector-expansion-gate]]. In short, with `G=Delta_0^{-1}_{det'}` and `D=delta_g`,

```text
Pi_AB = -d[ G_AB D + G_A D_B + G_B D_A + G D_AB ],
G_AB = G L_A G L_B G + G L_B G L_A G - G L_AB G.
```

The ambient-path formulas for `L_A`, `L_AB`, `D_A`, and `D_AB` are tracked in [[scalar-codifferential-ambient-gate]].
Their ambient substitution into `S_A`, `a_A`, `tau_A`, `w_AB`, and `p_AB` is tracked in [[projector-ambient-substitution-gate]].

Second-order reduced-operator terms include:

```text
Pi delta2Delta_1 Pi
(delta2 Pi) Delta_1 Pi + Pi Delta_1 (delta2 Pi)
(delta Pi_A) Delta_1 (delta Pi_B) + A<->B
(delta Pi_A)(delta_B Delta_1)Pi + A<->B
Pi(delta_A Delta_1)(delta Pi_B) + A<->B
```

### Projector Pass/Fail Gates

| Gate | Pass Means | Fail Means |
|---|---|---|
| Expand `delta2 Pi_coex` | projector can be inserted into C6 tables | projector remains only a label |
| Fix scalar `det'` inverse | zero-mode/gauge convention is compatible | same-scheme proof blocked |
| Check self-adjointness | reduced operator is determinant-safe | finite traces are not trustworthy |
| Compute `C_proj[1,1]` | direct comparison with connection/principal possible | C6 cannot close as theorem |
| Archive `C_proj[1,3]` | projection leakage is controlled | off-diagonal obstruction remains opaque |

## Hilbert/Basis Block

Known skeleton from `s2t_c6_l21_delta2_second_hilbert_formula_results.json`:

```text
<alpha,beta>_g = integral g^{ab} alpha_a beta_b dvol_g
```

The block contains:

- second variation of the one-form inner product;
- second variation of volume form;
- basis transport / Gram-Schmidt corrections;
- degenerate-shell rotations;
- self-adjoint representation of the reduced operator in the varied Hilbert metric.

### Hilbert/Basis Pass/Fail Gates

| Gate | Pass Means | Fail Means |
|---|---|---|
| Choose basis transport | the moving ruler is fixed before numbers | any finite correction is gauge-like |
| Compute Gram correction | fixed-basis trace can be repaired | current C11 traces remain incomplete |
| Check shell rotations | degenerate `n=1` and `n=3` bases are consistent | rank statements may be basis artifacts |
| Verify self-adjoint form | determinant trace is legal | trace comparison is not scheme-safe |
| Compute diagonal contribution | can test gap/cancellation quantitatively | no C6 theorem upgrade |

## Direct Trace Priority

From `s2t_c6_l21_delta2_finite_block_spec_results.json`, the determinant trace term

```text
Tr(Delta^{-1} delta2 Delta)
```

needs diagonal shell blocks first:

| Block | Shape Per Pair | Weight | Role |
|---|---:|---:|---|
| `C_delta2[1,1]` | `6 x 6` | `1/4` | primary diagonal trace |
| `C_delta2[3,3]` | `30 x 30` | `1/16` | primary diagonal trace |
| `C_delta2[1,3]` | `6 x 30` | archive | self-adjointness / leakage check |
| `C_delta2[3,1]` | `30 x 6` | archive | Hermitian partner |

## Sprint Decision Rule

This sprint succeeds only if it produces one of these:

1. a finite projector/Hilbert contribution that cancels or normalizes the existing principal+connection obstruction without a fitted coefficient;
2. a proof that projector/Hilbert terms are local/subtracted/zero in the fixed scheme;
3. a clear downgrade trigger showing `pi^-4` cannot be a mature determinant theorem in the current route.

It does not succeed by adding more labels, analogies, or nearby integers.

## Recommended Next Micro-Step

Start with the projector block:

```text
expand delta2_AB Pi_coex on the locked ambient path
```

because the projector decides what the physical coexact sector is. Then use the Hilbert/basis block to put the resulting operator in the correct moving inner product.

## Links

- [[finite-gap-source-audit]] — why projector and Hilbert/basis are the best live rescue components.
- [[delta2-projector-expansion-gate]] — explicit `delta2 Pi_coex` formula gate.
- [[scalar-codifferential-ambient-gate]] — explicit scalar-Laplacian/codifferential slots used by the projector gate.
- [[projector-ambient-substitution-gate]] — substitution of those slots into ambient low-shell objects.
- [[projector-green-chain-reduction-gate]] — next reduction step for scalar Green chains and shell leakage.
- [[finite-spectral-residue-gap]] — parent gap question.
- [[coexact-tower-delta]] — coexact tower and absorption route.
- [[s2t-closure-roadmap]] — current C6/C11 status.
- [[current-status-and-next-vectors]] — global next vectors.

## Source Notes

- Source paths: `s2t_c6_l21_delta2_second_projector_formula_results.json`, `s2t_c6_l21_delta2_second_hilbert_formula_results.json`, `s2t_c6_l21_delta2_finite_block_spec_results.json`, `s2t_c6_l21_delta2_principal_plus_connection_C11_results.json`, `wiki/questions/finite-gap-source-audit.md`.