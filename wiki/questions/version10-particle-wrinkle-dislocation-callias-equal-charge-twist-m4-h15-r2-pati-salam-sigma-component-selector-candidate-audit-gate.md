# Аудит селектора R2-компоненты Pati–Salam Sigma

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Можно ли канонически выделить `R2` и сопряжение из 60-компонентного
Pati–Salam-мультиплета `Sigma`?

## Результат

После нарушения до группы Стандартной модели — да. Только нужная пара имеет
`(6Y)^2=49`, поэтому

`P_R2 = (((6Y)^2-I)((6Y)^2-9I))/1920`.

Проектор имеет ранг/нуллитет `2/6`, совместим с гиперзарядом и Real-обменом
`R2↔barR2`. Его степень по `(6Y)^2` минимальна: аффинная интерполяция
невозможна.

Но динамического расщепления масс пока нет. Идеальный гессиан
`2(I-P_R2)` имеет ранг/ядро `6/2`, тогда как унаследованный selector-Hessian
имеет ранг ноль. Аудит кандидатов даёт `0/11`, physical origin `1/3`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_component_selector_candidate_audit_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-pati-salam-sigma-typed-embedding-gate]]
- [[version4-pati-salam-restricted-potential-gate]]
- [[pati-salam-generalized-inner-fluctuations]]