# Version VI: внутреннее время и родительская динамика quench

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Проект уже содержит нетривиальное модулярное состояние
`rho_beta=exp(-beta h_F)/Z`, согласующееся с гипотезой теплового времени
Connes--Rovelli. Оно ориентирует межвершинные стрелки, но `h_F` скалярно
на каждом семейном триплете, поэтому весь проекторный сектор `RP2`
остаётся неподвижным.

## Main Result

- внутреннее модулярное время в проекте действительно существует;
- оно не совпадает с нормированным следом действия;
- собственный поток `rho_beta` сохраняет само состояние и его энтропию;
- проекторный quench и необратимость из этого потока не следуют;
- внешний параметр `t` предыдущего гейта понижен до вычислительной
  координаты.

## Next Test

Четырёхтактная резонансная петля имеет clock-like структуру, но ещё не
является часами Page--Wootters. Нужно проверить наличие разложения
`clock + system`, глобального ограничения и условной эволюции
`(lambda,P)` без новых состояний.

Позднейший обратный аудит добавил более раннее логическое условие: до
построения часов необходимо вывести само одноосное вакуумное многообразие.
Точный контрольный переход найден в
[[version6-real-qutrit-purification-transition-gate]], но его коэффициент
пока не следует из родителя.

## Links

- [[relational-modular-internal-time-literature-2026]]
- [[version6-closed-bridge-destabilization-gate]]
- [[version6-rp2-geometric-phase-derivation-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version5-modular-commutant-parent-correspondence-gate]]
- [[version5-order-four-resonant-loop-transport-gate]]
- [[version5-self-consistent-internal-time-horizon-gate]]

## Source Notes

- `s2t/gates/version6_projective_quench_parent_dynamics_gate.tex`
- `s2t/audits/s2t_v6_projective_quench_parent_dynamics_gate.py`
- `s2t/results/s2t_v6_projective_quench_parent_dynamics_gate_results.json`