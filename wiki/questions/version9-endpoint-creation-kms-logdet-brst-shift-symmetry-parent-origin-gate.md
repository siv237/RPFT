# Parent-origin BRST shift-symmetry

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, существует ли в inherited four-slot parent десятипараметрическая
gauge orbit `x -> x+epsilon`, необходимая для minimal BRST complex.

## Search for solution

- Required generator-map `I10` имеет rank `10`.
- Tangent всех шести KMS type-parameters имеет rank `6` и cokernel `4`.
- Normalized relative shapes имеют rank `4`.
- Endpoint phase graph даёт одну zero mode.
- Type/family conjugations scalar blocks и discrete transport имеют
  continuous orbit rank `0`.
- Проверены zero-action spectator extension и positive quadratic parent.

## Expected result

Gauge orbit должна быть либо inherited symmetry общего parent, либо
conditional extension должна быть явно отделена от physical origin.

## Compliance check

- Maximum inherited continuous rank `6<10`; rank deficit `4`.
- Shift-origin candidates `0/6`.
- Conditional flat spectator shift `1/1`, но zero coupling target-loaded.
- Positive Hessian rank `10` разрушает full translation symmetry.
- FP operator origin `1/1`, но gauge orbit origin `0/1`.
- ProofDSL `10/10`, registry `54/422`.
- Physical logdet parent остаётся `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_minimal_stueckelberg_shift_parent_architecture_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-minimal-brst-complex-architecture-gate]]
- [[kms-brst-shift-symmetry-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_brst_shift_symmetry_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_brst_shift_symmetry_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_brst_shift_symmetry_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_brst_shift_symmetry_origin.py`