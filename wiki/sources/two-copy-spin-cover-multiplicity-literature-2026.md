# Двухкопийные коммутанты и spin-cover кратность

> Status: working
> Type: source
> Updated: 2026-08-19

## Вопрос

Может ли сама операция тензорного квадрата создать внутренний
`SU(2)`-дублет, или Pauli-алгебра появляется только на настоящем
пространстве кратности эквивалентных представлений?

## Первичные источники

### Flores--Peltola

Steven M. Flores, Eveliina Peltola, *Higher-spin quantum and classical
Schur--Weyl duality for sl2*, `arXiv:2008.06038`.

Работа строит double-commutant описание tensor-product представлений и
явные пространства кратности. Для проекта существенен принцип: размер
неприводимого слагаемого и размер его multiplicity space — разные вещи;
матричная алгебра, коммутирующая с группой, действует на втором.

### Albanese--Milivojević

Michael Albanese, Aleksandar Milivojević, *Spin-h and Further
Generalisations of Spin*, J. Geom. Phys. 164 (2021) 104174,
`arXiv:2008.04934`.

`Spin^h=(Spin x Sp(1))/Z2` предоставляет независимый кватернионный
внутренний фактор. Это возможный язык переоткрытия, но он является новой
структурой, если `Sp(1)` не выведен существующим конечным родителем.

### Anghel

Nicolae Anghel, *L2-Index Formulae for Perturbed Dirac Operators*,
Commun. Math. Phys. 128 (1990), 77--97.

Callias-потенциал является входным эндоморфизмом Clifford-модуля. Индексная
теорема классифицирует уже определённый оператор и не создаёт отсутствующее
пространство представительной кратности.

### Baez--Huerta

John C. Baez, John Huerta, *The Algebra of Grand Unified Theories*, Bull.
Amer. Math. Soc. 47 (2010), 483--552, `arXiv:0904.1556`.

Источник фиксирует представительный смысл упаковок одного поколения и
различие между совпадением размерностей и эквивалентностью представлений.

## Вывод для проекта

Литература согласуется с машинным no-go: `3 tensor 3=1+3+5` без
повторений не имеет скрытого `M2`; одинаковые ранги `X/Xbar` также не
являются эквивалентными gauge-копиями. Нужный Pauli-фактор должен быть
отдельно выведенным multiplicity space.

## Links

- [[version6-two-copy-spin-cover-multiplicity-gate]]
- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[spin-cover-callias-carrier-literature-2026]]