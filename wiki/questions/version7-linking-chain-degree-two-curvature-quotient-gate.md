# Version VII: quotient кривизны длины два связывающего комплекса

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, удаляются ли диагональные Gram-возвраты полного квадрата
каноническим фактором форм, сохраняющим крайний блок `B1B0=R_U`.

## Search for Solution

Обычный представленный Connes-calculus для узловой алгебры `C³` стабильно
даёт ранги `4,6,2,4` для одноформ, двухформ, junk и quotient. Оба
endpoint-блока принадлежат junk, поэтому стандартный quotient удаляет
нужную относительную кривизну.

Канонический оператор степени цепи
`N=diag(0 I11,1 I21,2 I10)` задаёт
`delta_N(F)=1/2[N,F]`. Эта производная уничтожает диагональные возвраты и
сохраняет ровно блоки `0 <-> 2`, то есть `R_U` и `R_U*`.

## Expected Result

- Обычный junk-маршрут закрыт.
- Relative mapping-cone производная проходит без ручного проектора.
- Она gauge-ковариантна и не зависит на уровне нормы от ориентации цепи.
- Получены гессианы `(7,0,20)` и `(0,0,27)`.
- Непрерывный секторный вес не вводится.

Открытым остаётся объединение рёберного Hodge-момента и относительной
производной в одной общей Hodge-метрике и одном следе.

## Links

- [[version7-real-linking-superconnection-assembly-gate]]
- [[version7-common-chain-number-hodge-relative-trace-gate]]
- [[version7-polar-transfer-cross-curvature-origin-gate]]
- [[version4-pati-salam-junk-mapping-cone-gate]]
- [[field-space-superconnection-bv-mapping-cone-literature-2026]]

## Source Notes

- `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex`
- `s2t/audits/s2t_v7_linking_chain_degree_two_curvature_quotient_gate.py`
- `s2t/results/s2t_v7_linking_chain_degree_two_curvature_quotient_gate_results.json`