# Формулы гейтов Version 7 — страница 25

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка восемнадцати блочных формул Real-подъёма двух цветов
стрелок и относительного семейного quotient. Первая формула точно повторяет
определение полного пространства новых стрелок из предыдущего гейта;
остальные семнадцать блоков новые.

## Formula 1 — полный модуль новых стрелок

$$
\mathcal E_{\rm new}
=\bigoplus_{e\in E_{\rm new}}
\operatorname{Hom}(\mathcal H_{s(e)},\mathcal H_{t(e)}),
\qquad |E_{\rm new}|=11.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:13-19`.
Exact repeat: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:13-19`.

## Formula 2 — двухступенный модуль

$$
\mathcal K_E=\mathcal E_{\rm new}^{0}\oplus
\mathcal E_{\rm new}^{1},
\qquad
\chi_E=\operatorname{diag}(-I,I).
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:27-33`.

## Formula 3 — действие алгебры

$$
\rho_E(a)=\operatorname{diag}(\rho_{\rm arr}(a),
\rho_{\rm arr}(a)).
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:35-39`.

## Formula 4 — фоновый бимодульный дифференциал

$$
\delta_E=\begin{pmatrix}0&P_+\\P_-&0\end{pmatrix},
\qquad
\delta_E^2=0,
\qquad
[\delta_E,\rho_E(a)]=[d_Z,\rho_E(a)]=0.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:41-48`.

## Formula 5 — одна суперсвязность и один момент

$$
\mathbb A_E=\nabla_E+d_Z+\mu\delta_E,
\qquad
\mathfrak m_E=[d_Z,d_Z^\dagger]
+\mu^2[\delta_E,\delta_E^\dagger].
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:51-57`.

## Formula 6 — Real-структура

$$
J_E\chi_EJ_E^{-1}=-\chi_E,
\qquad
J_E\delta_EJ_E^{-1}=\delta_E^\dagger.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:66-71`.

## Formula 7 — нулевой модуль обычных внутренних одноформ

$$
\Omega^1_{D_E}(\mathcal A_F)
=\operatorname{span}\{a[D_E,b]:a,b\in\mathcal A_F\}=0.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:79-83`.

## Formula 8 — шесть выбранных рёбер

$$
E_*=\{L_LY_R,Q_LY_R,X_LX_R,X_Le_R,X_Lu_R,Y_LY_R\}.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:93-96`.

## Formula 9 — выбранные рёбра образуют лес

$$
|V|=9,\qquad |E_*|=6,\qquad c_*=3,\qquad
\operatorname{rank}B_*=6,\qquad |E_*|-|V|+c_*=0.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:99-103`.

## Formula 10 — старые рёбра H15

$$
E_0=\{L_Le_R,Q_Ld_R,Q_Lu_R\}.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:111-114`.

## Formula 11 — полный граф имеет один цикл

$$
|E_0\cup E_*|=9,\qquad c_{\rm full}=1,\qquad
\operatorname{rank}B_{\rm full}=8,\qquad
b_1=9-9+1=1.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:120-125`.

## Formula 12 — действие семейных кадров

$$
\delta Z_e=\xi_{t(e)}-\xi_{s(e)},
\qquad \xi_v\in\mathfrak u(3).
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:131-135`.

## Formula 13 — кадры, сохраняющие H15

$$
B_0^T\xi=0,\qquad
\dim_{\mathbb R}\ker(B_0^T\otimes I_{\mathfrak u(3)})
=(9-3)\cdot9=54.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:137-142`.

## Formula 14 — ранг относительного действия

$$
\operatorname{rank}_{\mathbb R}
\left.(B_*^T\otimes I_{\mathfrak u(3)})\right|_{\ker B_0^T}
=5\cdot9=45.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:144-149`.

## Formula 15 — линейный остаток

$$
\dim_{\mathbb R}\mathcal M_{\rm orient}^{\rm rel}
=54-45=9=\dim_{\mathbb R}U(3).
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:152-156`.

## Formula 16 — циклическая голономия

$$
W_C=Z_{e_1}^{\epsilon_1}Z_{e_2}^{\epsilon_2}\cdots
Z_{e_6}^{\epsilon_6}\in U(3),
\qquad \epsilon_j\in\{1,-1\}.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:159-164`.

## Formula 17 — сопряжение голономии

$$
W_C\longmapsto U_{v_0}W_CU_{v_0}^{-1}.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:166-169`.

## Formula 18 — нелинейный quotient

$$
\mathcal M_C=U(3)/\operatorname{Ad}U(3),
\qquad \dim_{\mathbb R}\mathcal M_C^{\rm generic}=3.
$$

Source: `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex:174-178`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]

## Source Notes

- `s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex`