# Источники minimal BRST complex для KMS logdet

> Status: mature
> Type: source
> Updated: 2026-08-31

## Summary

Contractible BRST doublets позволяют вводить ghost, antighost и auxiliary
multiplier fields без изменения физической когомологии. Gauge-fixing
fermion порождает Faddeev--Popov determinant, если исходная gauge symmetry
и gauge-fixing map заданы независимо.

## Key Points

- Пары `s x=c`, `s c=0` и `s bar_c=b`, `s b=0` образуют
  contractible complex.
- Равенство image и kernel dimensions при nilpotence даёт zero cohomology.
- Ghost determinant задаётся linearization gauge condition вдоль gauge orbit.
- Нельзя выводить gauge redundancy из одного факта существования удобного
  BRST quartet.

## Links

- [[version9-endpoint-creation-kms-logdet-minimal-brst-complex-architecture-gate]]
- [[kms-auxiliary-fermion-statistics-sources-2026]]

## Source Notes

- A. Quadri, *Algebraic Properties of BRST Coupled Doublets*,
  JHEP 05 (2002) 051, arXiv:hep-th/0201122.
- R. A. Iseppi, *The BRST cohomology and a generalized Lie algebra
  cohomology: analysis of a matrix model*, arXiv:1909.05053.
- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_brst_complex_architecture_gate.tex`