# Гладкий относительный параметр порядка и изотипическая лазейка

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Полярный скачок не является единственным маршрутом. Кварк-лептонные
градуировки задают гладкий gauge-ковариантный параметр
`B(A)=Gamma_t A-A Gamma_s` и ненулевую относительную кривизну. Но её действие
имеет степень шесть, поэтому исходный гессиан равен нулю: кандидат укрепляет
вакуум, но не запускает переход.

## Problem

Проверить, существует ли гладкая полиномиальная замена moving polar,
определённая одновременно в `A=0` и на физическом вакууме.

## Search for solution

- Проверены естественные функции `A f(A* A)`; их relative-кривизна исчезает
  по ассоциативности.
- Использованы уже выведенные кварк-лептонные endpoint-проекторы.
- Построено эквивариантное отображение `B(A)=Gamma_t A-A Gamma_s`.
- Вычислены коммутант, ранг отображения, конечная gauge-ковариантность,
  радиальная степень и вакуумный гессиан.

## Expected result

Гладкий кандидат должен давать ненулевую relative-кривизну без нового поля.
Для полного успеха он также должен воспроизвести исходный запуск и быть
однозначно выбран архитектурой.

## Compliance check

- Transfer-модуль: `15 complex`.
- Эквивариантный коммутант: `13`.
- Ранг `B`: `6 complex`; ядро: `9 complex`.
- Остаток полной gauge-ковариантности: `<2.1e-14`.
- Норма relative-кривизны на пробах: `7.15..36.95`.
- `S_B(tA)=t^6 S_B(A)`.
- Гессиан в нуле: `0`.
- Вакуумный гессиан на `30 real`: ранг `12`, нульность `18`, положительные
  собственные значения `12 x6` и `16 x6`.
- Два запуска дали одинаковый SHA-256
  `5532037f9461f0ff4804aed04abc0ddc5d74afb2036c1bb5e1d47500414f6ecf`.

## Key Points

- Найден первый гладкий ненулевой relative-механизм на полном field space.
- Он опирается на физическое изотипическое разложение, а не на сглаженный
  polar.
- Он может стабилизировать 12 вакуумных направлений.
- Он не создаёт отрицательных мод в исходном нуле.
- Gauge-ковариантность не обеспечивает единственность: коммутант имеет
  размерность 13.

## Links

- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[version8-markov-fixed-algebra-selector-gate]]
- [[version8-unified-field-space-project-intuition-search]]
- [[superconnection-curvature-and-polar-strata-literature-2026]]

## Source Notes

- `s2t/gates/version8_smooth_relative_background_order_parameter_gate.tex`
- `s2t/audits/s2t_v8_smooth_relative_background_order_parameter_gate.py`
- `s2t/results/s2t_v8_smooth_relative_background_order_parameter_gate_results.json`