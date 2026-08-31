# Нормировка трёхчастичного шумового подъёма

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Одночастичный КМС-генератор не определяет единственный трёхчастичный шум.
Перестановочно-инвариантная ковариация копий

`R_c=(1-c)I_3+c 11^T`

вполне положительна при `-1/2<=c<=1`, и весь этот отрезок имеет одинаковую
одночастичную динамику. `c=0` соответствует независимым средам, `c=1` —
общему коллективному шуму.

## Точные отношения

- `K_3=3J_1q` следует из трёх аддитивных копий.
- На слабом секторе `I^2=(15/4)P_sym+(3/4)P_mix`.
- Поэтому `Delta_3=3c kappa_2`, `Delta_2=2c kappa_2` и
  `Delta_3/Delta_2=3/2` при `c!=0`.

Отношения `3` и `3/2` структурны, но не выбирают значение корреляции `c`.

## Дискриминатор

После точной одночастичной нормировки

`v_c=c*52(25x^2+38x+13)/(375x^3+3916x^2+7267x+2782)`.

Коллективная точка даёт `0.252005943190...`, независимая — нуль. Даже
максимум `c=1` строго ниже сравнительной мишени при `x=e^(-2)`.

## Статус

- Тензорный коэффициент `3`: закрыт.
- Отношение `3/2`: закрыто.
- Единственность трёхчастичного подъёма: запрещена.
- Происхождение общей среды проверено в
  [[version8-baryon-common-environment-correlation-origin-gate]]:
  однокопийный родитель не выбирает `c`.
- Физическая теорема о массах: не получена.

## Связи

- [[version8-baryon-directed-transfer-convention-selector-gate]]
- [[version8-baryon-canonical-weights-geta-no-go-gate]]
- [[global-formula-atlas]]
- [[version8-baryon-common-environment-correlation-origin-gate]]

## Исходники

- `s2t/gates/version8_baryon_three_particle_lift_normalization_gate.tex`
- `s2t/audits/s2t_v8_baryon_three_particle_lift_normalization_gate.py`
- `s2t/results/s2t_v8_baryon_three_particle_lift_normalization_gate_results.json`