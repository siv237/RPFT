# Гейты Version 6, часть 9

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **115** блочных формул из **13** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0001

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:24`
- Строки: `24--26`

```latex
\begin{equation}
 T=1.5744530783,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0002

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:31`
- Строки: `31--37`

```latex
\begin{equation}
 I_2=0.5174619005,
 \qquad
 I_4=0.4366199900,
 \qquad
 I_6=0.7206475643.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0003

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 w=\sqrt{I_2/T}=0.5732899499.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0004

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
 S_0=-T\int d^2\sigma\,\sqrt{-\gamma}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0005

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:68`
- Строки: `68--72`

```latex
\begin{equation}
 E_0(R)=2\pi T R,
 \qquad
 \frac{dE_0}{dR}=2\pi T=9.89258045>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0006

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:77`
- Строки: `77--81`

```latex
\begin{equation}
 E_0=17.01395,
 \qquad 28.35658,
 \qquad 56.71317.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0007

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:88`
- Строки: `88--91`

```latex
\begin{equation}
 E(R)=2\pi T R
 \left[1+c_4\left(\frac wR\right)^4+\cdots\right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0008

- Источник: `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex:93`
- Строки: `93--95`

```latex
\begin{equation}
 \frac{R_*}{w}=3^{1/4}=1.31607,
\end{equation}
```

## `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0009

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:30`
- Строки: `30--36`

```latex
\begin{equation}
 Q=\Delta u(r)\left(P-\frac{I_3}{3}\right),
 \qquad
 P=\widehat x\widehat x^T,
 \qquad
 A_Q=u(r)^2[P,dP].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0010

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:38`
- Строки: `38--43`

```latex
\begin{equation}
 u(0)=0,
 \qquad
 u(\infty)=1.
 \label{eq:v6-bosonic-radial-boundary-conditions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0011

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:46`
- Строки: `46--55`

```latex
\begin{align}
 |D_QQ|^2
 &=\frac23\Delta^2u'^2
 +\frac{4\Delta^2u^2(1-u^2)^2}{r^2},\\
 |F_{A_Q}|^2
 &=\frac{16u^2u'^2}{r^2}
 +\frac{2u^4(u^2-2)^2}{r^4},\\
 V(u)&=\Delta^4(1-u^2)^2.
 \label{eq:v6-bosonic-radial-densities}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0012

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:61`
- Строки: `61--65`

```latex
\begin{equation}
 \mathcal E[u]=\int_0^\infty
 \left(A(r,u)u'^2+W(r,u)\right)dr,
 \label{eq:v6-bosonic-radial-functional}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0013

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:67`
- Строки: `67--72`

```latex
\begin{align}
 A(r,u)&=\frac23c_D\Delta^2r^2+16c_Fu^2,\\
 W(r,u)&=4c_D\Delta^2u^2(1-u^2)^2
 +\frac{2c_Fu^4(u^2-2)^2}{r^2}
 +c_V\Delta^4r^2(1-u^2)^2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0014

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 2A u''+2A_r u'+A_u u'^2-W_u=0.
 \label{eq:v6-bosonic-radial-euler-lagrange}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0015

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 E_F(50,\infty)=\frac{8\pi c_F}{50}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0016

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:87`
- Строки: `87--94`

```latex
\begin{align}
 r_{1/2}&=1.0394444805\ldots,\\
 E_D&=11.0306107926\ldots,\\
 E_F&=35.3958853096\ldots,\\
 E_V&=8.1217582001\ldots,\\
 E_{\rm exact}&=54.5482543023\ldots.
 \label{eq:v6-bosonic-exact-radial-energy}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0017

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:98`
- Строки: `98--100`

```latex
\begin{equation}
 E_{\rm old}=60.7698954459\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0018

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:106`
- Строки: `106--109`

```latex
\begin{equation}
 E_D-E_F+3E_V=0
 \label{eq:v6-bosonic-radial-virial-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0019

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:124`
- Строки: `124--132`

```latex
\begin{equation}
 (c_D,c_F,c_V)\in
 \left\{
 (1,1,1),
 (1/4,1,1),(4,1,1),
 (1,1/4,1),(1,4,1),
 (1,1,1/4),(1,1,4)
 \right\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0020

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:147`
- Строки: `147--152`

```latex
\begin{equation}
 \mathcal H_{\rm rad}\eta
 =-\frac{d}{dr}\left(2A\frac{d\eta}{dr}\right)
 +U_{\rm rad}(r)\eta,
 \label{eq:v6-bosonic-radial-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0021

- Источник: `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex:154`
- Строки: `154--158`

```latex
\begin{equation}
 U_{\rm rad}
 =A_{uu}u'^2+W_{uu}
 -2\frac{d}{dr}(A_u u').
\end{equation}
```

## `s2t/gates/version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0022

- Источник: `s2t/gates/version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate.tex:10`
- Строки: `10--13`

```latex
\begin{equation}
 H_{Ka}=-\frac{2Ca(1-K)}r,qquad
 H_{ab}=r\,\partial_a\partial_bV.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0023

- Источник: `s2t/gates/version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 1.51051387, 1.51049856, 1.51046835, 1.51044709, 1.51043666.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0024

- Источник: `s2t/gates/version6_bosonic_defect_q_tetrahedral_vortex_radial_stability_gate.tex:26`
- Строки: `26--29`

```latex
\begin{equation}
 \{1.51044,1.59558,1.70182,1.86176,
 2.07352,2.33631,2.64961,3.01290\}.
\end{equation}
```

## `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0025

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 [W,H_S+H_C]=0.
 \label{eq:v6-energy-preserving-clock-control}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0026

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 H_S=\varepsilon\operatorname{diag}(0,1,1).
 \label{eq:v6-uniaxial-qutrit-hamiltonian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0027

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:23`
- Строки: `23--28`

```latex
\begin{equation}
 \varepsilon_*
 =\frac1{\beta_c}\log\frac{2a_*}{1-a_*}
 =1.9664146236\ldots.
 \label{eq:v6-coexistence-gibbs-gap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0028

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
 H_C=\varepsilon_*\operatorname{diag}(0,1,2,3),
 \label{eq:v6-four-tick-energy-ladder}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0029

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:36`
- Строки: `36--39`

```latex
\begin{equation}
 \tau_* =\frac{\pi}{2\varepsilon_*}
 =0.7988123705\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0030

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 |g,n\rangle
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0031

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:55`
- Строки: `55--57`

```latex
\begin{equation}
 |e_1,n-1\rangle,qquad |e_2,n-1\rangle
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0032

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 \frac{p_n}{3},\qquad\frac{p_{n-1}}{3},\qquad\frac{p_{n-1}}{3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0033

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:68`
- Строки: `68--74`

```latex
\begin{equation}
 a_{\rm out}\leq
 \frac13\left[
 p_0+\max(p_1,p_0)+\max(p_2,p_1)+\max(p_3,p_2)
 \right].
 \label{eq:v6-four-clock-ground-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0034

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:77`
- Строки: `77--80`

```latex
\begin{equation}
 \boxed{a_{\rm out}\leq\frac23.}
 \label{eq:v6-four-clock-axis-ceiling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0035

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:89`
- Строки: `89--91`

```latex
\begin{equation}
 a_*=0.9121665963\ldots,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0036

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:93`
- Строки: `93--96`

```latex
\begin{equation}
 a_*-\frac23=0.2454999296\ldots.
 \label{eq:v6-four-clock-axis-deficit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0037

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:112`
- Строки: `112--114`

```latex
\begin{equation*}
 a_*=0.9121666\ldots,
\end{equation*}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0038

- Источник: `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex:121`
- Строки: `121--123`

```latex
\begin{equation}
 1,\quad i,\quad-1,\quad-i.
\end{equation}
```

## `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0039

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:16`
- Строки: `16--22`

```latex
\begin{equation}
 \mathcal S_{\rm br}(B)
 =\frac1{21}\left[
  \Tr(I_3-B^TB)^2+\Tr(I_3-BB^T)^2\right]
 =\frac2{21}\Tr(I_3-B^TB)^2.
 \label{eq:v6-matrix-bridge-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0040

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:27`
- Строки: `27--31`

```latex
\begin{equation}
 \mathcal S_{\rm br}
 =\frac2{21}\left(3-2\Tr X+\Tr X^2\right).
 \label{eq:v6-bridge-purity-sign}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0041

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 \Tr X^2\ge\frac{r^2}{3},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0042

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:48`
- Строки: `48--50`

```latex
\begin{equation}
 R=\frac13X.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0043

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 \boxed{
 \mathcal S_{\rm br}(R)
 =\frac67\left(\Tr R^2-\frac13\right)}.
 \label{eq:v6-bridge-positive-purity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0044

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:61`
- Строки: `61--63`

```latex
\begin{equation}
 \kappa_{\rm br}=-\frac67,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0045

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:67`
- Строки: `67--69`

```latex
\begin{equation}
 R_c=\frac23P+\frac16(I_3-P)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0046

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:71`
- Строки: `71--76`

```latex
\begin{equation}
 \mathcal S_{\rm br}(R_c)
 =\frac67\left(\frac12-\frac13\right)
 =\frac17.
 \label{eq:v6-critical-state-bridge-cost}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0047

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:86`
- Строки: `86--88`

```latex
\begin{equation}
 \kappa_{\rm eff}=\kappa_{\rm fluc}-\frac67.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0048

- Источник: `s2t/gates/version6_exchange_bridge_induced_alignment_gate.tex:90`
- Строки: `90--94`

```latex
\begin{equation}
 \kappa_{\rm fluc}>\log4+\frac67
 =2.243437218\ldots.
 \label{eq:v6-fluctuation-alignment-threshold}
\end{equation}
```

## `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0049

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 C=U\operatorname{diag}(s_1,s_2)V^T,
 \qquad U,V\in O(2),\qquad s_i\geq0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0050

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:18`
- Строки: `18--22`

```latex
\begin{equation}
 dC=\mathrm{const}\,
 |s_1^2-s_2^2|\,ds_1ds_2\,d\mu(U)d\mu(V).
 \label{eq:v6-real-m2-svd-measure}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0051

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 R=\frac{XX^T}{\Tr(XX^T)},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0052

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:54`
- Строки: `54--59`

```latex
\begin{equation}
 d\mu_K(R)\propto
 (\det R)^{(K-4)/2}\,dR,
 \qquad R>0,\qquad\Tr R=1.
 \label{eq:v6-real-induced-state-measure}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0053

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:61`
- Строки: `61--65`

```latex
\begin{equation}
 \mathcal F_{\rm meas}(R)=-\nu_K\log\det R,
 \qquad \nu_K=\frac{K-4}{2}.
 \label{eq:v6-induced-logdet-barrier}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0054

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:79`
- Строки: `79--82`

```latex
\begin{equation}
 -\nu\log\det R
 =\mathrm{const}+\frac{9\nu}{2}\Tr(\delta R)^2+O(\delta R^3).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0055

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:85`
- Строки: `85--90`

```latex
\begin{equation}
 -\frac{51}{112}+\frac{9\nu}{2}<0
 \quad\Longleftrightarrow\quad
 \nu<\frac{17}{168}.
 \label{eq:v6-logdet-instability-upper-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0056

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:98`
- Строки: `98--104`

```latex
\begin{equation}
 Z_{\rm br}(R_\varepsilon)
 \sim A\int^\infty\frac{dt}{t}e^{-c\varepsilon t^4}
 =\frac A4 E_1(c\varepsilon)
 \sim\frac A4\log\frac1\varepsilon.
 \label{eq:v6-nonperturbative-boundary-log}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0057

- Источник: `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex:113`
- Строки: `113--116`

```latex
\begin{equation}
 \boxed{0<\nu<\frac{17}{168}}.
 \label{eq:v6-admissible-fractional-barrier-window}
\end{equation}
```

## `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0058

- Источник: `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 a<\operatorname{reach}(X).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0059

- Источник: `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex:39`
- Строки: `39--44`

```latex
\begin{equation}
 K\pi a^2\leq \frac{\pi}{2\sqrt3}\ell^2,
 \qquad
 \frac a\ell\leq\frac{1}{\sqrt{2\sqrt3K}}.
 \label{eq:v6-single-thread-packing-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0060

- Источник: `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 \frac a\ell\leq1.1278\cdot10^{-4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0061

- Источник: `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex:72`
- Строки: `72--78`

```latex
\begin{equation}
 I_2(\delta)
 =\int_0^1\!\!\int_0^1
 \frac{ds\,dt}{(s-t)^2+\delta^2}
 =\frac{2}{\delta}\arctan\frac1\delta
 -\log\frac{1+\delta^2}{\delta^2},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0062

- Источник: `s2t/gates/version6_single_thread_excluded_volume_reconnection_barrier_gate.tex:80`
- Строки: `80--82`

```latex
\begin{equation}
 \delta I_2(\delta)\longrightarrow\pi.
\end{equation}
```

## `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0063

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:9`
- Строки: `9--12`

```latex
\begin{equation}
 \oint dX=\oint \dot X(s)\,ds=0.
 \label{eq:v6-single-thread-zero-total-tangent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0064

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:23`
- Строки: `23--25`

```latex
\begin{equation}
 K_a^+=K_a^-=K_a.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0065

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 K^+=K^-=(22696855,829548,829548,829548)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0066

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 M_{\rm Real}=50370998.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0067

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:35`
- Строки: `35--37`

```latex
\begin{equation}
 \sum_a(K_a^+-K_a^-)n_a=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0068

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:49`
- Строки: `49--53`

```latex
\begin{equation}
 \chi(E)=+1,
 \qquad
 \chi(E^*)=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0069

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 \mathcal T_{\rm Real}
 =\operatorname{STF}\sum_{a,s}\frac{w_a}{2}\,s\,
 \operatorname{Sym}(d_{a,s}\otimes t_{a,s}\otimes t_{a,s}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0070

- Источник: `s2t/gates/version6_single_thread_framed_winding_embedding_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 \mathcal T_{\rm Real}=\frac34T_*.
\end{equation}
```

## `s2t/gates/version6_spectral_transition_candidate_menu_retrospective_correction_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0071

- Источник: `s2t/gates/version6_spectral_transition_candidate_menu_retrospective_correction_gate.tex:37`
- Строки: `37--39`

```latex
\begin{equation}
 300\longrightarrow45\longrightarrow15\longrightarrow2\longrightarrow1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0072

- Источник: `s2t/gates/version6_spectral_transition_candidate_menu_retrospective_correction_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 q(x)P_0\otimes P_\nu(H(x))
 \label{eq:v6-retrospective-operator-defect}
\end{equation}
```

## `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0073

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:31`
- Строки: `31--42`

```latex
\begin{equation}
 U_4=
 \begin{pmatrix}
  0&-1\\
  1&0
 \end{pmatrix},
 \qquad
 U_4^2=-I,
 \qquad
 U_4^4=I.
 \label{eq:v6-compacton-reduced-c4-step}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0074

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:47`
- Строки: `47--52`

```latex
\begin{equation}
 P_{\pm i}=\frac14\sum_{n=0}^3(\pm i)^{-n}U_4^n,
 \qquad
 \rank P_{\pm i}=1.
 \label{eq:v6-compacton-pm-i-character-projectors}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0075

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 w_{\pm}=\langle\Psi,(P_{\pm i}\otimes I_3)\Psi\rangle.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0076

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:58`
- Строки: `58--63`

```latex
\begin{equation}
 \mathcal D_\chi(\Psi)
 :=1-\left|\langle\Psi,(U_4\otimes I_3)\Psi\rangle\right|^2
 =4w_+w_-\geq0.
 \label{eq:v6-compacton-character-purity-defect}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0077

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:69`
- Строки: `69--73`

```latex
\begin{equation}
 F\Psi=+i\Psi,
 \qquad
 F\Psi=-i\Psi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0078

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:75`
- Строки: `75--77`

```latex
\begin{equation}
 v_R=\pm i v_L.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0079

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:95`
- Строки: `95--101`

```latex
\begin{equation}
 \mathbb C^4=\operatorname{im}P_1\oplus\operatorname{im}P_3,
 \qquad
 P_1=\frac14J_4,
 \qquad
 P_3=I-P_1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0080

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:104`
- Строки: `104--106`

```latex
\begin{equation}
 \Spec(c)=\{1,i,-1,-i\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0081

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:128`
- Строки: `128--130`

```latex
\begin{equation}
 \operatorname{End}_{S_4}(\mathbb C^4)=\operatorname{span}\{I,J\},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0082

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:138`
- Строки: `138--144`

```latex
\begin{equation}
 X=\rho V,
 \qquad
 VV^*=I_3,
 \qquad
 V^*V=P_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0083

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:151`
- Строки: `151--153`

```latex
\begin{equation}
 \mathcal D_\chi(F\Psi)=\mathcal D_\chi(\Psi).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0084

- Источник: `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex:159`
- Строки: `159--164`

```latex
\begin{equation}
 H_{\rm sink}=
 \begin{pmatrix}
 0&I_3\\ I_3&0
 \end{pmatrix}
\end{equation}
```

## `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0085

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 v_*=\left(\frac12,0,\frac12\right)\in\mathbb C^2\oplus\mathbb C.
 \label{eq:v6-c4-eta-selected-axis}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0086

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:33`
- Строки: `33--37`

```latex
\begin{equation}
 \|v_*\|^2=\frac12,
 \qquad
 \|v_{*,L}\|^2=|v_{*,R}|^2=\frac14.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0087

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:39`
- Строки: `39--44`

```latex
\begin{equation}
 \Psi_+=(v_*,-iv_*),
 \qquad
 \Psi_-=(v_*,+iv_*)
 \label{eq:v6-c4-eta-selected-compactons}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0088

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:56`
- Строки: `56--61`

```latex
\begin{equation}
 \psi(s+L)=C\psi(s),
 \qquad
 C=(1234).
 \label{eq:v6-c4-eta-boundary-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0089

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:66`
- Строки: `66--69`

```latex
\begin{equation}
 Z_{S_4}(C)=\{1,C,C^2,C^3\}=\langle C\rangle\simeq C_4.
 \label{eq:v6-c4-eta-centralizer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0090

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:88`
- Строки: `88--91`

```latex
\begin{equation}
 \eta_\alpha(0)=1-2\alpha.
 \label{eq:v6-c4-eta-twisted-circle}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0091

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:93`
- Строки: `93--101`

```latex
\begin{equation}
 \alpha_+=\frac14,
 \quad
 \alpha_-=\frac34,
 \qquad
 \eta_+=\frac12,
 \quad
 \eta_-=-\frac12.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0092

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:103`
- Строки: `103--108`

```latex
\begin{equation}
 Z_{\eta,\pm}
 =\exp\!\left(-\frac{i\pi}{2}\eta_\pm\right)
 =e^{\mp i\pi/4}.
 \label{eq:v6-c4-eta-unit-phases}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0093

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:111`
- Строки: `111--116`

```latex
\begin{equation}
 |Z_{\eta,+}|=|Z_{\eta,-}|=1,
 \qquad
 -\log|Z_{\eta,\pm}|=0.
 \label{eq:v6-c4-eta-zero-decay}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0094

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:138`
- Строки: `138--140`

```latex
\begin{equation}
 Q_\eta=P_{+i}-P_{-i}=\operatorname{diag}(1,-1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0095

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:152`
- Строки: `152--154`

```latex
\begin{equation}
 L_\varphi=\sqrt\gamma\,Q_\eta,
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0096

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:157`
- Строки: `157--161`

```latex
\begin{equation}
 w_+(t)=w_-(t)=\frac12,
 \qquad
 4w_+(t)w_-(t)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0097

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:168`
- Строки: `168--171`

```latex
\begin{equation}
 L_\downarrow=\sqrt\gamma\,|+i\rangle\langle-i|.
 \label{eq:v6-c4-eta-oriented-jump}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0098

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:173`
- Строки: `173--178`

```latex
\begin{equation}
 w_+(t)=1-(1-w_+(0))e^{-\gamma t},
 \qquad
 w_-(t)=w_-(0)e^{-\gamma t},
 \label{eq:v6-c4-eta-capture-law}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0099

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate.tex:188`
- Строки: `188--190`

```latex
\begin{equation}
 t_{0.99}=\frac{\log50}{\gamma};
\end{equation}
```

## `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0100

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 \frac{a}{\Delta t}=c.
 \label{eq:v6-compacton-causal-scale}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0101

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 E\Delta t=\frac{\pi\hbar}{2}.
 \label{eq:v6-compacton-quasienergy-scale}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0102

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:48`
- Строки: `48--52`

```latex
\begin{equation}
 (a,\Delta t,E)\longmapsto
 (\lambda a,\lambda\Delta t,E/\lambda).
 \label{eq:v6-compacton-scale-null-direction}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0103

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:59`
- Строки: `59--64`

```latex
\begin{equation}
 \boxed{EL=\pi\hbar c},
 \qquad
 \frac{L}{\lambda_C}=\pi,
 \label{eq:v6-compacton-conditional-mass-size-product}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0104

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 \Lambda_{\rm S2T}=\sqrt\pi\,10^{16}\ {\rm GeV},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0105

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:76`
- Строки: `76--79`

```latex
\begin{equation}
 a=\alpha\frac{\hbar c}{\Lambda_{\rm S2T}}.
 \label{eq:v6-compacton-alpha-assignment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0106

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:99`
- Строки: `99--102`

```latex
\begin{equation}
 \vartheta_n=\pm\frac\pi2+2\pi n,
 \qquad n\in\mathbb Z,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0107

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:112`
- Строки: `112--115`

```latex
\begin{equation}
 \kappa=ga,
 \qquad a\longrightarrow0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0108

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:117`
- Строки: `117--119`

```latex
\begin{equation}
 \kappa=2\pi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0109

- Источник: `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex:121`
- Строки: `121--124`

```latex
\begin{equation}
 g=\frac{2\pi}{a}\longrightarrow\infty.
 \label{eq:v6-compacton-divergent-continuum-coupling}
\end{equation}
```

## `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex`

### LIVE-FORMULAS-GATES-VERSION6-09-0110

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:14`
- Строки: `14--17`

```latex
\begin{equation}
 G_n(\Psi)=\sigma_y^{\rm dir}\otimes K(H_{{\rm eff},n}),
 \label{eq:v6-composite-spatial-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0111

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 H_{{\rm eff},n}
 =\sum_{d=\pm}\ell_{n,d}\overline{e_{n,d}}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0112

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:25`
- Строки: `25--28`

```latex
\begin{equation}
 \Psi^{t+1}=S\exp[-i\kappa G(\Psi^t)]\Psi^t,
 \label{eq:v6-composite-spatial-update}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0113

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 H_{\rm eff}(\varepsilon\Psi)=O(\varepsilon^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0114

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:43`
- Строки: `43--47`

```latex
\begin{equation}
 \exp[-i\kappa G(\varepsilon\Psi)]\varepsilon\Psi
 =\varepsilon\Psi+O(\varepsilon^3).
 \label{eq:v6-composite-cubic-linearization}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION6-09-0115

- Источник: `s2t/gates/version6_spectral_transition_discrete_composite_higgs_spatial_binding_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 \kappa\in\{0,0.5,1,2,4,8,16,32\}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]