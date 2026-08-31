# Полный 42-jump GKSL

> Status: working
> Type: question
> Updated: 2026-08-30

## Summary

Полный 42-мерный Hermitian frame задаёт унитальный сохраняющий след GKSL-
процесс. Прежний 25-jump span содержится в нём, поэтому неподвижная алгебра
остаётся `C I_21`, а процесс примитивен. Обратимое trace-dual whitening не
изменяет коммутант.

## Problem

Проверить динамическую состоятельность полного field-dual noise frame.

## Search for solution

- Собран 42-jump Lindblad generator.
- Проверены trace, unit, endpoint-алгебра и включение старого span.
- Применена монотонность коммутанта форм Дирихле.

## Expected result

Добавление 17 направлений не должно разрушать примитивность.

## Compliance check

- Jumps: `42`; base: `25`; added: `17`.
- `Fix=C I_21`; primitive: yes.
- Реестр: `20/134`; тесты: `30 passed`.
- Физическая rate-метрика, время и fresh ancilla открыты.

## Links

- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-full-primitive-markov-generator-lcf-migration-gate]]
- [[version8-metric-dual-environment-parent-action-origin-gate]]

## Source Notes

- `s2t/gates/version8_full_noise_42_jump_gksl_fixed_algebra_gate.tex`
- `s2t/audits/s2t_v8_full_noise_42_jump_gksl_fixed_algebra_gate.py`
- `s2t/results/s2t_v8_full_noise_42_jump_gksl_fixed_algebra_gate_results.json`