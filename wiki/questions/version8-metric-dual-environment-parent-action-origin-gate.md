# Происхождение метрически двойственной среды из parent-action

> Status: working
> Type: question
> Updated: 2026-08-30

## Summary

Существующая полевая часть parent-action не выводит метрически двойственную
среду. Точный контрпример даёт две положительные gauge-совместимые
bath-метрики `R_1=I_12/3` и `R_2=diag(I_6/3,2I_6/3)`: они имеют одну
полевую рестрикцию `K_B=3I_12`, но не пропорциональны и порождают разные
редуцированные генераторы. Условие `K_B R=I_12` единственно выбирает `R_1`,
однако является дополнительной Riesz-аксиомой.

## Problem

Проверить, является ли принцип метрически двойственной jump-среды следствием
уже построенного полевого суперследа или самостоятельным предположением.

## Search for solution

- Построены два точных положительных parent-Hessian с одинаковым полевым
  блоком `3I_12`.
- Проверено точное коммутирование обеих bath-метрик с gauge-действием.
- Доказано, что метрики не связаны общим масштабированием.
- Найден matrix-unit `E_(0,8)`, на котором соответствующие GKSL-генераторы
  различаются.
- Проверено, что линейное Riesz-условие `K_B R=I` имеет единственное решение
  `R=K_B^-1`.

## Expected result

Старое действие не должно считаться источником bath-динамики без явного
cotangent/BV-сектора или эквивалентного закона Riesz-взаимности.

## Compliance check

- Положительных неэквивалентных completion: не менее `2`.
- Полевая размерность: `12 real`.
- Одинаковая полевая рестрикция: точно.
- Свидетель разных динамик: `E_(0,8)`.
- LCF-обязательств: `6`.
- Общий реестр: `17` гейтов, `116` обязательств.
- Физический масштаб времени и источник свежих ancilla не выведены.

## Links

- [[version8-trace-dual-cross-interaction-selector-gate]] — условный
  положительный селектор `I_12/3`.
- [[version8-physical-correlation-kernel-parent-action-origin-gate]] — общее
  разделение равновесного гессиана и мобильности.
- [[version8-microscopic-repeated-interaction-hamiltonian-gate]] —
  микроскопический collision-Hamiltonian.
- [[version8-lcf-proofdsl-architecture-gate]] — формальный реестр.

## Source Notes

- `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex`
- `s2t/audits/s2t_v8_metric_dual_environment_parent_action_origin_gate.py`
- `s2t/results/s2t_v8_metric_dual_environment_parent_action_origin_gate_results.json`
- `s2t/proofdsl/examples/version8_metric_dual_environment_parent_action.py`