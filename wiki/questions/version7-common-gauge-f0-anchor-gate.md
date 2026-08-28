# Version VII: общий калибровочный якорь момента f0

> Status: mature
> Type: question
> Updated: 2026-08-27

## Problem

Product heat-kernel свёл эффективную рёберную квартику к
`lambda_E=pi²/f0`, но текущий вспомогательный носитель не содержит
доказанного общего физического калибровочного блока. Нужно проверить, может
ли один и тот же спектральный след одновременно нормировать gauge-кинетику
и Hodge-поле без ручного отождествления носителей.

## Search for Solution

Для полного конечного gauge-индекса `q_G` получен условный словарь

`f0=6 pi²/(q_G g²)`, `lambda_E=q_G g²/6`.

Старый относительный `U(1)` с `q_G=2` формально дал бы
`lambda_E=g²/3`. Однако Hodge-родитель использует незавешенный след по
одиннадцати меткам рёбер, тогда как физическая gauge-кривизна взвешивает
каждый полный блок его размерностью и индексом представления.

На шести выбранных рёбрах четыре канала имеют нулевую разность
гиперзарядов, а два — заряды `-2/3` и `5/3`. Поэтому их gauge-веса уже
неравны до учёта цветовых и слабых кратностей.

## Expected Result

Получена условная формула и точный no-go прямого переноса старого якоря.
Редуцированный носитель не определяет полный `q_G^edge`, поэтому
`lambda_E=g²/3` не является предсказанием. Следующий тест должен раскрыть
все калибровочные компоненты рёбер и повторно проверить Hodge-потенциал,
селектор и гессиан с одним физическим следом.

## Links

- [[version7-spacetime-kinetic-potential-ratio-admission-gate]]
- [[version4-heat-kernel-trace-dictionary-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[version7-full-gauge-weighted-edge-carrier-gate]]

## Source Notes

- `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex`
- `s2t/gates/version4_heat_kernel_trace_dictionary_gate.tex`
- `s2t/gates/version5_projector_superconnection_common_scale_gate.tex`
- `s2t/gates/version7_common_gauge_f0_anchor_gate.tex`
- `s2t/results/s2t_v7_common_gauge_f0_anchor_gate_results.json`