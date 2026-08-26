# Гейты Version 5, часть 1

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **115** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version5_affine_ko6_reference_corner_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0001

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:21`
- Строки: `21--26`

```latex
\begin{equation}
 P_1=\frac1{24}\sum_{g\in S_4}U_g=\frac14J_4,
 \qquad
 P_3=I_4-P_1.
 \label{eq:v5-affine-p1-p3}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0002

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:29`
- Строки: `29--37`

```latex
\begin{equation}
 V=
 \begin{pmatrix}
  1/\sqrt2&-1/\sqrt2&0&0\\
  1/\sqrt6&1/\sqrt6&-2/\sqrt6&0\\
  1/\sqrt{12}&1/\sqrt{12}&1/\sqrt{12}&-3/\sqrt{12}
 \end{pmatrix}
 \label{eq:v5-affine-coisometry}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0003

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:39`
- Строки: `39--45`

```latex
\begin{equation}
 VV^T=I_3,
 \qquad
 V^TV=P_3,
 \qquad
 V(1,1,1,1)^T=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0004

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:47`
- Строки: `47--51`

```latex
\begin{equation}
 R_g=VU_gV^T,
 \qquad
 R_gV=VU_g.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0005

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:60`
- Строки: `60--67`

```latex
\begin{equation}
 (0,0)^{\oplus4}
 \xrightarrow{\ X\ }
 (G,0)
 \xrightarrow{\ \Phi I_3\ }
 (G,2).
 \label{eq:v5-affine-family-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0006

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 4+3+3=10.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0007

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:73`
- Строки: `73--78`

```latex
\begin{equation}
 \boxed{
 2(4+3+3)\cdot15=300.
 }
 \label{eq:v5-affine-m300-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0008

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:84`
- Строки: `84--87`

```latex
\begin{equation}
 \mathcal A_{\mathrm{fam}}
 =\mathbb R_0\oplus M_3(\mathbb R)_G\oplus\mathbb C_2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0009

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:89`
- Строки: `89--93`

```latex
\begin{equation}
 a_0I_4,
 \qquad A_G,
 \qquad A_G,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0010

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:99`
- Строки: `99--102`

```latex
\begin{equation}
 X=\rho V,
 \qquad Y=\Phi I_3,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0011

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:104`
- Строки: `104--111`

```latex
\begin{equation}
 D_p=
 \begin{pmatrix}
 0&X^T&0\\
 X&0&\overline\Phi I_3\\
 0&\Phi I_3&0
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0012

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:113`
- Строки: `113--118`

```latex
\begin{equation}
 \gamma_p=\operatorname{diag}(I_4,-I_3,I_3),
 \qquad
 h_p=\operatorname{diag}(-P_3,0_3,I_3).
 \label{eq:v5-affine-height}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0013

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:123`
- Строки: `123--130`

```latex
\begin{align}
 D&=D^\dagger,&
 \{D,\gamma\}&=0,&
 JD&=DJ,&
 J\gamma&=-\gamma J,\\
 [\pi(a),\pi^o(b)]&=0,&
 [[D,\pi(a)],\pi^o(b)]&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0014

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:132`
- Строки: `132--138`

```latex
\begin{equation}
 D=d+d^\dagger,
 \qquad
 [h,d]=d,
 \qquad
 JdJ^{-1}=d^\dagger.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0015

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:146`
- Строки: `146--153`

```latex
\begin{equation}
 P_{\mathrm{ref}}
 =\operatorname{diag}(P_1,0_3,0_3;
                       P_1,0_3,0_3),
 \qquad
 P_{\mathrm{phys}}=I-P_{\mathrm{ref}}.
 \label{eq:v5-affine-reference-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0016

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:159`
- Строки: `159--163`

```latex
\begin{equation}
 \rank P_{\mathrm{ref}}=30,
 \qquad
 \rank P_{\mathrm{phys}}=270.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0017

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:166`
- Строки: `166--168`

```latex
\begin{equation}
 \dim\ker D_{\mathrm{phys}}=90.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0018

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:170`
- Строки: `170--172`

```latex
\begin{equation}
 \boxed{45}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0019

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:175`
- Строки: `175--177`

```latex
\begin{equation}
 \frac{270}{300}=\frac9{10}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0020

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:193`
- Строки: `193--201`

```latex
\begin{equation}
 \mathcal F_H=
 \operatorname{diag}\left(
 P_3-X^TX,
 XX^T-|\Phi|^2I_3,
 (|\Phi|^2-1)I_3
 \right).
 \label{eq:v5-affine-curvature-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0021

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:203`
- Строки: `203--206`

```latex
\begin{equation}
 X=V,
 \qquad |\Phi|=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0022

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:209`
- Строки: `209--218`

```latex
\begin{equation}
 \left\{
 0^{(4)},
 \left(\frac43\right)^{(3)},
 \left(\frac{16}3\right)^{(5)},
 \frac{32-8\sqrt7}{3},
 \frac{32+8\sqrt7}{3}
 \right\}.
 \label{eq:v5-affine-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0023

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:223`
- Строки: `223--225`

```latex
\begin{equation}
 (10_+,4_0,0_-).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0024

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:231`
- Строки: `231--235`

```latex
\begin{equation}
 \tau_{300}(\mathcal F_H^2)
 =\frac1{10}\Tr_{10}(\mathcal F_{H,p}^2).
 \label{eq:v5-affine-parent-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0025

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:237`
- Строки: `237--240`

```latex
\begin{equation}
 V_{\mathrm{red}}
 =\frac13\Tr_{10}(\mathcal F_{H,p}^2),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0026

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:242`
- Строки: `242--247`

```latex
\begin{equation}
 \boxed{
 \tau_{300}(\mathcal F_H^2)=\frac3{10}V_{\mathrm{red}}.
 }
 \label{eq:v5-affine-trace-scale}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0027

- Источник: `s2t/gates/version5_affine_ko6_reference_corner_gate.tex:272`
- Строки: `272--278`

```latex
\begin{equation}
 \mathcal A_{\mathrm{coord}}=\mathcal A_F^{\mathrm{SM}},
 \qquad
 \mathcal C_{\mathrm{fam}}
 \subseteq\pi(\mathcal A_F^{\mathrm{SM}})',
 \label{eq:v5-affine-commutant-route}
\end{equation}
```

## `s2t/gates/version5_centered_connection_potential_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0028

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:30`
- Строки: `30--34`

```latex
\begin{equation}
 C=\sum_{s=1}^{5}z_sP_s,
 \qquad
 (w_1,\ldots,w_5)=\frac1{15}(6,2,3,3,1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0029

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:36`
- Строки: `36--39`

```latex
\begin{equation}
 \tau_{15}(C)=\sum_{s=1}^{5}w_sz_s=0.
 \label{eq:v5-centered-connection-constraint}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0030

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 I_s=\tau_{15}(P_sC^*C)=w_s|z_s|^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0031

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:57`
- Строки: `57--60`

```latex
\begin{equation}
 V(C)=\sum_s m_s I_s+\sum_{s\le t}\lambda_{st}I_sI_t+\mathrm{const}.
 \label{eq:v5-general-centered-connection-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0032

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:78`
- Строки: `78--82`

```latex
\begin{equation}
 K=C^*C,\qquad
 p_1=\tau_{15}(K),\qquad
 p_2=\tau_{15}(K^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0033

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:84`
- Строки: `84--87`

```latex
\begin{equation}
 V_{a,b,c}=a\,p_1+b\,p_1^2+c\,p_2+\mathrm{const}.
 \label{eq:v5-trace-only-centered-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0034

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:94`
- Строки: `94--96`

```latex
\begin{equation}
 C=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0035

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:100`
- Строки: `100--102`

```latex
\begin{equation}
 V_{\mathrm{rad}}=(p_1-1)^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0036

- Источник: `s2t/gates/version5_centered_connection_potential_gate.tex:110`
- Строки: `110--115`

```latex
\begin{equation}
 V_{\mathrm{flat}}(C)
 =\tau_{15}\!\left(C^*C-\mathbf1\right)^2
 =\sum_s w_s\left(|z_s|^2-1\right)^2.
 \label{eq:v5-centered-flattening-potential}
\end{equation}
```

## `s2t/gates/version5_family_algebra_rectangle_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0037

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 M=\begin{pmatrix}yI_3&w\\v^\dagger&z\end{pmatrix},
 \qquad
 D_p=\begin{pmatrix}0&M\\M^\dagger&0\end{pmatrix},
 \label{eq:v5-active-family-M}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0038

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:23`
- Строки: `23--28`

```latex
\begin{align}
 \frac12\Tr D_p^4={}&3|y|^4+|z|^4+\|v\|^4+\|w\|^4\\
 &+2(|y|^2+|z|^2)(\|v\|^2+\|w\|^2)
 +4\Re(yz\,w^\dagger v).
 \label{eq:v5-rectangle-quartic}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0039

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 V=-\mu^2\Tr D_p^2+\lambda\Tr D_p^4,
 \qquad \lambda>0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0040

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 V=2\lambda\Tr(Q-r^2I_4)^2+\text{пост.}
 \label{eq:v5-rectangle-square}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0041

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:49`
- Строки: `49--54`

```latex
\begin{equation}|y|=|z|=r.\end{equation}

\begin{theorem}[Запрет спектрального вакуума с активными поколениями]
Во всяком глобальном минимуме обычного односледового квадратично-квартичного
спектрального потенциала
\begin{equation}v=w=0.\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0042

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:62`
- Строки: `62--64`

```latex
\begin{equation}
 \mu^2=2,\quad\lambda=1,\quad y=z=1,\quad v=w=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0043

- Источник: `s2t/gates/version5_family_algebra_rectangle_gate.tex:66`
- Строки: `66--68`

```latex
\begin{equation}0^{\times3},\qquad16^{\times4},\qquad48.\end{equation}
Три плоских направления задаются условием \(v=-w\). Вдоль них
\begin{equation}V(t)-V(0)=4t^4>0,\end{equation}
```

## `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0044

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:37`
- Строки: `37--39`

```latex
\begin{equation}
 a=|y_u|^2,\qquad b=|y_d|^2,\qquad c=|y_e|^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0045

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 I_u=3a^2,\qquad
 I_{de}=3b^2+c^2,\qquad
 I_{ud}=3ab.
 \label{eq:v5-h15-torsion-invariants}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0046

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 (y_u,y_d,y_e)\longmapsto
 t(y_u,y_d,y_e)
 \quad\Longrightarrow\quad
 I\longmapsto t^4I.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0047

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:63`
- Строки: `63--65`

```latex
\begin{equation}
 r=\frac{a}{b},\qquad s=\frac{c}{b}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0048

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:67`
- Строки: `67--71`

```latex
\begin{equation}
 R_1=\frac{I_{ud}}{I_u}=\frac1r,
 \qquad
 R_2=\frac{I_{de}}{3b^2}=1+\frac{s^2}{3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0049

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:73`
- Строки: `73--83`

```latex
\begin{equation}
 \frac{\partial(R_1,R_2)}{\partial(r,s)}
 =
 \begin{pmatrix}
 -r^{-2}&0\\
 0&2s/3
 \end{pmatrix},
 \qquad
 \det=-\frac{2s}{3r^2}.
 \label{eq:v5-h15-torsion-relative-jacobian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0050

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:99`
- Строки: `99--101`

```latex
\begin{equation}
 V_T=I_u^2+I_{de}^2+I_{ud}^2\geq0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0051

- Источник: `s2t/gates/version5_h15_spectral_torsion_selector_gate.tex:104`
- Строки: `104--106`

```latex
\begin{equation}
 a=b=c=0.
\end{equation}
```

## `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0052

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 {}_{M_{20}}E_{M_{15}}=M_{20\times15}(\mathbb C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0053

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 \operatorname{End}_{M_{20}-M_{15}}(E)=\mathbb C I_E.
 \label{eq:v5-projector-full-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0054

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 \mathbb C^3_{\rm fam}\otimes H_{15},
 \qquad \dim_{\mathbb C}=45
 \label{eq:v5-projector-light-sector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0055

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:48`
- Строки: `48--52`

```latex
\begin{equation}
 P_0=\frac13(I+C_3+C_3^2),
 \qquad \rank P_0=1.
 \label{eq:v5-projector-p0-again}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0056

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:54`
- Строки: `54--58`

```latex
\begin{equation}
 P_0\otimes I_{15}
 \quad\text{имеет ранг}\quad15.
 \label{eq:v5-projector-family-rank15}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0057

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:64`
- Строки: `64--68`

```latex
\begin{equation}
 H_{15}=Q_L^{(6)}\oplus L_L^{(2)}\oplus u_R^{(3)}
 \oplus d_R^{(3)}\oplus e_R^{(1)}.
 \label{eq:v5-projector-observed-blocks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0058

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:70`
- Строки: `70--73`

```latex
\begin{equation}
 6,\quad2,\quad3,\quad3,\quad1.
 \label{eq:v5-projector-combined-ranks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0059

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:82`
- Строки: `82--84`

```latex
\begin{equation}
 M_2(\mathbb C)'=\mathbb C I_2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0060

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:97`
- Строки: `97--101`

```latex
\begin{equation}
 P_\nu(H)=
 \frac{\widetilde H\widetilde H^\dagger}{H^\dagger H}.
 \label{eq:v5-higgs-neutrino-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0061

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:104`
- Строки: `104--107`

```latex
\begin{equation}
 P_\nu(UH)=U P_\nu(H)U^\dagger.
 \label{eq:v5-higgs-projector-covariance}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0062

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:112`
- Строки: `112--118`

```latex
\begin{equation}
 45
 \xrightarrow{P_0\otimes I_{15}}15
 \xrightarrow{P_L}2
 \xrightarrow{P_\nu(H)}1.
 \label{eq:v5-projector-rank-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0063

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:128`
- Строки: `128--131`

```latex
\begin{equation}
 P_0\otimes P_\nu(H)
 \label{eq:v5-combined-neutrino-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0064

- Источник: `s2t/gates/version5_holonomy_projector_defect_multiplicity_gate.tex:138`
- Строки: `138--141`

```latex
\begin{equation}
 q(x)\,P_0\otimes P_\nu(H(x)).
 \label{eq:v5-operator-valued-defect-candidate}
\end{equation}
```

## `s2t/gates/version5_one_seventh_k0_bridge_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0065

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:18`
- Строки: `18--22`

```latex
\begin{equation}
 \tau_{35}(p_{20}-p_{15})
 =\frac{20-15}{35}=\frac17.
 \label{eq:v5-one-seventh-corner}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0066

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:24`
- Строки: `24--27`

```latex
\begin{equation}
 P_0=\frac13(I+C_3+C_3^2),
 \qquad \rank P_0=1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0067

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:29`
- Строки: `29--33`

```latex
\begin{equation}
 \tau_{35}(p_{15})\tau_3(P_0)
 =\frac{15}{35}\frac13=\frac17.
 \label{eq:v5-one-seventh-holonomy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0068

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 (20-15)\cdot3=15\cdot1=15.
 \label{eq:v5-one-seventh-rank-duality}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0069

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 \mathcal B_{\rm cmp}=M_{35}(\mathbb C)\otimes M_3(\mathbb C)
 \simeq M_{105}(\mathbb C).
 \label{eq:v5-one-seventh-comparison-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0070

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:52`
- Строки: `52--54`

```latex
\begin{equation}
 ([p_{20}]-[p_{15}])\otimes[I_3]
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0071

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:56`
- Строки: `56--58`

```latex
\begin{equation}
 [p_{15}\otimes P_0]
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0072

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:61`
- Строки: `61--67`

```latex
\begin{equation}
 \boxed{
 ([p_{20}]-[p_{15}])\otimes[I_3]
 =[p_{15}\otimes P_0]
 }
 \label{eq:v5-one-seventh-k0-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0073

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:87`
- Строки: `87--89`

```latex
\begin{equation}
 r_5\le p_{20}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0074

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 \{0,2,6,8,12,14,18,20\}.
 \label{eq:v5-one-seventh-known-ranks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0075

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:100`
- Строки: `100--104`

```latex
\begin{equation}
 \operatorname{Gr}(5,20),
 \qquad
 \dim_{\mathbb R}\operatorname{Gr}(5,20)=2\cdot5\cdot15=150.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0076

- Источник: `s2t/gates/version5_one_seventh_k0_bridge_gate.tex:123`
- Строки: `123--129`

```latex
\begin{equation}
 \partial_{\rm hol}:
 [p_{15}\otimes P_0]
 \longmapsto
 ([p_{20}]-[p_{15}])\otimes[I_3],
 \label{eq:v5-one-seventh-transgression-target}
\end{equation}
```

## `s2t/gates/version5_parent_architecture_status_freeze_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0077

- Источник: `s2t/gates/version5_parent_architecture_status_freeze_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 \boxed{\text{нормировка состояния --- да, родительская мера --- нет}.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0078

- Источник: `s2t/gates/version5_parent_architecture_status_freeze_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 \boxed{\text{локальные модули --- частично да, единый источник --- нет}.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0079

- Источник: `s2t/gates/version5_parent_architecture_status_freeze_gate.tex:93`
- Строки: `93--95`

```latex
\begin{equation}
 \boxed{\text{ориентированное тождество --- да, его родительский выбор --- нет}.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0080

- Источник: `s2t/gates/version5_parent_architecture_status_freeze_gate.tex:178`
- Строки: `178--180`

```latex
\begin{equation}
 N_{\rm parent}=N_{\rm intersector}=N_{\rm physical}=0.
\end{equation}
```

## `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0081

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:15`
- Строки: `15--20`

```latex
\begin{equation}
 S^2_{\rm sp}
 \simeq SO(3)/SO(2)
 \simeq \operatorname{Spin}(3)/\operatorname{Spin}(2).
 \label{eq:v5-spin-bridge-spatial-sphere}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0082

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:22`
- Строки: `22--26`

```latex
\begin{equation}
 \mathbb{RP}^2_{\rm fam}
 \simeq SO(3)/O(2),
 \label{eq:v5-spin-bridge-projective-target}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0083

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:31`
- Строки: `31--38`

```latex
\begin{equation}
 q:S^2_{\rm sp}\longrightarrow\mathbb{RP}^2_{\rm fam},
 \qquad
 q(\mathbf n)=[\mathbf n],
 \qquad
 P(\mathbf n)=\mathbf n\mathbf n^{\mathsf T}.
 \label{eq:v5-spin-bridge-quotient-map}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0084

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:44`
- Строки: `44--46`

```latex
\begin{equation}
 f:S^2\longrightarrow\mathbb{RP}^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0085

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:52`
- Строки: `52--54`

```latex
\begin{equation}
 f(R\mathbf e_3)=R f(\mathbf e_3)=[R\mathbf e_3],
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0086

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 SO(2)\subset O(2)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0087

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:83`
- Строки: `83--86`

```latex
\begin{equation}
 \pi:S^2\longrightarrow\mathbb{RP}^2,
 \qquad \pi(\mathbf n)=[\mathbf n],
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0088

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:93`
- Строки: `93--98`

```latex
\begin{equation}
 \widetilde q_+(\mathbf n)=\mathbf n,
 \qquad
 \widetilde q_-(\mathbf n)=-\mathbf n.
 \label{eq:v5-spin-bridge-two-lifts}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0089

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:100`
- Строки: `100--105`

```latex
\begin{equation}
 \deg\widetilde q_+=+1,
 \qquad
 \deg\widetilde q_-=-1.
 \label{eq:v5-spin-bridge-lift-degrees}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0090

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:115`
- Строки: `115--118`

```latex
\begin{equation}
 P_+(\mathbf n)=\frac12
 \left(I+\mathbf n\cdot\boldsymbol\sigma\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0091

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:121`
- Строки: `121--124`

```latex
\begin{equation}
 L_+=\widetilde q_+^*H,
 \qquad c_1(L_+)=+1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0092

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:125`
- Строки: `125--130`

```latex
\begin{equation}
 L_-=\widetilde q_-^*H,
 \qquad c_1(L_-)=-1,
 \qquad L_-\simeq L_+^*.
 \label{eq:v5-spin-bridge-hopf-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0093

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:134`
- Строки: `134--138`

```latex
\begin{equation}
 E\longmapsto L_+,
 \qquad
 E^*\longmapsto L_-
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0094

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:157`
- Строки: `157--161`

```latex
\begin{equation}
 \text{точечный центр и полная }SO(3)\text{-эквивариантность}
 \Longrightarrow q(\mathbf n)=[\mathbf n].
 \label{eq:v5-spin-bridge-conditional-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0095

- Источник: `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex:186`
- Строки: `186--193`

```latex
\begin{equation}
 \boxed{
 S^2_{\rm sp}=SO(3)/SO(2)
 \xrightarrow{\;q\;}
 \mathbb{RP}^2_{\rm fam}=SO(3)/O(2)
 \xleftarrow{\;\pi\;}
 S^2_{\rm lift}}
\end{equation}
```

## `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0096

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 \mathcal H_{\rm light}=\mathbb C^3_{\rm fam}\otimes H_{15},
 \qquad \dim\mathcal H_{\rm light}=45,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0097

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 H_{15}=Q_L^{(6)}\oplus L_L^{(2)}\oplus
 u_R^{(3)}\oplus d_R^{(3)}\oplus e_R^{(1)}.
 \label{eq:v5-su2-h15}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0098

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:27`
- Строки: `27--31`

```latex
\begin{equation}
 \mathbb C^{10}_{F}\simeq\mathbf 1\oplus\mathbf 3\oplus
 \mathbf 3\oplus\mathbf 3.
 \label{eq:v5-su2-family-decomposition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0099

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:44`
- Строки: `44--46`

```latex
\begin{equation}
 SU(2)\longrightarrow SO(3)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0100

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:49`
- Строки: `49--52`

```latex
\begin{equation}
 \rho_{j=1}(-1)=+I_3.
 \label{eq:v5-su2-spin-one-center}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0101

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 \rho_{j=1/2}(-1)=-I_2.
 \label{eq:v5-su2-spin-half-center}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0102

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:77`
- Строки: `77--79`

```latex
\begin{equation}
 \gamma_{\rm KO6}=\sigma_z\otimes I_{10}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0103

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:82`
- Строки: `82--86`

```latex
\begin{equation}
 [\sigma_x\otimes I_{10},\gamma_{\rm KO6}]\ne0,
 \qquad
 [\sigma_y\otimes I_{10},\gamma_{\rm KO6}]\ne0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0104

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:100`
- Строки: `100--103`

```latex
\begin{equation}
 \operatorname{Spec}\rho_L(-1)=
 \{(-1)^{\times8},(+1)^{\times7}\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0105

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:112`
- Строки: `112--115`

```latex
\begin{equation}
 \mathbb C^3_{\rm fam}\longmapsto\mathbf2\oplus\mathbf1.
 \label{eq:v5-su2-two-plus-one}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0106

- Источник: `s2t/gates/version5_su2_family_lift_h15_representation_gate.tex:135`
- Строки: `135--137`

```latex
\begin{equation}
 E=M_{20\times15}(\mathbb C)
\end{equation}
```

## `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0107

- Источник: `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 S_{\rm loop}(V)=\tau_{210}\!\left([N,V]^*[N,V]\right).
 \label{eq:v5-loop-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0108

- Источник: `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 S_+=\sum_{a=1}^{105}k_a^2,
 \qquad \sum_a k_a=15.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0109

- Источник: `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 S_{\rm loop}(V_{15})=\frac{30}{210}=\frac17.
\end{equation}
```

## `s2t/gates/version5_twisted_family_automorphism_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-01-0110

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
 \mathcal A_q=\mathbb R_0\oplus M_3(\mathbb R)_G\oplus\mathbb C_2.
 \label{eq:v5-twist-current-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0111

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 \rho(e_0)=e_0,\qquad\rho(e_G)=e_G,\qquad\rho(e_2)=e_2.
 \label{eq:v5-twist-fixed-idempotents}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0112

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:23`
- Строки: `23--32`

```latex
\begin{equation}\rho_G(A)=OAO^T,\qquad O\in O(3),\end{equation}
а на \(\mathbb C\) --- тождественное преобразование или комплексное
сопряжение. Матричные автоморфизмы являются внутренними изменениями
калибровочного базиса. Выбор конкретного нецентрального \(O\) внёс бы
непрерывные данные ориентации.

\section{Почему известный механизм обмена отсутствует}

Скрученный коммутатор имеет вид
\begin{equation}[D,a]_\rho=Da-\rho(a)D.\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0113

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 X=\rho I_3,qquad\Phi=r\in\mathbb R.
 \label{eq:v5-twist-radial-fixed-slice}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0114

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}\Tr D_p^4=6(\rho^2+r^2)^2\end{equation}
в требуемую зависимость
\begin{equation}(\rho^2-r^2)^2.\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-01-0115

- Источник: `s2t/gates/version5_twisted_family_automorphism_gate.tex:74`
- Строки: `74--78`

```latex
\begin{equation}
 \mathbb R_0^{\oplus2},\qquad
 M_3(\mathbb R)_G^{\oplus2},\qquad
 \mathbb C_2^{\oplus2}.
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]