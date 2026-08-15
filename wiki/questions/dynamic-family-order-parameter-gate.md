# Dynamic Family Order Parameter Gate

> Status: working
> Research status: projected algebraic selector pass; bulk origin, parity and full gap open
> Type: question
> Updated: 2026-08-15

The residual group forbids a constant invariant antisymmetric family form,
but permits the dynamical invariant

```text
epsilon_ijk Sigma_k chi_i chi_j.
```

For every nonzero `Sigma`, the induced antisymmetric matrix has rank two and
reduces three Majorana core modes to one.

## Corrected Potential

For

```text
V=m2 |Sigma|^2 + (u/4)|Sigma|^4 + v Sigma1 Sigma2 Sigma3,
```

the favored diagonal branch obeys

```text
3 u s^2 - |v| s + 2 m2 = 0.
```

There are four favored sign orientations, not eight minima. A first-order
transition occurs at `m2=v^2/(27u)`, so condensation can occur even for
positive quadratic mass.

## Geometric Quadratic Term

The product-factor Laplacian supplies

```text
M_Sigma^2=m0^2 I + kappa L(w3,w1).
```

For positive `kappa` and the declared unit-radius kernels, the `S1` character
is the unique lowest direction. This is a geometric mass selector, although
`kappa` and its sign remain parent-action gates.

## Fermion Contribution

If both parity branches are available, the paired Majorana modes give the
ground-state cusp `-|g Sigma|/2`. This is not yet a universal condensation
theorem: fixed global fermion parity can forbid branch switching, and three
local Majoranas require a bulk or remote parity completion. At finite beta the
effect is a negative quadratic shift, so the full renormalized mass must still
be checked. The spectrum depends only on `|Sigma|` and cannot generate the
cubic orientation term.

## Bulk--Core Gate

The invariant `epsilon_ijk Sigma_k chi_i chi_j` is valid for projected real
core Majorana operators. A four-dimensional Lorentz-scalar Weyl/Majorana
bilinear is symmetric in family indices, so its contraction with epsilon
vanishes. The parent theory must therefore derive the antisymmetric core
operator from zero-mode projection, a family connection, or another allowed
bulk derivative operator.

## Exact Axis Stability

For an axial condensate `(0,s,0)`, the transverse Hessian is

```text
[[2(mu1-mu2), v s],
 [v s, 2(mu3-mu2)]].
```

The axis is stable iff `mu1>mu2`, `mu3>mu2`, and
`4(mu1-mu2)(mu3-mu2)>v^2 s^2`.

## Rank-One Scope

Rank one is exact in the three-mode projected core Hamiltonian. A full BdG
claim additionally requires a gap or Feshbach--Schur proof excluding other
bulk/core zero pairs.

## Evidence

- `s2t/audits/s2t_dynamic_family_order_parameter_audit.py`
- `s2t/results/s2t_dynamic_family_order_parameter_results.json`
- `s2t/gates/dynamic_family_order_parameter_gate.tex`