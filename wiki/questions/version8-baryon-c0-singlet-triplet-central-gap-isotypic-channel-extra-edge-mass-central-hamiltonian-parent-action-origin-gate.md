# Parent-origin центрального гамильтониана дополнительных масс

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Порождает ли существующее действие ненулевые значения двух центральных щелей?

## Search for solution

- Построен ортогональный базис `A=P_u-P_d`, `B=P_u+P_d-3P_Y`.
- Вычислены моменты второго и третьего порядка.
- Проверена gauge-Casimir карта в плоскость щелей.
- Проверены grading, coherence-радиус и минимальный двухкомпонентный источник.

## Expected result

Для полного прохода старый parent должен был породить ненулевые линейные
источники вдоль обоих центральных направлений.

## Compliance check

- `Tr A²=12`, `Tr B²=48`, `Tr AB=0`.
- Квадратичный след даёт stiffness `diag(24,96)`, но минимум в нуле.
- Gauge-Casimir map имеет ранг `2`; равные щели требуют `c1=0`.
- Grading и coherence-инвариант не дают щелей.
- Conditional shape `5/5`; parent-origin `0/7`.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-minimal-central-hamiltonian-data-gate]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate_results.json`