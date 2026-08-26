# Version VII: полный гессиан и относительные моды рёбер

> Status: working
> Type: question
> Updated: 2026-08-26

## Summary

Полный 72-мерный гессиан исправленного поля вычислен в rank-21 минимуме.
Минимум устойчив поперёк, но не изолирован: три физические кромки имеют
независимые семейные кадры.

## Exact Vacuum

Для каждого ребра:

`X_a X_a* = I3`, `X_a* X_a = P3`, поэтому `X_a = U_a V`.

Вакуумное многообразие:

`M_vac = U(3)_u x U(3)_d x U(3)_e`, `dim_R = 27`.

## Hessian

В trace-метрике:

- отрицательных направлений: `0`;
- нулевых: `27`;
- положительных: `45`;
- ненулевые уровни: `(4/45)^18` и `(16/45)^27`.

Даже после удаления гипотетического общего `U(3)` остаются `18`
относительных мод. В вещественном пределе остаются как минимум `6`.

## Meaning

Функционал фиксирует ранги и сингулярные числа, но не выбирает взаимную
ориентацию рёбер `u,d,e`. Поэтому наличие относительных матриц ещё не является
выводом CKM или PMNS.

## Next Gate

Нужно проверить физические двухформы и junk-фактор на всём трёхрёберном
модуле. Только канонический перекрёстный член, чувствительный к
`U_a U_b*`, может поднять относительные нули без ручного портала.

## Subsequent Result

[[version7-common-higgs-degree-two-cross-edge-gate]] закрыл прямой
физический маршрут: при одном общем Хиггсе смешанные произведения разных
рёбер равны нулю до junk, а физический бимодульный коммутант диагонален.
Следующий кандидат должен иметь выведенную квартичную или более высокую
степень.

## Links

- [[version7-affine-physical-module-canonical-lift-gate]]
- [[version7-chiral-hodge-index-instability-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-rank-one-tangent-junk-gate]]
- [[version7-relative-edge-formula-intuition-map]]
- [[version7-common-higgs-degree-two-cross-edge-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_corrected_vacuum_relative_edge_hessian_gate.tex`
- `s2t/audits/s2t_v7_corrected_vacuum_relative_edge_hessian_gate.py`
- `s2t/results/s2t_v7_corrected_vacuum_relative_edge_hessian_gate_results.json`