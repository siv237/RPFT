# Аудит кандидатов кварк–лептонного коннектора H15

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Можно ли физически реализовать условное межкомпонентное ребро, которое в
предыдущем гейте выбирало равномерный луч усиления на $H_{15}$?

## Результат

Прямое ребро `Q_L-L_L` связывает типовой граф, но соединяет одинаковые
хиральности и несёт ненулевые цветовой и гиперзарядовый дефекты. Оно не
является физическим Dirac-блоком.

Минимальное калибровочно типизированное завершение — пара
`L_L-u_R`, `Q_L-e_R`, то есть один комплексный лептокварк
`R2=(3,2)_{7/6}`. Пара связывает граф и создаёт один смешанный цикл, но оба
ребра меняют две бимодульные координаты и нарушают строгое условие первого
порядка на фиксированной геометрии Стандартной модели.

Аудит одиннадцати маршрутов даёт `0/11`. Следующий вопрос — существует ли
не target-loaded обобщённый первопорядковый родитель именно для пары `R2`.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate_results.json`
- `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex`
- `s2t/gates/version7_r2_real_first_order_admission_gate.tex`

## Связи

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-uniform-h15-amplification-parent-origin-gate]]
- [[version7-minimal-h15-mixed-connector-admission-gate]]
- [[version7-r2-real-first-order-admission-gate]]