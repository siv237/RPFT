# Масштаб спектрального действия, дилатон и уровень отображения момента

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Первичная литература различает три вещи, которые в проекте нельзя смешивать:

1. масштаб отсечения `Lambda` в спектральном действии;
2. динамическое поле дилатона, заменяющее постоянный масштаб;
3. центральный уровень `alpha` отображения момента, задающий условие
   устойчивости колчанного quotient.

Ни один из этих формализмов автоматически не вычисляет численное значение
вакуумного масштаба из одного графа. Дилатон превращает внешний масштаб в
поле, но положение его вакуума требует потенциала и квантовых граничных
данных. В теории представлений колчанов уровень отображения момента является
параметром quotient и стратификации.

## Spectral Scale and Dilaton

В исходном принципе спектрального действия функционал имеет вид
`Tr chi(D/Lambda)`: функция отсечения и масштаб являются данными действия.
Работа Chamseddine--Connes показывает, что `Lambda` можно заменить
дилатонным полем и получить почти масштабно-инвариантное действие с
определёнными связями дилатона.

Это важный структурный прецедент для Тома VII: параметр `mu` допустимо
заменить полем или нормой существующего оператора. Но сама такая замена ещё
не выбирает ненулевое среднее поля. Требуется отдельное уравнение вакуума,
гравитационный масштаб или квантовое нарушение масштабной симметрии.

## Moment-Map Level

В пространстве представлений колчана квадрат нормы обычно рассматривается
как `||Phi-alpha||^2`, где `alpha` является центральным параметром и задаёт
условие устойчивости. Harada--Wilkin доказывают сходимость потока и связь
Morse-стратификации с Harder--Narasimhan-стратификацией при выбранном
параметре.

Следовательно, теория отображения момента объясняет динамику после выбора
уровня, но не превращает сам уровень в следствие немеченого графа. Для S2T
это означает: `mu^2 Gamma_E` нельзя объявлять выведенным только потому, что
квадрат нормы отображения момента стандартен.

## Quantum Scale Generation

Coleman--Weinberg и связанные механизмы способны заменить классический
размерный параметр квантовой шкалой. Однако шкала зависит от безразмерных
связей, бета-функций и условия перенормировки. Проектный RG-аудит уже
зафиксировал эту границу как интеграционную константу траектории.

Поэтому квантовая трансмутация остаётся допустимой новой физической ветвью,
но не является бесплатным способом вычислить `mu` из `H15`.

## Project Consequence

Литература оставляет один ближайший экономный тест: попытаться атрибутировать
уровень Hodge-момента уже существующему фоновому оператору, а не вводить
новый FI-параметр. Нужно классифицировать Real-, gauge- и
градуировочно-эквивариантные отображения от инвариантов `D_H15` к
`Gamma_E`.

Даже положительный результат сможет вывести только отношение `mu` к масштабу
`D_H15`. Абсолютная единица по-прежнему потребует одного физического
scale-setting input или отдельного гравитационно-квантового механизма.

## Проверенный итог Тома VII

[[version7-hodge-level-background-attribution-gate]] выполнил этот тест.
Три калибровочно неэквивалентных фоновых ребра дают три независимых
положительных функционала момента. Поэтому пространство допустимых
отображений в прямую `R hatGamma_E` уже трёхмерно, а после нормировки остаётся
двумерным. Литературная граница реализовалась буквально: фон даёт
масштабные наблюдаемые, но не выбирает центральный уровень без
дополнительного параметра устойчивости или физической калибровки.

Последующий [[version7-single-scale-calibration-closure-gate]] показал
границу одной такой калибровки. Она фиксирует общий квадратичный масштаб и
отношение линейных масс `sqrt(2)`, но не эффективную квартику
`kappa/Z²`. Последующий product heat-kernel расчёт сделал границу точнее:
рескейлинг нечётного поля, `f2` и cutoff сокращаются, тогда как
`lambda_E=pi²/f0`. Значит, остаётся не произвольная пара нормировок, а один
момент функции отсечения. Попытка фиксировать его общим gauge-блоком дала
условное `lambda_E=q_Gg²/6`, но также подтвердила литературное требование:
`q_G` вычисляется полным следом по представлениям. Незавешенный след по
меткам рёбер его не определяет. Полное раскрытие дополнительно показало,
что два выбранных блока являются цветовыми триплетами; ненулевой
фундаментальный Hodge-вакуум поэтому не сохраняет `SU(3)_c`. Замкнутое
слово само gauge-инвариантно, но его классический ненулевой уровень требует
ненулевых множителей. Возможность нулевых одноточечных средних при ненулевом
составном корреляторе относится уже к квантовой мере.

Гейт [[version7-common-spectral-profile-singlet-virtual-ratio-gate]] уточнил
роль самой функции отсечения. После сведения размерностей остаётся
`R_chi=f2 f_{-2}/f0²`. Чистый heat-kernel профиль `exp(-t x)` даёт
`R_chi=1`, но положительная смесь тепловых масштабов оставляет этот инвариант
переменным. Следовательно, Gaussian является содержательной проектной
гипотезой, но не автоматическим следствием спектрального принципа. Плоский
в нуле профиль имеет `f_{-2}=0` и удаляет классический `a6`-цикл.

## Primary Sources

- A. H. Chamseddine, A. Connes, *The Spectral Action Principle*,
  arXiv:hep-th/9606001.
- A. H. Chamseddine, A. Connes, *Scale Invariance in the Spectral Action*,
  arXiv:hep-th/0512169.
- A. A. Andrianov, M. A. Kurkov, F. Lizzi, *Spectral Action from
  Anomalies*, arXiv:1103.0478.
- M. Harada, G. Wilkin, *Morse Theory of the Moment Map for
  Representations of Quivers*, arXiv:0807.4734.
- S. Coleman, E. Weinberg, *Radiative Corrections as the Origin of
  Spontaneous Symmetry Breaking*, Physical Review D 7 (1973), 1888--1910.

## Links

- [[version7-hodge-scale-origin-project-intuition-search]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[version3-absolute-scale-no-go]]
- [[version3-dilaton-radion-transmutation-gate]]
- [[version3-rg-anomaly-scale-setting-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[version7-hodge-level-background-attribution-gate]]
- [[version7-single-scale-calibration-closure-gate]]
- [[version7-spacetime-kinetic-potential-ratio-admission-gate]]
- [[version7-common-gauge-f0-anchor-gate]]
- [[version7-full-gauge-weighted-edge-carrier-gate]]
- [[version7-color-preserving-composite-cycle-parent-gate]]
- [[version7-virtual-colored-bridge-schur-complement-gate]]
- [[version7-color-preserving-quadratic-selector-origin-gate]]
- [[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]]
- [[version7-common-spectral-profile-singlet-virtual-ratio-gate]]
- [[version7-full-product-a6-cycle-coefficient-gate]]

## Source Notes

- `s2t/gates/version3_absolute_scale_no_go.tex`
- `s2t/gates/version3_dilaton_radion_transmutation_gate.tex`
- `s2t/gates/version3_rg_anomaly_scale_setting_gate.tex`
- `s2t/gates/version5_projector_superconnection_common_scale_gate.tex`
- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`