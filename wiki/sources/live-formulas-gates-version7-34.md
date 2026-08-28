# Формулы гейтов Version 7 — страница 34

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка девяти формул гейта виртуального цветного моста.

## Formula 1 — тяжёлые и лёгкие поля

$$
a=z_{u_RX_L}\in\overline{\mathbf3},\qquad
b=z_{Y_RQ_L}\in\mathbf3,
\qquad p=z_{X_Le_R},\qquad q=z_{L_LY_R}.
$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:14-20`.

## Formula 2 — тяжёлый блок

$$
K(pq)=\begin{pmatrix}M_a^2&-\kappa\overline{pq}\\-\kappa pq&M_b^2\end{pmatrix},
\qquad \Delta(pq)=M_a^2M_b^2-\kappa^2|pq|^2.
$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:24-31`.

## Formula 3 — область тяжёлой щели

$$\Delta(pq)>0.$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:35-38`.

## Formula 4 — классическое решение

$$a=b=0.$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:45-48`.

## Formula 5 — конечномерный детерминант

$$\Gamma_0(p,q)=3\log\Delta(pq)+\mathrm{const}.$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:59-62`.

## Formula 6 — первый индуцированный член

$$
\Gamma_0=3\log(M_a^2M_b^2)
-\frac{3\kappa^2}{M_a^2M_b^2}|pq|^2+O(|pq|^4).
$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:65-71`.

## Formula 7 — нулевой лёгкий гессиан

$$\Hess_{p=q=0}\Gamma_0=0.$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:74-77`.

## Formula 8 — тяжёлые собственные значения

$$
\lambda_\pm=\frac12\left[M_a^2+M_b^2
\pm\sqrt{(M_a^2-M_b^2)^2+4\kappa^2|pq|^2}\right].
$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:82-88`.

## Formula 9 — четырёхмерный Tr log

$$
\Gamma_4^{(1)}=-3\kappa^2|pq|^2
\int\frac{d^4k}{(2\pi)^4}
\frac1{(k^2+M_a^2)(k^2+M_b^2)}.
$$

Source: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:97-103`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-virtual-colored-bridge-schur-complement-gate]]

## Source Notes

- `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex`