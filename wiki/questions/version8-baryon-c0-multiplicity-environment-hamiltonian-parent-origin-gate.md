# Происхождение multiplicity-Hamiltonian из parent

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Собственные источники текущей multiplicity-среды не дают одноосный
Hamiltonian: старый Hessian равен `0_3`, уникальный trace полного `M5`
даёт `(2/5)I3`, а полный Kossakowski-пакет — `I3`. Локальный trace-симплекс
допускает анизотропию, но разные положительные следы выбирают разные оси.

Ранний семейный `R4+` является точным near miss: его дискриминант
`164241/16` ненулевой, но сумма квадратов endpoint-коммутаторов равна `50`.
Он действует на другом qutrit-носителе; формальный перенос требует элемента
девятимерного `M3(R)` и абсолютного энергетического множителя. Канонической
карты нет, поэтому parent-origin ledger равен `0/5`.

## Связи

- [[version8-baryon-c0-multiplicity-environment-hamiltonian-minimal-data-gate]]
- [[version8-baryon-c0-extended-endpoint-bimodule-weight-origin-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version4-variational-family-state-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate_results.json`