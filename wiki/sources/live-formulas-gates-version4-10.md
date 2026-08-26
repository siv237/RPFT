# Гейты Version 4, часть 10

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **110** блочных формул из **12** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0001

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:11`
- Строки: `11--15`

```latex
\begin{equation}
 D_F=\begin{pmatrix}0&M\\M^\dagger&0\end{pmatrix},
 \qquad
 \gamma=\begin{pmatrix}I&0\\0&-I\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0002

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 D_F^{2n}=\operatorname{diag}
 \left((MM^\dagger)^n,(M^\dagger M)^n\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0003

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 \Tr(\gamma D_F^{2n})=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0004

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:27`
- Строки: `27--32`

```latex
\begin{equation}
 \left.
 \frac{\partial^2}{\partial\sigma\,\partial\theta}
 \Tr p(D_F)
 \right|_{(0,0)}=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0005

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:44`
- Строки: `44--47`

```latex
\begin{equation}
 \det M(r,\theta)
 =\frac12r^2(2r+e^{i\theta})e^{-3i\theta}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0006

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:49`
- Строки: `49--54`

```latex
\begin{equation}
 \varphi_{\rm red}(\sigma,\theta)
 =\Im\left[
 2\sigma+\log(2e^\sigma+e^{i\theta})-3i\theta-\log2
 \right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0007

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 \partial_\theta\varphi_{\rm red}=-\frac83,
 \qquad
 \partial_\sigma\partial_\theta\varphi_{\rm red}=-\frac29.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0008

- Источник: `s2t/gates/version4_cp_odd_mixed_invariant_gate.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
 \operatorname{Pf}\mathcal A_{\rm full}
 =|\operatorname{Pf}\mathcal A_{\rm red}|^2,
\end{equation}
```

## `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0009

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:15`
- Строки: `15--17`

```latex
\begin{equation}
 W(H_u,H_d)=\Tr(P_-H_uH_d).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0010

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 W\in\left\{-\frac12,\,0,\,+\frac12\right\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0011

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 \Tr f(D_u^2)+\Tr f(D_d^2)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0012

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:43`
- Строки: `43--45`

```latex
\begin{equation}
 V_{ud}=\kappa_{ud}W(H_u,H_d)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0013

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:61`
- Строки: `61--64`

```latex
\begin{equation}
 Y_s=P_-+iH_s,
 \qquad s=u,d.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0014

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:66`
- Строки: `66--69`

```latex
\begin{equation}
 \Spec(Y_sY_s^\dagger)=
 \left\{\frac12,\,1,\,\frac52\right\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0015

- Источник: `s2t/gates/version4_cross_sector_transposition_orbit_gate.tex:71`
- Строки: `71--73`

```latex
\begin{equation}
 \Tr\left([Y_uY_u^\dagger,Y_dY_d^\dagger]^3\right)=0
\end{equation}
```

## `s2t/gates/version4_family_defect_cubic_root_action_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0016

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:15`
- Строки: `15--22`

```latex
\begin{equation}
 z(s)=\frac{\Phi(s)}{|\Phi(s)|}=e^{i\varphi(s)},
 \qquad
 \varphi(s+L)-\varphi(s)=2\pi\nu,
 \qquad
 \nu=\pm1.
 \label{eq:cubic-root-phase-winding}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0017

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:25`
- Строки: `25--29`

```latex
\begin{equation}
 W(s)=\exp\!\left[\frac{\varphi(s)}{3}\Omega(H)\right]
 \in SO(4).
 \label{eq:cubic-root-frame}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0018

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 W(s)^3=\exp[\varphi(s)\Omega(H)].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0019

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:36`
- Строки: `36--43`

```latex
\begin{equation}
 W(s+L)=W(s)Z_{H,\nu},
 \qquad
 Z_{H,\nu}=\exp\!\left[\nu\frac{2\pi}{3}\Omega(H)\right],
 \qquad
 Z_{H,\nu}^{,3}=I_4.
 \label{eq:cubic-root-monodromy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0020

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:60`
- Строки: `60--64`

```latex
\begin{equation}
 Q(H)=H^2-\frac1{\sqrt3}H-\frac14I_4,
 \qquad
 D_sW=\partial_sW+\mathcal A_sW,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0021

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:66`
- Строки: `66--73`

```latex
\begin{equation}
 S_{\rm root}[H,W,\mathcal A]
 =\int_0^L ds\left[
  \frac1L\Tr Q(H)^2
  +L\Tr\!\left((D_sW)^T D_sW\right)
 \right].
 \label{eq:cubic-root-parent-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0022

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 B_s=(\partial_sW)W^T
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0023

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 L\Tr\!\left[(\mathcal A_s+B_s)^T(\mathcal A_s+B_s)\right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0024

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:88`
- Строки: `88--93`

```latex
\begin{equation}
 \frac{\delta S_{\rm root}}{\delta\mathcal A_s}=0
 \quad\Longleftrightarrow\quad
 \mathcal A_s=-B_s=-\partial_sW\,W^T.
 \label{eq:connection-euler-lagrange}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0025

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:95`
- Строки: `95--100`

```latex
\begin{equation}
 \boxed{
 \mathcal A_s
 =-\frac{\partial_s\varphi}{3}\Omega(H)}.
 \label{eq:derived-projector-connection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0026

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:103`
- Строки: `103--106`

```latex
\begin{equation}
 \mathcal A
 =-\frac{2\pi\nu}{3L}\Omega(H)\,ds,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0027

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:127`
- Строки: `127--133`

```latex
\begin{align}
 \operatorname{Hol}_\gamma(\mathcal A)
 &=\exp\!\left[-\frac{\varphi(L)-\varphi(0)}{3}\Omega(H)\right]\\
 &=\exp\!\left[-\nu\frac{2\pi}{3}\Omega(H)\right]
 =C_{H,\nu}.
 \label{eq:root-action-holonomy}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0028

- Источник: `s2t/gates/version4_family_defect_cubic_root_action_gate.tex:146`
- Строки: `146--153`

```latex
\begin{align}
 \max\|D_{\mathcal A}W\|&<5.6\times10^{-16},\\
 \max\|Z_{H,\nu}^3-I\|&<5.1\times10^{-15},\\
 \max\|\operatorname{Hol}(\mathcal A)-C_{H,\nu}\|
 &<3.7\times10^{-15},\\
 \lambda_{\min}(\operatorname{Hess}_{\mathcal A}S_{\rm root})
 &=2-5\times10^{-16}.
\end{align}
```

## `s2t/gates/version4_frozen_k_family_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0029

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
K=\mathbb{RP}^3\times S^1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0030

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:16`
- Строки: `16--18`

```latex
\begin{equation}
d_1=0,\qquad d_2=2,\qquad d_3=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0031

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:20`
- Строки: `20--26`

```latex
\begin{align}
H_0(K;\mathbb Z)&=\mathbb Z,\\
H_1(K;\mathbb Z)&=\mathbb Z\oplus\mathbb Z_2,\\
H_2(K;\mathbb Z)&=\mathbb Z_2,\\
H_3(K;\mathbb Z)&=\mathbb Z,\\
H_4(K;\mathbb Z)&=\mathbb Z.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0032

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:28`
- Строки: `28--34`

```latex
\begin{align}
H^0(K;\mathbb Z)&=\mathbb Z,&
H^1(K;\mathbb Z)&=\mathbb Z,\\
H^2(K;\mathbb Z)&=\mathbb Z_2,&
H^3(K;\mathbb Z)&=\mathbb Z\oplus\mathbb Z_2,\\
H^4(K;\mathbb Z)&=\mathbb Z.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0033

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
H^1(K;\mathbb Z_2)\cong\mathbb Z_2\oplus\mathbb Z_2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0034

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
\pi_1(K)=\mathbb Z_2\times\mathbb Z,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0035

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
\operatorname{Hom}(\pi_1(K),U(1))\cong\{+1,-1\}\times U(1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0036

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:63`
- Строки: `63--65`

```latex
\begin{equation}
\mathcal R_K=\frac{6}{R^2}>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0037

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
D_{K,\rho}^2=\nabla_\rho^*\nabla_\rho+\frac{\mathcal R_K}{4}
\geq \frac{3}{2R^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0038

- Источник: `s2t/gates/version4_frozen_k_family_selector_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
\ker D_{K,\rho}=0
\end{equation}
```

## `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0039

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 \phi\sim(2_R,2_L,1),\qquad
 \Delta\sim(2_R,1_L,4),\qquad
 \Sigma_4\sim(1_R,1_L,15),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0040

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:24`
- Строки: `24--26`

```latex
\begin{equation}
 \langle\phi\rangle=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0041

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:28`
- Строки: `28--31`

```latex
\begin{align}
 Y={}&(k^\nu\phi+k^e\widetilde\phi)\Sigma_4
 +(k^u\phi+k^d\widetilde\phi)(I_4-\Sigma_4).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0042

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 \boxed{\phi=0\quad\Longrightarrow\quad Y=0}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0043

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 H_{\dot aI\dot bJ}
 =k^{\nu_R*}\Delta_{\dot aJ}\Delta_{\dot bI}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0044

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:50`
- Строки: `50--54`

```latex
\begin{equation}
 \rho=\Tr(\Delta^\dagger\Delta),
 \qquad
 \tau=\Tr[(\Delta^\dagger\Delta)^2].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0045

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:56`
- Строки: `56--60`

```latex
\begin{align}
 \frac12\Tr D_F^2&=\rho^2,\\
 \frac12\Tr D_F^4&=\tau^2.
 \label{eq:composite-ps-half-traces}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0046

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:68`
- Строки: `68--71`

```latex
\begin{equation}
 \boxed{V_\Delta=-\rho^2+\tau^2.}
 \label{eq:composite-ps-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0047

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:77`
- Строки: `77--82`

```latex
\begin{equation}
 \Delta_{\rm SM}
 =\begin{pmatrix}v&0&0&0\\0&0&0&0\end{pmatrix},
 \qquad
 v=2^{-1/4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0048

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:84`
- Строки: `84--86`

```latex
\begin{equation}
 V(\Delta_{\rm SM})=-\frac14.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0049

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:88`
- Строки: `88--94`

```latex
\begin{equation}
 \boxed{
 8\sqrt2\ (1),\qquad
 0\ (9),\qquad
 -2\sqrt2\ (6).}
 \label{eq:composite-ps-rank-one-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0050

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:101`
- Строки: `101--106`

```latex
\begin{equation}
 \Delta_{(2)}
 =\begin{pmatrix}v&0&0&0\\0&v&0&0\end{pmatrix},
 \qquad
 V(\Delta_{(2)})=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0051

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:108`
- Строки: `108--112`

```latex
\begin{equation}
 16\sqrt2\ (1),\qquad
 8\sqrt2\ (3),\qquad
 0\ (12),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0052

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:121`
- Строки: `121--124`

```latex
\begin{equation}
 V=f(\rho)+b\tau^2,
 \qquad b>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0053

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:127`
- Строки: `127--129`

```latex
\begin{equation}
 f'(p)+4bp^3=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0054

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:131`
- Строки: `131--134`

```latex
\begin{equation}
 \left.\frac{\partial V}{\partial q}\right|_{q=0}
 =f'(p)=-4bp^3<0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0055

- Источник: `s2t/gates/version4_pati_salam_composite_potential_hessian_gate.tex:150`
- Строки: `150--152`

```latex
\begin{equation}
 c_{\det}\det(\Delta\Delta^\dagger)
\end{equation}
```

## `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0056

- Источник: `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex:6`
- Строки: `6--10`

```latex
\begin{equation}
 G:\quad (I_R,R_4)=(1,\mathbf{10}),
 \qquad
 X:\quad (I_R,R_4)=(0,\mathbf6).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0057

- Источник: `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 C_2(1)=2,
 \qquad C_2(0)=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0058

- Источник: `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 C_2(\mathbf{10})=\frac92,
 \qquad
 C_2(\mathbf6)=\frac52.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0059

- Источник: `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex:49`
- Строки: `49--53`

```latex
\begin{equation}
 S_4=s_0\mathbf1_4+s_A T^A,
 \qquad
 S_4\in\mathbf1\oplus\mathbf{15}.
\end{equation}
```

## `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0060

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:11`
- Строки: `11--15`

```latex
\begin{equation}
 \pi(q_R,q_L,m)|_{V_R}=q_R\otimes I_4,
 \qquad
 \pi(q_R,q_L,m)|_{V_L}=q_L\otimes I_4,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0061

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:18`
- Строки: `18--20`

```latex
\begin{equation}
 \pi^o(b)=J_F\pi(b)J_F^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0062

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 4_{\mathbb H_R}+4_{\mathbb H_L}+32_{M_4(\mathbb C)}=40.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0063

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:27`
- Строки: `27--31`

```latex
\begin{equation}
 q_R(\lambda)=\operatorname{diag}(\lambda,\bar\lambda),
 \qquad
 m_4(\lambda,m_3)=\operatorname{diag}(\lambda,m_3),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0064

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:38`
- Строки: `38--41`

```latex
\begin{equation}
 \mathcal L_{a,b}(D_F)
 =[[D_F,\pi(a)],\pi^o(b)].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0065

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:55`
- Строки: `55--57`

```latex
\begin{equation}
 \dim_\mathbb R\ker\mathcal L_{PS}=272-264=8.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0066

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:59`
- Строки: `59--66`

```latex
\begin{equation}
 \boxed{
 Y=A\otimes I_4,
 \qquad
 A\in M_2(\mathbb C),
 \qquad
 M_R=M_L=0.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0067

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:73`
- Строки: `73--75`

```latex
\begin{equation}
 \boxed{\dim_\mathbb R\ker\mathcal L_{SM}=32.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0068

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:77`
- Строки: `77--81`

```latex
\begin{equation}
 Y=A_\ell\otimes P_\ell+A_q\otimes P_q,
 \qquad
 A_\ell,A_q\in M_2(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0069

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:83`
- Строки: `83--87`

```latex
\begin{equation}
 P_\ell=\operatorname{diag}(1,0,0,0),
 \qquad
 P_q=I_4-P_\ell.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0070

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:94`
- Строки: `94--104`

```latex
\begin{equation}
 \boxed{
 M_R=
 \begin{pmatrix}
 eu^T+ue^T&ve^T\\
 ev^T&0
 \end{pmatrix},
 \qquad
 M_L=0.}
 \label{eq:sm-first-order-mr-kernel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0071

- Источник: `s2t/gates/version4_pati_salam_first_order_kernel_gate.tex:131`
- Строки: `131--133`

```latex
\begin{equation}
 D_A=D+A_{(1)}+JA_{(1)}J^{-1}+A_{(2)}.
\end{equation}
```

## `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0072

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:26`
- Строки: `26--33`

```latex
\begin{equation}
 E_0^+=\bar4,
 \qquad
 E_1^-=2_R,
 \qquad
 E_2^+=4.
 \label{eq:ps-valid-module-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0073

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:36`
- Строки: `36--41`

```latex
\begin{equation}
 A_\Delta=\Delta:E_0\longrightarrow E_1,
 \qquad
 B_\Delta=c\,\Delta^T\varepsilon_2:E_1\longrightarrow E_2,
 \label{eq:ps-valid-module-edges}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0074

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:43`
- Строки: `43--46`

```latex
\begin{equation}
 \varepsilon_2=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0075

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:48`
- Строки: `48--50`

```latex
\begin{equation}
 U_R^T\varepsilon_2=\varepsilon_2U_R^{-1}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0076

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 B_\Delta A_\Delta
 =c\,\Delta^T\varepsilon_2\Delta.
 \label{eq:ps-valid-module-wedge}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0077

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:62`
- Строки: `62--66`

```latex
\begin{equation}
 \|B_\Delta A_\Delta\|_F^2
 =2c^2\det(\Delta\Delta^\dagger).
 \label{eq:ps-valid-module-minor-norm}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0078

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:71`
- Строки: `71--78`

```latex
\begin{equation}
 \mathcal D_\Delta=
 \begin{pmatrix}
 0&A_\Delta^\dagger&0\\
 A_\Delta&0&B_\Delta^\dagger\\
 0&B_\Delta&0
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0079

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:80`
- Строки: `80--86`

```latex
\begin{equation}
 \rho=\Tr(\Delta\Delta^\dagger),
 \qquad
 \tau=\Tr[(\Delta\Delta^\dagger)^2],
 \qquad
 d=\det(\Delta\Delta^\dagger)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0080

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:88`
- Строки: `88--94`

```latex
\begin{align}
 \Tr\mathcal D_\Delta^2
 &=2(1+c^2)\rho,\\
 \Tr\mathcal D_\Delta^4
 &=2(1+c^4)\tau+8c^2d.
 \label{eq:ps-valid-module-raw-traces}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0081

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:96`
- Строки: `96--98`

```latex
\begin{equation}
 \Tr\mathcal D_\Delta^4=4\rho^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0082

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:107`
- Строки: `107--112`

```latex
\begin{equation}
 F_{02}
 =P_0\mathcal D_\Delta^2P_2
 +P_2\mathcal D_\Delta^2P_0.
 \label{eq:ps-endpoint-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0083

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:115`
- Строки: `115--120`

```latex
\begin{equation}
 \boxed{
 \|F_{02}\|_F^2
 =4c^2\det(\Delta\Delta^\dagger).}
 \label{eq:ps-projected-curvature-selector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0084

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:126`
- Строки: `126--130`

```latex
\begin{equation}
 \boxed{\frac12\|F_{02}^{\rm KO6}\|_F^2
 =4\det(\Delta\Delta^\dagger).}
 \label{eq:ps-project-recovered-kappa-four}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0085

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:138`
- Строки: `138--140`

```latex
\begin{equation}
 \kappa=4c^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0086

- Источник: `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex:142`
- Строки: `142--147`

```latex
\begin{equation}
 \kappa>2
 \quad\Longleftrightarrow\quad
 c^2>\frac12.
 \label{eq:ps-project-recovery-window}
\end{equation}
```

## `s2t/gates/version4_relative_krajewski_star_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0087

- Источник: `s2t/gates/version4_relative_krajewski_star_gate.tex:11`
- Строки: `11--17`

```latex
\begin{equation}
 M_3=
 \rho M_3\rho
 \oplus\rho M_3Q
 \oplus QM_3\rho
 \oplus QM_3Q,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0088

- Источник: `s2t/gates/version4_relative_krajewski_star_gate.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 1,\qquad2,\qquad2,\qquad4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0089

- Источник: `s2t/gates/version4_relative_krajewski_star_gate.tex:32`
- Строки: `32--36`

```latex
\begin{equation}
 \rho M_3\rho\oplus\rho M_3Q\oplus QM_3\rho
 =\mathcal M_\rho,
 \qquad \dim\mathcal M_\rho=5.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0090

- Источник: `s2t/gates/version4_relative_krajewski_star_gate.tex:54`
- Строки: `54--58`

```latex
\begin{equation}
 \rho H+H\rho-\rho H\rho
 =H-QHQ
 =\Pi_\rho(H).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0091

- Источник: `s2t/gates/version4_relative_krajewski_star_gate.tex:72`
- Строки: `72--76`

```latex
\begin{equation}
 u,\nu\longmapsto H_{\rm up},
 \qquad
 d,e\longmapsto H_{\rm down}.
\end{equation}
```

## `s2t/gates/version4_s4_radius_boundary_no_go.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0092

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:10`
- Строки: `10--15`

```latex
\begin{equation}
 Z(a;\tau)=\sum_{\ell=0}^\infty
 d_\ell\exp\!\left(-\frac{\tau\mu_\ell}{a^2}\right),
 \qquad
 F(a;\tau)=-\frac1\tau\log Z(a;\tau).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0093

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 \frac{\partial F}{\partial a}
 =-\frac{2}{a^3}\langle\mu\rangle_{a,\tau}<0
 \qquad(a>0).
 \label{eq:s4-gibbs-radius-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0094

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 Z\to1,
 \qquad F\to0^-.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0095

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:33`
- Строки: `33--36`

```latex
\begin{equation}
 Z(a;\tau)\sim\frac{\operatorname{Vol}(S^4_a)}{(4\pi\tau)^2}
 =\frac{a^4}{6\tau^2},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0096

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:38`
- Строки: `38--41`

```latex
\begin{equation}
 F(a;\tau)sim-\frac1\tau
 \log\!\left(\frac{a^4}{6\tau^2}\right)\longrightarrow-\infty.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0097

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:53`
- Строки: `53--56`

```latex
\begin{equation}
 S_f(a)=\sum_{\ell=0}^\infty d_\ell
 f\!\left(\frac{\mu_\ell}{a^2\Lambda^2}\right),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0098

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:59`
- Строки: `59--66`

```latex
\begin{equation}
 \frac{dS_f}{da}
 =-\frac2a\sum_{\ell=0}^\infty d_\ell y_\ell f'(y_\ell)
 \ge0,
 \qquad
 y_\ell=\frac{\mu_\ell}{a^2\Lambda^2}.
 \label{eq:s4-positive-spectral-radius-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0099

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:91`
- Строки: `91--95`

```latex
\begin{equation}
 \partial_aS_{\rm state}<0,
 \qquad
 \partial_aS_{\rm EFT}>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0100

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:102`
- Строки: `102--104`

```latex
\begin{equation}
 \mathcal J(a)=\alpha S_f(a)+\beta F(a)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0101

- Источник: `s2t/gates/version4_s4_radius_boundary_no_go.tex:111`
- Строки: `111--113`

```latex
\begin{equation}
 Z(a)=\frac{\beta}{\alpha\tau}.
\end{equation}
```

## `s2t/gates/version4_standard_model_representation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0102

- Источник: `s2t/gates/version4_standard_model_representation_gate.tex:49`
- Строки: `49--55`

```latex
\begin{equation}
 \mathcal A_{333},\quad
 \mathcal A_{221},\quad
 \mathcal A_{331},\quad
 \mathcal A_{111},\quad
 \mathcal A_{\mathrm{grav}^2 1},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0103

- Источник: `s2t/gates/version4_standard_model_representation_gate.tex:86`
- Строки: `86--90`

```latex
\begin{equation}
 \{\text{допустимые finite geometries}\}
 \longrightarrow
 \{\text{anomaly-free observed candidates}\}.
\end{equation}
```

## `s2t/gates/version4_vectorlike_messenger_chain_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-10-0104

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
q_h(X_0)=0,
\qquad
q_h(X_q)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0105

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:19`
- Строки: `19--23`

```latex
\begin{align}
\overline F_L H_f X_{0R},\\
\overline X_{0L}\Omega X_{qR},\\
\overline X_{qL}\phi_h f_R,
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0106

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
\frac{1}{M_0M_q}\,
\overline F_L H_f\Omega\phi_h f_R.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0107

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:43`
- Строки: `43--45`

```latex
\begin{equation}
E-V+1=3-4+1=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0108

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
E-V+1=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0109

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:54`
- Строки: `54--59`

```latex
\begin{equation}
\arg\left(
y_{\Omega a}y_{\phi a}
y_{\Omega b}^*y_{\phi b}^*
\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-10-0110

- Источник: `s2t/gates/version4_vectorlike_messenger_chain_gate.tex:72`
- Строки: `72--80`

```latex
\begin{equation}
R_u=(\mathbf3,\mathbf1)_{2/3},
\quad
R_d=(\mathbf3,\mathbf1)_{-1/3},
\quad
R_e=(\mathbf1,\mathbf1)_{-1},
\quad
R_\nu=(\mathbf1,\mathbf1)_0.
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]