# Version IV: spin-branch mass stationarity gate

> Status: working
> Research status: closed negatively
> Type: question
> Updated: 2026-08-11

## Problem

An independent audit proposed the periodic/antiperiodic fermion determinant
difference as the last scheme-independent mechanism that might fix a
nonzero `chi R` without new physics. It also questioned whether the vector
mass was external because all three physical scalar modes are massive.

## Search for solution

- Rechecked the charged finite coordinates and BV complex.
- Distinguished the three physical quotient scalars from the gauge-orbit
  Goldstone direction.
- Differentiated the exact periodic/AP determinant ratio analytically with
  respect to `x=chi R3`.
- Verified the derivative with converged shell sums.

## Gauge clarification

The vector mass is derived from the charged vacuum:

```text
|x|=|z|=chi/sqrt(2),
m_A^2/chi^2=8g^2=3.
```

The Goldstone is not one of the three physical scalar eigenmodes. It belongs
to the gauge orbit and shares `Delta0+xi m_A^2` with the longitudinal and
ghost blocks. No external Stueckelberg mass is needed.

## Exact derivative

For two Dirac pairs,

```text
Delta Gamma_AP-P = -2 sum_k d_k I(r sqrt((k+3/2)^2+x^2)),
I(rho)=2 log coth(pi rho).
```

Its derivative is

```text
d_x Delta Gamma = 8 pi r x sum_k d_k /
  [sqrt((k+3/2)^2+x^2) sinh(2 pi r sqrt((k+3/2)^2+x^2))].
```

Every term is positive for `x>0`. Therefore the difference is strictly
monotone and has no nonzero stationary point. At `r=1`,

```text
x=1: Delta Gamma=-1.9482804e-4,
     derivative=+6.7652689e-4.
```

## Verdict

The branch difference is finite, nontrivial and free of local counterterm
ambiguities, but it does not select a nonzero mass ratio or absolute scale.
The last no-new-physics fixed-`K` route is closed.

Reopening now requires either a new chiral/topological measure or the
variational-carrier architecture described in
[[zero-prompt-toe-carrier-trace-2026-08-11]].

## Links

- [[version4-spin-sum-measure-gate]]
- [[zero-prompt-toe-carrier-trace-2026-08-11]]
- [[version4-observed-reconstruction-roadmap]]

## Sources

- `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex`
- `s2t/results/s2t_v4_spin_branch_mass_stationarity_gate_results.json`