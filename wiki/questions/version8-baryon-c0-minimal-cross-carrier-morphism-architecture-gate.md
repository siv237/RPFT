# Минимальная архитектура cross-carrier морфизма для c0

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Инвариантная исходная прямая и прямая auxiliary mass coefficient являются
тривиальными вещественными представлениями. Поэтому пространство
эквивариантных карт одномерно: `M_kappa(r)=kappa*r`.

Архитектура существует и даёт `c0=kappa*r_star`, но положительность
ограничивает лишь `kappa>0`. При `r_star=4` карты `kappa=1` и `kappa=1/4`
дают соответственно `c0=4` и `c0=1` при одинаковых симметриях.

## Граница

Изометричность нормированных прямых выбрала бы `kappa=1`, однако общий
родитель пока не выводит равенство pullback-метрик. Следующий тест должен
вычислить эту нормировку из общего следового вложения.

## Связи

- [[version8-baryon-c0-typed-internal-map-candidate-audit-gate]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[version8-baryon-spacetime-supercurvature-cubic-projection-admission-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate.py`
- `s2t/results/s2t_v8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate_results.json`