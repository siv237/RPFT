# Version VI: флуктуационный запуск проекторной фазы

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Если уже построенное семейное состояние `R` использовать как вес
нормированного следа кривизны обменного моста, его шестимерный физический
гессиан зависит от спектра `R`. Однопетлевой детерминант индуцирует
отрицательный коэффициент чистоты `-45/16`, превышающий порог
`log(4)+6/7`.

## Main Result

- три антисимметричные моды являются касательными к орбите `O(3)`;
- шесть физических масс вычислены точно;
- изотропное состояние получает отрицательный суммарный квадратичный
  коэффициент `-51/112` даже с классической ценой моста;
- локальная неустойчивость может запускаться без внешнего временного
  толчка;
- однопетлевой потенциал уходит к минус бесконечности при потере ранга, где
  одна из интегрируемых мод становится безмассовой, поэтому устойчивое
  насыщение ещё не доказано;
- полная полевая/BV-мера проекта остаётся открытым условием.

## Next Test

Построить непертурбативный конечномерный интеграл состояния-взвешенного
матричного моста, включая якобиан и орбитальный фактор, и проверить наличие
конечного одноосного минимума до пространственного quench.

Тест выполнен в
[[version6-state-weighted-bridge-nonperturbative-saturation-gate]]:
плоская мера имеет логарифмически расходящуюся четырёхмерную долину на
чистой страте и не даёт конечного насыщения.

## Links

- [[version6-exchange-bridge-induced-alignment-gate]]
- [[version6-state-weighted-bridge-nonperturbative-saturation-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[background-field-one-loop-determinant-literature-2026]]
- [[version5-carrier-measure-freeze-gate]]

## Source Notes

- `s2t/gates/version6_bridge_fluctuation_determinant_purity_gate.tex`
- `s2t/audits/s2t_v6_bridge_fluctuation_determinant_purity_gate.py`
- `s2t/results/s2t_v6_bridge_fluctuation_determinant_purity_gate_results.json`