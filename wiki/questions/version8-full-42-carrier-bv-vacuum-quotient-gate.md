# BV-вакуумный quotient полного 42-мерного носителя

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Фермионная часть закрыта точно: полная хиральная проекция на
`C^4 tensor C^21` имеет ранг `42` и переводит `Tr D_F^4=46` в физический
четвёртый момент `92`, поэтому determinant-вклад равен `-92`.

BV-проверка прежнего скалярного гессиана дала no-go. Нарушенная
калибровочная орбита имеет ранг `3`, но ограничение гессиана на неё также
имеет ранг `3` и след `34`, а не нуль. Значит, прежний блок был
фиксированно-фоновым грамовым гессианом, не физическим
калибровочно-инвариантным вакуумным гессианом. Формальное число
`4360268/3249` нельзя называть полным коэффициентом `B`.

## Следующий вопрос

Реконструировать вакуумный функционал с совместно движущимся фоном либо
сразу его гессиан на калибровочном quotient и повторить босонный ledger.

## Связи

- [[version8-full-42-carrier-base-k-determinant-compatibility-gate]]
- [[version3-fluctuated-product-bv-complex-gate]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Исходники

- `s2t/gates/version8_full_42_carrier_bv_vacuum_quotient_gate.tex`
- `s2t/audits/s2t_v8_full_42_carrier_bv_vacuum_quotient_gate.py`
- `s2t/results/s2t_v8_full_42_carrier_bv_vacuum_quotient_gate_results.json`
- `s2t/proofdsl/examples/version8_full_42_carrier_bv_vacuum_quotient.py`