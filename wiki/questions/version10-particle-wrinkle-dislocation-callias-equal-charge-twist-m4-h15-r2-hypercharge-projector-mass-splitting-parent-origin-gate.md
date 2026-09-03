# Родитель расщепления масс гиперзарядового проектора R2

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Превращает ли гиперзарядовый проектор на `R2+barR2` алгебраический селектор
в физическое расщепление масс полного Pati–Salam-мультиплета `Sigma`?

## Результат

Условно — да. Оператор

`G_Y = 49I-(6Y)^2 = diag(40,40,0,48,48,0,40,40)`

положителен и имеет ядро ровно на `R2+barR2`. Для Hessian
`H=kappa G_Y-mu2 I` только эта пара становится тахионной при
`kappa>0` и `0<mu2/kappa<40`. Свидетель `mu2/kappa=20` имеет сигнатуру
`(2,0,6)`.

Физический parent не найден: inherited gap имеет ранг ноль, а коэффициенты
`kappa`, `mu2/kappa`, квартальная стабилизация и абсолютный масштаб не
выведены. Поэтому значение `20` — лишь точный свидетель существования окна,
не предсказание.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_projector_mass_splitting_parent_origin_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-pati-salam-sigma-component-selector-candidate-audit-gate]]
- [[version4-pati-salam-restricted-potential-gate]]
- [[pati-salam-generalized-inner-fluctuations]]