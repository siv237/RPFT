# Классификация физического интертвинера стрелки--endpoint

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Классифицировать настоящие gauge-эквивариантные отображения полного
36-мерного модуля одиннадцати стрелок в физический endpoint-модуль.

## Search for Solution

Каждый блок `Hom(H_s,H_t)` разложен как представление
`R_t tensor R_s*` группы `SU(3)xSU(2)xU(1)`. Совпадающие неприводимые
компоненты сопоставлены с кратностями endpoint-модуля.

Полный ориентированный модуль имеет 10 комплексных интертвинеров, Real-
удвоенный — 14. Поэтому общий коннектор не уникален. Все 10 прямых каналов
принадлежат Hodge-заглушённым рёбрам.

На выбранной опоре прямых каналов нет. После Real-завершения появляется
ровно один: обратный партнёр выбранного ребра `Q_L--Y_R` содержит
`(3,1,2/3)` и отображается в `u_R`.

## Expected Result

- Размерностное отождествление окончательно заменено физической
  классификацией представлений.
- Полный коннектор неоднозначен.
- На выбранной Real-Hodge-опоре найден единственный физически типизированный
  канал с максимальным рангом 3.
- Он заслуживает отдельного подъёмного теста, но ещё не открывает новый том.

## Compliance Check

- `dim Hom_G(E_new,H21)=10`.
- После Real-удвоения размерность равна `14`.
- На выбранной прямой опоре размерность `0`.
- На выбранной Real-опоре размерность `1`.
- Единственный канал: `Y_R -> Q_L`, компонент `(3,1,2/3) -> u_R`.

## Links

- [[version8-polar-morita-connector-admission-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version7-rooted-cycle-isotypic-edge-projector-gate]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex`
- `s2t/audits/s2t_v8_physical_arrow_endpoint_intertwiner_classification_gate.py`
- `s2t/results/s2t_v8_physical_arrow_endpoint_intertwiner_classification_gate_results.json`