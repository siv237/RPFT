# Селектор чистого состояния multiplicity-среды

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Трёхмерная минимальная среда имеет скалярное gauge-действие, поэтому все её
состояния gauge-инвариантны. Real-чистые состояния образуют `RP2`. Общий
нормированный след и любой изотропный Gibbs-parent дают смешанное состояние
`I3/3`; минимум энтропии и ранний exterior-square purity-функционал выделяют
всю чистую орбиту, но не её направление.

Два допустимых вещественных гамильтониана `diag(0,1,2)` и `diag(2,0,1)`
выбирают разные чистые состояния при тех же объявленных симметриях. Поэтому
реестр внутренних уникальных селекторов равен `0/5`: одиночная карта `c0`
требует нового анизотропного спектрального и ориентационного данного.

## Связи

- [[version8-baryon-c0-full-multiplicity-frame-single-map-compatibility-gate]]
- [[version8-baryon-c0-connector-multiplicity-and-rate-parent-selector-gate]]
- [[version6-partial-isometry-rank-stratum-selection-gate]]
- [[version6-rp2-geometric-phase-derivation-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_multiplicity_environment_pure_state_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_multiplicity_environment_pure_state_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_multiplicity_environment_pure_state_selector_gate_results.json`