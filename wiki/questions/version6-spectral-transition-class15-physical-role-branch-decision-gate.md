# Том VI: физическая роль класса пятнадцать

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

После закрытия сфалеронного и product-map мостов требовалось окончательно
решить, является ли класс `15` физической кратностью рождения или только
классификационным объектом.

## Search for solution

Сведены предыдущие сертификаты:

- класс `15` строго существует в `KO6` и тёплицевой границе;
- минимальная физическая опора раскладывается как `12+3`;
- компоненты имеют самостоятельные циклы и не колокализованы;
- хиггс-разрешённый носитель равен `6+6+2+1`;
- сфалерон является седлом и имеет физический поток `4`;
- формальный product даёт `15` только из готового `rank q0`;
- физический эквивариантный product снова равен `4`.

## Expected result

Решение должно сохранить доказанный K-класс, но удалить физические
интерпретации, для которых нет общего оператора, локализации и динамики.

## Compliance check

Для версии VI выбран статус:

`15 = классификационный ledger полного пакета одного поколения`.

Он не является доказанным:

- числом частиц;
- рангом одного связанного солитона;
- числом сфалеронных пересечений;
- кратностью единого события рождения поколения.

Классы `12` и `3`, разложение `6+6+2+1`, вес `1/7` и Real/Toeplitz-пара
сохраняются. Новая динамика, одновременно действующая на слабые дублеты
и синглеты, должна быть объявлена отдельной моделью.

## Следующий гейт

[[version6-spectral-transition-componentwise-creation-observable-gate]]
показал, что текущая версия фиксирует целочисленные и зарядовые selection
rules, но не единую вероятность. Нормированные кандидаты из рангов,
потоков и зарядов равны соответственно `(4/5,1/5)`, `(3/4,1/4)` и
`(1/2,1/2)`; они несовместимы без нового динамического закона.

## Links

- [[version6-spectral-transition-anomaly-to-toeplitz-product-map-gate]]
- [[version6-spectral-transition-sphaleron-spectral-flow-gate]]
- [[version6-spectral-transition-component-boundary-gate]]
- [[version6-spectral-transition-component-colocalization-gate]]
- [[version6-matter-birth-program]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_class15_physical_role_branch_decision_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_class15_physical_role_branch_decision_gate.py`
- `s2t/results/s2t_v6_spectral_transition_class15_physical_role_branch_decision_gate_results.json`
- M. F. Atiyah, I. M. Singer, *The Index of Elliptic Operators: I* (1968).
- G. G. Kasparov, *The Operator K-Functor and Extensions of C*-Algebras* (1981).
- T. Krajewski, *Classification of Finite Spectral Triples* (1998).