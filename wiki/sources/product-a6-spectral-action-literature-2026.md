# Product-коэффициент $a_6$ и спектральное действие: литература 2026

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Первичная литература подтверждает, что коэффициент `a6` полного
четырёхмерного product-оператора нельзя отождествлять только с конечным
следом `Tr D_F^6`. В общем фоне он содержит производные поля, gauge-кривизну,
кривизну пространства-времени и смешанные локальные инварианты. Однако на
плоском фоне, при постоянном внутреннем поле и нулевой gauge-кривизне,
product heat trace факторизуется, и потенциальная часть `a6` извлекается
точно из конечного экспоненциального следа.

## Constant Flat Reduction

Для

$$
D=D_M\otimes1+\gamma^5\otimes\Phi,
\qquad D^2=D_M^2\otimes1+1\otimes\Phi^2
$$

при постоянном `Phi` выполнено

$$
\operatorname{Tr}e^{-tD^2}
=\operatorname{Tr}e^{-tD_M^2}\operatorname{Tr}_F e^{-t\Phi^2}.
$$

Внутренний множитель имеет точное разложение

$$
\operatorname{Tr}_F e^{-t\Phi^2}
=N-t\operatorname{Tr}\Phi^2
+\frac{t^2}{2}\operatorname{Tr}\Phi^4
-\frac{t^3}{6}\operatorname{Tr}\Phi^6+O(t^4).
$$

Поэтому в Gaussian-конвенции потенциальный коэффициент шестой степени имеет
знак `-1/6`. Если конечный след содержит циклический вклад
`12 r^4 ReTr W_C`, его голый Gaussian-множитель равен `-2` до общего
положительного spin/volume/Real-фактора. При сохранении знака явными
интертвинами это предпочитает `W_C=I`, а не `-I`.

## Why the General $a_6$ Is Larger

Общие формулы теплового ядра для оператора лапласова типа показывают, что
`a6` содержит множество инвариантов из `E`, `Omega`, их ковариантных
производных и геометрической кривизны. Работы о dimension-six секторе
спектрального действия также подчёркивают зависимость этих операторов от
деталей функции отсечения и масштаба.

Для текущего гейта это означает двухступенчатую проверку:

1. сначала постоянный плоский потенциальный блок;
2. затем производные и gauge-кривизна для кинетики и полной физической
   устойчивости.

Потенциальный гессиан однородных мод можно вычислять на первом уровне, но
его нельзя объявлять полным пространственно-временным гессианом.

## Quiver Boundary

Спектральное действие колчана организует конечные следы как суммы замкнутых
путей. Поэтому `Tr Phi^6` считает не только выбранный примитивный цикл, но и
все возвратные и повторные шестишаговые обходы. Проект уже вычислил полный
редуцированный ответ:

$$
\operatorname{Tr}\Phi^6
=54+144r^2+306r^4+324r^6+12r^4\operatorname{ReTr}W_C.
$$

В следующем гейте запрещено извлекать только последний член. Остальные
члены сдвигают квадратичные, квартичные и шестые радиальные коэффициенты и
могут изменить стационарность и гессиан.

## Project Risks Before Calculation

- Полный gauge-взвешенный носитель пока задаёт представления и кратности,
  но не все явные матричные интертвинеры и их нормировки.
- Два старых корневых ребра использовались как замороженный фон. В одном
  действии их радиальные вариации надо включить либо доказать их
  ортогональное отделение.
- Hodge-проекторный потенциал и обычный `Tr Phi^{2n}` не доказаны как
  коэффициенты одного и того же полного оператора. Добавлять `a6` к ранее
  выбранному Hodge-потенциалу вручную нельзя.
- Для Gaussian-профиля доступен точный конечный множитель
  `Tr exp(-Phi²/Lambda²)`. Поэтому после `a6`-усечения нужно измерить остаток;
  при `||Phi||/Lambda` порядка единицы асимптотический полином не является
  достаточным контролем.
- Real-полуслед и spin trace могут менять общий множитель, но не должны
  менять относительный знак; это требуется проверить на явной матрице.

## Project Result

[[version7-full-product-a6-cycle-coefficient-gate]] подтвердил, что явные
интертвинеры существенны: редуцированный up-цикл с коэффициентом `12`
обнулился множителем `H_tilde^dagger H=0`. Одновременно полный граф открыл
down-цикл и слабую дублетную пару с ненулевыми коэффициентами. Поэтому
литературная осторожность к полному эндоморфизму `E` реализовалась как
конкретная смена ветви проекта.

## Primary Sources

- D. V. Vassilevich, *Heat Kernel Expansion: User's Manual*,
  arXiv:hep-th/0306138.
- A. E. M. van de Ven, *Index-free Heat Kernel Coefficients*,
  arXiv:hep-th/9708152. Формулы высших коэффициентов следует использовать
  осторожно с учётом последующих замечаний к высоким порядкам.
- S. A. Franchino-Viñas, *Comment on ``Index-free Heat Kernel
  Coefficients''*, arXiv:2401.01296.
- A. Devastato, F. Lizzi, C. Valcarcel Flores, D. Vassilevich,
  *Unification of Coupling Constants, Dimension Six Operators and the
  Spectral Action*, arXiv:1410.6624.
- C. I. Pérez-Sánchez, *The Spectral Action on Quivers*,
  arXiv:2401.03705.
- A. H. Chamseddine, A. Connes, *The Spectral Action Principle*,
  arXiv:hep-th/9606001.

## Links

- [[version7-full-product-a6-cycle-coefficient-gate]]
- [[version7-common-spectral-profile-singlet-virtual-ratio-gate]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[version7-full-product-a6-project-intuition-search]]
- [[version7-weak-aligned-cycle-competition-gate]]

## Source Notes

- Литературный проход выполнен 2026-08-28.
- `s2t/gates/version3_product_heat_kernel_kappa_gate.tex`
- `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex`
- `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`
- `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex`