# Вещественный KO6-подъём цикла Тёплица

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Две ориентированные ветви Тёплица допускают один сбалансированный
вещественный фредгольмов цикл. Условия проекта
`J^2=1`, `JF=FJ`, `J gamma=-gamma J` заставляют `J` взаимно переводить
`ker T` и `ker T*`. Поэтому обычный индекс полного KO6-пакета всегда
равен нулю.

## Key Points

- Ориентированные комплексные половины имеют индексы `-15` и `+15`.
- Полный оператор имеет `dim ker T=dim ker T*=15` и индекс ноль.
- Компенсация следует из знаков KO6, а не из случайного выбора оператора.
- Суммарный компактный дефект имеет ранг 30 на удвоенном коэффициентном
  носителе 210, поэтому вес `30/210=1/7` сохраняется.
- Одна ориентированная половина не является `J`-инвариантной.
- Нулевой обычный индекс ещё не решает вопрос о возможном Real/KR-классе.
- Последующий гейт установил, что проектный `J` выбирает обменную, а не
  поточечную вещественную форму: её `KO6`-группа равна `Z`.

## Verdict

Сбалансированный KO6-подъём построен, но ненулевой целочисленный индекс
полного пакета структурно невозможен. Точная вещественная форма теперь
определена в [[version5-real-toeplitz-kr-classification-gate]]: кандидат
целочисленного класса сохраняется, но требует явного `Cl(0,6)`-индекса.

## Links

- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[version5-one-seventh-boundary-transgression-literature-gate]]
- [[one-seventh-boundary-transgression-literature-2026]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[version5-real-toeplitz-kr-classification-gate]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_ko6_parent_lift_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_ko6_parent_lift_gate_results.json`