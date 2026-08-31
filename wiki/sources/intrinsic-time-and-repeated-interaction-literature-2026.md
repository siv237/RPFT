# Внутреннее время и предел повторных взаимодействий

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Модульное время и collision models решают разные задачи. Первое извлекает
обратимый поток автоморфизмов из верного состояния; вторые получают
необратимую марковскую динамику из последовательности взаимодействий с
новыми подсистемами среды и подходящего непрерывного предела.

## Key Points

- Гипотеза теплового времени связывает физический поток с модульной группой
  состояния, но эта группа сохраняет само породившее её состояние.
- Повторные взаимодействия предполагают цепь внешних подсистем и масштабный
  предел силы связи и длительности столкновения.
- В подходящем пределе из полностью положительных дискретных карт возникает
  Lindblad-генератор и квантовый шум.
- Ни один из этих формализмов сам по себе не выбирает проектный коэффициент
  перевода безразмерного времени в физические единицы.
- Для проектных самосопряжённых jump-операторов repeated-interaction
  конструкция даёт явный кандидат
  `H_int=sum_a D_a tensor (|a><0|+|0><a|)`: его слабый предел возвращает
  GKSL-генератор, но не гарантирует совпадения с выбранным точным конечным
  Kraus-шагом на высших порядках.

## Links

- [[version8-intrinsic-noise-clock-dilation-gate]] — проектный тест.
- [[stinespring-rank-and-quantum-noise-dilation-literature-2026]] —
  непрерывная Fock-дилатация.
- [[version6-projective-quench-parent-dynamics-gate]] — ранний тест
  модульных и реляционных часов.
- [[version8-microscopic-interaction-hamiltonian-search]] — применение
  repeated-interaction механизма к двенадцатимерной cross-arrow опоре.

## Source Notes

- A. Connes, C. Rovelli, “Von Neumann algebra automorphisms and
  time–thermodynamics relation in generally covariant quantum theories”,
  Classical and Quantum Gravity 11 (1994), 2899–2918;
  arXiv:gr-qc/9406019.
- S. Attal, A. Joye, “Weak coupling and continuous limits for repeated
  quantum interactions”, Journal of Statistical Physics 126 (2007),
  1241–1283; arXiv:math-ph/0501012.
- S. Attal, Y. Pautrat, “From repeated to continuous quantum interactions”,
  Annales Henri Poincaré 7 (2006), 59–104; arXiv:math-ph/0311002.