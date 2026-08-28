# Version VII: спектральный родитель стрелочной когерентности

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Ручная сумма радиального и внешнеквадратного членов заменена одним полным
спектральным полиномом трёхузлового нечётного оператора.

## Exact Result

Для цепи комплексных размерностей `1 -> 6 -> 3` с

$$
A_B(1)=\operatorname{vec}B,\qquad
C_B=\frac12d(\Lambda^2)_B
$$

выполняются

$$
\operatorname{Tr}D_B^2=3T,\qquad
\operatorname{Tr}D_B^4=\frac94T^2+\frac{15}{4}d,
$$

где `T=Tr(BB*)` и `d=det(BB*)`. Поэтому

$$
\frac49\left(\operatorname{Tr}D_B^4-\mu\operatorname{Tr}D_B^2+\mu^2\right)
=\left(T-\frac{2\mu}{3}\right)^2+\frac53d.
$$

Относительный коэффициент `5/3` теперь выведен из одного носителя. При
`mu=9/2` нули имеют `T=3` и `rank B=1`.

## Hessian

- нулевой сектор: двенадцать собственных значений `-12`;
- ненулевой вакуум: семь нулей, четыре значения `10` и одно `24`;
- Real-срез: `6 negative` в нуле и `3 zero + 3 positive` в вакууме.

## Boundary

Получен положительный градуированный спектральный родитель, но пока не
строгая конечная спектральная тройка физической алгебры. Открыта
бимодульная типизация узлов `1,6,3`, первого порядка, Real-образов и
совместимости с классом `15`. Параметр `mu` остаётся общим масштабом.

## Verdict

Родительский разрыв предыдущего гейта закрыт на уровне одного полного
спектрального полинома. Физический algebraic admission остаётся открытым.

## Subsequent Result

[[version7-edge-coherence-bimodule-admission-gate]] закрыл вложение в
неизменённый фермионный носитель. Единственный одномерный тип `(C,C)` не
имеет общей координаты с шестимерными типами `(H,M3)` и `(M3,H)`, поэтому
первое ребро нарушает строгий первый порядок. Спектральный родитель
сохраняется как комплекс пространства полей.

[[version7-edge-coherence-field-space-superconnection-gate]] затем
реализовал этот комплекс как ассоциированный полевой суперсвязностный
носитель с положительной кинетической метрикой, без новых фермионов и
независимых калибровочных связностей.

## Links

- [[version7-edge-coherence-rank-one-condensate-gate]]
- [[version7-edge-coherence-formula-intuition-map]]
- [[version7-edge-coherence-bimodule-admission-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version7-rank-change-parent-program]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex`
- `s2t/audits/s2t_v7_edge_coherence_spectral_parent_gate.py`
- `s2t/results/s2t_v7_edge_coherence_spectral_parent_gate_results.json`