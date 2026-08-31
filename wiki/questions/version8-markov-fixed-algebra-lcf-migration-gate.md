# Точная LCF-проверка двухсекторной неподвижной алгебры

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Численный результат `dim Fix=2` перепроверен точно. Gauge-коммутант двух
endpoint-углов имеет размерность `13`; полный двусторонний linking-коммутант
имеет ранг системы `11` и нульмерность `2`. Проекторы имеют ранги `12+9`.

## Problem

Устранить зависимость гейта неподвижной алгебры от диагонализации матрицы
`221x221` и численного допуска.

## Search for solution

- Endpoint-представления разложены по точным изотипическим блокам.
- Общий gauge-коммутант параметризован тринадцатью переменными.
- Физическая incidence-матрица восстановлена точно из нулей и единиц.
- Проверены прямое и сопряжённое уравнения коммутанта.
- LCF-ядро проверило базис ядра и дополнительность проекторов.

## Expected result

Точная система должна воспроизвести размерность `2` и ранги `12/9` либо
понизить прежнее численное утверждение.

## Compliance check

- Gauge-коммутант: `13`.
- Только `A X_s = X_t A`: нульмерность `4`.
- Полная система вместе с `X_s A^* = A^* X_t`: форма `220x13`, ранг `11`,
  нульмерность `2`.
- Базис: `P_q`, `P_l`.
- Ранги: `12+9`; проекторы ортогональны и дают единицу.
- Статус: `lcf-checked` без численного допуска.

## Links

- [[version8-markov-fixed-algebra-selector-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_markov_fixed_algebra_lcf_migration_gate.py`
- `s2t/results/s2t_v8_markov_fixed_algebra_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_fixed_algebra.py`