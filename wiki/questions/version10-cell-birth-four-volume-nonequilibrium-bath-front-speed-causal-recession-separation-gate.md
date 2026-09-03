# Разделение причинной скорости ванны и рецессионной скорости фронта

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Причинность ограничивает локальную скорость `dot R-H_B R`, а не полную
скорость поверхности уровня. Фронт рождения клеток имеет локальную скорость
ноль и находится внутри конуса с характеристиками `H_B R +- v_b`.

## Key Points

- Разложение `u_total=u_recession+u_local` обратимо и имеет определитель `1`.
- Для фронта `u_local=0`; для характеристик ванны `u_local=+-v_b/c`.
- Равенство чисел `H_B R=v_b` на оболочке `R/ell_cell=121/8` не означает
  совпадения траекторий.
- Локальная сублиминальность требует `k_X<=24/121`.
- Условный проектный `S_vac` удовлетворяет этому ограничению, но его статус
  остаётся условным.
- Микроскопическое ядро распространения ещё не построено.

## Status

- Архитектура: `10/10`.
- Условное происхождение: `8/8`.
- Кинематическое разделение: `1/1`.
- Локальный причинный конус: `1/1`.
- Условная сублиминальность: `1/1`.
- Микроскопическое ядро и абсолютный масштаб: `0/2`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-group-velocity-cell-birth-front-speed-morphism-origin-gate]] — морфизм, после которого потребовалось разделить типы скоростей.
- [[current-status-and-next-vectors]] — положение результата на основном фронтире.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation.py`