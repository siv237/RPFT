# Projector Coefficient Test Protocol

> Status: working
> Type: question
> Updated: 2026-08-02

## Question

Which concrete coefficient tests decide whether the projector higher-shell leakage vanishes in the actual C6 quotient contractions?

## Plain-Language Summary

We already know the higher floor exists. This page defines the first tests that check whether C6 actually walks onto that floor. The test is not “can an `ell=4` harmonic exist?” It does. The test is whether the operators and quotient contractions used by C6 have nonzero matrix elements into those higher scalar shells.

## Starting Point

From [[projector-higher-shell-witness]], `ell=2 x ell=2` contains a nonzero `ell=4` component. From [[projector-shell-transition-table]],

```text
L_A:  ell -> ell-2, ell, ell+2,
L_AB: ell -> ell-4, ell-2, ell, ell+2, ell+4.
```

Therefore the rank-10 projector route survives only if the relevant coefficients vanish, or if higher-shell contributions are local/subtracted in the fixed determinant scheme.

## Test Objects

Use quotient-normalized scalar harmonics `Y_{ell,m}` on `RP^3` with even `ell`. Use `G=Delta_0^{-1}_{det'}`, so `ell=0` is excluded from the Green inverse.

Define coefficient families:

```text
T_A(ell_out,m_out; ell_in,m_in)
  = <Y_{ell_out,m_out}, L_A Y_{ell_in,m_in}>,

T_AB(ell_out,m_out; ell_in,m_in)
  = <Y_{ell_out,m_out}, L_AB Y_{ell_in,m_in}>.
```

For Green-chain leakage, define

```text
U_AB(ell_out,m_out; ell_in,m_in)
  = sum_{r,s in ell_mid}
      <Y_out, L_A Y_rs> (1/lambda_r) <Y_rs, L_B Y_in>
```

summed over allowed nonzero even intermediate shells.

## First Coefficient Tests

| Test | Coefficient | Why It Matters | Pass/Fail Meaning |
|---|---|---|---|
| T1 | `<ell=4 | L_A | ell=2>` | direct first-order leakage from first Green insertion | nonzero means `G L_A G` leaves rank-10 window |
| T2 | `<ell=4 | L_AB | ell=0>` | mixed second variation can create `ell=4` from trace direction | nonzero means trace direction feeds higher shells outside `G` bookkeeping |
| T3 | `<ell=4 | L_AB | ell=2>` | direct mixed second leakage from first nonzero scalar shell | nonzero means `G L_AB G` needs higher-shell sums |
| T4 | `<ell=6 | L_A G L_B | ell=2>` | two first-order insertions can climb two floors | nonzero means double Green-chain leakage reaches `ell=6` |
| T5 | low one-form contraction of T1/T3 | checks whether scalar leakage actually couples back into `n=1/n=3` one-form projector terms | nonzero means leakage survives C6 quotient contraction |

The first symbolic T1 witness is now tracked in [[projector-t1-coefficient-witness]]. It shows that `<ell=4|L_A|ell=2>` is not structurally zero.
The next symbolic T2/T3 check is tracked in [[projector-t2-t3-coefficient-witness]]: `T2` vanishes because `L_AB(1)=0`, while `T3` has a nonzero `ell=4` witness.
The direct T5 table is now tracked in [[projector-t5-quotient-contraction-table]]. Its complete `36 x 25` matrix has rank zero: after the outer `dG`, the scalar leakage is exact and is orthogonal to all background coexact `n=1/n=3` states. The remaining projector risk is the cross-return term in which `Delta_{1,A}` acts on a first projector variation before the final coexact projection.

## Minimal Witness Strategy

A full matrix is not needed for the first decision. It is enough to find one symmetry-allowed nonzero contraction in each dangerous family. A practical sequence is:

1. choose a simple `ell=2` scalar harmonic, e.g. `q=x1^2-x2^2`;
2. choose an ambient strain `A` aligned with `q`;
3. compute or project `L_A q` onto degree `4` harmonics;
4. compute or project `L_AB(1)` and `L_AB(q)` onto degree `4` harmonics;
5. if nonzero, test whether the resulting scalar piece contributes to the one-form projector side term after applying `dG` and pairing with the low one-form basis.

## Decision Rules

| Outcome | Consequence |
|---|---|
| All dangerous coefficients vanish by symmetry | projector route remains alive as finite rank-10 theorem candidate |
| Coefficients nonzero but one-form quotient contractions vanish | projector route remains alive, but needs documented quotient-cancellation lemma |
| Coefficients nonzero and quotient contractions nonzero | projector route leaks into higher shells; include higher-shell sums or downgrade |
| Coefficients nonzero but proven local/subtracted before fitting | route remains alive as same-scheme subtraction theorem |
| Coefficients nonzero and only ignored by cutoff | theorem route fails |

## Same-Scheme Requirement

A higher-shell term cannot be discarded because it is inconvenient. It may be removed only if one of the following is fixed before looking at the `alpha` match:

- a local heat-kernel subtraction theorem applies to the term;
- the term is pure gauge/slice and cancels with Hilbert/basis or zero/gauge Jacobian contributions;
- the physical transverse quotient definition excludes it by a proved projector identity;
- the full Maxwell--ghost determinant contains a paired cancellation in the same normalization.

## Plain-Language Verdict

The next job is a witness hunt in the coefficients. If we find one nonzero dangerous coefficient that survives quotient contraction, the rank-10 projector theorem is in serious trouble. If the dangerous coefficients vanish for structural reasons, the projector rescue becomes much stronger.

Current update: the direct outer-`dG` T5 contractions vanish structurally. The next job is no longer another direct scalar-shell witness; it is the projector cross-return matrix `Pi Delta_{1,A} Pi_B + A<->B`.

## Links

- [[projector-higher-shell-witness]] — proves the `ell=4` floor exists.
- [[projector-t1-coefficient-witness]] — explicit nonzero T1 coefficient witness.
- [[projector-t2-t3-coefficient-witness]] — T2/T3 symbolic coefficient result.
- [[projector-t5-quotient-contraction-table]] — complete direct T5 table and exact quotient-cancellation lemma.
- [[projector-shell-transition-table]] — selection rules for possible leakage.
- [[projector-green-chain-reduction-gate]] — scalar Green-chain reduction protocol.
- [[projector-ambient-substitution-gate]] — formulas for `L_A` and `L_AB`.
- [[projector-hilbert-rescue-sprint]] — broader C6 rescue sprint.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `wiki/questions/projector-higher-shell-witness.md`, `wiki/questions/projector-shell-transition-table.md`, `wiki/questions/projector-green-chain-reduction-gate.md`, `wiki/questions/projector-ambient-substitution-gate.md`.
- This page defines coefficient tests. It does not yet compute the full coefficients.