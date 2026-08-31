# Минимальная typed-архитектура бинарного u/d-различителя

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Каков минимальный единый носитель, превращающий две фиксированные
incidence-геометрии в состояния одной статической и динамической системы?

## Search for solution

- Построен gauge-тривиальный бинарный носитель `C²`.
- Построен управляемый endpoint-проектор ранга `12`.
- Квадратичные гиперзарядные индексы записаны как двухуровневый гамильтониан.
- Сопоставлены унитарная динамика, нуль-температурный скачок и конечная
  detailed-balance пара.

## Expected result

Архитектура должна иметь единственное статическое основное состояние и
явно отделять его от механизма реальной релаксации.

## Compliance check

- `C²` минимален для двух ортогональных ненулевых проекторов.
- `H_inc=(29/6)I+(7/2)sigma_z`, щель равна `7`.
- При положительном коэффициенте основное состояние — `d`.
- Унитарный коммутатор имеет двумерную неподвижную алгебру и не меняет
  популяции.
- Скачок `|d><u|` имеет Heisenberg-ранг `3`, fixed algebra `C I2` и
  единственное стационарное состояние `|d><d|`.
- Конечная температура оставляет отношение популяций `exp(-7 beta gamma)`;
  чистый выбор возникает лишь при нулевой температуре.
- Static architecture `8/8`, conditional relaxation `5/5`, origin `0/5`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-parent-origin-gate]]
- [[binary-incidence-dynamics-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_architecture_gate_results.json`