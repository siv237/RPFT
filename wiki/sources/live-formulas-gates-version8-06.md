# Гейты Version 8 — часть 6

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **68** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_modular_bohr_parent_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0001

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:26`
- Строки: `26--29`

```latex
\begin{equation}
 N=\operatorname{diag}(0I_{11},I_{21},2I_{10}).
 \label{eq:v8-chain-number-full}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0002

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
 N_{\partial}=0I_{11}\oplus2I_{10}.
 \label{eq:v8-chain-number-endpoint}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0003

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:37`
- Строки: `37--42`

```latex
\begin{equation}
 [N_{\partial},V]=2V,
 \qquad
 [N_{\partial},V^*]=-2V^*.
 \label{eq:v8-chain-number-bohr-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0004

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:47`
- Строки: `47--53`

```latex
\begin{equation}
 \rho_N=\frac{e^{-N_{\partial}}}{\Tr e^{-N_{\partial}}}
 =aI_{11}\oplus bI_{10},
 \qquad
 \frac ba=e^{-2},
 \label{eq:v8-chain-number-gibbs-state}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0005

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:55`
- Строки: `55--58`

```latex
\begin{equation}
 \frac{\gamma_\uparrow}{\gamma_\downarrow}=e^{-2}.
 \label{eq:v8-chain-number-rate-ratio}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0006

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:66`
- Строки: `66--72`

```latex
\begin{align}
 \dim\ker\mathcal L_N&=1,
 &\lambda_{\rm gap}&=0.0212599674\ldots,\nonumber\\
 \Pr(\mathbb C^{11})&=0.8904465168\ldots,
 &\Pr(\mathbb C^{10})&=0.1095534832\ldots.
 \label{eq:v8-chain-number-forward-process}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0007

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:83`
- Строки: `83--86`

```latex
\begin{equation}
 N\longmapsto2I-N.
 \label{eq:v8-chain-number-reversal}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0008

- Источник: `s2t/gates/version8_modular_bohr_parent_origin_gate.tex:89`
- Строки: `89--91`

```latex
\begin{equation}
 \frac{b_{\rm rev}}{a_{\rm rev}}=e^2.
\end{equation}
```

## `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0009

- Источник: `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex:8`
- Строки: `8--11`

```latex
\begin{equation}
 P_X=I_4-X^*(XX^*)^{-1}X.
 \label{eq:v8-moving-kernel-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0010

- Источник: `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex:14`
- Строки: `14--19`

```latex
\begin{equation}
 \nabla P_X=B_X+B_X^*,
 \qquad
 B_X=(I-P_X)(\nabla P_X)P_X.
 \label{eq:v8-moving-kernel-second-form}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0011

- Источник: `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 B_X\widehat\otimes I_{\mathcal Y_{\rm phys}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0012

- Источник: `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex:43`
- Строки: `43--52`

```latex
\begin{equation}
 X_\varepsilon(x)=
 \begin{pmatrix}
  1&0&0&0\\
  0&1&0&0\\
  0&0&\varepsilon\cos(x/\varepsilon)&
       \varepsilon\sin(x/\varepsilon)
 \end{pmatrix}.
 \label{eq:v8-moving-kernel-singular-path}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0013

- Источник: `s2t/gates/version8_moving_kernel_second_fundamental_form_gate.tex:55`
- Строки: `55--59`

```latex
\begin{equation}
 \|B_{X_\varepsilon}(0)\|=\frac1{\varepsilon},
 \qquad
 \|B_{X_\varepsilon}(0)\|^2=\frac1{\varepsilon^2}.
\end{equation}
```

## `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0014

- Источник: `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 2.21094673.
 \label{eq:v8-selected-noise-gauge-leakage}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0015

- Источник: `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex:37`
- Строки: `37--40`

```latex
\begin{equation}
 \dim_{\mathbb C}\mathcal N_{\rm tr}^{\rm gauge}=5+10=15.
 \label{eq:v8-full-gauge-transfer-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0016

- Источник: `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex:45`
- Строки: `45--48`

```latex
\begin{equation}
 \boxed{\dim_{\mathbb C}\mathcal N_{\rm full}=15+12=27.}
 \label{eq:v8-full-gauge-noise-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0017

- Источник: `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex:57`
- Строки: `57--62`

```latex
\begin{equation}
 \dim\operatorname{Comm}_{19}=10,
 \qquad
 \dim\operatorname{Comm}_{27}=16.
 \label{eq:v8-noise-symmetry-commutants}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0018

- Источник: `s2t/gates/version8_noise_isotropy_symmetry_admission_gate.tex:67`
- Строки: `67--71`

```latex
\begin{equation}
 G_\eta=\eta P_{\rm tr}+P_{\rm gauge},
 \qquad \eta>0.
 \label{eq:v8-symmetry-invariant-noise-family}
\end{equation}
```

## `s2t/gates/version8_page_wootters_stinespring_history_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0019

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:8`
- Строки: `8--11`

```latex
\begin{equation}
 \sum_{a=0}^{12}K_a^*K_a=I_{21}.
 \label{eq:v8-pw-kraus-completeness}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0020

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:13`
- Строки: `13--17`

```latex
\begin{equation}
 W\psi=\sum_{a=0}^{12}K_a\psi\otimes|a\rangle,
 \qquad W^*W=I_{21}.
 \label{eq:v8-pw-stinespring-isometry}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0021

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:22`
- Строки: `22--26`

```latex
\begin{equation}
 |\mathsf H_2(\psi)\rangle=
 \frac1{\sqrt3}\sum_{n=0}^{2}|n\rangle_C\otimes W_n\cdots W_1\psi.
 \label{eq:v8-pw-history-state}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0022

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 1,\qquad13,\qquad13^2=169.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0023

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:37`
- Строки: `37--44`

```latex
\begin{equation}
 \Tr_{E_1\cdots E_n}
 \left({}_C\langle n|\mathsf H_2\rangle
       \langle\mathsf H_2|n\rangle_C\right)
 =\frac13\Phi_{p,*}^{,n}(\rho_0),
 \qquad n=0,1,2.
 \label{eq:v8-pw-conditional-recovery}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0024

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 21\cdot13^2=3549,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0025

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 \psi_{n+1}=W_{n+1}\psi_n
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0026

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 H_{\rm hist}|\mathsf H_2(\psi)\rangle=0.
 \label{eq:v8-pw-stationary-history}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0027

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:74`
- Строки: `74--76`

```latex
\begin{equation}
 273-21=252,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0028

- Источник: `s2t/gates/version8_page_wootters_stinespring_history_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 \Phi_{u/n,*}^{,n}\longrightarrow e^{u\mathcal L_*}
\end{equation}
```

## `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0029

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:9`
- Строки: `9--13`

```latex
\begin{equation}
 \mathcal E_{\rm new}=\bigoplus_{e\in E_{\rm new}}
 \operatorname{Hom}(\mathcal H_{s(e)},\mathcal H_{t(e)}),
 \qquad \dim_{\mathbb C}\mathcal E_{\rm new}=36,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0030

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:24`
- Строки: `24--26`

```latex
\begin{equation}
 \dim_{\mathbb C}\operatorname{Hom}_G(\mathcal E_{\rm new},H_{21})=10.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0031

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 \dim_{\mathbb C}\operatorname{Hom}_G(
 \mathcal E_{\rm new}\oplus J\mathcal E_{\rm new},H_{21})=14.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0032

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 Y_R\longrightarrow Q_L
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0033

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
 (mathbf3,mathbf1,2/3),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0034

- Источник: `s2t/gates/version8_physical_arrow_endpoint_intertwiner_classification_gate.tex:50`
- Строки: `50--54`

```latex
\begin{equation}
 \dim_{\mathbb C}\operatorname{Hom}_G(
 J\mathcal E_* ,H_{21})=1.
 \label{eq:v8-unique-real-selected-intertwiner}
\end{equation}
```

## `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0035

- Источник: `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 \Sigma=H^{-1}.
 \label{eq:v8-parent-equilibrium-covariance}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0036

- Источник: `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex:18`
- Строки: `18--25`

```latex
\begin{equation}
 A=MH,
 \qquad
 \mathcal C_\tau=e^{-\tau A},
 \qquad
 A\Sigma+\Sigma A^{*}=2M.
 \label{eq:v8-parent-mobility-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0037

- Источник: `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex:35`
- Строки: `35--42`

```latex
\begin{equation}
 H_{QX}=
 \begin{pmatrix}
 0.92492997&-0.44926187\\
 -0.44926187&0.58178422
 \end{pmatrix}.
 \label{eq:v8-parent-qx-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0038

- Источник: `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 \frac1{15}(4,1,1,1,4,4)
 \quad\hbox{и}\quad
 \frac1{15}(1,4,4,4,1,1).
 \label{eq:v8-parent-distinct-mobilities}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0039

- Источник: `s2t/gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex:66`
- Строки: `66--68`

```latex
\begin{equation}
 0.91681,qquad 0.95737,qquad 0.58000,
\end{equation}
```

## `s2t/gates/version8_polar_morita_connector_admission_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0040

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:7`
- Строки: `7--9`

```latex
\begin{equation}
 M_{22}(\mathbb C)\oplus M_{21}(\mathbb C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0041

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:14`
- Строки: `14--17`

```latex
\begin{equation}
 T_0=\operatorname{diag}(I_{11},U^*),
 \label{eq:v8-polar-formal-connector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0042

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:22`
- Строки: `22--26`

```latex
\begin{equation}
 T_0^*T_0=I_{21},\qquad
 T_0T_0^*=I_{11}\oplus P,
 \qquad I_{11}-P=Q,\quad\rank Q=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0043

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:33`
- Строки: `33--38`

```latex
\begin{equation}
 \mathcal K_E=\mathbb C^{E_{\rm new}}\oplus
              \mathbb C^{E_{\rm new}},
 \qquad |E_{\rm new}|=11.
 \label{eq:v8-polar-edge-label-space}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0044

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:41`
- Строки: `41--47`

```latex
\begin{equation}
 \mathcal E_{\rm new}
 =\bigoplus_{e\in E_{\rm new}}
   \operatorname{Hom}(\mathcal H_{s(e)},\mathcal H_{t(e)}),
 \qquad \dim_{\mathbb C}\mathcal E_{\rm new}=36.
 \label{eq:v8-polar-full-arrow-module}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0045

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
 \mathcal K_V=\mathbb C^{11}_{\rm state}\oplus\mathbb C^{10}_{\rm state},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0046

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:54`
- Строки: `54--58`

```latex
\begin{equation}
 \mathbb C^{11}_{\rm state}
 =Q_L^{(6)}\oplus L_L^{(2)}\oplus X_L^{(1)}\oplus Y_L^{(2)}.
 \label{eq:v8-polar-left-state-space}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0047

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:67`
- Строки: `67--73`

```latex
\begin{equation}
 T_j=\operatorname{diag}(j,jU^*),
 \qquad
 j:\mathbb C^{11}_{\rm state}\longrightarrow
       \mathbb C^{E_{\rm new}}.
 \label{eq:v8-polar-j-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0048

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 \dim_{\mathbb R}U(11)=121.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0049

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:84`
- Строки: `84--90`

```latex
\begin{equation}
 X_ET_j-T_jX_V
 =\begin{pmatrix}0&0\\jQ&0\end{pmatrix},
 \qquad
 \|X_ET_j-T_jX_V\|_{\rm HS}=1.
 \label{eq:v8-polar-j-independent-defect}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0050

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:105`
- Строки: `105--107`

```latex
\begin{equation}
 E_{ap}T_jE_{qb}=(T_j)_{pq}E_{ab},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0051

- Источник: `s2t/gates/version8_polar_morita_connector_admission_gate.tex:111`
- Строки: `111--113`

```latex
\begin{equation}
 \operatorname{Alg}^*(M_{22}\oplus M_{21},T_j,T_j^*)=M_{43}(\mathbb C).
\end{equation}
```

## `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0052

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:8`
- Строки: `8--11`

```latex
\begin{equation}
 X\in\operatorname{Hom}(\mathbb C^2_{Y_R},
 \mathbb C^3_c\otimes\mathbb C^2_w)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0053

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 J(X)=\frac1{\sqrt2}\Tr_wX\in\mathbb C^3_{u_R}.
 \label{eq:v8-qlyr-weak-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0054

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:18`
- Строки: `18--20`

```latex
\begin{equation}
 JJ^*=I_3,\qquad J^*J=P_{(\mathbf1_w)},\qquad\rank P_{(\mathbf1_w)}=3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0055

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 \mathbb J=\begin{pmatrix}0&J^*\\J&0\end{pmatrix}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0056

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:29`
- Строки: `29--31`

```latex
\begin{equation}
 \mathbb J^2=P_{(\mathbf1_w)}\oplus I_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0057

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 Q_L--Y_R
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0058

- Источник: `s2t/gates/version8_qlyr_ur_real_connector_lift_gate.tex:44`
- Строки: `44--47`

```latex
\begin{equation}
 J P_G=0.
 \label{eq:v8-qlyr-color-projection-zero}
\end{equation}
```

## `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0059

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 A:\mathbb C^{11}\longrightarrow\mathbb C^{10}.
 \label{eq:v8-real-oriented-transfer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0060

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 A^*:\mathbb C^{10}\longrightarrow\mathbb C^{11}.
 \label{eq:v8-real-opposite-transfer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0061

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 \mathcal T_{15}\oplus\overline{\mathcal T}_{15},
 \qquad
 J(A,\overline B)=(B,\overline A).
 \label{eq:v8-real-transfer-doubling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0062

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:33`
- Строки: `33--36`

```latex
\begin{equation}
 \dim_{\mathbb C}\operatorname{End}_G(\mathcal T_{(1,0)})=10.
 \label{eq:v8-real-degenerate-block-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0063

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 P_I(\theta)=e^{i\theta K}P_Ie^{-i\theta K}.
 \label{eq:v8-real-compatible-projector-orbit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0064

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:54`
- Строки: `54--58`

```latex
\begin{equation}
 \widehat P(\theta)
 =\operatorname{diag}\bigl(P_I(\theta),\overline{P_I(\theta)}\bigr).
 \label{eq:v8-real-doubled-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0065

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:60`
- Строки: `60--63`

```latex
\begin{equation}
 J\widehat P(\theta)J^{-1}=\widehat P(\theta)
 \label{eq:v8-real-projector-compatibility}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0066

- Источник: `s2t/gates/version8_real_incidence_multiplicity_quotient_gate.tex:69`
- Строки: `69--74`

```latex
\begin{equation}
 \frac12\Tr\operatorname{diag}(X,\overline X)^*
                 \operatorname{diag}(X,\overline X)
 =\Tr X^*X.
 \label{eq:v8-real-half-trace-uniform-again}
\end{equation}
```

## `s2t/gates/version8_second_family_tensor_inheritance_no_go_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-06-0067

- Источник: `s2t/gates/version8_second_family_tensor_inheritance_no_go_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 \Tr D_F^4=104+16\cos\theta\,\Tr(P_-H_uH_d),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-06-0068

- Источник: `s2t/gates/version8_second_family_tensor_inheritance_no_go_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 K_s=\frac{[Z_{4,s},Z_{6,s}]}{2i}.
 \label{eq:v8-moment-commutator-candidate}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]