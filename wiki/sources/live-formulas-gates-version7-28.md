# Формулы гейтов Version 7 — страница 28

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка девяти формул проверки, может ли фон `H15`
единственным образом породить уровень Hodge-родителя.

## Formula 1 — уровень Hodge-момента

$$
\mathfrak m_\mu(Z)=[d_Z,d_Z^\dagger]-\mu^2\widehat\Gamma_E.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:7-11`.

## Formula 2 — типизированный фон

$$
d_{15}=d_u\oplus d_d\oplus d_e,\qquad
K_{15}=[d_{15},d_{15}^\dagger],\qquad
\chi_{15}=\operatorname{diag}(-I_3,I_3).
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:19-26`.

## Formula 3 — три положительные координаты

$$
k_a(K_{15})=\frac12\operatorname{Tr}
(\chi_{15}\Pi_aK_{15}\Pi_a)=\operatorname{Tr}(Y_a^\dagger Y_a)\ge0.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:29-34`.

## Formula 4 — семейство эквивариантных отображений

$$
\Psi_c(K_{15})=(c_uk_u+c_dk_d+c_ek_e)\widehat\Gamma_E,
\qquad c\in\mathbb R^3.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:41-46`.

## Formula 5 — точные орбиты типов

$$
\{u\},\qquad\{d\},\qquad\{e\}.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:53-56`.

## Formula 6 — грубые орбиты

$$
\{u,d\},\qquad\{e\}.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:59-62`.

## Formula 7 — единичный фон

$$
(k_u,k_d,k_e)=(1,1,1),\qquad \operatorname{Tr}D_{H_{15}}^2=6.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:80-85`.

## Formula 8 — неоднозначность нормированного следа

$$
\frac1{9}\operatorname{Tr}D_{H_{15}}^2=\frac23,\qquad
\frac1{5}\operatorname{Tr}_{\rm active}D_{H_{15}}^2=\frac65,\qquad
\frac1{2|E_0|}\operatorname{Tr}D_{H_{15}}^2=1.
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:87-94`.

## Formula 9 — неравный фон

$$
(k_u,k_d,k_e)=(1,4,9).
$$

Source: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:99-102`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-hodge-level-background-attribution-gate]]

## Source Notes

- `s2t/gates/version7_hodge_level_background_attribution_gate.tex`