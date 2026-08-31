# Минимальное нейтральное endpoint-расширение для карты c0

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Поскольку старый `H21` не содержит neutral singlet, для двух углов
linking-блока необходимо добавить две нейтральные комплексные линии:
`H23=H21 direct_sum C s0 direct_sum C a0`.

Противоположная градуировка делает два off-diagonal Hermitian направления
нечётными. Их коммутатор порождает диагональное третье направление, поэтому
минимальный gauge-closed frame растёт `42 -> 45`, а его метрика равна
`K45=K42 direct_sum 2I3`.

## Граница

Архитектура сохраняет условные `kappa=1`, `c0=4`, но физическое
происхождение двух новых endpoint states ещё не выведено.

## Связи

- [[version8-baryon-c0-existing-42-carrier-linking-bridge-classification-gate]]
- [[version8-baryon-c0-linking-algebra-offdiagonal-bridge-admission-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_minimal_neutral_endpoint_extension_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate.py`
- `s2t/results/s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate_results.json`