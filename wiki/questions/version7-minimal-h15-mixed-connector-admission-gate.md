# Version VII: минимальный смешивающий коннектор H15

> Status: mature
> Type: question
> Updated: 2026-08-26

## Summary

На фиксированных вершинах заряженного `H15` текущие рёбра `u,d,e` образуют
лес. Первый смешанный четырёхцикл требует ровно двух новых рёбер.

## Exact Classification

Полный перебор даёт три минимальных прямоугольника:

- `L_L-u_R` плюс `L_L-d_R`;
- `L_L-u_R` плюс `Q_L-e_R`;
- `L_L-d_R` плюс `Q_L-e_R`.

Только второй вариант реализуется одним комплексным мультиплетом
`R2=(3,2)_(7/6)` с сопряжённым полем. Два других варианта требуют также
независимый `R2_tilde=(3,2)_(1/6)`.

## Boundary

Это классификация минимального расширения, а не допуск новой частицы.
На момент этого гейта `R2` отсутствовал в текущем одноформенном бимодуле
`C^3`, а полное условие первого порядка и Real-совместимость ещё не были
проверены. Последующий результат приведён ниже.

Второй обычный хиггсовский дублет новых графовых рёбер не добавляет и этот
структурный no-go не снимает.

## Verdict

Неизменённый родитель остаётся закрыт. Единственный графово минимальный
одно-мультиплетный кандидат найден и направлен в отдельный admission-гейт.

## Subsequent Result

[[version7-r2-real-first-order-admission-gate]] показал, что оба ребра
кандидата меняют сразу две бимодульные координаты и потому нарушают строгое
условие первого порядка. Графовая минимальность сохранена как классификация,
но физический допуск в неизменённом родителе закрыт отрицательно.

## Links

- [[version7-quartic-cross-edge-invariant-admission-gate]]
- [[version7-r2-real-first-order-admission-gate]]
- [[version7-common-higgs-degree-two-cross-edge-gate]]
- [[version4-order-one-krajewski-square-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[mixed-connector-krajewski-leptoquark-literature-2026]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex`
- `s2t/audits/s2t_v7_minimal_h15_mixed_connector_admission_gate.py`
- `s2t/results/s2t_v7_minimal_h15_mixed_connector_admission_gate_results.json`