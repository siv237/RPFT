# Двухкомпонентная source-parent архитектура дополнительных щелей

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Какова минимальная устойчивая архитектура, реализующая произвольную пару
центральных щелей без введения новой матрицы жёсткости?

## Search for solution

- Наследована trace-метрика `diag(12,48)` на базисе `A,B`.
- Квадратичный функционал дополнен двумя линейными источниками `j_A,j_B`.
- Точно вычислены минимум, source-to-gap map и обратная карта.
- Проверены минимальность числа источников и совместимость с симметриями.

## Expected result

Два вещественных источника должны биективно параметризовать двумерную
плоскость щелей, а положительность должна следовать из уже выведенного следа.

## Compliance check

- `Hess V=diag(12,48)>0`.
- Единственный минимум: `(a*,b*)=(j_A/12,j_B/48)`.
- Определитель source-to-gap map равен `1/72`.
- Обратная карта: `j_A=6(Delta_u-Delta_d)`, `j_B=6(Delta_u+Delta_d)`.
- Один источник недостаточен; два необходимы и достаточны.
- Architecture-ledger `9/9`; source-origin `0/2`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-central-hamiltonian-parent-action-origin-gate]]
- [[extra-edge-mass-two-source-parent-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate_results.json`