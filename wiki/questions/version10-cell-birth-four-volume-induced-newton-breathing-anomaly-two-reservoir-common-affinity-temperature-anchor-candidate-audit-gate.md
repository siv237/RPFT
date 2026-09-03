# Аудит общего сродства и температурного якоря

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Выбирает ли текущий корпус общий сдвиг двух KMS-сродств и их абсолютную
физическую температуру?

## Результат

Десять кандидатов проверены по шести независимым критериям. Матрица имеет
ранг `6`, максимальная оценка равна `4/6`, полных проходов нет: `0/10`.

Ближайший кандидат — пути хопфовского цикла длины один и два:

$$
(a_h,a_c)=(\log2,2\log2).
$$

Он воспроизводит обе безразмерные величины без нового числа, но текущий
родитель не назначает пути двум резервуарам. Даже после такого назначения
сохраняется температурно-энергетическая орбита
`(beta_h,beta_c,Delta)->(beta_h/c,beta_c/c,c Delta)`.

## Статус

- покрытие кандидатов: `10/10`;
- покрытие критериев: `6/6`;
- общий сдвиг сродств: `0/1`;
- физическая температура: `0/1`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_common_affinity_temperature_anchor_candidate_audit_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-two-reservoir-affinity-hopf-cycle-typed-origin-gate]]
- [[version8-modular-bohr-parent-origin-gate]]
- [[version9-endpoint-creation-kms-gap-conductance-parent-origin-gate]]