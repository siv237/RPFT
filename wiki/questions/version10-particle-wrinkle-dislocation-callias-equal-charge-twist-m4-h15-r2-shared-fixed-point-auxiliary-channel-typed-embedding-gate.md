# Типизированное вложение общего fixed-point auxiliary-канала

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Содержит ли 36-мерная fixed-point auxiliary algebra типизированный образ
`Q Sigma`, необходимый для положительного Schur-parent гиперзарядового gap?

## Результат

Нет. После комплексизации fixed-point algebra несёт только веса
`0^22`, `(±4)^6`, `(±6)^1`, тогда как `Q Sigma` требует
`(±1)^1`, `(±3)^2`, `(±7)^1`. Пересечение пусто, поэтому
гиперзаряд-эквивариантный `Hom` имеет размерность `0`; точный constraint
имеет rank/nullity `288/0`.

Обычная изометрия ранга `8` существует, но её equivariance defect имеет
rank `8`, а even grading fixed-point curvature несовместим с требуемым odd
образом. Условно проблему решает новый odd auxiliary-бимодуль размерности
`8` с тем же спектром, reality и trace metric, но он не унаследован.
Inherited/conditional typed status: `2/4`, `4/4`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-stabilizer-moment-map-curvature-parent-origin-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-mapping-cone-common-parent-typed-embedding-gate]]
- [[pati-salam-irreducible-relative-cycle-gate]]