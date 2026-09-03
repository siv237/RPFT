# Аудит кандидатов odd auxiliary cross-bilinear

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Какой внутренний механизм может породить mixed bilinear
`<A_Sigma,Q Sigma>` с фиксированным `Q=6Y`, не загружая target вручную?

## Результат

Двенадцать кандидатов дали `0/12`; матрица шести критериев имеет rank `6`.
В Cartan-базисе `(T,B)` оператор `Q` единственно имеет коэффициенты `(1,1)`.
Унаследованный cross-block имеет rank `0`, требуемый — `8`.

Лучшие пути, оба `5/6`, — единый `Delta` moment-map trilinear и mixed
superconnection curvature. Они фиксируют точный `Q`, gauge/Real type и
нормировку, но отсутствуют в текущем action вместе с независимым
`A_Sigma`. Physical origin остаётся `5/6`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-hubbard-stratonovich-odd-auxiliary-parent-origin-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-stabilizer-moment-map-curvature-parent-origin-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-minimal-odd-auxiliary-bimodule-candidate-audit-gate]]