# Формулы гейтов Version 7 — страница 31

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка десяти формул проверки общего gauge-якоря момента
`f0`.

## Formula 1 — исходная квартика

$$
C_0=\frac{f_0}{8\pi^2},\qquad
\lambda_E=\frac1{8C_0}=\frac{\pi^2}{f_0}.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:7-12`.

## Formula 2 — полный gauge-индекс

$$
q_G=\operatorname{Tr}_{\mathcal H_F}Q^2.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:14-17`.

## Formula 3 — коэффициент кривизны

$$
\frac{C_0q_G}{3}F_{\mu\nu}F^{\mu\nu}.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:19-22`.

## Formula 4 — условный gauge-якорь

$$
f_0=\frac{6\pi^2}{q_Gg^2},\qquad
\lambda_E=\frac{q_G}{6}g^2.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:24-29`.

## Formula 5 — старый относительный U(1)

$$
\lambda_E=\frac13g^2.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:31-34`.

## Formula 6 — редуцированный след меток

$$
\mathcal E_{\rm new}^{\rm red}\simeq\mathbb C^{11},\qquad
\operatorname{Tr}_{\rm red}|e\rangle\langle e|=1.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:42-48`.

## Formula 7 — индуцированный заряд блока

$$
q_e=Y_t-Y_s,\qquad
\operatorname{Tr}_eF^2\mathrel{\propto}\dim(R_e)q_e^2F^2.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:54-60`.

## Formula 8 — заряды выбранных рёбер

$$
(Y_t-Y_s)_{E_*}=\left(0,-\frac23,0,0,\frac53,0\right).
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:66-72`.

## Formula 9 — неравномерный индекс

$$
\sum_{e\in E_*}(Y_t-Y_s)^2=\frac{29}{9},\qquad
\{q_e^2\}=\left\{0,\frac49,\frac{25}{9}\right\}.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:75-80`.

## Formula 10 — индекс блочной суммы

$$
q_G^{\rm tot}=q_G^{H_{15}}+q_G^{\rm edge}.
$$

Source: `s2t/gates/version7_common_gauge_f0_anchor_gate.tex:88-91`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-common-gauge-f0-anchor-gate]]

## Source Notes

- `s2t/gates/version7_common_gauge_f0_anchor_gate.tex`