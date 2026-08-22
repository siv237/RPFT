# Кинетика перехода первого рода и проекторная кристаллизация

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная база для динамической интерпретации найденного перехода
`I3/3 -> RP2`: метастабильность, нуклеация, спинодальный распад,
релаксационная динамика ориентационного параметра и образование дефектов.

## Nucleation and Metastability

- J. S. Langer, *Theory of Nucleation Rates*, Physical Review Letters 21
  (1968) 973--976, DOI `10.1103/PhysRevLett.21.973`.
- J. S. Langer, *Statistical Theory of the Decay of Metastable States*,
  Annals of Physics 54 (1969) 258--275, DOI
  `10.1016/0003-4916(69)90153-5`.
- J. W. Cahn, J. E. Hilliard, *Free Energy of a Nonuniform System. I.
  Interfacial Free Energy*, Journal of Chemical Physics 28 (1958)
  258--267, DOI `10.1063/1.1744102`.
- J. W. Cahn, J. E. Hilliard, *Free Energy of a Nonuniform System. III.
  Nucleation in a Two-Component Incompressible Fluid*, Journal of
  Chemical Physics 31 (1959) 688--699, DOI `10.1063/1.1730447`.

Лангер даёт общий закон распада метастабильной фазы через критический
зародыш. Критический радиус и экспонента скорости зависят от натяжения
границы и объёмного выигрыша свободной энергии. Поэтому один локальный
потенциал определяет наличие барьера, но не абсолютную скорость перехода.

## Spinodal Decomposition

- J. W. Cahn, *On Spinodal Decomposition*, Acta Metallurgica 9 (1961)
  795--801, DOI `10.1016/0001-6160(61)90182-1`.
- P. C. Hohenberg, B. I. Halperin, *Theory of Dynamic Critical
  Phenomena*, Reviews of Modern Physics 49 (1977) 435--479, DOI
  `10.1103/RevModPhys.49.435`.
- S. M. Allen, J. W. Cahn, *A Microscopic Theory for Antiphase Boundary
  Motion and Its Application to Antiphase Domain Coarsening*, Acta
  Metallurgica 27 (1979) 1085--1095, DOI
  `10.1016/0001-6160(79)90196-2`.

Внутри спинодали однородная фаза имеет отрицательную кривизну и распадается
без активационного зародыша. Для не сохраняемого ориентационного параметра
естественна динамика Model A / Allen--Cahn. Она требует коэффициента
подвижности, градиентной нормы и шума, не определяемых статической свободной
энергией.

## Nematic Quench and Defects

- Z. Bradač, S. Kralj, S. Žumer, *Molecular Dynamics Study of the
  Isotropic--Nematic Quench*, Physical Review E 65 (2002) 021705, DOI
  `10.1103/PhysRevE.65.021705`.
- I. Chuang, R. Durrer, N. Turok, B. Yurke, *Cosmology in the
  Laboratory: Defect Dynamics in Liquid Crystals*, Science 251 (1991)
  1336--1342, DOI `10.1126/science.251.4999.1336`.
- T. W. B. Kibble, *Topology of Cosmic Domains and Strings*, Journal of
  Physics A 9 (1976) 1387--1398, DOI
  `10.1088/0305-4470/9/8/029`.
- W. H. Zurek, *Cosmological Experiments in Superfluid Helium?*, Nature
  317 (1985) 505--508, DOI `10.1038/317505a0`.

Моделирование изотропно-нематического quench различает ранний рост
параметра порядка, доменный режим и позднюю динамику отдельных дефектов.
Космологическая аналогия жидких кристаллов подтверждает сам принцип:
несогласованные выборы вакуума в разных доменах оставляют топологические
дефекты.

## First-Order Boundary of Kibble--Zurek

- F. Suzuki, W. H. Zurek, *Topological Defect Formation in a Phase
  Transition with Tunable Order*, Physical Review Letters 132 (2024)
  241601, DOI `10.1103/PhysRevLett.132.241601`.

Стандартный Kibble--Zurek предназначен для непрерывных переходов и не
переносится автоматически на строгий переход первого рода. Для слабого
перехода первого рода Suzuki--Zurek объединяют неравновесное замораживание
с теорией нуклеации. Это поддерживает проектное разделение: топология
Киббла задаёт тип дефекта, а динамический размер домена должен вычисляться
из нуклеации или спинодального роста.

## Project Consequence

Точный функционал проекта имеет три различные температуры:

- `beta_ord = 1.3417938971...` — рождение метастабильного ordered-минимума;
- `beta_c = 1.5426695409...` — равновесное сосуществование;
- `beta_sp = 21/2` — потеря локальной устойчивости изотропной фазы.

Поэтому возможен длительный переохлаждённый гладкий режим, заканчивающийся
либо случайной нуклеацией, либо спинодальным распадом. Литература объясняет
эту кинетику условно при заданном quench, но не выводит проектный закон
`beta(tau)` из безвременной замкнутой системы.

## Links

- [[version6-modular-cooling-projective-transition-gate]]
- [[version6-tensor-square-relative-carrier-normalization-gate]]
- [[kibble-zurek-projective-defect-quench-literature-2026]]
- [[rp2-vacuum-manifold-and-nematic-transition-literature-2026]]
- [[version6-nongaussian-spatial-stiffness-saturation-gate]]