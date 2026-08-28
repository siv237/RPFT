# Version VII: атрибуция Hodge-уровня фоновому оператору

> Status: mature
> Type: question
> Updated: 2026-08-27

## Problem

Проверить, может ли фоновый момент `K15=[d15,d15†]` единственным образом
определить уровень `mu² hatGamma_E` Hodge-родителя и тем самым вывести хотя
бы относительное отношение `mu/||D_H15||`.

## Search for Solution

После ортогонального разложения трёх физических рёбер определены независимые
положительные координаты

$$
k_a=\frac12\operatorname{Tr}(\chi_{15}\Pi_aK_{15}\Pi_a)
=\operatorname{Tr}(Y_a^\dagger Y_a),\qquad a\in\{u,d,e\}.
$$

Минимальные линейные gauge-, Real- и градуировочно-совместимые отображения в
уже выведенную прямую `R hatGamma_E` имеют вид

$$
\Psi_c(K_{15})=(c_uk_u+c_dk_d+c_ek_e)\widehat\Gamma_E.
$$

Точные калибровочные типы не переставляют `u,d,e`, поэтому уже минимальный
класс таких отображений содержит трёхмерное подпространство. Даже после
искусственного забывания различия `u/d` остаются две независимые орбиты.

## Result

Гейт закрыт отрицательно:

- положительность оставляет конус `c_u,c_d,c_e >= 0`;
- одна нормировка оставляет двумерный симплекс;
- грубая симметрия `u<->d` оставляет одномерный интервал;
- полный, активный и рёберный нормированные следы дают соответственно
  `2/3`, `6/5` и `1` на единичном фоне;
- неравные семейные нормы превращают свободу коэффициентов в физически
  различающиеся уровни.

Следовательно, `H15` содержит ненулевые масштабные наблюдаемые, но не
каноническое отображение между физическим и полевым носителями. Ни
относительный, ни абсолютный Hodge-масштаб не выведен.

## Compliance Check

- ранг минимального точного пространства отображений: `3`;
- минимальная размерность после грубой `u/d`-симметрии: `2`;
- `Tr D_H15²=6` на единичном типизированном фоне;
- `hatGamma_E²=I22`, `Tr hatGamma_E²=22`;
- остатки самосопряжённости, Real-нечётности и градуировочной совместимости:
  `0`;
- общий неравный тест `k=(1,4,9)` различает три положительных
  нормированных отображения.

## Next Gate

[[version7-single-scale-calibration-closure-gate]] выполнил этот тест:
линейный спектр замкнулся, но эффективная квартика осталась свободной.
Следующий вопрос —
[[version7-spacetime-kinetic-potential-ratio-admission-gate]].

## Links

- [[version7-hodge-scale-origin-project-intuition-search]]
- [[spectral-dilaton-moment-map-scale-literature-2026]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]
- [[version7-single-scale-calibration-closure-gate]]
- [[version7-spacetime-kinetic-potential-ratio-admission-gate]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_hodge_level_background_attribution_gate.tex`
- `s2t/audits/s2t_v7_hodge_level_background_attribution_gate.py`
- `s2t/results/s2t_v7_hodge_level_background_attribution_gate_results.json`