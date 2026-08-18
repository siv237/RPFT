# Обменный Real-символ степени семь

> Status: working
> Type: question
> Updated: 2026-08-17

## Summary

Сверка соглашений исправила ошибку предыдущего гейта: в ковариантной
таблице real K-theory boundary имеет вид `KO_n -> KO_(n-1)`. Поэтому для
выхода в `KO6` нужен символ степени 7, а не 5.

## Result

Пусть `B=M105(C)_R`, а `kappa_15=[T_R]=15 in KO6(B)` — уже доказанный
обменный коэффициентный класс. Канонический генератор вещественной
групповой алгебры даёт winding-класс `[u_R] in KO1(C*_R(Z))`. Тогда

`xi_15=[u_R] external_product kappa_15 in KO7(C*_R(Z) tensor B)`.

Модульность Toeplitz boundary даёт

`partial_7(xi_15)=+/-15 in KO6(B)`.

После согласования ориентации комплексификация равна `(-15,+15)`, а
нормированный вес остаётся `1/7`.

## Status Boundary

Классовая факторизация через неограниченный extension закрыта. Ещё не
записан единичный матричный представитель `xi_15` в унитарной модели
`KO7`; физическое действие также не получено.

## Links

- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version5-real-toeplitz-bott-comparison-map-gate]]
- [[one-seventh-boundary-transgression-literature-2026]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_degree_seven_symbol_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_degree_seven_symbol_gate_results.json`
- Bourne--Kellendonk--Rennie, `arXiv:1604.02337v3`, Proposition 3.3.
- Boersema--Loring, `arXiv:1504.03284v3`, Sections 7--9.
- Boersema--Schochet, `arXiv:2407.05880v4`, Examples 10.2--10.7.