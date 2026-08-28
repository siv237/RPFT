# Том VII: поиск происхождения Hodge-масштаба по формулам проекта

> Status: working
> Type: synthesis
> Updated: 2026-08-28

## Summary

Повторный проход по Томам III--VII, дотомовой генеалогии и литературе не
нашёл механизма, способного вывести абсолютный `mu` из одной безразмерной
структуры `H15`. Этот отрицательный итог уже поддерживается несколькими
независимыми линиями: гомотетией, свободой спектрального профиля,
перенормировочной схемой, RG-интеграционной константой и свободной
нормировкой нечётного поля суперсвязности.

Поиск выявил более точный вопрос: может ли `mu` быть относительной
амплитудой уже существующего физического фона `D_H15`. Последующий
[[version7-hodge-level-background-attribution-gate]] дал отрицательный
ответ. Три неэквивалентных фоновых ребра уже оставляют трёхмерное семейство
эквивариантных отображений; одна нормировка не устраняет две оставшиеся
степени свободы.

## Наследуемые запреты масштаба

| Механизм | Формульный результат | Граница |
|---|---|---|
| Глобальная гомотетия | `(g,D)->(lambda^2 g,lambda^-1 D)` | топология и конечная алгебра фиксируют только безразмерные отношения |
| Спектральное действие | `S=Tr f(D/Lambda)` | `Lambda` и моменты `f` являются данными, пока не сделаны динамическими |
| Компактные `a2/a4` | `chi^2=(f2/f0)Lambda^2-R/12` | две bare-связи сведены к одной, но комбинация остаётся свободной |
| Дилатон и radion | scale-invariant потенциал имеет общую плоскую орбиту | ненулевой классический масштаб не выбирается |
| Coleman--Weinberg | `Lambda_DT=mu exp(-integral dg/beta)` | требуется RG boundary condition и схема перенормировки |
| Product-superconnection | кинетика меняется как `a^2`, потенциал как `a^4` | нормированный след не выбирает нормировку нечётного поля `a` |
| Колчанное отображение момента | `||Phi-alpha||^2` | центральный уровень `alpha` является параметром устойчивости |
| Топологический дефект | фиксирует индексы и произведения масштаба | абсолютная длина или масса остаётся вдоль непрерывной орбиты |

Совпадение этих запретов означает, что очередной красивый способ положить
`mu=1` не является новым решением. Он лишь выбирает единицы.

## Философская зацепка проекта

В раннем проекте мир описывался как ткань или кристалл, а поздняя строгая
линия сформулировала принцип «первичен переход». Из этого следует полезное
уточнение:

> Масштаб должен быть не меткой топологии, а измеримой интенсивностью,
> частотой, щелью или нормой уже существующего перехода.

Поэтому естественный кандидат для `mu` — не число, приписанное проектору
`Gamma_E`, а инвариант фонового оператора, который действительно участвует
в замыкании цикла. В текущей ветви таким объектом является `D_H15`.

## Почему простой нормированный след неоднозначен

Для семейно-слепого фона три единичных ребра `H15` дают

$$
\operatorname{Tr}D_{H15}^2=6
$$

на скалярном девятивершинном графе. Но три естественные нормировки дают
разные ответы:

$$
\frac1{9}\operatorname{Tr}D_{H15}^2=\frac23,
\qquad
\frac1{5}\operatorname{Tr}_{\rm active}D_{H15}^2=\frac65,
\qquad
\frac1{2|E_0|}\operatorname{Tr}D_{H15}^2=1.
$$

Полный вершинный след, след активной опоры и среднее по ориентированным
рёбрам одинаково естественны до выбора физической меры. Поэтому формула
вида `mu^2=tau(D_H15^2)` сама по себе скрывает новый выбор `tau`.

## Операторный маршрут вместо скаляризации

Более сильный кандидат должен использовать не число, а сам фоновый
операторный момент. Пусть

$$
K_{15}=[d_{15},d_{15}^\dagger].
$$

Следующий гейт должен классифицировать отображения

$$
\Psi:\operatorname{Alg}(K_{15},P_C,P_I)
\longrightarrow\operatorname{End}(\mathcal K_E)
$$

со следующими условиями:

1. gauge-, Real- и градуировочная эквивариантность;
2. отсутствие выбора активной опоры после вычисления;
3. положительность относительно единого следа;
4. `Psi(K15)` пропорционален производной градуировке `hatGamma_E`;
5. пространство допустимых `Psi` одномерно, а нормировка фиксирована
   унитальным или следосохраняющим условием.

Классификация показала второй исход: отображений больше одного даже после
удаления общей нормировки. Поэтому происхождение уровня из `H15` закрыто;
отношение `mu/||D_H15||` также не выведено.

## Приоритет маршрутов

1. **Основной маршрут:** вывести отношение кинетики и Hodge-потенциала из
   одного произведённого пространственно-временного оператора.
2. **Резервный маршрут:** динамический дилатон полного спектрального действия
   с вычисленным суперследом и RG boundary condition.
3. **Честный EFT-маршрут:** принять одну абсолютную шкалу как train input и
   предсказывать только безразмерные отношения.
4. **Закрытые повторы:** `mu=1`, планковское отождествление, свободный
   spectral profile, выбранный FI-уровень и минимальная дзета-схема.

## Next Gate

[[version7-single-scale-calibration-closure-gate]] показал, что одна масса
замыкает линейные щели и даёт отношение `sqrt(2)`. Последующий
[[version7-spacetime-kinetic-potential-ratio-admission-gate]] сократил
рескейлинг поля, `f2` и cutoff, но оставил
`lambda_E=pi²/f0`. Gauge-якорь формально дал `lambda_E=q_Gg²/6`, но
редуцированный Hodge-след не определяет физический индекс `q_G`; прямой
перенос старого `q_G=2` закрыт. Полный gauge-подъём сохранил опору
селектора, но ненулевые `Q_LY_R` и `X_Lu_R` оказались цветовыми
триплетами, поэтому фундаментальный вакуум ломает `SU(3)_c`. Следующий гейт
— [[version7-color-preserving-composite-cycle-parent-gate]]. Он закрыл
классический составной обход нулевым гессианом и логикой произведения.

Повторный Schur-проход уточнил оставшуюся виртуальную ветвь. Два цветных
ребра входят в укоренённый цикл билинейно как тяжёлые бозонные переменные.
Без линейного источника их классическое исключение оставляет лёгкий
потенциал неизменным. Конечномерный детерминант создаёт отрицательный
квартичный член `-|z_(X_L e_R)z_(L_L Y_R)|^2`, но его гессиан в полном
нуле также равен нулю. Поэтому виртуальный блок может связывать уже
запущенные бесцветные рёбра, но не является самостоятельным источником их
квадратичного запуска; см.
[[version7-virtual-colored-bridge-project-intuition-search]]. Последующий
[[version7-virtual-colored-bridge-schur-complement-gate]] подтвердил это
точно: цвет сохраняется при `a=b=0`, но tree-level поправка равна нулю,
детерминант начинается с квартики, а четырёхмерная нормировка требует
контрчлена. Следующий гейт —
[[version7-color-preserving-quadratic-selector-origin-gate]]. Он дал
положительный результат: точное ядро gauge-Casimir совпало с ранее
выведенным изотипическим проектором `P_I`. Четыре gauge-синглетных ребра
получают отрицательный Hodge-знак, два цветных циклических моста остаются
массивными, а пять нежелательных рёбер сохраняют щель. Следующий гейт —
[[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]].
Он подтвердил локальную совместимость: существует открытая область
`a u²(2u-1)<1`, в которой singlet-радиалы устойчивы и цветная тяжёлая мода
не закрывается. Однако конечномерная determinant-модель не ограничена снизу
у границы щели, не фиксирует четыре фазы и зависит от двух безразмерных
отношений. Следующий гейт
[[version7-common-spectral-profile-singlet-virtual-ratio-gate]] показал,
что чистый Gaussian выделяет `R_chi=1`, но общий положительный профиль
оставляет этот инвариант переменным, а determinant-вес требует
перенормировочного условия. Следующий тест —
[[version7-full-product-a6-cycle-coefficient-gate]].
Он дал строгий отрицательный ответ для прежней up-ветви:
`tilde(H)^dagger H=0`, поэтому её полный коэффициент равен нулю. При этом
down-цикл и слабая дублетная пара оба выживают с коэффициентом `12` в
`Tr Phi^6` и коэффициентом `-2` в Gaussian-`a6`. Следующий гейт должен
проверить их совместную конкуренцию и устойчивость полного точного профиля:
[[version7-weak-aligned-cycle-competition-gate]].
Смешивание остаётся замороженным до второго некоммутирующего семейного
тензора.

## Links

- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[version7-higher-cycle-character-mixing-freeze-gate]]
- [[version3-absolute-scale-no-go]]
- [[version3-dilaton-radion-transmutation-gate]]
- [[version3-rg-anomaly-scale-setting-gate]]
- [[version3-spectral-function-moment-menu-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[version5-ordinary-spectral-moment-map-no-go-gate]]
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
- [[pre-tome-formula-genealogy]]
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
- [[version7-weak-aligned-cycle-competition-gate]]

## Source Notes

- `s2t/gates/version3_absolute_scale_no_go.tex`
- `s2t/gates/version3_compact_a2_a4_moment_gate.tex`
- `s2t/gates/version3_dilaton_radion_transmutation_gate.tex`
- `s2t/gates/version3_rg_anomaly_scale_setting_gate.tex`
- `s2t/gates/version5_projector_superconnection_common_scale_gate.tex`
- `s2t/gates/version5_m300_hodge_curvature_hessian_gate.tex`
- `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex`
- `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex`
- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`