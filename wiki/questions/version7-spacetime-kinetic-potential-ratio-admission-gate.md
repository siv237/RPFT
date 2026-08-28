# Version VII: пространственно-временное отношение кинетики и потенциала

> Status: mature
> Type: question
> Updated: 2026-08-27

## Problem

Одной размерной калибровки достаточно для линейных масс, но не для полного
EFT: остаётся свободная безразмерная связь
`lambda_E=kappa/Z²`. Нужно проверить, фиксирует ли её один произведённый
спектральный оператор без независимой нормировки нечётного поля.

## Search for Solution

Построен минимальный плоский product-оператор
`D_E=i gamma^mu partial_mu + gamma^5 a Phi_E`. В одной конвенции
heat-kernel и физического полуследа получены

`Z=4 C0 a²`, `kappa=2 C0 a⁴`, `C0=f0/(8 pi²)`.

После канонической нормировки общий рескейлинг `a` сокращается точно:

`lambda_E=kappa/Z²=pi²/f0`.

Моменты `f2` и cutoff также не входят в это безразмерное отношение после
одной массовой калибровки. Семейное и Real-удвоение не создают новой
свободы, если оба члена вычисляются одним физическим следом.

## Expected Result

Получен частичный проход. Несколько независимых нормировок сведены к одному
безразмерному моменту `f0`, но численная квартика ещё не предсказана.
Назначать `f0=1` нельзя. Следующий проверяемый маршрут — получить `f0` из
калибровочного кинетического члена того же физического product-следа.

## Links

- [[version7-single-scale-calibration-closure-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[version7-common-gauge-f0-anchor-gate]]

## Source Notes

- `s2t/gates/version7_single_scale_calibration_closure_gate.tex`
- `s2t/gates/version5_projector_superconnection_common_scale_gate.tex`
- `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex`
- `s2t/results/s2t_v7_spacetime_kinetic_potential_ratio_admission_gate_results.json`