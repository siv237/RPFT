# Version VII: бикомплекс полной степени и Hodge-метрика

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, устраняют ли бикомплекс, полная степень, Real-структура или
Hodge-звезда свободу относительной метрики блоков размерностей `54` и `42`.

## Search for Solution

Построен точный квадратный бикомплекс. Перескалирование одного дифференциала
`d_v -> c d_v` сохраняет нильпотентность, антикоммутатор и полную степень при
всех `c>0`. Для общего кривизностного носителя явно построено семейство
положительных метрик `G_eta=P_E+eta P_L` и Real-совместимых изометрических
Hodge-инволюций при всех `eta>0`.

Унитарный обмен блоков невозможен: максимальная изометрия `42 -> 54`
оставляет ортогональный дефект размерности `12`. Это число совпадает с
`dim_C E_aff`, но каноническое отождествление пока отсутствует.

## Expected Result

- Total-degree и Hodge-звезда не фиксируют `eta`.
- Качественные сигнатуры остаются `(7,0,20)` и `(0,0,27)`.
- Вакуумные спектры при разных `eta` не связаны общим масштабом, поэтому
  отношения масс не выведены.
- Новый конкретный след — дефект `54-42=12`, совпадающий с размерностью
  аффинного носителя. Следующий гейт проверяет, является ли он каноническим
  дополнением, способным сделать бикомплекс неприводимым.

## Links

- [[version7-common-chain-number-hodge-relative-trace-gate]]
- [[version7-affine-defect-bicomplex-completion-gate]]
- [[version7-clifford-form-degree-weight-origin-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[clifford-form-degree-normalization-literature-2026]]

## Source Notes

- `s2t/gates/version7_bicomplex_total_degree_hodge_metric_gate.tex`
- `s2t/audits/s2t_v7_bicomplex_total_degree_hodge_metric_gate.py`
- `s2t/results/s2t_v7_bicomplex_total_degree_hodge_metric_gate_results.json`