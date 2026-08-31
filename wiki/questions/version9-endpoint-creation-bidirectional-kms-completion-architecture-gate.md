# Bidirectional KMS completion creation-frame

> Status: mature
> Type: question
> Updated: 2026-08-31

## Problem

Можно ли минимально дополнить outward-only creation-frame так, чтобы получить
primitive quantum Markov generator с faithful stationary state?

## Search for solution

- Введены три symmetry-compatible energy gaps.
- Каждый creator дополнен reverse jump.
- Forward/reverse rates связаны KMS-отношением через Boltzmann ratios.
- Точно вычислены generated algebra, Liouvillian rank и stationary state.

## Expected result

Bidirectional frame должна порождать полную матричную алгебру, иметь
одномерное стационарное ядро и отделять архитектурное закрытие от
происхождения физических параметров.

## Compliance check

- Пять bidirectional channel pairs порождают `M6(C)`.
- Architecture `10/10`, primitive closure `1/1`.
- Exact witness: Liouvillian rank/nullity `35/1`.
- Faithful stationary state `diag(12,6,4,3,3,3)/31`.
- KMS parameter origin `0/6`: три gap и три conductance не выбраны.
- Следующий гейт: `version9_endpoint_creation_kms_gap_conductance_parent_origin_gate`.

## Links

- [[version9-endpoint-finite-geometry-creation-operator-parent-origin-gate]]
- [[endpoint-bidirectional-kms-sources-2026]]
- [[tome9-opening-contract]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_bidirectional_kms_completion_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_bidirectional_kms_completion_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_bidirectional_kms_completion_architecture_gate_results.json`