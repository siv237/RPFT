# Источники общего carrier для physical reopening

> Status: mature
> Type: source
> Updated: 2026-09-01

## Summary

LogDet divergence `Tr Q-log det Q-n` является удвоенной относительной
энтропией centered Gaussian covariance `Q` относительно unit covariance.
Это даёт source-free математический parent, но одновременно выявляет
необходимость физически вывести reference covariance и её масштаб.

## Key Points

- Gaussian relative entropy связывает trace и log determinant одного
  positive covariance operator.
- Два KMS type-block минимально требуют covariance dimension `10`.
- Unit reference covariance выбирает dimensionless `e=1`, а не абсолютный
  `E_*` без independently заданного `mu`.
- Existing endpoint QMS не содержит автоматически Gaussian covariance
  state на новом десятимёрном carrier.

## Links

- [[version9-physical-reopening-common-origin-carrier-admission-gate]]
- [[version9-axiom-augmented-physical-origin-reopening-criterion-gate]]
- [[kms-logdet-measure-origin-sources-2026]]
- [[kms-reservoir-spectral-density-sources-2026]]

## Source Notes

- L. Lami, C. Hirche, G. Adesso, A. Winter, “From log-determinant
  inequalities to Gaussian entanglement via recoverability theory”,
  arXiv:1703.06149. The paper records
  `D(p_A||p_B)=1/2[log(det B/det A)+Tr(B^{-1}A)-n]`.
- `s2t/gates/version9_physical_reopening_common_origin_carrier_admission_gate.tex`
- `s2t/results/s2t_v9_physical_reopening_common_origin_carrier_admission_gate_results.json`