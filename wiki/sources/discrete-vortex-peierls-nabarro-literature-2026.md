# Литература по решёточному закреплению дефектов

> Status: working
> Type: source
> Updated: 2026-08-20

## Первичные источники

- `arXiv:1601.04598`, *Discrete Solitary Waves in Systems with Nonlocal
  Interactions and the Peierls-Nabarro Barrier* — узловые и межузловые
  стационарные ветви возникают из-за нарушения непрерывной
  трансляционной симметрии дискретизацией.
- `arXiv:nlin/0603047`, *Discrete Nonlinear Schrodinger Equations Free of
  the Peierls-Nabarro Potential* — специальные дискретизации могут
  восстанавливать непрерывную орбиту переносов и дополнительные нулевые
  моды.
- `arXiv:0902.1201`, *Lattice vortices induced by noncommutativity* —
  вихревые структуры могут испытывать эффективный решёточный потенциал
  Пайерлса--Набарро.

## Значение для проекта

Гессиан следует вычислять только после дискретной стационаризации фона.
Иначе направление, перемещающее sampled-профиль между узловым и
межузловым положениями, может выглядеть как физическая отрицательная
мода. Закрепление центра допустимо как удаление переносной степени
свободы, но окончательный сертификат требует трансляционно ковариантной
дискретизации и проверки восстановления нулевой пары.

## Связи

- [[version6-bosonic-defect-corrected-vortex-negative-mode-nonlinear-saturation-gate]]
- [[version6-bosonic-defect-corrected-vortex-covariant-zero-mode-resolution-gate]]
- [[so3-z3-vortex-profile-and-stability-literature-2026]]