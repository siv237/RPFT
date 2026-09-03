# Типизированное вложение причинного ядра в клеточный комплекс

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Локальный оператор предыдущего гейта не является произвольной матрицей:
он точно получается из границы семиузлового клеточного пути как
`A=(D-BB^T)/2`. Вложение типизировано, не зависит от ориентации рёбер и
сохраняет графовый световой конус. При этом комплекс не выбирает физическую
длину ребра, глобальную топологию или затухание памяти.

## Key Points

- `B:C1 -> C0` имеет размер `7x6` и ранг `6`.
- `Delta0=B B^T` имеет ранг/ядро `6/1`; ядро порождается постоянной цепью.
- `A=(D-Delta0)/2` в точности совпадает с прежним оператором ближайших
  соседей с весом `1/2`.
- Переориентация рёбер оставляет `Delta0` и `A` неизменными, а перестановка
  вершин действует сопряжением.
- Причинные дефекты на шагах `1,2,3` равны нулю.
- Родитель памяти сохраняет ранг/ядро `3/1`; параметр `r` не выбран.
- Строгий физический остаток: глобальный комплекс, длина ребра и затухание
  имеют статус `0/3`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-local-causal-propagation-kernel-parent-origin-gate]] — исходное локальное ядро.
- [[current-status-and-next-vectors]] — общий фронтир Тома X.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding.py`