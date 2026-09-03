# Аудит кандидатов смешанной Delta–Sigma curvature

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Какой единый mixed-curvature канал может породить гиперзарядовый `R2`-gap
после выбора нейтрального `Delta`-фона?

## Результат

На `Sigma` выполнено точное разложение

`G_Y = 40I-B²-2TB`, где `T=6T3_R`, `B=3(B-L)`.

Базис `(I,B²,TB)` имеет ранг `3`, а коэффициенты `(40,-1,-2)` уникальны.
Каналы `B²` и `TB` по отдельности недостаточны; независимое назначение их
весов не считается происхождением отношения `1:2`.

Аудит даёт `0/11`. Лучший кандидат (`5/6`) — квадрат единого moment map
нейтрального `Delta`-стабилизатора; он проваливает только inherited common
parent. Текущая coefficient-map имеет rank `0`, physical origin `2/4`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-mapping-cone-common-parent-typed-embedding-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-hypercharge-projector-mass-splitting-parent-origin-gate]]
- [[version4-pati-salam-projected-curvature-selector-gate]]