# Внешний аудит winding determinant на RP3 x S1

> Статус: внутреннее Bessel-число подтверждено, determinant-интерпретация уточнена
> Дата: 2026-08-03
> Машинный результат: `external_rp3xs1_winding_determinant_results.json`

## Вопрос

Совпадает ли внутренняя величина

```text
T_coex = sum d*rho*sum_q K1(2*pi*q*rho)/q
```

с конечной winding-частью Maxwell determinant на `RP^3 x S^1`?

## Независимое воспроизведение

Для untwisted coexact spectrum

```text
rho_m=2m,
d_m=8m^2-2,
m>=1
```

высокоточное независимое суммирование даёт

```text
T_coex^RP3 = 1.5227161455271526e-5.
```

Внутреннее значение равно `1.5227161455271536e-5`. Различие меньше `10^-18`. Следовательно, старый численный расчёт Bessel-суммы корректен.

## Какой объект вычисляет K1-сумма

Внутренняя формула начинается не с `log det`, а с Casimir-energy zeta function

```text
E(s)=1/2 sum_{k in Z}(k^2+rho^2)^(1/2-s).
```

Применение Epstein/Poisson continuation даёт для nonzero windings

```text
E_nonlocal = -(rho/pi) sum_{q>=1} K1(2*pi*q*rho)/q.
```

Поэтому для полной башни

```text
E_coex^nonlocal = -T_coex/pi
                 = -4.846956029729684e-6.
```

Старая величина `T_coex` является положительным ядром этой энергии, но не самой физически нормированной энергией.

## Что даёт настоящий log determinant

Для оператора на окружности выполняется

```text
det(-d_tau^2+rho^2) = 4 sinh^2(pi*rho).
```

После удаления локальной части `2*pi*rho` остаётся

```text
(log det)_winding = 2 log(1-exp(-2*pi*rho)).
```

Суммирование untwisted coexact tower даёт

```text
(log det)_winding = -4.1848910943358096e-5,
Gamma_boson,winding = 1/2 log det
                     = -2.0924455471679048e-5.
```

По модулю bosonic determinant contribution в `1.374153...` раза больше `T_coex`. Следовательно, Bessel Casimir-energy sum и Euclidean determinant winding part не являются одной и той же величиной.

## Вердикт

Положительный результат:

- spectrum и внутреннее число `T_coex` подтверждены;
- coexact nonlocal tail действительно ненулевой;
- доминирование первой оболочки подтверждено.

Отрицательный результат:

- `T_coex` нельзя непосредственно называть determinant residue;
- множитель, знак и размерность зависят от выбора между Casimir energy и Euclidean effective action;
- прежняя связь `T_coex -> pi^-4` требует нового вариационного моста, а не только численного совпадения.

## Влияние на теорию

Это ещё сильнее снижает перспективность точной вакуумной формулы в текущем виде. Проблема уже не только в отсутствии cancellation: необходимо сначала однозначно определить функционал, из которого строится `S_vac`.

При этом спектральная часть исследования усиливается: ненулевой глобальный coexact contribution подтверждён двумя разными объектами --- Casimir energy и log determinant.

## Следующий шаг

Нужно выбрать один первичный функционал:

1. Casimir energy на пространственном `RP^3` с периодическим направлением;
2. Euclidean one-loop effective action на `RP^3 x S^1`.

После этого следует вывести полный Maxwell--FP prefactor, включая scalar half-determinant, знак, радиусные степени и перевод результата в безразмерный `S_vac`. До этого дальнейшее сравнение с `pi^-4` не является однозначным.