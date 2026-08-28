# Version VII: аффинное дефектное дополнение бикомплекса

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, является ли совпадение `54-42=12=dim_C E_aff` каноническим
аффинным дополнением связывающего носителя.

## Search for Solution

Связывающая кривизна на полной цепи `11 -> 21 -> 10` тождественно нулевая
на средней 21-мерной ступени. Сжатие к концам даёт минимальный носитель
размерности `21` и точно сохраняет след. Нулевое дополнение меняет полную
размерность, не меняя действие, поэтому разность `54-42=12` неинвариантна;
для минимальной опоры разность равна `33`.

Дополнительно вычислено представление `E_aff`:
`1 + 2 + 2*3 + 3'`. У предполагаемого дефекта действие `S4` не задано;
при тривиальном действии эквивариантная карта имеет ранг не выше единицы.
Выбор самого дефектного подпространства лежит в `Gr_C(42,54)` вещественной
размерности `1008`.

## Expected Result

- Аффинное дополнение не выведено.
- Совпадение `12=12` является эффектом выбранного нулевого контейнера.
- Общий качественный вакуум не затронут.
- Следующий гейт должен работать с минимальной фактической опорой
  кривизности, а не с полными размерами матричных контейнеров.

## Links

- [[version7-bicomplex-total-degree-hodge-metric-gate]]
- [[version7-minimal-curvature-support-trace-gate]]
- [[version7-affine-physical-module-canonical-lift-gate]]
- [[version7-index-defect-reduced-linking-quotient-gate]]
- [[version7-rank-change-parent-program]]

## Source Notes

- `s2t/gates/version7_affine_defect_bicomplex_completion_gate.tex`
- `s2t/audits/s2t_v7_affine_defect_bicomplex_completion_gate.py`
- `s2t/results/s2t_v7_affine_defect_bicomplex_completion_gate_results.json`