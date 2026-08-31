# Parent вакуумной ancilla-цепи и индексный запрет локального Hamiltonian сдвига

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

Граница главы 56 разделена на две части. Product-vacuum 43-мерных ячеек
имеет простой локальный commuting-projector parent с единственным
конечномерным вакуумом и зазором `1`. Но точный одноклеточный конвейер
имеет мультипликативный GNVW-индекс `43`, тогда как любая конечновременная
эволюция Lieb--Robinson-локального Hamiltonian имеет тривиальный индекс
`1`. Поэтому локальный parent состояния существует, а локальный
Hamiltonian точного сдвига запрещён.

## Problem

Проверить, можно ли одновременно вывести подготовку vacuum-цепи и её
точный Toeplitz-сдвиг из одного локального автономного Hamiltonian.

## Search for solution

- Для каждой ячейки построен проектор `h_m=I-|0><0|_m`.
- На конечном интервале проверены commuting-projector структура,
  одномерное ядро и зазор `1`.
- Для сдвига `C^43`-ячеек применён индекс GNVW: `ind(S)=43`.
- Локальный collision имеет индекс `1`, поэтому `ind(V)=43`.
- Использован ALPU converse to Lieb--Robinson: Hamiltonian-путь от
  тождества имеет нулевой аддитивный, то есть единичный мультипликативный
  индекс.

## Expected result

Состояние резервуара получает локальный parent, но точный конвейер не
должен ошибочно объявляться экспонентой локального стационарного
Hamiltonian.

## Compliance check

- Cell dimension: `43=1+42`.
- Vacuum parent: local, translation invariant, frustration free.
- Finite-volume ground dimension: `1`.
- Parent gap: `1`.
- Shift/global-step GNVW index: `43`.
- Local Hamiltonian path index: `1`.
- Exact local Hamiltonian origin: `false`.
- Current exact Floquet dilation remains valid: `true`.

## Links

- [[version8-full-noise-toeplitz-ancilla-chain-dilation-gate]]
- [[version8-current-status-synchronization]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[gnvw-alpu-ancilla-shift-obstruction]]

## Source Notes

- `s2t/gates/version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate.tex`
- `s2t/audits/s2t_v8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate.py`
- `s2t/results/s2t_v8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate_results.json`
- `s2t/proofdsl/examples/version8_vacuum_chain_parent_state_and_local_hamiltonian_origin.py`
- Gross--Nesme--Vogts--Werner, `arXiv:0910.3675`.
- Ranard--Walter--Witteveen, `arXiv:2012.00741`.