# Частичные изометрии, страты ранга и топологическая селекция

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная опора для проверки, может ли геометрия или мера выбрать
ранг один среди нулевых частичных изометрий обменного моста.

## Matrix Manifolds

- Edelman, Arias, Smith, *The Geometry of Algorithms with Orthogonality
  Constraints*, SIAM J. Matrix Anal. Appl. 20 (1998), 303--353,
  DOI `10.1137/S0895479895290954`: геометрия многообразий Штифеля и
  Грассмана.
- Mishra et al., *Fixed-rank matrix factorizations and Riemannian
  low-rank optimization*, `arXiv:1209.0430`: факторизационная и
  квотиентная геометрия матриц фиксированного ранга.

## Morse--Bott Measure

- Ludewig, *Strong Short Time Asymptotics and Convolution Approximation
  of the Heat Kernel*, `arXiv:1607.05152`: локальная лапласова асимптотика
  около чистых критических многообразий.
- *Laplace Asymptotics near Stratified Minimum Sets*,
  `arXiv:2608.02626`: явное разделение касательных и нормальных вкладов
  для стратифицированных минимумов.

## Defect Topology

- Mermin, *The topological theory of defects in ordered media*, Rev. Mod.
  Phys. 51 (1979), DOI `10.1103/RevModPhys.51.591`.
- Alexander, Chen, Matsumoto, Kamien, *Disclination loops, point defects,
  and all that in nematic liquid crystals*, Rev. Mod. Phys. 84 (2012),
  DOI `10.1103/RevModPhys.84.497`.

Эти работы подтверждают классификацию дефектов по вакуумному многообразию,
но не дают динамического предпочтения между двумя реализациями одного
`RP2`: линиями и ортогональными им плоскостями.

## Project Synthesis

Главный новый вывод проекта не является цитатой из литературы:

- плоская мера самосогласованного действия выбирает ранг 2;
- ранги 1 и 2 имеют одинаковую проекторную топологию `RP2`;
- нормированная double-path норма внешнего квадрата воспроизводит
  отрицательный инвариант чистоты с коэффициентом выше порога перехода;
- её присутствие в текущем родителе ещё нужно вывести.

## Links

- [[version6-partial-isometry-rank-stratum-selection-gate]]
- [[purification-induced-state-rank-strata-literature-2026]]
- [[rp2-vacuum-manifold-and-nematic-transition-literature-2026]]
- [[kibble-zurek-projective-defect-quench-literature-2026]]
- [[version6-matter-birth-program]]