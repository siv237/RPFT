# Классификация Real/KR-класса цикла Тёплица

> Status: working
> Type: question
> Updated: 2026-08-17

## Summary

Проектная вещественная структура не является поточечным сопряжением одной
ветви. Она меняет две хопфовы ориентации местами. Поэтому её неподвижная
алгебра изоморфна `M105(C)`, рассматриваемой как вещественная алгебра, и
соответствующая группа равна `KO6 = Z`, а не нулю.

## Key Points

- Поточечное сопряжение даёт `M105(R)` и `KO6=0`, но не реализует обмен
  `L <-> L*`, `E <-> E*` и `T+ <-> T-`.
- Правильная инволюция пары имеет вид
  `rho(a,b)=(conjugate(b),conjugate(a))`.
- Её неподвижная вещественная алгебра
  `{(a,conjugate(a))}` изоморфна `M105(C)_R`.
- По инвариантности Мориты `KO6(M105(C)_R)=Z`.
- Поэтому равенство полного комплексного индекса нулю не доказывает
  тривиальность вещественного класса.
- Естественный кандидат имеет абсолютную величину 15 и следовой вес
  `15/105=30/210=1/7`.
- Число 15 ещё не доказано как вещественный индекс: требуется явный
  `Cl(0,6)`-линейный фредгольмов цикл и проверка отображения в пару
  комплексных классов `-15/+15`.

## Verdict

Ветка не закрылась сокращением комплексных индексов. После правильного
выбора вещественной формы остаётся целочисленная `KO6`-группа и кандидат
класса величины 15. Ретроспективный аудит затем показал, что конечный
KO6-каркас уже построен раньше; следующий строгий тест сужен до
вещественно-комплексного Bott-отображения. Физическое замыкание пока не
заявляется.

## Links

- [[version5-real-toeplitz-ko6-parent-lift-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[one-seventh-boundary-transgression-literature-2026]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[version5-real-toeplitz-cross-tome-reuse-audit-gate]]
- [[version5-real-toeplitz-bott-comparison-map-gate]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_kr_classification_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_kr_classification_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_kr_classification_gate_results.json`
- Boersema--Schochet, `arXiv:2407.05880v4`.
- Schick, `arXiv:math/0311295`.
- Boersema--Loring, `arXiv:1504.03284`.