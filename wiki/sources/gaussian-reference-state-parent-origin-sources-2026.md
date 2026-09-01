# Источники parent-origin Gaussian reference state

> Status: mature
> Type: source
> Updated: 2026-09-01

## Summary

Multivariate Ornstein--Uhlenbeck process имеет centered Gaussian stationary
state, covariance которого решает Lyapunov equation. Это обеспечивает
условную stationary architecture, но не выбирает diffusion/drift ratio.

## Key Points

- Для `dX=-BX dt+sqrt(2D)dW` stationary covariance решает
  `BS+SB^T=2D`.
- Stable drift делает solution unique при фиксированных `B,D`.
- В isotropic family `S=(delta/gamma)I`, поэтому unit covariance требует
  дополнительного fluctuation--dissipation relation.
- Common time rescaling не устраняет свободный covariance ratio.

## Links

- [[version9-physical-reopening-gaussian-reference-state-parent-origin-gate]]
- [[version9-physical-reopening-common-origin-carrier-admission-gate]]
- [[physical-reopening-common-origin-carrier-sources-2026]]

## Source Notes

- C. Godrèche, J.-M. Luck, “Characterising the nonequilibrium stationary
  states of Ornstein–Uhlenbeck processes”, Journal of Physics A 52 (2019),
  035002; arXiv:1807.00694. Equations (2.12)--(2.17) give the covariance
  evolution, stationary Lyapunov equation and reversible solution.
- `s2t/gates/version9_physical_reopening_gaussian_reference_state_parent_origin_gate.tex`
- `s2t/results/s2t_v9_physical_reopening_gaussian_reference_state_parent_origin_gate_results.json`