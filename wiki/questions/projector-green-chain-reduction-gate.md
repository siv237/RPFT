# Projector Green Chain Reduction Gate

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

How should the scalar Green chains

```text
G L_A G,
G L_A G L_B G,
G L_AB G
```

inside the projector variation be reduced on `RP^3` without introducing a manual cutoff or a fitted finite residue?

## Plain-Language Summary

The projector formulas now reduce to scalar Green chains. This means the next problem is spectral: insert scalar harmonics between the operators, divide by scalar eigenvalues, and sum the allowed `RP^3` even shells. The danger is obvious: if we manually keep only `ell=0,2`, we repeat the rank-10 assumption instead of proving it. This page sets the rules for doing the reduction honestly.

## Scalar Spectrum Convention

For scalar harmonics on unit `S^3`, use

```text
lambda_ell = ell(ell+2),
d_ell = (ell+1)^2.
```

On `RP^3=S^3/Z2`, only even `ell` scalar harmonics descend:

| `ell` | `lambda_ell` | degeneracy | role |
|---:|---:|---:|---|
| `0` | `0` | `1` | true scalar zero mode; removed from `G=Delta_0^{-1}_{det'}` |
| `2` | `8` | `9` | first nonzero even scalar shell |
| `4` | `24` | `25` | first dangerous higher shell |
| `6` | `48` | `49` | higher shell |

The rank `10=1+9` remains structurally important for `P02`, but the Green operator `G` must not invert the `ell=0` zero mode. Therefore projector Green-chain calculations must distinguish:

```text
P02 as deformation space: ell=0 plus ell=2,
G as scalar inverse: ell=2,4,6,... only.
```

## Operator Selection Rules To Test

The ambient-substituted first variation has the schematic form

```text
L_A = 2 S_A^{ij} nabla_i nabla_j - 6 a_A^k nabla_k.
```

Since `A` lives in `Sym^2(R4)`, its scalar content is `ell=0 plus ell=2`. Acting on scalar shell `ell`, `L_A` can in principle couple to shells allowed by the Clebsch/product rules with a degree-2 tensor insertion. The expected scalar shell window is therefore roughly

```text
ell -> ell-2, ell, ell+2
```

subject to parity and derivative selection rules. This must be verified, not assumed.

## Green-Chain Expansion Template

Let `{Y_{ell,m}}` be quotient-normalized even scalar harmonics on `RP^3`, excluding the zero mode for `G`. Then

```text
G L_A G
= sum_{ell,m; ell',m'}
    |Y_ellm> (1/lambda_ell)
    <Y_ellm, L_A Y_ell'm'>
    (1/lambda_ell') <Y_ell'm'|.
```

Similarly,

```text
G L_A G L_B G
= sum_{ell,m; r,s; ell',m'}
    |Y_ellm> (1/lambda_ell)
    <Y_ellm, L_A Y_rs>
    (1/lambda_r)
    <Y_rs, L_B Y_ell'm'>
    (1/lambda_ell') <Y_ell'm'|.
```

And

```text
G L_AB G
= sum_{ell,m; ell',m'}
    |Y_ellm> (1/lambda_ell)
    <Y_ellm, L_AB Y_ell'm'>
    (1/lambda_ell') <Y_ell'm'|.
```

All sums are over even nonzero scalar shells unless a separate zero-mode/gauge-volume convention explicitly contributes outside `G`.

## Pass/Fail Gates

| Gate | Pass Means | Fail Means |
|---|---|---|
| Zero-mode separation | `ell=0` is excluded from `G` but retained as deformation trace direction where appropriate | scalar zero mode contaminates `det'` inverse |
| Shell selection rule | allowed `ell` transitions are derived from representation/product rules | cutoff is manual |
| Higher-shell suppression/locality | `ell>=4` contributions are proven local/subtracted/suppressed in same scheme | rank-10 projector theorem fails |
| Finite matrix reduction | chains reduce to finite low-shell moments entering `C_proj` | projector remains formal |
| Same-scheme compatibility | scalar Green chain matches Maxwell--ghost `det'` and gauge-volume convention | C6 cannot be theorem-level |

## Key Warning

The number `10` cannot be imported into this calculation as a cutoff. It can only appear as an output of one of these mechanisms:

1. deformation-space rank `P02=1+9` while Green chains remain separately summed;
2. same-scheme locality/subtraction removes higher-shell finite parts before fitting;
3. representation rules make higher-shell contributions vanish in the needed matrix elements;
4. a computed residual forces downgrade of exact `pi^-4` absorption.

## Immediate Next Calculation

Build a scalar-shell transition table for `L_A` and `L_AB`:

```text
ell_in -> ell_out
```

for even `RP^3` shells, starting with `ell=2,4,6`, and classify which transitions can contribute when the outer projector acts on the low one-form shells `n=1` and `n=3`.

The first selection-rule table is now tracked in [[projector-shell-transition-table]]. It shows that higher even shells are generically allowed by representation selection, and [[projector-higher-shell-witness]] gives an explicit nonzero `ell=4` witness from `ell=2 x ell=2`. Thus rank-10 closure requires explicit coefficient vanishing, same-scheme locality/subtraction, or downgrade.

## Plain-Language Verdict

We have reached the projector's spectral accounting problem. The next thing to prove is not a number; it is whether the scalar Green chains naturally stay in the rank-10 window or leak into higher even shells. If they leak and are not local/subtracted, C6 does not become a theorem.

## Links

- [[projector-ambient-substitution-gate]] — ambient reduction producing the Green-chain problem.
- [[projector-shell-transition-table]] — first shell-leakage selection table for `L_A` and `L_AB`.
- [[projector-higher-shell-witness]] — explicit symbolic witness that the `ell=4` channel exists.
- [[projector-coefficient-test-protocol]] — T1--T5 tests for dangerous coefficients and quotient contractions.
- [[delta2-projector-expansion-gate]] — `Pi_AB` formula containing the Green chains.
- [[scalar-codifferential-ambient-gate]] — `L_A`, `L_AB`, `D_A`, `D_AB` slots.
- [[projector-hilbert-rescue-sprint]] — computation-facing sprint.
- [[finite-gap-source-audit]] — gap-source verdict table.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `s2t/results/s2t_determinant_casmix_results.json`, `s2t/results/s2t_integer10_origin_results.json`, `s2t/results/s2t_mixed_trace_operator_results.json`, `s2t/results/s2t_c6_l21_coexact_basis_results.json`, `wiki/questions/projector-ambient-substitution-gate.md`.
- This page is a reduction protocol, not a completed Green-chain computation.