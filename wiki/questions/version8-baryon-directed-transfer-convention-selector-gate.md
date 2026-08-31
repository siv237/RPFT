# Селектор направленного переноса в барионный сектор

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Общий КМС-след разрешает направленную двусмысленность на уровне
одночастичного исходного угла. Для `x=e^(-2)` канонические пружины равны

- `J_Q=x I_6/[2(a+b)]` для `QLYR`;
- `J_L=x I_6/[13(a+b)]` для связывающей инцидентности.

Множитель `x` нельзя удалять: он является скоростью исходного угла в
направленном КМС-генераторе.

## Новый точный дефект

Проверяемое барионное отображение использовало стрелочную пружину
`x I_6/[4(a+b)]`, то есть половину прямого канонического ограничения.
Линкинговая пружина совпала точно. Поэтому требуемые множители равны
`QLYR: 2`, `linking: 1`.

При неизменной калибровочной парной форме прямой кандидат даёт

`v_dir=52(25x^2+38x+13)/(375x^3+3916x^2+7267x+2782)`,

или `0.252005943190...` при `x=e^(-2)`. Это не третья подгонка, а следствие
исправления одночастичного оператора; полный трёхчастичный подъём ещё надо
вывести независимо.

## Статус

- Направление КМС: закрыто.
- Одночастичный оператор исходного угла: закрыт.
- Дефект половинного стрелочного веса: доказан точно.
- Полный переход к трёхчастичному оператору разобран в
  [[version8-baryon-three-particle-lift-normalization-gate]]: единственность
  запрещена непрерывным отрезком корреляций копий.
- Физическая теорема о массах: не получена.

## Связи

- [[version8-baryon-canonical-weights-geta-no-go-gate]]
- [[version8-canonical-noise-frame-common-trace-gate]]
- [[version8-kms-nontracial-relative-rate-selector-gate]]
- [[external-baryon-canonical-point-c1]]
- [[global-formula-atlas]]
- [[version8-baryon-three-particle-lift-normalization-gate]]

## Исходники

- `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_directed_transfer_convention_selector_gate.py`
- `s2t/results/s2t_v8_baryon_directed_transfer_convention_selector_gate_results.json`