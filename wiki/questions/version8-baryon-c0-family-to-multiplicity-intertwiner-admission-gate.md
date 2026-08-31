# Допуск family-to-multiplicity интертвейнера

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Семейный qutrit является стандартной тройкой `SO(3)_fam`, тогда как
текущая multiplicity-среда состоит из трёх тривиальных линий. Точная
система `T J_a=0` имеет ранг `9` на девяти неизвестных, поэтому текущий
`SO(3)`-Hom равен нулю. Запрет сохраняется после ограничения на `A4`.

Условный проход требует объявить на среде вторую стандартную тройку.
Тогда лемма Шура даёт `T=kappa I3`, а изометрия — `kappa=+-1`. Но такое
действие смешивает текущие endpoint-линии; одновременно требуется
ковариантный подъём endpoint-алгебры. Эти две новые структуры не выведены,
поэтому extension ledger равен `0/2`.

## Связи

- [[version8-baryon-c0-multiplicity-environment-hamiltonian-parent-origin-gate]]
- [[version6-bosonic-defect-family-connection-parent-identification-gate]]
- [[version4-variational-family-state-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate.py`
- `s2t/results/s2t_v8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate_results.json`