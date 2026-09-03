# Родитель происхождения M4 cross-генератора

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Может ли общий положительный родитель динамически породить ненулевой
резервуарно-хопфовский cross-генератор?

## Результат

Условно — да. Квартальный partial-isometry-потенциал с ориентационным
штрафом имеет в `V=I2` гессиан ранга `4`, определитель `32` и спектр
`(2,2,2,4)`. Однако он оставляет четыре вещественных знаковых минимума и
комплексный фазовый тор `U(1)^2`.

Унаследованный cross-гессиан имеет ранг/ядро `0/4`, линейный источник
равен нулю. Ненулевая норма конденсата уже загружена членом `V*V-I`;
происхождение её коэффициентов равно `0/3`, строгое физическое
происхождение — `0/4`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-intertwiner-common-carrier-admission-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-intertwiner-candidate-audit-gate]]
- [[version10-cell-birth-four-volume-nonequilibrium-bath-birth-tick-reference-scale-ratio-minimal-portal-operator-architecture-gate]]