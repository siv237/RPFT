# Формулы гейтов Version 7 — страница 23

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка тринадцати блочных формул циклически-изотипического
проектора полного меню рёбер.

## Формулы

### 1. Пространство новых стрелок

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:13`
- Строки: `13--19`

$$
\mathcal E_{\rm new}=\bigoplus_{e\in E_{\rm new}}
\operatorname{Hom}(\mathcal H_{s(e)},\mathcal H_{t(e)}),
\qquad |E_{\rm new}|=11.
$$

### 2. Формальная степень участия ребра

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:27`
- Строки: `27--31`

$$
\nu_e=x_e\frac{\partial}{\partial x_e}\log\mathcal R_6(x)\in\{0,1\}.
$$

### 3. Циклический проектор

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:35`
- Строки: `35--39`

$$
P_C=\sum_{e\in E_{\rm new}}\nu_e|e\rangle\langle e|,
\qquad \operatorname{rank}P_C=4.
$$

### 4. Опора циклического проектора

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:41`
- Строки: `41--44`

$$
E_C=\{L_LY_R,Q_LY_R,X_Le_R,X_Lu_R\}.
$$

### 5. Изотипический индикатор

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:52`
- Строки: `52--56`

$$
\epsilon_e^{\rm iso}=\mathbf1[\rho_{s(e)}\simeq\rho_{t(e)}].
$$

### 6. Изотипический проектор

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:63`
- Строки: `63--67`

$$
P_I=\sum_{e\in E_{\rm new}}\epsilon_e^{\rm iso}|e\rangle\langle e|,
\qquad \operatorname{rank}P_I=4.
$$

### 7. Опора изотипического проектора

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:69`
- Строки: `69--72`

$$
E_I=\{L_LY_R,Y_LY_R,X_Le_R,X_LX_R\}.
$$

### 8. Объединение проекторов

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:81`
- Строки: `81--85`

$$
P_*=P_C\vee P_I=P_C+P_I-P_CP_I,
\qquad P_*^2=P_*,\qquad \operatorname{rank}P_*=6.
$$

### 9. Точное разбиение рёбер

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:87`
- Строки: `87--94`

$$
\begin{aligned}
\operatorname{supp}P_*
&=\{L_LY_R,Q_LY_R,X_LX_R,X_Le_R,X_Lu_R,Y_LY_R\},\\
\operatorname{supp}(I-P_*)
&=\{L_LX_R,X_LY_R,X_Ld_R,X_RY_L,Y_Le_R\}.
\end{aligned}
$$

### 10. Градуировка пространства рёбер

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:103`
- Строки: `103--108`

$$
\Gamma_E=I-2P_*,\qquad \Gamma_E^*=\Gamma_E,
\qquad \Gamma_E^2=I.
$$

### 11. Квадратичная знаковая форма

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:110`
- Строки: `110--114`

$$
q_E(z)=\langle z,\Gamma_Ez\rangle
=\sum_{e\notin E_*}\|z_e\|^2-\sum_{e\in E_*}\|z_e\|^2.
$$

### 12. Сигнатуры гессиана

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:117`
- Строки: `117--122`

$$
(n_-,n_0,n_+)_{\rm one\ gen}=(12,0,10),\qquad
(n_-,n_0,n_+)_{3\times3\rm\ family}=(108,0,90).
$$

### 13. Открытые родительские данные

- Источник: `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex:133`
- Строки: `133--140`

$$
\begin{gathered}
\text{общий масштаб запуска},\qquad
\text{единая квартичная стабилизация},\\
\text{ненулевой минимум всех шести целевых блоков}.
\end{gathered}
$$

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-rooted-cycle-isotypic-edge-projector-gate]]

## Source Notes

- `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex`