# Admission общего carrier двух physical-origin пакетов

> Status: mature
> Type: question
> Updated: 2026-09-01

## Summary

Один positive Gaussian covariance operator dimension `10` условно несёт
scale/coupling и logdet packages. Его spectral-entropy parent имеет полный
Hessian, но выбирает лишь отношение `e=E_*/mu`; physical reference scale и
происхождение Gaussian state остаются открыты.

## Key Points

- `Q=diag(e R_theta,e chi^2 R_kappa)`.
- `Tr Q=5e(1+chi^2)`.
- `det Q=e^10 chi^10 det(R_theta)det(R_kappa)`.
- `Phi=Tr Q-log det Q-10` имеет minimum при unit covariance.
- Hessian rank/determinant `6/36`, spectrum строго положителен.
- Common rescaling `(E_*,mu)->(sE_*,s mu)` сохраняет `e`.
- Conditional joint selection `2/2`, physical-origin packages `0/2`.

## Answer

Common-origin carrier архитектурно существует и заменяет два несвязанных
parent-term одним LogDet divergence. Однако он не переоткрывает physical
branch: `E_*=mu` не выводит абсолютную энергию, а unit Gaussian reference
covariance пока не является stationary state существующего microscopic
carrier.

## Links

- [[version9-axiom-augmented-physical-origin-reopening-criterion-gate]] — predecessor.
- [[physical-reopening-common-origin-carrier-sources-2026]] — источники и интерпретация.
- [[live-formulas-gates-version9-34]] — формулы гейта.
- [[current-status-and-next-vectors]] — актуальный фронтир.

## Source Notes

- `s2t/gates/version9_physical_reopening_common_origin_carrier_admission_gate.tex`
- `s2t/audits/s2t_v9_physical_reopening_common_origin_carrier_admission_gate.py`
- `s2t/results/s2t_v9_physical_reopening_common_origin_carrier_admission_gate_results.json`
- `s2t/proofdsl/examples/version9_physical_reopening_common_origin_carrier.py`