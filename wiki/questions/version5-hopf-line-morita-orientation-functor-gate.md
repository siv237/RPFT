# Ориентационный функтор Мориты для хопфовой линии

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Связывающая алгебра сама различает направления `E` и `E*` посредством
градуировки `Gamma_link=p20-p15`. Это даёт функториальное назначение
`E -> E tensor L`, `E* -> E* tensor L*` и выбирает классы Черна `+1/-1`
без ручного знака.

## Key Points

- `[Gamma_link,X]=2 deg(X) X`.
- `deg(E)=+1`, `deg(E*)=-1`, диагональные углы имеют степень ноль.
- Степень аддитивна на всех ненулевых композициях и меняет знак при `*`.
- Назначение `T(X)=X tensor L^deg(X)` является мультипликативным.
- В произведениях `E E*` и `E* E` линии `L` и `L*` сокращаются.
- Углы рангов 20 и 15 нельзя переставить внутренним унитарным
  сопряжением.
- Две ветви подъёма `n/-n` получают `c1=+1/-1`.
- KO6 обменивает `E tensor L` и `E* tensor L*`.
- Ранг конечного внутреннего модуля и нормированный след `M35` не
  меняются.
- Неединственность прежней трёхуровневой высоты не опровергается:
  ориентация теперь выводится между двумя углами.

## Verdict

Топологический ориентационный мост пройден. Следующий гейт должен вывести
единый пространственный суперсвязностный функционал, где одна хопфова
кривизна одновременно обеспечивает конечную энергию ежа и индекс один.

## Links

- [[version5-hopf-twisted-defect-superconnection-energy-index-gate]] —
  совместный тест конечной энергии и индекса.
- [[version5-hopf-fell-line-transition-lift-gate]] — хопфова линия и
  условное переоткрытие.
- [[version5-morita-linking-parent-gate]] — связывающая алгебра `M35`.
- [[version5-affine-ko6-reference-corner-gate]] — KO6 и обращение
  ориентированного дифференциала.
- [[version5-oriented-height-hodge-ko6-gate]] — прежняя неединственность
  трёхуровневой высоты.
- [[version5-projective-hedgehog-point-defect-gate]] — энергия ежа и
  единичная хопфова линия.

## Source Notes

- `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex`
- `s2t/audits/s2t_v5_hopf_line_morita_orientation_functor_gate.py`
- `s2t/results/s2t_v5_hopf_line_morita_orientation_functor_gate_results.json`
- R. Meyer, *Equivariant Kasparov Theory and Generalized Homomorphisms*,
  arXiv:math/0001094.
- V. Deaconu, *Groupoid Actions on C*-Correspondences*,
  arXiv:math/0612746.