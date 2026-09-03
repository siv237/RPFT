# Хопфовское происхождение разности сродств двух резервуаров

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Следует ли требуемая разность KMS-сродств двух ванн из уже построенного
ориентированного хопфовского трёхцикла, без подстановки целевого тока?

## Результат

Полное сродство цикла равно `3 log 2`. Циклическая симметрия делит его на
три равных ребра, поэтому локальное сродство равно `log 2`. Для отношений
KMS-переходов `1/2` и `1/4` разность сродств также равна

$$
\log\frac{1/2}{1/4}=\log 2.
$$

Совпадение типизировано, а ток `1/66` согласуется с прежней хопфовской
формулой `J_edge=kappa/3` через `kappa Delta t=1/22`. Однако матрица
сродств имеет ранг/ядро `2/1`: общий сдвиг обеих температур не наблюдается.
Отдельно сохраняется контрмасштабирование скорости и шага времени.

## Статус

- условный перенос сродства: `8/8`;
- происхождение разности сродств: `1/1`;
- происхождение общего температурного якоря: `0/1`;
- происхождение абсолютных часов и масштаба: `0/2`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_two_reservoir_affinity_hopf_cycle_typed_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-k43-nonequilibrium-two-reservoir-output-current-parent-admission-gate]]
- [[version10-cell-birth-four-volume-hopf-cycle-conductance-common-parent-origin-gate]]
- [[version10-cell-birth-four-volume-throughflow-affinity-impedance-origin-audit-gate]]