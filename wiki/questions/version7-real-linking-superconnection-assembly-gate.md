# Version VII: единая Real-связывающая суперсвязность

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, является ли относительная полярная кривизна блоком квадрата
заранее типизированного нечётного оператора и проходит ли нулевой гессиан
полной самосопряжённой кривизны.

## Search for Solution

Построен трёхступенный комплекс размерностей `11 -> 21 -> 10`:

```text
B0 = column(A*U,A),
B1 = row(A,-UA*).
```

Он даёт точную факторизацию

```text
B1 B0 = AA*U-UA*A = R_U.
```

Дифференциал нечётен, его квадрат чётен, а `R_U` является крайним блоком
`Hom(H0,H2)` оператора `d²`. Однако полный самосопряжённый квадрат
`Q²=(d+d*)²` дополнительно содержит три диагональных Gram-блока.

## Expected Result

Результат смешанный:

- факторизация `R_U=(d²)20` получена точно;
- блок длины два сохраняет `(7,0,20)` и вакуум `(0,0,27)`;
- полная кривизна даёт в нуле `(27,0,0)`;
- допустимый вес полной кривизны требует `alpha<1/15`;
- стандартные множители `1,1/2,1/4,1/8` не проходят;
- проекция на степень два ещё не выведена представленным исчислением.

Следующий тест должен определить, удаляются ли диагональные блоки
каноническим junk/когомологическим quotient, а не ручной проекцией.

## Links

- [[version7-polar-transfer-cross-curvature-origin-gate]]
- [[version7-linking-chain-degree-two-curvature-quotient-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version5-morita-linking-parent-gate]]
- [[polar-transfer-linking-expectation-literature-2026]]

## Source Notes

- `s2t/gates/version7_real_linking_superconnection_assembly_gate.tex`
- `s2t/audits/s2t_v7_real_linking_superconnection_assembly_gate.py`
- `s2t/results/s2t_v7_real_linking_superconnection_assembly_gate_results.json`