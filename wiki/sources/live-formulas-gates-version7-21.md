# Формулы гейтов Version 7 — страница 21

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка одиннадцати блочных формул полной графовой конкуренции
конденсата когерентности.

## Формулы

### 1. Прямоугольник когерентности

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:14`
- Строки: `14--17`

$$
\{L_L,Y_L\}\times\{e_R,X_R,Y_R\}.
$$

### 2. Целевая внутренняя маска

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:20`
- Строки: `20--24`

$$
M_{\rm target}^{B}=\begin{pmatrix}1&0&1\\0&0&1\end{pmatrix}.
$$

### 3. Внешние новые рёбра

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:30`
- Строки: `30--33`

$$
\{Q_LY_R,\ X_LX_R,\ X_LY_R,\ X_Ld_R,\ X_Le_R,\ X_Lu_R\}.
$$

### 4. Общий представитель целевой опоры

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:39`
- Строки: `39--44`

$$
B_{\rm target}=\begin{pmatrix}a&0&b\\0&0&c\end{pmatrix},
\qquad abc\ne0.
$$

### 5. Ненулевой минор

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:46`
- Строки: `46--50`

$$
\det B_{\{e,Y\}}=ac\ne0,\qquad \rank B_{\rm target}=2.
$$

### 6. Вакуум когерентности

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:52`
- Строки: `52--56`

$$
\Lambda^2B=0,\qquad \rank B=1.
$$

### 7. Прямоугольная опора ранга один

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:61`
- Строки: `61--65`

$$
\operatorname{supp}(uv^\dagger)
=\operatorname{supp}(u)\times\operatorname{supp}(v).
$$

### 8. Действие на целевой страте

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:75`
- Строки: `75--79`

$$
\mathcal S_B=(x+y+z-3)^2+\frac53xz.
$$

### 9. Энергия единичного представителя

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:86`
- Строки: `86--91`

$$
\Tr BB^\dagger=3,\qquad
\det(BB^\dagger)=1,\qquad
\mathcal S_B=\frac53>0.
$$

### 10. Спектаторное расширение

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:98`
- Строки: `98--102`

$$
\mathcal S_{\rm ext}(B,z)=\mathcal S_B(B),
\qquad \frac{\partial\mathcal S_{\rm ext}}{\partial z}=0.
$$

### 11. Расширенный гессиан

- Источник: `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex:106`
- Строки: `106--109`

$$
(n_-,n_0,n_+)=(0,19,5).
$$

## Links

- [[live-formula-source-index]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[global-formula-atlas]]