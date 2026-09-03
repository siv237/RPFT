# Двухрезервуарный неравновесный ток K43

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Можно ли заменить равновесный KMS-канал с нулевым чистым током точной
двухрезервуарной CPTP-динамикой, сохранив локальную вероятность выхода `1/6`?

## Результат

Для горячей ванны взяты вероятности `(p_down,p_up)=(1/6,1/12)`, для
холодной — `(1/6,1/24)`. Суммарная переходная матрица имеет стационарное
состояние

$$
\pi=\left(\frac8{11},\frac3{11}\right).
$$

Направленные токи равны `J_h=1/66` и `J_c=-1/66`, а производство энтропии
равно `log(2)/66>0`. Тем самым неравновесное сквозное дыхание математически
реализовано. Происхождение трёх параметров резервуарного пакета и абсолютного
темпа остаётся открытым.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_nonequilibrium_two_reservoir_output_current_parent_admission_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-k43-kms-output-channel-parent-origin-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-two-reservoir-affinity-hopf-cycle-typed-origin-gate]]