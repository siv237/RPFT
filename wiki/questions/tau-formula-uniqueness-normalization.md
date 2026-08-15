# Tau Formula Uniqueness and Normalization

> Status: strong numerical relation; derivation conditional
> Date: 2026-08-04

## Numerical Robustness

Against the current control `m_tau=1776.93(9) MeV`, the formula

```text
m_tau/m_mu=pi^2+2pi+2/3-alpha/3
```

predicts `1776.85943 MeV`, or `-0.78 sigma`. Removing the QED term gives `+2.07 sigma`.

## Look-Elsewhere Diagnostic

Freeze the grammar

```text
pi^2+n*pi+p/q+c*alpha,
n=0...4,
|p|<=4,
q<=6,
c in {0,+/-1,+/-1/2,+/-1/3,+/-2/3}.
```

Among `1485` candidates, the claimed formula ranks first and is the only one inside one or two experimental sigmas. The same remains true when restricted to candidates of equal or lower description complexity. This is evidence that the numerical relation is not a trivial dense rational approximation inside this grammar. It is not a universal probability against all possible formula searches.

## Provenance Failure

The Tome does not derive the seed

```text
rho0=pi^2+2pi+2/3;
```

it introduces it as the premise of the QED theorem.

The displayed compact self-energy sum evaluates to

```text
sum (-1)^q integral_0^1 (1+x)K0(2pi qx) dx = -0.19382665,
sum/pi = -0.06169694.
```

Therefore it does not itself produce coefficient `1/3`. Matching the claimed magnitude requires an `RP3` Jacobian of magnitude `5.40275`, but no explicit projection trace or numerical derivation of that Jacobian is supplied.

## Verdict

The tau relation survives as the strongest low-complexity numerical pattern in the current program, but not as a closed theorem. It should be classified as a strong conditional relation until both `rho0` and the projection normalization are independently derived.

## Constructive Follow-Up

A direct-sum Gram tangent reproduces `rho0` exactly, while the pre-existing traceless rank-nine strain space combined with the quotient volume suggests `J=9/2`. This gives the revised prediction `m_tau=1776.90237 MeV`, or `-0.31 sigma`. The proposal remains post-audit until the ambient lepton trace fixes its normalization. See [[tau-operator-projection-candidate]].

The ambient normalization gate later rejects `J=9/2`: normalized quotient modes cancel the half-volume, and a canonical single collective field gives `J=1`. The original relation therefore remains numerical rather than operator-derived.