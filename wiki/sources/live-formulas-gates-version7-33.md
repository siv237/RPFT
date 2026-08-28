# Формулы гейтов Version 7 — страница 33

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка девяти формул классического составного циклического
гейта.

## Formula 1 — полное слово

$$
\mathcal W_C=D_{Q_Lu_R}D_{u_RX_L}D_{X_Le_R}
D_{e_RL_L}D_{L_LY_R}D_{Y_RQ_L}.
$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:9-14`.

## Formula 2 — переменная часть

$$C=z_{u_RX_L}z_{X_Le_R}z_{L_LY_R}z_{Y_RQ_L}.$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:22-26`.

## Formula 3 — цветные множители

$$
z_{u_RX_L}\in\overline{\mathbf3}_{-5/3},\qquad
z_{Y_RQ_L}\in\mathbf3_{2/3}.
$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:28-33`.

## Formula 4 — ненулевое произведение

$$C\ne0\Longrightarrow z_{u_RX_L}\ne0,\quad z_{Y_RQ_L}\ne0.$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:41-46`.

## Formula 5 — вспомогательное ограничение

$$\Sigma=C(z).$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:52-55`.

## Formula 6 — нулевой гессиан

$$\nabla C(0)=0,\qquad\Hess_0C=0.$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:64-68`.

## Formula 7 — массивный потенциал

$$
V=m^2\sum_{j=1}^4|z_j|^2
-\kappa(C+\overline C)+O(|z|^4),\qquad m^2>0.
$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:74-79`.

## Formula 8 — устойчивый нуль

$$\Hess_0V=2m^2I>0.$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:81-84`.

## Formula 9 — квантовая возможность

$$
\langle z_{u_RX_L}\rangle=\langle z_{Y_RQ_L}\rangle=0,
\qquad\langle C(z)\rangle\ne0.
$$

Source: `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex:95-101`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-color-preserving-composite-cycle-parent-gate]]

## Source Notes

- `s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex`