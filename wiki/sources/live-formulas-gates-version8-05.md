# Гейты Version 8 — часть 5

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **67** блочных формул из **10** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0001

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:9`
- Строки: `9--12`

```latex
\begin{equation}
 \mathcal A_{\rm end}=M_{11}(\mathbb C)\oplus M_{10}(\mathbb C),
 \label{eq:v8-endpoint-observable-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0002

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:19`
- Строки: `19--23`

```latex
\begin{equation}
 D_A=\begin{pmatrix}0&A_0^*\\A_0&0\end{pmatrix}
 \quad\text{на}\quad \mathbb C^{11}\oplus\mathbb C^{10}.
 \label{eq:v8-linking-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0003

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 \mathcal L_A(Z)=-\frac12[D_A,[D_A,Z]].
 \label{eq:v8-linking-qms-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0004

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:34`
- Строки: `34--41`

```latex
\begin{equation}
 \mathcal L_A(X,Y)=
 \left(
 A_0^*YA_0-\frac12\{A_0^*A_0,X\},
 A_0XA_0^*-\frac12\{A_0A_0^*,Y\}
 \right).
 \label{eq:v8-linking-corner-markov-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0005

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 T_t=e^{t\mathcal L_A},\qquad t\ge0,
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0006

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:52`
- Строки: `52--55`

```latex
\begin{equation}
 \exp\left[-\frac t2(\lambda_i-\lambda_j)^2\right],
 \label{eq:v8-linking-gaussian-schur-kernel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0007

- Источник: `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex:67`
- Строки: `67--71`

```latex
\begin{equation}
 \dim\ker\mathcal L_A
 =6^2+4\cdot1^2+1^2=41.
 \label{eq:v8-linking-fixed-algebra-dimension}
\end{equation}
```

## `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0008

- Источник: `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex:9`
- Строки: `9--12`

```latex
\begin{equation}
 D_A=\begin{pmatrix}0&A^*\\A&0\end{pmatrix}
 \label{eq:v8-lcf-linking-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0009

- Источник: `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex:15`
- Строки: `15--19`

```latex
\begin{equation}
 \mathcal L(Z)=D_AZD_A-\frac12\{D_A^2,Z\}
 =-\frac12[D_A,[D_A,Z]].
 \label{eq:v8-lcf-linking-gksl}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0010

- Источник: `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex:29`
- Строки: `29--35`

```latex
\begin{equation}
 \mathcal L(X,Y)=\left(
 A^*YA-\frac12\{A^*A,X\},
 AXA^*-\frac12\{AA^*,Y\}
 \right).
 \label{eq:v8-lcf-linking-corner-formula}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0011

- Источник: `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex:42`
- Строки: `42--46`

```latex
\begin{equation}
 AX=X_tA,
 \qquad
 XA^*=A^*X_t.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0012

- Источник: `s2t/gates/version8_linking_qms_gksl_lcf_migration_gate.tex:48`
- Строки: `48--51`

```latex
\begin{equation}
 221-180=41.
 \label{eq:v8-lcf-linking-fixed-forty-one}
\end{equation}
```

## `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0013

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:14`
- Строки: `14--18`

```latex
\begin{equation}
 \left\|\Phi_{u/n}^{,n}-e^{u\mathcal L_{42}}\right\|
 \leq \frac{C_u}{n}.
 \label{eq:v8-clocked-qms-collision-error}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0014

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:22`
- Строки: `22--27`

```latex
\begin{equation}
 \boxed{
 \left\|\widetilde\Phi_{u/n,d}^{,n}-e^{u\mathcal L_{42}}\right\|
 \leq \frac{C_u}{n}+nAe^{-cd}.}
 \label{eq:v8-clocked-qms-total-error}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0015

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 d_n\geq \frac{1+\alpha}{c}\log n.
 \label{eq:v8-clocked-qms-dimension-schedule}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0016

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:39`
- Строки: `39--46`

```latex
\begin{equation}
 nAe^{-cd_n}\leq \frac{A}{n^\alpha},
 \qquad
 \left\|\widetilde\Phi_{u/n,d_n}^{,n}
 -e^{u\mathcal L_{42}}\right\|
 \leq \frac{C_u}{n}+\frac{A}{n^\alpha}longrightarrow0.
 \label{eq:v8-clocked-qms-joint-limit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0017

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:66`
- Строки: `66--68`

```latex
\begin{equation}
 \Omega t_{\rm phys},\qquad \Gamma t_{\rm phys}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0018

- Источник: `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex:70`
- Строки: `70--75`

```latex
\begin{equation}
 (\Omega,\Gamma,t_{\rm phys})\longmapsto
 (\lambda\Omega,\lambda\Gamma,t_{\rm phys}/\lambda),
 \qquad \lambda>0,
 \label{eq:v8-clocked-qms-common-scale-orbit}
\end{equation}
```

## `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0019

- Источник: `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 \bigl(1^2+2^2+1^2\bigr)_{E_s}
 +\bigl(1^2+1^2+2^2+1^2\bigr)_{E_t}=13.
 \label{eq:v8-lcf-gauge-commutant-thirteen}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0020

- Источник: `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 D_A=\begin{pmatrix}0&A^*\\A&0\end{pmatrix}
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0021

- Источник: `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex:26`
- Строки: `26--31`

```latex
\begin{equation}
 AX_s=X_tA,
 \qquad
 X_sA^*=A^*X_t.
 \label{eq:v8-lcf-two-sided-linking-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0022

- Источник: `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex:38`
- Строки: `38--41`

```latex
\begin{equation}
 13-11=2.
 \label{eq:v8-lcf-fixed-nullity-two}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0023

- Источник: `s2t/gates/version8_markov_fixed_algebra_lcf_migration_gate.tex:43`
- Строки: `43--50`

```latex
\begin{equation}
 \ker=\mathbb CP_q\oplus\mathbb CP_\ell,
 \qquad
 \rank P_q=12,
 \qquad
 \rank P_\ell=9.
 \label{eq:v8-lcf-fixed-projector-ranks}
\end{equation}
```

## `s2t/gates/version8_markov_fixed_algebra_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0024

- Источник: `s2t/gates/version8_markov_fixed_algebra_selector_gate.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 \mathcal L_G=-\frac12\operatorname{ad}_G^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0025

- Источник: `s2t/gates/version8_markov_fixed_algebra_selector_gate.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 P_q=P_{Q_L}\oplus P_{u_R}\oplus P_{d_R},
 \qquad \rank P_q=6+3+3=12,
 \label{eq:v8-markov-quark-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0026

- Источник: `s2t/gates/version8_markov_fixed_algebra_selector_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 P_\ell=I-P_q,
 \qquad \rank P_\ell=9.
 \label{eq:v8-markov-lepton-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0027

- Источник: `s2t/gates/version8_markov_fixed_algebra_selector_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 \mathcal Z_{\rm fix}=\mathbb CP_q\oplus\mathbb CP_\ell\simeq\mathbb C^2.
\end{equation}
```

## `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0028

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:7`
- Строки: `7--10`

```latex
\begin{equation}
 R_{\rm tr}=K_B^{-1}=\frac13I_{12}
 \label{eq:v8-riesz-cross-rate}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0029

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:16`
- Строки: `16--20`

```latex
\begin{equation}
 S_{\rm field}^{(2)}(x)=\frac12x^TK_Bx,
 \qquad K_B=3I_{12}.
 \label{eq:v8-cross-field-parent-restriction}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0030

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:23`
- Строки: `23--27`

```latex
\begin{equation}
 S_R^{(2)}(x,\xi)
 =\frac12x^TK_Bx+\frac12\xi^TR^{-1}\xi.
 \label{eq:v8-cross-field-bath-parent-completion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0031

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:32`
- Строки: `32--38`

```latex
\begin{equation}
 R_1=\frac13I_{12},
 \qquad
 R_2=\operatorname{diag}\left(
 \frac13I_6,\frac23I_6\right).
 \label{eq:v8-two-bath-rate-completions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0032

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:40`
- Строки: `40--45`

```latex
\begin{align}
 \mathcal H_1&=\operatorname{diag}(3I_{12},3I_{12}),\\
 \mathcal H_2&=\operatorname{diag}
 \left(3I_{12},3I_6,\frac32I_6\right)
 \label{eq:v8-two-parent-hessians}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0033

- Источник: `s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 K_BR=I_{12}.
 \label{eq:v8-riesz-reciprocity-condition}
\end{equation}
```

## `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0034

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:8`
- Строки: `8--10`

```latex
\begin{equation}
 G=\sum_{a=1}^{12}D_a^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0035

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 \mathcal K_{\rm env}
 =\mathbb C|0\rangle\oplus
 \operatorname{span}_{\mathbb C}\{|a\rangle:a=1,\ldots,12\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0036

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 H_{\rm int}
 =\sum_{a=1}^{12}D_a\otimes
 \bigl(|a\rangle\langle0|+|0\rangle\langle a|\bigr).
 \label{eq:v8-star-interaction-hamiltonian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0037

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:26`
- Строки: `26--31`

```latex
\begin{equation}
 H_{\rm int}=H_{\rm int}^*,
 \qquad
 \langle0|H_{\rm int}^2|0\rangle=G.
 \label{eq:v8-star-interaction-second-moment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0038

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:36`
- Строки: `36--38`

```latex
\begin{equation}
 U_h=\exp\bigl(-i\sqrt h\,H_{\rm int}\bigr)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0039

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:41`
- Строки: `41--44`

```latex
\begin{align}
 K_0(h)&=I-\frac h2G+O(h^2),\\
 K_a(h)&=-i\sqrt h\,D_a+O(h^{3/2}).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0040

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:46`
- Строки: `46--52`

```latex
\begin{equation}
 \Psi_h(X)=X+h\mathcal L_{q\ell}(X)+O(h^2),
 \qquad
 \mathcal L_{q\ell}(X)
 =\sum_aD_aXD_a-\frac12\{G,X\}.
 \label{eq:v8-star-interaction-gksl-tangent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0041

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:55`
- Строки: `55--57`

```latex
\begin{equation}
 \lim_{n\to\infty}\Psi_{u/n}^{\,n}=e^{u\mathcal L_{q\ell}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0042

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:70`
- Строки: `70--76`

```latex
\begin{equation}
 \dim_{\mathbb R}\operatorname{Comm}_G(E_{q\ell}^{\rm cross})=8,
 \qquad
 \dim_{\mathbb R}\operatorname{Comm}^{\rm sym}_G
 (E_{q\ell}^{\rm cross})=4.
 \label{eq:v8-star-coupling-commutant-dimensions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0043

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:90`
- Строки: `90--93`

```latex
\begin{equation}
 \Phi_h(X)=\sqrt{I-hG}\,X\sqrt{I-hG}
 +h\sum_aD_aXD_a
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0044

- Источник: `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex:96`
- Строки: `96--102`

```latex
\begin{align}
 [h^2]\Psi_h(X)
 &=\frac14GXG+\frac1{24}\{G^2,X\}
   -\frac16\{G,J(X)\},\\
 [h^2]\Phi_h(X)
 &=\frac14GXG-\frac18\{G^2,X\}.
\end{align}
```

## `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0045

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:8`
- Строки: `8--10`

```latex
\begin{equation}
 G=\sum_{a=1}^{12}D_a^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0046

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:12`
- Строки: `12--17`

```latex
\begin{equation}
 K_0(p)=\sqrt{I-pG},
 \qquad
 K_a(p)=\sqrt p\,D_a.
 \label{eq:v8-one-step-stinespring-kraus}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0047

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 \Spec G=\{0^{(9)},1^{(6)},2^{(3)},3^{(2)},6^{(1)}\},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0048

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 0\leq p\leq\frac16.
 \label{eq:v8-stinespring-step-window}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0049

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 \Phi_p(X)=\sum_{a=0}^{12}K_a(p)^*XK_a(p)
 \label{eq:v8-exact-one-step-channel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0050

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:40`
- Строки: `40--47`

```latex
\begin{equation}
 \mathcal K_{\rm env}
 =\mathbb C|0\rangle\oplus
 \bigl(E_{q\ell}^{\rm cross}\otimes_{\mathbb R}\mathbb C\bigr),
 \qquad \dim_{\mathbb C}\mathcal K_{\rm env}=13,
 \quad \dim_{\mathbb R}E_{q\ell}^{\rm cross}=12.
 \label{eq:v8-minimal-environment-carrier}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0051

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex:62`
- Строки: `62--67`

```latex
\begin{equation}
 \left.\frac{d\Phi_p}{dp}\right|_{p=0}(X)
 =\sum_aD_aXD_a-\frac12\{G,X\}
 =\mathcal L_{q\ell}(X).
 \label{eq:v8-channel-generator-derivative}
\end{equation}
```

## `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0052

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:8`
- Строки: `8--10`

```latex
\begin{equation}
 \Tr(D_aD_b)=2\delta_{ab}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0053

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 \Spec G=\{0^9,1^6,2^3,3^2,6\}.
 \label{eq:v8-lcf-stinespring-gram-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0054

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 K_0(p)=\sqrt{I-pG},\qquad K_a(p)=\sqrt p\,D_a
 \label{eq:v8-lcf-stinespring-kraus-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0055

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:33`
- Строки: `33--36`

```latex
\begin{equation}
 \mathbb C\lvert0\rangle\oplus\mathcal E_{\rm cross}^{\mathbb C},
 \qquad \dim_{\mathbb R}\mathcal E_{\rm cross}=12.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0056

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:45`
- Строки: `45--47`

```latex
\begin{equation}
 K_0(0)=I,\qquad K_0'(0)=-\frac12G,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0057

- Источник: `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 \Phi_{1/50}\!\circ\Phi_{3/100}\ne\Phi_{1/20}.
\end{equation}
```

## `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-05-0058

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:15`
- Строки: `15--20`

```latex
\begin{equation}
 \mathcal K_E=\mathbb C|0\rangle\oplus\mathcal N_{42},
 \qquad
 P_E=\sum_{a=1}^{42}|a\rangle\langle a|.
 \label{eq:v8-mixed-parent-environment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0059

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 H_0=I_{21}\otimes
 \left(P_E\otimes I_C+I_E\otimes N_C\right).
 \label{eq:v8-mixed-parent-free-energy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0060

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:31`
- Строки: `31--36`

```latex
\begin{equation}
 B_a=|a\rangle\langle0|\otimes|0_C\rangle\langle1_C|,
 \qquad
 G=\sum_{a=1}^{42}F_a\otimes(B_a+B_a^*).
 \label{eq:v8-mixed-parent-interaction}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0061

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 [H_0,G]=0.
 \label{eq:v8-mixed-parent-energy-conservation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0062

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:49`
- Строки: `49--56`

```latex
\begin{equation}
 \langle\eta|G|\eta\rangle=0,
 \qquad
 \langle\eta|G^2|\eta\rangle=\sum_{a=1}^{42}F_a^2,
 \qquad
 \langle a,0_C|G|\eta\rangle=F_a.
 \label{eq:v8-mixed-parent-moments}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0063

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:74`
- Строки: `74--78`

```latex
\begin{equation}
 P_3=I_4-\frac14J_4,
 \qquad \rank P_3=3.
 \label{eq:v8-mixed-parent-affine-rank}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0064

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:82`
- Строки: `82--86`

```latex
\begin{equation}
 \dim_{\mathbb C}\operatorname{Hom}
 \left(P_3\mathbb C^4,\mathcal N_{42}\right)=3\cdot42=126.
 \label{eq:v8-mixed-parent-affine-map-freedom}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0065

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:96`
- Строки: `96--100`

```latex
\begin{equation}
 H_{\rm mix}(E_C,\chi)=E_C\left(H_0+\chi G\right),
 \qquad E_C>0,\quad\chi>0.
 \label{eq:v8-mixed-parent-dimensional-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0066

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:103`
- Строки: `103--111`

```latex
\begin{equation}
 H_{\rm mix}(\lambda E_C,\chi)=
 \lambda H_{\rm mix}(E_C,\chi),
 \qquad
 e^{-\frac{i}{\hbar}\frac{t}{\lambda}
 H_{\rm mix}(\lambda E_C,\chi)}
 =e^{-\frac{i}{\hbar}tH_{\rm mix}(E_C,\chi)}.
 \label{eq:v8-mixed-parent-scale-orbit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-05-0067

- Источник: `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex:115`
- Строки: `115--122`

```latex
\begin{equation}
 \tau_C=\frac{\hbar}{E_C},
 \qquad
 \Gamma=\chi^2\frac{E_C}{\hbar},
 \qquad
 \frac{\Gamma}{\Omega}=\chi^2.
 \label{eq:v8-mixed-parent-rate}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]