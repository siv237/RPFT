# Том VI: исправленный нерадиальный спектр вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

После подстановки канонических коэффициентов
`A=C=128/243`, `B=160/243`, `G=2/27` отрицательных мод на проверенных
сетках не найдено, но положительный нерадиальный зазор также не
подтверждён.

На сетке `56` все восемь нижних значений лежат между `0.01327` и
`0.02437`. Третья мода при переходе `48 -> 56` уменьшается до `0.1105`
своего прежнего значения. Поэтому старое разделение на два переноса и
жёсткий положительный сектор отвергнуто.

## Статус

- исправленный эффективный оператор построен;
- отрицательная мода пока не обнаружена;
- восемь мод смягчаются к нулю;
- наивные переносные касательные не совпадают с низшим подпространством;
- нерадиальная устойчивость не сертифицирована;
- следующий вопрос — точный ковариантный проектор переносов и
  калибровочных направлений.

## Последующее разрешение

[[version6-bosonic-defect-corrected-vortex-covariant-zero-mode-resolution-gate]]
обнаружил ошибку знака в фоновой калибровке. После её исправления появился
изолированный отрицательный уровень `-0.189047...`. Поэтому мягкий кластер
этой страницы является промежуточным численным симптомом, а прямая нить
фактически линейно неустойчива.

## Связи

- [[version6-bosonic-defect-q-stiffness-parent-normalization-gate]]
- [[version6-bosonic-defect-corrected-vortex-covariant-zero-mode-resolution-gate]]
- [[version6-bosonic-defect-q-tetrahedral-vortex-angular-stability-gate]]
- [[version6-bosonic-defect-q-tetrahedral-vortex-full-hessian-gate]]
- [[so3-z3-vortex-profile-and-stability-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_corrected_vortex_nonradial_stability_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_corrected_vortex_nonradial_stability_gate_results.json`