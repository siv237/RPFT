# Сравнение следовой метрики с родительским гессианом

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Полево-шумовой изоморфизм не превращает внутреннюю следовую метрику в
родительский гессиан. На постояннополевом срезе точный гессиан переноса
имеет ранг `30`, а калибровочный блок равен `0_12`. Поэтому полный гессиан
имеет ранг `30`, тогда как `K` имеет ранг `42` и калибровочный блок ранга
`12` со следом `367/3`.

Равенство `H=cK` невозможно при любом вещественном `c`: калибровочный блок
вынуждает `c=0`, чему противоречит ненулевой гессиан переноса.

## Физическая граница

При ненулевом импульсе калибровочный гессиан содержит множитель
`p^2 g^{mu nu}-p^mu p^nu`, имеет продольное ядро и требует фиксации
калибровочной свободы. Поэтому он не сводится канонически к конечной
внутренней матрице `K`.

## Следующий вопрос

Построить типизированную пространственно-временную факторизацию
кинетического оператора, отделить внутреннюю метрику от поперечного
оператора и проверить зависимость обратной формы от фиксации калибровочной
свободы.

## Связи

- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[version8-isotypic-relative-curvature-parent-hessian-gate]]
- [[version8-metric-dual-environment-parent-action-origin-gate]]
- [[quantum-gradient-flow-and-noise-metric-literature-2026]]

## Исходники

- `s2t/gates/version8_field_noise_metric_to_parent_hessian_comparison_gate.tex`
- `s2t/audits/s2t_v8_field_noise_metric_to_parent_hessian_comparison_gate.py`
- `s2t/results/s2t_v8_field_noise_metric_to_parent_hessian_comparison_gate_results.json`