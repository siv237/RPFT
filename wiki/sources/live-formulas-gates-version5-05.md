# Гейты Version 5, часть 5

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **114** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version5_commuting_square_readout_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0001

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:8`
- Строки: `8--18`

```latex
\begin{equation}
 H_{\mathrm{par}}
 =H_{\mathrm{fam}}\otimes H_{\mathrm{obs}},
 \qquad
 \dim H_{\mathrm{fam}}=20,
 \qquad
 \dim H_{\mathrm{obs}}=15,
 \qquad
 \dim H_{\mathrm{par}}=300.
 \label{eq:v5-commuting-square-factorization}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0002

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:27`
- Строки: `27--33`

```latex
\begin{equation}
 \mathcal M_{\mathrm{fam}}
 =B(H_{\mathrm{fam}})\otimes I_{15},
 \qquad
 \mathcal M_{\mathrm{obs}}
 =I_{20}\otimes B(H_{\mathrm{obs}}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0003

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:35`
- Строки: `35--40`

```latex
\begin{equation}
 [\mathcal M_{\mathrm{fam}},\mathcal M_{\mathrm{obs}}]=0,
 \qquad
 \mathcal M_{\mathrm{fam}}\cap\mathcal M_{\mathrm{obs}}
 =\mathbb C I_{300}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0004

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 \tau_{300}=\tau_{20}\otimes\tau_{15}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0005

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:46`
- Строки: `46--52`

```latex
\begin{equation}
 \begin{aligned}
 E_{\mathrm{fam}}&=\operatorname{id}\otimes\tau_{15},\\
 E_{\mathrm{obs}}&=\tau_{20}\otimes\operatorname{id}.
 \end{aligned}
 \label{eq:v5-factor-expectations}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0006

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:55`
- Строки: `55--60`

```latex
\begin{equation}
 E_{\mathrm{fam}}E_{\mathrm{obs}}
 =E_{\mathrm{obs}}E_{\mathrm{fam}}
 =\tau_{300}(\,\cdot\,)I_{300}.
 \label{eq:v5-commuting-square}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0007

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:73`
- Строки: `73--75`

```latex
\begin{equation}
 \mathcal F_{\mathrm{fam}}=[d,d^\dagger]-h.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0008

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:77`
- Строки: `77--79`

```latex
\begin{equation}
 \tau_{20}(\mathcal F_{\mathrm{fam}})=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0009

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:82`
- Строки: `82--87`

```latex
\begin{equation}
 \tau_{300}\!\left[
 (\mathcal F_{\mathrm{fam}}\otimes I)
 (I\otimes\mathcal F_{\mathrm{obs}})
 \right]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0010

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:89`
- Строки: `89--96`

```latex
\begin{equation}
 \boxed{
 \tau_{300}(\mathcal F_{\mathrm{tot}}^2)
 =\tau_{20}(\mathcal F_{\mathrm{fam}}^2)
 +\tau_{15}(\mathcal F_{\mathrm{obs}}^2),
 }
 \label{eq:v5-one-trace-pythagoras}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0011

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:98`
- Строки: `98--102`

```latex
\begin{equation}
 \mathcal F_{\mathrm{tot}}
 =\mathcal F_{\mathrm{fam}}\otimes I
 +I\otimes\mathcal F_{\mathrm{obs}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0012

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:118`
- Строки: `118--120`

```latex
\begin{equation}
 \dim\operatorname{Hom}_{S_4}(\mathbb C^4,\mathbb C^3)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0013

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:122`
- Строки: `122--124`

```latex
\begin{equation}
 \dim\operatorname{End}_{A_4}(\mathbb C^3)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0014

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:126`
- Строки: `126--133`

```latex
\begin{equation}
 \boxed{
 X=\rho V,
 \qquad
 Y=\Phi I_3.
 }
 \label{eq:v5-equivariant-field-content}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0015

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:156`
- Строки: `156--162`

```latex
\begin{equation}
 V(\rho,\Phi)
 =(1-\rho^2)^2
 +(\rho^2-|\Phi|^2)^2
 +( |\Phi|^2-1)^2.
 \label{eq:v5-equivariant-radial-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0016

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:164`
- Строки: `164--167`

```latex
\begin{equation}
 \rho^2=1,
 \qquad |\Phi|^2=1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0017

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:169`
- Строки: `169--171`

```latex
\begin{equation}
 \{24,8,0\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0018

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:176`
- Строки: `176--182`

```latex
\begin{equation}
 \rho^2=\frac56,
 \qquad
 |\Phi|^2=\frac23,
 \qquad
 V_\star=\frac56.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0019

- Источник: `s2t/gates/version5_commuting_square_readout_gate.tex:184`
- Строки: `184--188`

```latex
\begin{equation}
 12-\frac{4\sqrt{21}}3,
 \qquad
 12+\frac{4\sqrt{21}}3
\end{equation}
```

## `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0020

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:18`
- Строки: `18--25`

```latex
\begin{equation}
 P_0(x)=
 \begin{pmatrix}
 1&0&0\\0&0&0\\0&0&0
 \end{pmatrix},
 \qquad x\in M.
 \label{eq:v5-sector-selection-constant-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0021

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:27`
- Строки: `27--33`

```latex
\begin{equation}
 P_0^2=P_0,
 \qquad
 dP_0=0,
 \qquad
 [P_0(x)]=\text{const}\in\mathbb{RP}^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0022

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 K=\mathbb{RP}^3\times S^1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0023

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:58`
- Строки: `58--63`

```latex
\begin{equation}
 \pi_2(K)=0,
 \qquad
 H^2(K;\mathbb Z)\simeq\mathbb Z_2.
 \label{eq:v5-sector-selection-carrier-groups}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0024

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:70`
- Строки: `70--72`

```latex
\begin{equation}
 2i^*a=i^*(2a)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0025

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 i^*a=0.
 \label{eq:v5-sector-selection-torsion-restriction}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0026

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:87`
- Строки: `87--89`

```latex
\begin{equation}
 H^2(S^4;\mathbb Z)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0027

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:108`
- Строки: `108--111`

```latex
\begin{equation}
 \sum_i Q_i=0.
 \label{eq:v5-sector-selection-charge-neutrality}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0028

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:124`
- Строки: `124--127`

```latex
\begin{equation}
 \mathcal S_{\rm loop}(V)=
 \tau\!\left([N,V]^*[N,V]\right)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0029

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:129`
- Строки: `129--131`

```latex
\begin{equation}
 \mathcal S_{\rm loop}(V_0)=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0030

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:133`
- Строки: `133--136`

```latex
\begin{equation}
 \mathcal S_{\rm loop}(V_{15})=\frac17.
 \label{eq:v5-sector-selection-loop-cost}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0031

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:141`
- Строки: `141--146`

```latex
\begin{equation}
 \Gamma_{\rm def}
 =\frac17\log\frac{m^2+a}{m^2}>0,
 \qquad a>0,quad m^2>0.
 \label{eq:v5-sector-selection-positive-response}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0032

- Источник: `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex:176`
- Строки: `176--178`

```latex
\begin{equation}
 \text{``сам вакуум обязан выбрать этот сектор''}.
\end{equation}
```

## `s2t/gates/version5_h15_neutrino_degree_split_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0033

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 15=6+2+3+3+1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0034

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 E_{15}=M_{20\times15}(\mathbb C),\qquad
 \mathcal L(E_{15})=M_{35}(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0035

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 \tau_{35}(p_{20})=\frac47,
 \qquad
 \tau_{35}(p_{15})=\frac37.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0036

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 E_{16}=M_{20\times16}(\mathbb C),\qquad
 \mathcal L(E_{16})=M_{36}(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0037

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 \tau_{36}(p_{20})=\frac59,
 \qquad
 \tau_{36}(p_{16})=\frac49.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0038

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:66`
- Строки: `66--72`

```latex
\begin{equation}
 \overline Q_L\widetilde H u_R,
 \qquad
 \overline Q_L H d_R,
 \qquad
 \overline L_L H e_R.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0039

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 \frac{c_{ij}}{\Lambda}
 (\overline{L_i^c}\,\widetilde H^*)
 (\widetilde H^\dagger L_j),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0040

- Источник: `s2t/gates/version5_h15_neutrino_degree_split_gate.tex:87`
- Строки: `87--90`

```latex
\begin{equation}
 \pi\text{-поток}+\Phi\ne0
 \Longrightarrow \operatorname{wind}\Phi=1,
\end{equation}
```

## `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0041

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 \mathcal H_{60}^{(p)}
 =\mathbb C^4_{\mathrm{menu}}\otimes
 (\mathbf{10}\oplus\overline{\mathbf5}),
 \qquad \dim\mathcal H_{60}^{(p)}=60.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0042

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:21`
- Строки: `21--26`

```latex
\begin{equation}
 \mathcal H_{45}
 =\mathbb C^3_{\mathrm{fam}}\otimes
 (\mathbf{10}\oplus\overline{\mathbf5}),
 \qquad \dim\mathcal H_{45}=45.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0043

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:30`
- Строки: `30--35`

```latex
\begin{equation}
 \mathcal H_{135}^{(p)}
 =(V_L\oplus V_G\oplus V_R)
 \otimes(\mathbf{10}\oplus\overline{\mathbf5}),
 \qquad \dim\mathcal H_{135}^{(p)}=135.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0044

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 60+135-45=150,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0045

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:43`
- Строки: `43--46`

```latex
\begin{equation}
 \dim\mathcal H_{\mathrm{par}}=300.
 \label{eq:v5-m300-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0046

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:53`
- Строки: `53--57`

```latex
\begin{equation}
 \mathcal B_{\mathrm{par}}=M_{300}(\mathbb C),
 \qquad
 \tau_{300}(A)=\frac1{300}\Tr_{300}A.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0047

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 120+270-90=300.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0048

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 \frac{45}{60}=\frac34.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0049

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 \frac{15}{45}=\frac13.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0050

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:84`
- Строки: `84--88`

```latex
\begin{equation}
 D_{135}=D_9\otimes I_{15},
 \qquad
 T_{SU(5)}=I_9\otimes T_{15},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0051

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:90`
- Строки: `90--92`

```latex
\begin{equation}
 [D_{135},T_{SU(5)}]=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0052

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:104`
- Строки: `104--107`

```latex
\begin{equation}
 X=\rho I_3,
 \qquad Y=rI_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0053

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:109`
- Строки: `109--117`

```latex
\begin{equation}
 \Spec D_{135}
 =\left\{
 0^{(45)},
 +\sqrt{\rho^2+r^2}^{\,(45)},
 -\sqrt{\rho^2+r^2}^{\,(45)}
 \right\}.
 \label{eq:v5-m300-chain-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0054

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:137`
- Строки: `137--139`

```latex
\begin{equation}
 2\cdot3\cdot15=90.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0055

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:141`
- Строки: `141--146`

```latex
\begin{equation}
 \frac1{90}\Tr\left(
 \widehat p_G[d,d^\dagger]^2\otimes I_{15}
 \right)
 =\tau_3(XX^\dagger-Y^\dagger Y)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0056

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:149`
- Строки: `149--151`

```latex
\begin{equation}
 I_{SU(3)}=I_{SU(2)}=I_{U(1)}=6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0057

- Источник: `s2t/gates/version5_modular_ko6_m60_amalgamation_gate.tex:158`
- Строки: `158--164`

```latex
\begin{equation}
 \boxed{
 \mathcal B_{\mathrm{par}}=M_{300}(\mathbb C),
 \quad
 \mathcal H_{\mathrm{par}}=\mathbb C^{300}
 }
\end{equation}
```

## `s2t/gates/version5_physical_corner_connection_classification_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0058

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:28`
- Строки: `28--30`

```latex
\begin{equation}
 {}_{M_{20}}E_{M_{15}}=M_{20\times15}(\mathbb C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0059

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:32`
- Строки: `32--35`

```latex
\begin{equation}
 \operatorname{End}_{M_{20}-M_{15}}(E)=\mathbb C I_E.
 \label{eq:v5-full-factor-connection-ambiguity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0060

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:42`
- Строки: `42--45`

```latex
\begin{equation}
 H_{15}=Q_L^{(6)}\oplus L_L^{(2)}\oplus u_R^{(3)}
 \oplus d_R^{(3)}\oplus e_R^{(1)}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0061

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:47`
- Строки: `47--51`

```latex
\begin{equation}
 \mathcal B_{\mathrm{obs}}
 =M_6(\mathbb C)\oplus M_2(\mathbb C)
 \oplus M_3(\mathbb C)\oplus M_3(\mathbb C)\oplus\mathbb C.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0062

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:53`
- Строки: `53--59`

```latex
\begin{equation}
 \mathcal B_{\mathrm{obs}}'
 =\mathbb CP_Q\oplus\mathbb CP_L\oplus\mathbb CP_u
 \oplus\mathbb CP_d\oplus\mathbb CP_e,
 \qquad \dim_{\mathbb C}=5.
 \label{eq:v5-observed-block-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0063

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:70`
- Строки: `70--74`

```latex
\begin{equation}
 \dim M_{15}'=1,
 \qquad
 \dim\mathcal B_{\mathrm{obs}}'=5
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0064

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:82`
- Строки: `82--85`

```latex
\begin{equation}
 P_\rho(\xi C)=(P_\rho\xi)C,
 \qquad C\in\mathcal B_{\mathrm{obs}}'.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0065

- Источник: `s2t/gates/version5_physical_corner_connection_classification_gate.tex:97`
- Строки: `97--102`

```latex
\begin{equation}
 G_{ss'}=\tau_{15}(P_sP_{s'})
 =\delta_{ss'}\left(\frac25,\frac2{15},\frac15,
 \frac15,\frac1{15}\right)_s.
 \label{eq:v5-observed-connection-metric}
\end{equation}
```

## `s2t/gates/version5_rank_one_tangent_junk_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0066

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 \rho=\operatorname{diag}(1,0,0),\qquad Q=I-\rho.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0067

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:18`
- Строки: `18--23`

```latex
\begin{equation}
 T_\rho\{X:\rank X\leq1\}
 =\{Z:QZQ=0\}
 =\rho M_3+M_3\rho.
 \label{eq:v5-rank-one-tangent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0068

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:29`
- Строки: `29--33`

```latex
\begin{equation}
 \mathcal E_\rho=\rho M_3Q\oplus QM_3\rho,
 \qquad \dim_{\mathbb C}\mathcal E_\rho=4.
 \label{eq:v5-rank-one-orbit-tangent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0069

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 \mathcal A_\rho=\mathbb C\rho\oplus QM_3(\mathbb C)Q
 \simeq\mathbb C\oplus M_2(\mathbb C).
 \label{eq:v5-rank-one-zero-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0070

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:45`
- Строки: `45--48`

```latex
\begin{equation}
 D_w=\begin{pmatrix}0&w^*\\w&0\end{pmatrix},
 \qquad w\in\mathbb C^2\setminus\{0\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0071

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:62`
- Строки: `62--66`

```latex
\begin{equation}
 \pi(\Omega_u^2\mathcal A_\rho)
 =\mathbb C\rho\oplus QM_3Q,
 \qquad \dim_{\mathbb C}=5.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0072

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 \sum_{a,b}c_{ab}\,a[D_w,b]=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0073

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 \sum_{a,b}c_{ab}[D_w,a][D_w,b].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0074

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:77`
- Строки: `77--83`

```latex
\begin{equation}
 \pi(d\ker\pi_1)=QM_3Q,
 \qquad
 \Omega_{D_w}^2(\mathcal A_\rho)
 \simeq\mathbb C\rho.
 \label{eq:v5-rank-one-twoform-quotient}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0075

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:92`
- Строки: `92--95`

```latex
\begin{align}
 [d_w,d_w^*]&=\operatorname{diag}(-\|w\|^2,ww^*),\\
 D_w^2&=\operatorname{diag}(\|w\|^2,ww^*).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0076

- Источник: `s2t/gates/version5_rank_one_tangent_junk_gate.tex:97`
- Строки: `97--101`

```latex
\begin{equation}
 [d_w,d_w^*]\longmapsto-\|w\|^2\rho,
 \qquad
 D_w^2\longmapsto+\|w\|^2\rho.
\end{equation}
```

## `s2t/gates/version5_real_selector_leaf_ko6_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0077

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 (a_i-a_k)D_{ij,kl}(b_j-b_l),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0078

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 A=(o,o),\quad B=(o,h),\quad C=(h,h),\quad D=(h,o)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0079

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 E_L=(s,o),\qquad E_R=(o,s).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0080

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:38`
- Строки: `38--41`

```latex
\begin{equation}
 D_{AB}=d_{AB}\otimes Y_{AB},
 \qquad Y_{AB}\in M_3(\mathbb R),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0081

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:55`
- Строки: `55--58`

```latex
\begin{equation}
 K_A(z)\mapsto
 K_A(z)-D_{AE}(K_E-z)^{-1}D_{EA}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0082

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
 A=(G,o),\qquad B=(G,h),
 \qquad G=M_3(\mathbb R).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0083

- Источник: `s2t/gates/version5_real_selector_leaf_ko6_gate.tex:73`
- Строки: `73--75`

```latex
\begin{equation}
 \operatorname{End}_{M_3(\mathbb R)}(\mathbb R^3)=\mathbb R I_3.
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0084

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:11`
- Строки: `11--18`

```latex
\begin{equation}
 \mathcal H=\ell^2(\mathbb Z)\otimes q_0\mathbb C^{105},
 \qquad
 Ne_n=ne_n,
 \qquad
 Ue_n=e_{n+1}.
 \label{eq:v5-unbounded-number-shift}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0085

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:20`
- Строки: `20--25`

```latex
\begin{equation}
 [N,U]=U,
 \qquad
 [N,U^*]=-U^*.
 \label{eq:v5-unbounded-commutators}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0086

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:31`
- Строки: `31--36`

```latex
\begin{equation}
 \bigl(C(S^1)\widehat\otimes Cl_{0,1},
 \ell^2(\mathbb Z)\widehat\otimes\Lambda^*\mathbb R,
 N\otimes\gamma_{\rm ext}\bigr),
 \label{eq:v5-unbounded-literature-cycle}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0087

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:44`
- Строки: `44--47`

```latex
\begin{equation}
 P=\chi_{[0,\infty)}(N).
 \label{eq:v5-unbounded-spectral-projection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0088

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 P\ell^2(\mathbb Z)=\ell^2(\mathbb N_0)\simeq H^2(S^1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0089

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:57`
- Строки: `57--62`

```latex
\begin{equation}
 PUP=S,
 \qquad
 PU^*P=S^*.
 \label{eq:v5-unbounded-compressions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0090

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:64`
- Строки: `64--67`

```latex
\begin{align}
 S^*S&=I,& SS^*&=I-|e_0\rangle\langle e_0|,\
 \operatorname{ind}S&=-1,& \operatorname{ind}S^*&=+1.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0091

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:70`
- Строки: `70--72`

```latex
\begin{equation}
 |e_0\rangle\langle e_0|\otimes q_0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0092

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:86`
- Строки: `86--91`

```latex
\begin{equation}
 KNK^{-1}=-N,
 \qquad
 KUK^{-1}=U^*.
 \label{eq:v5-unbounded-real-exchange}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0093

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:107`
- Строки: `107--109`

```latex
\begin{equation}
 [\mathrm{ext}]\in KKO_1(C(S^1),\mathbb R)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0094

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:117`
- Строки: `117--119`

```latex
\begin{equation}
 \partial_n:KO_n(A)\longrightarrow KO_{n-1}(B).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0095

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:122`
- Строки: `122--125`

```latex
\begin{equation}
 7-1=6\pmod 8.
 \label{eq:v5-unbounded-degree-ledger}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0096

- Источник: `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex:127`
- Строки: `127--130`

```latex
\begin{equation}
 [u_{\mathbb R},q_0]\in KO_7(C^*_{\mathbb R}(\mathbb Z)\otimes
 M_{105}(\mathbb C)_{\mathbb R})
\end{equation}
```

## `s2t/gates/version5_reduction_triangle_cocycle_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0097

- Источник: `s2t/gates/version5_reduction_triangle_cocycle_gate.tex:10`
- Строки: `10--14`

```latex
\begin{align}
 R_g&=(K,g,\mathcal E,\nabla;\text{спиновые и граничные данные}),\\
 R_s&=(\mathcal H,D;\Spec D,\text{кратности}),\\
 R_c&=(C_\tau,\tau),\qquad C_\tau=e^{-\tau H},\quad\tau>0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0098

- Источник: `s2t/gates/version5_reduction_triangle_cocycle_gate.tex:21`
- Строки: `21--28`

```latex
\begin{equation}H=-\tau^{-1}\log C_\tau.\end{equation}

\section{Точный конечный контрпример}

Связная звезда \(K_{1,4}\) и несвязное объединение
\(C_4\sqcup\{\mathrm{pt}\}\) имеют одинаковый характеристический многочлен
матрицы смежности
\begin{equation}\chi_A(\lambda)=\lambda^3(\lambda^2-4).\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0099

- Источник: `s2t/gates/version5_reduction_triangle_cocycle_gate.tex:30`
- Строки: `30--36`

```latex
\begin{equation}H_\star=3I-A_\star,\qquad H_\square=3I-A_\square\end{equation}
получаем один спектр \((1,3,3,3,5)\), а значит,
\begin{equation}
 \Spec e^{-\tau H_\star}=\Spec e^{-\tau H_\square},
 \qquad
 \Tr f(H_\star)=\Tr f(H_\square)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0100

- Источник: `s2t/gates/version5_reduction_triangle_cocycle_gate.tex:62`
- Строки: `62--65`

```latex
\begin{equation}
 R_c^{\text{богат}}=(\mathcal A,\mathcal H,C_\tau,J,\gamma;
 \text{данные первого порядка и локальности})
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0101

- Источник: `s2t/gates/version5_reduction_triangle_cocycle_gate.tex:78`
- Строки: `78--80`

```latex
\begin{equation}
 \Omega_{gsc}=\Gamma(T_{gs})+\Gamma(T_{sc})+\Gamma(T_{cg})
\end{equation}
```

## `s2t/gates/version5_superconnection_skyrme_coefficient_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0102

- Источник: `s2t/gates/version5_superconnection_skyrme_coefficient_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
 dL+L\wedge L=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0103

- Источник: `s2t/gates/version5_superconnection_skyrme_coefficient_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 A_P=P\,dP,
 \qquad F_P=P(dP)^2
\end{equation}
```

## `s2t/gates/version5_topological_closure_deficit_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-05-0104

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:14`
- Строки: `14--18`

```latex
\begin{equation}
 \widehat T_+
 =S\otimes q_0+I\otimes(1-q_0).
 \label{eq:v5-full-coefficient-toeplitz}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0105

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:20`
- Строки: `20--26`

```latex
\begin{equation}
 \widehat T_+^*\widehat T_+=I,
 \qquad
 I-\widehat T_+\widehat T_+^*
 =|e_0\rangle\langle e_0|\otimes q_0.
 \label{eq:v5-one-sided-closure-defect}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0106

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:32`
- Строки: `32--36`

```latex
\begin{equation}
 \ker F=0,
 \qquad
 \operatorname{coker}F=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0107

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:43`
- Строки: `43--47`

```latex
\begin{equation}
 \Delta_{\rm cl}(F)
 =\frac{\dim\ker F+\dim\operatorname{coker}F}{105}.
 \label{eq:v5-closure-deficit-definition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0108

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:49`
- Строки: `49--52`

```latex
\begin{equation}
 \operatorname{ind}F
 =\dim\ker F-\dim\operatorname{coker}F=-15.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0109

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 k+c\geq |k-c|.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0110

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 \Delta_{\rm cl}(F)\geq\frac{15}{105}=\frac17.
 \label{eq:v5-closure-deficit-bound}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0111

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:86`
- Строки: `86--90`

```latex
\begin{equation}
 \Delta_{\rm cl}^{\rm Real}
 =\frac{15+15}{105+105}=\frac17.
 \label{eq:v5-real-pair-closure-deficit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0112

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:93`
- Строки: `93--95`

```latex
\begin{equation}
 15\in KO_6\bigl(M_{105}(\mathbb C)_{\mathbb R}\bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0113

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:115`
- Строки: `115--117`

```latex
\begin{equation}
 S_{\rm loop}(V_{15})=\frac{30}{210}=\frac17.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-05-0114

- Источник: `s2t/gates/version5_topological_closure_deficit_gate.tex:126`
- Строки: `126--133`

```latex
\begin{equation}
 \begin{aligned}
  \text{минимальная стоимость внутреннего перехода}
  &=\text{минимальная доля незамыкания}\\
  &=\frac17.
 \end{aligned}
 \label{eq:v5-two-minima-one-seventh}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]