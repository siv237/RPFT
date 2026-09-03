# Родитель локального причинного ядра распространения ванны

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Может ли локальность клеточного распространения сама вывести форму и
масштаб памяти ванны после провала меню готовых спектральных профилей?

## Результат

Оператор ближайших соседей удовлетворяет точному световому конусу:
`(A^n)_ij=0` при расстоянии больше `n`. Семейство
`K_n(r)=r^n A^n`, `0<r<1`, имеет положительную геометрическую память
`M(r)=1/(1-r)`.

Условные значения `r=1/2` и `r=1/4` дают память `2` и `4/3` шага.
Ковариационные определители положительны. Однако цепной родитель имеет
ранг/ядро `3/1`: вся кривая `(r,r²,r³)` остаётся минимумом. Локальность
выбирает причинную поддержку, но не коэффициент затухания.

## Статус

- условная архитектура: `8/8`;
- причинная поддержка: `3/3`;
- происхождение затухания и абсолютного времени: `0/2`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-nonequilibrium-bath-spectral-density-memory-scale-candidate-audit-gate]]
- [[version8-correlation-kernel-short-time-rate-selector-gate]]
- [[version10-cell-birth-four-volume-nonequilibrium-bath-correlation-time-parent-origin-gate]]