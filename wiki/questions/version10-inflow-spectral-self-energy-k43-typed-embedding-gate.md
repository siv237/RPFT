# Том X: типизированное вложение спектральной самоэнергии в K43

> Status: working
> Type: question
> Updated: 2026-09-01

## Summary

Абстрактный двухмодовый резервуар прошлого гейта канонически вложен в
существующую 43-мерную столкновительную ячейку как пара из вакуума и
гиперзарядовой шумовой моды. Вложение калибровочно-инвариантно, имеет
ненулевое старое звёздное взаимодействие и совместимо по типу с
шестимерным KMS-множителем. Старый родитель ячейки не порождает зависимость
`exp(+-zeta)`.

## Key Points

- `W_Y=span{|Y>,|0>} subset K43` и `E_Y^* E_Y=I2`.
- Гиперзарядовая линия коммутирует со всеми 12 калибровочными генераторами.
- Матрица гиперзаряда на концевом пространстве имеет ранг `21`.
- Ограниченное звёздное взаимодействие имеет ранг `42`.
- `E_Y tensor I6` имеет ранг `12` и сохраняет изометрию.
- Вложенный оператор сжимается в `diag(exp(-zeta),exp(zeta))`.
- Старый родитель `I43-|0><0|` сжимается в `diag(1,0)` и имеет нулевой ход.
- Архитектура `8/8`, реестр происхождения `4/6`; физический спектральный
  закон и его общий родитель остаются `0/2`.

## Open Boundary

Следующий узел должен получить взаимно обратные коэффициенты
`exp(+-zeta)` как стационарное или вариационное следствие геометрического
родителя роста, а не как определение оператора на уже найденном
подпространстве.

## Links

- [[version10-inflow-spectral-self-energy-running-parent-origin-gate]]
- [[version10-quantum-rg-common-carrier-admission-gate]]
- [[version8-full-noise-repeated-interaction-hamiltonian-gate]]
- [[version8-vacuum-chain-parent-state-and-local-hamiltonian-origin-gate]]

## Source Notes

- `s2t/gates/version10_inflow_spectral_self_energy_k43_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_inflow_spectral_self_energy_k43_typed_embedding_gate.py`
- `s2t/results/s2t_v10_inflow_spectral_self_energy_k43_typed_embedding_gate_results.json`
- `s2t/proofdsl/examples/version10_inflow_spectral_self_energy_k43_typed_embedding.py`