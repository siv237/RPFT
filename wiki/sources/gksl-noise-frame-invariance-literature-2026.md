# Инвариантность шумового кадра в форме GKSL

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Форма GKSL определяет генератор через положительную квадратичную форму на
пространстве операторов шума. Конкретный список операторов скачка не
единственен: унитарная замена ортонормированного кадра сохраняет генератор,
а нулевые или линейно зависимые компоненты должны быть удалены.

## Key Points

- Теоремы Gorini–Kossakowski–Sudarshan и Lindblad задают общую форму
  генераторов норм-непрерывных вполне положительных полугрупп.
- Физическим объектом является положительная Kossakowski-форма, а не
  отдельное координатное представление скачков.
- Ортонормированный кадр фиксирован лишь с точностью до унитарной замены;
  сумма диссипаторов по полному кадру инвариантна.
- Проектный common-trace Casimir является конечномерной реализацией этого
  принципа на уже выбранном шумовом подмодуле.

## Links

- [[version8-canonical-noise-frame-common-trace-gate]] — применение к
  19-мерному noise quotient Тома VIII.
- [[quantum-gradient-flow-and-noise-metric-literature-2026]] — формы Дирихле
  и KMS-метрика.
- [[version8-minimal-covariant-stinespring-carrier-gate]] — минимальный
  Stinespring-носитель cross-канала.

## Source Notes

- V. Gorini, A. Kossakowski, E. C. G. Sudarshan, “Completely positive
  dynamical semigroups of N-level systems”, J. Math. Phys. 17 (1976)
  821–825.
- G. Lindblad, “On the generators of quantum dynamical semigroups”, Commun.
  Math. Phys. 48 (1976) 119–130.