# Вакуумный отклик на дефицит замыкания

> Status: working
> Type: question
> Updated: 2026-08-18

## Summary

Детерминант теперь рассматривается как вторичный отклик на уже неизбежный
дефект. Замкнутый и дефектный квадратичные операторы различаются только
проектором ранга 15, поэтому относительный тепловой след конечен:

`K(t)=(1/7)(1-exp(-t))`.

При положительной щели `m` относительный детерминант вычисляется точно:

`Gamma_def=(1/7) log((m^2+a)/m^2)`.

Кратность `1/7` полностью фиксирована топологией, локальные UV-контрчлены
сокращаются. Но щель `m` не выведена, а при `a(R)=R^-2` отклик монотонно
убывает и не выбирает конечный радиус.

Для Real-пары ориентированный суперслед сокращается, тогда как
положительный модуль считает оба дефектных проектора и сохраняет вес
`30/210=1/7`. Выбор физической determinant-line меры остаётся открытым.

## Links

- [[version5-topological-closure-deficit-gate]]
- [[version5-fermionic-determinant-induced-skyrme-gate]]
- [[version4-pfaffian-eta-orientation-gate]]
- [[version4-determinant-line-inflow-gate]]
- [[index-supertrace-determinant-response-2026]]

## Source Notes

- `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex`
- `s2t/audits/s2t_v5_closure_deficit_induced_vacuum_response_gate.py`
- `s2t/results/s2t_v5_closure_deficit_induced_vacuum_response_gate_results.json`