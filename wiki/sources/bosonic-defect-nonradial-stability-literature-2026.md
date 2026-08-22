# Нерадиальная устойчивость тензорных ежей

> Status: working
> Type: source
> Updated: 2026-08-20

## Summary

Первичная литература показывает, почему существование радиального профиля
не завершает проверку дефекта. В пятикомпонентной теории параметра порядка
двухосные и угловые возмущения способны менять знак второй вариации, а
отрицательная нерадиальная мода может описывать распад симметричного ежа.

## Sources

- Radu Ignat, Luc Nguyen, Valeriy Slastikov, Arghir Zarnescu,
  *Stability of the melting hedgehog in the Landau-de Gennes theory of
  nematic liquid crystals*, `arXiv:1404.1729` — устойчивость относительно
  произвольных `Q`-тензорных возмущений вблизи критической температуры и
  потеря устойчивости в глубокой нематической фазе.
- Xavier Lamy, *Some properties of the nematic radial hedgehog in
  Landau-de Gennes' theory*, `arXiv:1212.1072` — монотонность и
  единственность радиального минимизатора при заданных граничных условиях;
  это радиальный результат, не заменяющий полный гессиан.
- Thomas Waindzoch, Jochen Wambach, *Stability of the B=2 hedgehog in the
  Skyrme model*, `arXiv:hep-ph/9509421` — решёточное вычисление
  нерадиальных отрицательных мод и последующего распада симметричного ежа
  на два солитона.

## Project Use

Для Тома VI литература задаёт три обязательных уровня: канонический
локальный потенциал, полный пятикомпонентный гессиан и отдельный анализ
каналов конечной несферической деформации. Выполненный расчёт закрывает
только конечномерный вариант второго уровня.

## Links

- [[version6-bosonic-defect-nonradial-stability-gate]]
- [[bosonic-defect-radial-stability-literature-2026]]
- [[projective-order-parameter-fields-and-defects-literature-2026]]
- [[spatial-projective-defect-energy-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_nonradial_stability_gate.tex`
- `s2t/results/s2t_v6_bosonic_defect_nonradial_stability_gate_results.json`