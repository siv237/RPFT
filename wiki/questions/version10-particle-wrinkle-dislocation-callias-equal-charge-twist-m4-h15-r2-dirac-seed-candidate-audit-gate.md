# Аудит кандидатов конечного Dirac-seed R2 на H15

> Status: working
> Type: question
> Updated: 2026-09-03

## Вопрос

Содержит ли какой-либо унаследованный оператор точную двухрёберную опору
`R2=(3,2)_{7/6}`?

## Результат

Hadamard-проекции стандартного `D_F`, Higgs-одноформы, допущенного `A_(2)`,
Callias–`M4` усилителя и лапласиана `H15` имеют ранг ноль. Явный `D_R2`
имеет требуемую проекцию ранга четыре, но является target-loaded.

Аудит одиннадцати маршрутов дал `0/11`. Ближайшее структурное расширение —
Pati–Salam-поле `Sigma=(2_R,2_L,15_4)`, содержащее компоненту нужного типа
после ветвления, но не принадлежащее текущей конечной геометрии.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_dirac_seed_candidate_audit_gate_results.json`
- `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex`
- `s2t/gates/version7_r2_generalized_fluctuation_seed_origin_gate.tex`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-generalized-first-order-parent-admission-gate]]
- [[version4-pati-salam-finite-dirac-block]]
- [[mixed-connector-krajewski-leptoquark-literature-2026]]