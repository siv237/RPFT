# Минимальный invariant parent relative-shape sources

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Построить source-free invariant parent, который выбирает четыре sources
minimal KMS shape selector без component-wise seed.

## Search for solution

- Shapes подняты в positive type-operators `diag(r_s,r_a,r_t I3)`.
- При `Tr R=5` использован общий barrier `-log det R`.
- Weighted AM–GM выбирает единственный isotropic operator `I5`.
- В log-ratio chart barrier индуцирует source `(1,1)` на каждую копию.
- Algebraic core перенесён в ProofDSL как `GateSpec` с 10 обязательствами.

## Expected result

Один invariant term должен условно выбрать source-package `4/4`, сохранив
границу между архитектурой logdet и физическим происхождением этого term.

## Compliance check

- Selected source `q=(1,1,1,1)`; shapes `r_theta=r_kappa=(1,1,1)`.
- Constrained Hessian spectrum `{1,5/3}`, doubled rank/determinant `4/(25/9)`.
- Common Hessian rank/determinant `12/(5184/25)`.
- ProofDSL `10/10`, status `lcf-checked`; registry `49/372`.
- Global AM–GM lemma остаётся вне текущего kernel.
- Logdet parent-origin `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_relative_shape_logdet_parent_measure_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-relative-shape-selector-source-parent-origin-gate]]
- [[version9-endpoint-creation-kms-relative-shape-minimal-selector-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_relative_shape_selector_source_minimal_invariant_parent_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_relative_shape_selector_source_minimal_invariant_parent_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_relative_shape_selector_source_minimal_invariant_parent_architecture_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_relative_shape_invariant_parent.py`