# Том X: родитель собственного четырёхмерного объёма ячейки

> Status: working
> Type: question
> Updated: 2026-09-01

## Summary

Построена изотропная четырёхмерная ячейка с собственным объёмом
`v_cell=ell_cell^4`. Рождение одной ячейки увеличивает полный объём ровно
на `v_cell`. Общий родитель выбирает безразмерное произведение объёма и
энергии, но сохраняет одну противоположную масштабную моду.

## Key Points

- `G_cell=ell_cell² I4`, `det(G_cell)=ell_cell^8`.
- `v_cell=sqrt(det(G_cell))=ell_cell^4`.
- Нормированная форма равна `I4` и имеет определитель `1`.
- `V_(N+1)-V_N=v_cell`.
- `Y=E_C^4 v_cell/(hbar c)^4`; условие `Y=1` даёт
  `E_C ell_cell=hbar c`.
- Родитель имеет гессиан ранга `3`, ядро размерности `1` и определитель `0`.
- Архитектура `8/8`, относительное происхождение `3/3`, абсолютное
  происхождение объёма и энергии `0/2`.

## Open Boundary

Следующий узел проверяет, может ли спектральная счётная мера конечной ячейки
квантовать её четырёхмерный объём без свободного обрезания.

## Links

- [[version10-cell-birth-clock-energy-geometric-anchor-candidate-audit-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version10_cell_birth_intrinsic_four_volume_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_intrinsic_four_volume_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_intrinsic_four_volume_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_intrinsic_four_volume_parent_origin.py`