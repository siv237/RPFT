# Аудит кандидатов коэффициента гиперзарядового gap R2

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Выбирает ли текущий родитель коэффициенты Hessian
`H=aI+b(6Y)^2`, оставляющего тахионной только `R2+barR2`?

## Результат

Нет. Правильная сигнатура задаёт открытый конус

`b<0`, `a+49b<0`, `a+9b>0`.

После нормировки это весь интервал `0<mu2/kappa<40`. Точные отношения `10`
и `30` оба проходят, поэтому знак не фиксирует коэффициент. Сам
`G_Y=49I-(6Y)^2` лежит на границе и оставляет `R2` безмассовым.

Одиннадцать механизмов дают `0/11`. Лучший — connected spectral trace на
общем фоне нарушения до SM (`5/6`), но нужный фон `T3_R+(B-L)/2` не
унаследован текущим носителем. Physical origin остаётся `1/3`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_gap_coefficient_candidate_audit_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-hypercharge-projector-mass-splitting-parent-origin-gate]]
- [[version4-pati-salam-restricted-potential-gate]]
- [[version4-pati-salam-vacuum-singlet-gate]]