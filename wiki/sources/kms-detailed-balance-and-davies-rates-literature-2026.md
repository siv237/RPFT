# KMS detailed balance и боровские скорости

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Квантовое detailed balance формулируется относительно заранее заданного
верного инвариантного состояния. В тепловых генераторах направленные
скачки раскладываются по боровским частотам, а KMS связывает прямую и
обратную скорости множителем `exp(-beta omega)`. Это условие не выводит
гамильтониан, температуру или общий масштаб скоростей.

## Key Points

- Опорное состояние detailed balance обязано быть инвариантным.
- Примитивная полугруппа имеет единственное верное инвариантное состояние,
  поэтому второй KMS-вес нельзя добавить к ней без изменения генератора.
- Самосопряжённый скачок, соединяющий разные энергии, раскладывается на две
  противоположные боровские моды.
- Соотношение `gamma(omega)=exp(-beta omega) gamma(-omega)` выбирает только
  отношение парных скоростей при уже заданных `beta` и `omega`.
- Оператор степени градуированной цепи может служить боровским
  классификатором, если все скачки являются его собственными операторами;
  физический статус такого оператора требует отдельной проверки.

## Links

- [[version8-kms-nontracial-relative-rate-selector-gate]] — применение к
  полному генератору Тома VIII.
- [[primitive-qms-and-detailed-balance-literature-2026]] — примитивность и
  следовая симметрия.
- [[intrinsic-time-and-repeated-interaction-literature-2026]] — отличие
  модульного времени от диссипативной скорости.
- [[version8-modular-bohr-parent-origin-gate]] — проектный кандидат на базе
  цепного оператора степени.

## Source Notes

- F. Fagnola, V. Umanità, “Generators of Detailed Balance Quantum Markov
  Semigroups”, arXiv:0707.2147.
- E. A. Carlen, J. Maas, “Gradient flow and entropy inequalities for
  quantum Markov semigroups with detailed balance”, arXiv:1609.01254.
- K. Temme et al., “The chi-square divergence and mixing times of quantum
  Markov processes”, arXiv:1005.2358.
- S. Chen et al., “Designing open quantum systems with known steady
  states”, arXiv:2404.14538.