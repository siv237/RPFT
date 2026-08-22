# Version VI: родитель внешнего квадрата обменного моста

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Обычная двухузловая Real-суперсвязность даёт только
`2 Tr((B^T B)^2)` и не содержит `e2(B^T B)`. Поэтому внешний квадрат не
скрыт в уже принятом каноническом действии.

Функториальная трёхузловая цепь
`R -> R3 tensor R3 -> Lambda2(R3) tensor Lambda2(R3)` строится без нового
поля и имеет двухшаговый путь `Lambda2(B)`. Её каноническая относительная
норма равна `2 e2(B^T B)`.

## Main Result

После возвращения полной самосогласованной радиальной энергии переход
требует коэффициента

`m_crit = 3.0261454269...`

перед `e2(R)`. Одна нормированная exterior-цепь даёт только `m=2` и не
разрушает изотропную фазу.

Сырой direct-minus-crossed тензор даёт `m=4` и проходит полный тест:
возникает одноосный спектр приблизительно
`(0.966890,0.016555,0.016555)`. Но дополнительный множитель два пока не
выведен из родителя.

## Status Boundary

- KO6-удвоение сокращается физическим half-trace;
- вторая одинаковая relative-копия нарушает неприводимость;
- выбор ненормированной тензорной метрики вручную запрещён;
- текущий минимальный родитель недостаточен;
- raw tensor-square carrier остаётся условно рабочим механизмом.

## Next Test

Проверить тензорный квадрат Real-пары и установить, существуют ли два
независимых endpoint-пути, фиксирующие коэффициент четыре без нового веса.

Тест выполнен в
[[version6-tensor-square-relative-carrier-normalization-gate]]. Тензорный
квадрат не даёт дополнительной кратности, а raw antisymmetrizer является
ненормированным проектором. Однако канонический вес `2e2(R)` сам становится
достаточным при охлаждении: найден переход при
`beta_c=1.5426695409...`.

## Links

- [[version6-partial-isometry-rank-stratum-selection-gate]]
- [[exterior-power-superconnection-parent-literature-2026]]
- [[version6-exchange-bridge-minimal-parent-gate]]
- [[version5-graded-correspondence-superconnection-gate]]
- [[pati-salam-relative-parent-action-gate]]
- [[version6-matter-birth-program]]
- [[version6-tensor-square-relative-carrier-normalization-gate]]

## Source Notes

- `s2t/gates/version6_exchange_bridge_exterior_square_parent_gate.tex`
- `s2t/audits/s2t_v6_exchange_bridge_exterior_square_parent_gate.py`
- `s2t/results/s2t_v6_exchange_bridge_exterior_square_parent_gate_results.json`