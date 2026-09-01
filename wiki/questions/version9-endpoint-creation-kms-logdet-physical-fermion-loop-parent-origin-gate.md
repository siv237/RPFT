# Parent-origin physical fermion loop для KMS logdet

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Проверить, может ли target `-log det R_theta-log det R_kappa` возникнуть
из однопетлевого determinant уже существующих физических endpoint-fermions.

## Search for solution

- Physical target creation-cell имеет одну multiplet dimension `5=1+1+3`.
- Один homogeneous linear fermion kernel имеет scaling degree `5`, target —
  degree `10`.
- Проверено KO6/Real doubling: Pfaffian half-count возвращает один
  determinant, а independent packages нарушают Real exchange с rank `10`.
- Две multiplets дают `R_theta direct_sum R_kappa`, но требуют новую
  physical copy.
- Один composite kernel `R_theta R_kappa` даёт target, но содержит
  target-loaded mixed coupling.
- Conductances являются dissipative rates, а не eigenvalues существующего
  Hamiltonian fermion bilinear.

## Expected result

Physical loop должен воспроизвести оба independent determinants без новой
species, без нарушения Real structure и без вставки product kernel вручную.

## Compliance check

- Physical target carrier `5/5`.
- Independent determinant capacity `1/2`.
- Conditional algebraic routes существуют, physical origin отсутствует.
- Candidate parent-origin `0/6`; physical logdet parent `0/1`.
- ProofDSL `11/11`, registry `56/443`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-minimal-stueckelberg-shift-parent-architecture-gate]]
- [[kms-physical-fermion-loop-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_physical_fermion_loop_parent_origin_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_physical_fermion_loop_parent_origin_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_physical_fermion_loop_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_physical_fermion_loop_origin.py`