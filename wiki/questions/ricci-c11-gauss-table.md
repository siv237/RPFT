# Ricci C11 Gauss Table

> Status: working
> Research status: computed / geometric cancellation failed
> Type: question
> Research type: question / audit result
> Updated: 2026-08-02

## Question

Can the mixed second Ricci/curvature block cancel the already nonzero principal-plus-connection `C_delta2[1,1]` table?

## Plain-Language Summary

No. Curvature is a real and nontrivial contribution, but it reinforces rather than removes the key obstruction. After adding Ricci to principal plus connection, all `55` symmetric deformation pairs remain nonzero.

This lowers the prospects of closing `C6` through a purely geometric cancellation. The theory remains viable only if the remaining same-scheme determinant terms provide a mandatory compensation, or if `pi^-4` is downgraded from theorem to structural compression.

## Geometric Method

Instead of expanding all second Christoffel derivatives directly, the calculation uses the Gauss equation for the linear ellipsoid

```text
F(x)=Mx,
M=I+epsilon A+eta B.
```

Let

```text
C=M^T M,
t=x^T C^(-1)x,
Q=C^(-1)-C^(-1)x x^T C^(-1)/t.
```

The shape operator pulled back to the background tangent space is

```text
S=t^(-1/2) Q,
```

and the mixed Ricci endomorphism follows exactly from

```text
Ric# = tr(S)S-S^2.
```

The mixed `epsilon eta` coefficient is integrated against the six quotient-normalized `n=1` Killing forms using exact rational sphere moments.

## Controls

- Pure scaling `A=B=I` gives `delta2 Ric#=12I` on tangent one-forms exactly.
- Every Ricci matrix is symmetric in the six-state basis.
- A separate pointwise finite-difference check on representative strain pairs agrees with the Gauss expansion to maximum error about `1.6e-6` at step `2e-5`.

## Ricci Table

| Quantity | Result |
|---|---:|
| Symmetric strain pairs | `55` |
| Rank `0` pairs | `12` |
| Rank `4` pairs | `27` |
| Rank `6` pairs | `16` |
| Matrix asymmetry | `0` |
| Pure-scaling control error | `0` |

The twelve zero Ricci pairs are mixed diagonal/off-diagonal combinations. Their vanishing does not create a cancellation because the principal-plus-connection block is nonzero there.

## Combined Table

After adding

```text
C_total = C_principal + C_connection + C_Ricci,
```

the result is:

| Combined rank | Pair count |
|---|---:|
| `4` | `39` |
| `6` | `16` |
| `0` | `0` |

Thus every one of the `55` deformation pairs remains active.

## Key Witness

For

```text
A=diag(1,-1,0,0),
```

the principal-plus-connection matrix is

```text
diag(26/3,4,4,4,4,6),
```

the Ricci matrix is

```text
diag(6,10/3,10/3,10/3,10/3,6),
```

and the combined result is

```text
diag(44/3,22/3,22/3,22/3,22/3,12).
```

Its trace increases from `92/3` to `56`, and `Tr(M^2)` increases from `1576/9` to `5168/9`.

## Effect On The Theory

This result **reduces the prospects of the current C6 rescue route**:

- projector leakage is already closed;
- Hilbert/basis transport is determinant-neutral;
- Ricci does not cancel principal plus connection;
- the purely geometric second-order block remains nonzero for every pair.

It does not disprove the entire theory. Independent successes `S_geo`, the tau row, and the Higgs EFT bridge are unaffected. It specifically weakens the claim that exact `pi^-4` absorption follows from the current Maxwell/coexact geometric determinant without an additional same-scheme identity.

## Next Gate

The next honest calculation is no longer another geometric subblock. It is the remaining determinant bookkeeping:

```text
Tr(L_0^(-1)L_AB)
- Tr(L_0^(-1)L_A L_0^(-1)L_B)
```

including ghost powers, `det'`, zero/gauge volume, local subtraction fixed before comparison, and the possible scalar half-determinant residue. If these do not provide a mandatory compensation, exact `pi^-4` should be downgraded.

## Reproduction

- Script: `s2t/audits/s2t_c6_l21_delta2_ricci_C11_gauss_audit.py`
- Ricci table: `s2t/results/s2t_c6_l21_delta2_ricci_C11_gauss_table_data.json`
- Combined table: `s2t/results/s2t_c6_l21_delta2_principal_connection_ricci_C11_table_data.json`
- Summary: `s2t/results/s2t_c6_l21_delta2_ricci_C11_gauss_results.json`

## Links

- [[tome2-svac-em-block-audit]] — full electromagnetic determinant audit.
- [[projector-t5-quotient-contraction-table]] — closed projector channel.
- [[finite-gap-source-audit]] — remaining same-scheme candidates.
- [[research-roadmap-2026-08-02]] — current decision roadmap.
- [[s2t-closure-roadmap]] — global C6 history.