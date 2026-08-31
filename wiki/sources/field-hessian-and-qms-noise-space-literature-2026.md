# Полевой гессиан и шумовое пространство QMS

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Литература поддерживает различение двух объектов: гессиан действия задан на
касательном пространстве полей, тогда как ковариантный QMS задаётся
операторами на алгебре наблюдаемых и их шумовым представлением. Их нельзя
отождествлять только по равенству размерностей.

## Key Points

- У ковариантной квантово-марковской полугруппы ковариантность относится к
  полностью положительной части и операторным коэффициентам генератора.
- Gaussian QMS требует отдельно drift и diffusion/noise data; одна
  квадратичная равновесная форма не является всем генератором процесса.
- Для проекта это означает необходимость явного отображения из общего
  пространства superconnection-полей в noise-module до сравнения гессианов.

## Project Use

Использовано в
[[version8-gauge-closed-noise-parent-hessian-gate]] для проверки типизации,
а не как доказательство численных результатов проекта.

## Sources

- A. S. Holevo, *Covariant Quantum Dynamical Semigroups: Unbounded
  Generators*, arXiv:quant-ph/9701037.
- F. Girotti, D. Poletti, *Gaussian quantum Markov semigroups on finitely
  many modes admitting a normal invariant state*, arXiv:2412.10020.

## Links

- [[covariant-noise-modules-and-stabilizers-literature-2026]]
- [[parent-action-equilibrium-and-mobility-literature-2026]]

## Source Notes

- Поиск и сверка литературы выполнены 2026-08-29.