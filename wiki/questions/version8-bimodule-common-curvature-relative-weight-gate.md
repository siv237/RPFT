# Общая бимодульная кривизна и относительный Gram-вес

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Незавешенный общий след edge-Hodge и endpoint-Gram кривизн даёт
`beta=1`, который проваливает исходный селектор. Real-полуслед отношения не
меняет, а любой gauge-ковариантный линейный коннектор `21 -> 20` имеет ранг
не выше `9`. Поэтому рабочее `beta=1/2` пока остаётся недовыведенным.

## Problem

Проверить, устраняет ли одна общая бимодульная кривизна последний
относительный вес между edge- и Gram-частями действия.

## Search for solution

- Построены Real-завершённая edge-кривизна размерности `40` и endpoint-Gram
  кривизна размерности `21`.
- Сверены обычный след, Real-удвоение и физический полуслед.
- Решена полная система интертвинеров между endpoint-представлением `21` и
  transfer-представлением `20` для двенадцати gauge-генераторов.
- Проверены центральные проекторы общего носителя и сигнатуры при
  `beta=1/2, 2/3, 1`.

## Expected result

Успех требовал либо внутреннего появления коэффициента `1/sqrt(2)` перед
Gram-кривизной, либо ковариантного коннектора полного ранга, уничтожающего
независимость двух центральных проекторов.

## Compliance check

- Общий носитель: `40+21=61`.
- Незавешенный след: точно `S_E+S_G`, то есть `beta=1`.
- Real-полуслед: отношение не меняет.
- Пространство интертвинеров: `13 complex`.
- Общий endpoint-coimage всех интертвинеров: ранг `9`; полный ранг `20`
  невозможен.
- При `beta=1/2`: исходная сигнатура `(20,0,20)`.
- При `beta=1`: исходная сигнатура `(38,0,2)`.

## Key Points

- Близость размерностей `20` и `21` не создаёт индекс-один мост.
- Запись `Omega_G/sqrt(2)` является параметризацией желаемого ответа, а не
  его выводом.
- Следующий допустимый маршрут должен быть нелинейным или цепным и выводить
  incidence-boundary коннектор из самой суперсвязности.

## Links

- [[version8-bimodule-multiplicity-separator-gate]]
- [[version8-real-incidence-multiplicity-quotient-gate]]
- [[version7-common-chain-number-hodge-relative-trace-gate]]
- [[version7-common-irreducible-trace-multiplicity-gate]]

## Source Notes

- `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex`
- `s2t/audits/s2t_v8_bimodule_common_curvature_relative_weight_gate.py`
- `s2t/results/s2t_v8_bimodule_common_curvature_relative_weight_gate_results.json`