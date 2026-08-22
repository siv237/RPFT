# Version VI: существующие кратности как резонансный сток

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Проверены кратности `15`, `18`, `20`, `35`, KO6 и Real-пара. Единственный
настоящий резонансный кандидат найден не в больших числах, а в раннем
аффинном разложении `C4 = 1 + 3`.

## Positive Finding

Проектор `P3=I-P1` имеет ранг три, высота первого узла равна `-P3`, а
коизометрия `V` удовлетворяет

`V V* = I3`, `V* V = P3`.

Следовательно, проект уже содержит три ортогональные моды одной высоты,
канонически связанные с семейным триплетом. Нужная резонансная кратность
два имеется с запасом.

## Boundary

Аффинный триплет является соседним углом прямой суммы, а не независимым
тензорным bath. Условный ordered-спектр можно получить, если поперечные
компоненты уходят в этот угол с вероятностью `0.9518545...`; в семейном
углу остаётся `0.3654303...` полной вероятности.

Каноническая связь `X=rho V` действует одинаково на все три семейных
направления. После любого равного переноса условное состояние остаётся
`I3/3`. Для кристаллизации нужна state-selective нелинейная связь, но
вставлять готовый проектор `P` запрещено как круг.

## Negative Ledger

- `H15`: пять различных gauge-иррепов с кратностью один;
- KO6: противоположные градуировки, не свободный дублет;
- ранг шесть `M18`: family + Real, не multiplicity factor;
- `M20/M35`: размеры алгебр, не энергетические вырождения;
- Real exterior pair: повторное использование закрывает нормировку
  двойным счётом.

## Next Test

Гейт [[version6-nonlinear-affine-feedback-instability-gate]] построил
осесвободный усилитель `R^2/Tr(R^2)` и доказал неустойчивость изотропии.
Теперь требуется его двухкопийная линейная дилатация и механизм насыщения
до конечного полнорангового спектра.

## Links

- [[version6-clock-controlled-energy-conserving-quench-gate]]
- [[symmetry-multiplicity-noiseless-subsystems-literature-2026]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[version6-matter-birth-program]]
- [[version6-nonlinear-affine-feedback-instability-gate]]

## Source Notes

- `s2t/gates/version6_existing_multiplicity_resonant_sink_gate.tex`
- `s2t/audits/s2t_v6_existing_multiplicity_resonant_sink_gate.py`
- `s2t/results/s2t_v6_existing_multiplicity_resonant_sink_gate_results.json`