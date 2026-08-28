# Формулы гейтов Version 7 — страница 17

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка двенадцати блочных формул из гейта
ранга-один конденсата стрелочной когерентности.

## Формулы

### 1. Поле когерентности и копийная ковариация

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:14`
- Строки: `14--19`

$$
B\in\operatorname{Hom}(\mathbb C_{\rm ch}^3,
\mathbb C_{\rm copy}^2)\simeq M_{2\times3}(\mathbb C),
\qquad C=BB^\dagger.
$$

### 2. Антисимметризованная двухпутевая амплитуда

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:24`
- Строки: `24--27`

$$
W_{ia,jb}(B)=B_{ia}B_{jb}-B_{ib}B_{ja}.
$$

### 3. Тождество внешнего квадрата

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:29`
- Строки: `29--34`

$$
\|W(B)\|_F^2
=4\|\Lambda^2B\|_F^2
=4\det(BB^\dagger).
$$

### 4. Потенциал когерентности

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:42`
- Строки: `42--46`

$$
\mathcal S_{\rm coh}(B)
=\left(\Tr BB^\dagger-3\right)^2+\|W(B)\|_F^2.
$$

### 5. Точный нулевой слой

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:48`
- Строки: `48--54`

$$
\mathcal S_{\rm coh}(B)=0
\quad\Longleftrightarrow\quad
\Tr BB^\dagger=3,
\qquad \rank B=1.
$$

### 6. Сингулярная форма вакуума

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:56`
- Строки: `56--61`

$$
B_\star=\sqrt3\,u v^\dagger,
\qquad u\in\mathbb C^2,\qquad v\in\mathbb C^3,
\qquad \|u\|=\|v\|=1.
$$

### 7. Размерность вакуумного многообразия

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:64`
- Строки: `64--68`

$$
\dim_{\mathbb R}\mathcal M_{\rm coh}
=\dim S^3+\dim S^5-\dim U(1)=7.
$$

### 8. Гессиан в нуле

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:75`
- Строки: `75--79`

$$
\Spec\Hess_0\mathcal S_{\rm coh}
=\{-12\}^{\times12}.
$$

### 9. Гессиан в ненулевом вакууме

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:85`
- Строки: `85--89`

$$
\Spec\Hess_{B_0}\mathcal S_{\rm coh}
=\{0\}^{\times7}\cup\{24\}^{\times5}.
$$

### 10. Чистый копийный проектор

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:96`
- Строки: `96--102`

$$
R_{\rm copy}(B_\star)
=\frac{B_\star B_\star^\dagger}{\Tr B_\star B_\star^\dagger}
=uu^\dagger,
\qquad R_{\rm copy}^2=R_{\rm copy}.
$$

### 11. Модулярная высота

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:104`
- Строки: `104--108`

$$
h_{\rm copy}=2R_{\rm copy}-I_2,
\qquad h_{\rm copy}^2=I_2.
$$

### 12. Чистый канальный проектор

- Источник: `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex:114`
- Строки: `114--119`

$$
R_{\rm ch}(B_\star)
=\frac{B_\star^\dagger B_\star}{\Tr B_\star^\dagger B_\star}
=vv^\dagger.
$$

## Links

- [[live-formula-source-index]]
- [[version7-edge-coherence-rank-one-condensate-gate]]
- [[version7-edge-coherence-formula-intuition-map]]
- [[global-formula-atlas]]