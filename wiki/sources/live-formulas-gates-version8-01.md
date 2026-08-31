# Гейты Version 8 — часть 1

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **68** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0001

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:13`
- Строки: `13--22`

```latex
\begin{equation}
 a=\frac1{11+10x},
 \qquad
 b=\frac{x}{11+10x},
 \qquad
 11a+10b=1,
 \qquad
 \frac ba=x.
 \label{eq:v8-baryon-kms-density}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0002

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:24`
- Строки: `24--40`

```latex
\begin{align}
 \kappa_L&=\frac1{13(a+b)}
 =\frac{10x+11}{13(x+1)},
 &
 \kappa_{3}&=\frac1{a+b}
 =\frac{10x+11}{x+1},
 \nonumber\\
 \kappa_{2}&=\frac1{(5a+b)/2}
 =\frac{20x+22}{x+5},
 &
 \kappa_{1}&=\frac1{(13a+25b)/6}
 =\frac{60x+66}{25x+13},
 \nonumber\\
 \kappa_Q&=\kappa_X=\frac1{2(a+b)}
 =\frac{10x+11}{2(x+1)}.
 \label{eq:v8-baryon-six-exact-weights}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0003

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:64`
- Строки: `64--70`

```latex
\begin{equation}
 v_\eta(x,\eta)=
 \frac{104(25x^2+38x+13)}
 {425\eta x^3+2346\eta x^2+1105\eta x
  +3692x^2+12584x+5564}.
 \label{eq:v8-baryon-geta-value}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0004

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:72`
- Строки: `72--78`

```latex
\begin{equation}
 \frac{\partial v_\eta}{\partial\eta}
 =-\frac{1768x(x+1)(x+5)(25x+13)^2}
 {\left(425\eta x^3+2346\eta x^2+1105\eta x
 +3692x^2+12584x+5564\right)^2}<0
 \label{eq:v8-baryon-geta-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0005

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:83`
- Строки: `83--86`

```latex
\begin{equation}
 v_{\rm ext}=\frac{293.1}{3\cdot349.0}=\frac{977}{3490}.
 \label{eq:v8-baryon-external-target}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0006

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:88`
- Строки: `88--93`

```latex
\begin{equation}
 \eta_*(x)=
 \frac{52\left(105133x^2+28806x-13799\right)}
 {16609x(x+5)(25x+13)}.
 \label{eq:v8-baryon-geta-root}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0007

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:98`
- Строки: `98--101`

```latex
\begin{equation}
 P(x)=105133x^2+28806x-13799.
 \label{eq:v8-baryon-sign-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0008

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:103`
- Строки: `103--110`

```latex
\begin{equation}
 e^2>\sum_{n=0}^{4}\frac{2^n}{n!}=7,
 \qquad
 x=e^{-2}<\frac17,
 \qquad
 P\!\left(\frac17\right)=-\frac{52768}{7}<0.
 \label{eq:v8-baryon-exp-exact-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0009

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:112`
- Строки: `112--117`

```latex
\begin{equation}
 v_{\rm ext}-\sup_{\eta>0}v_\eta
 =-\frac{P(x)}{3490(71x^2+242x+107)}>0
 \quad\text{при }x=e^{-2}.
 \label{eq:v8-baryon-geta-strict-gap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0010

- Источник: `s2t/gates/version8_baryon_canonical_weights_geta_no_go_gate.tex:119`
- Строки: `119--124`

```latex
\begin{align}
 v_1&=0.256960942726249\ldots,\nonumber\\
 \sup_{\eta>0}v_\eta&=0.263742325124295\ldots,\nonumber\\
 \eta_*&=-2.19282832819175\ldots.
 \label{eq:v8-baryon-geta-display}
\end{align}
```

## `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0011

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 E_c=\frac1{\sqrt2}\langle c|\otimes I_2,
 \qquad
 \Tr(E_c^*E_d)=\delta_{cd}.
 \label{eq:v8-baryon-qlyr-normalized-arrows}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0012

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:22`
- Строки: `22--29`

```latex
\begin{equation}
 G_c=(a+b)
 \begin{pmatrix}1&-i\\ i&1\end{pmatrix},
 \qquad
 G_c^+=\frac1{4(a+b)}
 \begin{pmatrix}1&-i\\ i&1\end{pmatrix}.
 \label{eq:v8-baryon-qlyr-gram-pseudoinverse}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0013

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:31`
- Строки: `31--35`

```latex
\begin{equation}
 C_Q=\frac1{a+b}\sum_{c=1}^{3}E_c^*E_c
 =\frac{I_6}{2(a+b)}.
 \label{eq:v8-baryon-qlyr-source-casimir}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0014

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 C_L=\frac{I_6}{13(a+b)}.
 \label{eq:v8-baryon-link-source-casimir}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0015

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:48`
- Строки: `48--53`

```latex
\begin{equation}
 J_Q^{\rm src}=xC_Q=\frac{x}{2(a+b)}I_6,
 \qquad
 J_L^{\rm src}=xC_L=\frac{x}{13(a+b)}I_6.
 \label{eq:v8-baryon-directed-source-springs}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0016

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:66`
- Строки: `66--71`

```latex
\begin{equation}
 \widetilde J_Q=\frac{x}{4(a+b)}I_6,
 \qquad
 \widetilde J_L=\frac{x}{13(a+b)}I_6.
 \label{eq:v8-baryon-supplied-transfer-springs}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0017

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:74`
- Строки: `74--79`

```latex
\begin{equation}
 \frac{J_Q^{\rm src}}{\widetilde J_Q}=2,
 \qquad
 \frac{J_L^{\rm src}}{\widetilde J_L}=1.
 \label{eq:v8-baryon-transfer-required-multipliers}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0018

- Источник: `s2t/gates/version8_baryon_directed_transfer_convention_selector_gate.tex:87`
- Строки: `87--96`

```latex
\begin{align}
 r_1^{\rm dir}
 &=\frac{(10x+11)(375x^3+3916x^2+7267x+2782)}
 {26(x+1)(x+5)(25x+13)},
 \\
 v_{\rm dir}(x)
 &=\frac{52(25x^2+38x+13)}
 {375x^3+3916x^2+7267x+2782}.
 \label{eq:v8-baryon-direct-restriction-discriminator}
\end{align}
```

## `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0019

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:9`
- Строки: `9--13`

```latex
\begin{equation}
 \Omega_E=\operatorname{diag}(m_1,\ldots,m_{20},-m_1,\ldots,-m_{20}),
 \qquad \frac12\Tr\Omega_E^2=S_E.
 \label{eq:v8-common-edge-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0020

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:15`
- Строки: `15--20`

```latex
\begin{equation}
 \Omega_G(A)=\operatorname{diag}
 \bigl(AA^*-A_0A_0^*,\;A^*A-A_0^*A_0\bigr),
 \qquad \frac12\Tr\Omega_G^2=S_G.
 \label{eq:v8-common-gram-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0021

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:22`
- Строки: `22--25`

```latex
\begin{equation}
 \Omega=\Omega_E\oplus\Omega_G
 \label{eq:v8-unweighted-common-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0022

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 J:E_t\oplus E_s\longrightarrow\mathcal T_{\rm bimod},
 \qquad \dim(E_t\oplus E_s)=21.
 \label{eq:v8-index-one-connector-candidate}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0023

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:43`
- Строки: `43--46`

```latex
\begin{equation}
 R_{\mathcal T}(X)J=J R_E(X)
 \label{eq:v8-connector-intertwiner-equation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0024

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:51`
- Строки: `51--54`

```latex
\begin{equation}
 \rank J\leq9<20
 \label{eq:v8-connector-rank-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0025

- Источник: `s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex:65`
- Строки: `65--69`

```latex
\begin{equation}
 G_\eta=P_E+\eta P_G,
 \qquad \eta>0,
 \label{eq:v8-common-central-metric-family}
\end{equation}
```

## `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0026

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:8`
- Строки: `8--13`

```latex
\begin{equation}
 E_s=Q_L\oplus L_L\oplus X_L\oplus Y_L,
 \qquad
 E_t=u_R\oplus d_R\oplus e_R\oplus X_R\oplus Y_R.
 \label{eq:v8-endpoint-bimodule-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0027

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 A\longmapsto P_t^bAP_s^a.
 \label{eq:v8-endpoint-block-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0028

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 \dim_{\mathbb C}\mathcal T_{\rm bimod}=20.
 \label{eq:v8-bimodule-transfer-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0029

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
 2\cdot20+12=52
 \label{eq:v8-bimodule-full-field-real-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0030

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:41`
- Строки: `41--45`

```latex
\begin{align}
 E_I=\{&u_RQ_L,d_RQ_L,e_RL_L,
 e_RX_L,X_RX_L,Y_RL_L,Y_RY_L\}.
 \label{eq:v8-bimodule-incidence-support}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0031

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 E_H=\{d_RX_L,e_RY_L,X_RL_L,Y_RQ_L\}.
 \label{eq:v8-bimodule-heavy-support}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0032

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:55`
- Строки: `55--58`

```latex
\begin{equation}
 \mathcal T_{\rm bimod}=\mathcal I_{10}\oplus\mathcal H_{10}.
 \label{eq:v8-bimodule-ten-plus-ten}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0033

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:69`
- Строки: `69--73`

```latex
\begin{equation}
 S_E=\sum_{a\in E_I}(|z_a|^2-1)^2
 +\sum_{b\in E_H}\bigl[(|w_b|^2+1)^2-1\bigr].
 \label{eq:v8-bimodule-common-level-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0034

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:79`
- Строки: `79--82`

```latex
\begin{equation}
 0\leq\beta<\frac23.
 \label{eq:v8-bimodule-beta-window}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0035

- Источник: `s2t/gates/version8_bimodule_multiplicity_separator_gate.tex:84`
- Строки: `84--91`

```latex
\begin{equation}
 (n_-,n_0,n_+)_{0}=(20,0,20),
 \qquad
 (n_-,n_0,n_+)_{*}=(0,0,40),
 \qquad
 \lambda_{\min}^{*}=5.773318\ldots.
 \label{eq:v8-bimodule-full-transition}
\end{equation}
```

## `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0036

- Источник: `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex:16`
- Строки: `16--19`

```latex
\begin{equation}
 \varepsilon_d\leq A e^{-cd},\qquad A,c>0.
 \label{eq:v8-quasi-ideal-clock-error}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0037

- Источник: `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex:22`
- Строки: `22--27`

```latex
\begin{equation}
 \left\|\widetilde\Phi_L-\Phi_L\right\|_\diamond
 \leq N_L\varepsilon_d
 \leq 2LAe^{-cd}.
 \label{eq:v8-clock-global-error}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0038

- Источник: `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 d\geq \frac1c\log\frac{2AL}{\delta}.
 \label{eq:v8-clock-dimension-schedule}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0039

- Источник: `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex:36`
- Строки: `36--39`

```latex
\begin{equation}
 E_d=O\!\left(\log\frac{L}{\delta}\right).
 \label{eq:v8-clock-energy-schedule}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0040

- Источник: `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex:59`
- Строки: `59--62`

```latex
\begin{equation}
 \varepsilon_{\rm loc}\leq N_{\rm loc}Ae^{-cd},
 \label{eq:v8-clock-local-observable-error}
\end{equation}
```

## `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0041

- Источник: `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 W:\mathbb C^{21}\longrightarrow\mathbb C^{21}\otimes\mathbb C^{13}
 =\mathbb C^{273}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0042

- Источник: `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 U_0(\psi\otimes|0\rangle)=W\psi
 \label{eq:v8-clock-unitary-extension-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0043

- Источник: `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex:27`
- Строки: `27--31`

```latex
\begin{equation}
 V_z=P_W+z(I-P_W),
 \qquad U_z=V_zU_0.
 \label{eq:v8-clock-complement-phase-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0044

- Источник: `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex:33`
- Строки: `33--37`

```latex
\begin{equation}
 V_zW=W,
 \qquad
 U_z(\psi\otimes|0\rangle)=W\psi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0045

- Источник: `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex:45`
- Строки: `45--47`

```latex
\begin{equation}
 z=+1,\qquad z=-1
\end{equation}
```

## `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0046

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:10`
- Строки: `10--13`

```latex
\begin{equation}
 G_{ab}=\Tr(\rho_N F_a^*F_b).
 \label{eq:v8-common-trace-noise-gram}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0047

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:26`
- Строки: `26--33`

```latex
\begin{equation}
 \dim_{\mathbb C}\mathcal N_{\rm tr}=7,
 \qquad
 \dim_{\mathbb C}\mathcal N_{\rm gauge}=12,
 \qquad
 \dim_{\mathbb C}\mathcal N=19.
 \label{eq:v8-common-trace-noise-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0048

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:41`
- Строки: `41--49`

```latex
\begin{equation}
 \mathcal L_{\rm tr}=
 \sum_{a=1}^{7}\mathcal D^{\rm KMS}_{W_a},
 \qquad
 \mathcal L_{\rm gauge}=\sum_{b=1}^{12}\mathcal D_{T_b},
 \qquad
 \mathcal L_{\rm can}=\mathcal L_{\rm tr}+\mathcal L_{\rm gauge}.
 \label{eq:v8-canonical-noise-casimir}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0049

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:58`
- Строки: `58--64`

```latex
\begin{align}
 \dim\ker\mathcal L_{\rm can}&=1,\\
 \operatorname{gap}(-\mathcal L_{\rm can})&=0.0207491297,\\
 \|G\mathcal L_{\rm can}-\mathcal L_{\rm can}^*G\|
 &=3.40\cdot10^{-17}.
 \label{eq:v8-canonical-noise-generator-diagnostics}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0050

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:71`
- Строки: `71--75`

```latex
\begin{equation}
 (0.83698439,\ 10.88079708,\ 4.81111832,\ 4.52410355,\
 5.44039854,\ 5.44039854).
 \label{eq:v8-canonical-trace-family-weights}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0051

- Источник: `s2t/gates/version8_canonical_noise_frame_common_trace_gate.tex:77`
- Строки: `77--81`

```latex
\begin{equation}
 (0.0262100,\ 0.3407298,\ 0.1506591,\ 0.1416713,\
 0.1703649,\ 0.1703649).
 \label{eq:v8-canonical-trace-normalized-weights}
\end{equation}
```

## `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0052

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:14`
- Строки: `14--19`

```latex
\begin{equation}
 U:\mathbb C^{11}\longrightarrow\mathbb C^{10},
 \qquad UU^*=I_{10},
 \qquad \dim\ker U=1,
 \qquad \dim\ker U^*=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0053

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 \operatorname{ind}U=1.
 \label{eq:v8-polar-fredholm-index}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0054

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:29`
- Строки: `29--32`

```latex
\begin{equation}
 \Gamma=\operatorname{diag}(-I_{11},+I_{10}).
 \label{eq:v8-endpoint-chiral-grading}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0055

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:34`
- Строки: `34--39`

```latex
\begin{equation}
 N_{\partial}-I_{21}=\Gamma,
 \qquad
 (2I_{21}-N_{\partial})-I_{21}=-\Gamma.
 \label{eq:v8-chain-grading-dictionary}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0056

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 -\Tr\Gamma=1=\operatorname{ind}U.
 \label{eq:v8-index-grading-sign}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0057

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:52`
- Строки: `52--56`

```latex
\begin{equation}
 S_{\pm}(A)=\frac1{21}
 \left\|[d_A,d_A^*]\mp\Gamma\right\|_{\rm HS}^2.
 \label{eq:v8-two-chiral-sign-actions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0058

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 S_+(tU)=\frac{1+20(1-t^2)^2}{21}.
 \label{eq:v8-selected-radial-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0059

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:64`
- Строки: `64--66`

```latex
\begin{equation}
 S_+(U)=\frac1{21}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0060

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:71`
- Строки: `71--74`

```latex
\begin{equation}
 S_-(tU)=\frac{1+20(1+t^2)^2}{21}.
 \label{eq:v8-reversed-radial-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0061

- Источник: `s2t/gates/version8_chain_orientation_index_defect_selector_gate.tex:83`
- Строки: `83--88`

```latex
\begin{equation}
 N_{\partial}=0I_{11}\oplus2I_{10},
 \qquad
 \frac{\gamma_\uparrow}{\gamma_\downarrow}=e^{-2}.
 \label{eq:v8-index-selected-rate-ratio}
\end{equation}
```

## `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0062

- Источник: `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 H_{\rm hist}=\sqrt2\bigl(
 |1\rangle\langle0|\otimes W_0+|2\rangle\langle1|\otimes W_1+\mathrm{h.c.}
 \bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0063

- Источник: `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 A=\begin{pmatrix}0&\sqrt2&0\\ \sqrt2&0&\sqrt2\\0&\sqrt2&0\end{pmatrix},
 \qquad A^3=4A.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0064

- Источник: `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex:23`
- Строки: `23--27`

```latex
\begin{equation}
 e^{-i\tau H_{\rm hist}}
 (|0\rangle\otimes|\psi\rangle)
 =-|2\rangle\otimes W_1W_0|\psi\rangle.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0065

- Источник: `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex:40`
- Строки: `40--42`

```latex
\begin{equation}
 J_t=\sqrt{(t+1)(T-t)},\qquad J_{\max}\geq T/2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0066

- Источник: `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex:44`
- Строки: `44--46`

```latex
\begin{equation}
 \tau_{\rm tr}\geq\frac{\pi T}{4}=\frac{\pi L}{2}.
\end{equation}
```

## `s2t/gates/version8_clock_energy_anchor_candidate_audit_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-01-0067

- Источник: `s2t/gates/version8_clock_energy_anchor_candidate_audit_gate.tex:5`
- Строки: `5--7`

```latex
\begin{equation}
 \Gamma=\chi^2\frac{E_C}{\hbar}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-01-0068

- Источник: `s2t/gates/version8_clock_energy_anchor_candidate_audit_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 E_{\rm candidate}\longmapsto
 (E_C,E_{\rm int})
 \quad\text{с}\quad E_{\rm int}=\chi E_C.
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]