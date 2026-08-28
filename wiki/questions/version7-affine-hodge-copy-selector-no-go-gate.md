# Version VII: запрет аффинно-Hodge-селектора копий

> Status: mature
> Type: question
> Updated: 2026-08-27

## Summary

Существующий аффинно-Hodge-родитель выбирает размерность лёгкого ядра, но
не способен выбрать его ориентацию между старой и новой копиями.

## Exact Result

Для `M : C6 -> C3` преобразование `M -> M(U tensor I3)` сохраняет
`MM*`, сингулярные числа и Hodge-действие, но сопрягает проектор ядра.
На явной полуокружности `U(2)` действие неизменно с остатком ниже `1e-24`,
тогда как проектор ядра перемещается на фробениусово расстояние `sqrt(6)`,
а его перекрытие со старой копией меняется от `0` до `3`.

Аффинный проектор имеет вид `P3 tensor I2` и точно коммутирует со всеми
копийными вращениями. Коммутант представленной алгебры содержит полный
`M2(C)` на совпадающих старых и новых бимодулях.

## Verdict

Старый родитель закрыт как селектор копий. Он сохраняется как канонический
селектор ранга и числа лёгких направлений. Следующий кандидат обязан вывести
второй нецентральный оператор из алгебры путей, Morita-угла или другого
независимого носителя; ручная `Z2`-градуировка запрещена.

## Links

- [[version7-four-vertex-vectorlike-selector-gate]]
- [[version7-vectorlike-kernel-selector-intuition-map]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_affine_hodge_copy_selector_no_go_gate.tex`
- `s2t/audits/s2t_v7_affine_hodge_copy_selector_no_go_gate.py`
- `s2t/results/s2t_v7_affine_hodge_copy_selector_no_go_gate_results.json`