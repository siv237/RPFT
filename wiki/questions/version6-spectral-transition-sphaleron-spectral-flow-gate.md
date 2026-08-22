# Том VI: спектральный поток сфалерона

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, совпадает ли стандартный фермионный спектральный поток через
электрослабый сфалерон с проектным тёплицевым Real-классом ранга `15`.

## Search for solution

Для перехода между соседними gauge-вакуумами `Delta N_CS=1`. Один левый
`SU(2)`-дублет даёт одно ориентированное пересечение нуля. В одном
поколении имеются три цветовые копии `Q_L` и один `L_L`, поэтому поток
равен

`3 + 1 = 4`.

Правые синглеты `u_R,d_R,e_R` независимых слабых дублетных пересечений не
добавляют. Аномальные заряды равны `Delta B=Delta L=1`, поэтому `B-L`
сохраняется.

## Expected result

Настоящий мост к классу `15` требовал бы одного семейства операторов, в
котором сфалеронный поток, коэффициентный проектор `q0`, Real-структура и
аномальные веса возникают одновременно.

## Compliance check

Стандартный поток не совпадает с проектным классом:

- на поколение поток равен `4`, а не `15`;
- на три поколения поток равен `12`, но это `3*(3+1)`, а не проектный
  кварковый ранг `6+3+3=12` одного поколения;
- проектное разложение `15=12+3` считает полный левый и правый
  коэффициентный носитель, тогда как сфалерон видит `3+1` левых
  дублетных копий;
- сопряжённые ориентации дают обычную сумму потоков `+4-4=0`, что
  совместимо с Real-парой, но не выводит индексы `-15/+15`.

Итак, сфалерон подтверждает физическую осмысленность языка «переход через
нулевую моду», но не объясняет число `15`.

## Следующий гейт

[[version6-spectral-transition-anomaly-to-toeplitz-product-map-gate]]
показал, что формальный продукт даёт `15` лишь после забывания
`SU(2)`-действия и использования готового `rank(q0)=15`. Физическое
эквивариантное спаривание сохраняет дублеты и синглеты и возвращает
поток `4`. Прямой сфалеронный мост к классу пятнадцать закрыт.

## Links

- [[version6-spectral-transition-higgs-zero-finite-energy-saddle-gate]]
- [[version6-spectral-transition-minimal-support-gate]]
- [[version6-spectral-transition-component-boundary-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_sphaleron_spectral_flow_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_sphaleron_spectral_flow_gate.py`
- `s2t/results/s2t_v6_spectral_transition_sphaleron_spectral_flow_gate_results.json`
- F. R. Klinkhamer, C. Rupp, *Sphalerons, Spectral Flow, and Anomalies* (2003).
- F. R. Klinkhamer, Y. J. Lee, *Spectral Flow of Chiral Fermions in Nondissipative Yang–Mills Gauge Field Backgrounds* (2001).
- G. 't Hooft, *Computation of the Quantum Effects Due to a Four-Dimensional Pseudoparticle* (1976).
- M. F. Atiyah, V. K. Patodi, I. M. Singer, *Spectral Asymmetry and Riemannian Geometry I* (1975).