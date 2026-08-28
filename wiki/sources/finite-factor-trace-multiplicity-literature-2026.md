# Конечные факторы, кратности и следовые веса

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Классификация конечных спектральных троек кодирует представления и их
кратности диаграммами Краевского. Простой матричный фактор имеет единственный
нормированный след; прямая сумма факторов допускает центральные относительные
веса. Переход от блочно-диагональной суммы к простому фактору требует
внедиагональных связующих блоков и потому меняет физический носитель.

## Project Reading

Носители размерностей `22` и `21` не создают коэффициент автоматически.
Равномерная кратность сокращается в нормированном следе. Отношение `11/21`
численно проходит гессиан, но умножение всего действия на след corner-
проектора не равно вставке этого проектора внутрь одного следа.

Новый проход по минимальным опорам усиливает границу. Концевая кривизна
после сжатия живёт на `C21` и порождает полный фактор
`M21(C)`. Но 54-мерный диагональный рёберный суррогат остаётся разложимым.
Их помещение в общий `M75(C)` не делает проекторы нецентральными, пока не
построен физический внедиагональный оператор размерности `54 x 21`.

Это повторяет проектные положительные прецеденты: единственный след в
`M18` и `M300` был содержательным только потому, что полная простая алгебра
и переходные операторы действительно входили в родительскую архитектуру.
Один матричный контейнер без коннектора такого вывода не даёт.

## Links

- [[version7-common-irreducible-trace-multiplicity-gate]]
- [[version7-incidence-transfer-markov-weight-gate]]
- [[vertex-edge-hodge-dirac-literature-2026]]
- [[multi-trace-measure-hypothesis-gate]]
- [[version7-minimal-curvature-support-trace-gate]]
- [[version7-minimal-support-trace-project-intuition-search]]

## Source Notes

- T. Krajewski, “Classification of Finite Spectral Triples”,
  arXiv:hep-th/9701081.
- T. Masson, G. Nieuviarts, “Lifting Bratteli Diagrams between Krajewski
  Diagrams: Spectral Triples, Spectral Actions, and AF Algebras”,
  arXiv:2207.04466.
- B. Ćaćić, “Moduli Spaces of Dirac Operators for Finite Spectral Triples”,
  arXiv:0902.2068.
- T. Kania, “A Short Proof of the Fact that the Matrix Trace is the
  Expectation of the Numerical Values”, arXiv:1402.4272.