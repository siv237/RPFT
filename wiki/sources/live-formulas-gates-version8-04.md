# Гейты Version 8 — часть 4

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **54** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0001

- Источник: `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 D_e=\begin{pmatrix}0&e^*\\e&0\end{pmatrix}
 \in\operatorname{End}(\mathbb C^{21}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0002

- Источник: `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex:19`
- Строки: `19--23`

```latex
\begin{equation}
 \mathcal L_{q\ell}(Z)
 =\sum_{a=1}^{12}\left(D_aZD_a-\frac12\{D_a^2,Z\}\right).
 \label{eq:v8-lcf-gauge-twirl-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0003

- Источник: `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 \dim\bigcap_G\ker R_G=0.
 \label{eq:v8-lcf-no-linear-gauge-singlet}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0004

- Источник: `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex:48`
- Строки: `48--54`

```latex
\begin{equation}
 M_0=\begin{pmatrix}
 \frac12&-\frac1{\sqrt3}\\
 -\frac1{\sqrt3}&\frac23
 \end{pmatrix},
 \qquad \Spec M_0=\left\{0,\frac76\right\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0005

- Источник: `s2t/gates/version8_gauge_twirl_kraus_lcf_migration_gate.tex:56`
- Строки: `56--64`

```latex
\begin{equation}
 M_{q\ell}=\begin{pmatrix}
 1&-\frac2{\sqrt3}\\
 -\frac2{\sqrt3}&\frac43
 \end{pmatrix},
 \qquad
 \det(\lambda I-M_{q\ell})=\lambda\left(\lambda-\frac73\right).
 \label{eq:v8-lcf-cross-central-matrix}
\end{equation}
```

## `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0006

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:11`
- Строки: `11--15`

```latex
\begin{equation}
 A_m\longmapsto A_{m+1},
 \qquad
 B_m\longmapsto B_{m-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0007

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 \operatorname{ind}(S_A S_B^{-1})
 =43\cdot\frac1{43}=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0008

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:26`
- Строки: `26--29`

```latex
\begin{align}
 W_0&=\prod_{m\in\mathbb Z}\operatorname{SWAP}(A_m,B_m),\\
 W_1&=\prod_{m\in\mathbb Z}\operatorname{SWAP}(B_m,A_{m+1}).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0009

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:31`
- Строки: `31--35`

```latex
\begin{equation}
 A_m^{\rm out}=A_{m-1}^{\rm in},
 \qquad
 B_m^{\rm out}=B_{m+1}^{\rm in}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0010

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 \exp\!\left[-\frac{i\pi}{2}(I-P)\right]=P.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0011

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:52`
- Строки: `52--54`

```latex
\begin{equation}
 V_{\rm bal}=(I_{21}\otimes W_1W_0)U_{\rm col}^{(A_0)}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0012

- Источник: `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex:59`
- Строки: `59--65`

```latex
\begin{equation}
 \Tr_{A,B}\!\left[
 V_{\rm bal}^{,n}
 (\rho_0\otimes\omega_A\otimes\omega_B)
 V_{\rm bal}^{-n}\right]
 =\Phi_h^n(\rho_0)
\end{equation}
```

## `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0013

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:7`
- Строки: `7--11`

```latex
\begin{equation}
 T_u=\exp(u\mathcal L_{q\ell}),
 \qquad u\geq0.
 \label{eq:v8-dimensionless-lindblad-flow}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0014

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 \mathcal L_{q\ell}\longmapsto\kappa\mathcal L_{q\ell}
 \label{eq:v8-rate-rescaling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0015

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 i[-\log\rho_*,X]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0016

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 \rho_{q\ell}=aP_q+bP_\ell,
 \qquad a,b>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0017

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 [\log\rho_{q\ell},P_q]
 = [\log\rho_{q\ell},P_\ell]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0018

- Источник: `s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 p=\frac{u}{n},\qquad n\longrightarrow\infty.
 \label{eq:v8-fresh-ancilla-scaling}
\end{equation}
```

## `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0019

- Источник: `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex:8`
- Строки: `8--13`

```latex
\begin{equation}
 \Spec(-\mathcal L_{q\ell})=
 \{0^{46},(1/2)^{48},1^{62},(3/2)^{20},2^8,(5/2)^{12},
 3^8,(7/2)^{12},4^4,8\}.
 \label{eq:v8-lcf-noise-clock-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0020

- Источник: `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex:16`
- Строки: `16--18`

```latex
\begin{equation}
 T_u=\exp(u\mathcal L_{q\ell}),\qquad u\ge0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0021

- Источник: `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex:26`
- Строки: `26--28`

```latex
\begin{equation}
 \rho=aP_q/12+bP_\ell/9
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0022

- Источник: `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
 \Tr\!\left(\mathcal L_{q\ell}(P_q)^*
                  \mathcal L_{q\ell}(P_q)\right)=72,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0023

- Источник: `s2t/gates/version8_intrinsic_noise_clock_lcf_migration_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 \lim_{n\to\infty}\Phi_{u/n}^{,n}=\exp(u\mathcal L_{q\ell}).
 \label{eq:v8-lcf-collision-limit}
\end{equation}
```

## `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0024

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:7`
- Строки: `7--12`

```latex
\begin{equation}
 S_B(A)=\|AA^*B(A)-B(A)A^*A\|^2,
 \qquad
 B(A)=\Gamma_tA-A\Gamma_s.
 \label{eq:v8-isotypic-action-recall}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0025

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:15`
- Строки: `15--19`

```latex
\begin{equation}
 S_{\rm VII}+\kappa S_B,
 \qquad \kappa\geq0,
 \label{eq:v8-old-slice-isotypic-extension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0026

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 \mathcal T_{15}=\mathcal I_5\oplus\mathcal H_{10},
 \label{eq:v8-incidence-heavy-complex-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0027

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 \operatorname{sig}H_{\rm Gram}^{0}=(30,0,0),
 \qquad
 \operatorname{sig}H_{\rm Gram}^{*}=(0,2,28).
 \label{eq:v8-full-transfer-gram-signatures-again}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0028

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:63`
- Строки: `63--69`

```latex
\begin{align}
 H_0(m_I,m_H)
 &=-m_IP_I+m_H(1-P_I)+\frac12H_{\rm Gram}^{0},\label{eq:v8-full-origin-two-mass-completion}\\
 H_*(m_I,m_H)
 &=2m_IP_I+m_H(1-P_I)+\frac12H_{\rm Gram}^{*}+H_B.
 \label{eq:v8-full-vacuum-two-mass-completion}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0029

- Источник: `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex:71`
- Строки: `71--78`

```latex
\begin{equation}
 \operatorname{sig}H_0=(10,0,20),
 \qquad
 \operatorname{sig}H_*=(0,0,30),
 \qquad
 \lambda_{\min}(H_*)=5.53437\ldots.
 \label{eq:v8-full-transfer-qualitative-transition}
\end{equation}
```

## `s2t/gates/version8_kms_nontracial_relative_rate_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0030

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_lcf_migration_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
 \rho_*=I_{21}/21.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0031

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_lcf_migration_gate.tex:14`
- Строки: `14--16`

```latex
\begin{equation}
 13\kappa_L+6\kappa_Q+6\kappa_X>0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0032

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_lcf_migration_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 \gamma_\uparrow/\gamma_\downarrow=e^{-\beta\Delta},
\end{equation}
```

## `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0033

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:9`
- Строки: `9--14`

```latex
\begin{equation}
 \rho_{a,b}=aI_{11}\oplus bI_{10},
 \qquad a,b>0,
 \qquad 11a+10b=1.
 \label{eq:v8-central-kms-state}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0034

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 \rho_*=\frac{I_{21}}{21}.
 \label{eq:v8-unique-tracial-kms-state}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0035

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:28`
- Строки: `28--33`

```latex
\begin{equation}
 \rho_{a,b}\ \hbox{стационарно}
 \quad\Longleftrightarrow\quad
 a=b=\frac1{21}.
 \label{eq:v8-central-kms-only-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0036

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:37`
- Строки: `37--39`

```latex
\begin{equation}
 G_{a,b}=aI_{121}\oplus bI_{100}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0037

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:46`
- Строки: `46--49`

```latex
\begin{equation}
 13,\qquad 6,\qquad 6.
 \label{eq:v8-positive-transfer-traces}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0038

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:56`
- Строки: `56--58`

```latex
\begin{equation}
 H_\Delta=0\cdot P_{11}+\Delta P_{10}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0039

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:62`
- Строки: `62--67`

```latex
\begin{equation}
 [H_\Delta,V]=\Delta V,
 \qquad
 [H_\Delta,V^*]=-\Delta V^*.
 \label{eq:v8-directed-bohr-split}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0040

- Источник: `s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex:71`
- Строки: `71--76`

```latex
\begin{equation}
 \frac{\gamma_\uparrow}{\gamma_\downarrow}
 =e^{-\beta\Delta}
 =\frac ba.
 \label{eq:v8-kms-directed-rate-ratio}
\end{equation}
```

## `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0041

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex:14`
- Строки: `14--20`

```latex
\begin{equation}
 E_{q\ell}(z)
 =-\langle Q,\mathcal L_zQ\rangle,
 \qquad
 \mathcal L_z=\sum_a z_a^2\mathcal L_a.
 \label{eq:v8-field-dependent-kraus-dirichlet}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0042

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex:22`
- Строки: `22--27`

```latex
\begin{equation}
 E_{q\ell}(z)=\frac7{36}\sum_{a=1}^{12}z_a^2,
 \qquad
 \Hess E_{q\ell}=\frac7{18}I_{12}.
 \label{eq:v8-cross-dirichlet-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0043

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{\rm origin}=(7,0,20),
 \qquad
 (n_-,n_0,n_+)_{\rm vac}=(0,0,27).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0044

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex:50`
- Строки: `50--56`

```latex
\begin{equation}
 z_a=0\quad\Longrightarrow\quad
 \mathcal L_z=0,
 \qquad
 \Gamma_{q\ell}^{\rm tree}=0.
 \label{eq:v8-tree-kraus-rate-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0045

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex:65`
- Строки: `65--68`

```latex
\begin{equation}
 \Gamma_{q\ell}(c_Q,c_X)=\frac76(c_Q+c_X).
 \label{eq:v8-kraus-rate-covariance-scale}
\end{equation}
```

## `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0046

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex:8`
- Строки: `8--10`

```latex
\begin{equation}
 -\langle Q,\mathcal L_aQ\rangle=\frac7{36}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0047

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex:12`
- Строки: `12--17`

```latex
\begin{equation}
 E_{q\ell}(z)=\frac7{36}\sum_{a=1}^{12}z_a^2,
 \qquad
 \Hess E_{q\ell}=\frac7{18}I_{12}.
 \label{eq:v8-lcf-kraus-parent-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0048

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex:29`
- Строки: `29--35`

```latex
\begin{equation}
 \operatorname{sign}H_0(\lambda)=(7,0,20),
 \qquad
 \operatorname{sign}H_*(\lambda)=(0,0,27),
 \qquad \lambda\ge0.
 \label{eq:v8-lcf-kraus-parent-signatures}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0049

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex:40`
- Строки: `40--46`

```latex
\begin{equation}
 E_{q\ell}(0)=0,
 \qquad
 \nabla E_{q\ell}(0)=0,
 \qquad
 (z_0^2,\ldots,z_{11}^2)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0050

- Источник: `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex:53`
- Строки: `53--55`

```latex
\begin{equation}
 \Gamma_{q\ell}=\frac76(c_Q+c_X).
\end{equation}
```

## `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-04-0051

- Источник: `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex:10`
- Строки: `10--13`

```latex
\begin{equation}
 \dim E_t\times\dim E_s.
 \label{eq:v8-proofdsl-morphism-shape}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0052

- Источник: `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 \rho_t(X)J-J\rho_s(X)=0
 \label{eq:v8-proofdsl-intertwiner-rule}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0053

- Источник: `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex:46`
- Строки: `46--51`

```latex
\begin{equation}
 \dim\operatorname{Hom}_G(E_{21},T_{20})=13,
 \qquad
 \max\rank J=2\min(3,4)+3\min(1,1)=9<20.
 \label{eq:v8-proofdsl-connector-exact}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-04-0054

- Источник: `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex:57`
- Строки: `57--63`

```latex
\begin{equation}
 \left.\frac{\partial^2\mathcal F_\beta}{\partial a^2}\right|_{a=1/3}
 =\frac92-\frac{3\beta}{7},
 \qquad
 \beta_{\rm sp}=\frac{21}{2}.
 \label{eq:v8-proofdsl-spinodal-exact}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]