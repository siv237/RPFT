# Version VII: индексный дефект и редуцированный связывающий quotient

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Однократная UCP-карта согласованных десятимерных Gram-углов локально выводит
нужную половину и правильный гессиан, но полный сохраняющий след expectation
дублирует общий угол и возвращает провальный вес один.

## Search for Solution

Сопоставлены сырая однокопийная норма `1/2 ||Z||²`, метрика, индуцированная
исходным двухугловым носителем, общий Real-полуслед, прежний лесной quotient,
текущий представленный junk и касательное gauge/BRST--BV-действие в нуле.

## Expected Result

Индуцированная quotient-метрика равна `||Z||²`, то есть имеет масштаб `c=2`
относительно сырого локального кандидата. Она точно восстанавливает прежний
физический гессиан и даёт провал `(21,0,6)`. Рабочее окно равно
`0 <= c < 16/15`, поэтому `c=1` проходит, а наследуемое `c=2` — нет.
Ни одна из уже построенных редукций не выводит понижение метрики до `c=1`.

## Links

- [[version7-incidence-transfer-markov-weight-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version5-morita-linking-parent-gate]]
- [[version5-sm-linking-corner-gate]]
- [[polar-transfer-linking-expectation-literature-2026]]
- [[version7-polar-transfer-cross-curvature-origin-gate]]

## Source Notes

- `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex`
- `s2t/audits/s2t_v7_index_defect_reduced_linking_quotient_gate.py`
- `s2t/results/s2t_v7_index_defect_reduced_linking_quotient_gate_results.json`