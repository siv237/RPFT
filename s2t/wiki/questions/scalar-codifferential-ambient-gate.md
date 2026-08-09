# Scalar Codifferential Ambient Gate

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

What are the ambient-path formulas for the scalar Laplacian variations `L_A`, `L_AB` and codifferential variations `D_A`, `D_AB` needed inside the `delta2 Pi_coex` gate?

## Plain-Language Summary

The projector formula now names the hinges of the moving coexact doorway. This page names the pieces that move those hinges: the scalar Laplacian `L=Delta_0` and the codifferential `D=delta_g`. The result is still a formula gate, not a matrix computation.

## Conventions

Use the positive Laplacian convention compatible with the one-form sign convention

```text
Delta_1 alpha = -nabla^2 alpha + Ric(alpha).
```

For scalar functions,

```text
L f = Delta_0 f = - g^{ij} nabla_i nabla_j f.
```

For one-forms,

```text
D alpha = delta_g alpha = - g^{ij} nabla_i alpha_j.
```

Let the locked ambient path be

```text
F_eps(x) = (I + eps A)x,      A=A^T,
g_eps = F_eps^* <.,.>.
```

Define inverse-metric variations

```text
p_A^{ij}  := partial_A g^{ij} = - h_A^{ij},
p_AB^{ij} := partial_A partial_B g^{ij}
          = h_A^i{}_k h_B^{kj} + h_B^i{}_k h_A^{kj} - k_AB^{ij}.
```

Define connection variations

```text
Gamma_A^k{}_{ij}  := partial_A Gamma^k{}_{ij},
Gamma_AB^k{}_{ij} := partial_A partial_B Gamma^k{}_{ij}.
```

Existing ambient-path audits already provide formulas for `h_A`, `p_AB`, and the connection slots.

## First Variations

For a scalar `f`,

```text
L_A f
  = h_A^{ij} nabla_i nabla_j f
    + C_A^k nabla_k f,

C_A^k := g^{ij} Gamma_A^k{}_{ij}
       = nabla^i h_A{}_i{}^k - 1/2 nabla^k tr(h_A).
```

For a one-form `alpha`,

```text
D_A alpha
  = h_A^{ij} nabla_i alpha_j
    + C_A^k alpha_k.
```

Thus the same contracted connection vector `C_A` controls both first variations. This is useful for projector work because `D_A` and `L_A` share the same metric-divergence data.

## Mixed Second Variations

For a scalar `f`,

```text
L_AB f
  = - p_AB^{ij} nabla_i nabla_j f
    + p_A^{ij} Gamma_B^k{}_{ij} nabla_k f
    + p_B^{ij} Gamma_A^k{}_{ij} nabla_k f
    + g^{ij} Gamma_AB^k{}_{ij} nabla_k f.
```

Equivalently, using `p_A=-h_A`,

```text
L_AB f
  = - p_AB^{ij} Hess_ij(f)
    - h_A^{ij} Gamma_B^k{}_{ij} nabla_k f
    - h_B^{ij} Gamma_A^k{}_{ij} nabla_k f
    + g^{ij} Gamma_AB^k{}_{ij} nabla_k f.
```

For a one-form `alpha`,

```text
D_AB alpha
  = - p_AB^{ij} nabla_i alpha_j
    + p_A^{ij} Gamma_B^k{}_{ij} alpha_k
    + p_B^{ij} Gamma_A^k{}_{ij} alpha_k
    + g^{ij} Gamma_AB^k{}_{ij} alpha_k.
```

Equivalently,

```text
D_AB alpha
  = - p_AB^{ij} nabla_i alpha_j
    - h_A^{ij} Gamma_B^k{}_{ij} alpha_k
    - h_B^{ij} Gamma_A^k{}_{ij} alpha_k
    + g^{ij} Gamma_AB^k{}_{ij} alpha_k.
```

These formulas are component-fixed variations. They must later be combined with Hilbert/basis transport if the basis itself is moved or re-orthonormalized.

## Insertion Into Projector Gate

The [[delta2-projector-expansion-gate]] uses

```text
G_A  = - G L_A G,
G_AB = G L_A G L_B G + G L_B G L_A G - G L_AB G,
Pi_AB = -d[ G_AB D + G_A D_B + G_B D_A + G D_AB ].
```

This page supplies the required `L_A`, `L_AB`, `D_A`, and `D_AB` formula slots.

## Pass/Fail Gates

| Gate | Status | Meaning |
|---|---|---|
| `L_A` formula | pass | first scalar Laplacian variation is insertion-ready |
| `D_A` formula | pass | first codifferential variation is insertion-ready |
| `L_AB` formula | pass/formula-level | mixed scalar Laplacian variation is expressed through `p_AB`, `Gamma_A`, `Gamma_B`, `Gamma_AB` |
| `D_AB` formula | pass/formula-level | mixed codifferential variation is expressed through the same ambient data |
| quotient matrix evaluation | not yet | no `C_proj` values computed |
| self-adjointness with Hilbert metric | not yet | needs moving inner-product check |

## Remaining Work

1. Substitute the already-derived ambient simplifications for `Gamma_A`, `Gamma_AB`, and `p_AB`.
2. Reduce the resulting operators against scalar harmonics and one-form Killing/coexact bases.
3. Check which terms vanish on initially coexact input and which re-enter through side projectors.
4. Combine with Hilbert/basis transport before interpreting determinant traces.

## Plain-Language Verdict

The doorway hinges now have motion formulas. This is progress from “we need projector variation” to “here are the four operators to insert.” No C6 rescue is claimed until these formulas produce quotient-normalized matrix entries.

## Links

- [[projector-ambient-substitution-gate]] — ambient simplification of these slots into `S_A`, `a_A`, `tau_A`, `w_AB`, and `p_AB`.
- [[delta2-projector-expansion-gate]] — projector formula gate using these slots.
- [[projector-hilbert-rescue-sprint]] — sprint page for projector/Hilbert rescue.
- [[finite-gap-source-audit]] — why projector/Hilbert remain live rescue components.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `s2t_c6_l21_metric_strain_tensor_results.json`, `s2t_c6_l21_delta2_principal_second_symbol_formula_results.json`, `s2t_c6_l21_delta2_second_projector_formula_results.json`, `s2t_c6_l21_delta2_connection_single_gammaAB_ambient_simplified_results.json`, `s2t_c6_l21_laplacian_variation_results.json`.
- This page fixes formula slots only; it does not evaluate quotient integrals.