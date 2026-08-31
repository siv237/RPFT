# Гейты Version 7, продолжение — часть 50

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **110** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0001

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:8`
- Строки: `8--11`

```latex
\begin{equation}
 C=(Q_L,u_R,X_L,e_R,L_L,Y_R,Q_L).
 \label{eq:v7-cycle-moment-cycle}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0002

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:19`
- Строки: `19--24`

```latex
\begin{equation}
 D_{vw}=a_{vw}U_{vw},\qquad
 D_{wv}=a_{vw}U_{vw}^\dagger,\qquad
 a_{vw}=\begin{cases}1,&vw\in E_0,\\r,&vw\in E_*,\end{cases}
 \label{eq:v7-cycle-moment-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0003

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:30`
- Строки: `30--34`

```latex
\begin{align}
 \Tr D^2&=18(2r^2+1),\nonumber\\
 \Tr D^4&=6(18r^4+10r^2+5),
 \label{eq:v7-cycle-moment-low-traces}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0004

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:36`
- Строки: `36--41`

```latex
\begin{equation}
 \Tr D^6
 =54+144r^2+306r^4+324r^6
 +12r^4\Re\Tr W_C.
 \label{eq:v7-cycle-moment-sixth-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0005

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:43`
- Строки: `43--47`

```latex
\begin{equation}
 \Tr D^6\big|_{W_C=I_3}
 =18(18r^6+19r^4+8r^2+3).
 \label{eq:v7-cycle-moment-sixth-trivial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0006

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 k_{\min}^{\rm hol}=6,\qquad
 \Delta\Tr D^6=12r^4(\Re\Tr W_C-3).
 \label{eq:v7-cycle-moment-first-sensitive-degree}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0007

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:64`
- Строки: `64--67`

```latex
\begin{equation}
 V_6(W_C)=12c_6r^4\Re\Tr W_C.
 \label{eq:v7-cycle-moment-holonomy-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0008

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:69`
- Строки: `69--77`

```latex
\begin{equation}
 W_C^*=\begin{cases}
 I_3,&c_6<0,\\
 -I_3,&c_6>0,
 \end{cases}
 \qquad
 c_6=0:\quad W_C\ \text{не виден}.
 \label{eq:v7-cycle-moment-central-minima}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0009

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 \Hess V_6\big|_{W_C^*}=12|c_6|r^4I_9,
 \qquad (n_-,n_0,n_+)=(0,0,9).
 \label{eq:v7-cycle-moment-holonomy-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0010

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:93`
- Строки: `93--97`

```latex
\begin{equation}
 \mathcal S_{246}(r,W_C)
 =c_2\Tr D^2+c_4\Tr D^4+c_6\Tr D^6.
 \label{eq:v7-cycle-moment-spectral-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0011

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:99`
- Строки: `99--103`

```latex
\begin{equation}
 \mathcal S_{246}(r)=\mathcal S_{246}(0)
 +ar^2+br^4+cr^6,
 \label{eq:v7-cycle-moment-radial-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0012

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:105`
- Строки: `105--110`

```latex
\begin{equation}
 a=36c_2+60c_4+144c_6,\qquad
 b=108c_4+270c_6,\qquad
 c=324c_6.
 \label{eq:v7-cycle-moment-radial-coefficients}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0013

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:112`
- Строки: `112--115`

```latex
\begin{equation}
 a+2br^2+3cr^4=0.
 \label{eq:v7-cycle-moment-scale-equation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0014

- Источник: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:123`
- Строки: `123--126`

```latex
\begin{equation}
 a>0,\qquad b>0,\qquad c\ge0,\qquad r_*=0,
 \label{eq:v7-cycle-moment-positive-profile-origin}
\end{equation}
```

## `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0015

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:9`
- Строки: `9--14`

```latex
\begin{equation}
 \mathcal S_V(A)=\frac12\left(
 \|A^*A-A_0^*A_0\|_{\rm HS}^2+
 \|AA^*-A_0A_0^*\|_{\rm HS}^2\right).
 \label{eq:v7-relative-norm-vertex-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0016

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:18`
- Строки: `18--24`

```latex
\begin{equation}
 \mathcal S_E=
 \sum_{a=1}^7m_a(|z_a|^2-1)^2
 +\sum_{j\in d}\bigl[(|w_j|^2+8/5)^2-(8/5)^2\bigr]
 +\sum_{j\in W}\bigl[(|w_j|^2+9/10)^2-(9/10)^2\bigr],
 \label{eq:v7-relative-norm-edge-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0017

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:26`
- Строки: `26--30`

```latex
\begin{equation}
 \mathcal S_\beta=\mathcal S_E+\beta\mathcal S_V,
 \qquad \beta\ge0.
 \label{eq:v7-relative-norm-combined-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0018

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:37`
- Строки: `37--40`

```latex
\begin{equation}
 0\le\beta<\frac8{15}.
 \label{eq:v7-relative-norm-beta-window}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0019

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:42`
- Строки: `42--46`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{0}=(7,0,20),
 \qquad \lambda_{\rm heavy}^{\min}=0.4.
 \label{eq:v7-relative-norm-origin-signature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0020

- Источник: `s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex:55`
- Строки: `55--59`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{*}=(0,0,27),
 \qquad \lambda_{\min}=5.6.
 \label{eq:v7-relative-norm-vacuum-signature}
\end{equation}
```

## `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0021

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 h_e(t)=8tc_e e^{-tc_e^2},\qquad t>0.
 \label{eq:v7-exact-unification-hodge-mass}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0022

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 c_d=\frac85,\qquad c_W=\frac9{10}.
 \label{eq:v7-exact-unification-casimir-values}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0023

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:29`
- Строки: `29--34`

```latex
\begin{equation}
 \mathcal S_t^{\rm gr}
 =-\Tr_{\rm edge}e^{-t\mathfrak m_C^2}
  +\Tr_{\rm phys}e^{-t\Phi^2}.
 \label{eq:v7-exact-unification-graded-profile}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0024

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 H_{\rm tot}(t)=H_{\rm phys}(t)
 +\operatorname{diag}\bigl(h_e(t)\bigr).
 \label{eq:v7-exact-unification-total-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0025

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:49`
- Строки: `49--53`

```latex
\begin{equation}
 \lambda_{\min}H_{\rm tot}(1)=1.03081235398>0,
 \qquad (n_-,n_0,n_+)=(0,0,20).
 \label{eq:v7-exact-unification-benchmark}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0026

- Источник: `s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 0<t<t_*\quad\Longrightarrow\quad H_{\rm tot}(t)>0,
 \qquad t_*\simeq2.36617,
 \label{eq:v7-exact-unification-positive-window}
\end{equation}
```

## `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0027

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:9`
- Строки: `9--12`

```latex
\begin{equation}
 R_e=(d_3,d_2)_{Y_e}
 \label{eq:v7-full-edge-representation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0028

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:14`
- Строки: `14--19`

```latex
\begin{equation}
 I_1(e)=d_3d_2Y_e^2,qquad
 I_2(e)=d_3T_2(R_e),qquad
 I_3(e)=d_2T_3(R_e),
 \label{eq:v7-full-edge-indices}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0029

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:25`
- Строки: `25--41`

```latex
\begin{equation}
\begin{array}{c|c|c}
e&R_e&\text{статус}\\ \hline
L_LY_R&(1,1)_0&*\\
Q_LY_R&(3,1)_{2/3}&*\\
X_LX_R&(1,1)_0&*\\
X_Le_R&(1,1)_0&*\\
X_Lu_R&(3,1)_{5/3}&*\\
Y_LY_R&(1,1)_0&*\\ \hline
L_LX_R&(1,2)_{1/2}&+\\
X_LY_R&(1,2)_{1/2}&+\\
X_Ld_R&(3,1)_{2/3}&+\\
Y_LX_R&(1,2)_{1/2}&+\\
Y_Le_R&(1,2)_{1/2}&+
\end{array}
 \label{eq:v7-full-edge-multiplet-table}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0030

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:51`
- Строки: `51--57`

```latex
\begin{equation}
 \mathcal S_{\rm full}(\phi)
 =\sum_{e\in E_*}w_e(\|\phi_e\|^2-\mu^2)^2
 +\sum_{e\notin E_*}w_e
 (\|\phi_e\|^4+2\mu^2\|\phi_e\|^2).
 \label{eq:v7-full-edge-weighted-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0031

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:59`
- Строки: `59--63`

```latex
\begin{equation}
 \|\phi_e\|=\mu\quad(e\in E_*),qquad
 \phi_e=0\quad(e\notin E_*).
 \label{eq:v7-full-edge-weighted-vacuum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0032

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:68`
- Строки: `68--71`

```latex
\begin{equation}
 d_* =10,qquad d_+=11.
 \label{eq:v7-full-edge-dimensions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0033

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:73`
- Строки: `73--77`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{0}=(20,0,22),qquad
 (n_-,n_0,n_+)_{*}=(0,14,28).
 \label{eq:v7-full-edge-hessian-signatures}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0034

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:84`
- Строки: `84--88`

```latex
\begin{equation}
 \phi_{Q_LY_R}\in(3,1)_{2/3},qquad
 \phi_{X_Lu_R}\in(3,1)_{5/3}.
 \label{eq:v7-full-edge-selected-colored-fields}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0035

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:91`
- Строки: `91--94`

```latex
\begin{equation}
 (\mathbb C^3)^{SU(3)}=\{0\}.
 \label{eq:v7-full-edge-no-color-invariant-vector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0036

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:101`
- Строки: `101--107`

```latex
\begin{equation}
 (I_1,I_2,I_3)_{E_*}
 =\left(\frac{29}{3},0,1\right),qquad
 (I_1,I_2,I_3)_{E\setminus E_*}
 =\left(\frac{10}{3},2,\frac12\right).
 \label{eq:v7-full-edge-sector-indices}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0037

- Источник: `s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex:109`
- Строки: `109--112`

```latex
\begin{equation}
 (I_1,I_2,I_3)_{E}=\left(13,2,\frac32\right),
 \label{eq:v7-full-edge-total-indices}
\end{equation}
```

## `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0038

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:9`
- Строки: `9--14`

```latex
\begin{equation}
 H=\begin{pmatrix}0\\1\end{pmatrix},\qquad
 \widetilde H=i\sigma_2\overline H
 =\begin{pmatrix}1\\0\end{pmatrix}.
 \label{eq:v7-full-a6-higgs-frame}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0039

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 \boxed{\widetilde H^\dagger H=0.}
 \label{eq:v7-full-a6-up-overlap-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0040

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:32`
- Строки: `32--37`

```latex
\begin{equation}
 \Tr\Phi_u^6
 =50+24x^2+42y^2+12x^4+24y^4
 +6x^2y^2+2x^6+4y^6.
 \label{eq:v7-full-a6-up-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0041

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 [xy]\Tr\Phi_u^6=0.
 \label{eq:v7-full-a6-up-mixed-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0042

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:54`
- Строки: `54--62`

```latex
\begin{equation}
\begin{array}{c|c|c}
\text{ветвь}&\text{два нулевых ребра}&\text{слабый множитель}\\ \hline
u&(Q_LY_R,X_Lu_R)&\widetilde H^\dagger H=0\\
d&(Q_LY_R,X_Ld_R)&H^\dagger H=1\\
W&(L_LX_R,Y_Le_R)&\langle\ell,y\rangle
\end{array}
 \label{eq:v7-full-a6-three-quadratic-cycles}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0043

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:68`
- Строки: `68--73`

```latex
\begin{equation}
 \Tr\Phi_d^6
 =50+24x^2+42y^2+12xy+12x^4+24y^4
 +6x^2y^2+2x^6+4y^6,
 \label{eq:v7-full-a6-down-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0044

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:75`
- Строки: `75--78`

```latex
\begin{equation}
 [xy]\Tr\Phi_d^6=12.
 \label{eq:v7-full-a6-down-mixed}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0045

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 \Tr\Phi_W^6
 =48+30(x^2+y^2)+12xy+12(x^4+y^4)+2(x^6+y^6),
 \label{eq:v7-full-a6-weak-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0046

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 -\frac16\Tr\Phi^6.
 \label{eq:v7-full-a6-gaussian-factor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0047

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:97`
- Строки: `97--100`

```latex
\begin{equation}
 0,\qquad -2xy,\qquad -2xy.
 \label{eq:v7-full-a6-gaussian-mixed-terms}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0048

- Источник: `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex:105`
- Строки: `105--112`

```latex
\begin{align}
 H_u&=\begin{pmatrix}48&0\\0&84\end{pmatrix},\nonumber\\
 H_d&=\begin{pmatrix}48&12\\12&84\end{pmatrix},\qquad
 \Spec H_d=\{66-6\sqrt{13},66+6\sqrt{13}\},\nonumber\\
 H_W&=\begin{pmatrix}60&12\\12&60\end{pmatrix},\qquad
 \Spec H_W=\{48,72\}.
 \label{eq:v7-full-a6-heavy-hessians}
\end{align}
```

## `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0049

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:9`
- Строки: `9--14`

```latex
\begin{equation}
 W_C=V\operatorname{diag}(e^{i\theta_1},e^{i\theta_2},e^{i\theta_3})V^\dagger,
 \qquad
 D(r,W_C)\simeq\bigoplus_{j=1}^3D(r,e^{i\theta_j}).
 \label{eq:v7-higher-character-direct-sum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0050

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:20`
- Строки: `20--27`

```latex
\begin{equation}
 \Tr D^{2n}
 =A_{2n}(r)+
 \sum_{m=1}^{\lfloor n/3\rfloor}
 a_{2n,m}(r)\Re\Tr W_C^m,
 \qquad a_{2n,m}(r)\in\mathbb Z_{\ge0}[r].
 \label{eq:v7-higher-character-general-expansion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0051

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:30`
- Строки: `30--34`

```latex
\begin{equation}
 k_{\min}(m)=6m,
 \qquad m=1,2,3,4,5.
 \label{eq:v7-higher-character-first-degree}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0052

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:43`
- Строки: `43--46`

```latex
\begin{equation}
 [\Tr D^6]_{\rm hol}=12r^4\chi_1(W_C),
 \label{eq:v7-higher-character-six}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0053

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 [\Tr D^8]_{\rm hol}=(48r^4+96r^6)\chi_1(W_C),
 \label{eq:v7-higher-character-eight}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0054

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 [\Tr D^{10}]_{\rm hol}
 =(140r^4+460r^6+540r^8)\chi_1(W_C).
 \label{eq:v7-higher-character-ten}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0055

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:57`
- Строки: `57--63`

```latex
\begin{align}
 [\Tr D^{12}]_{\rm hol}
 ={}&(360r^4+1560r^6+3072r^8+2592r^{10})\chi_1(W_C)
 \nonumber\\
 &+12r^8\chi_2(W_C).
 \label{eq:v7-higher-character-twelve}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0056

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:66`
- Строки: `66--69`

```latex
\begin{equation}
 [\chi_3]\Tr D^{18}=12r^{12}.
 \label{eq:v7-higher-character-eighteen-third}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0057

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:75`
- Строки: `75--81`

```latex
\begin{equation}
 \theta_{2n}^*(r)=\pi,
 \qquad
 2n=6,8,\ldots,30,
 \qquad 0.05\le r\le20,
 \label{eq:v7-higher-character-individual-minima}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0058

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:90`
- Строки: `90--93`

```latex
\begin{equation}
 V_{12}(W_C)=a\Re\Tr W_C+b\Re\Tr W_C^2.
 \label{eq:v7-higher-character-two-harmonic-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0059

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:95`
- Строки: `95--98`

```latex
\begin{equation}
 \sin\theta\,(a+4b\cos\theta)=0.
 \label{eq:v7-higher-character-stationarity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0060

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:100`
- Строки: `100--106`

```latex
\begin{equation}
 b>0,
 \qquad |a|<4b,
 \qquad
 \cos\theta_*=-\frac{a}{4b}.
 \label{eq:v7-higher-character-interior-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0061

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:108`
- Строки: `108--114`

```latex
\begin{equation}
 a=12c_6+7584c_{12},
 \qquad b=12c_{12},
 \qquad
 -636<\frac{c_6}{c_{12}}<-628.
 \label{eq:v7-higher-character-tuned-ratio}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0062

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:123`
- Строки: `123--126`

```latex
\begin{equation}
 \mathcal S_f(W_C)=\sum_{j=1}^3F_f(\theta_j),
 \label{eq:v7-higher-character-separable-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0063

- Источник: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:128`
- Строки: `128--132`

```latex
\begin{equation}
 \mathcal S_f(UW_CU^\dagger)=\mathcal S_f(W_C)
 \qquad\text{для всех }U\in U(3).
 \label{eq:v7-higher-character-conjugation-invariance}
\end{equation}
```

## `s2t/gates/version7_hodge_level_background_attribution_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0064

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:7`
- Строки: `7--11`

```latex
\begin{equation}
 \mathfrak m_\mu(Z)
 =[d_Z,d_Z^\dagger]-\mu^2\widehat\Gamma_E.
 \label{eq:v7-background-level-moment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0065

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:19`
- Строки: `19--26`

```latex
\begin{equation}
 d_{15}=d_u\oplus d_d\oplus d_e,
 \qquad
 K_{15}=[d_{15},d_{15}^\dagger],
 \qquad
 \chi_{15}=\operatorname{diag}(-I_3,I_3).
 \label{eq:v7-background-level-typed-complex}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0066

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:29`
- Строки: `29--34`

```latex
\begin{equation}
 k_a(K_{15})
 =\frac12\Tr\!\left(\chi_{15}\Pi_aK_{15}\Pi_a\right)
 =\Tr(Y_a^\dagger Y_a)\ge0.
 \label{eq:v7-background-level-edge-energies}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0067

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \Psi_c(K_{15})
 =\left(c_uk_u+c_dk_d+c_ek_e\right)\widehat\Gamma_E,
 \qquad c=(c_u,c_d,c_e)\in\mathbb R^3.
 \label{eq:v7-background-level-map-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0068

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 \{u\},\qquad\{d\},\qquad\{e\}.
 \label{eq:v7-background-level-exact-orbits}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0069

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:61`
- Строки: `61--64`

```latex
\begin{equation}
 \{u,d\},\qquad\{e\},
 \label{eq:v7-background-level-coarse-orbits}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0070

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:83`
- Строки: `83--88`

```latex
\begin{equation}
 (k_u,k_d,k_e)=(1,1,1),
 \qquad
 \Tr D_{H_{15}}^2=6.
 \label{eq:v7-background-level-unit-background}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0071

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:90`
- Строки: `90--97`

```latex
\begin{equation}
 \frac1{9}\Tr D_{H_{15}}^2=\frac23,
 \qquad
 \frac1{5}\Tr_{\rm active}D_{H_{15}}^2=\frac65,
 \qquad
 \frac1{2|E_0|}\Tr D_{H_{15}}^2=1.
 \label{eq:v7-background-level-trace-ambiguity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0072

- Источник: `s2t/gates/version7_hodge_level_background_attribution_gate.tex:102`
- Строки: `102--105`

```latex
\begin{equation}
 (k_u,k_d,k_e)=(1,4,9)
 \label{eq:v7-background-level-unequal-example}
\end{equation}
```

## `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0073

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:10`
- Строки: `10--15`

```latex
\begin{equation}
 \lambda_{\rm extra}=-\frac25,
 \qquad
 v_{\rm extra}=\operatorname{Im}(L_LX_R)_{w=1}.
 \label{eq:v7-transfer-extra-source-mode}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0074

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:28`
- Строки: `28--32`

```latex
\begin{equation}
 A_0:\mathbb C^{11}\longrightarrow\mathbb C^{10},
 \qquad \rank A_0=10.
 \label{eq:v7-transfer-reference-rank}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0075

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:34`
- Строки: `34--42`

```latex
\begin{equation}
 U=A_0(A_0^*A_0)^{-1/2}_{\operatorname{supp}},
 \qquad
 UU^*=I_{10},
 \qquad
 P=U^*U,
 \qquad Q=I_{11}-P.
 \label{eq:v7-transfer-polar-coisometry}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0076

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:44`
- Строки: `44--50`

```latex
\begin{equation}
 \rank P=10,
 \qquad \rank Q=1,
 \qquad
 21=10_{\rm source\ support}+10_{\rm target}+1_{\rm defect}.
 \label{eq:v7-transfer-index-decomposition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0077

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:56`
- Строки: `56--61`

```latex
\begin{equation}
 C_s(A)=A^*A-A_0^*A_0,
 \qquad
 C_t(A)=AA^*-A_0A_0^*.
 \label{eq:v7-transfer-two-gram-curvatures}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0078

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:66`
- Строки: `66--70`

```latex
\begin{equation}
 T_U(X,Y)=\frac12\left(UXU^*+Y\right):
 M_{11}(\mathbb C)\oplus M_{10}(\mathbb C)\longrightarrow M_{10}(\mathbb C).
 \label{eq:v7-transfer-ucp-channel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0079

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:75`
- Строки: `75--79`

```latex
\begin{equation}
 \mathcal S_{\rm quot}(A)
 =\frac12\left\|T_U(C_s(A),C_t(A))\right\|_{\rm HS}^2.
 \label{eq:v7-transfer-quotient-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0080

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 \Hess_0\mathcal S_{\rm quot}
 =\frac12\Hess_0\mathcal S_V.
 \label{eq:v7-transfer-half-hessian-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0081

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:91`
- Строки: `91--100`

```latex
\begin{align}
 \operatorname{sig}\Hess_0\mathcal S_{\rm tot}^{\rm quot}
  &=(7,0,20),
 &\lambda_{\rm heavy}^{\min}&=\frac25,
 \label{eq:v7-transfer-quotient-origin-pass}\\
 \operatorname{sig}\Hess_{A_0}\mathcal S_{\rm tot}^{\rm quot}
  &=(0,0,27),
 &\lambda_{\rm vac}^{\min}&=4.5827630148\ldots.
 \label{eq:v7-transfer-quotient-vacuum-pass}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0082

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:108`
- Строки: `108--114`

```latex
\begin{equation}
 E_U(X\oplus Y)
 =\left(U^*ZU+\Tr(QXQ)Q\right)\oplus Z,
 \qquad
 Z=T_U(X,Y).
 \label{eq:v7-transfer-trace-preserving-expectation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0083

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:119`
- Строки: `119--123`

```latex
\begin{equation}
 \Hess_0\frac12\|E_U(C_s\oplus C_t)\|_{\rm HS}^2
 =2\Hess_0\mathcal S_{\rm quot}.
 \label{eq:v7-transfer-expectation-double-count}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0084

- Источник: `s2t/gates/version7_incidence_transfer_markov_weight_gate.tex:126`
- Строки: `126--129`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{E_U}=(21,0,6).
 \label{eq:v7-transfer-expectation-no-go}
\end{equation}
```

## `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0085

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:7`
- Строки: `7--12`

```latex
\begin{equation}
 Z=T_U(C_s,C_t)=\frac12(UC_sU^*+C_t),
 \qquad
 \mathcal S_{\rm raw}=\frac12\|Z\|_{\rm HS}^2.
 \label{eq:v7-reduced-raw-quotient-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0086

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:15`
- Строки: `15--19`

```latex
\begin{equation}
 \mathcal S_V
 =\frac12\left(\|C_s\|_{\rm HS}^2+\|C_t\|_{\rm HS}^2\right).
 \label{eq:v7-reduced-original-two-corner-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0087

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:22`
- Строки: `22--29`

```latex
\begin{equation}
 X=UP C_sPU^*,
 \qquad Y=C_t,
 \qquad
 Z=\frac{X+Y}{2},
 \qquad D=\frac{X-Y}{2}.
 \label{eq:v7-reduced-symmetric-antisymmetric-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0088

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:31`
- Строки: `31--35`

```latex
\begin{equation}
 \frac12\left(\|X\|_{\rm HS}^2+\|Y\|_{\rm HS}^2\right)
 =\|Z\|_{\rm HS}^2+\|D\|_{\rm HS}^2.
 \label{eq:v7-reduced-parallelogram-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0089

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 U(A_0^*A_0)U^*=A_0A_0^*.
 \label{eq:v7-reduced-background-intertwining}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0090

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:49`
- Строки: `49--53`

```latex
\begin{equation}
 \Hess_0\|Z\|_{\rm HS}^2
 =\Hess_0\mathcal S_V.
 \label{eq:v7-reduced-inherited-hessian-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0091

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:56`
- Строки: `56--59`

```latex
\begin{equation}
 \mathcal S_c=\mathcal S_E+\frac c2\|Z\|_{\rm HS}^2.
 \label{eq:v7-reduced-metric-scale-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0092

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:61`
- Строки: `61--64`

```latex
\begin{equation}
 0\le c<\frac{16}{15}.
 \label{eq:v7-reduced-metric-scale-window}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0093

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:67`
- Строки: `67--74`

```latex
\begin{align}
 c=1:&\quad (n_-,n_0,n_+)=(7,0,20),
 &\lambda_{\rm heavy}^{\min}&=\frac25,
 \label{eq:v7-reduced-raw-pass}\\
 c=2:&\quad (n_-,n_0,n_+)=(21,0,6),
 &\lambda_{\rm heavy}^{\min}&=-\frac{28}{5}.
 \label{eq:v7-reduced-inherited-fail}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0094

- Источник: `s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex:105`
- Строки: `105--108`

```latex
\begin{equation}
 \delta A=\xi_tA-A\xi_s
 \label{eq:v7-reduced-gauge-variation}
\end{equation}
```

## `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-50-0095

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 (d_A^2)_{20}=B_1B_0=\mathcal R_U,
 \label{eq:v7-degree-two-endpoint-block}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0096

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:24`
- Строки: `24--27`

```latex
\begin{equation}
 \mathcal A_{\rm node}=\mathbb C^3
 \label{eq:v7-degree-two-node-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0097

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:29`
- Строки: `29--34`

```latex
\begin{equation}
 H_0=\mathbb C^{11},\qquad
 H_1=\mathbb C^{21},\qquad
 H_2=\mathbb C^{10}.
 \label{eq:v7-degree-two-node-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0098

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:39`
- Строки: `39--43`

```latex
\begin{align}
 \pi_D(e_i\,de_j)&=e_i[Q_A,e_j],\nonumber\\
 \pi_D(e_i\,de_j\,de_k)&=e_i[Q_A,e_j][Q_A,e_k],
 \label{eq:v7-degree-two-represented-forms}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0099

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:45`
- Строки: `45--48`

```latex
\begin{equation}
 J_D^2=\pi_D\!\left(d\ker\pi_D|_{\Omega^1}\right).
 \label{eq:v7-degree-two-junk}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0100

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:51`
- Строки: `51--56`

```latex
\begin{equation}
 \rank\pi_D(\Omega^1)=4,\qquad
 \rank\pi_D(\Omega^2)=6,\qquad
 \rank J_D^2=2,
 \label{eq:v7-degree-two-ranks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0101

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 \rank\Omega_D^2=4.
 \label{eq:v7-degree-two-quotient-rank}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0102

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:75`
- Строки: `75--78`

```latex
\begin{equation}
 N=\operatorname{diag}(0\cdot I_{11},1\cdot I_{21},2\cdot I_{10}).
 \label{eq:v7-degree-two-number-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0103

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:84`
- Строки: `84--87`

```latex
\begin{equation}
 F_A=Q_A^2-Q_{A_0}^2
 \label{eq:v7-degree-two-full-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0104

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:89`
- Строки: `89--92`

```latex
\begin{equation}
 \delta_N(F_A)=\frac12[N,F_A].
 \label{eq:v7-degree-two-relative-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0105

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:95`
- Строки: `95--103`

```latex
\begin{equation}
 \delta_N(F_A)=
 \begin{pmatrix}
 0&0&-\mathcal R_U^*\\
 0&0&0\\
 \mathcal R_U&0&0
 \end{pmatrix}.
 \label{eq:v7-degree-two-relative-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0106

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:105`
- Строки: `105--109`

```latex
\begin{equation}
 \|\delta_N(F_A)\|_{\rm HS}^2
 =2\|\mathcal R_U(A)\|_{\rm HS}^2.
 \label{eq:v7-degree-two-relative-norm}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0107

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:117`
- Строки: `117--120`

```latex
\begin{equation}
 \delta_N(gF_Ag^*)=g\,\delta_N(F_A)\,g^*.
 \label{eq:v7-degree-two-covariance}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0108

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:125`
- Строки: `125--129`

```latex
\begin{equation}
 \|\delta_{2I-N}(F_A)\|_{\rm HS}
 =\|\delta_N(F_A)\|_{\rm HS}.
 \label{eq:v7-degree-two-orientation-independence}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0109

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:136`
- Строки: `136--142`

```latex
\begin{equation}
 \mathcal S_{\rm rel}
 =\mathcal S_E+\frac14
 \|\delta_N(Q_A^2-Q_{A_0}^2)\|_{\rm HS}^2
 =\mathcal S_E+\frac12\|\mathcal R_U(A)\|_{\rm HS}^2.
 \label{eq:v7-degree-two-relative-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-50-0110

- Источник: `s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex:148`
- Строки: `148--155`

```latex
\begin{align}
 (n_-,n_0,n_+)_{0}&=(7,0,20),
 &\lambda_{\rm heavy}^{\min}&=\frac{18}{5},
 \label{eq:v7-degree-two-origin-signature}\\
 (n_-,n_0,n_+)_{A_0}&=(0,0,27),
 &\lambda_{\min}&=3.9368554658\ldots.
 \label{eq:v7-degree-two-vacuum-signature}
\end{align}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]