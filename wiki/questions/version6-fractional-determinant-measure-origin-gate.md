# Version VI: происхождение дробного детерминантного барьера

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Обратный аудит проекта нашёл несколько уже доказанных следовых весов внутри
окна `0 < nu < 17/168`:

- `M300`: полный determinant `nu=1/10`, Pfaffian `nu=1/20`;
- локальный Real-носитель `M210`: Pfaffian `nu=1/14`;
- полный determinant на `M210` даёт `1/7` и уже слишком силён.

Для `nu=1/10` отрицательная локальная кривизна сохраняется с малым точным
остатком `-3/560`; расстояние до верхней границы равно `1/840`.

## Status Boundary

Это условный проход, а не готовое рождение материи. `M300` сохраняется как
единый носитель нормированного следа, но не как выведенная координатная
алгебра. Кроме того, внутренний KO6-модуль сам по себе не даёт требуемый
реальный фермионный интеграл: необходим полный product-Dirac суммарной
KO-степени два и его Pfaffian line.

Коэффициенты `1/24` и половинный scalar-FP остаток также численно подходят,
но принадлежат другим операторам и не имеют карты к `log det R`.

## Next Test

Тест выполнен в [[version6-product-ko2-family-pfaffian-operator-gate]].
Product-KO2 пфаффиан существует, но обычный березинский интеграл даёт
показатель `15`, а не `1/20`. Дробные отношения относятся к нормированному
интенсивному логарифму детерминанта и требуют отдельного общего принципа
свободной энергии.

## Links

- [[version6-polar-bv-rank-loss-barrier-gate]]
- [[version6-product-ko2-family-pfaffian-operator-gate]]
- [[normalized-pfaffian-fuglede-kadison-literature-2026]]
- [[version5-modular-ko6-m60-amalgamation-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version5-closure-deficit-induced-vacuum-response-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_fractional_determinant_measure_origin_gate.tex`
- `s2t/audits/s2t_v6_fractional_determinant_measure_origin_gate.py`
- `s2t/results/s2t_v6_fractional_determinant_measure_origin_gate_results.json`