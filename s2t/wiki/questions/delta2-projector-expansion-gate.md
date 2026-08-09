# Delta2 Projector Expansion Gate

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

What is the explicit second-order expansion of the moving coexact projector `Pi_coex` that must be inserted before C6 determinant traces are trusted?

## Plain-Language Summary

This page turns the “moving doorway” into a formula gate. The coexact projector depends on the metric because the codifferential and scalar inverse Laplacian depend on the metric. At second order, the doorway can move because the inverse scalar Laplacian moves twice, the codifferential moves twice, or the first movements cross. These pieces must be fixed before any projector contribution can be evaluated in `C_delta2[1,1]` or `C_delta2[3,3]`.

## Convention

Work on non-harmonic scalar modes with the true scalar zero mode removed by the same `det'` / gauge-volume convention used in the Maxwell--ghost determinant. Let

```text
D := delta_g                    codifferential on one-forms
L := Delta_0                    scalar Laplacian
G := L^{-1}_{det'}              scalar Green operator on zero-mean scalars
Pi := Pi_coex = I - d G D
```

For a metric strain direction `A`, write

```text
D_A  := delta_A D
L_A  := delta_A L
G_A  := delta_A G = - G L_A G
```

For the mixed second variation in directions `A,B`, write

```text
D_AB := delta2_AB D
L_AB := delta2_AB L
```

## Core Expansion

The required second variation of the inverse scalar Laplacian is

```text
G_AB = G L_A G L_B G + G L_B G L_A G - G L_AB G.
```

Therefore the mixed second variation of the projector is

```text
Pi_AB
  = - d [
        G_AB D
      + G_A D_B
      + G_B D_A
      + G D_AB
    ].
```

Equivalently, after substituting `G_A` and `G_AB`,

```text
Pi_AB
  = -d [
        (G L_A G L_B G + G L_B G L_A G - G L_AB G) D
      - G L_A G D_B
      - G L_B G D_A
      + G D_AB
    ].
```

All operators act on the one-form input through the trailing codifferential factors. Terms with trailing `D` vanish only on an initially coexact input before any side operator acts; they must not be dropped inside `Pi Delta Pi` expansions.

## Reduced Operator Insertion

For

```text
L_phys = Pi Delta_1 Pi,
```

the projector part of the mixed second variation includes

```text
Pi_AB Delta_1 Pi + Pi Delta_1 Pi_AB
+ Pi_A Delta_1 Pi_B + Pi_B Delta_1 Pi_A
+ Pi_A Delta_{1,B} Pi + Pi_B Delta_{1,A} Pi
+ Pi Delta_{1,A} Pi_B + Pi Delta_{1,B} Pi_A.
```

The pure `Pi Delta_{1,AB} Pi` piece belongs to the operator second-variation blocks already split into principal, connection, Ricci, and related terms; this page tracks only projector-side movement.

## Pass/Fail Gates

| Gate | Needed Object | Status |
|---|---|---|
| Scalar Green convention | `G=L^{-1}_{det'}` on zero-mean scalars | fixed schematically; must match gauge-volume convention |
| First scalar Laplacian variation | `L_A` on the locked ambient path | required from scalar metric-variation formulas |
| Second scalar Laplacian variation | `L_AB` on the locked ambient path | not yet expanded here |
| First codifferential variation | `D_A` | required from Hodge-star/volume variation |
| Second codifferential variation | `D_AB` | not yet expanded here |
| Projector insertion | `Pi_AB` and cross terms in `L_phys,AB` | formula gate written, not measured |
| Matrix output | `C_proj[1,1]`, `C_proj[3,3]`, archive `1<->3` | not yet evaluated |

## Immediate Next Calculation

The next formula-level calculation should expand `D_A`, `D_AB`, `L_A`, and `L_AB` for the locked ambient strain path. The formula slots are now tracked in [[scalar-codifferential-ambient-gate]]. The path is

```text
F_eps(x) = (I + eps A) x,
A = A^T,
```

then insert them into the `Pi_AB` formula above. Only after that can quotient integrals against the six `n=1` Killing states and the `n=3` coexact basis be trusted.

## Plain-Language Verdict

The doorway formula is now explicit. We know which hinges move. The remaining work is to compute how much each hinge moves on the locked ambient path and whether that movement changes the obstruction already seen in the principal-plus-connection block.

## Links

- [[projector-hilbert-rescue-sprint]] — sprint page that requested this expansion gate.
- [[scalar-codifferential-ambient-gate]] — formula slots for scalar Laplacian and codifferential variations.
- [[projector-ambient-substitution-gate]] — ambient substitution of those slots before scalar Green-chain reduction.
- [[finite-gap-source-audit]] — why projector motion is a live rescue component.
- [[coexact-tower-delta]] — coexact tower and absorption route.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `s2t_c6_l21_projector_variation_formula_results.json`, `s2t_c6_l21_delta2_second_projector_formula_results.json`, `s2t_c6_l21_laplacian_variation_results.json`, `wiki/questions/projector-hilbert-rescue-sprint.md`.
- This page is a formula gate. It does not claim a computed projector matrix or C6 closure.