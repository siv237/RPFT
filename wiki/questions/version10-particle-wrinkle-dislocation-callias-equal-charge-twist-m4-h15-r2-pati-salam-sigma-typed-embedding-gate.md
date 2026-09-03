# Типизированное вложение R2 в Pati–Salam Sigma

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Содержит ли `Sigma=(2_R,2_L,15_4)` точную компоненту
`R2=(3,2)_{7/6}`, реализующую два недостающих ребра `H15`?

## Результат

Да. Ветвление по правилу `Y=T3_R+(B-L)/2` даёт восемь SM-секторов,
включая один `R2` и его сопряжение. Они имеют суммарную комплексную
размерность `12`, создают два нужных ребра и сокращают ядро графа `H15`
до одной равномерной компоненты.

Однако полный `Sigma` имеет размерность `60`. Вместе с `R2` неизбежно
присутствуют `tilde_R2`, цветные октет-дублеты и Higgs-подобные дублеты.
Проектор на `R2` совместим с группой Стандартной модели, но его коммутатор
с `SU(2)_R`-переворотом имеет ранг `4`. Поэтому необходим отдельный
динамический селектор после нарушения Pati–Salam-симметрии.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_pati_salam_sigma_typed_embedding_gate_results.json`
- `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-dirac-seed-candidate-audit-gate]]
- [[version4-pati-salam-finite-dirac-block]]
- [[pati-salam-generalized-inner-fluctuations]]