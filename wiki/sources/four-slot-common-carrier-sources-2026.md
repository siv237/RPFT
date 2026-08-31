# Источники архитектуры общего four-slot carrier

> Status: working
> Type: source
> Updated: 2026-08-31

## Summary

Узел объединяет три результата Тома VIII: endpoint-разложение `H24`,
шумовую ячейку `K45` и GNVW-различие между односторонним и сбалансированным
транспортом. Новое утверждение состоит в их размещении на одной удвоенной
цепи, а не в происхождении самих условных расширений.

## Key Points

- `H24` содержит old, neutral-linking и family-triplet sectors.
- Одна `K45` реализует collision; вторая нужна как inverse-flow compensator.
- Forward и balanced transport теперь сравнимы внутри одной алгебры.
- Общий носитель не является селектором endpoint или transport.

## Links

- [[version9-four-slot-common-carrier-architecture-gate]]
- [[version9-four-slot-dynamic-parent-program-admission-gate]]
- [[tome9-opening-contract]]

## Source Notes

- `s2t/gates/version8_baryon_c0_minimal_neutral_endpoint_extension_gate.tex`
- `s2t/gates/version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate.tex`
- `s2t/gates/version8_baryon_c0_charged_mediator_dynamic_parent_data_admission_gate.tex`
- `s2t/gates/version9_four_slot_common_carrier_architecture_gate.tex`