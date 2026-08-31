# Точная LCF-проверка безразмерного шумового времени

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Cross-arrow процесс точно образует безразмерную полугруппу. Его полный
спектр на 221-мерной endpoint-алгебре и collision-limit теперь проверены
LCF-ядром. Физический коэффициент времени `kappa` остаётся свободным.

## Problem

Заменить численный scan столкновений строгим пределом и проверить, способен
ли собственный модульный поток дать требуемый диссипативный перенос.

## Search for solution

- Построена точная матрица cross-GKSL генератора на полном corner-базисе.
- Характеристический многочлен факторизован над рациональными числами.
- Применено конечномерное правило Чернова к точному Kraus-тангенсу.
- Модульные коммутаторы центральных проекторов вычислены символически.
- Проверена инвариантность ядра при любом положительном масштабе `kappa`.

## Expected result

Безразмерный поток и collision-limit должны быть строгими, но ни один из них
не должен без дополнительного закона фиксировать секунду или источник
свежих состояний среды.

## Compliance check

- `dim ker L_cross=46`, щель `1/2`, максимум `8` — точно.
- Полный спектр имеет суммарную кратность `221`.
- `T_(u+v)=T_u T_v` для матричной экспоненты.
- Модульный поток фиксирует `Pq,Pl`, тогда как норма диссипативного движения
  `Pq` в квадрате равна `72`.
- `Phi_(u/n)^n -> exp(u L_cross)` в операторной норме.
- `kappa`, длительность такта и автономная подача ancilla не выведены.

## Links

- [[version8-intrinsic-noise-clock-dilation-gate]]
- [[version8-minimal-covariant-stinespring-lcf-migration-gate]]
- [[version8-full-primitive-markov-generator-assembly-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]

## Source Notes

- `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_intrinsic_noise_clock_lcf_migration_gate.py`
- `s2t/results/s2t_v8_intrinsic_noise_clock_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_noise_clock.py`