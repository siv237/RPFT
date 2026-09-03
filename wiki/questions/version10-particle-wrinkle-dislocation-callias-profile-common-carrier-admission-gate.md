> Status: working
> Type: question
> Updated: 2026-09-02

# Допуск общего каллиасова носителя

## Вопрос

Можно ли собрать минимальный каллиасов носитель из уже существующих
пространственного спинора, Real-пары, поля порядка и K43-комплекса?

## Результат

Условный минимум
`C2_spin tensor C2_twist tensor H15` имеет комплексную размерность `60`.
Spin- и twist-Pauli-тройки коммутируют; массовые проекторы имеют ранги
`30+30`, а индексная кратность равна `15`.

Строгий допуск отрицателен. KO6 particle/conjugate-пара имеет
противоположные заряды, поэтому twist-flip даёт коммутатор ранга `30`.
Клеточное ребро допускает абстрактную равнозарядную Pauli-алгебру, но его
унаследованное отображение во все пятнадцать каналов равно нулю.
Архитектура `10/10`, отдельные ингредиенты `5/5`, происхождение `0/3`.

## Следующий вопрос

`version10_particle_wrinkle_dislocation_callias_equal_charge_twist_candidate_audit_gate`
проверит источники равнозарядной двойки: клеточное ребро, flavor-пары,
семейные кратности, KMS-удвоение и минимальное расширение.

## Связи

- [[version10-particle-wrinkle-dislocation-mixed-bridge-candidate-audit-gate]]
- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[version6-callias-toeplitz-index-comparison-gate]]
- [[version6-two-copy-spin-cover-multiplicity-gate]]
- Гейт: `s2t/gates/version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate.tex`.
- Аудит: `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate.py`.
- Результат: `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate_results.json`.