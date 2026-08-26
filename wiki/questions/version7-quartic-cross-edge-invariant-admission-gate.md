# Version VII: допуск квартичного межрёберного инварианта

> Status: mature
> Type: question
> Updated: 2026-08-26

## Summary

Повышение степени обычного спектрального полинома не создаёт смешивание.
Из ортогональности кромок следует, что все положительные моменты текущего
физического оператора распадаются на независимые вклады `u,d,e`.

## Exact Result

Для любого `n >= 1`:

`Tr(D*D)^n = sum_a Tr(D_a*D_a)^n`,

`Tr(DD*)^n = sum_a Tr(D_aD_a*)^n`.

На коизометрическом вакууме квартичный след равен `42` при любых
`U_u,U_d,U_e`.

## Typing Boundary

Family-only матрица `W_ab=X_a X_b*=U_a U_b*` видит относительный кадр, но
её сокращение требует внедиагональной матричной единицы между метками
рёбер. Физический бимодульный коммутант равен `C^3`, поэтому такая единица
отсутствует.

## Krajewski Precedent

Старый четырёхрёберный rectangle действительно порождал смешанное слово из
одного `Tr D^4`, но использовал новый общий коннектор и 24-мерный оператор.
Он не является подграфом текущего `H15` и не может быть перенесён без нового
представительного гейта.

## Verdict

Коэффициент-свободный квартичный межрёберный инвариант на неизменённом
носителе не допущен. Следующий шаг — вывести минимальный gauge/Real-
совместимый коннектор, замыкающий физический Krajewski-цикл.

## Links

- [[version7-minimal-h15-mixed-connector-admission-gate]]
- [[version7-common-higgs-degree-two-cross-edge-gate]]
- [[version7-corrected-vacuum-relative-edge-hessian-gate]]
- [[version4-common-updown-krajewski-loop-gate]]
- [[version5-h15-spectral-torsion-selector-gate]]
- [[version7-relative-edge-formula-intuition-map]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_quartic_cross_edge_invariant_admission_gate.tex`
- `s2t/audits/s2t_v7_quartic_cross_edge_invariant_admission_gate.py`
- `s2t/results/s2t_v7_quartic_cross_edge_invariant_admission_gate_results.json`