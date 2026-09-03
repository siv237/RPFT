# Том X: аудит топологических квантов четырёхмерного объёма

> Status: working
> Type: question
> Updated: 2026-09-01

## Summary

Восемь топологических кандидатов проверены по пяти условиям. Все способны
фиксировать целые классы или кратности, но ни один не имеет размерности
`L^4` и не выбирает элементарный физический объём.

## Key Points

- Матрица кандидатов имеет размер `8x5`, ранг `2`, проходы `0/8`.
- Размерный столбец и столбец разрыва орбиты полностью нулевые.
- Полный объём факторизуется как `V=n v0`.
- Топологическая плотность `n/V` получает размерность от метрики.
- Родитель кратности имеет гессиан `diag(1,0)`, ранг/ядро `1/1`.
- Архитектура `8/8`, топологическое происхождение `2/4`, физический квант
  объёма `0/1`.

## Open Boundary

Следующий гейт проверяет, может ли объёмная плотность кривизны создать
размерный родитель без заранее заданного коэффициента.

## Links

- [[version10-cell-birth-four-volume-spectral-counting-measure-origin-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_topological_quantum_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_topological_quantum_candidate_audit_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_topological_quantum_candidate_audit.py`