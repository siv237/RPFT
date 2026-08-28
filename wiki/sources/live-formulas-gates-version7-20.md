# Формулы гейтов Version 7 — страница 20

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка тринадцати блочных формул полевого
суперсвязностного допуска цепи когерентности.

## Формулы

### 1. Пучки копий и каналов

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:9`
- Строки: `9--14`

$$
V=\mathbb C^2_{\rm copy},\qquad
W=W_e\oplus W_X\oplus W_Y\simeq\mathbb C^3,
\qquad B\in\operatorname{Hom}(W,V).
$$

### 2. Градуированный носитель

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:21`
- Строки: `21--26`

$$
\mathcal E^0=\underline{\mathbb C},\qquad
\mathcal E^1=\operatorname{Hom}(W,V),\qquad
\mathcal E^2=\operatorname{Hom}(\Lambda^2W,\Lambda^2V).
$$

### 3. Ориентированная часть

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:34`
- Строки: `34--43`

$$
d_B|_{\mathcal E^0}=A_B,\qquad
d_B|_{\mathcal E^1}=C_B,\qquad
d_B|_{\mathcal E^2}=0.
$$

### 4. Квадрат ориентированной части

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:45`
- Строки: `45--49`

$$
d_B^2|_{\mathcal E^0}=C_BA_B=\Lambda^2B,
\qquad d_B^2|_{\mathcal E^1\oplus\mathcal E^2}=0.
$$

### 5. Норма кривизны

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:51`
- Строки: `51--55`

$$
\|d_B^2\|^2=\|\Lambda^2B\|_F^2=\det(BB^\dagger).
$$

### 6. Интегрируемая страта

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:58`
- Строки: `58--63`

$$
\rank B\leq1\quad\Longleftrightarrow\quad d_B^2=0.
$$

### 7. Индуцированные связности

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:71`
- Строки: `71--77`

$$
\nabla^{\mathcal E^1}X=\nabla^V X-X\nabla^W,
\qquad
\nabla^{\mathcal E^2}Y
=\nabla^{\Lambda^2V}Y-Y\nabla^{\Lambda^2W}.
$$

### 8. Блочная группа

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:86`
- Строки: `86--90`

$$
G_{\rm blk}=U(2)_{\rm copy}\times U(2)_{eX}\times U(1)_Y
\subset U(V)\times U(W).
$$

### 9. Преобразование поля

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:92`
- Строки: `92--95`

$$
B\longmapsto gBh^\dagger.
$$

### 10. Ковариантность внешней степени

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:97`
- Строки: `97--103`

$$
\Lambda^2(gBh^\dagger)
=\Lambda^2g\,(\Lambda^2B)\,(\Lambda^2h)^\dagger,
\qquad
C_{gBh^\dagger}(gXh^\dagger)
=\Lambda^2g\,C_B(X)\,(\Lambda^2h)^\dagger.
$$

### 11. Эрмитова часть

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:112`
- Строки: `112--115`

$$
\mathcal D_B=d_B+d_B^\dagger.
$$

### 12. Конечные следы

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:118`
- Строки: `118--123`

$$
\Tr\mathcal D_B^2=3\Tr(BB^\dagger),\qquad
\Tr\mathcal D_B^4=\frac94(\Tr BB^\dagger)^2
+\frac{15}{4}\det(BB^\dagger).
$$

### 13. Кинетическая метрика

- Источник: `s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex:126`
- Строки: `126--131`

$$
\Tr(\delta\mathcal D_B\,\delta\mathcal D_B)
=3\Tr(\delta B\,\delta B^\dagger).
$$

## Links

- [[live-formula-source-index]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[global-formula-atlas]]