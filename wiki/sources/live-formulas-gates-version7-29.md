# Формулы гейтов Version 7 — страница 29

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка девяти формул одномасштабного EFT-теста Hodge-родителя.

## Formula 1 — общая эффективная плотность

$$
\mathcal L_E=\frac Z2\sum_e[(\partial_\mu x_e)^2+(\partial_\mu y_e)^2]
-\kappa\mathcal S_\mu(z),\qquad z_e=x_e+iy_e.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:13-20`.

## Formula 2 — канонические переменные

$$
\phi_e=\sqrt Zz_e,\qquad v=\sqrt Z\mu,\qquad
\lambda_E=\frac\kappa{Z^2}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:28-35`.

## Formula 3 — единый квадратичный масштаб

$$
M_0^2=\frac{\kappa\mu^2}{Z}=\lambda_Ev^2.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:37-40`.

## Formula 4 — спектр в нуле

$$
\operatorname{Spec}(M_0^{-2}G^{-1}\operatorname{Hess}_0)
=\{-4^{(12)},4^{(10)}\}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:47-51`.

## Formula 5 — вакуумный спектр

$$
\operatorname{Spec}(M_0^{-2}G^{-1}\operatorname{Hess}_*)
=\{0^{(6)},4^{(10)},8^{(6)}\}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:53-57`.

## Formula 6 — линейные отношения

$$
\frac{m_{\rm rad}}{m_{\rm gap}}=\sqrt2,\qquad
\frac{\xi_{\rm rad}}{\xi_{\rm gap}}=\frac1{\sqrt2}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:61-66`.

## Formula 7 — вырождение амплитуды и квартики

$$
v=\frac{M_0}{\sqrt{\lambda_E}}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:80-83`.

## Formula 8 — три одинаковых линейных спектра

$$
\lambda_E\in\left\{\frac14,1,4\right\}
\Longrightarrow
v\in\left\{2M_0,M_0,\frac12M_0\right\}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:85-90`.

## Formula 9 — нелинейное натяжение

$$
\sigma_{\rm nl}\sim v^2M_0=\frac{M_0^3}{\lambda_E}.
$$

Source: `s2t/gates/version7_single_scale_calibration_closure_gate.tex:94-97`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-single-scale-calibration-closure-gate]]

## Source Notes

- `s2t/gates/version7_single_scale_calibration_closure_gate.tex`