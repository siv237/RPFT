# Формулы гейтов Version 7 — страница 24

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка четырнадцати блочных формул полевого Hodge-родителя
градуировки полного пространства рёбер.

## Формулы

### 1. Проекторы и градуировка

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:12`
- Строки: `12--17`

$$
P_+=P_*,\qquad P_-=I-P_*,\qquad
\Gamma_E=P_--P_+,\qquad
(\operatorname{rank}P_+,\operatorname{rank}P_-)=(6,5).
$$

### 2. Двухступенный носитель

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:24`
- Строки: `24--31`

$$
\mathcal K_E=\mathcal E_E^0\oplus\mathcal E_E^1,
\qquad
\dim_{\mathbb C}(\mathcal E_E^0,\mathcal E_E^1)=(11,11),
\qquad
\chi_E=\operatorname{diag}(-I_{11},I_{11}).
$$

### 3. Динамический дифференциал

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:34`
- Строки: `34--38`

$$
d_Z=\begin{pmatrix}0&0\\Z&0\end{pmatrix},
\qquad d_Z^2=0.
$$

### 4. Фоновый дифференциал

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:41`
- Строки: `41--45`

$$
\delta_E=\begin{pmatrix}0&P_+\\P_-&0\end{pmatrix},
\qquad \delta_E^2=0.
$$

### 5. Производная градуировка

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:51`
- Строки: `51--57`

$$
[\delta_E,\delta_E^\dagger]
=-\widehat\Gamma_E,
\qquad
\widehat\Gamma_E=\operatorname{diag}(\Gamma_E,-\Gamma_E).
$$

### 6. Суммарное отображение момента

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:68`
- Строки: `68--74`

$$
\mathfrak m_\mu(Z)
=[d_Z,d_Z^\dagger]+\mu^2[\delta_E,\delta_E^\dagger]
=[d_Z,d_Z^\dagger]-\mu^2\widehat\Gamma_E.
$$

### 7. Единый функционал

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:76`
- Строки: `76--81`

$$
\mathcal S_\mu(Z)
=\frac12\operatorname{Tr}_{\mathcal K_E}\mathfrak m_\mu(Z)^2
-5\mu^4.
$$

### 8. Точная редукция действия

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:86`
- Строки: `86--92`

$$
\mathcal S_\mu(z)
=\sum_{e\in E_*}(|z_e|^2-\mu^2)^2
+\sum_{e\notin E_*}(|z_e|^4+2\mu^2|z_e|^2).
$$

### 9. Гессиан нуля

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:100`
- Строки: `100--103`

$$
(n_-,n_0,n_+)_{z=0}=(12,0,10).
$$

### 10. Точный вакуум

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:109`
- Строки: `109--116`

$$
|z_e|^2=\mu^2\quad(e\in E_*),\qquad
z_e=0\quad(e\notin E_*),\qquad
\min\mathcal S_\mu=0.
$$

### 11. Вакуумный гессиан

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:118`
- Строки: `118--121`

$$
(n_-,n_0,n_+)_{z=z_*}=(0,6,16).
$$

### 12. Семейный вакуум

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:129`
- Строки: `129--134`

$$
Z_e\in\mu U(3)\quad(e\in E_*),\qquad
Z_e=0\quad(e\notin E_*).
$$

### 13. Семейные гессианы

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:137`
- Строки: `137--142`

$$
(n_-,n_0,n_+)_{0}^{\rm family}=(108,0,90),\qquad
(n_-,n_0,n_+)_{*}^{\rm family}=(0,54,144).
$$

### 14. Real-обмен градуировки

- Источник: `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex:153`
- Строки: `153--156`

$$
J_E\widehat\Gamma_EJ_E^{-1}=-\widehat\Gamma_E.
$$

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]

## Source Notes

- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`