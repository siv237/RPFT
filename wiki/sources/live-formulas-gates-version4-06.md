# Гейты Version 4, часть 6

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **111** блочных формул из **12** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_bimodule_multiplicity_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0001

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
Q_L,\quad u_R,\quad d_R,\quad L_L,\quad e_R,\quad \nu_R,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0002

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:14`
- Строки: `14--18`

```latex
\begin{equation}
m_u=m_d=m_Q,
\qquad
m_e=m_\nu=m_L.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0003

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
m_e=m_L,
\qquad
m_\nu=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0004

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
\mathcal A_{333}=2m_Q-m_u-m_d,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0005

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
\mathcal A_{221}=\frac12(m_Q-m_L).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0006

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:35`
- Строки: `35--37`

```latex
\begin{equation}
m_Q=m_L=:g.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0007

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:44`
- Строки: `44--46`

```latex
\begin{equation}
(m_Q,m_u,m_d,m_L,m_e,m_\nu)=g(1,1,1,1,1,1)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0008

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:52`
- Строки: `52--54`

```latex
\begin{equation}
(m_Q,m_u,m_d,m_L,m_e,m_\nu)=(1,1,1,1,1,0)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0009

- Источник: `s2t/gates/version4_bimodule_multiplicity_gate.tex:65`
- Строки: `65--67`

```latex
\begin{equation}
g=1,2,3,\ldots
\end{equation}
```

## `s2t/gates/version4_determinant_line_inflow_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0010

- Источник: `s2t/gates/version4_determinant_line_inflow_gate.tex:10`
- Строки: `10--15`

```latex
\begin{align}
 \operatorname{Pf}\mathcal A_-(z)
 &=-\frac12(z+2)z^{-3},\\
 \operatorname{Pf}\mathcal A_+(z)
 &=+\frac12(z-2)z^{-3}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0011

- Источник: `s2t/gates/version4_determinant_line_inflow_gate.tex:27`
- Строки: `27--32`

```latex
\begin{equation}
 H_d(t)=(1-t)H_d^-+tH_d^+,
 \qquad
 z(t)=e^{i\pi t},
 \qquad 0\le t\le1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0012

- Источник: `s2t/gates/version4_determinant_line_inflow_gate.tex:34`
- Строки: `34--40`

```latex
\begin{equation}
 \det M(t)
 =
 \left(
 1+\left(\frac12-t\right)e^{i\pi t}
 \right)e^{-3i\pi t}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0013

- Источник: `s2t/gates/version4_determinant_line_inflow_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \left|1-u e^{i\pi(1/2+u)}\right|^2
 =
 1+u^2+2u\sin(\pi u)
 \ge1.
\end{equation}
```

## `s2t/gates/version4_family_defect_holonomy_realization_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0014

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 u=\frac12(1,1,1,1)^T
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0015

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:16`
- Строки: `16--20`

```latex
\begin{equation}
 \Omega(h_a)_{bc}
 =\sum_{d,e=1}^4\epsilon_{bcde}u_d(h_a)_e.
 \label{eq:orientation-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0016

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:23`
- Строки: `23--28`

```latex
\begin{align}
 \Omega^T&=-\Omega,\\
 \Omega u&=0,\\
 \Omega h_a&=0,\\
 \Omega^2&=-\left(I_4-uu^T-h_ah_a^T\right).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0017

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 [\Omega(h_a),H_a]=0.
 \label{eq:connection-field-commutator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0018

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \mathcal A_{a,\nu}
 =-\frac{2\pi\nu}{3L}\Omega(h_a)\,ds,
 \qquad \nu=\pm1.
 \label{eq:projector-flat-connection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0019

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:49`
- Строки: `49--52`

```latex
\begin{equation}
 \operatorname{Hol}_\gamma(\mathcal A_{a,\nu})
 =\exp\!\left[-\nu\frac{2\pi}{3}\Omega(h_a)\right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0020

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:56`
- Строки: `56--59`

```latex
\begin{equation}
 \operatorname{Hol}_\gamma(\mathcal A_{a,\nu})=C_{a,\nu}
 \label{eq:holonomy-equals-three-cycle}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0021

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 g\Omega(h_a)g^{-1}
 =\operatorname{sgn}(g)\Omega(h_{g(a)}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0022

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 \nu\longmapsto\operatorname{sgn}(g)\nu,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0023

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:83`
- Строки: `83--88`

```latex
\begin{align}
 g\mathcal A_{a,\nu}g^{-1}
 &=\mathcal A_{g(a),\operatorname{sgn}(g)\nu},\\
 gC_{a,\nu}g^{-1}
 &=C_{g(a),\operatorname{sgn}(g)\nu}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0024

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:94`
- Строки: `94--96`

```latex
\begin{equation}
 \mathbb A_{a,\nu}=d+\mathcal A_{a,\nu}+T(H_a),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0025

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:99`
- Строки: `99--105`

```latex
\begin{equation}
 F_{\mathcal A}=0,
 \qquad
 D_{\mathcal A}H_a=0,
 \qquad
 Q(H_a)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0026

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:126`
- Строки: `126--130`

```latex
\begin{equation}
 \mathcal A
 =-\frac{2\pi\nu}{3L}\Omega(h)\,ds.
 \label{eq:constitutive-holonomy-relation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0027

- Источник: `s2t/gates/version4_family_defect_holonomy_realization_gate.tex:147`
- Строки: `147--150`

```latex
\begin{equation}
 \mathcal A_s=-\partial_sW\,W^T
 =-\frac{\partial_s\varphi}{3}\Omega(H),
\end{equation}
```

## `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0028

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 F=\left\{x\in\mathbb R^4:\sum_{a=1}^4x_a=0\right\},
 \qquad \|x\|=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0029

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 I_3(x)=\sum_{a=1}^4x_a^3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0030

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 -\frac1{\sqrt3}\leq I_3(x)\leq\frac1{\sqrt3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0031

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:26`
- Строки: `26--28`

```latex
\begin{equation}
 \pm\frac1{\sqrt{12}}(3,-1,-1,-1)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0032

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:36`
- Строки: `36--38`

```latex
\begin{equation}
 \chi_3(\theta)=\Tr R_n(\theta)=1+2\cos\theta.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0033

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:41`
- Строки: `41--43`

```latex
\begin{equation}
 \theta=\frac{2\pi}{3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0034

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:56`
- Строки: `56--64`

```latex
\begin{equation}
 \begin{split}
 V_\nu(r,\theta,n)={}&(r^2-1)^2
 +r^2\bigl(1+2\cos\theta\bigr)^2\\
 &+r^2\left(1-\sqrt3\,\nu I_3(Bn)\right),
 \qquad \|n\|=1.
 \end{split}
 \label{eq:family-defect-three-cycle-lock}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0035

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:67`
- Строки: `67--73`

```latex
\begin{equation}
 r=1,
 \qquad
 \theta=\frac{2\pi}{3},
 \qquad
 I_3(Bn)=\frac{\nu}{\sqrt3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0036

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:91`
- Строки: `91--97`

```latex
\begin{equation}
 \lambda_r=8,
 \qquad
 \lambda_\theta=6,
 \qquad
 \lambda_{n,1}=\lambda_{n,2}=6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0037

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:100`
- Строки: `100--102`

```latex
\begin{equation}
 K_n=\frac{2\pi}{3}[n]_\times
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0038

- Источник: `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex:105`
- Строки: `105--109`

```latex
\begin{equation}
 \dim\ker K_n=1,
 \qquad
 3\longrightarrow1.
\end{equation}
```

## `s2t/gates/version4_gibbs_fisher_geometry_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0039

- Источник: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex:4`
- Строки: `4--7`

```latex
\begin{equation}
 p_n(r)=Z(r)^{-1}d_ne^{-\mu_n/r^2},
 \qquad x=\log r,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0040

- Источник: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex:9`
- Строки: `9--11`

```latex
\begin{equation}
 \partial_x\log p_n=2(\mu_n-\langle\mu\rangle)/r^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0041

- Источник: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 \boxed{I_x=\frac{4\operatorname{Var}(\mu)}{r^4}},
 \qquad d\mu_J=\sqrt{I_x}\,dx.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0042

- Источник: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 H_F=\frac{r_*^2\mathfrak f''(r_*)}{I_x(r_*)}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0043

- Источник: `s2t/gates/version4_gibbs_fisher_geometry_gate.tex:23`
- Строки: `23--26`

```latex
\begin{align}
 H_F(S^4)&=0.00588026822269\ldots,\\
 H_F(S^2\times S^2)&=0.00456099125215\ldots.
\end{align}
```

## `s2t/gates/version4_old_problem_rotation_audit.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0044

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 G_{\rm ren},\quad c_{W^2},\quad c_E,\quad
 \xi_s,\quad\text{и origin massive-vector sector}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0045

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
 4\ \text{transpositions}
 \;+\;
 8\ \text{three-cycles}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0046

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:47`
- Строки: `47--51`

```latex
\begin{equation}
 R_n(\theta_\star)\in SO(3),
 \qquad
 K_n=\theta_\star[n]_\times,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0047

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 0.89220655,
 \qquad
 0.81649658,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0048

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:86`
- Строки: `86--90`

```latex
\begin{equation}
 0.46858872,
 \qquad
 0.61547971.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0049

- Источник: `s2t/gates/version4_old_problem_rotation_audit.tex:92`
- Строки: `92--96`

```latex
\begin{equation}
 \theta_\star=2.50675535,
 \qquad
 \theta_{3{\rm cyc}}=\frac{2\pi}{3}=2.09439510,
\end{equation}
```

## `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0050

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 V_\alpha(D_F)
 =-\frac\alpha2\Tr D_F^2+\frac12\Tr D_F^4,
 \qquad \alpha>0,
 \label{eq:ps-common-scale-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0051

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:22`
- Строки: `22--26`

```latex
\begin{equation}
 \|M_R\|_{\rm op}^2=\frac\alpha2,
 \qquad
 \Delta_{\dot1,1}=\left(\frac\alpha2\right)^{1/4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0052

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:29`
- Строки: `29--35`

```latex
\begin{equation}
 \boxed{
 H_{Y,\alpha}(Y)
 =-4\alpha\|Y\|_F^2+8\|M_R^\dagger Y\|_F^2
 \le0.}
 \label{eq:ps-common-scale-yukawa-no-go}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0053

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 \alpha\left[-34.92338966\ (4),-7.30661034\ (4)\right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0054

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 \mathbb H^2\oplus\mathbb C^2\oplus M_3(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0055

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:108`
- Строки: `108--113`

```latex
\begin{equation}
 \bigl(\Tr \dot H^2\bigr)^2,
 \qquad
 \Tr(\dot H^2)\Tr(\Sigma^2),
 \label{eq:ps-missing-mixed-invariants}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0056

- Источник: `s2t/gates/version4_pati_salam_project_wide_rescue_archaeology_gate.tex:120`
- Строки: `120--124`

```latex
\begin{align}
 I_Y&=\Tr(M_R^\dagger M_R)\Tr(Y^\dagger Y),\\
 I_\Sigma&=\Tr(M_R^\dagger M_R)\Tr(\Sigma_4^2),\\
 I_{\rm conn}&=\Tr(M_R^\dagger M_R\,\mathcal C(\Sigma_4,Y)),
\end{align}
```

## `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0057

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:15`
- Строки: `15--21`

```latex
\begin{equation}
 \mu_\ell=\ell(\ell+2),
 \qquad
 d_\ell=(\ell+1)^2,
 \qquad
 \ell=0,2,4,\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0058

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 \mathfrak f_{\mathbb{RP}^3}(s)
 =-\frac{\log Z_{\mathbb{RP}^3}(s)}{\pi^2s^3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0059

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 \frac{2\langle\mu\rangle}{s^2}=d\log Z,
 \qquad d=3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0060

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 s_*=1.99760832726935\ldots,
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0061

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:36`
- Строки: `36--41`

```latex
\begin{equation}
 \mathfrak f_{\mathbb{RP}^3}(s_*)
 =-0.0104399545649812\ldots,
 \qquad
 \mathfrak f''(s_*)=0.0186601722182339\ldots>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0062

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:44`
- Строки: `44--46`

```latex
\begin{equation}
 \frac{s_*}{2}-1=-1.1958363653\cdot10^{-3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0063

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:48`
- Строки: `48--51`

```latex
\begin{equation}
 \frac{\operatorname{Vol}(\mathbb{RP}^3_{b_*})}{\sigma^3}
 =78.6739154398455\ldots,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0064

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:53`
- Строки: `53--56`

```latex
\begin{equation}
 \frac{\operatorname{sys}(\mathbb{RP}^3_{b_*})}{\sigma}
 =\pi s_*=6.27567164569920\ldots
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0065

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 X=S^4_a\times\mathbb{RP}^3_b,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0066

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:72`
- Строки: `72--77`

```latex
\begin{equation}
 \mathfrak f_X(r,s)
 =-\frac{\log Z_{S^4}(r)+\log Z_{\mathbb{RP}^3}(s)}
 {v_4\pi^2r^4s^3}.
 \label{eq:s4-rp3-joint-density}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0067

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:79`
- Строки: `79--85`

```latex
\begin{equation}
 \log Z_{\mathbb{RP}^3}(s)\to0,
 \qquad
 \mathfrak f_X(r,s)
 \sim-\frac{\log Z_{S^4}(r)}{v_4\pi^2r^4s^3}
 \longrightarrow-\infty.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0068

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:104`
- Строки: `104--108`

```latex
\begin{equation}
 \frac{m_{\rm KK}^{\rm trivial}}{\sigma^{-1}}
 =\frac{\sqrt8}{s_*}
 =1.41590675516\ldots,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0069

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:109`
- Строки: `109--113`

```latex
\begin{equation}
 \frac{m_{\rm KK}^{\rm twisted}}{\sigma^{-1}}
 =\frac{\sqrt3}{s_*}
 =0.867062268376\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0070

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:120`
- Строки: `120--122`

```latex
\begin{equation}
 s_*=1.34900141462449\ldots
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0071

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:160`
- Строки: `160--163`

```latex
\begin{equation}
 (R_3/\sigma,R_1/\sigma)
 =(1.225861334\ldots,1.106633155\ldots),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0072

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:165`
- Строки: `165--168`

```latex
\begin{equation}
 (R_3/\sigma,R_1/\sigma)
 =(1.032467629\ldots,0.977157086\ldots).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0073

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:173`
- Строки: `173--177`

```latex
\begin{equation}
 I(B:C)=D(\rho_{BC}\|\rho_B\otimes\rho_C)\ge0,
 \qquad
 F_{BC}=F_B+F_C+T I(B:C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0074

- Источник: `s2t/gates/version4_s4_rp3_hybrid_experiment_gate.tex:181`
- Строки: `181--184`

```latex
\begin{equation}
 F_{\rm bundle}-F_{\rm product}
 =0.3689227663\ldots>0.
\end{equation}
```

## `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0075

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:12`
- Строки: `12--18`

```latex
\begin{equation}
 a=\left(\frac{3}{8\pi^2}\right)^{1/4}
 \quad\text{для }S^4,
 \qquad
 b=\left(\frac{1}{16\pi^2}\right)^{1/4}
 \quad\text{для каждого }S^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0076

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:21`
- Строки: `21--25`

```latex
\begin{equation}
 \rho_\tau(M)=\frac{e^{-\tau\Delta_0(M)}}{Z_M(\tau)},
 \qquad
 Z_M(\tau)=\Tr e^{-\tau\Delta_0(M)},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0077

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:26`
- Строки: `26--32`

```latex
\begin{equation}
 \mathcal P_\tau(M)=\Tr\rho_\tau(M)^2
 =\frac{Z_M(2\tau)}{Z_M(\tau)^2},
 \qquad
 S_2(M;\tau)=-\log\mathcal P_\tau(M).
 \label{eq:carrier-renyi2-definition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0078

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 \Delta S_2(\tau)
 =S_2(S^4;\tau)-S_2(S^2\times S^2;\tau).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0079

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:42`
- Строки: `42--46`

```latex
\begin{equation}
 \lambda_\ell^{(4)}=\frac{\ell(\ell+3)}{a^2},
 \qquad
 d_\ell^{(4)}=\frac{(\ell+1)(\ell+2)(2\ell+3)}6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0080

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:48`
- Строки: `48--52`

```latex
\begin{equation}
 \lambda_\ell^{(2)}=\frac{\ell(\ell+1)}{b^2},
 \qquad
 d_\ell^{(2)}=2\ell+1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0081

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 Z_{S^2\times S^2}(\tau)=Z_{S^2}(\tau)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0082

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:63`
- Строки: `63--68`

```latex
\begin{equation}
 \Delta S_2(\tau)
 =\frac{16\pi^2}{15}\tau^2+O(\tau^3)>0
 \qquad(\tau\to0^+).
 \label{eq:carrier-small-tau-positive}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0083

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:71`
- Строки: `71--74`

```latex
\begin{equation}
 \lambda_1(S^4)=\frac4{a^2}=20.52079728\ldots,
 \qquad d_1(S^4)=5,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0084

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:75`
- Строки: `75--79`

```latex
\begin{equation}
 \lambda_1(S^2\times S^2)=\frac2{b^2}=8\pi
 =25.13274123\ldots,
 \qquad d_1(S^2\times S^2)=6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0085

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 \Delta S_2(\tau)
 \sim10e^{-4\tau/a^2}-12e^{-2\tau/b^2}>0.
 \label{eq:carrier-large-tau-positive}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0086

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:91`
- Строки: `91--93`

```latex
\begin{equation}
 10^{-5}\le\tau\le2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0087

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:96`
- Строки: `96--99`

```latex
\begin{equation}
 \Delta S_2(0.1133942342\ldots)
 =0.1810734171\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0088

- Источник: `s2t/gates/version4_s4_s2xs2_correlation_purity_gate.tex:117`
- Строки: `117--119`

```latex
\begin{equation}
 S_2(S^4;\tau)>S_2(S^2\times S^2;\tau)
\end{equation}
```

## `s2t/gates/version4_spectral_gauge_normalization_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0089

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:10`
- Строки: `10--14`

```latex
\begin{align}
C_Y&=\sum_{\rm Weyl}d_3d_2Y^2=\frac{10}{3},\\
C_2&=\sum_{\rm Weyl}d_3T_2(R)=2,\\
C_3&=\sum_{\rm Weyl}d_2T_3(R)=2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0090

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:16`
- Строки: `16--18`

```latex
\begin{equation}
T_1=\sqrt{\frac35}\,Y
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0091

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
C_1=\frac35C_Y=2=C_2=C_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0092

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
\boxed{g_1=g_2=g_3,}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0093

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:32`
- Строки: `32--38`

```latex
\begin{equation}
g_Y^2=\frac35g_2^2,
\qquad
g_2^2=g_3^2,
\qquad
\sin^2\theta_W=\frac38
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0094

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:49`
- Строки: `49--55`

```latex
\begin{equation}
\widehat\alpha^{-1}(M_Z)=127.955,
\qquad
\sin^2\widehat\theta_W(M_Z)=0.23122,
\qquad
\alpha_s(M_Z)=0.1180.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0095

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:61`
- Строки: `61--67`

```latex
\begin{equation}
g_1(M_Z)=0.46142,
\qquad
g_2(M_Z)=0.65172,
\qquad
g_3(M_Z)=1.21772.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0096

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
(b_1,b_2,b_3)=\left(\frac{41}{10},-\frac{19}{6},-7\right),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0097

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:76`
- Строки: `76--79`

```latex
\begin{equation}
\frac1{g_i^2(\mu)}=
\frac1{g_i^2(M_Z)}-\frac{b_i}{8\pi^2}\log\frac{\mu}{M_Z}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0098

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:81`
- Строки: `81--85`

```latex
\begin{align}
g_1=g_2:&\quad \mu_{12}=1.03\times10^{13}\,\mathrm{GeV},\\
g_1=g_3:&\quad \mu_{13}=2.43\times10^{14}\,\mathrm{GeV},\\
g_2=g_3:&\quad \mu_{23}=9.73\times10^{16}\,\mathrm{GeV}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0099

- Источник: `s2t/gates/version4_spectral_gauge_normalization_gate.tex:89`
- Строки: `89--93`

```latex
\begin{equation}
g_1=g_3=0.55806,
\qquad
g_2=0.53438,
\end{equation}
```

## `s2t/gates/version4_state_anchored_bimodule_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0100

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:13`
- Строки: `13--17`

```latex
\begin{equation}
 \mathcal M_{\rho}:=
 \rho_\star M_3+M_3\rho_\star
 =\{X\in M_3:Q_\star XQ_\star=0\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0101

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 \mathcal A_\rho=
 \operatorname{span}\{\rho_\star,Q_\star\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0102

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 \dim_{\mathbb C}\mathcal M_\rho=5,
 \qquad
 \dim_{\mathbb C}\ker\Pi_\rho=4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0103

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
 \boxed{
 \Pi_\rho(X)=X-Q_\star XQ_\star
 =\rho_\star X+X\rho_\star-\rho_\star X\rho_\star.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0104

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 \Pi_{U\rho U^\dagger}(UXU^\dagger)
 =U\Pi_\rho(X)U^\dagger.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0105

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:51`
- Строки: `51--54`

```latex
\begin{equation}
 Y_s^{\rm anch}=P_-+i\Pi_{\rho_\star}(H_s),
 \qquad s=u,d.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0106

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:59`
- Строки: `59--62`

```latex
\begin{align}
 m_u/m_{u,\max}&=(0.192658,\,0.375569,\,1),\\
 m_d/m_{d,\max}&=(0.119012,\,0.430519,\,1),
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0107

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:64`
- Строки: `64--66`

```latex
\begin{equation}
 \Im\Tr[M_u,M_d]^3=-0.287960\ne0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0108

- Источник: `s2t/gates/version4_state_anchored_bimodule_gate.tex:68`
- Строки: `68--75`

```latex
\begin{equation}
 |V_{\rm anch}|\simeq
 \begin{pmatrix}
 0.4302&0.8512&0.3007\\
 0.8349&0.4751&0.2777\\
 0.3432&0.2230&0.9124
 \end{pmatrix}.
\end{equation}
```

## `s2t/gates/version4_yukawa_operator_map_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-06-0109

- Источник: `s2t/gates/version4_yukawa_operator_map_gate.tex:4`
- Строки: `4--9`

```latex
\begin{equation}
 \rho_\star=|\psi_\star\rangle\langle\psi_\star|,
 \qquad
 |\psi_\star\rangle\simeq
 (0.939575,\,0.310502,\,-0.144179)^T.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0110

- Источник: `s2t/gates/version4_yukawa_operator_map_gate.tex:18`
- Строки: `18--24`

```latex
\begin{align}
 Y^{(0)}(H)&=P_-+iH,\\
 Y^{(\rho)}(H)&=P_-+i\{\rho_\star,H\},\\
 Y_u^{(\nabla)}&=\frac{\partial V_4}{\partial H_u},
 &
 Y_d^{(\nabla)}&=\frac{\partial V_4}{\partial H_d}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-06-0111

- Источник: `s2t/gates/version4_yukawa_operator_map_gate.tex:56`
- Строки: `56--63`

```latex
\begin{equation}
 |V^{(\nabla)}|\simeq
 \begin{pmatrix}
 0.2254&0.8161&0.5321\\
 0.8819&0.4030&0.2445\\
 0.4140&0.4141&0.8106
 \end{pmatrix},
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]