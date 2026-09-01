# Минимальный BRST complex для KMS logdet

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Построить минимальный BRST complex, который структурно назначает ghost
variables нечётность и воспроизводит determinant двух KMS type-operators,
не меняя физическую когомологию.

## Search for solution

- На base-space `E=V_type tensor P_KMS`, dimension `10`, введён quartet
  `(x,b|c,bar_c)` dimensions `(20|20)`.
- Differential задан как `s x=c`, `s c=0`, `s bar_c=b`, `s b=0`.
- Exact matrix имеет `Q^2=0`, rank/nullity `20/20` и zero cohomology.
- Gauge-fixing fermion:
  `Psi=bar_c^T(D_aux x-alpha b/2)`.
- FP operator `D_aux=R_theta direct sum R_kappa` имеет rank `10` и
  determinant `det R_theta det R_kappa`.
- BRST block действует тривиально на physical creation-cell.

## Expected result

Contractible quartet должен дать required Grassmann statistics и determinant
без новых physical states, сохраняя origin самой gauge redundancy отдельным.

## Compliance check

- Minimal BRST architecture `10/10`.
- Even/odd dimensions `20/20`, superdimension `0`.
- `Q^2=0`, rank/nullity `20/20`, cohomology dimension `0`.
- Conditional FP determinant `1/1`.
- Physical state increment `0`.
- ProofDSL `10/10`, registry `53/412`.
- Shift gauge-symmetry origin `0/1`; physical logdet parent `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_brst_shift_symmetry_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-statistics-parent-origin-gate]]
- [[kms-minimal-brst-complex-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_minimal_brst_complex.py`