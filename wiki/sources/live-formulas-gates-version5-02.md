# Гейты Version 5, часть 2

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **115** блочных формул из **12** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version5_defect_transport_part_conclusion_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0001

- Источник: `s2t/gates/version5_defect_transport_part_conclusion_gate.tex:16`
- Строки: `16--34`

```latex
\begin{equation}
 \boxed{
 \begin{gathered}
 \text{типизированный переход}
 \longrightarrow
 \text{локальный перенос}
 \\
 \longrightarrow
 \text{голономный характер}
 \longrightarrow
 \text{самопорождающийся дефект}
 \\
 \longrightarrow
 \text{точечный проекторный заряд}
 \longrightarrow
 \text{условный спинорный индекс}.
 \end{gathered}}
 \label{eq:v5-part-conclusion-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0002

- Источник: `s2t/gates/version5_defect_transport_part_conclusion_gate.tex:66`
- Строки: `66--69`

```latex
\begin{equation}
 \Tr(\partial_iP\,\partial_iP)=\frac4{r^2},
 \qquad dE=8\pi\,dr.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0003

- Источник: `s2t/gates/version5_defect_transport_part_conclusion_gate.tex:72`
- Строки: `72--75`

```latex
\begin{equation}
 D_iP=\partial_iP+[A_i,P],
 \label{eq:v5-part-conclusion-covariant-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0004

- Источник: `s2t/gates/version5_defect_transport_part_conclusion_gate.tex:82`
- Строки: `82--84`

```latex
\begin{equation}
 P(\mathbf n)=P(-\mathbf n).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0005

- Источник: `s2t/gates/version5_defect_transport_part_conclusion_gate.tex:100`
- Строки: `100--112`

```latex
\begin{equation}
 \begin{split}
 S_{\rm parent}[P,A,\mathcal L,\psi,H]
 =\int d^4x\,\bigg[
 &\frac1{4g^2}\Tr(F_{\mu\nu}F^{\mu\nu})
 +\frac{f^2}{2}\Tr(D_\mu P D^\mu P)
 +V(P)
 \\
 &+\overline\psi\bigl(i\gamma^\mu D_\mu-mQ_{1/2}(P,\mathcal L)\bigr)\psi
 +\mathcal R_H(P,H)\bigg].
 \end{split}
 \label{eq:v5-part-conclusion-parent-target}
\end{equation}
```

## `s2t/gates/version5_defect_transport_reframing_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0006

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:69`
- Строки: `69--73`

```latex
\begin{equation}
 U_e:\mathcal H_x\longrightarrow\mathcal H_y,
 \qquad e=(x,y),
 \label{eq:v5-local-transfer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0007

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:123`
- Строки: `123--125`

```latex
\begin{equation}
 E=M_{20\times15}(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0008

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:139`
- Строки: `139--141`

```latex
\begin{equation}
 (\mathcal A_x,\mathcal H_x,J_x,\gamma_x,\rho_x,\tau_x).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0009

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:144`
- Строки: `144--148`

```latex
\begin{equation}
 U_e=\mathcal P\exp\!\left(-\int_e\nabla\right)
 :\rho_x\mathcal H_x\longrightarrow\rho_y\mathcal H_y
 \label{eq:v5-connection-transfer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0010

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:151`
- Строки: `151--153`

```latex
\begin{equation}
 U(p)=U_{e_n}\cdots U_{e_1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0011

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:160`
- Строки: `160--163`

```latex
\begin{equation}
 W=\sum_{e\in\Gamma_1}S_e\otimes U_e,
 \label{eq:v5-global-step}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0012

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:166`
- Строки: `166--173`

```latex
\begin{align}
 W^*W&=WW^*=I,
 \label{eq:v5-transfer-unitarity}\\
 [W,a]&\ \text{локален},\\
 JW&=WJ,\qquad \gamma W\gamma=W^*
 \quad\text{либо выполняется эквивалентное условие},\\
 \tau(W^*XW)&=\tau(X).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0013

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:182`
- Строки: `182--184`

```latex
\begin{equation}
 W(k)=\exp[-iaH_{\rm eff}(k)].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0014

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:186`
- Строки: `186--189`

```latex
\begin{equation}
 H_{\rm eff}(k)=c\,\alpha^ik_i+\beta M+O(a|k|^2),
 \label{eq:v5-dirac-limit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0015

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:203`
- Строки: `203--205`

```latex
\begin{equation}
 m_s=\frac1{c^2}\min_k|\omega_s(k)|,
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0016

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:207`
- Строки: `207--210`

```latex
\begin{equation}
 \omega_s(k)^2=c^2|k|^2+m_s^2c^4+O(a|k|^3).
 \label{eq:v5-relativistic-dispersion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0017

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:226`
- Строки: `226--231`

```latex
\begin{equation}
 \mathcal C^0\xrightarrow{d_0}\mathcal C^1
 \xrightarrow{d_1}\mathcal C^2,
 \qquad d_1d_0=0,
 \label{eq:v5-neutrino-complex}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0018

- Источник: `s2t/gates/version5_defect_transport_reframing_gate.tex:245`
- Строки: `245--249`

```latex
\begin{equation}
 \mathcal P_{\alpha\to\beta}(n)
 =\left\|P_\beta W^nP_\alpha\psi\right\|^2.
 \label{eq:v5-flavour-transfer}
\end{equation}
```

## `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0019

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:6`
- Строки: `6--9`

```latex
\begin{equation}
 \Gamma_{\rm F}[V]=-\log\det D[V].
 \label{eq:v5-fermion-determinant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0020

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 D_{M,V}=\mathord{\not\!\partial}
 +M\bigl(P_LV+P_RV^*\bigr)
 \label{eq:v5-chiral-dirac-coupling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0021

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:26`
- Строки: `26--32`

```latex
\begin{equation}
 \Gamma_{\rm F}^{+}[V]
 =c_0+c_2\int\Tr(L_\mu L^\mu)
 +\sum_jc_{4,j}\int\mathcal O_{4,j}(L)+O(\partial^6),
 \qquad L_\mu=V^{-1}\partial_\mu V.
 \label{eq:v5-fermion-derivative-expansion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0022

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 x=\frac{M^2}{\Lambda^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0023

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 \frac{\Gamma(2,x)}{\Gamma(1,x)}=1+x,
 \label{eq:v5-incomplete-gamma-ratio}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0024

- Источник: `s2t/gates/version5_fermionic_determinant_induced_skyrme_gate.tex:62`
- Строки: `62--66`

```latex
\begin{equation}
 R_*=\frac1M\,
 \mathcal R\!\left(\frac{M}{\Lambda},\{Y\},\text{схема}\right),
 \label{eq:v5-fermion-induced-radius}
\end{equation}
```

## `s2t/gates/version5_foundational_relative_architecture_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0025

- Источник: `s2t/gates/version5_foundational_relative_architecture_gate.tex:36`
- Строки: `36--38`

```latex
\begin{equation}
 \Gamma(X\to Y)\mapsto\Gamma(X\to Y)+B(Y)-B(X).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0026

- Источник: `s2t/gates/version5_foundational_relative_architecture_gate.tex:52`
- Строки: `52--55`

```latex
\begin{equation}
 R_g\xrightarrow{T_{gs}}R_s\xrightarrow{T_{sc}}R_c
 \xrightarrow{T_{cg}}R_g.
\end{equation}
```

## `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0027

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 \chi(k)=i^k,
 \qquad k\in\mathbb Z_4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0028

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 \chi(a+b)=\chi(a)\chi(b).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0029

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:29`
- Строки: `29--31`

```latex
\begin{equation}
 \omega(a,b)=\frac{\chi(a)\chi(b)}{\chi(a+b)}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0030

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:37`
- Строки: `37--39`

```latex
\begin{equation}
 c_1=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0031

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:52`
- Строки: `52--55`

```latex
\begin{equation}
 U(1)\longrightarrow S^3\longrightarrow S^2.
 \label{eq:v5-hopf-fibration}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0032

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:57`
- Строки: `57--64`

```latex
\begin{equation}
 z_N(\theta,\phi)=
 \begin{pmatrix}
  \cos(\theta/2)\\
  e^{i\phi}\sin(\theta/2)
 \end{pmatrix}.
 \label{eq:v5-hopf-north-section}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0033

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:66`
- Строки: `66--71`

```latex
\begin{equation}
 n_a=z_N^\dagger\sigma_a z_N,
 \qquad
 P_+=z_Nz_N^\dagger=\frac{I+n_a\sigma_a}{2}.
 \label{eq:v5-hopf-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0034

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:74`
- Строки: `74--76`

```latex
\begin{equation}
 z_S=e^{-i\phi}z_N.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0035

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 A=-iz^\dagger dz
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0036

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 F=\frac12\sin\theta\,d\theta\wedge d\phi,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0037

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:87`
- Строки: `87--90`

```latex
\begin{equation}
 c_1(L)=\frac1{2\pi}\int_{S^2}F=1.
 \label{eq:v5-hopf-c1-one}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0038

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:98`
- Строки: `98--100`

```latex
\begin{equation}
 z\longmapsto e^{i\alpha}z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0039

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:102`
- Строки: `102--104`

```latex
\begin{equation}
 z\mapsto iz\mapsto-z\mapsto-iz\mapsto z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0040

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:115`
- Строки: `115--119`

```latex
\begin{equation}
 S^3\simeq SU(2),
 \qquad
 \mathbb{RP}^3\simeq SO(3)=SU(2)/\{\pm1\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0041

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:124`
- Строки: `124--130`

```latex
\begin{equation}
 \boxed{
 \text{спинорное накрытие }S^3\Rightarrow c_1=1,
 \qquad
 \text{векторный quotient }\mathbb{RP}^3\Rightarrow c_1=2.}
 \label{eq:v5-hopf-cover-quotient-c1}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0042

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:141`
- Строки: `141--144`

```latex
\begin{equation}
 \mathcal F_{y\leftarrow x}=L_y\otimes L_x^*.
 \label{eq:v5-hopf-fell-arrow}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0043

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:146`
- Строки: `146--152`

```latex
\begin{equation}
 \mathcal F_{z\leftarrow y}\otimes
 \mathcal F_{y\leftarrow x}
 \longrightarrow
 \mathcal F_{z\leftarrow x},
 \label{eq:v5-hopf-fell-composition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0044

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:166`
- Строки: `166--168`

```latex
\begin{equation}
 E:M_{15}\longrightarrow M_{20},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0045

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:170`
- Строки: `170--175`

```latex
\begin{equation}
 E\otimes L,
 \qquad
 E^*\otimes L^*.
 \label{eq:v5-hopf-oriented-morita-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0046

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:177`
- Строки: `177--181`

```latex
\begin{equation}
 c_1(L)=+1
 \quad\longleftrightarrow\quad
 c_1(L^*)=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0047

- Источник: `s2t/gates/version5_hopf_fell_line_transition_lift_gate.tex:201`
- Строки: `201--206`

```latex
\begin{equation}
 E\longmapsto n,
 \qquad
 E^*\longmapsto-n.
 \label{eq:v5-hopf-missing-orientation-functor}
\end{equation}
```

## `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0048

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 T:\mathbb C^{15}\longrightarrow\mathbb C^{20}.
 \label{eq:v5-odd-core-rectangular-T}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0049

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:18`
- Строки: `18--26`

```latex
\begin{equation}
 Q_T=
 \begin{pmatrix}
 0&T\\T^*&0
 \end{pmatrix}
 \quad\text{на}\quad
 \mathbb C^{20}\oplus\mathbb C^{15}.
 \label{eq:v5-odd-core-selfadjoint-Q}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0050

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:29`
- Строки: `29--36`

```latex
\begin{equation}
 \dim\ker T=0,
 \qquad
 \dim\ker T^*=5,
 \qquad
 \dim\ker Q_T=5.
 \label{eq:v5-odd-core-asymptotic-nullity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0051

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:45`
- Строки: `45--51`

```latex
\begin{equation}
 \dim\ker T=1,
 \qquad
 \dim\ker T^*=6,
 \qquad
 \dim\ker Q_T=7.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0052

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:53`
- Строки: `53--58`

```latex
\begin{equation}
 \operatorname{ind}T
 =\dim\ker T-\dim\ker T^*
 =15-20=-5.
 \label{eq:v5-odd-core-constant-index}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0053

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 \Gamma_{\rm link}=p_{20}-p_{15}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0054

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:76`
- Строки: `76--80`

```latex
\begin{equation}
 \tau_{35}(\Gamma_{\rm link})
 =\frac{20-15}{35}=\frac17.
 \label{eq:v5-odd-core-one-seventh-superdimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0055

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:102`
- Строки: `102--105`

```latex
\begin{equation}
 \{0,2,6,8,12,14,18,20\}.
 \label{eq:v5-odd-core-compatible-ranks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0056

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:121`
- Строки: `121--127`

```latex
\begin{equation}
 E=M_{20\times15}(\mathbb C),
 \qquad
 E^*=M_{15\times20}(\mathbb C),
 \qquad
 \dim E=\dim E^*=300.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0057

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:131`
- Строки: `131--133`

```latex
\begin{equation}
 X\longmapsto X^*
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0058

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:155`
- Строки: `155--160`

```latex
\begin{equation}
 E=(H_{10}\otimes H_{15})
 \oplus J(H_{10}\otimes H_{15}),
 \qquad 300=150+150.
 \label{eq:v5-odd-core-150-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0059

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:179`
- Строки: `179--183`

```latex
\begin{equation}
 T^*T\in M_{15},
 \qquad
 TT^*\in M_{20}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0060

- Источник: `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex:220`
- Строки: `220--226`

```latex
\begin{equation}
 \begin{gathered}
 \text{обратим на сфере бесконечности},\\
 \text{теряет ровно один ранг на ядре},\\
 \text{сохраняет KO6, }H_{15}\text{ и след }M_{35}.
 \end{gathered}
\end{equation}
```

## `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0061

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 1\longmapsto i\longmapsto-1\longmapsto-i\longmapsto1.
 \label{eq:v5-order-four-phase-history}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0062

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 t=\sqrt{1-r^2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0063

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 q(\omega)=e^{4i\omega}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0064

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:59`
- Строки: `59--62`

```latex
\begin{equation}
 S(\omega)=\frac{r-q(\omega)}{1-rq(\omega)}.
 \label{eq:v5-ring-scattering}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0065

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:64`
- Строки: `64--66`

```latex
\begin{equation}
 |S(\omega)|=1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0066

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:70`
- Строки: `70--75`

```latex
\begin{equation}
 \tau(\theta)=
 4\frac{1-r^2}{1+r^2-2r\cos\theta},
 \qquad \theta=4\omega.
 \label{eq:v5-ring-group-delay}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0067

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:77`
- Строки: `77--80`

```latex
\begin{equation}
 \tau_{\rm res}=4\frac{1+r}{1-r}.
 \label{eq:v5-ring-resonant-delay}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0068

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:97`
- Строки: `97--100`

```latex
\begin{equation}
 P_n=r^{2n}.
 \label{eq:v5-ring-survival}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0069

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:103`
- Строки: `103--105`

```latex
\begin{equation}
 t=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0070

- Источник: `s2t/gates/version5_order_four_resonant_loop_transport_gate.tex:125`
- Строки: `125--127`

```latex
\begin{equation}
 1,\quad i,\quad-1,\quad-i.
\end{equation}
```

## `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0071

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 q(z)P_0\otimes P_\nu(H)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0072

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:36`
- Строки: `36--41`

```latex
\begin{equation}
 P(\mathbf n)=\mathbf n\mathbf n^T,
 \qquad \mathbf n\in S^2,
 \qquad \mathbf n\sim-\mathbf n.
 \label{eq:v5-projective-order-parameter}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0073

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:43`
- Строки: `43--48`

```latex
\begin{equation}
 \mathcal V_P\simeq\mathbb{RP}^2,
 \qquad
 \pi_2(\mathbb{RP}^2)\simeq\mathbb Z.
 \label{eq:v5-rp2-pi2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0074

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:50`
- Строки: `50--55`

```latex
\begin{equation}
 \mathbf n(\mathbf x)=\frac{\mathbf x}{|\mathbf x|},
 \qquad
 P(\mathbf x)=\frac{\mathbf x\mathbf x^T}{|\mathbf x|^2}.
 \label{eq:v5-projective-hedgehog}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0075

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:57`
- Строки: `57--63`

```latex
\begin{equation}
 \frac1{4\pi}\int_{S^2}
 \mathbf n\cdot
 (\partial_\theta\mathbf n\times\partial_\phi\mathbf n)
 \,d\theta d\phi=1.
 \label{eq:v5-hedgehog-degree}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0076

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:70`
- Строки: `70--73`

```latex
\begin{equation}
 E_P=\frac12\int d^3x\,\Tr(\partial_iP\,\partial_iP)
 \label{eq:v5-projector-gradient-energy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0077

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:75`
- Строки: `75--77`

```latex
\begin{equation}
 \Tr(\partial_iP\,\partial_iP)=\frac4{r^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0078

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 Q_P=3P-I_3.
 \label{eq:v5-projector-mass-matrix}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0079

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:108`
- Строки: `108--113`

```latex
\begin{equation}
 c_1(P)=\frac1{2\pi i}\int_{S^2}
 \Tr\!\left(P[\partial_\theta P,\partial_\phi P]\right)
 d\theta d\phi=0.
 \label{eq:v5-vector-projector-chern-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0080

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:131`
- Строки: `131--134`

```latex
\begin{equation}
 Q_{1/2}(\mathbf n)=\mathbf n\cdot\boldsymbol\sigma.
 \label{eq:v5-spinor-hedgehog-mass}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0081

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:136`
- Строки: `136--138`

```latex
\begin{equation}
 P_+(\mathbf n)=\frac12(I+\mathbf n\cdot\boldsymbol\sigma).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0082

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:140`
- Строки: `140--145`

```latex
\begin{equation}
 \frac1{2\pi i}\int_{S^2}
 \Tr\!\left(P_+[\partial_\theta P_+,\partial_\phi P_+]\right)
 d\theta d\phi=1.
 \label{eq:v5-spinor-projector-chern-one}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0083

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:155`
- Строки: `155--157`

```latex
\begin{equation}
 \mathbb{RP}^2\longleftarrow S^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0084

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:163`
- Строки: `163--166`

```latex
\begin{equation}
 h^2=-1,
 \qquad h^4=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0085

- Источник: `s2t/gates/version5_projective_hedgehog_point_defect_gate.tex:175`
- Строки: `175--180`

```latex
\begin{equation}
 (P,\text{корневая линия})
 \longmapsto
 \mathbf n\cdot\boldsymbol\sigma
 \label{eq:v5-projector-spinor-lift-target}
\end{equation}
```

## `s2t/gates/version5_projector_superconnection_common_scale_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0086

- Источник: `s2t/gates/version5_projector_superconnection_common_scale_gate.tex:4`
- Строки: `4--6`

```latex
\begin{equation}
 D_{\rm tot}=D_{\rm space}\widehat\otimes1+gamma\widehat\otimes N/\ell.
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0087

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 \partial_n:KO_n(A/J)\longrightarrow KO_{n-1}(J).
 \label{eq:v5-ko7-boundary-convention}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0088

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:24`
- Строки: `24--27`

```latex
\begin{equation}
 \boxed{7-1=6\pmod 8.}
 \label{eq:v5-ko7-correct-degree}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0089

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 B=M_{105}(\mathbb C)_{\mathbb R}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0090

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:44`
- Строки: `44--49`

```latex
\begin{equation}
 KO_{2k}(B)\simeq\mathbb Z,
 \qquad
 KO_{2k+1}(B)=0.
 \label{eq:v5-ko7-coefficient-table}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0091

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:51`
- Строки: `51--56`

```latex
\begin{equation}
 \kappa_{15}:=[T_{\mathbb R}]=15\in KO_6(B),
 \qquad
 c_6(\kappa_{15})=(-15,+15).
 \label{eq:v5-ko7-coefficient-fifteen}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0092

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 [u_{\mathbb R}]\in KO_1(C^*_{\mathbb R}(\mathbb Z)).
 \label{eq:v5-ko7-real-winding}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0093

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:77`
- Строки: `77--79`

```latex
\begin{equation}
 KO_1(C^*_{\mathbb R}(\mathbb Z))\simeq\mathbb Z\oplus\mathbb Z_2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0094

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:84`
- Строки: `84--89`

```latex
\begin{equation}
 \xi_{15}
 =[u_{\mathbb R}]\boxtimes\kappa_{15}
 \in KO_7(C^*_{\mathbb R}(\mathbb Z)\otimes B).
 \label{eq:v5-ko7-symbol}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0095

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:94`
- Строки: `94--98`

```latex
\begin{equation}
 \widetilde{KO}_7(C^*_{\mathbb R}(\mathbb Z)\otimes B)
 \simeq KO_6(B)\simeq\mathbb Z.
 \label{eq:v5-ko7-reduced-group}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0096

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:105`
- Строки: `105--109`

```latex
\begin{equation}
 \partial_1([u_{\mathbb R}])=\varepsilon[1],
 \qquad \varepsilon\in\{+1,-1\},
 \label{eq:v5-ko7-base-index}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0097

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:111`
- Строки: `111--117`

```latex
\begin{align}
 \partial_7(\xi_{15})
 &=\partial_1([u_{\mathbb R}])\boxtimes\kappa_{15}\\
 &=\varepsilon\kappa_{15}
 =\varepsilon15\in KO_6(B).
 \label{eq:v5-ko7-boundary-fifteen}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0098

- Источник: `s2t/gates/version5_real_toeplitz_degree_seven_symbol_gate.tex:133`
- Строки: `133--135`

```latex
\begin{equation}
 \frac{|\partial_7(\xi_{15})|}{105}=\frac{15}{105}=\frac17.
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0099

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:21`
- Строки: `21--28`

```latex
\begin{equation}
 J^2=1,
 \qquad
 JD=DJ,
 \qquad
 J\gamma=-\gamma J.
 \label{eq:v5-real-toeplitz-ko6-signs}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0100

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:33`
- Строки: `33--45`

```latex
\begin{equation}
 F=
 \begin{pmatrix}
  0&T^*\\
  T&0
 \end{pmatrix},
 \qquad
 \gamma=
 \begin{pmatrix}
  I&0\\0&-I
 \end{pmatrix}.
 \label{eq:v5-real-toeplitz-F}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0101

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 F(Jx)=J(Fx)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0102

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:62`
- Строки: `62--64`

```latex
\begin{equation}
 J:\ker T\xrightarrow{\simeq}\ker T^*.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0103

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:66`
- Строки: `66--70`

```latex
\begin{equation}
 \operatorname{ind}T
 =\dim\ker T-\dim\ker T^*=0.
 \label{eq:v5-real-toeplitz-zero-index-theorem}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0104

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 T_+=S\otimes q_0,
 \qquad
 T_-=S^*\otimes\overline{q_0}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0105

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:87`
- Строки: `87--90`

```latex
\begin{equation}
 T_{\mathbb R}=T_+\oplus T_-.
 \label{eq:v5-real-toeplitz-balanced-T}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0106

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:92`
- Строки: `92--96`

```latex
\begin{align}
 \dim\ker T_{\mathbb R}&=15,\\
 \dim\ker T_{\mathbb R}^*&=15,\\
 \operatorname{ind}T_{\mathbb R}&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0107

- Источник: `s2t/gates/version5_real_toeplitz_ko6_parent_lift_gate.tex:105`
- Строки: `105--108`

```latex
\begin{equation}
 \frac{30}{210}=\frac17.
 \label{eq:v5-real-toeplitz-weight-survives}
\end{equation}
```

## `s2t/gates/version5_state_corner_curvature_readout_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-02-0108

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 X=rV,\qquad Y=\Phi I_3,\qquad VV^*=I_3
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0109

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:31`
- Строки: `31--37`

```latex
\begin{equation}
 \mathcal F_{\mathrm{fam}}
 =XX^*-Y^*Y
 =(r^2-|\Phi|^2)I_3
 =\mu I_3.
 \label{eq:v5-full-equivariant-moment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0110

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 C_\rho(A)=\rho A\rho.
 \label{eq:v5-state-corner-compression}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0111

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:50`
- Строки: `50--53`

```latex
\begin{equation}
 C_\rho(\mu I_3)=\mu\rho.
 \label{eq:v5-corner-moment-readout}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0112

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 \tau_3((\mu I_3)^2)=\mu^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0113

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:64`
- Строки: `64--69`

```latex
\begin{equation}
 \tau_\rho(B)=\frac{\Tr(\rho B\rho)}{\Tr\rho},
 \qquad
 \tau_\rho((\mu\rho)^2)=\mu^2.
 \label{eq:v5-corner-normalized-norm}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0114

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 \tau_{45}(P_\rho\mu^2)=\frac13\mu^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-02-0115

- Источник: `s2t/gates/version5_state_corner_curvature_readout_gate.tex:89`
- Строки: `89--91`

```latex
\begin{equation}
 6+2+3+3+1=15
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]