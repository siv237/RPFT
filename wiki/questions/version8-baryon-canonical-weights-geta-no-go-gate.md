# Канонические барионные веса и запрет семейства G_eta

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Независимо подтверждены точные формы шести весов стабилизаторной ветви
общего КМС-следа. В заданном барионном отображении внешняя мишень строго
недостижима вдоль всего положительного семейства
`G_eta=eta P_tr+P_gauge`.

## Усиленное доказательство

Требуемый корень пропорционален

`P(x)=105133x^2+28806x-13799`.

Многочлен возрастает при `x>0`. Поскольку

`e^2 > sum_(n=0)^4 2^n/n! = 7`,

получаем `x=e^(-2)<1/7`, тогда как `P(1/7)=-52768/7<0`.
Следовательно, корень `eta*` отрицателен точно, без использования
десятичной аппроксимации `e^(-2)`.

## Научная граница

- Принимается точный провенанс шести весов в `Q(e^(-2))`.
- Принимается условный запрет положительного `G_eta`-среза.
- Остаток `8.21%` не принимается как безусловное предсказание: мишень
  внешняя, а направленный перенос `V,V*` в барионную форму неоднозначен.
- Расхождение `0.2570` и `0.1962` разобрано в
  [[version8-baryon-directed-transfer-convention-selector-gate]]: оба
  чтения отличаются от прямого канонического ограничения.

## Связи

- [[external-baryon-canonical-point-c1]]
- [[version8-baryon-material-merge-review]]
- [[version8-canonical-noise-frame-common-trace-gate]]
- [[version8-common-chain-dirichlet-rate-metric-gate]]
- [[version8-chain-orientation-index-defect-selector-gate]]
- [[version8-baryon-directed-transfer-convention-selector-gate]]

## Исходники

- `prism-uploads/baryon_canonical_point_result.md`
- `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex`
- `s2t/audits/s2t_v8_baryon_canonical_weights_geta_no_go_gate.py`
- `s2t/results/s2t_v8_baryon_canonical_weights_geta_no_go_gate_results.json`