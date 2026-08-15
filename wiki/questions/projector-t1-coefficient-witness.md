# Projector T1 Coefficient Witness

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Is the first dangerous projector coefficient

```text
T1 = <ell=4 | L_A | ell=2>
```

generically nonzero?

## Plain-Language Summary

Yes, at the symbolic witness level. For a simple traceless strain `A=diag(1,-1,0,0)` and the matching `ell=2` scalar harmonic `q=x1^2-x2^2`, the ambient-substituted operator `L_A` produces a function whose degree-4 harmonic projection is nonzero. This means the first projector Green insertion can really leave the rank-10 window.

This is not yet the full C6 quotient matrix, but it is the first concrete dangerous coefficient witness.

## Setup

Use the locked ambient first-strain formulas from [[projector-ambient-substitution-gate]]:

```text
L_A f = 2 S_A^{ij} nabla_i nabla_j f - 6 a_A^k nabla_k f.
```

Choose

```text
A = diag(1,-1,0,0),
q = x1^2 - x2^2.
```

Here `q` is an `ell=2` scalar harmonic on `S^3` and descends to `RP^3` because it is even under `x -> -x`.

Using the sphere identities

```text
Hess(q) = 2 S_A - 2 q g,
grad(q) = 2 a_A,
tau_A = Tr_T(S_A) = -q,
```

one obtains a sphere representative for `L_A q`. Reducing modulo `r^2=1`, the expression contains the quartic part

```text
20 x1^4 - 40 x1^2 x2^2 + 20 x2^4 = 20 (x1^2-x2^2)^2.
```

## Harmonic Projection

The degree-4 harmonic projection of the quartic part is nonzero. Explicitly, for

```text
P = 20 (x1^2-x2^2)^2,
r^2=x1^2+x2^2+x3^2+x4^2,
```

write

```text
H = P - (1/16) r^2 Delta(P) + (1/384) r^4 Delta^2(P).
```

Then

```text
Delta(H)=0,
H != 0.
```

One expanded form is

```text
H =  35/3 x1^4 - 170/3 x1^2 x2^2
   - 20/3 x1^2 x3^2 - 20/3 x1^2 x4^2
   + 35/3 x2^4 - 20/3 x2^2 x3^2 - 20/3 x2^2 x4^2
   + 5/3 x3^4 + 10/3 x3^2 x4^2 + 5/3 x4^4.
```

Therefore

```text
Proj_ell=4(L_A q) != 0.
```

## Consequence

The coefficient family

```text
<ell=4 | L_A | ell=2>
```

is not structurally zero. Hence `G L_A G` can connect the first nonzero scalar Green shell `ell=2` to `ell=4`.

This strengthens the warning from [[projector-shell-transition-table]]:

```text
L_A: ell=2 -> ell=4
```

is not merely allowed; it has a concrete nonzero witness.

## Pass/Fail Result

| Test | Result | Meaning |
|---|---|---|
| T1 representation allowed | pass | selection rules allow `ell=2 -> ell=4` |
| T1 symbolic coefficient witness | pass | explicit `L_A q` has nonzero `ell=4` projection |
| Rank-10 closure by first projector insertion | fail/generic | `G L_A G` is not confined to `ell=2` |
| Full C6 quotient leakage | not yet | must still test low one-form contraction `T5` |

## Plain-Language Verdict

The first door sensor fires. The projector Green chain can step from `ell=2` to `ell=4`. The only remaining ways to save rank-10 projector closure are quotient contraction cancellation, same-scheme locality/subtraction, or full inclusion of higher shells.

## Reproduction Snippet

The witness was checked with `sympy` by computing a sphere representative of `L_A q`, reducing modulo `r^2=1`, and projecting the quartic part to degree-4 harmonics:

```python
import sympy as sp
x1,x2,x3,x4=sp.symbols('x1 x2 x3 x4')
# A=diag(1,-1,0,0), q=x1**2-x2**2
# quartic part of L_A q on S3 is 20*(x1**2-x2**2)**2
P=20*(x1**2-x2**2)**2
r2=x1**2+x2**2+x3**2+x4**2
Delta=lambda F: sum(sp.diff(F,v,2) for v in [x1,x2,x3,x4])
H=sp.expand(P - sp.Rational(1,16)*r2*Delta(P) + sp.Rational(1,384)*r2**2*Delta(Delta(P)))
assert sp.expand(Delta(H)) == 0
assert H != 0
```

## Links

- [[projector-coefficient-test-protocol]] — defines T1--T5 tests.
- [[projector-t2-t3-coefficient-witness]] — next coefficient witness page for the mixed second slot.
- [[projector-higher-shell-witness]] — earlier `ell=2 x ell=2` witness.
- [[projector-shell-transition-table]] — selection rules.
- [[projector-green-chain-reduction-gate]] — scalar Green-chain protocol.
- [[projector-ambient-substitution-gate]] — formula for `L_A`.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `wiki/questions/projector-coefficient-test-protocol.md`, `wiki/questions/projector-ambient-substitution-gate.md`, `wiki/questions/projector-higher-shell-witness.md`.
- This page proves a symbolic coefficient witness, not a full quotient-normalized projector matrix.