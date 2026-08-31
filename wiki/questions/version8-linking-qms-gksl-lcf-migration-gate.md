# Точная LCF-проверка linking-GKSL полугруппы

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Linking-QMS перенесена в proof eDSL. Точно проверены GKSL-типизация,
сохранение следа на `441` матричной единице, унитальность, инвариантность и
явная формула на `221`-мерной endpoint-алгебре, а также `dim Fix=41`.

## Problem

Заменить выборочные численные проверки linking-полугруппы полным точным
сертификатом конечномерного генератора.

## Search for solution

- Incidence-матрица восстановлена точно из нулей и единиц.
- Построен типизированный самосопряжённый `D_A`.
- GKSL-конструктор проверил носители, эрмитовость и скорость.
- След и corner-инвариантность проверены на полных матричных базисах.
- Неподвижная размерность вычислена как точная нульмерность коммутантной
  системы.

## Expected result

Все конечномерные алгебраические утверждения исходного QMS-гейта должны
стать независимыми от floating-point допуска.

## Compliance check

- `rank A=10`.
- Trace-базис: `441/441`.
- `L(I)=0` точно.
- Endpoint-базис: `221/221`; явная corner-формула совпадает.
- Система фиксированных точек: `220x221`, ранг `180`, нульмерность `41`.
- Полная положительность пока опирается на доверенное правило GKSL, а не на
  отдельный Choi proof-object.

## Links

- [[version8-linking-dirichlet-quantum-markov-semigroup-gate]]
- [[version8-markov-fixed-algebra-lcf-migration-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_linking_qms_gksl_lcf_migration_gate.py`
- `s2t/results/s2t_v8_linking_qms_gksl_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_linking_qms.py`