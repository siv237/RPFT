# Version VI: родительский вывод spin-cover носителя

> Status: mature
> Type: question
> Updated: 2026-08-19

## Summary

Топологическая двойка существует: `L direct_sum L*` имеет переход
`diag(z,z^-1)` в `SU(2)`, полный `c1=0` и локально реализует массу
`n dot sigma`. Но физическая Callias-конструкция требует, чтобы эта
двойка была независима от пространственного Clifford-фактора и чтобы её
две компоненты имели одинаковые внутренние квантовые числа.

## Results

- использование одной `C2` одновременно для пространственного spin и
  массы оставляет первый порядок в `[D,Phi]`;
- корректный минимум имеет вид `C2_spin tensor C2_twist`;
- существующая KO6-пара не является внутренним дублетом: два
  недиагональных генератора Паули нарушают градуировку и смешивают
  сопряжённые калибровочные заряды;
- слабый `SU(2)L` действует знаком `-1` только на 8 из 15 состояний;
- новая равнозарядная двойка `C2_twist tensor H15` работает, но меняет
  particle-размерность `15 -> 30`, Real-размерность `30 -> 60` и требует
  нового следа и аномального аудита;
- топологический класс `±15` сохраняется, но пятнадцать физических
  локализованных мод из текущего `H15/M35` не выведены.

## Final Test

Tensor-square, SWAP и exterior-power carriers проверены. Семейный квадрат
разлагается без повторений, статистическая пара не сохраняет полный
Pauli-фактор, а тензорные произведения `H15` не содержат равномерной копии
всех физических блоков. Канонической кратности два нет.

Ретроспективный аудит атласа сделал цель точнее. В контрольной
проекторной фазе `Delta^2=1/4=6/24`, а спектр состояния имеет rank-чтение
`(16,4,4)/24`. Поэтому двухкопийная конструкция должна не просто дать
абстрактную `C2`, а операторно вывести квадрат щели и повтор rank-four
электрослабого адреса, сохраняя gauge-коммутант.

Последующий аудит показал, что два rank-four слота совпадают как проектор:
их Gram-матрица имеет ранг один. Rank-six блоки `X/Xbar` сопряжены, а не
равнозарядны. Поэтому ретроспективная подсказка не стала carrier.

## Links

- [[version6-callias-toeplitz-index-comparison-gate]]
- [[spin-cover-callias-carrier-literature-2026]]
- [[version5-spinh-orientation-family-locking-reopening-gate]]
- [[version5-su2-family-lift-h15-representation-gate]]
- [[version5-hopf-line-morita-orientation-functor-gate]]
- [[version6-two-copy-affine-dilation-gate]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[version6-naive-atlas-order-parameter-rank-bridge-gate]]
- [[version6-two-copy-spin-cover-multiplicity-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spin_cover_carrier_parent_derivation_gate.tex`
- `s2t/audits/s2t_v6_spin_cover_carrier_parent_derivation_gate.py`
- `s2t/results/s2t_v6_spin_cover_carrier_parent_derivation_gate_results.json`