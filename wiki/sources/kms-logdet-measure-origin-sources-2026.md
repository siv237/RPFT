# Источники происхождения logdet-меры KMS parent

> Status: mature
> Type: source
> Updated: 2026-08-31

## Summary

Конечномерные Gaussian-интегралы различают знак determinant-term:
bosonic integration порождает положительный `+log det` в effective action,
а complex Grassmann/Berezin integration — требуемый `-log det`.

## Key Points

- Для complex boson `Z_B proportional (det R)^(-1)`.
- Для complex fermion `Z_F=det R`.
- Majorana/Pfaffian даёт половинный logdet coefficient.
- В type-space `1+1+3` determinant имеет степень пять; две KMS copies
  требуют десять complex Grassmann-пар в минимальной linear realization.
- Это механизм представления, а не доказательство наличия auxiliary fields
  в исходном four-slot carrier.

## Links

- [[version9-endpoint-creation-kms-relative-shape-logdet-parent-measure-origin-gate]]
- [[version9-endpoint-creation-kms-relative-shape-selector-source-minimal-invariant-parent-architecture-gate]]

## Source Notes

- F. A. Berezin, *The Method of Second Quantization*, Academic Press, 1966.
- `s2t/gates/version9_endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate.tex`
- `s2t/proofdsl/examples/version9_kms_logdet_measure_origin.py`