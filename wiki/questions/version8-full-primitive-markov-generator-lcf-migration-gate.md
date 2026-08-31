# Точная LCF-сборка полного примитивного Markov-генератора

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Полный процесс из 25 самосопряжённых jump-операторов перенесён в LCF-слой.
Его неподвижная алгебра скалярна для всех строго положительных весов, но
следовая обратимость не выбирает метрику скоростей.

## Problem

Заменить численный scan 48 наборов весов точным доказательством
примитивности всего положительного конуса.

## Search for solution

- Все шесть семейств собраны одним типизированным GKSL-конструктором.
- Проверены след, единица и полный endpoint-базис.
- Использовано пересечение базовой `C^2` с одномерным cross-ядром.
- Положительная сумма квадратов коммутаторов заменяет случайный scan.

## Expected result

Качественная примитивность должна стать строгой, а относительные и
абсолютная скорости должны остаться открытыми.

## Compliance check

- `25=1+8+3+1+6+6` самосопряжённых jump-операторов.
- Проверены `221` endpoint-единица.
- `Fix(L_full)=C I21`; QLYR и XLdR замыкают `C^2` также по отдельности.
- Для всех шести `kappa_r>0` ядро одномерно и щель строго положительна.
- Trace detailed balance выполняется посемейно и не выбирает веса.

## Links

- [[version8-full-primitive-markov-generator-assembly-gate]]
- [[version8-intrinsic-noise-clock-lcf-migration-gate]]
- [[version8-kms-nontracial-relative-rate-selector-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]

## Source Notes

- `s2t/gates/version8_full_primitive_markov_generator_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_full_primitive_markov_generator_lcf_migration_gate.py`
- `s2t/results/s2t_v8_full_primitive_markov_generator_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_full_primitive.py`