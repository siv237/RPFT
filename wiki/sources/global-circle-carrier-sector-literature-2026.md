# Окружностный носитель и принуждение топологического сектора

> Status: working
> Type: source
> Updated: 2026-08-18

## Scope

Кластер первичной литературы для проверки, определяет ли полное пространство
главного `U(1)`-расслоения над `S2` его класс Черна и может ли моритова
структура сама выбрать ненулевую линию.

## Circle Bundles over `S2`

- M. Blau, G. Thompson, *Chern-Simons Theory on S1-Bundles*,
  `arXiv:hep-th/0601068`. Используется семейство `M(g,p)`; для базы `S2`
  полные пространства равны `M(0,p)=L(p,1)`, а `p=0` даёт произведение.
- P. Bouwknegt, J. Evslin, V. Mathai, *T-Duality: Topology Change from
  H-flux*, `arXiv:hep-th/0306062`. Явно фиксирует `S3` как окружностное
  расслоение над `S2` с классом Черна один и тривиальный дуальный носитель.
- V. Mathai, J. Rosenberg, *T-duality for torus bundles with H-fluxes via
  noncommutative topology*, `arXiv:hep-th/0409073`. Линзовое пространство
  `S3/Z_p` описано как окружностное расслоение над `S2` с `c1=p`.
- J. Evslin, *Trivializing a Family of Sasaki-Einstein Spaces*,
  `arXiv:0803.3241`. Явно отмечает `RP3` как окружностное расслоение над
  `S2` с классом Черна два.

Совместно эти источники подтверждают таблицу
`c1=0 -> S2 x S1`, `|c1|=1 -> S3`, `|c1|=2 -> RP3`.

## Picard and Morita Structure

- H. Bursztyn, *Semiclassical Geometry of Quantum Line Bundles and Morita
  Equivalence of Star Products*, `arXiv:math/0105001`. Линейные расслоения
  образуют действие группы Пикара, связанной с `H2(M,Z)`.
- H. Bursztyn, A. Weinstein, *Picard groups in Poisson geometry*,
  `arXiv:math/0304048`. Моритовы самоэквивалентности организованы в группу
  Пикара с тензорной композицией.

Для проекта важен отрицательный вывод: наличие тензорной композиции и
двойственности линии не выделяет генератор группы Пикара. Тривиальная линия
остаётся нейтральным допустимым элементом.

## Project Use

Литературные результаты применяются только к условию, где уже дано главное
окружностное расслоение над физической сферой дефекта. Они не доказывают
проектное отождествление семейной проекторной сферы с
`Spin(3)/Spin(2)`; этот мост должен быть построен отдельно.

## Links

- [[version5-global-carrier-forced-nontrivial-sector-gate]]
- [[version5-hopf-fell-line-transition-lift-gate]]
- [[version5-hopf-line-morita-orientation-functor-gate]]
- [[version5-projective-hedgehog-point-defect-gate]]