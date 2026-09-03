# Морфизм групповой скорости ванны в скорость фронта рождения клеток

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Групповая скорость ванны не равна скорости геометрического фронта на всей
истории. Она задаёт её через зависящий от состояния морфизм
`v_f/v_b=(8/121)(R/ell_cell)`. Равенство возникает лишь на оболочке
`R/ell_cell=121/8`.

## Key Points

- `v_b/c=(121/24)k_X` и `H_B ell_cell/c=k_X/3` дают локальную длину
  распространения `v_b/H_B=(121/8)ell_cell`.
- Кинематика `R=ell_cell N^(1/3)` даёт `v_f=H_B R`.
- Типизированный морфизм не содержит нового коэффициента, но зависит от
  текущего безразмерного радиуса.
- Положительный родитель после якоря роста имеет полный ранг `3` и
  определитель `1`.
- Скорость поверхности уровня нельзя без отдельного доказательства читать
  как микроскопическую скорость передачи сигнала.

## Status

- Архитектура: `10/10`.
- Условное происхождение: `8/8`.
- Морфизм фронта: `1/1`.
- Универсальное равенство скоростей: `0/1`.
- Причинная идентичность: `0/1`.
- Абсолютный масштаб: `0/1`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-group-velocity-vacuum-growth-common-parent-origin-gate]] — предыдущий общий родитель скорости ванны и роста.
- [[current-status-and-next-vectors]] — положение результата на основном фронтире.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin.py`