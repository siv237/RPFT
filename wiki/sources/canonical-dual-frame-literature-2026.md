# Канонический двойственный каркас и восстановление проходов

> Status: working
> Type: source
> Updated: 2026-08-21

## Краткий вывод

Для каркаса с оператором `R=Σ_a w_a n_a n_a^T` канонический
двойственный каркас строится без нового выбора как `R^-1 n_a`. Он даёт
тождественную формулу восстановления. В проекте это позволяет читать
`R^-1` кинематически — как сопряжение плотности проходов и локального
правила сшивки, — не превращая его в дополнительную энергию.

## Первичный источник

- R. J. Duffin, A. C. Schaeffer, *A Class of Nonharmonic Fourier
  Series*, Transactions of the American Mathematical Society 72 (1952),
  341–366 — исходная теория каркасов и двойственного восстановления.

## Значение для проекта

Аффинная коизометрия проекта удовлетворяет `VV^T=I3` и
`V^T V=P3`. Её четыре нормированных столбца имеют взаимные скалярные
произведения `-1/3`, то есть образуют правильный тетраэдр.

Взвешенный оператор этого каркаса совпадает с локальным вторым моментом
`R`. Поэтому смешанный первично-двойственный третий момент является
каноническим кандидатом на наблюдаемое локальной сшивки одной нити.

## Связи

- [[version6-single-thread-connectivity-weighted-moment-parent-gate]]
- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version6-modular-dual-weight-bridge-coercivity-gate]]
- [[single-chain-orientational-moments-literature-2026]]

## Исходные материалы

- `s2t/gates/version6_single_thread_connectivity_weighted_moment_parent_gate.tex`
- `s2t/audits/s2t_v6_single_thread_connectivity_weighted_moment_parent_gate.py`
- `s2t/results/s2t_v6_single_thread_connectivity_weighted_moment_parent_gate_results.json`
