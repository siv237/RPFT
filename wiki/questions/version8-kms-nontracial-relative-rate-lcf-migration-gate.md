# Точный LCF-запрет нетривиального KMS-селектора

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Примитивный унитальный процесс допускает только состояние `I21/21`.
Нетривиальный центральный KMS-вес не выбирает скорости; направленная модель
лишь переносит свободу в невыведенный параметр `beta_Delta`.

## Problem

Проверить без scan, способен ли KMS detailed balance закрыть метрику шести
скоростей.

## Search for solution

- Использована точная скалярность неподвижной алгебры.
- Получены transfer-следы `13,6,6` и запрет положительной компенсации.
- Тринадцать скачков разложены на точные боровские пары `V,V*`.

## Expected result

Текущий процесс должен принуждать след, а условная направленная формула не
должна объявляться новым выводом.

## Compliance check

- Центральная стационарность: `a=b=1/21`.
- Положительные веса не отменяют transfer-поток.
- `gamma_up/gamma_down=exp(-beta_Delta)` условно; `beta_Delta` свободно.

## Links

- [[version8-kms-nontracial-relative-rate-selector-gate]]
- [[version8-full-primitive-markov-generator-lcf-migration-gate]]
- [[version8-modular-bohr-parent-origin-gate]]

## Source Notes

- `s2t/gates/version8_kms_nontracial_relative_rate_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_kms_nontracial_relative_rate_lcf_migration_gate.py`
- `s2t/results/s2t_v8_kms_nontracial_relative_rate_lcf_migration_gate_results.json`