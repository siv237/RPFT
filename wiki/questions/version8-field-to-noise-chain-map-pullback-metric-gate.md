# Полево-шумовое отображение и обратный перенос следовой метрики

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Каноническое блочное отображение
`J(delta A,delta B_s,delta B_t)=[[delta B_s,delta A*],[delta A,delta B_t]]`
является точным изоморфизмом полного 42-мерного пространства полей и
42-мерного шумового репера. Его матрица в согласованных базисах равна
`I_42`, ранг равен `42`, ядро нулевое.

Для двенадцати калибровочных генераторов проверены все `504` пары
«генератор — направление»; дефекты тождества
`J delta_X = i ad_X J` равны нулю точно. Следовая метрика переносится как
`G_поле=J* K J=K`, а обратный тензор равен `K^-1`.

## Граница результата

Получен кинематический изоморфизм, но не динамический закон. Разложение
`30+12` допускает два независимых эквивариантных масштаба, поэтому одна
калибровочная симметрия не выбирает их отношение. Ранее доказанный запрет
вывода физической мобильности из одного полевого действия остаётся в силе.

## Следующий вопрос

Вычислить полный родительский гессиан на том же 42-мерном носителе и точно
сравнить его с `G_поле`. Только такое сравнение может установить, является
ли `K^-1` физической мобильностью или требует дополнительного принципа.

## Связи

- [[version8-temporary-boundary-and-retrospective-return]]
- [[version8-retrospective-strength-building-fork]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-metric-dual-environment-parent-action-origin-gate]]

## Исходники

- `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex`
- `s2t/audits/s2t_v8_field_to_noise_chain_map_pullback_metric_gate.py`
- `s2t/results/s2t_v8_field_to_noise_chain_map_pullback_metric_gate_results.json`