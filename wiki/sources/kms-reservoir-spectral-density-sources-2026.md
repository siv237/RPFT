# Источники reservoir spectral density для KMS logdet

> Status: mature
> Type: source
> Updated: 2026-09-01

## Summary

Weak-coupling rates считывают bath correlations на Bohr frequencies, тогда
как influence functional и self-energy зависят от полного frequency
profile. Поэтому конечный набор rates не восстанавливает reservoir
spectral density без дополнительного model class или sum rules.

## Key Points

- On-shell evaluation в трёх gaps имеет большое kernel уже в конечном
  polynomial class.
- Positive off-shell deformation может сохранять все три rates.
- Разные spectral moments меняют high-frequency self-energy expansion.
- Type covariance оставляет independent strengths трёх channel types;
  одна normalization не устраняет две relative freedoms.

## Links

- [[version9-endpoint-creation-kms-logdet-reservoir-spectral-density-parent-origin-gate]]
- [[kms-keldysh-influence-functional-sources-2026]]
- [[endpoint-kms-parameter-origin-sources-2026]]

## Source Notes

- E. B. Davies, *Markovian master equations*, Commun. Math. Phys. 39
  (1974) 91--110.
- A. Nüsseler et al., `arXiv:1909.09589`.
- `s2t/gates/version9_endpoint_creation_kms_logdet_reservoir_spectral_density_parent_origin_gate.tex`