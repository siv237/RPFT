# Квадрат состояния, постселекция и virtual distillation

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная опора для нелинейной условной карты
`R -> R^2/Tr(R^2)` как осесвободного усилителя анизотропии.

## Primary Sources

- W. J. Huggins et al., *Virtual Distillation for Quantum Error
  Mitigation*, Physical Review X 11 (2021) 041036, DOI
  `10.1103/PhysRevX.11.041036`, `arXiv:2011.07064`.
- B. Koczor, *Exponential Error Suppression for Near-Term Quantum
  Devices*, Physical Review X 11 (2021) 031057, DOI
  `10.1103/PhysRevX.11.031057`.

Virtual distillation использует несколько копий состояния и
перестановочные измерения для получения наблюдаемых, соответствующих
`R^M/Tr(R^M)`. При росте `M` доминирующий собственный вектор подавляет
остальные компоненты экспоненциально.

Для двух копий точны формулы
`Tr[(O tensor I)SWAP(R tensor R)]=Tr(O R^2)` и
`Tr[SWAP(R tensor R)]=Tr(R^2)`. Они дают отношение наблюдаемых
виртуального состояния, но не означают его физического приготовления.

## Linearity Boundary

Карта `R -> R^2/Tr(R^2)` нелинейна по входной матрице и потому не может
быть одним фиксированным детерминированным CPTP-каналом на неизвестном
однокопийном состоянии. Физическая реализация требует нескольких копий,
постселекции, измерительного feedback или mean-field описания.

## Project Consequence

Квадратная карта:

- точна по `SO(3)` и не выбирает ось;
- усиливает traceless-флуктуацию вдвое;
- уменьшает энтропию и ведёт к ранг-один проектору;
- не стабилизирует полноранговую ordered-фазу;
- может получить линейную дилатацию только на расширенном двухкопийном
  carrier.

Проектный двухкопийный аудит подтвердил виртуальное чтение и закрыл
детерминированную реализацию: на одноосном семействе выход любого
фиксированного линейного канала квадратичен по параметру, тогда как
нормированный квадрат рационален. Остаются только явно условные или
эффективные реализации.

## Links

- [[version6-nonlinear-affine-feedback-instability-gate]]
- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[version6-two-copy-affine-dilation-gate]]
- [[version6-matter-birth-program]]