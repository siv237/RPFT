# Происхождение времени корреляции неравновесной ванны

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Определяет ли обратная UV-частота физическое время памяти ванны или для
этого необходимо независимо вывести форму её спектральной плотности?

## Результат

Экспоненциальный и гауссов профили с одной UV-шкалой дают разные ответы:

$$
\tau_E\omega_{\rm UV}=1,\qquad
\tau_G\omega_{\rm UV}=\sqrt\pi/2.
$$

Их коротковременные наклоны также различны: `-1` и `0`. Смесь с параметром
`a` непрерывно интерполирует как время корреляции, так и наклон. Поэтому
`1/omega_UV` является доступной единицей времени, но не единственным
физическим временем памяти.

При заранее выбранном экспоненциальном профиле положительный родитель
фиксирует `tau_corr omega_UV=1`. Размерная карта имеет ранг/ядро `2/2`;
якорь скорости оставляет длино-временную орбиту `3/1`.

## Статус

- условная архитектура: `8/8`;
- точный свидетель неединственности: `3/3`;
- происхождение спектральной формы и абсолютного времени: `0/2`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-nonequilibrium-bath-microscopic-carrier-cutoff-parent-admission-gate]]
- [[version8-correlation-kernel-short-time-rate-selector-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-k43-nonequilibrium-two-reservoir-output-current-parent-admission-gate]]