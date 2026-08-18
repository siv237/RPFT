# Bott-сравнение обменного класса Тёплица

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Для комплексных чисел, рассматриваемых как вещественная алгебра,
стандартная таблица объединённой K-теории даёт

`c6 : Z -> Z^2, n -> (-n,n)`.

Поэтому пара индексов Тёплица `(-15,+15)` имеет единственный вещественный
прообраз 15.

## Checks

- `C_R tensor_R C = C direct_sum C`.
- `c6(1)=(-1,+1)` — требуемый антидиагональный образ.
- `r6(a,b)=-a+b`, поэтому `r6(c6(1))=2`.
- Сопряжение `psi6(a,b)=(-b,-a)` фиксирует образ `c6`.
- `c6(15)=(-15,+15)` точно совпадает с построенной ориентированной парой.
- Инъективность `c6` доказывает уникальность вещественного класса 15.
- Нормированный вес равен `15/105=1/7`.

## Verdict

Целочисленный класс 15 теперь доказан на уровне вещественной K-теории.
Явные матрицы `Cl(0,6)` могут дать конкретного представителя, но больше не
являются логическим пробелом классификации. Открыты неограниченный
родительский оператор и физическая динамика. Последующий гейт уже вывел
поляризацию Харди из оператора числа, но обнаружил отдельный разрыв
степени: extension имеет степень 1 и требует входного Real-символа
степени 5.

## Links

- [[version5-real-toeplitz-cross-tome-reuse-audit-gate]]
- [[version5-real-toeplitz-kr-classification-gate]]
- [[version5-real-toeplitz-ko6-parent-lift-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[one-seventh-boundary-transgression-literature-2026]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_bott_comparison_map_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_bott_comparison_map_gate_results.json`
- Boersema--Schochet, `arXiv:2407.05880v4`, Example 10.2.
- Schick, `arXiv:math/0311295`, Definitions 3.7–3.8 and Lemma 3.9.