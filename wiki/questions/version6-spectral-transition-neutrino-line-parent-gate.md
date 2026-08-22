# Том VI: родитель нейтринной линии

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Нормированная нейтринная линия не является глобальным parent-объектом.
Она неизбежно сингулярна при `H=0`.

Однако существует регулярный ненормированный ковариант

`W_nu(H)=tilde(H)tilde(H)^dagger`,

который имеет ранг один при `H!=0` и обращается в нулевой оператор при
`H=0`.

## Строгий no-go

Коммутант фундаментального `SU(2)`-дублета одномерен и состоит из
скаляров. Поэтому постоянные инвариантные проекторы имеют ранги только
`0` и `2`.

Точка `H=0` фиксирована всей группой. Эквивариантное продолжение
ранг-один проектора потребовало бы инвариантного проектора ранга один,
которого нет. Два направления приближения к нулю дают проекторы на
расстоянии `sqrt(2)`.

## Положительный остаток

- `W_nu` полиномиален второй степени и непрерывен;
- паринговый тензор `B_nu=tilde(H)tilde(H)^T` также ковариантен;
- остатки ковариантности не выше `6.23e-15`;
- семейная компрессия `P0 tensor W_nu` имеет ранг `1` при `H!=0` и
  ранг `0` при `H=0`.

Это даёт язык рождения спектральной опоры: не вечная внутренняя линия,
а переход ранга `0 -> 1` вместе с ненулевым Хиггсом.

## Что остаётся открытым

Оператор Вайнберга структурно допустим, но проект пока не вывел:

- его коэффициент и подавляющий масштаб;
- семейную симметричную матрицу;
- источник нарушения лептонного числа;
- единый нелинейный функционал рождения ненулевого `H` и паринга.

Последующий [[version6-spectral-transition-weinberg-pairing-parent-gate]]
показал, что тип паринга и одна семейная ось доступны, но коэффициент,
полный семейный тензор и масштаб родителем не фиксируются.

## Links

- [[version6-spectral-transition-higgs-resolved-support-gate]]
- [[version6-spectral-transition-weinberg-pairing-parent-gate]]
- [[version5-h15-neutrino-degree-split-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[transition-primitive]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_neutrino_line_parent_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_neutrino_line_parent_gate.py`
- `s2t/results/s2t_v6_spectral_transition_neutrino_line_parent_gate_results.json`
- T. Krajewski, *Classification of Finite Spectral Triples* (1998).
- A. H. Chamseddine, A. Connes, M. Marcolli, *Gravity and the Standard
  Model with Neutrino Mixing* (2007).
- S. Weinberg, *Baryon- and Lepton-Nonconserving Processes* (1979).
