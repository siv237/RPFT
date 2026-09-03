# Родитель curvature moment map Delta-стабилизатора

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Может ли единый moment map нейтрального `Delta`-фона породить правильный
`R2`-gap с фиксированным знаком и отношением Cartan-каналов?

## Результат

Moment map фиксирует оператор
`Q=6Y=6 mu_R-4 ad(mu_4)`, но положительная норма даёт `+Q²` и делает
`R2` самым тяжёлым сектором.

Правильный знак возникает условно через общий auxiliary-Hessian
`[[49I,Q],[Q,I]]`. Он положителен, имеет rank/nullity `14/2`, а Schur
complement точно равен `49I-Q²=G_Y`.

Физический parent пока не закрыт: унаследованный auxiliary cross-блок имеет
rank `0`. Требуется типизированно вложить образ `Q Sigma` в 36-мерную
fixed-point auxiliary algebra. Conditional/physical origin: `3/4`, `2/4`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-sigma-mixed-curvature-candidate-audit-gate]]
- [[pati-salam-irreducible-relative-cycle-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-hypercharge-projector-mass-splitting-parent-origin-gate]]