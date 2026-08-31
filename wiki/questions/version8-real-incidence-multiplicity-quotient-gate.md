# Real-кратностный quotient incidence-блока

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Real-структура не снимает неоднозначность `4 incidence + 4 heavy`. Она
обменивает ориентированный transfer-модуль с противоположной сопряжённой
половиной, а на удвоенном носителе совместима с непрерывной орбитой
gauge-инвариантных проекторов ранга четыре.

## Problem

Проверить, выбирает ли Real-самосопряжённость incidence-копию внутри
восьмимерного вырожденного блока.

## Search for solution

- Сопоставлены типы `10x11` и `11x10` двух ориентаций.
- Построен Real-удвоенный блок и его неподвижная вещественная часть.
- Вычислен gauge-коммутант вырожденного блока.
- Построена непрерывная орбита проекторов, смешивающая incidence и heavy.
- Проверены gauge-, Real-совместимость и физический полуслед.

## Expected result

Успех требовал единственного Real-совместимого проектора ранга четыре или
уменьшения физической размерности, устраняющего одну из копий.

## Compliance check

- Ориентированный модуль: `15 complex = 30 real`.
- Real-неподвижная часть удвоения: также `30 real`.
- Коммутант блока `4+4`: `10 complex`.
- При `theta=1.5` расстояние между допустимыми проекторами: `1.36328`.
- Gauge-остатки всей орбиты: `<1.5e-15`.
- Real-остатки: `0`.
- Полуслед действует на обе копии одинаково.
- Два запуска дали одинаковый SHA-256
  `5141307cc9460ff1121e3c69f6d780762be5e23b984753f584c3453f91246e13`.

## Key Points

- Real меняет ориентацию стрелки, но не выбирает её multiplicity-копию.
- Самосопряжённое завершение не делит число физических параметров пополам.
- Все проекторы орбиты одинаково допустимы по gauge и Real.
- Следующий возможный селектор должен использовать полные бимодульные метки.

## Links

- [[version8-gauge-closed-edge-hodge-origin-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version7-affine-hodge-copy-selector-no-go-gate]]
- [[version8-physical-arrow-endpoint-intertwiner-classification-gate]]

## Source Notes

- `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex`
- `s2t/audits/s2t_v8_real_incidence_multiplicity_quotient_gate.py`
- `s2t/results/s2t_v8_real_incidence_multiplicity_quotient_gate_results.json`