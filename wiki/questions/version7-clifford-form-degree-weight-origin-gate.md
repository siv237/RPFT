# Version VII: происхождение веса из степени формы и следа Клиффорда

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Real-удвоение и один общий полуслед сохраняют равный вес двух Hodge-норм,
тогда как селективный запуск требует `beta<8/15` и проходит при `beta=1/2`.

## Search for Solution

Оба момента классифицированы как пространственно-временные нуль-формы и
чётные внутренние квадратичные моменты. Явный четырёхмерный клиффордов след
проверен на случайных двухформах и скалярах.

## Expected Result

Нормированный клиффордов след является изометрией Hodge-нормы. Половина в
`1/2 sum_{mu,nu}|F_mu_nu|²` только удаляет двойной подсчёт антисимметричных
индексов и не создаёт секторный вес. Получается `beta=1` и сигнатура
`(21,0,6)`, поэтому маршрут закрыт для текущего носителя.

## Links

- [[version7-real-half-trace-curvature-weight-gate]]
- [[version7-derived-relative-involution-curvature-norm-gate]]
- [[superconnection-curvature-norm-normalization-literature-2026]]
- [[clifford-form-degree-normalization-literature-2026]]
- [[version7-common-irreducible-trace-multiplicity-gate]]

## Source Notes

- `s2t/gates/version7_clifford_form_degree_weight_origin_gate.tex`
- `s2t/audits/s2t_v7_clifford_form_degree_weight_origin_gate.py`
- `s2t/results/s2t_v7_clifford_form_degree_weight_origin_gate_results.json`