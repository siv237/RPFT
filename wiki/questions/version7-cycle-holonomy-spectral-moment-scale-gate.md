# Version VII: шестой момент голономии и no-go масштаба

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Единственная относительная `U(3)`-голономия полного графа действительно
входит в выведенный спектральный инвариант. Первым чувствительным моментом
является `Tr D^6`; второй и четвёртый моменты её не видят.

Однако шестой момент выбирает только центральную матрицу `I3` или `-I3`.
Нецентральное семейное смешивание и масштаб `mu` не выведены.

## Exact Spectral Visibility

Для общего радиуса шести новых рёбер:

$$
\operatorname{Tr}D^2=18(2r^2+1),
$$

$$
\operatorname{Tr}D^4=6(18r^4+10r^2+5).
$$

Эти выражения не зависят от голономии. Первый зависимый момент равен

$$
\operatorname{Tr}D^6
=54+144r^2+306r^4+324r^6
+12r^4\operatorname{ReTr}W_C.
$$

Коэффициент `12` происходит от шести начальных вершин и двух ориентаций
простого цикла.

## Holonomy Minimum

Голономная часть спектрального полинома имеет вид

$$
V_6(W_C)=12c_6r^4\operatorname{ReTr}W_C.
$$

- при `c6 < 0` минимум равен `W_C=I3`;
- при `c6 > 0` минимум равен `W_C=-I3`;
- при `c6 = 0` голономия остаётся плоской;
- при ненулевом `c6` гессиан поднимает все девять линейных мод.

Следовательно, шестой момент закрывает плоскую ориентацию, но делает это
только центрально и не создаёт CKM/PMNS.

## Scale No-Go

Для

$$
S=c_2\operatorname{Tr}D^2+c_4\operatorname{Tr}D^4
+c_6\operatorname{Tr}D^6
$$

радиальная часть равна `a r^2+b r^4+c r^6`, где

$$
a=36c_2+60c_4+144c_6,
\qquad b=108c_4+270c_6,
\qquad c=324c_6.
$$

`H15` определяет целые коэффициенты замкнутых маршрутов, но не определяет
спектральные числа `c2,c4,c6`. Поэтому стационарное уравнение

$$
a+2br^2+3cr^4=0
$$

не предсказывает `r=mu` без дополнительного спектрального профиля или
динамического уровня отображения момента.

## Status Boundary

Закрыто:

- спектральная видимость единственного цикла;
- точный коэффициент голономного следа;
- lifting девяти линейных мод при `c6 != 0`.

Открыто:

- происхождение и знак `c6`;
- абсолютный масштаб `mu`;
- нецентральный минимум;
- семейные массы и наблюдаемое смешивание.

## Next Gate

Проверить, существуют ли независимо выведенные высшие циклические характеры,
которые создают нецентральный минимум без свободных отношений спектральных
коэффициентов. Если нет, семейную ветвь смешивания следует заморозить.

## Links

- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version7-baseline-rooted-primitive-cycle-admission-gate]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[field-space-superconnection-bv-mapping-cone-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[version7-rank-change-parent-program]]
- [[live-formulas-gates-version7-26]]

## Source Notes

- `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`
- `s2t/audits/s2t_v7_cycle_holonomy_spectral_moment_scale_gate.py`
- `s2t/results/s2t_v7_cycle_holonomy_spectral_moment_scale_gate_results.json`