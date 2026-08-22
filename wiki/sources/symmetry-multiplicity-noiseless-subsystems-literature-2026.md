# Пространства кратности, симметрия и noiseless subsystems

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная опора для различения размерности неприводимого
представления, числа эквивалентных копий и физически доступного
пространства кратности.

## Primary Sources

- P. Zanardi, M. Rasetti, *Noiseless Quantum Codes*, Physical Review
  Letters 79 (1997) 3306--3309, DOI
  `10.1103/PhysRevLett.79.3306`, `arXiv:quant-ph/9705044`.
- E. Knill, R. Laflamme, L. Viola, *Theory of Quantum Error Correction
  for General Noise*, Physical Review Letters 84 (2000) 2525--2528, DOI
  `10.1103/PhysRevLett.84.2525`, `arXiv:quant-ph/9908066`.

В разложении представления на неприводимые компоненты симметрично
доступная память находится в пространстве кратности эквивалентных копий.
Размерность одной неприводимой компоненты не является такой памятью:
операторы коммутанта действуют на ней скалярно.

## Project Consequence

- размеры блоков `H15=(6,2,3,3,1)` являются gauge-размерностями пяти
  различных представлений с кратностью один;
- KO6-удвоение связывает противоположные градуировки и не является двумя
  свободными копиями;
- ранги углов `M20`, `M35` относятся к алгебрам операторов;
- аффинный сектор `P3 C4` является настоящим трёхмерным вырожденным
  подпространством высоты и канонически изометричен семейному триплету.

Последний пункт даёт реальную резонансную кратность, но она расположена в
соседнем углу прямой суммы. Каноническая связь `rho V` изотропна, поэтому
сама не выбирает одноосную фазу.

## Links

- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version6-clock-controlled-energy-conserving-quench-gate]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]