# Том VI: аномалия и тёплицев внешний продукт

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, может ли внешний индексный продукт автоматически превратить
единичный сфалеронный поток в проектный Real-класс `15`.

## Search for solution

Относительно слабой группы физический носитель одного поколения равен

`H15|SU(2) = 4[doublet] + 7[singlet]`.

На нём действуют две разные аддитивные карты:

- забывающая размерность: `4*2+7*1=15`;
- сфалеронное индексное спаривание: `4*1+7*0=4`.

Формальный неэквивариантный продукт единичного потока с уже заданным
проектором `q0` ранга `15` действительно имеет индекс `15`. Однако он
получает это число из входного ранга и заменяет физические дублеты и
синглеты пятнадцатью одинаковыми активными копиями.

## Expected result

Физический мост требовал сохранения `SU(2)`-представлений, хиральности и
Real-структуры. В этом случае продукт должен был самостоятельно вывести
`15`, а не использовать `rank(q0)=15` как предпосылку.

## Compliance check

Эквивариантный продукт возвращает физический поток `4`, а не `15`.
Компонентные сравнения также несовместимы с общей перенормировкой:

- проектные ранги: `(12,3)`;
- сфалеронные потоки: `(3,1)`;
- отношения: `(4,3)`.

Формальные Real-индексы `(-15,+15)` и физические `(-4,+4)` имеют нулевые
обычные суммы, но не являются одной парой.

Итак, стандартный сфалерон не выводит класс `15`. Этот класс сохраняется
как классификационный ledger полного поколения, но не как доказанная
кратность рождения.

## Следующий гейт

[[version6-spectral-transition-class15-physical-role-branch-decision-gate]]
выбрал первую ветвь: `15` зафиксирован как классификационный ledger
полного поколения, но не как multiplicity рождения. Новая динамика
полного конечного оператора допустима только как отдельно объявленная
модель. Скрыто продолжать сфалеронный маршрут запрещено.

## Links

- [[version6-spectral-transition-sphaleron-spectral-flow-gate]]
- [[version6-spectral-transition-minimal-support-gate]]
- [[version6-spectral-transition-component-boundary-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_anomaly_to_toeplitz_product_map_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_anomaly_to_toeplitz_product_map_gate.py`
- `s2t/results/s2t_v6_spectral_transition_anomaly_to_toeplitz_product_map_gate_results.json`
- M. F. Atiyah, I. M. Singer, *The Index of Elliptic Operators: I* (1968).
- M. F. Atiyah, V. K. Patodi, I. M. Singer, *Spectral Asymmetry and Riemannian Geometry I* (1975).
- G. G. Kasparov, *The Operator K-Functor and Extensions of C*-Algebras* (1981).
- F. R. Klinkhamer, C. Rupp, *Sphalerons, Spectral Flow, and Anomalies* (2003).