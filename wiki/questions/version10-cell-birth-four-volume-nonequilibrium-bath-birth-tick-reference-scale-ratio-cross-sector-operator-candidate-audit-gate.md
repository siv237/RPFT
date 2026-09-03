# Аудит межсекторных операторов RG--K43

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Восемь кандидатов дали `0/8`: формальные смешанные члены существуют, но ни
один унаследованный кандидат не имеет одновременно ненулевой блок и
выбранный некруговой коэффициент.

## Key Points

- Матрица `8x6` имеет ранг `5`, максимум `5/6`.
- Формальные смешанные блоки: `5/8`; унаследованные выбранные: `0`.
- Portal `[[1,lambda],[lambda,1]]` устойчив при `|lambda|<1`, но является новым входом.
- Физическое происхождение оператора, коэффициента и общего носителя: `0/3`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-birth-tick-reference-scale-ratio-common-parent-origin-gate]] — требование смешанного блока.
- [[current-status-and-next-vectors]] — общий фронтир.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_reference_scale_ratio_cross_sector_operator_candidate_audit_gate_results.json`