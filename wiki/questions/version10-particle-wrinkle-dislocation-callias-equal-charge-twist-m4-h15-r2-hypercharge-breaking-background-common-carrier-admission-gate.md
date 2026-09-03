# Общий носитель гиперзарядового breaking-background

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Нужны ли два независимых adjoint-фона для реализации
`Y=T3_R+(B-L)/2`, или общий scalar carrier уже существует?

## Результат

Общий минимальный носитель существует в constrained composite branch:
`Delta=(2_R,1_L,4_4)`. Его восемь значений `6Y` равны
`(4,4,4,-2,-2,-2,0,-6)`, поэтому нейтральный луч единственен.

Вес нейтральной компоненты `(3,-3)` оставляет единственный Cartan-луч
`(1,1)`, то есть `6Y=6T3_R+3(B-L)`. На `Sigma` совместная спектральная
алгебра двух Cartan-генераторов и алгебра одного `Y` обе имеют ранг `6` и
совпадают.

Admission остаётся условным. General-fundamental branch не содержит
`Delta`; минимальный composite potential имеет rank-one instability.
Relative mapping-cone parent ранее исправил `Delta+C`-Hessian, но ещё не
встроен в общий parent Тома X. Conditional/current origin: `3/4` и `2/4`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_hypercharge_breaking_background_common_carrier_admission_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-hypercharge-gap-coefficient-candidate-audit-gate]]
- [[version4-pati-salam-finite-dirac-block]]
- [[pati-salam-irreducible-relative-cycle-gate]]