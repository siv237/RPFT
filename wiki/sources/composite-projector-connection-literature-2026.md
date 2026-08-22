# Составные проекторные и restricted-связности

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная база для связности, построенной из локального направления
параметра порядка, и для границы между составной геометрией косета и
независимым калибровочным полем.

## Primary Sources

- Y. M. Cho, *Restricted Gauge Theory*, Physical Review D 21 (1980)
  1080--1088, DOI `10.1103/PhysRevD.21.1080`.
- L. Faddeev, A. J. Niemi, *Partially Dual Variables in SU(2)
  Yang--Mills Theory*, Physical Review Letters 82 (1999) 1624--1627,
  DOI `10.1103/PhysRevLett.82.1624`, `arXiv:hep-th/9807069`.
- L. Faddeev, A. J. Niemi, *Partial Duality in SU(N) Yang--Mills
  Theory*, Physics Letters B 449 (1999) 214--218,
  DOI `10.1016/S0370-2693(99)00100-8`, `arXiv:hep-th/9812090`.
- J. E. Avron, R. Seiler, B. Simon, *Homotopy and Quantization in
  Condensed Matter Physics*, Physical Review Letters 51 (1983) 51--53,
  DOI `10.1103/PhysRevLett.51.51`.

## Established Structure

Локальный единичный вектор или проектор позволяет выделить restricted
часть неабелевой связности и её топологическую кривизну. В проекторном
языке естественная кривизна имеет форму `P(dP)^2`, а составная
антисимметричная одноформа — тип `[P,dP]`.

Такая конструкция описывает геометрию орбиты параметра порядка, но сама по
себе не создаёт все независимые компоненты исходного Yang--Mills поля.
Стабилизаторная связность и дополнительные динамические моды требуют
отдельных данных.

## Project Consequence

Проектная формула `A_Q=[Q,dQ]/Delta^2` фиксирует профиль составной
связности непосредственно величиной ordered-щели. Она устраняет дальний
градиент ежа, но трансформационный аудит показывает отсутствие
неоднородного `O(2)`-компонента. Граничный тип этого компонента уже
присутствует как хопфова линия `L/L*`; её гладкое ядро и фермионный
оператор остаются открытыми.

## Links

- [[version6-gauged-projective-spin-cover-parent-gate]]
- [[version6-spatial-projective-defect-energy-spectrum-gate]]
- [[version5-spatial-so3-superconnection-parent-trace-gate]]
- [[version5-hopf-line-morita-orientation-functor-gate]]