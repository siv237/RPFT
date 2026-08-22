# Том VI: пространственное связывание составной монеты

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, связывает ли составной дублет `H_eff` локальный пакет после
добавления встречного пространственного сдвига.

## Search for solution

Построена минимальная монета с генератором
`sigma_y(direction) tensor K(H_eff)`. Проведены аналитическая линеаризация
около вакуума и проспективный скан восьми значений `kappa`.

## Expected result

Успех требовал спектральной щели или устойчивого профиля с ограниченным
вторым моментом и ненулевой долей нормы в ядре.

## Compliance check

- правило локально, унитарно и калибровочно ковариантно;
- нелинейная поправка имеет третий порядок по амплитуде;
- линейный вакуумный оператор — безмассовый свободный сдвиг без щели;
- при `kappa=0..32` второй момент после 80 шагов превышает `3000`;
- IPR уменьшается, вероятность в `|x|<=8` меньше `0.1`;
- большая связь замедляет разлёт, но не создаёт связанный профиль;
- малая экспоненциально локализованная мода исключена;
- конечноподдержанный нелинейный compacton ещё не исключён.

## Следующий гейт

[[version6-spectral-transition-discrete-compacton-existence-gate]] решит
точные уравнения отсутствия утечки для одно- и двухузловых профилей.

## Links

- [[version6-spectral-transition-discrete-chiral-coin-closure-gate]]
- [[version6-spectral-transition-discrete-equivariant-coin-selector-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_composite_higgs_spatial_binding_gate_results.json`