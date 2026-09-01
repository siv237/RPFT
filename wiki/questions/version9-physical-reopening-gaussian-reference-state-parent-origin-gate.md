# Parent-origin Gaussian reference state

> Status: mature
> Type: question
> Updated: 2026-09-01

## Summary

OU architecture даёт unique Gaussian stationary covariance при фиксированных
drift и diffusion, но structural conditions не выбирают их отношение.
Unit covariance остаётся условием `delta=gamma`, а не выведенным состоянием.

## Key Points

- `B=gamma I_10`, `D=delta I_10`.
- Stationary equation: `BS+SB^T=2D`.
- `S=(delta/gamma)I_10`.
- Covariance space dimension `55`; Lyapunov rank/nullity `55/0`.
- Witnesses `(1,1)` и `(1,2)` дают `I_10` и `2I_10`.
- Common coefficient rescaling сохраняет covariance ratio.
- Physical reference-state origin `0/1`; reopening packages `0/2`.

## Answer

Gaussian reference state существует условно, но не происходит из прежнего
parent. Uniqueness работает только после задания `gamma,delta`; symmetry,
stability и detailed balance допускают любое положительное
`delta/gamma`. Поэтому unit covariance не повышается до physical status.

## Links

- [[version9-physical-reopening-common-origin-carrier-admission-gate]] — predecessor.
- [[gaussian-reference-state-parent-origin-sources-2026]] — OU/Lyapunov источники.
- [[live-formulas-gates-version9-35]] — формулы гейта.
- [[current-status-and-next-vectors]] — актуальный фронтир.

## Source Notes

- `s2t/gates/version9_physical_reopening_gaussian_reference_state_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_physical_reopening_gaussian_reference_state_parent_origin_gate.py`
- `s2t/results/s2t_v9_physical_reopening_gaussian_reference_state_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_gaussian_reference_state_parent_origin.py`