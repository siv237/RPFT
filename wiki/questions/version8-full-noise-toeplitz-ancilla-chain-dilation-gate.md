# Toeplitz-конвейер свежих ancilla полного шумового процесса

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

Оператор числа и двусторонний сдвиг ранней Toeplitz-ветви подняты на
двустороннюю цепь 43-мерных collision-ячеек. Один фиксированный глобальный
Floquet-унитарий подводит к системе ранее не использованную vacuum-ячейку и
для любого конечного `n` точно возвращает редуцированную динамику
`Phi_h^n`. Внешний reset или ручная подмена ancilla между тактами больше не
нужны.

## Problem

Заменить внешнюю инструкцию «возьми следующую свежую ancilla» одним
автономно повторяемым глобальным квантовым шагом.

## Search for solution

- Переиспользованы `N e_n=n e_n`, `U^k e_n=e_(n+k)` и
  `[N,U^k]=kU^k`.
- Каждая ячейка типизирована как `C|0> direct_sum C^42_jump = C43`.
- Локальный star-collision соединён со сдвигом одинаковых ячеек.
- Редукция доказана конечной цилиндрической индукцией, поэтому бесконечная
  матрица не строится.
- Gauge-действие продолжено одинаково на каждую ячейку.

## Expected result

Один и тот же унитарий должен реализовать произвольное конечное число
итераций канала, не возвращая использованную ячейку к системе.

## Compliance check

- Dimensions: system `21`, jumps `42`, cell `43`.
- Counter: `[N,U^k]=kU^k` exactly.
- Used-cell revisit: `false`.
- Reduced dynamics: `Phi_h^n` for all finite `n>=0`.
- External per-step reset: `false`.
- Gauge covariance: cell-wise.
- Реестр: `23/153`; тесты: `33 passed`.
- Boundary: product-vacuum chain, её parent и time-independent local
  Hamiltonian ещё не выведены.

## Links

- [[version8-time-mechanism-project-archaeology]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version6-single-thread-c4-suspension-parent-gate]]
- [[version8-full-noise-repeated-interaction-hamiltonian-gate]]
- [[version8-full-noise-physical-time-scale-no-go-gate]]

## Source Notes

- `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex`
- `s2t/audits/s2t_v8_full_noise_toeplitz_ancilla_chain_dilation_gate.py`
- `s2t/results/s2t_v8_full_noise_toeplitz_ancilla_chain_dilation_gate_results.json`
- `s2t/proofdsl/examples/version8_full_noise_toeplitz_ancilla_chain.py`