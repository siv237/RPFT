# Гейты Version 8 — часть 3

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **51** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_full_noise_physical_time_scale_no_go_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0001

- Источник: `s2t/gates/version8_full_noise_physical_time_scale_no_go_gate.tex:6`
- Строки: `6--10`

```latex
\begin{equation}
 H_{\rm int}^{42}\longmapsto gH_{\rm int}^{42},
 \qquad
 \mathcal L_{42}\longmapsto g^2\mathcal L_{42}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0002

- Источник: `s2t/gates/version8_full_noise_physical_time_scale_no_go_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 t_{\rm phys}\longmapsto \frac{t_{\rm phys}}{g^2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0003

- Источник: `s2t/gates/version8_full_noise_physical_time_scale_no_go_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 t_*=\frac{\hbar}{E_*},
 \qquad E_*t_*=\hbar,
\end{equation}
```

## `s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0004

- Источник: `s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex:6`
- Строки: `6--10`

```latex
\begin{equation}
 \mathcal K_{42}=\mathbb C|0\rangle\oplus
 \operatorname{span}\{|a\rangle:a=1,\ldots,42\},
 \qquad \dim\mathcal K_{42}=43,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0005

- Источник: `s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 H_{\rm int}^{42}=\sum_{a=1}^{42}F_a\otimes
 (|a\rangle\langle0|+|0\rangle\langle a|).
\end{equation}
```

## `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0006

- Источник: `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex:5`
- Строки: `5--7`

```latex
\begin{equation}
 Ne_n=ne_n,\qquad U^ke_n=e_{n+k},\qquad [N,U^k]=kU^k
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0007

- Источник: `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex:10`
- Строки: `10--13`

```latex
\begin{equation}
 \mathcal K_{\rm cell}=\mathbb C^{43}
 =\mathbb C|0\rangle\oplus\mathbb C^{42}_{\rm jump}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0008

- Источник: `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 \mathcal K_{\rm chain}
 =\bigotimes_{m\in\mathbb Z}(\mathcal K_{\rm cell},|0\rangle).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0009

- Источник: `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex:23`
- Строки: `23--25`

```latex
\begin{equation}
 V=(I_{21}\otimes S_{\rm chain})U_{\rm col}^{(0)}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0010

- Источник: `s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex:33`
- Строки: `33--37`

```latex
\begin{equation}
 \Tr_{\rm chain}\!\left[
 V^n(\rho_0\otimes\omega_{\rm vac})V^{-n}\right]
 =\Phi_h^n(\rho_0).
\end{equation}
```

## `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0011

- Источник: `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
 1\longrightarrow4\longrightarrow5\longrightarrow5.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0012

- Источник: `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 \mathcal F_{\rm noise}=\{F_a\}_{a=1}^{42}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0013

- Источник: `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 K_{ab}=\Tr(F_a^*F_b),
 \qquad \rank K=42.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0014

- Источник: `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 R_{\rm tr}=K^{-1},\qquad KR_{\rm tr}=I_{42}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0015

- Источник: `s2t/gates/version8_full_noise_trace_frame_metric_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 17=9_{\rm linking\ orbit}+8_{\rm internal\ transfer}.
\end{equation}
```

## `s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0016

- Источник: `s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex:8`
- Строки: `8--17`

```latex
\begin{equation}
 \mathcal L_{\rm full}
 =\mathcal L_{\rm link}
 +\mathcal L_{SU(3)}
 +\mathcal L_{SU(2)}
 +\mathcal L_{U(1)}
 +\mathcal L_{QLYR}
 +\mathcal L_{XLdR}.
 \label{eq:v8-full-primitive-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0017

- Источник: `s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 \mathcal A_{\rm obs}=M_{11}(\mathbb C)\oplus M_{10}(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0018

- Источник: `s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 \ker\mathcal L_{\rm full}=\mathbb CI_{21}.
 \label{eq:v8-full-generator-scalar-kernel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0019

- Источник: `s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex:53`
- Строки: `53--58`

```latex
\begin{equation}
 \mathcal L_{\boldsymbol\kappa}
 =\sum_r\kappa_r\mathcal L_r,
 \qquad \kappa_r>0,
 \label{eq:v8-positive-rate-family}
\end{equation}
```

## `s2t/gates/version8_full_primitive_markov_generator_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0020

- Источник: `s2t/gates/version8_full_primitive_markov_generator_lcf_migration_gate.tex:8`
- Строки: `8--10`

```latex
\begin{equation}
 25=1+8+3+1+6+6
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0021

- Источник: `s2t/gates/version8_full_primitive_markov_generator_lcf_migration_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 \operatorname{Fix}(\mathcal L_{\rm full})=\mathbb CI_{21}.
\end{equation}
```

## `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0022

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 \mathcal T_{15}=\mathcal I_5\oplus\mathcal H_{10}
 \label{eq:v8-edge-origin-desired-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0023

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:17`
- Строки: `17--21`

```latex
\begin{equation}
 \operatorname{Spec}\mathcal C_G
 =\{0^{\times1},1^{\times8},(16/9)^{\times6}\}.
 \label{eq:v8-transfer-gauge-casimir-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0024

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 \mathcal B(A)=\Gamma_tA-A\Gamma_s
 \label{eq:v8-transfer-sector-order-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0025

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:28`
- Строки: `28--32`

```latex
\begin{equation}
 \operatorname{Spec}\mathcal B
 =\{(-2)^{\times3},0^{\times9},2^{\times3}\}.
 \label{eq:v8-transfer-sector-order-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0026

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:41`
- Строки: `41--45`

```latex
\begin{equation}
 (0,0):1,qquad (1,0):8,qquad
 (16/9,-2):3,qquad (16/9,2):3.
 \label{eq:v8-casimir-sector-joint-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0027

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 1,qquad 4,qquad0,qquad0.
 \label{eq:v8-incidence-overlap-joint-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0028

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 \|P_I-P_I^{\rm spec}\|_{\rm HS}=\sqrt2,qquad
 \|P_I-P_I^{\rm spec}\|_{\rm op}=\frac12.
 \label{eq:v8-incidence-projector-spectral-residual}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0029

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 0.4\sqrt2=0.565685\ldots.
 \label{eq:v8-two-mass-spectral-residual}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0030

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 \rho=\rho_sI_{11}\oplus\rho_tI_{10}
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0031

- Источник: `s2t/gates/version8_gauge_closed_edge_hodge_origin_gate.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 \langle A,B\rangle_\rho
 = (\rho_s+\rho_t)\Tr(A^*B).
 \label{eq:v8-common-kms-transfer-metric}
\end{equation}
```

## `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0032

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 A\in\Gamma\bigl(\operatorname{Hom}(E_s,E_t)\bigr).
 \label{eq:v8-full-transfer-field-section}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0033

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 2\cdot15+12=42
 \label{eq:v8-gauge-closed-field-real-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0034

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:28`
- Строки: `28--33`

```latex
\begin{equation}
 \rho_{\rm tr}(X_s,X_t)A=i(X_tA-AX_s),
 \qquad
 \rho_{\rm ad}(X)Y=i[X,Y].
 \label{eq:v8-field-space-infinitesimal-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0035

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:41`
- Строки: `41--48`

```latex
\begin{equation}
 \mathbb A=
 \begin{pmatrix}
  \nabla_s&A^*\\
  A&\nabla_t
 \end{pmatrix}.
 \label{eq:v8-endpoint-field-superconnection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0036

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:50`
- Строки: `50--59`

```latex
\begin{equation}
 \mathbb F=
 \begin{pmatrix}
  F_s+A^*A&\nabla A^*\\
  \nabla A&F_t+AA^*
 \end{pmatrix},
 \qquad
 \nabla A=dA+\nabla_tA-A\nabla_s.
 \label{eq:v8-endpoint-field-supercurvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0037

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:63`
- Строки: `63--68`

```latex
\begin{equation}
 1.64\cdot10^{-15},\qquad
 5.26\cdot10^{-16},\qquad
 6.31\cdot10^{-15}.
 \label{eq:v8-field-supercurvature-covariance-residuals}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0038

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:79`
- Строки: `79--82`

```latex
\begin{equation}
 \mathcal R_U(A)=AA^*U-UA^*A.
 \label{eq:v8-field-space-relative-polar-curvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0039

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:89`
- Строки: `89--92`

```latex
\begin{equation}
 U\longmapsto g_tUg_s^*,
 \label{eq:v8-moving-polar-transformation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0040

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:96`
- Строки: `96--100`

```latex
\begin{equation}
 \operatorname{Pol}(g_tA_0g_s^*)
 =g_t\operatorname{Pol}(A_0)g_s^*.
 \label{eq:v8-polar-equivariance}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0041

- Источник: `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex:104`
- Строки: `104--111`

```latex
\begin{equation}
 \operatorname{Pol}(\varepsilon A_0)=U,
 \qquad
 \operatorname{Pol}(0)=0,
 \qquad
 \|U-0\|_{\rm HS}=\sqrt{10}.
 \label{eq:v8-polar-rank-zero-jump}
\end{equation}
```

## `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0042

- Источник: `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex:7`
- Строки: `7--12`

```latex
\begin{equation}
 \mathcal N_{\rm full}
 =\mathcal N_{\rm tr}^{\rm gauge}\oplus\mathcal N_{\rm gauge},
 \qquad \dim_{\mathbb C}\mathcal N_{\rm full}=15+12=27.
 \label{eq:v8-full-noise-splitting-for-parent-test}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0043

- Источник: `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex:27`
- Строки: `27--33`

```latex
\begin{align}
 \dim_{\mathbb R}T_{\rm VII}&=27,&
 \dim_{\mathbb R}\mathcal N_{\rm tr}^{\rm gauge,\mathbb R}&=30,\\
 \dim(T_{\rm VII}\cap\mathcal N_{\rm tr}^{\rm gauge,\mathbb R})&=23,&
 \dim(T_{\rm VII}+\mathcal N_{\rm tr}^{\rm gauge,\mathbb R})&=34.
 \label{eq:v8-field-noise-space-intersection}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0044

- Источник: `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 1.47987812,
 \label{eq:v8-old-field-slice-gauge-leakage}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0045

- Источник: `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 \operatorname{sig}H_{\rm Gram}^{0}=(30,0,0),
 \qquad
 \operatorname{sig}H_{\rm Gram}^{*}=(0,2,28).
 \label{eq:v8-relative-gram-on-full-transfer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0046

- Источник: `s2t/gates/version8_gauge_closed_noise_parent_hessian_gate.tex:64`
- Строки: `64--67`

```latex
\begin{equation}
 H_{\lambda}=\frac12H_{\rm Gram}+\lambda I_{30}.
 \label{eq:v8-undetermined-transfer-mass-completion}
\end{equation}
```

## `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-03-0047

- Источник: `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 \mathcal Z_{\rm fix}=\mathbb CP_q\oplus\mathbb CP_\ell,
 \qquad (\rank P_q,\rank P_\ell)=(12,9).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0048

- Источник: `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 Q_L\longleftrightarrow Y_R,
 \qquad
 X_L\longleftrightarrow d_R,
 \label{eq:v8-existing-cross-arrow-multiplets}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0049

- Источник: `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex:32`
- Строки: `32--34`

```latex
\begin{equation}
 D_{e_a}=\begin{pmatrix}0&e_a^*\\e_a&0\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0050

- Источник: `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
 \mathcal L_{q\ell}
 =-\frac12\sum_a\operatorname{ad}_{D_{e_a}}^2.
 \label{eq:v8-gauge-twirled-kraus-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-03-0051

- Источник: `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex:56`
- Строки: `56--64`

```latex
\begin{equation}
 \begin{pmatrix}
 1&-2/\sqrt3\\
 -2/\sqrt3&4/3
 \end{pmatrix},
 \qquad
 \Spec=\left\{0,\frac73\right\}.
 \label{eq:v8-cross-kraus-central-restriction}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]