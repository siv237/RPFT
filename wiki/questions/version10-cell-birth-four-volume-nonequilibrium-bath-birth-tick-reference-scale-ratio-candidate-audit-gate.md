# Аудит кандидатов отношения опорных шкал такта рождения

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Требуемое отношение точно факторизуется как произведение RG-подавления и
`1/42`, но эта факторизация не является независимым происхождением. Из
одиннадцати кандидатов ни один не проходит полный контракт.

## Key Points

- Формальный мост равен `exp(-32 pi²/3)/42`.
- Родитель одной композиционной невязки имеет ранг/ядро `1/2` и не выбирает
  два множителя.
- Матрица кандидатов `11x6` имеет ранг `5`, максимум `5/6`, проходов `0/11`.
- Отдельные RG- и K43-факторы внутренни, но каждый неполон; их произведение
  тавтологично без общего операторного носителя.
- Размерная карта остаётся `2/2`: отношение является зависимой строкой и
  не устраняет ни скоростную, ни общую масштабную свободу.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-birth-tick-k43-rg-boundary-matching-origin-gate]] — вывод требуемого отношения.
- [[version10-cell-birth-four-volume-induced-newton-dimensional-transmutation-beta-parent-origin-gate]] — RG-фактор.
- [[version10-cell-birth-four-volume-spectral-counting-measure-origin-gate]] — K43-фактор.
- [[current-status-and-next-vectors]] — общий фронтир.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_candidate_audit.py`