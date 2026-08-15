# Projector Ambient Substitution Gate

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

After inserting the locked ambient strain formulas, what do the projector-gate operators `L_A`, `D_A`, `L_AB`, and `D_AB` reduce to?

## Plain-Language Summary

The previous gate named the four hinge operators of the moving coexact doorway. This page substitutes the ambient geometry into those operators. The important simplification is that first-order motion is controlled by three elementary objects:

```text
a_A = (Ax)^T,
S_A = P_T A P_T,
tau_A = Tr_T(S_A) = Tr(A) - <Ax,x>.
```

So the doorway is no longer an abstract Hodge object; at first order it is built from a tangent arrow `a_A`, a tangent endomorphism `S_A`, and a tangent trace `tau_A`.

## Ambient Identities

For the locked path

```text
F_eps(x) = (I + eps A)x,       A=A^T,
```

use

```text
q_A = <x,Ax>,
a_A = (Ax)^T = Ax - q_A x,
S_A = P_T A P_T,
tau_A = Tr_T(S_A) = Tr(A) - q_A.
```

The first metric and connection variations on the round `S^3/RP^3` background are

```text
h_A^{ij} = 2 S_A^{ij},
p_A^{ij} = partial_A g^{ij} = -2 S_A^{ij},
Gamma_A^k{}_{ij} = -2 g_ij a_A^k.
```

Therefore the contracted first connection vector is

```text
C_A^k = g^{ij} Gamma_A^k{}_{ij} = -6 a_A^k
```

because the tangent dimension is `3`.

## First Variation Slots

Substituting into [[scalar-codifferential-ambient-gate]] gives

```text
L_A f
  = 2 S_A^{ij} nabla_i nabla_j f
    - 6 a_A^k nabla_k f,

D_A alpha
  = 2 S_A^{ij} nabla_i alpha_j
    - 6 a_A^k alpha_k.
```

These are the first insertion-ready formulas for the projector gate.

## Mixed Second Variation Slots

The second connection audit gives

```text
Gamma_AB^k{}_{ij} = g_ij w_AB^k,

w_AB = -((AB+BA)x)^T + 4 A_T a_B + 4 B_T a_A.
```

The metric-cross audit gives the useful first-order contractions

```text
p_A^{ij} Gamma_B^k{}_{ij} = 4 tau_A a_B^k,
p_B^{ij} Gamma_A^k{}_{ij} = 4 tau_B a_A^k,
g^{ij} Gamma_AB^k{}_{ij} = 3 w_AB^k.
```

Therefore

```text
L_AB f
  = - p_AB^{ij} nabla_i nabla_j f
    + (4 tau_A a_B^k + 4 tau_B a_A^k + 3 w_AB^k) nabla_k f,

D_AB alpha
  = - p_AB^{ij} nabla_i alpha_j
    + (4 tau_A a_B^k + 4 tau_B a_A^k + 3 w_AB^k) alpha_k.
```

Here

```text
p_AB^{ij} = partial_A partial_B g^{ij}
          = h_A^i{}_m h_B^{mj} + h_B^i{}_m h_A^{mj} - k_AB^{ij},

k_AB(u,v)=<Au,Bv>+<Bu,Av>.
```

The remaining non-simplified second-order object is the principal tensor `p_AB`. It is already known from the principal second-symbol gate and must be kept unless a further ambient moment identity reduces it.

## Insertion Into `Pi_AB`

The [[delta2-projector-expansion-gate]] uses

```text
G_A  = -G L_A G,
G_AB = G L_A G L_B G + G L_B G L_A G - G L_AB G,
Pi_AB = -d[ G_AB D + G_A D_B + G_B D_A + G D_AB ].
```

After this substitution, all first-order projector pieces are expressed using `S_A` and `a_A`; all mixed second-order non-Green pieces use `p_AB` and the vector

```text
b_AB := 4 tau_A a_B + 4 tau_B a_A + 3 w_AB.
```

So

```text
L_AB f = -p_AB^{ij} Hess_ij(f) + b_AB^k nabla_k f,
D_AB alpha = -p_AB^{ij} nabla_i alpha_j + b_AB^k alpha_k.
```

## Pass/Fail Gates

| Gate | Status | Meaning |
|---|---|---|
| First slot substitution | pass | `L_A` and `D_A` reduced to `S_A`, `a_A` |
| Mixed connection contraction | pass | gradient/vector part reduced to `b_AB` |
| `p_AB` tensor handling | open | must be reduced through known ambient moments or retained in matrix integrals |
| Green insertion | not yet | `G L_A G`, `G L_AB G` not evaluated on scalar harmonics |
| Quotient matrix output | not yet | no `C_proj` table computed |

## Immediate Next Calculation

Reduce the scalar Green chains on the `RP^3` scalar even shells:

```text
G L_A G,
G L_A G L_B G,
G L_AB G,
```

using the `ell=0,2,...` scalar spectrum and the `n=1/n=3` one-form bases. The reduction protocol is now tracked in [[projector-green-chain-reduction-gate]]. This is where the projector gate becomes a finite moment problem rather than a formal operator list.

## Plain-Language Verdict

The projector hinge formulas now use the same simple ambient objects as the connection block. This is real narrowing: the next obstacle is no longer tensor notation, but scalar Green-chain reduction and quotient integrals.

## Links

- [[scalar-codifferential-ambient-gate]] — parent formula slots before substitution.
- [[delta2-projector-expansion-gate]] — `Pi_AB` formula using these slots.
- [[projector-green-chain-reduction-gate]] — scalar spectral reduction protocol for the resulting Green chains.
- [[projector-shell-transition-table]] — selection-rule table showing generic higher-shell leakage.
- [[projector-hilbert-rescue-sprint]] — computation-facing sprint.
- [[finite-gap-source-audit]] — why projector motion remains a live rescue component.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `s2t/results/s2t_c6_l21_metric_strain_tensor_results.json`, `s2t/results/s2t_c6_l21_delta2_connection_single_gammaAB_ambient_simplified_results.json`, `s2t/results/s2t_c6_l21_delta2_connection_metric_cross_ambient_formula_results.json`, `s2t/results/s2t_c6_l21_delta2_principal_second_symbol_formula_results.json`, `wiki/questions/scalar-codifferential-ambient-gate.md`.
- This page is still formula-level. It does not evaluate scalar Green chains or quotient matrices.