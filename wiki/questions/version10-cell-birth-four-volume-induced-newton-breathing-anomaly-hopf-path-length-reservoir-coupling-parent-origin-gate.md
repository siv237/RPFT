# Родитель связи длин хопфовских путей с резервуарами

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Выводит ли текущий общий родитель назначение хопфовских путей длины `1:2`
горячей и холодной ваннам?

## Результат

При уже выведенном знаке `a_c-a_h=log 2` назначение единственно:
горячей ванне соответствует путь длины один, холодной — длины два.
Согласованный морфизм имеет нулевой дефект, а переставленный — дефект
`diag(-2,2)` с квадратом нормы `8` и неправильным знаком разности.

Условный родитель строг (`rank=2`, `det=1`) и даёт KMS-отношения
`(1/2,1/4)`. Но унаследованный резервуарно-хопфовский смешанный блок равен
нулю, поэтому происхождение самого морфизма остаётся `0/1`. Физическая
температура также остаётся `0/1`: температурно-энергетическая карта имеет
ранг/ядро `2/1`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_path_length_reservoir_coupling_parent_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-two-reservoir-common-affinity-temperature-anchor-candidate-audit-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-two-reservoir-affinity-hopf-cycle-typed-origin-gate]]
- [[version10-cell-birth-four-volume-hopf-cycle-conductance-common-parent-origin-gate]]