# Родитель равномерного усиления Callias–M4 по H15

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Выбирает ли физический граф $H_{15}$ единственную равномерную амплитуду
cross-оператора во всех пятнадцати каналах?

## Результат

Нет. Рёбра `Q-u`, `Q-d`, `L-e` образуют две компоненты с кратностями
`12+3`; лапласиан имеет ранг/ядро `3/2`. Одно условное ребро `Q-L`
делает граф связным: ранг/ядро становятся `4/1`, а ядро поднимается в
`ones(15)`.

Это ребро не унаследовано — его ранг равен нулю. Кроме того, связность
фиксирует только относительную равномерность, но не абсолютную амплитуду.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate_results.json`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-fermionic-cross-typed-embedding-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version7-minimal-h15-mixed-connector-admission-gate]]