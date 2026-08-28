# Version VII: цветосохраняющий составной циклический родитель

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Полный gauge-подъём показал, что фундаментальный шестирёберный Hodge-вакуум
требует двух ненулевых цветовых триплетов и потому ломает `SU(3)_c`.
Нужно проверить, может ли тот же укоренённый цикл войти в действие только
через составные цветосинглетные слова, оставляя цветные рёбра нулевыми в
вакууме и ненулевыми лишь как переходные возбуждения.

## Search for Solution

Восстановлено полное ориентированное слово единственного укоренённого цикла.
Оно gauge-инвариантно, но после фиксации двух старых рёбер имеет степень
четыре по новым полям. Его градиент и гессиан в нуле равны нулю.

Ненулевое классическое значение произведения требует ненулевого значения
каждого множителя, включая два цветных. Поэтому переименование цикла в
составной синглет не устраняет нарушение цвета. При положительных массах
фундаментальных мостов нуль остаётся локально устойчивым независимо от
коэффициента циклического слова.

## Expected Result

Классический составной маршрут закрыт. Возможность нулевых одноточечных
цветных средних при ненулевом среднем цикла относится к квантовой мере и
связанным корреляторам, которых текущий Hodge-функционал не содержит.
Следующий проверяемый маршрут — оставить цветные мосты массивными и
интегрировать их виртуально через детерминант или дополнение Шура.

## Links

- [[version7-full-gauge-weighted-edge-carrier-gate]]
- [[version7-baseline-rooted-primitive-cycle-admission-gate]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[version7-virtual-colored-bridge-schur-complement-gate]]

## Source Notes

- `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex`
- `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`
- `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`
- `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex`
- `s2t/results/s2t_v7_color_preserving_composite_cycle_parent_gate_results.json`