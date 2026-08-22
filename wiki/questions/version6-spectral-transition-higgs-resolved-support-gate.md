# Том VI: хиггс-разрешённые опоры пакета 15

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

На области `H!=0` пакет поколения канонически разлагается как

`15 = 6_up + 6_down + 2_e + 1_nu`.

Проекторы ортогональны и gauge-ковариантны. Три заряженных блока имеют
степень-один дираковские рёбра. Нейтринная линия остаётся односторонней,
поскольку в `H15` отсутствует `nu_R`.

## Машинная проверка

- ранги проекторов: `6,6,2,1`;
- остаток суммы до единицы: `3.15e-16`;
- максимальный остаток `SU(2)`-ковариантности: `1.21e-15`;
- цветные коммутаторы: ноль;
- ранг тестового заряженного оператора: `14`;
- нульность: `1`;
- KO6-классы складываются в `15`, веса — в `1/7`.

Использованные ненулевые амплитуды были только тестом структуры. Значения
заряженных масс и абсолютный масштаб Хиггса не выведены.

## Граница результата

Нейтринный проектор

`P_nu(H)=tilde(H)tilde(H)^dagger/(H^dagger H)`

определён только при `H!=0`. Поэтому ранг один ещё нельзя объявить
глобальным элементарным объектом родителя.

## Следующий гейт

[[version6-spectral-transition-neutrino-line-parent-gate]] проверяет
глобальность нормированной линии и регулярность ненормированного
квадратичного носителя.

## Links

- [[version6-spectral-transition-component-colocalization-gate]]
- [[version5-h15-neutrino-degree-split-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[transition-primitive]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_higgs_resolved_support_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_higgs_resolved_support_gate.py`
- `s2t/results/s2t_v6_spectral_transition_higgs_resolved_support_gate_results.json`
