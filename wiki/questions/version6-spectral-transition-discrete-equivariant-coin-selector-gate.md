# Том VI: эквивариантный селектор дискретной монеты

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, выбирает ли физическая алгебра Стандартной модели единственную
нескалярную локальную монету после скалярного запрета полного бимодуля.

## Search for solution

Монета классифицирована на точном разложении
`H15 = Q_L(6) + L_L(2) + u_R(3) + d_R(3) + e_R(1)`.
Проверены центральные проекторы, секторные `U(2)`-вращения и слабая
ковариантность ранг-один селектора.

## Expected result

Успех требовал единственного нескалярного блока, который одновременно
задаёт полный физический endpoint без внешнего Хиггса и юкавской амплитуды.

## Compliance check

- существуют не менее пяти независимых секторных монет;
- после удаления общего угла остаются четыре относительных угла;
- единственный центральный ранг один — `e_R`;
- `e_R` является только правым хиральным концом, а не массивной частицей;
- его калибровочно замкнутая опора `L_L + e_R` имеет ранг три;
- выбор одной компоненты `L_L` требует направления Хиггса;
- постоянного нейтринного проектора ранга один нет;
- единственная физическая монета, endpoint и новое число не выведены.

## Следующий гейт

[[version6-spectral-transition-discrete-chiral-coin-closure-gate]] проверит,
является ли монета на `L_L + e_R` новой динамикой или только дискретной
записью старого хиггсовско-юкавского ребра.

## Links

- [[version6-spectral-transition-discrete-nonlinear-parent-reopening-gate]]
- [[version5-physical-corner-connection-classification-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_equivariant_coin_selector_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_equivariant_coin_selector_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_equivariant_coin_selector_gate_results.json`