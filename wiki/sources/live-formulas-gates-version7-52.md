# Гейты Version 7, продолжение — часть 52

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **34** блочных формул из **4** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-52-0001

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 r=\frac{|p|}{\mu},\qquad s=\frac{|q|}{\mu},\qquad
 a=\left(\frac{\kappa\mu^2}{M_aM_b}\right)^2.
 \label{eq:v7-combined-hessian-variables}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0002

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 V(r,s)=(r^2-1)^2+(s^2-1)^2
 +\gamma\log(1-ar^2s^2),
 \qquad ar^2s^2<1,
 \label{eq:v7-combined-hessian-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0003

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:32`
- Строки: `32--35`

```latex
\begin{equation}
 r=s=\sqrt u,\qquad u>1.
 \label{eq:v7-combined-hessian-symmetric-branch}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0004

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:37`
- Строки: `37--40`

```latex
\begin{equation}
 \gamma=\frac{2(u-1)(1-au^2)}{au}.
 \label{eq:v7-combined-hessian-stationarity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0005

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 au^2<1.
 \label{eq:v7-combined-hessian-gap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0006

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:54`
- Строки: `54--60`

```latex
\begin{align}
 \lambda_{\parallel}
 &=8\frac{1-au^2(2u-1)}{1-au^2},
 \label{eq:v7-combined-hessian-radial-parallel}\\
 \lambda_{\perp}&=8(2u-1).
 \label{eq:v7-combined-hessian-radial-perpendicular}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0007

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 \boxed{au^2(2u-1)<1.}
 \label{eq:v7-combined-hessian-local-stability}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0008

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:72`
- Строки: `72--76`

```latex
\begin{equation}
 a=\frac1{10},\qquad u=\frac65,qquad
 \gamma=\frac{214}{75}
 \label{eq:v7-combined-hessian-benchmark}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0009

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:87`
- Строки: `87--90`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{\rm singlet}=(0,4,4)
 \label{eq:v7-combined-hessian-singlet-signature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0010

- Источник: `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex:104`
- Строки: `104--107`

```latex
\begin{equation}
 \lim_{ar^2s^2\to1^-}V(r,s)=-\infty.
 \label{eq:v7-combined-hessian-boundary-divergence}
\end{equation}
```

## `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-52-0011

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:9`
- Строки: `9--14`

```latex
\begin{equation}
 \mathcal D_E
 =i\gamma^\mu\partial_\mu\otimes I
 +\gamma^5\otimes a\Phi_E(x),
 \label{eq:v7-spacetime-ratio-product-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0012

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 C_0=\frac{f_0}{8\pi^2}.
 \label{eq:v7-spacetime-ratio-common-coefficient}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0013

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:31`
- Строки: `31--35`

```latex
\begin{equation}
 \Tr_{\mathcal K_E}(\partial_\mu\Phi_Z)^2
 =2\sum_e\left[(\partial_\mu x_e)^2+(\partial_\mu y_e)^2\right].
 \label{eq:v7-spacetime-ratio-kinetic-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0014

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 \Tr_{\mathcal K_E}\mathfrak m_\mu^2
 =2\mathcal S_\mu+10\mu^4.
 \label{eq:v7-spacetime-ratio-potential-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0015

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:43`
- Строки: `43--48`

```latex
\begin{equation}
 Z=4C_0a^2,
 \qquad
 \kappa=2C_0a^4.
 \label{eq:v7-spacetime-ratio-induced-coefficients}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0016

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:53`
- Строки: `53--58`

```latex
\begin{equation}
 \boxed{
 \lambda_E=\frac{\kappa}{Z^2}
 =\frac1{8C_0}=\frac{\pi^2}{f_0}.}
 \label{eq:v7-spacetime-ratio-effective-quartic}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0017

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:61`
- Строки: `61--65`

```latex
\begin{equation}
 M_0^2=\frac{\kappa\mu^2}{Z}
 =\frac{a^2\mu^2}{2},
 \label{eq:v7-spacetime-ratio-mass-scale}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0018

- Источник: `s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex:81`
- Строки: `81--86`

```latex
\begin{equation}
 f_0\in\left\{\frac12,1,2,5\right\}
 \quad\Longrightarrow\quad
 \lambda_E\in\left\{2\pi^2,\pi^2,\frac{\pi^2}{2},\frac{\pi^2}{5}\right\}.
 \label{eq:v7-spacetime-ratio-f0-family}
\end{equation}
```

## `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-52-0019

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:14`
- Строки: `14--20`

```latex
\begin{equation}
 a=z_{u_RX_L}\in\overline{\mathbf3},\qquad
 b=z_{Y_RQ_L}\in\mathbf3,
 \qquad
 p=z_{X_Le_R},\qquad q=z_{L_LY_R}.
 \label{eq:v7-virtual-bridge-fields}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0020

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:24`
- Строки: `24--33`

```latex
\begin{equation}
 K(pq)=
 \begin{pmatrix}
  M_a^2&-\kappa\overline{pq}\\
  -\kappa pq&M_b^2
 \end{pmatrix},
 \qquad
 \Delta(pq)=\det K=M_a^2M_b^2-\kappa^2|pq|^2.
 \label{eq:v7-virtual-bridge-heavy-block}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0021

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 \Delta(pq)>0.
 \label{eq:v7-virtual-bridge-positive-domain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0022

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:45`
- Строки: `45--48`

```latex
\begin{equation}
 a=b=0.
 \label{eq:v7-virtual-bridge-tree-solution}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0023

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:59`
- Строки: `59--63`

```latex
\begin{equation}
 \Gamma_{0}(p,q)
 =3\log\Delta(pq)+\mathrm{const}.
 \label{eq:v7-virtual-bridge-zero-mode-logdet}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0024

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:65`
- Строки: `65--71`

```latex
\begin{equation}
 \Gamma_{0}(p,q)
 =3\log(M_a^2M_b^2)
 -\frac{3\kappa^2}{M_a^2M_b^2}|pq|^2
 +O(|pq|^4).
 \label{eq:v7-virtual-bridge-quartic-expansion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0025

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 \Hess_{p=q=0}\Gamma_0=0.
 \label{eq:v7-virtual-bridge-zero-light-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0026

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:82`
- Строки: `82--87`

```latex
\begin{equation}
 \lambda_{\pm}
 =\frac12\left[M_a^2+M_b^2
 \pm\sqrt{(M_a^2-M_b^2)^2+4\kappa^2|pq|^2}\right]
 \label{eq:v7-virtual-bridge-heavy-eigenvalues}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0027

- Источник: `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex:97`
- Строки: `97--103`

```latex
\begin{equation}
 \Gamma_{4}^{(1)}
 =-3\kappa^2|pq|^2
 \int\frac{d^4k}{(2\pi)^4}
 \frac{1}{(k^2+M_a^2)(k^2+M_b^2)}.
 \label{eq:v7-virtual-bridge-four-dimensional-term}
\end{equation}
```

## `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-52-0028

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:10`
- Строки: `10--17`

```latex
\begin{equation}
 \mathcal E_{
m heavy}^{\mathbb R}
 =\mathcal E_d^{\mathbb R}\oplus\mathcal E_W^{\mathbb R},
 \qquad \dim_{\mathbb R}\mathcal E_d=12,
 \quad \dim_{\mathbb R}\mathcal E_W=8.
 \label{eq:v7-weak-competition-heavy-split}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0029

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 S_t(\Phi)=\Tr e^{-t\Phi^2},\qquad t>0.
 \label{eq:v7-weak-competition-exact-gaussian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0030

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:29`
- Строки: `29--36`

```latex
\begin{equation}
 (H_t)_{ab}=\sum_{i,j}g_t(\lambda_i,\lambda_j)
 (E_a')_{ij}(E_b')_{ji},
 \qquad
 g_t(x,y)=\frac{f_t'(x)-f_t'(y)}{x-y},
 \quad f_t(x)=e^{-tx^2},
 \label{eq:v7-weak-competition-divided-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0031

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 H_t=H_d(t)\oplus H_W(t).
 \label{eq:v7-weak-competition-block-split}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0032

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:46`
- Строки: `46--51`

```latex
\begin{align}
 \Spec H_d(1)&=\{0.041312^{\times6},\ 0.736618^{\times6}\},\nonumber\\
 \Spec H_W(1)&=\{-1.280223^{\times2},-1.004339,-0.558141,
 -0.265457^{\times2},-0.093662^{\times2}\}.
 \label{eq:v7-weak-competition-t-one-spectrum}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0033

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 10^{-4}\le t\le10^2
 \label{eq:v7-weak-competition-scan-domain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-52-0034

- Источник: `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex:69`
- Строки: `69--73`

```latex
\begin{equation}
 (-4.414553,-4.414553,-0.549001,-0.635003,
  -0.866155,-0.093662,-1.407496),
 \label{eq:v7-weak-competition-root-tadpoles}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]