# Минимальная fermion-bath архитектура KMS logdet

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Проверить, может ли одна минимальная five-channel fermion bath одновременно
дать недостающий conductance determinant и физически взаимодействовать с
endpoint-system без изменения target logdet.

## Search for solution

- Построен carrier `V_sys direct_sum V_bath` dimension `5+5=10`.
- Введена family-covariant coupling
  `G=diag(g_s,g_a,g_t,g_t,g_t)` rank `5`.
- Coupled determinant вычислен через точный Schur complement.
- Positive witness `R_theta=R_kappa=2I5`, `G=I5` имеет spectrum
  `{1^(5),3^(5)}`, determinant `243` вместо target `1024`.
- При `G=0` target восстанавливается, но system self-energy исчезает.

## Expected result

Минимальный bath должен сохранять target determinant и одновременно
создавать nonzero system self-energy, из которой могут происходить
conductances.

## Compliance check

- Minimal carrier architecture `10/10`, nonzero Hermitian coupling `1/1`.
- Coupled exact target `0/1`; zero-coupling target `1/1`.
- Exact determinant defect `1024-243=781`.
- Physical bath parent-origin `0/1`.
- ProofDSL `12/12`, registry `57/455`.
- Следующий гейт:
  После отдельной разведки формулировка уточнена до
  `version9_endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate`:
  требуется проверить normalized contour, а не только causal triangular
  kernel. См. [[kms-keldysh-next-gate-reconnaissance-2026]].

## Links

- [[version9-endpoint-creation-kms-logdet-physical-fermion-loop-parent-origin-gate]]
- [[kms-minimal-fermion-bath-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_minimal_fermion_bath.py`