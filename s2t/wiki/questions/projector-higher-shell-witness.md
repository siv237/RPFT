# Projector Higher Shell Witness

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Is the higher-shell leakage in the projector Green-chain route merely allowed by selection rules, or can we exhibit an explicit nonzero `ell=4` witness?

## Plain-Language Summary

This page gives a simple witness that higher scalar shells are real. A degree-2 scalar harmonic squared has a nonzero degree-4 harmonic part on `S^3`. Therefore, whenever projector Green-chain terms contain products/couplings of two first ambient strains, an `ell=4` channel is generically available. This does not yet compute the C6 projector matrix, but it blocks the shortcut “maybe representation theory keeps everything in `ell=0,2`.”

## Witness Setup

Work in ambient `R^4` with coordinates

```text
(x1,x2,x3,x4),   r^2=x1^2+x2^2+x3^2+x4^2.
```

Choose a traceless quadratic harmonic

```text
q = x1^2 - x2^2.
```

Restricted to `S^3`, this is an `ell=2` scalar harmonic. Consider

```text
P = q^2 = x1^4 - 2 x1^2 x2^2 + x2^4.
```

If `P` had no `ell=4` component, its degree-4 harmonic projection would vanish.

## Harmonic Projection Calculation

For degree `4` polynomials in `R^4`, write

```text
H = P + a r^2 Delta(P) + b r^4 Delta^2(P)
```

and choose `a,b` so that `Delta(H)=0`. Direct symbolic calculation gives

```text
Delta(P)  = 8 x1^2 + 8 x2^2,
Delta^2(P)=32,
a=-1/16,
b=1/384.
```

Thus

```text
H = P - (1/16) r^2 Delta(P) + (1/384) r^4 Delta^2(P),
Delta(H)=0,
H != 0.
```

One explicit expanded form is

```text
H =  7/12 x1^4 - 17/6 x1^2 x2^2
   - 1/3 x1^2 x3^2 - 1/3 x1^2 x4^2
   + 7/12 x2^4 - 1/3 x2^2 x3^2 - 1/3 x2^2 x4^2
   + 1/12 x3^4 + 1/6 x3^2 x4^2 + 1/12 x4^4.
```

Since this harmonic projection is nonzero, the product of two `ell=2` strain scalars contains a genuine `ell=4` component.

## Consequence For Projector Green Chains

From [[projector-shell-transition-table]], `L_A` carries degree `0+2` content and `L_AB` can carry degree `0+2+4` content. The witness above shows that the degree-4 content from two first strains is generically nonzero.

Therefore:

```text
ell=2 --L_A--> ell=4
ell=2 --L_A G L_B--> ell=6 possible through repeated degree-2 steps
ell=0 or 2 --L_AB--> ell=4 possible through degree-4 content
```

The exact C6 coefficient could still vanish after contraction with one-form bases or after same-scheme subtraction, but it cannot vanish merely because the `ell=4` representation is absent. It is present.

## Pass/Fail Result

| Test | Result | Meaning |
|---|---|---|
| Nonzero `ell=4` harmonic in `ell=2 x ell=2` | pass | higher shell exists explicitly |
| Representation-only rank-10 closure | fail | `P02=10` cannot be promoted to theorem by selection rules alone |
| Need coefficient test | yes | must test actual contractions such as `<ell=4|L_A|ell=2>` |
| Need subtraction/locality theorem | yes if coefficients nonzero | higher-shell finite pieces must be handled in same scheme |

## Plain-Language Verdict

The higher floor is real. We found a concrete `ell=4` piece, not just a formal possibility. The projector route now needs either explicit coefficient cancellation or a same-scheme rule that removes higher-shell contributions.

## Reproduction Snippet

The symbolic check used only `sympy`:

```python
import sympy as sp
x1,x2,x3,x4=sp.symbols('x1 x2 x3 x4')
vars=[x1,x2,x3,x4]
r2=sum(v*v for v in vars)
q=x1**2-x2**2
P=sp.expand(q*q)
Delta=lambda F: sum(sp.diff(F,v,2) for v in vars)
a,b=sp.symbols('a b')
H=sp.expand(P + a*r2*Delta(P) + b*r2**2*Delta(Delta(P)))
sol=sp.solve(sp.Poly(sp.expand(Delta(H)), *vars).coeffs(), [a,b], dict=True)
```

It returns `a=-1/16`, `b=1/384`, and a nonzero harmonic `H`.

## Links

- [[projector-coefficient-test-protocol]] — next coefficient tests deciding whether the witness survives C6 contractions.
- [[projector-t1-coefficient-witness]] — first concrete T1 witness for `L_A` leakage.
- [[projector-shell-transition-table]] — selection-rule table that this witness strengthens.
- [[projector-green-chain-reduction-gate]] — scalar Green-chain protocol.
- [[projector-ambient-substitution-gate]] — ambient substitution producing the Green-chain problem.
- [[projector-hilbert-rescue-sprint]] — computation-facing sprint.
- [[s2t-closure-roadmap]] — global C6/C11 roadmap.

## Source Notes

- Source paths: `wiki/questions/projector-shell-transition-table.md`, `wiki/questions/projector-green-chain-reduction-gate.md`.
- This page uses a local symbolic witness. It does not evaluate full quotient-normalized C6 projector matrix elements.