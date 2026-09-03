# Происхождение Hubbard–Stratonovich odd auxiliary parent

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Выводит ли Hubbard–Stratonovich поле отсутствующий гиперзарядовый gap или
только переписывает заранее введённый mixed bilinear?

## Результат

Завершение квадрата точно даёт
`V_HS=1/2||A+Q Sigma||²+1/2 Sigmaᵀ(49I-Q²)Sigma`; stationary solution
равно `A*=-Q Sigma`, shift и Gaussian metric имеют determinant `1`.

Однако inherited source-free Hessian `diag(49I,I)` имеет rank/nullity
`16/0`, тогда как требуемый `[[49I,Q],[Q,I]]` — `14/2`. Они не связаны
обратимой заменой полей. Новый cross-increment `[[0,Q],[Q,0]]` имеет rank
`16` и inertia `(8,0,8)`. Поэтому HS является точной линеаризацией уже
данного `-Q²`, но не физическим источником этого члена. Formal/physical
origin: `4/4`, `3/4`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hubbard_stratonovich_odd_auxiliary_parent_origin_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-minimal-odd-auxiliary-bimodule-candidate-audit-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-stabilizer-moment-map-curvature-parent-origin-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-shared-fixed-point-auxiliary-channel-typed-embedding-gate]]