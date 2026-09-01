# Источники минимальной fermion-bath архитектуры

> Status: mature
> Type: source
> Updated: 2026-09-01

## Summary

Fermionic bath после интегрирования создаёт system self-energy, выраженную
Schur complement. Для текущего KMS target Hermitian interaction меняет
product determinant; exact factorization остаётся только на decoupled face.

## Key Points

- Минимальная bath, повторяющая channel types `1+1+3`, имеет dimension `5`.
- Hermitian system--bath coupling создаёт self-energy
  `G R_bath^-1 G^dagger`.
- Nonzero coupling меняет determinant через Schur complement.
- Block-triangular retarded/advanced kernels требуют полного Keldysh
  doubling, noise block и normalization identities.
- Разведка следующего шага показала, что decisive test относится к
  normalized influence functional: identity `Z_SK[J,J]=1` может удалить
  именно тот vacuum determinant, который формально сохраняет triangular
  block.
- Наличие finite bath carrier ещё не доказывает Markovian limit или
  происхождение трёх conductance components.

## Links

- [[version9-endpoint-creation-kms-logdet-minimal-fermion-bath-architecture-gate]]
- [[kms-physical-fermion-loop-sources-2026]]
- [[endpoint-kms-parameter-origin-sources-2026]]
- [[kms-keldysh-next-gate-reconnaissance-2026]]

## Source Notes

- A. Nüsseler et al., `arXiv:1909.09589`.
- A. Kamenev, A. Levchenko, `arXiv:0901.3586`.
- A. McDonald, A. A. Clerk, `arXiv:2302.14047`.
- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate.tex`