# Том VI: родитель паринга Вайнберга

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Текущий родитель фиксирует gauge-тип оператора Вайнберга, слабый
квадратичный носитель `B_nu(H)`, одну семейную ось после голономного
сжатия `P0` и следовой вес канала `1/7`.

Но он не фиксирует коэффициент оператора, полный семейный тензор,
подавляющий масштаб и пространственную локализацию. Поэтому оператор
структурно допустим, но нейтринная масса не выведена.

## Семейная граница

Симметричные `C3`-инвариантные матрицы образуют двумерное пространство:

`C = x P0 + y (I-P0)`.

После сжатия `P0 C P0=x P0` направление одномерно, но амплитуда `x`
остаётся свободной. Остаток сжатия равен `1.67e-16`.

## No-go спектральной меры

Для семейства

`g_alpha(z)=z exp(-z^2)+alpha exp(-z^2)`

нечётная кинетическая часть одинакова, тогда как коэффициент чётного
парингового члена принимает значения `0,1,2` при `alpha=0,1,2` и может
меняться непрерывно. Обычная кинетическая нормировка не выбирает
коэффициент Вайнберга.

## Почему `1/7` не является массой

Общий следовой вес одинаково умножает кинетический и массовый члены и
сокращается после нормировки поля. Контрольные веса `1/7,2/7,1` дали
одну физическую массу с нулевым разбросом.

Остаточная формула имеет невыведенные множители:

`m_nu ~ r_tau kappa_e v_H^2/Lambda`.

## Следующий гейт

`version6_spectral_transition_rank_change_localization_gate` должен
проверить не абсолютную массу, а возможность пространственно
локализовать область смены ранга `W_nu: 0 -> 1` существующей динамикой
Хиггса и дефекта.

Последующий аудит дал отрицательный ответ: радиальный минимум сохраняет
`|H|^2>=1/2`, поэтому текущий вихрь не создаёт область ранга ноль. См.
[[version6-spectral-transition-rank-change-localization-gate]].

## Links

- [[version6-spectral-transition-neutrino-line-parent-gate]]
- [[version5-h15-majorana-pairing-correspondence-gate]]
- [[version5-h15-fermionic-spectral-weinberg-measure-gate]]
- [[version5-ordinary-spectral-moment-map-no-go-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[transition-primitive]]
- [[version6-spectral-transition-rank-change-localization-gate]]

## Source Notes

- `s2t/gates/version6_spectral_transition_weinberg_pairing_parent_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_weinberg_pairing_parent_gate.py`
- `s2t/results/s2t_v6_spectral_transition_weinberg_pairing_parent_gate_results.json`
- S. Weinberg, *Baryon- and Lepton-Nonconserving Processes* (1979).
- M. Sakellariadou, A. Sitarz, *Fermionic Spectral Action and the Origin
  of Nonzero Neutrino Masses* (2019).
