# Типизированное K43-вложение минимального SU(2)+8D носителя

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Разложение `K43=(C² tensor C¹⁶) direct_sum C¹¹` реализует шестнадцать
вейлевских `SU(2)`-дублетов, даёт точно `b=-2` и проходит обе anomaly-
проверки. Но активный gauge-инвариантный проектор не может иметь ранг один.

## Key Points

- Активный сектор имеет размерность `32`, синглетное дополнение — `11`.
- `Tr(T_a T_b)=8 delta_ab`, поэтому `b=-22/3+16/3=-2`.
- Локальная кубическая аномалия равна нулю; Witten parity равна нулю.
- Размерность коммутанта равна `377`, поэтому вложение не выбрано уникально.
- Активный rank-one pole имеет gauge defect `1`.
- Инвариантный rank-one pole лежит в синглетах и не пересекает AF-сектор.
- Минимальный инвариантный активный проектор имеет ранг `2`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-discrete-resolution-transmuted-mode-asymptotically-free-anomaly-free-carrier-candidate-audit-gate]] — выбор кандидата.
- [[version10-cell-birth-four-volume-nonequilibrium-bath-discrete-resolution-transmuted-mode-spectral-pole-parent-origin-gate]] — требуемый ранговый полюс.
- [[current-status-and-next-vectors]] — общий фронтир.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate_results.json`