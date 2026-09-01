# Источники auxiliary fermion module для KMS logdet

> Status: mature
> Type: source
> Updated: 2026-08-31

## Summary

Grassmann/Berezin variables естественно живут в нечётной части graded
configuration space. Ghost-like auxiliary carrier может порождать
determinant, не добавляя состояния в физическое QMS-пространство, однако
его нечётность должна иметь отдельное BRST/BV или иное структурное
происхождение.

## Key Points

- Parity shift `Pi V` меняет статистический тип носителя, но не его
  complex dimension.
- Complex fermionic Gaussian требует пары `psi,bar(psi)`: module
  dimension `10` соответствует `20` odd integration coordinates.
- Physical state-space определяется отдельно от auxiliary graded variables.
- Functorial tensor product существующих type/package spaces не выводит
  Grassmann parity автоматически.

## Links

- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-module-admission-gate]]
- [[kms-logdet-measure-origin-sources-2026]]

## Source Notes

- G. Grensing, M. Nitschmann, *Berezin integration over anticommuting
  variables and cyclic cohomology*, arXiv:hep-th/0401231.
- M. Henneaux, C. Teitelboim, *Quantization of Gauge Systems*, 1992.
- `s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_module_admission_gate.tex`