# Минимальные данные центрального гамильтониана дополнительных масс

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Каков минимальный гамильтонов набор данных, параметризующий весь
трёхкомпонентный trace-симплекс, и какие физические масштабы он не определяет?

## Search for solution

- Факторизован общий центральный гамильтониан на блоках `4+6+6`.
- Выполнен quotient по общему сдвигу энергии.
- Построены прямая и обратная softmax-карты двух щелей.
- Вычислены якобиан и гессиан Gibbs-функционала.
- Проверены счётная, equal-mass и несимметричная точки.
- Отделены безразмерные разрывы, энергия, общий масштаб масс и bath-время.

## Expected result

Две координаты должны быть необходимы и достаточны для внутренности
симплекса. Полное физическое закрытие дополнительно требует их parent-origin
и независимых абсолютных масштабов.

## Compliance check

- После общего сдвига остаются `Delta_u,Delta_d`.
- `(theta_u,theta_d)=(beta Delta_u,beta Delta_d)` диффеоморфно
  параметризуют `int Delta²`.
- Якобиан равен `p_Y p_u p_d>0`; в центре — `1/27`.
- Gibbs-гессиан положителен, его определитель `1/(p_Yp_up_d)`.
- Архитектура закрыта `7/7`; origin щелей `0/2`.
- Энергетический, массовый и релаксационный масштабы имеют по `0/1`.

## Boundary

Минимальная параметризация построена, но значения двух щелей и три
абсолютных масштаба не выведены.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-central-trace-simplex-selector-gate]]
- [[extra-edge-mass-minimal-central-hamiltonian-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate_results.json`