# Version VI: произведение KO2 и нормировка семейного пфаффиана

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Внешняя KO4-геометрия и внутренний KO6-модуль дают суммарную степень
`4+6=2 mod 8`, поэтому физический киральный пфаффиан допустим. Явный
антисимметричный блок на `M300` построен, но обычный березинский интеграл
даёт

`-log|Pf A_R| = -15 log det R + const`,

а не слабый коэффициент `1/20`.

## Main Result

Множитель `1/300` перед квадратичной фермионной формой изменяет только
не зависящую от `R` нормировку пфаффиана. Он не делит число семейных копий.
Коэффициент `1/20` возникает только после отдельного определения
интенсивной величины `(1/300) log|Pf A_R|`, то есть через нормированный
детерминант Фугледе--Кадисона.

Любой обычный конечный гауссов интеграл имеет показатель в решётке
`(1/2) Z`. Её минимальный положительный элемент `1/2` уже больше границы
`17/168`. Поэтому стандартная конечная determinant/Pfaffian мера не может
дать нужный слабый барьер.

## Status Boundary

Кинематика product-KO2 пройдена. Стандартный фермионный вывод дробного
барьера закрыт. Открыт только новый, более сильный вопрос: существует ли
у всего родителя единый принцип интенсивной свободной энергии, одинаково
нормирующий классическое действие, энтропию, мостовые флуктуации и
фермионный пфаффиан.

## Next Test

Тест выполнен в
[[version6-common-intensive-free-energy-normalization-gate]]. Общая
нормировка не спасает отрицательную моду; выборочная нормировка
фермионного члена запрещена. Стандартная детерминантная ветвь закрыта.

## Links

- [[version6-fractional-determinant-measure-origin-gate]]
- [[version6-common-intensive-free-energy-normalization-gate]]
- [[product-ko2-pfaffian-normalization-literature-2026]]
- [[normalized-pfaffian-fuglede-kadison-literature-2026]]
- [[version6-bridge-fluctuation-determinant-purity-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_product_ko2_family_pfaffian_operator_gate.tex`
- `s2t/audits/s2t_v6_product_ko2_family_pfaffian_operator_gate.py`
- `s2t/results/s2t_v6_product_ko2_family_pfaffian_operator_gate_results.json`