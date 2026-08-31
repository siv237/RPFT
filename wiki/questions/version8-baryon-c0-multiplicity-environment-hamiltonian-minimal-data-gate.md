# Минимальные гамильтоновы данные multiplicity-среды

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Все Real- и gauge-допустимые энергии multiplicity-среды образуют
`Sym3(R)`. Для выбора одной линии достаточно минимального одноосного
представителя `h=epsilon I3+Delta(I3-P)`, где `P in RP2`, `Delta>0`.
После факторизации положительного масштаба и сдвига энергии единственным
неустранимым данным селектора остаётся сама точка `P`.

При конечном `beta Delta` Gibbs-состояние имеет ранг `3` и purity строго
меньше единицы. Точный проектор получается только в пределе
`beta Delta -> infinity` или через внешний протокол чистой подготовки.
Поэтому различаются три слоя новых данных: направление `P`, охлаждение и
абсолютная щель `Delta_phys`; текущий parent выводит `0/3`.

## Связи

- [[version8-baryon-c0-multiplicity-environment-pure-state-selector-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version8-typed-clock-energy-to-noise-rate-anchor-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate.py`
- `s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate_results.json`