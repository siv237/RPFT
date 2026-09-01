# Происхождение invariant logdet parent из меры

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Проверить, выводится ли term
`-log det R_theta-log det R_kappa` из меры уже существующего four-slot
carrier.

## Search for solution

- Сопоставлены flat, real/complex bosonic, complex fermionic,
  Majorana/Pfaffian, coordinate-Jacobian и ghost candidates.
- Формула Березина даёт правильный знак:
  `Z_F(R)=det R`, `S_eff=-log det R`.
- Степень `det R=r_s r_a r_t^3` равна `5`; две независимые copies требуют
  minimal block dimension `5+5=10`.
- Coordinate Jacobian вычислен точно:
  `J=(3/5)r_s r_a r_t`, поэтому он отличается от target determinant
  непостоянным множителем `(5/3)r_t^2`.
- Algebraic core перенесён в ProofDSL как десять обязательств.

## Expected result

Должен быть найден минимальный measure mechanism либо доказано, что
существующая мера его не содержит.

## Compliance check

- Correct conditional mechanism: complex fermionic Gaussian, `1/1`.
- Measure candidates: `1/7`.
- Minimal auxiliary dimension: `10` complex Grassmann-пар.
- ProofDSL `10/10`, registry `50/382`.
- Gaussian/Berezin integral identities явно оставлены вне kernel.
- Typed odd auxiliary module в текущем carrier отсутствует; inherited
  measure-origin `0/1`, physical parent `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate`.

## Links

- [[version9-endpoint-creation-kms-relative-shape-selector-source-minimal-invariant-parent-architecture-gate]]
- [[kms-logdet-measure-origin-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_logdet_measure_origin.py`