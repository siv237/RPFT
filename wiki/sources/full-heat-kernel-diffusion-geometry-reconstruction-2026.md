# Полное тепловое ядро, диффузия и реконструкция геометрии

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Литература поддерживает принципиальное различие между одним спектром
оператора и полной диффузионной полугруппой. При дополнительных условиях
полное тепловое ядро или диффузионное исчисление несёт локальную
геометрическую информацию, утраченную после перехода к тепловому следу.

## Key Points

- Varadhan-type асимптотика связывает малое время полного теплового ядра с
  геодезическим расстоянием; след ядра такой двухточечной информации не
  содержит.
- Результаты об embeddings через тепловое ядро показывают, что конечные
  наборы его координат могут кодировать и приближать риманову геометрию.
- Современная диффузионная реконструкция требует не только спектральных
  чисел, но симметричную сильно локальную полугруппу и её исчисление первого
  и второго порядка.
- Поэтому проектный finite-гейт является лишь доказательством существования
  пропущенного промежуточного класса. Он ещё не доказывает сильную
  локальность или римановость физического S2T-ядра.

## Links

- [[version8-full-correlation-kernel-locality-reconstruction-gate]] —
  конечный точный тест различия полного ядра и его спектра.
- [[version5-reduction-triangle-cocycle-gate]] — граница spectrum-only.
- [[spectral-correlational-source]] — проектное происхождение гипотезы.

## Source Notes

- A. Sangha, *Recovering Riemannian Geometry from Diffusion*,
  arXiv:2601.17166.
- J. Portegies, *Embeddings of Riemannian manifolds with heat kernels and
  eigenfunctions*, arXiv:1311.7568.
- C. Fefferman et al., *The Reconstruction Problem for Riemannian
  Manifolds from Dirichlet-to-Neumann and Heat Kernel Data*,
  arXiv:2111.14528.