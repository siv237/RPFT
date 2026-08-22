# Version VI: родительская допустимость обменного моста

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Обменный мост совместим с базовой Real-симметрией и может быть представлен
одноформой, если гладкая алгебра содержит компактный идеал Тёплица. Однако
он отсутствует в замороженном физическом модуле одноформ `H15`, содержащем
только заряженные рёбра `u,d,e`.

## Exact Checks

- `R T_lambda = T_lambda* R`;
- `E01 [N,E10] = E00 = P0`;
- `P0` принадлежит компактному идеалу, но не одной символической алгебре
  окружности;
- ориентационно-обменного ребра нет в `Y_rho = E_rho tensor C3`.

## Verdict

Механизм скрытого класса не закрыт, но мост нельзя считать уже выведенной
физической модой. Требуется явный выбор: расширить координатную алгебру
гладкими компактами либо ввести мост как нечётный эндоморфизм
суперсвязности. Оба варианта должны заново пройти дифференциальный,
вариационный и мерный аудит.

Следующий гейт [[version6-exchange-bridge-minimal-parent-gate]] выбрал
нечётный Real-эндоморфизм как минимальный кинематический вариант, но его
каноническое положительное действие стабилизирует замкнутый мост, а не
дефектную пару.

## Links

- [[version6-common-configuration-space-gate]] — явное обратимое дополнение.
- [[fredholm-index-zero-invertible-completion-literature-2026]] — операторная литература.
- [[version5-h15-physical-oneform-bimodule-gate]] — замороженный модуль `u,d,e`.
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]] — оператор числа и компактный дефект.

## Source Notes

- `s2t/gates/version6_exchange_bridge_parent_admissibility_gate.tex`
- `s2t/audits/s2t_v6_exchange_bridge_parent_admissibility_gate.py`
- `s2t/results/s2t_v6_exchange_bridge_parent_admissibility_gate_results.json`