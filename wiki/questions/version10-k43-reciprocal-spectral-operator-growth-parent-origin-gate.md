# Том X: геометрический родитель взаимно обратного спектрального хода

> Status: working
> Type: question
> Updated: 2026-09-01

## Summary

Взаимно обратный спектр на гиперзарядово-вакуумной подячейке теперь получен
как единственная нулевая траектория положительного геометрического
родителя. Безследовый генератор `Q_X=P_0-P_Y` фиксируется типами,
нормировкой и стрелкой притока. Результат остаётся безразмерным: мера
рождения ячеек и физическая секунда не выведены.

## Key Points

- `Tr Q_X=0`, `Q_X^2=P_0+P_Y`, `rank Q_X=2`.
- Спектр `Q_X` равен `{-1^1,0^41,1^1}`.
- Условие сохранения определителя оставляет одномерный диагональный
  генератор; стрелка роста выбирает знак по счёту `2>-2`.
- Родитель пути есть сумма квадрата начального условия и нормы
  `K'-{Q_X,K}/2`.
- Единственная нулевая траектория: `K_X(zeta)=exp(zeta Q_X)`.
- Локальный струйный гессиан имеет ранг `4` и определитель `1`.
- Архитектура `9/9`, структурное происхождение спектрального закона `4/4`.
- Мера переходов рождения ячеек и физическая временно-энергетическая
  калибровка остаются `0/2`.

## Open Boundary

Следующий гейт должен построить нормированную меру переходов `N -> N+1` и
проверить, выводится ли темп роста, ранее условно записанный как
`h_vac=exp(-S_vac)/sqrt(8 pi)`.

## Links

- [[version10-inflow-spectral-self-energy-k43-typed-embedding-gate]]
- [[version10-inflow-spectral-self-energy-running-parent-origin-gate]]
- [[version10-quantum-rg-common-carrier-admission-gate]]
- [[version9-physical-reopening-reference-scale-mu-parent-origin-gate]]

## Source Notes

- `s2t/gates/version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_k43_reciprocal_spectral_operator_growth_parent_origin_gate.py`
- `s2t/results/s2t_v10_k43_reciprocal_spectral_operator_growth_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_k43_reciprocal_spectral_operator_growth_parent_origin.py`