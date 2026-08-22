# Оператор числа, сдвиг и абсолютная кратность намотки

> Status: working
> Type: source
> Updated: 2026-08-21

## Краткий вывод

Неограниченный оператор числа на `ell2(Z)` хранит полный целый номер
обхода, тогда как конечная голономия хранит только его остаточный класс.
Компрессия степеней двустороннего сдвига даёт индекс, пропорциональный
целому winding-числу.

## Первичные источники

- C. Bourne, J. Kellendonk, A. Rennie, *The K-theoretic bulk–edge
  correspondence for topological insulators*, Annales Henri Poincaré 18
  (2017), 1833–1866, `arXiv:1604.02337` — неограниченный модуль
  расширения Тёплица с оператором числа.
- F. Arici, B. Mesland, *Toeplitz extensions in noncommutative topology
  and mathematical physics*, `arXiv:1911.05823` — обзор расширений
  Тёплица и неограниченных представителей.

## Значение для проекта

В проекте уже доказаны `N e_n=n e_n`, `U e_n=e_(n+1)`, `[N,U]=U`, индекс
компрессии `U^k`, равный `-k`, и Real-обмен `N↔-N`, `U↔U*`.

Эта структура подходит на роль абсолютного счётчика проходов одной нити.
Проектные `C4`, `Z3` и `Z6` тогда являются конечными проекциями полного
целого числа. Открытым остаётся переход от спектрального номера к
геометрически разнесённым виткам конечной толщины.

## Связи

- [[version6-single-thread-c4-suspension-parent-gate]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[version5-toeplitz-parent-action-variational-gap-gate]]
- [[version6-single-thread-global-cycle-sewing-gate]]

## Исходные материалы

- `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex`
- `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex`
- `s2t/gates/version6_single_thread_c4_suspension_parent_gate.tex`
- `s2t/results/s2t_v6_single_thread_c4_suspension_parent_gate_results.json`