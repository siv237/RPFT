# Version VII: единый точный Hodge–cycle функционал

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, восстанавливают ли отброшенные ненулевые собственные значения
gauge-Casimir устойчивость down--weak сектора при одной тепловой шкале.

## Search for Solution

К точному физическому Gaussian-гессиану добавлен Hodge-тепловой гессиан

$$h_e(t)=8tc_e e^{-tc_e^2}$$

с уже выведенными `c_d=8/5` и `c_W=9/10`. Формальный общий функционал
записан одним градуированным следом на прямой сумме рёберного и физического
носителей. Свободный относительный численный коэффициент не вводился.

## Expected Result

Получен существенный частичный проход. При `t=1` полный 20-мерный тяжёлый
гессиан имеет сигнатуру `(0,0,20)` и минимальное собственное значение
`1.03081235398`. Положительность сохраняется до
`t*=2.36617354515`.

Однако семь корневых производных остаются ненулевыми, а градуированный
прямосуммовой след ещё не выведен квадратом одной физической
Real-суперсвязности. Следующий гейт —
[[version7-common-carrier-root-stationarity-gate]].

## Compliance Check

- Проверены 601 значение тепловой шкалы и уточнена граница окна.
- Down- и weak-секторы одновременно положительны в открытом интервале.
- Два запуска дали одинаковый SHA-256.
- Статус: `heavy Hessian partial pass; common carrier and roots open`.

## Links

- [[version7-exact-hodge-cycle-project-intuition-search]]
- [[version7-weak-aligned-cycle-competition-gate]]
- [[version7-common-carrier-root-stationarity-gate]]
- [[hodge-heat-superconnection-literature-2026]]

## Source Notes

- `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex`
- `s2t/audits/s2t_v7_exact_profile_hodge_cycle_unification_gate.py`
- `s2t/results/s2t_v7_exact_profile_hodge_cycle_unification_gate_results.json`