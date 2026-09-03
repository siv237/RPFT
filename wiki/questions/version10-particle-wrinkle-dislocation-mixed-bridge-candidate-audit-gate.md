> Status: working
> Type: question
> Updated: 2026-09-02

# Аудит смешанных мостов морщинки и дислокации

## Вопрос

Какой из уже встречавшихся механизмов может одновременно локализовать
индексный дефект, стабилизировать морщинку и породить её спектральный полюс?

## Результат

Одиннадцать кандидатов проверены по шести независимым критериям. Матрица
`11x6` имеет ранг `6`, оценки `(3,3,4,4,3,4,5,4,4,3,5)`, строгих и
унаследованных проходов `0/11`.

Градуированное произведение и моритов коннектор закрыты нулевым смешанным
блоком. Лучший физически содержательный кандидат — профиль Каллиаса
(`5/6`): он условно сохраняет индекс, локализует 15 каналов и связывает
профиль с полюсом, но нужный spinor--Clifford carrier не унаследован.

## Следующий вопрос

`version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate`
должен проверить, можно ли собрать каллиасов носитель из уже имеющихся
пространственного спинора, Real-пары, поля `Q` и K43-клеточного комплекса.

## Связи

- [[version10-particle-wrinkle-dislocation-common-parent-reopening-gate]]
- [[version6-callias-toeplitz-index-comparison-gate]]
- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[version6-spectral-transition-morita-two-step-connector-gate]]
- Гейт: `s2t/gates/version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate.tex`.
- Аудит: `s2t/audits/s2t_v10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate.py`.
- Результат: `s2t/results/s2t_v10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate_results.json`.