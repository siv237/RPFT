# Неограниченный родитель цикла Тёплица

> Status: working
> Type: question
> Updated: 2026-08-17

## Summary

Оператор числа `N e_n=n e_n` на `ell2(Z)` канонически выводит
пространство Харди как `P=chi_[0,infinity)(N)`. Компрессии `PUP` и
`PU*P` являются операторами `S` и `S*`, поэтому индексы `-15/+15` и вес
`1/7` больше не требуют внешнего выбора поляризации.

## Passed

- `[N,U]=U` и `[N,U*]=-U*`.
- `(1+N^2)^(-1/2)` компактен.
- `P ell2(Z)=ell2(N0)=H2(S1)`.
- `PUP=S`, `PU*P=S*`.
- Комплексное сопряжение даёт `K N K=-N`, `K U K=U*`.
- Коэффициентный проектор ранга 15 воспроизводит класс и вес `1/7`.

## Degree Gap and Subsequent Closure

Стандартный неограниченный модуль расширения Тёплица записан как `KKO1`
с действием `Cl(0,1)`, но в ковариантной точной последовательности
boundary имеет вид `KO_n -> KO_(n-1)`. Для выходного класса `KO6`
необходим входной обменный Real-символ степени семь:
`7-1=6 mod 8`.

Последующий гейт построил его как
`xi_15=[u_R] external_product kappa_15` и получил
`partial_7(xi_15)=+/-15`.

## Verdict

Аналитический неограниченный родитель и внутренняя поляризация построены.
На момент этого гейта классовая факторизация оставалась открытой; теперь
она закрыта в [[version5-real-toeplitz-degree-seven-symbol-gate]].
Физическое действие не получено.

## Links

- [[version5-real-toeplitz-bott-comparison-map-gate]]
- [[version5-real-toeplitz-degree-seven-symbol-gate]]
- [[version5-real-toeplitz-cross-tome-reuse-audit-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[one-seventh-boundary-transgression-literature-2026]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_unbounded_parent_cycle_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_unbounded_parent_cycle_gate_results.json`
- Bourne--Kellendonk--Rennie, `arXiv:1604.02337v3`, Proposition 3.3.
- Arici--Mesland, `arXiv:1911.05823`.