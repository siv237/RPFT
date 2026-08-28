# Version VII: кратности общего неприводимого следового носителя

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Real-полуслед, степень формы и нормированный клиффордов след сохраняют
`beta=1`, тогда как селективный запуск требует `0 <= beta < 8/15`.

## Search for Solution

Проверены полный след, нормированные corner-следы, равномерные кратности,
простой completion `M43(C)`, ранги `22/20` и проекторы рангов `11/10`.

## Expected Result

Обычный общий след сохраняет `beta=1`. Число `11/21` условно проходит и
даёт тяжёлую щель `4/35`, но честная вставка source-проектора оставляет один
Gram-конец и даёт `(8,0,19)`. Поэтому размерностный резонанс ещё не является
одним действием; требуется передаточная карта на самой кривизне.

## Links

- [[version7-clifford-form-degree-weight-origin-gate]]
- [[version7-real-superconnection-common-trace-origin-gate]]
- [[version7-derived-relative-involution-curvature-norm-gate]]
- [[finite-factor-trace-multiplicity-literature-2026]]
- [[version7-incidence-transfer-markov-weight-gate]]

## Source Notes

- `s2t/gates/version7_common_irreducible_trace_multiplicity_gate.tex`
- `s2t/audits/s2t_v7_common_irreducible_trace_multiplicity_gate.py`
- `s2t/results/s2t_v7_common_irreducible_trace_multiplicity_gate_results.json`