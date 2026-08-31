# Бимодульный селектор кратности и расширение полного поля

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Полные endpoint-метки снимают барьер `4+4`, но требуют расширить transfer-
поле с `15` до `20 complex`. Новый модуль раскладывается как
`10 incidence + 10 heavy`; общий Hodge-уровень фиксирует равные edge-массы
и даёт переход `(20,0,20) -> (0,0,40)` при `beta<2/3`.

## Problem

Проверить, различают ли полные левые и правые бимодульные метки incidence-
и heavy-копии до выбора вакуумных амплитуд.

## Search for solution

- Применены все endpoint-проекторы к 15D transfer-модулю.
- Построено минимальное бимодульное и повторное gauge-замыкание.
- Разложены все ненулевые пары `(target,source)`.
- Построен структурный incidence-проектор из baseline и изотипических пар.
- Проверен единый Hodge-уровень и полный 40D гессиан.

## Expected result

Успех требовал селектора, не использующего вакуумные амплитуды, и единой
edge-Hodge метрики на полном замкнутом модуле.

## Compliance check

- Старый модуль: `15 complex`, максимальная block-leakage `0.429699`.
- Минимальное бимодульное замыкание: `20 complex`.
- Повторное gauge-замыкание: `20 -> 20`.
- Incidence/heavy: `10+10 complex`, пересечение нулевое.
- Полный внутренний field space: `52 real`.
- Общий уровень: edge-массы `-4/+4` в нуле.
- Критический вес: `beta*=2/3`.
- При `beta=1/2`: `(20,0,20) -> (0,0,40)`, щель `5.773318`.
- Два запуска дали одинаковый SHA-256
  `9d17a4dbd27861484f51073568c59cc751de8dde7cd8e258008e2cc13580c288`.

## Key Points

- Бимодульная типизация успешно различает копии, невидимые gauge и Real.
- Цена — пять дополнительных комплексных transfer-компонент.
- Новых фермионных endpoint-состояний и gauge-генераторов нет.
- Относительная edge-метрика замкнута одним уровнем.
- Вес между edge-Hodge и Gram-кривизнами остаётся открытым.

## Links

- [[version8-real-incidence-multiplicity-quotient-gate]]
- [[version8-gauge-closed-edge-hodge-origin-gate]]
- [[version7-rooted-cycle-isotypic-edge-projector-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]

## Source Notes

- `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex`
- `s2t/audits/s2t_v8_bimodule_multiplicity_separator_gate.py`
- `s2t/results/s2t_v8_bimodule_multiplicity_separator_gate_results.json`