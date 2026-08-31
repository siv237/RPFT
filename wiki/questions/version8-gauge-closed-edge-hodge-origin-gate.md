# Происхождение gauge-замкнутого edge-Hodge запуска

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Известные канонические операторы не выводят два веса полного transfer-
гессиана. Gauge-Casimir и кварк-лептонная градуировка оставляют общий блок
ранга восемь, содержащий `4 incidence + 4 heavy` неразличимых комплексных
копии. Общий KMS-след и цепная степень эту кратность не снимают.

## Problem

Вывести отношение `m_I/m_H` из gauge-Casimir, цепной степени, секторной
градуировки или общего следа без вставки готового incidence-проектора.

## Search for solution

- Вычислен полный gauge-Casimir на `T_15`.
- Построен совместный спектр Casimir и секторного оператора `B`.
- Проверена реконструкция `P_I` функциями совместного спектра.
- Проверены trace-, KMS- и полярные endpoint-плотности.
- Проверено множество индексов Морса, доступных спектральными порогами.

## Expected result

Успех требовал канонического оператора, спектральный проектор которого равен
`P_I`, либо единственной следовой метрики с выведенным `m_I/m_H`.

## Compliance check

- `Spec C_G = {0 x1, 1 x8, 16/9 x6}`.
- `Spec B = {-2 x3, 0 x9, 2 x3}`.
- Совместные ранги: `1,8,3,3`.
- В блоке ранга 8: `4 incidence + 4 heavy`.
- Лучший остаток восстановления `P_I`: `sqrt(2)` по Гильберту–Шмидту и
  `1/2` по операторной норме.
- Общий KMS-transfer-след скалярен при всех проверенных плотностях.
- Коммутант остаётся 13-мерным.
- Два запуска дали одинаковый SHA-256
  `3026c09b35b1d3e10aecba7d9c7758525c12e80a4c3f5918fa26a52538e510b9`.

## Key Points

- Два свободных веса имеют конкретный источник: кратность `4+4`.
- Gauge- и chain-данные не видят различия между этими копиями.
- Использование `P_I`, выведенного из уже выбранного `A_0`, было бы
  круговым запуском.
- Следующий допустимый источник различия — Real- или бимодульная структура,
  определённая до выбора вакуума.

## Links

- [[version8-isotypic-relative-curvature-parent-hessian-gate]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[version7-affine-hodge-copy-selector-no-go-gate]]
- [[version7-common-irreducible-trace-multiplicity-gate]]

## Source Notes

- `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex`
- `s2t/audits/s2t_v8_gauge_closed_edge_hodge_origin_gate.py`
- `s2t/results/s2t_v8_gauge_closed_edge_hodge_origin_gate_results.json`