# Том VI: компонентные observables рождения

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

После фиксации класса `15` как ledger проверено, остаётся ли в текущей
архитектуре параметрически чистая вероятность или branching ratio
рождения для компонент `12` и `3`.

## Search for solution

Сопоставлены четыре точных набора:

- компонентные K-ранги: `(12,3)`, отношение `4:1`;
- физический сфалеронный поток: `(3,1)`, отношение `3:1`;
- аномальные заряды: `(Delta B,Delta L)=(1,1)`;
- хиггс-разрешённые опоры: `(6,6,2,1)`.

Нормированные двухкомпонентные кандидаты равны соответственно
`(4/5,1/5)`, `(3/4,1/4)` и `(1/2,1/2)`. Они различны.

## Expected result

Настоящая вероятность требовала единой меры на траекториях, переходной
энергии, температуры или неравновесного состояния, real-time оператора и
динамического prefactor.

## Compliance check

Текущая версия строго сохраняет:

- классы `(12,3)` и веса `(4/35,1/35)`;
- поток `(3,1)`;
- `Delta B=Delta L=1` и сохранение `B-L`;
- возможность локальной смены ранга `W_nu:0→1` при `H=0`.

Но не выводит:

- branching ratio кваркового и лептонного каналов;
- абсолютную скорость;
- multiplicity частиц;
- массу и размер конечного продукта;
- вероятность получения устойчивой материи.

Следовые веса не являются вероятностями рождения.

## Следующий гейт

[[version6-spectral-transition-dynamic-closure-status-gate]] сведёт
полный ledger спектральной ветви и определит, какие уровни программы
закрыты, а где неизменённая архитектура должна остановиться.

## Links

- [[version6-spectral-transition-class15-physical-role-branch-decision-gate]]
- [[version6-spectral-transition-component-boundary-gate]]
- [[version6-spectral-transition-sphaleron-spectral-flow-gate]]
- [[version6-spectral-transition-higgs-resolved-support-gate]]
- [[version6-matter-birth-program]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_componentwise_creation_observable_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_componentwise_creation_observable_gate.py`
- `s2t/results/s2t_v6_spectral_transition_componentwise_creation_observable_gate_results.json`
- F. R. Klinkhamer, C. Rupp, *Sphalerons, Spectral Flow, and Anomalies* (2003).
- V. A. Kuzmin, V. A. Rubakov, M. E. Shaposhnikov, *On the Anomalous Electroweak Baryon Number Nonconservation in the Early Universe* (1985).
- G. D. Moore, *Measuring the Broken Phase Sphaleron Rate Nonperturbatively* (1999).
- M. Barroso Mancha, G. D. Moore, *The Sphaleron Rate from 4D Euclidean Lattices* (2023).