# Источники нечётной статистики auxiliary KMS module

> Status: mature
> Type: source
> Updated: 2026-08-31

## Summary

BRST/BV формализм назначает ghost fields нечётность из gauge generators и
nilpotent differential. Одна operator grading физического channel-space
сама по себе не превращает соответствующие координаты в Grassmann variables.

## Key Points

- Operator parity и Grassmann parity являются различными структурами.
- Uniform parity package-lines не исправляет смешанный spectrum physical
  type-grading до purely odd carrier.
- Ghost statistics требует gauge redundancy, ghost number и nilpotent
  differential либо отдельного statistics-parent.
- Для paired complex Grassmann variables dual basis Jacobians сокращаются,
  поэтому orientation не создаёт дополнительный relative selector.

## Links

- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-statistics-parent-origin-gate]]
- [[kms-auxiliary-fermion-module-sources-2026]]

## Source Notes

- G. Barnich, F. Brandt, M. Henneaux, *Local BRST cohomology in gauge
  theories*, Phys. Rept. 338 (2000), arXiv:hep-th/0002245.
- G. Grensing, M. Nitschmann, *Berezin integration over anticommuting
  variables and cyclic cohomology*, arXiv:hep-th/0401231.
- `s2t/gates/version9_endpoint_creation_kms_logdet_auxiliary_fermion_statistics_parent_origin_gate.tex`