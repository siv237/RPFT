# Пространственно-временная кинетическая факторизация

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Калибровочный гессиан факторизуется на внутреннюю метрику и поперечный
пространственно-временной проектор. До фиксации его ранг равен `36`, а
нулевое пространство имеет размерность `12`. После ковариантной фиксации
ранг равен `48` и
`H_xi^-1=K_к^-1 tensor p^-2(P_T+xi P_L)`.

Поперечная часть обратного оператора не зависит от `xi`; продольная часть
зависит и является следствием фиксации. Тем самым `K_к^-1` выделен как
внутренний множитель, но абсолютная физическая мобильность не получена.

## Следующий вопрос

Проверить, выводят ли корреляции среды общий множитель и поперечную
мобильность либо сохраняют независимый спектральный масштаб.

## Связи

- [[version8-field-noise-metric-to-parent-hessian-comparison-gate]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[version8-metric-dual-environment-parent-action-origin-gate]]
- [[quantum-gradient-flow-and-noise-metric-literature-2026]]

## Исходники

- `s2t/gates/version8_spacetime_kinetic_factorization_and_gauge_fixing_gate.tex`
- `s2t/audits/s2t_v8_spacetime_kinetic_factorization_and_gauge_fixing_gate.py`
- `s2t/results/s2t_v8_spacetime_kinetic_factorization_and_gauge_fixing_gate_results.json`