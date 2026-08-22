# Version VI: сравнение индексов Каллиаса и Тёплица

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Сравнение усилено от равенства чисел до тождества граничных символов.
Положительная spin-cover линия массы `n dot sigma` имеет на экваторе
clutching-функцию `z`. После умножения на канонический проектор `q0`
ранга 15 получается

`g15(z)=z q0 + 1 - q0`,

то есть в точности первая компонента Real-унитария `V15` Тома V.
Сопряжённая ветвь даёт `z^-1 conjugate(q0)+1-conjugate(q0)` и совпадает
со второй компонентой.

## Result

- determinant winding равен `+15/-15`;
- Callias boundary и Toeplitz boundary представляют один граничный
  `K`-класс, а не просто имеют одинаковый индекс;
- окружность Тёплица является clutching-экватором сферы дефекта, а не
  дополнительным физическим измерением;
- для принятого spin-cover оператора ненулевой индекс условно гарантирует
  15 локализованных нулевых мод одной ориентации;
- конечный родитель всё ещё не выводит необходимый комплексный носитель
  ранга два, поэтому физические фермионы не объявляются полученными.

## Subsequent Result

[[version6-spin-cover-carrier-parent-derivation-gate]] показал, что
`L direct_sum L*` действительно даёт топологическую двойку, но
существующая KO6 particle/conjugate пара не допускает полного
complex-linear Pauli-действия без нарушения градуировки и gauge-зарядов.
Честный равнозарядный дублет работает, но пока является новым модулем.

## Links

- [[version6-composite-connection-callias-fredholm-gate]]
- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[callias-toeplitz-clutching-literature-2026]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[version5-spin-cover-defect-sphere-bridge-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_callias_toeplitz_index_comparison_gate.tex`
- `s2t/audits/s2t_v6_callias_toeplitz_index_comparison_gate.py`
- `s2t/results/s2t_v6_callias_toeplitz_index_comparison_gate_results.json`