# Parent-origin минимального бинарного incidence-носителя

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Содержит ли существующий расширенный parent сам бинарный носитель,
off-diagonal jump и компенсирующую среду для релаксации `u->d`?

## Search for solution

- Классифицирован центр `P_u,P_d` и invariant-коммутант гиперзаряда.
- Вычислен gauge-вес `L_down=|d><u|`.
- Проверена ковариантность его GKSL-диссипатора.
- Проверено действие старого 42-frame на новый бинарный сектор.
- Классифицирован charged-singlet environment carrier и его семейные
  неподвижные векторы.

## Expected result

Полный проход требовал системного jump, единственной компенсирующей
environment-линии, gauge-инвариантного взаимодействия, резонанса, состояния
среды и физической скорости.

## Compliance check

- Классическая алгебра `C P_u direct_sum C P_d` уже существует.
- Invariant off-diagonal Hom равен нулю.
- `L_down` имеет заряд `-1`, но его dissipator gauge-ковариантен.
- Старый 42-frame действует в `End(H21)` и не содержит новый jump.
- Требуется environment-transition заряда `+1`.
- Первичный coarse-аудит считал кратность `3` одним `SO(3)`-triplet и
  получал нулевой fixed layer. Это чтение superseded admission-гейтом:
  условное полное разложение равно `1 direct_sum 3` и содержит одну
  family-singlet линию.
- Резонанс `7 gamma`, состояние среды и скорость не выведены.
- Static center `4/4`, transition shape `6/6`, microscopic origin `0/6`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-architecture-gate]]
- [[charged-binary-environment-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_cubic_incidence_up_down_binary_selector_minimal_typed_discriminator_binary_carrier_parent_origin_gate_results.json`