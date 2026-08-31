# Точная LCF-проверка полярной cross-ковариации

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Численный linking-блок восстановлен в точном поле
`Q(sqrt(2),2 cos(pi/7))`. Cross-пространство состоит из шести одинаковых
положительных пар и точно отделено от остальных 15 направлений. Общая ось
выведена, полный эллипс ковариации и его масштаб — нет.

## Problem

Проверить, является ли угол `55.45092°` устойчивой алгебраической
структурой или следствием численной полярной декомпозиции.

## Search for solution

- Физическая матрица `A0:C11->C10` восстановлена из нулей и единиц.
- Обратный квадратный корень её target-Gram матрицы построен спектральными
  проекторами в алгебраическом поле степени 6.
- Полный линейный relative-curvature гессиан вычислен точно.
- Проверены повторение `I6 tensor B`, нулевой блок `12x15`, критерий
  Сильвестра и общий спектральный базис аффинного семейства.
- Для трёх правил меры проверена нетривиальная зависимость от внешнего
  масштаба или времени.

## Expected result

Геометрия должна однозначно задавать cross-ось, но не должна скрыто
устранять свободный `eta` и внешние нормировки меры.

## Compliance check

- Поле коэффициентов имеет степень `6`.
- `UU*=I10` точно.
- Cross-блок: `I6 tensor B`; остаток повторения ноль.
- Связь с другими 15 модами: нулевая матрица `12x15`.
- `B` положительно определена и имеет различные собственные значения.
- Мягкая ось: `55.4509155208...°`, одинакова для всех `eta>0`.
- Анизотропия, классический масштаб, кинетический множитель и тепловое
  время остаются нетривиальными параметрами.

## Links

- [[version8-cross-arrow-covariance-origin-gate]]
- [[version8-kraus-bridge-parent-action-lcf-migration-gate]]
- [[version8-minimal-covariant-stinespring-carrier-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_cross_arrow_covariance_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_cross_arrow_covariance_lcf_migration_gate.py`
- `s2t/results/s2t_v8_cross_arrow_covariance_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_cross_covariance.py`