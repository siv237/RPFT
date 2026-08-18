# Хопфова линия на ориентированных переходах

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Повторное чтение раннего «Хабр 2» открыло маршрут, отличный от
запрещённого `SU(2)_F`. Плоская фаза порядка четыре сама имеет `c1=0`, но
полное расслоение Хопфа на существующем накрытии `S3 -> RP3` даёт линию
с `c1=1`. Её можно условно связать с направленными стрелками Мориты
`E/E*` как пару `L/L*` без нового фиксированного семейного дублета.

## Key Points

- Последовательность `1,i,-1,-i` является характером `C4`, а не
  нетривиальным проективным множителем.
- Плоская `Z4`-линия не может дать единичный индекс.
- Хопфов спинор `z` задаёт `n=z^* sigma z` и
  `P_+=z z^*=(I+n.sigma)/2`.
- Связность `A=-i z^* dz` имеет
  `F=(1/2) sin(theta) dtheta wedge dphi` и `c1=1`.
- Четверть волоконного оборота `z -> i z` сохраняет `n` и `P_+`, но
  после двух шагов даёт знак минус.
- `S3` как хопфово расслоение имеет `c1=1`; quotient `RP3=L(2,1)` имеет
  `c1=2`. Это совпадает с различием спинорного и векторного чтений.
- На стрелках можно использовать линию Фелла
  `F(y<-x)=L_y tensor L_x^*` с канонической композицией.
- Кандидат KO6 имеет вид `E tensor L` и `E* tensor L*`.
- Новый `SU(2)_F` и новый фиксированный `C2_family` не требуются.
- Не выведено главное: почему направление `E/E*` обязано выбирать
  `n/-n`, а не произвольную ориентацию.

## Verdict

Ветка условно переоткрыта одним узким тестом. Следует вывести
ориентационный функтор из существующей градуировки, высоты или полярной
декомпозиции суперсвязности. Если ориентация остаётся ручным выбором,
хопфов маршрут закрывается.

Последующий тест прошёл: ориентацию задаёт двухугловая градуировка
`p20-p15`. См. [[version5-hopf-line-morita-orientation-functor-gate]].

## Links

- [[early-light-mobius-resonator-hypothesis]] — ранний источник хопфовой
  интуиции.
- [[version5-transition-primitive-scientific-language-gate]] — группоид
  переходов и композиция стрелок.
- [[version5-order-four-resonant-loop-transport-gate]] — плоская фаза
  порядка четыре.
- [[version5-projective-hedgehog-point-defect-gate]] — единичный класс
  Черна спинорной линии.
- [[version5-su2-family-lift-h15-representation-gate]] — отличие от
  запрещённого внутреннего `SU(2)_F`.
- [[version5-spinh-orientation-family-locking-reopening-gate]] — отличие
  от запрещённой двойной роли одной `C2`.
- [[version5-hopf-line-morita-orientation-functor-gate]] — вывод
  назначения `E/E* -> L/L*`.

## Source Notes

- `архив-2025-2026/2025-12-истоки/habr/print2.md`
- `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex`
- `s2t/audits/s2t_v5_hopf_fell_line_transition_lift_gate.py`
- `s2t/results/s2t_v5_hopf_fell_line_transition_lift_gate_results.json`
- D. Freed, M. Hopkins, C. Teleman, *Loop Groups and Twisted K-Theory I*,
  arXiv:0711.1906.
- J.-L. Tu, P. Xu, C. Laurent-Gengoux, *Twisted K-Theory of
  Differentiable Stacks*, arXiv:math/0306138.
- A. Stoffel, *Supersymmetric Field Theories from Twisted Vector
  Bundles*, arXiv:1801.03016.