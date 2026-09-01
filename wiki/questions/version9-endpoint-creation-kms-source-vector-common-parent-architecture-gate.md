# Общий source-parent KMS-параметров

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Построить один bounded parent, условно выбирающий три KMS-gap и три
conductance, не выдавая source-covectors за уже выведенные данные.

## Search for solution

- Введён шестимерный source-carrier из двух type-covectors.
- Использована multiplicity metric `diag(1,1,3)`.
- KMS-часть объединена с существующим four-slot functional.
- Проверены точный минимум и общий continuous Hessian.

## Expected result

Архитектура должна быть строго выпуклой, сохранять старый `S4` как
restriction и выбирать положительные KMS-параметры при positive sources.

## Compliance check

- Architecture `9/9`, conditional KMS selection `6/6`.
- Common Hessian rank/determinant `8/576`.
- Exact minimum: `theta=(1,2,3)`, `kappa=(2,1,2)`.
- Source-package origin `0/2`, component origin `0/6`.
- Следующий гейт: `version9_endpoint_creation_kms_source_covector_four_slot_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-gap-conductance-parent-origin-gate]]
- [[tome9-opening-contract]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_source_vector_common_parent_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_source_vector_common_parent_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_source_vector_common_parent_architecture_gate_results.json`