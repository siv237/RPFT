# Формулы гейтов Version 7 — страница 36

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Механическая выписка десяти формул совместного гессиана singlet-вакуума и
виртуального цикла.

## Formula 1 — безразмерные переменные

$$r=|p|/\mu,\qquad s=|q|/\mu,\qquad a=(\kappa\mu^2/(M_aM_b))^2.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:12`

## Formula 2 — совместный потенциал

$$V=(r^2-1)^2+(s^2-1)^2+\gamma\log(1-ar^2s^2),\qquad ar^2s^2<1.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:18`

## Formula 3 — симметричная ветвь

$$r=s=\sqrt u,\qquad u>1.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:32`

## Formula 4 — стационарность

$$\gamma=2(u-1)(1-au^2)/(au).$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:37`

## Formula 5 — тяжёлая щель

$$au^2<1.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:42`

## Formula 6 — радиальные собственные значения

$$
\lambda_{\parallel}=8\frac{1-au^2(2u-1)}{1-au^2},\qquad
\lambda_{\perp}=8(2u-1).
$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:54`

## Formula 7 — условие локальной устойчивости

$$au^2(2u-1)<1.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:63`

## Formula 8 — контрольная точка

$$a=1/10,\qquad u=6/5,\qquad\gamma=214/75.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:72`

## Formula 9 — singlet-сигнатура

$$ (n_-,n_0,n_+)_{\rm singlet}=(0,4,4). $$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:87`

## Formula 10 — граница конечномерной модели

$$\lim_{ar^2s^2\to1^-}V(r,s)=-\infty.$$

Source: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:104`

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]]

## Source Notes

- `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:12-107`