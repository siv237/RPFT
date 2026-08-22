# Охлаждение подсистемы, корреляции и конечные квантовые часы

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Первичная литература для вопроса, может ли малая подсистема охлаждаться и
упорядочиваться внутри полностью замкнутой квантовой системы, передавая
энтропию внутреннему носителю часов.

## Canonical Typicality and Equilibration

- S. Popescu, A. J. Short, A. Winter, *The Foundations of Statistical
  Mechanics from Entanglement: Individual States vs. Averages*,
  `arXiv:quant-ph/0511225`; опубликовано как *Entanglement and the
  Foundations of Statistical Mechanics*, Nature Physics 2 (2006)
  754--758, DOI `10.1038/nphys444`.
- N. Linden, S. Popescu, A. J. Short, A. Winter, *Quantum Mechanical
  Evolution Towards Thermal Equilibrium*, Physical Review E 79 (2009)
  061103, DOI `10.1103/PhysRevE.79.061103`, `arXiv:0812.2385`.

Малая подсистема большого замкнутого целого может иметь почти тепловое
редуцированное состояние. Глобальная чистота или унитарность не запрещает
локального роста или уменьшения энтропии. Но типичность и устойчивое
равновесие требуют достаточно большого эффективного окружения и не
следуют из одного четырёхмерного носителя.

## Correlations and the Thermodynamic Arrow

- M. H. Partovi, *Entanglement Versus Stosszahlansatz: Disappearance of
  the Thermodynamic Arrow in a High-Correlation Environment*, Physical
  Review E 77 (2008) 021110, DOI `10.1103/PhysRevE.77.021110`.
- D. Jennings, T. Rudolph, *Entanglement and the Thermodynamic Arrow of
  Time*, Physical Review E 81 (2010) 061130, DOI
  `10.1103/PhysRevE.81.061130`, `arXiv:1002.0314`.

Начальные корреляции способны менять и даже обращать обычное направление
теплового потока. Поэтому коррелированный начальный мир может охладить
выбранную подсистему, но такая корреляция является физическим ресурсом и
граничным условием, а не бесплатным следствием унитарности.

## Autonomous Clocks and Backreaction

- P. Erker, M. T. Mitchison, R. Silva, M. P. Woods, N. Brunner,
  M. Huber, *Autonomous Quantum Clocks: Does Thermodynamics Limit Our
  Ability to Measure Time?*, `arXiv:1609.06704`.
- M. P. Woods, R. Silva, J. Oppenheim, *Autonomous Quantum Machines and
  the Finite Sized Quasi-Ideal Clock*, Annales Henri Poincaré 20 (2019)
  125--218, `arXiv:1607.04591`.

Автономные часы являются неравновесным ресурсом. Их точность связана с
энтропийным производством, а управление другой подсистемой вызывает
обратную реакцию. Это поддерживает проектный запрет считать один
четырёхтактный носитель одновременно идеальными часами и неизменным
стоком энтропии.

## Autonomous Refrigeration

- N. Linden, S. Popescu, P. Skrzypczyk, *How Small Can Thermal Machines
  Be? The Smallest Possible Refrigerator*, Physical Review Letters 105
  (2010) 130401, DOI `10.1103/PhysRevLett.105.130401`.

Автономное охлаждение возможно в малых квантовых системах, но требует
резонансных энергетических уровней и нескольких тепловых ресурсов. Само
условие `U^4=I` не задаёт ни энергетические разрывы, ни холодильный цикл.

## Project Consequence

Четырёхсостояний носитель имеет энтропийную ёмкость `log4`, превышающую
требуемый экспорт `0.7402345698...`. Более того, существует явная
унитарная орбита полного `3 x 4`-состояния, дающая ordered-редукцию
триплета. Но часы при этом становятся смешанными ранга три. Не выведены
энергосохраняющее взаимодействие, автономное управление и необратимый
предел.

## Links

- [[version6-internal-entropy-transfer-cooling-gate]]
- [[version6-modular-cooling-projective-transition-gate]]
- [[relational-modular-internal-time-literature-2026]]
- [[version6-projective-quench-parent-dynamics-gate]]