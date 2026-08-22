# Version VI: минимальный родитель обменного моста

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Расширение координатной алгебры конечными матрицами порождает весь
компактный сектор одноформ, а не один мост. Минимальный кинематический
вариант — Real-линейный нечётный эндоморфизм градуированного
соответствия с одной вещественной амплитудой `lambda`.

## Main Result

Каноническое положительное действие равно

`S_can(lambda) = (2/7)(1-lambda^2)^2`.

Оно имеет отрицательный гессиан `-8/7` в дефектной точке `lambda=0` и
положительный гессиан `16/7` в замкнутой точке `lambda=1`. Поэтому
минимальный родитель кинематически допустим, но естественная динамика
стремится уничтожить дефект, а не родить материю.

## Verdict

- компактное координатное расширение: не минимально;
- нечётный Real-эндоморфизм: кинематический проход;
- спонтанное рождение дефектной пары: не получено;
- следующий вопрос: существует ли уже доказанный проектный член,
  дестабилизирующий закрытый мост без ручной смены знака.

Следующий гейт [[version6-closed-bridge-destabilization-gate]] показал, что
статическая дестабилизация не обязательна: быстрый проекторный quench может
оставлять топологически запертые пары, хотя спокойный вакуум устойчив.

## Links

- [[version6-exchange-bridge-parent-admissibility-gate]]
- [[version6-common-configuration-space-gate]]
- [[superconnection-odd-endomorphism-parent-literature-2026]]
- [[version5-graded-correspondence-superconnection-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version5-fermionic-determinant-induced-skyrme-gate]]

## Source Notes

- `s2t/gates/version6_exchange_bridge_minimal_parent_gate.tex`
- `s2t/audits/s2t_v6_exchange_bridge_minimal_parent_gate.py`
- `s2t/results/s2t_v6_exchange_bridge_minimal_parent_gate_results.json`