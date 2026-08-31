# Горизонтальная реконструкция вакуумного гессиана

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Следовая метрика ограничивается на нарушенную калибровочную орбиту как
`14 I_3` и канонически задаёт ортогональный проектор. Компрессия
`H_quot=Q^T H_Phi Q` зануляет все три голдстоуновские моды.

Исправленный гессиан имеет ранг `26` и ядро `4`: три калибровочные моды и
одну горизонтальную плоскую моду. Квадратичный BV-ledger равен
`N_bos=226371884/159201`, а после фермионного вклада `-92` —
`N_quad=211725392/159201`.

Это точный результат на горизонтальном квадратичном quotient, но не вывод
единого гладкого нелинейного калибровочно-инвариантного родителя.

## Следующий вопрос

Определить происхождение единственной горизонтальной плоской моды и
проверить, допускает ли она нелинейный родительский подъём без нового
свободного коэффициента.

## Связи

- [[version8-full-42-carrier-bv-vacuum-quotient-gate]]
- [[version8-full-42-carrier-base-k-determinant-compatibility-gate]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Исходники

- `s2t/gates/version8_gauge_invariant_vacuum_hessian_reconstruction_gate.tex`
- `s2t/audits/s2t_v8_gauge_invariant_vacuum_hessian_reconstruction_gate.py`
- `s2t/results/s2t_v8_gauge_invariant_vacuum_hessian_reconstruction_gate_results.json`
- `s2t/proofdsl/examples/version8_gauge_invariant_vacuum_hessian_reconstruction.py`