# Селектор совместимой комплексной структуры и положительной метрики

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Существующая следовая метрика не переносится на новый симплектический
носитель без дефицита. Его вещественная размерность равна `52`, тогда как
полный старый полево-шумовой репер имеет размерность `42`. Любой обратный
образ старой метрики имеет ранг не выше `42` и ядро не меньше `10`.
Transfer-only блок размерности `30` оставляет ядро `22`.

Даже в наиболее благоприятном согласованном вложении получено непрерывное
семейство положительных метрик `G_s` и комплексных структур `J_s`.
Представители `s=1` и `s=2` различны, удовлетворяют `J_s^2=-I` и
`G_s=Omega J_s>0`, но одинаково ограничиваются на весь старый 42-мерный
следовой носитель.

Следовательно, следовая база проекта не выбирает комплексную структуру и
не поднимает горизонтальную фазу. Требуется происхождение метрики на десяти
новых вещественных направлениях.

## Следующий вопрос

Можно ли получить недостающий десятиранговый метрический блок из общей
концевой следовой формы, Stinespring-среды или BV-кокасательного сектора без
нового свободного коэффициента?

## Связи

- [[version8-horizontal-phase-cotangent-doubled-quiver-parent-admission-gate]]
- [[version3-bf-aksz-pairing-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_cotangent_complex_structure_metric_selector_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_cotangent_complex_structure_metric_selector_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_cotangent_complex_structure_metric_selector.py`