# Projector T5 Quotient Contraction Table

> Status: computed / direct channel closed
> Type: question / audit result
> Updated: 2026-08-02

## Question

Does the scalar `ell=4` leakage already found in `T1` and `T3` survive after the outer projector factor `dG` is paired with the quotient-normalized low coexact one-form bases?

## Plain-Language Summary

No, not through the direct outer-`dG` channel. The full table contains `36` low coexact one-forms and all `25` scalar harmonics in the `ell=4` shell. Every entry vanishes to numerical precision, and the vanishing follows from an exact Hodge identity rather than from an accidental cancellation.

This is a real positive result for the projector route. The subsequent cross-return channel also vanishes by `Delta_1(g)d=dDelta_0(g)`. Hilbert/basis transport changes the intermediate self-adjoint representation but is exactly determinant-neutral after its second-order similarity term is included.

## Bases And Normalization

The audit uses:

```text
scalar columns: complete ell=4 harmonic shell, dimension 25,
one-form rows: 6 normalized n=1 Killing forms + 30 normalized n=3 coexact forms,
space: L(2,1)=RP3,
Vol(L(2,1))=pi^2,
Delta_0 Y_4 = 24 Y_4,
G Y_4 = Y_4/24.
```

The resulting table is

```text
C_T5[beta,Y_4] = <beta_coex, d G Y_4>,
shape = 36 x 25.
```

## Exact Reason For Vanishing

For every coexact one-form `beta` and every zero-mean scalar `phi`,

```text
<beta_coex, d G phi>
  = <delta beta_coex, G phi>
  = 0.
```

Thus any scalar leakage appearing only inside the outer `dG` of `Pi_AB` is exact and cannot survive direct projection onto the background coexact quotient. This applies not only to the explicit `T1/T3` `ell=4` witnesses, but to any scalar shell in that same outer-`dG` position.

## Computed Table

| Quantity | Result |
|---|---:|
| Table shape | `36 x 25` |
| Maximum absolute raw entry | `2.7712207529e-16` |
| Frobenius norm | `1.1182636696e-15` |
| Numerical rank at `1e-10` | `0` |
| `T1` witness maximum contraction | `1.8041124150e-16` |
| `T3` witness maximum contraction | `2.8310687128e-15` |

The `T1` and `T3` scalar witnesses themselves are nonzero. Their `dG` one-forms also have nonzero norm. What vanishes is specifically their projection onto the low coexact quotient.

## Basis Checks

| Check | Result |
|---|---:|
| `ell=4` scalar dimension | `25` |
| Scalar harmonic constraint residual | `1.37e-14` |
| Scalar orthonormality error | `3.11e-15` |
| `n=3` coexact dimension | `30` |
| `n=3` constraint residual | `5.57e-15` |
| `n=3` orthonormality error | `1.89e-15` |

## What Is Closed

- Direct `T1/T3 -> ell=4 -> dG -> n=1/n=3 coexact` contraction is zero.
- Pure higher-shell terms inside the outer `dG` of `Pi_AB` do not by themselves spoil the coexact quotient matrix.
- A manual `ell=0,2` cutoff is not needed for this direct channel; exact/coexact orthogonality removes it structurally.

## What Remains Open

The full reduced-operator second variation also contains terms of the form

```text
Pi Delta_{1,A} Pi_B + Pi Delta_{1,B} Pi_A.
```

Here `Pi_B alpha` is exact, but `Delta_{1,A}` acts before the final `Pi`. The varied one-form operator need not preserve the background exact/coexact splitting. Therefore the next matrix is the cross-return block

```text
R_AB(beta,alpha)
  = <beta_coex, Pi Delta_{1,A} d G D_B alpha> + (A <-> B).
```

This block vanishes by Hodge commutation. The active bottleneck is now the genuine mixed second Hodge operator, not projector or Hilbert representation motion.

## Verdict

`T5` passes for the direct outer-`dG` channel, the cross-return channel vanishes, and Hilbert similarity leaves the log determinant unchanged. This increases confidence in projector/Hilbert consistency but does not upgrade `S_vac`; the genuine `L_AB` operator remains open.

## Reproduction

- Script: `s2t_c6_projector_t5_quotient_contraction_audit.py`
- Result: `s2t_c6_projector_t5_quotient_contraction_results.json`

## Links

- [[projector-coefficient-test-protocol]] — definitions of `T1--T5`.
- [[projector-t1-coefficient-witness]] — nonzero `T1` scalar leakage.
- [[projector-t2-t3-coefficient-witness]] — zero `T2`, nonzero `T3`.
- [[delta2-projector-expansion-gate]] — full second-projector formula.
- [[projector-hilbert-rescue-sprint]] — broader projector/Hilbert work package.
- [[research-roadmap-2026-08-02]] — current decision roadmap.
- [[s2t-closure-roadmap]] — global `C6` closure history.