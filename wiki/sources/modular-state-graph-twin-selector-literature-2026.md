# Модулярное состояние, графовые близнецы и селектор копий

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Литературная сверка поддерживает два разных утверждения. Модулярные
спектральные тройки действительно используют состояние и его модулярную
группу как геометрические данные. Теория графовых близнецов, напротив,
подтверждает, что одинаковые соседства создают спектрально неразличимые
вершины. Вместе это означает: модулярный вес может стать селектором только
после независимого происхождения проекторов, различающих копии.

## Key Points

- В модулярной спектральной геометрии вес или состояние является частью
  конструкции, а не безобидной заменой обычного следа.
- В обычном спектральном действии базовый бозонный функционал строится из
  следа функции оператора Дирака; локализованный проекторный вес требует
  отдельного обоснования.
- Вершины-близнецы имеют одинаковые соседства. Их перестановка является
  автоморфизмом графа, поэтому матрица смежности и её спектральные функции
  не выбирают одну вершину из пары.
- Современные работы по взвешенным графам отдельно изучают сильную
  коспектральность и динамику пар близнецов; это согласуется с точным
  `S2 x S2` препятствием четырёхвершинного графа Тома VII.
- Классификация конечных спектральных троек рассматривает оператор Дирака и
  его стрелки как часть данных тройки; множество допустимых стрелочных
  мест не предоставляет канонический ненулевой элемент каждого блока.

## Relevance to Tome VII

Литература не выводит проектор старой копии. Она лишь подтверждает
правильную логическую последовательность:

$$
\text{независимая проекторная алгебра}
\longrightarrow
\text{модулярное состояние}
\longrightarrow
\text{поляризация или взвешенный момент}.
$$

Обратный порядок, при котором проектор выбирается после просмотра нужного
ядра, остаётся подгонкой.

## Primary Sources

- M. Eckstein, B. Iochum, *Spectral Action in Noncommutative Geometry*,
  arXiv:1902.05306.
- F. Ciolli, F. Fidaleo, *Modular spectral triples and deformed Fredholm
  modules*, arXiv:2206.14762.
- H. Monterde, *Strong cospectrality and twin vertices in weighted graphs*,
  arXiv:2111.01265.
- S. Kirkland, H. Monterde, S. Plosker, *Quantum state transfer between
  twins in weighted graphs*, arXiv:2201.02720.
- T. Krajewski, *Classification of finite spectral triples*,
  arXiv:hep-th/9701081.
- B. Cacic, *Moduli Spaces of Dirac Operators for Finite Spectral Triples*,
  arXiv:0902.2068.

## Links

- [[version7-copy-selector-project-archaeology]]
- [[version7-vectorlike-kernel-selector-intuition-map]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[version7-universal-incidence-parent-admissibility-gate]]

## Source Notes

- Literature checked on 2026-08-27.
- Project comparison: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex`.