# Version VI: полярный/BV-барьер и дробное окно

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Полярное разложение и стандартный FP/BV-фактор не устраняют плоскую
долину: SVD-якобиан `|s1^2-s2^2|` сохраняет радиальную меру `t^3 dt`, а
после поперечного множителя `t^-4` остаётся `dt/t`.

## Main Result

Полная непертурбативная расходимость у чистой вершины растёт лишь как
`log(1/epsilon)`. Поэтому слабый барьер может сработать: для сохранения
самозапуска и подавления границы требуется точное окно
`0 < nu < 17/168`.

Вещественная индуцированная мера очищения размерности `3 x K` дала бы
`nu_K=(K-4)/2`, но такого очищающего носителя текущий родитель не выводит.
В частности, проектное число пять является виртуальной разностью `20-15`,
а не каноническим положительным носителем очищения. Кроме того, минимальный
положительный Wishart-коэффициент `nu=1/2` уже лежит выше рабочего окна.

## Next Test

Тест выполнен в [[version6-fractional-determinant-measure-origin-gate]].
Проект действительно содержит веса `1/10`, `1/20` и `1/14` внутри окна,
но их физический выбор требует полного product-KO2 фермионного оператора и
единой нормировки следа.

## Links

- [[version6-state-weighted-bridge-nonperturbative-saturation-gate]]
- [[version6-fractional-determinant-measure-origin-gate]]
- [[polar-wishart-bv-measure-literature-2026]]
- [[version6-bridge-fluctuation-determinant-purity-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex`
- `s2t/audits/s2t_v6_polar_bv_rank_loss_barrier_gate.py`
- `s2t/results/s2t_v6_polar_bv_rank_loss_barrier_gate_results.json`