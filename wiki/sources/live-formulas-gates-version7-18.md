# Формулы гейтов Version 7 — страница 18

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка пятнадцати блочных формул спектрального родителя
стрелочной когерентности.

## Формулы

### 1. Исходные пространства

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:13`
- Строки: `13--18`

$$
V=\mathbb C_{\rm copy}^2,\qquad
W=\mathbb C_{\rm ch}^3,\qquad
B\in\operatorname{Hom}(W,V).
$$

### 2. Градуированная цепь

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:20`
- Строки: `20--29`

$$
\mathcal H_0=\mathbb C\to
\mathcal H_1=V\otimes W^*\to
\mathcal H_2=\Lambda^2V\otimes\Lambda^2W^*,
\qquad\dim_{\mathbb C}\mathcal H=(1,6,3).
$$

### 3. Два ребра

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:31`
- Строки: `31--36`

$$
A_B(1)=\operatorname{vec}B,\qquad
C_B=\frac12d(\Lambda^2)_B.
$$

### 4. Поляризационное тождество

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:39`
- Строки: `39--42`

$$
C_BA_B=\Lambda^2B.
$$

### 5. Нечётный оператор

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:47`
- Строки: `47--57`

$$
\mathcal D_B=
\begin{pmatrix}0&A_B^\dagger&0\\A_B&0&C_B^\dagger\\0&C_B&0\end{pmatrix},
\qquad\Gamma=\operatorname{diag}(1,-I_6,I_3).
$$

### 6. Два инварианта

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:60`
- Строки: `60--63`

$$
T=\operatorname{Tr}(BB^\dagger),\qquad d=\det(BB^\dagger).
$$

### 7. Следы второго ребра

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:65`
- Строки: `65--70`

$$
\|A_B\|_F^2=T,\qquad
\|C_B\|_F^2=\frac12T,\qquad
\operatorname{Tr}(C_B^\dagger C_B)^2=\frac18(T^2-d).
$$

### 8. Спектральные моменты

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:72`
- Строки: `72--76`

$$
\operatorname{Tr}\mathcal D_B^2=3T,\qquad
\operatorname{Tr}\mathcal D_B^4=\frac94T^2+\frac{15}{4}d.
$$

### 9. Полный спектральный полином

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:84`
- Строки: `84--90`

$$
\mathcal S_\mu(B)=\frac49\left(
\operatorname{Tr}\mathcal D_B^4-\mu\operatorname{Tr}\mathcal D_B^2+\mu^2
\right).
$$

### 10. Точное разложение действия

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:92`
- Строки: `92--97`

$$
\mathcal S_\mu(B)=
\left(T-\frac{2\mu}{3}\right)^2+\frac53d.
$$

### 11. Радиальный масштаб

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:101`
- Строки: `101--104`

$$
T_\star=\frac{2\mu}{3}.
$$

### 12. Нормированное действие

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:110`
- Строки: `110--113`

$$
\mathcal S_{9/2}(B)=(T-3)^2+\frac53\det(BB^\dagger).
$$

### 13. Нулевой слой

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:116`
- Строки: `116--121`

$$
\mathcal S_{9/2}(B)=0
\Longleftrightarrow T=3,\qquad\rank B=1.
$$

### 14. Гессиан нуля

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:126`
- Строки: `126--130`

$$
\operatorname{Spec}\operatorname{Hess}_0\mathcal S_{9/2}
=\{-12\}^{\times12}.
$$

### 15. Гессиан вакуума

- Источник: `s2t/gates/version7_edge_coherence_spectral_parent_gate.tex:134`
- Строки: `134--140`

$$
\operatorname{Spec}\operatorname{Hess}_{B_0}\mathcal S_{9/2}
=\{0\}^{\times7}\cup\{10\}^{\times4}\cup\{24\}.
$$

## Links

- [[live-formula-source-index]]
- [[version7-edge-coherence-spectral-parent-gate]]
- [[global-formula-atlas]]