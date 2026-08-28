# Формулы гейтов Version 7 — страница 38

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Выписка двенадцати формульных утверждений полного product-`a6` гейта,
соответствующих одиннадцати внешним LaTeX-блокам.

## Formula 1 — слабый кадр

$$H=(0,1)^T,\qquad\widetilde H=(1,0)^T.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:9-14`

## Formula 2 — ортогональность

$$\widetilde H^\dagger H=0.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:19-22`

## Formula 3 — up-полином

$$\operatorname{Tr}\Phi_u^6=50+24x^2+42y^2+12x^4+24y^4+6x^2y^2+2x^6+4y^6.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:32-37`

## Formula 4 — нулевой up-коэффициент

$$[xy]\operatorname{Tr}\Phi_u^6=0.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:39-42`

## Formula 5 — три локальных цикла

$$u:(QLYR,XLuR),\qquad d:(QLYR,XLdR),\qquad W:(LLXR,YLeR).$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:54-62`

## Formula 6 — down-полином

$$\operatorname{Tr}\Phi_d^6=\operatorname{Tr}\Phi_u^6+12xy.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:68-73`

## Formula 7 — down-коэффициент

$$[xy]\operatorname{Tr}\Phi_d^6=12.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:75-78`

## Formula 8 — слабый полином

$$\operatorname{Tr}\Phi_W^6=48+30(x^2+y^2)+12xy+12(x^4+y^4)+2(x^6+y^6).$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:80-84`

## Formula 9 — Gaussian-множитель

$$-\frac16\operatorname{Tr}\Phi^6.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:92-95`

## Formula 10 — три билинейных вклада

$$0,\qquad-2xy,\qquad-2xy.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:97-100`

## Formula 11 — down-гессиан

$$H_d=\begin{pmatrix}48&12\\12&84\end{pmatrix},\qquad\operatorname{Spec}H_d=\{66-6\sqrt{13},66+6\sqrt{13}\}.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:105-112`

## Formula 12 — слабый гессиан

$$H_W=\begin{pmatrix}60&12\\12&60\end{pmatrix},\qquad\operatorname{Spec}H_W=\{48,72\}.$$

Source: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:105-112`

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-full-product-a6-cycle-coefficient-gate]]

## Source Notes

- `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex`