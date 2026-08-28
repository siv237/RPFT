# Version VII: высшие характеры и заморозка ветви смешивания

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Высшие степени спектрального оператора действительно создают новые
циклические характеры: `ReTr W_C^2` впервые появляется в `Tr D^12`, а
`ReTr W_C^3` — в `Tr D^18`. Но это не даёт параметр-свободного вывода
семейного смешивания.

Все отдельно проверенные моменты степеней `6,8,...,30` выбирают центральный
минимум `W_C=-I3`. Нецентральная собственная фаза возможна только после
настройки отношения разных коэффициентов спектрального профиля. Кроме того,
одна классовая функция не выбирает собственные семейные оси и потому не
определяет полную CKM/PMNS.

## Exact Character Structure

Для единственного шестирёберного цикла

$$
\operatorname{Tr}D^{2n}=A_{2n}(r)+
\sum_{m=1}^{\lfloor n/3\rfloor}
a_{2n,m}(r)\operatorname{ReTr}W_C^m.
$$

Первое появление `m`-го оборота:

$$
k_{\min}(m)=6m.
$$

В частности,

$$
[\operatorname{Tr}D^{12}]_{\mathrm{hol}}
=(360r^4+1560r^6+3072r^8+2592r^{10})\operatorname{ReTr}W_C
+12r^8\operatorname{ReTr}W_C^2.
$$

## Tuned Loophole

Потенциал двух характеров

$$
V=a\operatorname{ReTr}W_C+b\operatorname{ReTr}W_C^2
$$

имеет внутреннюю собственную фазу только при `b>0` и `|a|<4b`. Для
комбинации `c6 TrD6+c12 TrD12` при `r=1` это требует

$$
-636<c_6/c_{12}<-628.
$$

Такое отношение не выводится из `H15`; его выбор был бы настройкой профиля.

## Structural No-Go

В семейно-слепом подъёме

$$
D(r,W_C)\simeq\bigoplus_{j=1}^3D(r,e^{i\theta_j}),
\qquad
S_f(W_C)=\sum_jF_f(\theta_j).
$$

Поэтому действие зависит только от собственных фаз и инвариантно при
`W_C -> U W_C U†`. Оно не выбирает относительные up/down-оси. Даже
нецентральный спектр одной голономии не равен выводу CKM.

## Status Boundary

Закрыто:

- ближайшая лазейка индивидуальных высших моментов;
- параметр-свободный вывод CKM/PMNS из одной циклической классовой функции;
- повторное продолжение этой ветви без нового семейного объекта.

Открыто:

- эндогенный масштаб Hodge-родителя;
- второй независимо выведенный некоммутирующий семейный тензор;
- повторное открытие смешивания после появления такого тензора.

## Next Gate

Вернуться к проблеме масштаба и проверить, может ли уровень Hodge-момента
возникнуть из нормировки или динамики самого родителя без коэффициентов
спектрального профиля. Ветвь смешивания не открывать до появления второго
некоммутирующего семейного тензора.

## Links

- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-theorem-and-no-go-ledger]]
- [[live-formulas-gates-version7-27]]

## Source Notes

- `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex`
- `s2t/audits/s2t_v7_higher_cycle_character_mixing_freeze_gate.py`
- `s2t/results/s2t_v7_higher_cycle_character_mixing_freeze_gate_results.json`