# Селектор коэффициента центральной щели

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Для одного направления `Q=P3-3I4/4` шесть естественных нормировок дают
разные модули коэффициента:
`1`, `2`, `2/sqrt(3)`, `4/3`, `2/3`, `4/sqrt(3)`. Норма
нецентрированного гамильтониана дополнительно зависит от произвольного нуля
энергии.

Чётный потенциал `a lambda^2/2+b lambda^4/4` выбирает модуль только через
свободное отношение `-a/b` и сохраняет пару `+-lambda`. Максимум энтропии
даёт нулевую щель, а KMS выбирает лишь `beta lambda` после задания target.
Итоговый selector ledger равен `0/8`.

## Связи

- [[version8-baryon-c0-singlet-triplet-central-gap-parent-action-origin-gate]]
- [[version8-baryon-c0-singlet-triplet-central-weight-minimal-hamiltonian-data-gate]]
- [[singlet-triplet-gibbs-gap-literature-2026]]

## Исходники

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate_results.json`