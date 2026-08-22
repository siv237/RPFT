# Том VI: нелинейный дискретный родитель

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, может ли одно локальное нелинейное дискретное правило заменить
заранее заданный гладкий массовый профиль и одновременно выбрать
физический внутренний канал.

## Search for solution

Построено state-dependent квантовое блуждание на
`C2_dir tensor M20x15`: локальная монета зависит от билинеара состояния,
после чего две компоненты сдвигаются в противоположные стороны.

## Expected result

Успех требовал точного сохранения нормы, нелинейного дираковского предела,
ненулевого минимального размера и автоматического сокращения внутренней
кратности без внешнего проектора.

## Compliance check

- норма сохраняется с машинным остатком ниже `1e-12`;
- правило локально и имеет нелинейный дираковский предел;
- поведение зависит от свободной нелинейной связи `kappa`;
- физическое значение шага решётки не выведено;
- полная внутренняя ковариантность точна;
- коммутант полного бимодуля скалярен, поэтому сохраняются `300` каналов;
- единственная частица, устойчивый endpoint и новое число не получены.

## Следующий гейт

[[version6-spectral-transition-discrete-equivariant-coin-selector-gate]]
классифицирует нескалярные монеты для физической редуцированной алгебры.

## Links

- [[version6-spectral-transition-candidate-menu-retrospective-correction-gate]]
- [[version5-self-generated-transition-defect-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_nonlinear_parent_reopening_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_nonlinear_parent_reopening_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_nonlinear_parent_reopening_gate_results.json`