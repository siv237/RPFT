# Аудит кандидатов IR-массового члена трансмутированной моды

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Одиннадцать механизмов дают `0/11`: ни один текущий кандидат не выводит
точный IR-массовый член без круговой подстановки. Асимптотическая свобода с
`b=-2` условно воспроизводит точную обратную экспоненту, но текущий носитель
имеет противоположный знак `b=+2`.

## Key Points

- Критериальная матрица `11x6` имеет полный ранг `6`.
- Лучшие кандидаты получают `5/6`, но точного некругового прохода нет.
- KMS thermal mass и конечный объём не выбирают показатель `64 pi²/3`.
- Формальный массовый член и наблюдаемый полюс являются target-loaded.
- При `b_AF=-2`, `g²=3/8` получается точно `m²/mu²=exp(-64 pi²/3)`.
- Физическое происхождение beta-знака, AF-носителя и связи с полюсом: `0/3`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-discrete-resolution-transmuted-mode-spectral-pole-parent-origin-gate]] — условный полюс.
- [[version10-cell-birth-four-volume-induced-newton-dimensional-transmutation-beta-parent-origin-gate]] — унаследованный положительный beta-знак.
- [[current-status-and-next-vectors]] — общий фронтир.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_ir_mass_term_candidate_audit_gate_results.json`