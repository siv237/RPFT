# Version VII: общий спектральный профиль singlet–virtual отношения

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, фиксирует ли один спектральный профиль два безразмерных параметра
совместного singlet--virtual потенциала: классическую силу циклического
смешивания `a` и перенормированный determinant-вес `gamma`.

## Search for Solution

Четырёхмерное тепловое разложение разделяет три уровня:

- Hodge-масса использует `f2 Lambda^2 a2`;
- Hodge-квартика использует `f0 a4`;
- первый шестирёберный цикл использует `f_{-2} a6/Lambda^2`.

После устранения размерностей остаётся профильный инвариант

$$R_\chi=\frac{f_2f_{-2}}{f_0^2}.$$

Для чистого профиля `chi_t(x)=exp(-t x)` он точно равен единице. Однако для
положительной смеси двух тепловых масштабов

$$
R_\chi=1+\frac{w(1-w)(t_1-t_2)^2}{t_1t_2},
$$

поэтому общий положительный профиль не фиксирует отношение. При плоском
профиле `chi'(0)=0` шестой коэффициент вообще исчезает.

Четырёхмерный determinant-вклад дополнительно требует локального
`|pq|^2`-контрчлена и масштаба согласования. Поэтому даже Gaussian-сокращение
классических моментов не фиксирует перенормированный `gamma`.

## Expected Result

Получен частичный положительный результат: Gaussian-линия проекта выделяет
класс `R_chi=1` без зависимости от теплового масштаба. Полного замыкания нет:
одна неизвестная функция не является одним числом, конечный коэффициент
полного `a6` ещё не вычислен, а `gamma` зависит от перенормировочного условия.

Следующий проверяемый шаг [[version7-full-product-a6-cycle-coefficient-gate]]
обнулил прежний up-цикл после раскрытия слабых интертвинеров. Ненулевая
ветвь перенесена в [[version7-weak-aligned-cycle-competition-gate]].

## Compliance Check

- Символьный аудит проверяет чистый Gaussian и двухмасштабную смесь точно.
- Контрольная смесь `w=1/2`, `t1=1`, `t2=4` даёт `R_chi=25/16`.
- Отдельно зафиксированы плоская ветвь `f_{-2}=0` и необходимость
  четырёхмерного контрчлена.
- Итог: `gaussian classical partial pass; general and renormalized no-go`.

## Links

- [[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[background-field-one-loop-determinant-literature-2026]]
- [[version7-full-product-a6-cycle-coefficient-gate]]

## Source Notes

- `s2t/gates/version7_common_spectral_profile_singlet_virtual_ratio_gate.tex`
- `s2t/audits/s2t_v7_common_spectral_profile_singlet_virtual_ratio_gate.py`
- `s2t/results/s2t_v7_common_spectral_profile_singlet_virtual_ratio_gate_results.json`