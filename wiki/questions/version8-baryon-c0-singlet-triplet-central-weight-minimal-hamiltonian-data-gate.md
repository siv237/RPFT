# Минимальные гамильтоновы данные центрального веса синглета и триплета

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

После факторизации общего нуля энергии всякий `SO(3)`-инвариантный
гамильтониан типа `1+3` имеет одну щель `Delta`. Равновесный вес зависит
только от `theta=beta Delta`:
`p=1/(1+3 exp(-theta))`, `r=exp(-theta)`.

Отображение `theta in R <-> p in (0,1)` биективно. Gibbs-вариационный
функционал строго выпуклый и имеет единственный минимум `p(theta)`, поэтому
`theta` является минимальным достаточным селектором. Но равновесие не
разделяет `beta` и физическую `Delta` и не задаёт скорость релаксации.
Текущий родитель не выводит `theta`: ledger `0/1`.

## Литературный вывод

MaxEnt требует заданных ограничений, Gibbs-вариация — заданного
гамильтониана, а detailed balance — заданного верного состояния. Эти
принципы проверяют достаточность `theta`, но не создают его.

## Связи

- [[singlet-triplet-gibbs-gap-literature-2026]]
- [[version8-baryon-c0-singlet-triplet-central-trace-weight-parent-origin-gate]]
- [[version8-kms-nontracial-relative-rate-selector-gate]]
- [[version4-gibbs-free-energy-carrier-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate_results.json`