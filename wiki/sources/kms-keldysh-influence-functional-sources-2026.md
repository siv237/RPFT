# Источники Keldysh influence functional для KMS logdet

> Status: mature
> Type: source
> Updated: 2026-09-01

## Summary

Schwinger--Keldysh doubling даёт causal retarded/advanced/Keldysh
архитектуру и связывает fluctuation с dissipation через KMS/FDT. Однако
closed-time-path functional нормирован как `Z[J,J]=1`, поэтому его vacuum
determinant нельзя автоматически отождествлять с требуемым Euclidean
barrier `-log det R_theta-log det R_kappa`.

## Key Points

- Для fermions в Larkin--Ovchinnikov basis inverse propagator и self-energy
  имеют causal triangular form `pmatrix(R,K;0,A)`; Keldysh/noise block не
  меняет block determinant.
- В equilibrium выполняется fermionic FDT
  `G^K=(G^R-G^A)tanh((omega-mu)/(2T))`; noise и dissipation поэтому не
  являются двумя независимыми packages.
- Нормировка closed contour даёт `Z=1`, а при равных sources —
  `Z[J,J]=1`. Выполненный gate дал exact normalized Gaussian ratio `1` и
  vacuum action `0`.
- Конечный bath создаёт frequency-dependent self-energy. Markovian
  conductance требует reservoir limit, repeated fresh probes или иной
  контролируемый coarse-graining, а не только одну конечную bath-copy.
- Следующий гейт должен проверять полный normalized influence functional,
  а не одну triangular matrix identity.

## Links

- [[kms-keldysh-next-gate-reconnaissance-2026]] — вывод для программы.
- [[version9-endpoint-creation-kms-logdet-keldysh-influence-functional-admission-gate]] —
  выполненный causal/normalization audit.
- [[version9-endpoint-creation-kms-logdet-minimal-fermion-bath-architecture-gate]] — непосредственный predecessor.
- [[kms-minimal-fermion-bath-sources-2026]] — Hermitian Schur obstruction.
- [[kms-physical-fermion-loop-sources-2026]] — determinant-capacity и
  contour doubling.
- [[intrinsic-time-and-repeated-interaction-literature-2026]] —
  microscopic origin Markovian time.

## Source Notes

- A. Kamenev, A. Levchenko, *Keldysh technique and non-linear sigma-model:
  basic principles and applications*, `arXiv:0901.3586`, особенно equations
  (97), (106), (108), (118).
- F. M. Haehl, R. Loganayagam, M. Rangamani, *Schwinger-Keldysh formalism I:
  BRST symmetries and superspace*, `arXiv:1610.01940`.
- S. Attal, Y. Pautrat, *From repeated to continuous quantum interactions*,
  Ann. Henri Poincare 7 (2006) 59--104.
- J.-F. Bougron, A. Joye, C.-A. Pillet, *Markovian Repeated Interaction
  Quantum Systems*, `arXiv:2202.05321`.
- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate.tex`