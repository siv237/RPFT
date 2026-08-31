# No-Go статического Hamiltonian на минимальном двухцепочечном носителе

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

Тривиальный суммарный GNVW-индекс не обеспечивает статический локальный
логарифм. В одночастичном Bloch-секторе встречный conveyor равен
`diag(exp(-ik),exp(+ik))`; его eigenchannel windings равны `(-1,+1)`.
Экспонента непрерывного периодического скалярного Hamiltonian имеет winding
`0`. Поэтому минимальный translation-invariant finite-range
number-preserving static Hamiltonian невозможен.

## Problem

Проверить, можно ли заменить два управляемых SWAP-слоя одним стационарным
локальным Hamiltonian без расширения носителя.

## Search for solution

- Построен точный двухполосный Bloch-представитель.
- Символьно вычислены windings `(-1,+1)` и determinant winding `0`.
- Использовано `exp(-i h)=U => [h,U]=0`.
- На невырожденных интервалах `h(k)` обязан быть диагональным.
- Периодичность каждой диагонали противоречит ненулевому winding.

## Expected result

Минимальный статический класс должен быть либо явно построен, либо закрыт
строгим no-go с перечислением предположений.

## Compliance check

- Exact windings: `(-1,+1)`.
- Static periodic logarithm: absent.
- Piecewise Floquet construction: retained.
- General interacting/clock-augmented carrier: not excluded.
- Next gate: clock-augmented static Hamiltonian conveyor.

## Links

- [[version8-index-balanced-ancilla-conveyor-gate]]
- [[gnvw-alpu-ancilla-shift-obstruction]]

## Source Notes

- `s2t/gates/version8_static_local_hamiltonian_embedding_or_no_go_gate.tex`
- `s2t/audits/s2t_v8_static_local_hamiltonian_embedding_or_no_go_gate.py`
- `s2t/results/s2t_v8_static_local_hamiltonian_embedding_or_no_go_gate_results.json`
- `s2t/proofdsl/examples/version8_static_local_hamiltonian_embedding_no_go.py`
- Nagaj--Wocjan, `arXiv:0802.0886` (граница: enlarged clock carrier).