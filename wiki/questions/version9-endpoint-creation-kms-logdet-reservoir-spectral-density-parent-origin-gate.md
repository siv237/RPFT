# Parent-origin reservoir spectral density для KMS logdet

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Определяют ли три on-shell conductances полный reservoir profile,
off-shell self-energy и bath logdet.

## Search for solution

- Построен evaluation map полиномов степени `<=6` в gaps `(1,2,3)`.
- Сравнены positive profiles `J0=1` и
  `J1=1+(omega-1)^2(omega-2)^2(omega-3)^2/16`.
- Проверены on-shell rates, два spectral moments и self-energy asymptotics.
- Algebraic core перенесён в ProofDSL.

## Expected result

Одинаковые rates должны единственно фиксировать spectral density и
соответствующий determinant functional.

## Compliance check

- Evaluation rank/nullity `3/4`.
- Оба rate vector равны `(1,1,1)`.
- Zeroth/first moment defects: `107/105`, `214/105`.
- Rate normalization оставляет две relative type-strength freedoms.
- Unique spectral density `0/1`, rates determine logdet `0/1`.
- ProofDSL `12/12`, registry `59/480`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_reservoir_measure_anomaly_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-keldysh-influence-functional-admission-gate]]
- [[kms-reservoir-spectral-density-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_reservoir_spectral_density_origin.py`