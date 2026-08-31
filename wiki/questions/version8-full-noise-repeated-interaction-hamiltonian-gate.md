# Полный шумовой repeated-interaction Hamiltonian

> Status: working
> Type: question
> Updated: 2026-08-30

## Summary

Для полного 42-jump кадра построен структурный звёздный Hamiltonian на
`C21 tensor C43 = C903`. Среда размерности 43 минимальна: vacuum плюс 42
независимых шумовых направления. Проверены 504 gauge-коммутаторных
включения, GKSL-касательная и collision-limit.

## Problem

Дать полному примитивному QMS явную unitary микрореализацию.

## Search for solution

- Использована vacuum-to-jump star-конструкция.
- Проверены независимость и gauge closure полного frame.
- Минимальность доказана рангом 42.

## Expected result

Repeated interactions должны возвращать `exp(u L_42)` при `h=u/n`.

## Compliance check

- Dimensions: `21/42/43/903`.
- Gauge checks: `504`.
- Реестр: `21/140`; тесты: `31 passed`.
- Fresh ancilla source и физический масштаб не выведены.

## Links

- [[version8-full-noise-42-jump-gksl-fixed-algebra-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-microscopic-repeated-interaction-hamiltonian-gate]]

## Source Notes

- `s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex`
- `s2t/audits/s2t_v8_full_noise_repeated_interaction_hamiltonian_gate.py`
- `s2t/results/s2t_v8_full_noise_repeated_interaction_hamiltonian_gate_results.json`