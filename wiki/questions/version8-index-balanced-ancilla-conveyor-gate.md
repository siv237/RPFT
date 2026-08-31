# Индексно-сбалансированный ancilla-конвейер

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

К рабочей `C43`-цепи добавлена встречная `C43`-цепь. Индексы `43` и
`1/43` сокращаются до `1`. Пара встречных сдвигов реализуется точной
nearest-neighbour схемой из двух SWAP-слоёв, каждый из которых является
экспонентой commuting local Hamiltonian terms. Рабочая цепь продолжает
давать свежие vacuum-ancilla и точно воспроизводит `Phi_h^n`.

## Problem

Устранить GNVW-препятствие одностороннего конвейера, не меняя проверенный
42-jump collision-процесс.

## Search for solution

- Добавлена spectator-цепь с обратным индексом `1/43`.
- Построены слои `SWAP(A_m,B_m)` и `SWAP(B_m,A_(m+1))`.
- Символьно прослежены итоговые действия `A_m<-A_(m-1)` и
  `B_m<-B_(m+1)`.
- Проверено `exp[-i*pi/2*(I-SWAP)]=SWAP` по собственным значениям `±1`.
- Исходная finite-cylinder induction расширена тривиальным spectator-
  потоком.

## Expected result

Полный conveyor должен иметь тривиальный индекс, локальную конечную
глубину и сохранять точную редуцированную динамику.

## Compliance check

- Total GNVW index: `43*(1/43)=1`.
- Circuit depth: `2`.
- Range: nearest neighbour.
- Gauge/Real covariance: pass.
- Reduced iteration: `Phi_h^n`, residual `0`.
- Piecewise local Hamiltonian: constructed.
- Single static local Hamiltonian: open.
- Absolute tick duration: open.

## Links

- [[version8-vacuum-chain-parent-state-and-local-hamiltonian-origin-gate]]
- [[version8-full-noise-toeplitz-ancilla-chain-dilation-gate]]
- [[gnvw-alpu-ancilla-shift-obstruction]]

## Source Notes

- `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex`
- `s2t/audits/s2t_v8_index_balanced_ancilla_conveyor_gate.py`
- `s2t/results/s2t_v8_index_balanced_ancilla_conveyor_gate_results.json`
- `s2t/proofdsl/examples/version8_index_balanced_ancilla_conveyor.py`