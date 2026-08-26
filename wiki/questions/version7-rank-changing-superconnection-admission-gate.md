# Version VII: допуск рангоизменяющей суперсвязности

> Status: stale
> Type: question
> Updated: 2026-08-26

## Summary

Том VII открыт не новым названием, а новым родительским кандидатом. Основное
поле `Phi(x)` является физической бимодульной одноформой переменного ранга на
общем аффинном, хиральном, пространственном и Real-носителе. Проекторное
состояние `R_Phi` и поле порядка `Q_Phi` должны быть производными от `Phi`, а
не входами действия.

Ретроспективная поправка: исходное произведение
`E_aff tensor Y_phys` содержало фиксированный семейный tangent `E_rho` и
позднее закрыто как двойной семейный счёт. Действующая коррекция находится в
[[version7-affine-physical-module-canonical-lift-gate]].

## Parent Candidate

Общий носитель:

`E_aff = Hom(C4, im P3)`, `P3 = I4 - J4/4`, `rank P3 = 3`.

Фундаментальное поле:

`Phi in Gamma(X, E_aff tensor Y_phys)`,

где `Y_phys = Omega^1_DF(A_F)` — физический модуль конечных одноформ.
Real-завершение равно `Phi + epsilon' J Phi J^-1`.

Единственный родительский функционал — нормированный квадрат кривизны одной
суперсвязности. Независимые секторные коэффициенты запрещены.

## Admission Result

- `P0`: предварительно пройден — четыре сектора типизированы одним полем;
- `P1`: предварительно пройден — задано одно действие и один след;
- `P2`: сформулирован — физический гессиан вычисляется из линейной вариации
  кривизны и её квадратичного члена;
- `P6`: гейт, аудит, результат и стоп-критерий созданы одновременно.

## Negative Control

В минимальном плоском фоне поле представлено оператором

`B(X) = block(0,X*;X,0)`, `X in M_(3x4)(C)`.

Аудит проверяет:

- `dim_C E_aff = 12`, `dim_R E_aff = 24`;
- ранги нечётного оператора равны `0,2,4,6` на стратах ранга `0,1,2,3`;
- `S4`-ковариантность, самосопряжённость и Real-условие;
- полный плоский гессиан равен `(8/7) I_24`.

Следовательно, переменный ранг сам по себе не запускает переход. Возможная
отрицательная мода должна происходить только из нецентральной кривизны полного
физического `D_F`, пространственной связи или их канонического смешанного
члена.

## Stop Criterion

Кандидат закрывается до обсуждения частиц, если полный физический модуль
интертвинеров пуст или факторизован, единый след требует независимых весов
либо полный физический гессиан нулевого сектора неотрицателен.

## Later Result

[[version7-full-physical-rank-field-hessian-gate]] выполнил решающий тест и
закрыл этот чистый кривизностный родитель. При ненулевом `D_F` точка
`Phi=0` нестационарна; при нулевом `D_F` отрицательной моды нет.

## Links

- [[version7-rank-change-parent-program]]
- [[version7-full-physical-rank-field-hessian-gate]]
- [[version7-affine-physical-module-canonical-lift-gate]]
- [[version6-final-conclusion-and-next-program]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]
- [[version6-exchange-bridge-parent-admissibility-gate]]
- [[version6-spectral-transition-post-radiative-bridge-final-dynamic-status-gate]]

## Source Notes

- `s2t/gates/version7_rank_changing_superconnection_admission_gate.tex`
- `s2t/audits/s2t_v7_rank_changing_superconnection_admission_gate.py`
- `s2t/results/s2t_v7_rank_changing_superconnection_admission_gate_results.json`