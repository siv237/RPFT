# Projector T2 T3 Coefficient Witness

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

What happens to the next projector leakage tests

```text
T2 = <ell=4 | L_AB | ell=0>,
T3 = <ell=4 | L_AB | ell=2> ?
```

## Plain-Language Summary

One sensor turns off and one sensor fires. `T2` vanishes for a simple reason: `L_AB` is differential and kills the scalar constant. But `T3` is dangerous: for the same simple traceless strain used in the T1 witness, `L_AA q` has a nonzero `ell=4` harmonic projection. Thus the mixed second projector slot can also leak from `ell=2` to `ell=4`.

## T2: Constant Input

From [[projector-ambient-substitution-gate]],

```text
L_AB f = -p_AB^{ij} Hess_ij(f) + b_AB^k nabla_k f.
```

For the constant scalar `f=1`,

```text
Hess(1)=0,
nabla(1)=0,
```

therefore

```text
L_AB(1)=0,
T2=<ell=4|L_AB|ell=0>=0.
```

This is a genuine simplification: the trace scalar zero mode does not feed `ell=4` through `L_AB` itself. It still must be handled separately in determinant/gauge-volume bookkeeping because `ell=0` is excluded from `G=Delta_0^{-1}_{det'}`.

## T3: `ell=2` Input

Use

```text
A=B=diag(1,-1,0,0),
q=x1^2-x2^2.
```

Using the ambient-substituted mixed slot

```text
L_AA q = -p_AA^{ij} Hess_ij(q) + b_AA^k nabla_k q,
```

with

```text
b_AA = 8 tau_A a_A + 3 w_AA,
```

a symbolic sphere representative reduces modulo `r^2=1` to

```text
L_AA q = 96 x1^6 - 288 x1^4 x2^2 - 172 x1^4
        +288 x1^2 x2^4 +100 x1^2
        -96 x2^6 +172 x2^4 -100 x2^2.
```

The quartic part is

```text
-172 x1^4 + 172 x2^4.
```

Its degree-4 harmonic projection is nonzero:

```text
H4 = -43 x1^4 + 129 x1^2 x3^2 + 129 x1^2 x4^2
     +43 x2^4 -129 x2^2 x3^2 -129 x2^2 x4^2,
Delta(H4)=0,
H4 != 0.
```

Therefore

```text
Proj_ell=4(L_AA q) != 0,
T3=<ell=4|L_AB|ell=2> != 0
```

at symbolic witness level.

## Pass/Fail Result

| Test | Result | Meaning |
|---|---|---|
| T2 `<ell=4|L_AB|ell=0>` | zero | constant input is killed by `Hess` and `nabla` |
| T3 `<ell=4|L_AB|ell=2>` | nonzero witness | mixed second slot leaks to `ell=4` |
| Rank-10 closure by `L_AB` structure | fail/generic | `L_AB` is not confined to `ell=0,2` |
| Full C6 quotient survival | not yet | still requires T5 low one-form contraction check |

## Plain-Language Verdict

The trace direction is safe for this particular `L_AB` operator, but the first nonzero scalar shell is not safe. The second mixed projector hinge can also open into `ell=4`.

## Reproduction Notes

The symbolic check used the same ambient objects as [[projector-ambient-substitution-gate]]:

```text
p_AA = 2 h_A^2 - k_AA,
L_AA q = -p_AA:Hess(q) + b_AA.grad(q).
```

A `sympy` reduction modulo `r^2=1` and degree-4 harmonic projection gave the nonzero `H4` above.

## Links

- [[projector-coefficient-test-protocol]] — defines T1--T5 tests.
- [[projector-t1-coefficient-witness]] — first nonzero T1 witness.
- [[projector-shell-transition-table]] — shell transition rules.
- [[projector-green-chain-reduction-gate]] — scalar Green-chain protocol.
- [[projector-ambient-substitution-gate]] — formulas for `L_AB`.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `wiki/questions/projector-coefficient-test-protocol.md`, `wiki/questions/projector-ambient-substitution-gate.md`, `wiki/questions/projector-t1-coefficient-witness.md`.
- This page is a symbolic witness page. It does not evaluate the final quotient-normalized projector matrix.