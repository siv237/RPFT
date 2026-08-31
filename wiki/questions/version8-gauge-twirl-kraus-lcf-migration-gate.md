# Точная LCF-проверка gauge-twirl Kraus-моста

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Численная gauge-twirl проверка заменена точным сертификатом. Все `12`
межсекторных jump-направлений замкнуты под `12` генераторами
`SU(3) x SU(2) x U(1)`, линейных инвариантов нет, но квадратичный
GKSL-генератор сокращает центральную `C^2` до единицы.

## Problem

Проверить, не был ли положительный результат исходного Kraus-гейта
артефактом случайных gauge-преобразований и сканирования 64 скоростей.

## Search for solution

- Физические `QLYR`- и `XLdR`-стрелки восстановлены точными матрицами.
- Их вещественные и мнимые части подняты в 12 самосопряжённых jump-
  операторов на `C^21`.
- Для восьми генераторов `su(3)`, трёх `su(2)` и гиперзаряда проверено
  точное замыкание рамки и кососимметричность индуцированного действия.
- Независимость квадратичной суммы от ортогонального Kraus-базиса доказана
  общим правилом равных скоростей.
- Ограничение на `P_q/sqrt(12), P_l/3` вычислено символически.

## Expected result

Положительный межсекторный мост должен сохраняться без floating-point и
случайной выборки, но его динамическая скорость и parent-action не должны
объявляться выведенными.

## Compliance check

- Вещественная jump-размерность: `12`.
- Точных gauge-генераторов: `12`.
- Остаток замыкания: ноль; матрицы действия кососимметричны.
- Размерность линейного gauge-синглета: `0`.
- Центральная матрица: `[[1,-2/sqrt(3)],[-2/sqrt(3),4/3]]`.
- Характеристический многочлен: `lambda(lambda-7/3)`; ядро `1`.
- Для символических `gamma_QLYR,gamma_XLdR>0` ядро остаётся `1`.
- Parent-action, его гессиан и значения скоростей остаются открытыми.

## Links

- [[version8-gauge-twirl-cross-sector-kraus-bridge-gate]]
- [[version8-linking-qms-gksl-lcf-migration-gate]]
- [[version8-kraus-bridge-parent-action-hessian-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_gauge_twirl_kraus_lcf_migration_gate.py`
- `s2t/results/s2t_v8_gauge_twirl_kraus_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_gauge_twirl_kraus.py`