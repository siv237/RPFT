# Гейты Version 5, часть 4

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **114** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0001

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:13`
- Строки: `13--19`

```latex
\begin{equation}
 \mathcal O_5=
 \frac{c_{ij}}{\Lambda}
 (\overline{L_i^c}\,\widetilde H^*)
 (\widetilde H^\dagger L_j).
 \label{eq:v5-h15-weinberg-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0002

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:34`
- Строки: `34--42`

```latex
\begin{equation}
 C_3=
 \begin{pmatrix}
 0&0&1\\
 1&0&0\\
 0&1&0
 \end{pmatrix},
 \qquad C_3^3=I.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0003

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:44`
- Строки: `44--49`

```latex
\begin{equation}
 C^T=C,
 \qquad
 C_3^T C C_3=C.
 \label{eq:v5-c3-majorana-invariance}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0004

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:52`
- Строки: `52--60`

```latex
\begin{equation}
 P_0=\frac13(I+C_3+C_3^2)
 =\frac13
 \begin{pmatrix}
 1&1&1\\1&1&1\\1&1&1
 \end{pmatrix},
 \qquad Q=I-P_0.
 \label{eq:v5-c3-zero-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0005

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:62`
- Строки: `62--65`

```latex
\begin{equation}
 C=xP_0+yQ.
 \label{eq:v5-c3-majorana-family-tensor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0006

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 \tau_3(C^*C)=\frac{|x|^2+2|y|^2}{3}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0007

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:95`
- Строки: `95--98`

```latex
\begin{equation}
 P_0 C P_0=xP_0.
 \label{eq:v5-zero-compressed-majorana}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0008

- Источник: `s2t/gates/version5_h15_majorana_pairing_correspondence_gate.tex:106`
- Строки: `106--111`

```latex
\begin{equation}
 w_0=\frac37\cdot\frac13=\frac17,
 \qquad
 w_\perp=\frac37\cdot\frac23=\frac27.
 \label{eq:v5-h15-zero-line-weight}
\end{equation}
```

## `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0009

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:17`
- Строки: `17--24`

```latex
\begin{equation}
 \mathcal L(E)=
 \begin{pmatrix}
  M_{20}&E\\
  E^*&M_{15}
 \end{pmatrix}
 \simeq M_{35}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0010

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:27`
- Строки: `27--32`

```latex
\begin{equation}
 \Gamma_{\rm link}=p_{20}-p_{15},
 \qquad
 \Gamma_{\rm link}^2=I_{35}.
 \label{eq:v5-hopf-link-grading}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0011

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 [\Gamma_{\rm link},X]=2\deg(X)X.
 \label{eq:v5-hopf-link-degree}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0012

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:40`
- Строки: `40--47`

```latex
\begin{equation}
 \deg(E)=+1,
 \qquad
 \deg(E^*)=-1,
 \qquad
 \deg(M_{20}\oplus M_{15})=0.
 \label{eq:v5-hopf-link-degrees}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0013

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:56`
- Строки: `56--59`

```latex
\begin{equation}
 \deg(XY)=\deg(X)+\deg(Y).
 \label{eq:v5-hopf-degree-additivity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0014

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:61`
- Строки: `61--64`

```latex
\begin{equation}
 \deg(X^*)=-\deg(X).
 \label{eq:v5-hopf-degree-star}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0015

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:71`
- Строки: `71--76`

```latex
\begin{equation}
 \mathfrak T(X)=X\otimes L^{\otimes\deg(X)},
 \qquad
 L^{-1}:=L^*.
 \label{eq:v5-hopf-orientation-functor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0016

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:78`
- Строки: `78--81`

```latex
\begin{align}
 (E\otimes L)(E^*\otimes L^*)&\subset M_{20},\\
 (E^*\otimes L^*)(E\otimes L)&\subset M_{15},
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0017

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:95`
- Строки: `95--99`

```latex
\begin{equation}
 \rank p_{20}=20,
 \qquad
 \rank p_{15}=15.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0018

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:112`
- Строки: `112--114`

```latex
\begin{equation}
 P=nn^T
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0019

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:117`
- Строки: `117--121`

```latex
\begin{equation}
 c_1(L_n)=+1,
 \qquad
 c_1(L_{-n})=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0020

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:123`
- Строки: `123--128`

```latex
\begin{equation}
 \deg(E)=+1\longmapsto L_n,
 \qquad
 \deg(E^*)=-1\longmapsto L_{-n}=L_n^*.
 \label{eq:v5-hopf-arrow-lift-selection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0021

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:139`
- Строки: `139--142`

```latex
\begin{equation}
 J(E\otimes L)J^{-1}=E^*\otimes L^*.
 \label{eq:v5-hopf-J-oriented-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0022

- Источник: `s2t/gates/version5_hopf_line_morita_orientation_functor_gate.tex:165`
- Строки: `165--169`

```latex
\begin{equation}
 \boxed{
 E/E^*\longrightarrow L/L^*
 \longrightarrow c_1=\pm1}
\end{equation}
```

## `s2t/gates/version5_massless_holonomy_defect_index_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0023

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 C_3^3=I,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0024

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:16`
- Строки: `16--19`

```latex
\begin{equation}
 1,qquad \omega=e^{2\pi i/3},qquad \bar\omega=e^{-2\pi i/3}.
 \label{eq:v5-c3-eigenvalues}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0025

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 v_0=\frac1{\sqrt3}(1,1,1)^T.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0026

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:28`
- Строки: `28--30`

```latex
\begin{equation}
 D=-i\frac{d}{ds}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0027

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:32`
- Строки: `32--35`

```latex
\begin{equation}
 \psi(s+L)=C_3\psi(s).
 \label{eq:v5-c3-boundary-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0028

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:44`
- Строки: `44--47`

```latex
\begin{equation}
 p_{n,\alpha}=\frac{2\pi}{L}(n+\alpha),
 \qquad n\in\mathbb Z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0029

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:49`
- Строки: `49--54`

```latex
\begin{align}
 p_{n,-}&=\frac{2\pi}{L}\left(n-\frac13\right),\\
 p_{n,0}&=\frac{2\pi n}{L},\\
 p_{n,+}&=\frac{2\pi}{L}\left(n+\frac13\right).
 \label{eq:v5-third-shift-spectrum}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0030

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:56`
- Строки: `56--61`

```latex
\begin{equation}
 p_{0,0}=0,
 \qquad
 \dim_{\mathbb C}\ker D=1.
 \label{eq:v5-one-boundary-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0031

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 \Delta p=\frac{2\pi}{3L}.
 \label{eq:v5-holonomy-third-gap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0032

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:97`
- Строки: `97--100`

```latex
\begin{equation}
 \dim_{\mathbb R}\ker D\equiv1\pmod2.
 \label{eq:v5-boundary-mod-two}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0033

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:109`
- Строки: `109--113`

```latex
\begin{equation}
 \dim\ker D=1,
 \qquad
 \dim\operatorname{coker}D=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0034

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:115`
- Строки: `115--118`

```latex
\begin{equation}
 \operatorname{ind}D=0.
 \label{eq:v5-boundary-index-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0035

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:126`
- Строки: `126--128`

```latex
\begin{equation}
 \eta_{+}(0)+\eta_{-}(0)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0036

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:134`
- Строки: `134--136`

```latex
\begin{equation}
 \psi_0(s)=\frac1{\sqrt L}v_0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0037

- Источник: `s2t/gates/version5_massless_holonomy_defect_index_gate.tex:139`
- Строки: `139--141`

```latex
\begin{equation}
 \sum_{x=1}^{N}|\psi_0(x)|^4=\frac1N.
\end{equation}
```

## `s2t/gates/version5_nonordinary_architecture_fork_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0038

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 h=\operatorname{diag}(-I_3,0_3,I_3),\qquad D=d+d^\dagger.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0039

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:53`
- Строки: `53--55`

```latex
\begin{equation}
 [h,d]=d,\qquad[h,d^\dagger]=-d^\dagger.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0040

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:57`
- Строки: `57--60`

```latex
\begin{equation}
 \boxed{d=\frac12\bigl(D+[h,D]\bigr).}
 \label{eq:v5-height-oriented-differential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0041

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:65`
- Строки: `65--67`

```latex
\begin{equation}
 d=\begin{pmatrix}0&0&0\\X&0&0\\0&Y&0\end{pmatrix}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0042

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:69`
- Строки: `69--72`

```latex
\begin{equation}
 [d,d^\dagger]\big|_{V_G}=XX^\dagger-Y^\dagger Y.
 \label{eq:v5-height-middle-moment-map}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0043

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:77`
- Строки: `77--80`

```latex
\begin{equation}
 \boxed{P_G=I-h^2=\operatorname{diag}(0_3,I_3,0_3).}
 \label{eq:v5-height-middle-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0044

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:85`
- Строки: `85--90`

```latex
\begin{equation}
 S_{hH}(D,h)=\frac13\Tr_{\mathcal H}
 \left(P_G[d,d^\dagger]^2\right),
 \qquad d=\frac12(D+[h,D]).
 \label{eq:v5-height-hodge-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0045

- Источник: `s2t/gates/version5_nonordinary_architecture_fork_gate.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 \boxed{S_{hH}=\tau_3\left((XX^\dagger-Y^\dagger Y)^2\right).}
 \label{eq:v5-height-hodge-exact-target}
\end{equation}
```

## `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0046

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 M_{35}\otimes M_3\simeq M_{105}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0047

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:15`
- Строки: `15--22`

```latex
\begin{equation}
 q_0=p_{15}\otimes P_0,
 \qquad
 \rank q_0=15,
 \qquad
 \tau_{105}(q_0)=\frac{15}{105}=\frac17.
 \label{eq:v5-toeplitz-q0}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0048

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 S e_n=e_{n+1},
 \qquad n=0,1,2,\ldots
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0049

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 u_H(z)=z,
 \qquad \operatorname{wind}(u_H)=1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0050

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \mathcal H_+=H^2(S^1)\otimes q_0\mathbb C^{105},
 \qquad
 \mathbb T_+=S\otimes q_0.
 \label{eq:v5-toeplitz-coefficient-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0051

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:49`
- Строки: `49--55`

```latex
\begin{equation}
 \mathbb T_+^*\mathbb T_+=I,
 \qquad
 I-\mathbb T_+\mathbb T_+^*
 =|e_0\rangle\langle e_0|\otimes q_0.
 \label{eq:v5-toeplitz-defect-projection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0052

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 \operatorname{ind}\mathbb T_+=-15
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0053

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:65`
- Строки: `65--69`

```latex
\begin{equation}
 \Tr_{\mathcal K}(|e_0\rangle\langle e_0|)
 \tau_{105}(q_0)=1\cdot\frac17=\frac17.
 \label{eq:v5-toeplitz-defect-weight}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0054

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:85`
- Строки: `85--87`

```latex
\begin{equation}
 u_H^*(z)=z^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0055

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:89`
- Строки: `89--93`

```latex
\begin{equation}
 \mathbb T_-=S^*\otimes q_0,
 \qquad
 \operatorname{ind}\mathbb T_-=+15.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0056

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:96`
- Строки: `96--99`

```latex
\begin{equation}
 J\mathbb T_+J^{-1}=\mathbb T_-.
 \label{eq:v5-toeplitz-J-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0057

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:114`
- Строки: `114--118`

```latex
\begin{equation}
 \operatorname{ind}S=-1,
 \qquad
 \operatorname{ind}S_N=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0058

- Источник: `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex:151`
- Строки: `151--157`

```latex
\begin{equation}
 [u_H]\boxtimes[q_0]
 \xmapsto{\partial_{\mathcal T}}
 \pm[|e_0\rangle\langle e_0|\otimes q_0]
 =\pm([p_{20}]-[p_{15}])\otimes[I_3].
 \label{eq:v5-toeplitz-closed-class-bridge}
\end{equation}
```

## `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0059

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:12`
- Строки: `12--17`

```latex
\begin{equation}
 \mathcal H=\mathcal H_0^+\oplus\mathcal H_1^-\oplus\mathcal H_2^+,
 \qquad
 D=\begin{pmatrix}0&X^\dagger&0\\X&0&Y^\dagger\\0&Y&0\end{pmatrix}.
 \label{eq:v5-three-node-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0060

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 M=(X\;\;Y^\dagger):\mathcal H_0\oplus\mathcal H_2\to\mathcal H_1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0061

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:24`
- Строки: `24--26`

```latex
\begin{equation}
 A=XX^\dagger,\qquad B=Y^\dagger Y.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0062

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 \Tr f(D^2)=2\Tr_{\mathcal H_1}f(A+B)+c_f,
 \label{eq:v5-general-spectral-functional}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0063

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 \Tr(A_t-B_t)^2=(2t-1)^2\Tr S^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0064

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:59`
- Строки: `59--65`

```latex
\begin{align}
 \Tr D^4&=2\Tr(A+B)^2
 =2\Tr A^2+2\Tr B^2+4\Tr AB,
 \label{eq:v5-positive-cross}\\
 \Tr\mu^2&=\Tr A^2+\Tr B^2-2\Tr AB.
 \label{eq:v5-negative-cross}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0065

- Источник: `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex:75`
- Строки: `75--79`

```latex
\begin{equation}
 \Str f(D^2)=f(0)\operatorname{ind}M,
 \qquad \Str D^{2k}=0\quad(k>0).
 \label{eq:v5-supertrace-index}
\end{equation}
```

## `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0066

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:14`
- Строки: `14--17`

```latex
\begin{equation}
 C_{a,\nu}=\exp\!\left(-\nu\frac{2\pi}{3}\Omega(h_a)\right).
 \label{eq:v5-tetra-holonomy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0067

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:31`
- Строки: `31--35`

```latex
\begin{equation}
 u=\frac12(1,1,1,1)^T,
 \qquad
 h_a=\frac2{\sqrt3}\left(e_a-\frac14\mathbf1\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0068

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 T_a=\{u,h_a\}^{\perp},
 \qquad
 P_{T_a}=I-uu^T-h_ah_a^T.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0069

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:43`
- Строки: `43--48`

```latex
\begin{equation}
 \Omega_a^T=-\Omega_a,
 \qquad
 \Omega_a^2=-P_{T_a}.
 \label{eq:v5-transverse-complex-structure}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0070

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:55`
- Строки: `55--59`

```latex
\begin{equation}
 C_{a,\nu}|_{T_a}
 =\cos\frac{2\pi}{3}\,I
 -\nu\sin\frac{2\pi}{3}\,J_a,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0071

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:61`
- Строки: `61--63`

```latex
\begin{equation}
 e^{2\pi i/3},\qquad e^{-2\pi i/3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0072

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 \mathcal J_a=2P_a-I_4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0073

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 \mathcal J_a|_{T_a}=-I_{T_a}.
 \label{eq:v5-projector-involution-transverse}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0074

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:80`
- Строки: `80--82`

```latex
\begin{equation}
 [\mathcal J_a,J_a]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0075

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:89`
- Строки: `89--91`

```latex
\begin{equation}
 J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0076

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:94`
- Строки: `94--102`

```latex
\begin{equation}
 R(\alpha)=
 \begin{pmatrix}
  \cos2\alpha&\sin2\alpha\\
  \sin2\alpha&-\cos2\alpha
 \end{pmatrix},
 \qquad \alpha\in\mathbb R/\pi\mathbb Z.
 \label{eq:v5-reflection-circle}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0077

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:104`
- Строки: `104--108`

```latex
\begin{equation}
 R(\alpha)^2=I,qquad
 R(\alpha)JR(\alpha)=-J,qquad
 \det R(\alpha)=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0078

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:114`
- Строки: `114--116`

```latex
\begin{equation}
 \alpha=0,\quad\frac\pi3,\quad\frac{2\pi}3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0079

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:118`
- Строки: `118--120`

```latex
\begin{equation}
 R_0\longmapsto R_2\longmapsto R_1\longmapsto R_0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0080

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:124`
- Строки: `124--127`

```latex
\begin{equation}
 \{X:[X,C_3]=0,\ XJ+JX=0\}=\{0\}.
 \label{eq:v5-no-invariant-reflection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0081

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:136`
- Строки: `136--138`

```latex
\begin{equation}
 \operatorname{span}_{\mathbb R}\{I,J_a\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0082

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:147`
- Строки: `147--149`

```latex
\begin{equation}
 \mu_{\rm hol}=\frac{2\pi}{3L}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0083

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:152`
- Строки: `152--156`

```latex
\begin{equation}
 n=\cos\frac{2\pi a}{3L},
 \qquad
 m=\sin\frac{2\pi a}{3L},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0084

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:158`
- Строки: `158--161`

```latex
\begin{equation}
 \lim_{a\to0}\frac{m}{a}=\frac{2\pi}{3L}.
 \label{eq:v5-conditional-holonomy-mass}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0085

- Источник: `s2t/gates/version5_rank_one_tetrahedral_transfer_reflection_gate.tex:183`
- Строки: `183--185`

```latex
\begin{equation}
 1,\qquad e^{2\pi i/3},\qquad e^{-2\pi i/3}.
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0086

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:4`
- Строки: `4--10`

```latex
\begin{equation}
 c_6:KO_6(\mathbb C_{\mathbb R})
 \longrightarrow
 K_6(\mathbb C\otimes_{\mathbb R}\mathbb C)
 \simeq K_0(\mathbb C\oplus\mathbb C).
 \label{eq:v5-bott-comparison-target}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0087

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:21`
- Строки: `21--25`

```latex
\begin{equation}
 \mathbb C_{\mathbb R}\otimes_{\mathbb R}\mathbb C
 \simeq\mathbb C\oplus\mathbb C.
 \label{eq:v5-bott-c-complexification}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0088

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:27`
- Строки: `27--33`

```latex
\begin{align}
 c_0(n)&=(n,n),&
 c_2(n)&=(-n,n),\
 c_4(n)&=(n,n),&
 \boxed{c_6(n)=(-n,n).}
 \label{eq:v5-bott-c-even-maps}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0089

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:35`
- Строки: `35--40`

```latex
\begin{equation}
 r_6(a,b)=-a+b,
 \qquad
 \psi_6(a,b)=(-b,-a),
 \label{eq:v5-bott-r-psi-six}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0090

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:47`
- Строки: `47--54`

```latex
\begin{equation}
 c_6(1)=(-1,+1),
 \qquad
 r_6c_6(1)=2,
 \qquad
 \psi_6c_6(1)=c_6(1).
 \label{eq:v5-bott-generator-checks}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0091

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:57`
- Строки: `57--60`

```latex
\begin{equation}
 \{(-n,n):n\in\mathbb Z\}.
 \label{eq:v5-bott-antidiagonal-image}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0092

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:69`
- Строки: `69--74`

```latex
\begin{equation}
 \operatorname{ind}T_+=-15,
 \qquad
 \operatorname{ind}T_-=+15.
 \label{eq:v5-bott-existing-pair}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0093

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:76`
- Строки: `76--79`

```latex
\begin{equation}
 c_6(15)=(-15,+15).
 \label{eq:v5-bott-fifteen-image}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0094

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:88`
- Строки: `88--94`

```latex
\begin{equation}
 [T_{\mathbb R}]=15
 \quad\text{в}\quad
 KO_6\bigl(M_{105}(\mathbb C)_{\mathbb R}\bigr)
 \simeq\mathbb Z,
 \label{eq:v5-bott-real-class-fifteen}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0095

- Источник: `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex:100`
- Строки: `100--105`

```latex
\begin{equation}
 \frac{|[T_{\mathbb R}]|}{105}
 =\frac{15}{105}
 =\frac17.
 \label{eq:v5-bott-real-one-seventh}
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0096

- Источник: `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex:11`
- Строки: `11--17`

```latex
\begin{equation}
 V_{15}(z)=\left(
 zq_0+1-q_0,
 z^{-1}\overline q_0+1-\overline q_0
 \right).
 \label{eq:v5-ko7-explicit-unitary}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0097

- Источник: `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 \tau(f_+,f_-)(z)=
 \bigl(f_-(\bar z)^T,f_+(\bar z)^T\bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0098

- Источник: `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 V_{15}^{\tau}=V_{15}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0099

- Источник: `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex:32`
- Строки: `32--34`

```latex
\begin{equation}
 ([V_+],[V_-])=(15,-15).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0100

- Источник: `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
 \operatorname{ind}T_{V_+}=-15,
 \qquad
 \operatorname{ind}T_{V_-}=+15.
\end{equation}
```

## `s2t/gates/version5_spatial_extension_derrick_balance_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0101

- Источник: `s2t/gates/version5_spatial_extension_derrick_balance_gate.tex:5`
- Строки: `5--9`

```latex
\begin{equation}
 W(z,n)=\bigl(zP(n)+1-P(n)\bigr)
 \bigl(zP_0+1-P_0\bigr)^*
 \label{eq:v5-relative-bott-unitary}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0102

- Источник: `s2t/gates/version5_spatial_extension_derrick_balance_gate.tex:23`
- Строки: `23--25`

```latex
\begin{equation}
 R_*=\sqrt{b/a}.
\end{equation}
```

## `s2t/gates/version5_transition_primitive_scientific_language_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-04-0103

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:24`
- Строки: `24--27`

```latex
\begin{equation}
 {}_{A_y}E_{A_x},
 \label{eq:v5-transition-correspondence}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0104

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 {}_{A_z}F_{A_y}\widehat\otimes_{A_y}{}_{A_y}E_{A_x}.
 \label{eq:v5-transition-composition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0105

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:43`
- Строки: `43--45`

```latex
\begin{equation}
 E=M_{20\times15}(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0106

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:48`
- Строки: `48--55`

```latex
\begin{equation}
 \mathcal L(E)=
 \begin{pmatrix}
 M_{20}(\mathbb C)&E\\
 E^*&M_{15}(\mathbb C)
 \end{pmatrix}.
 \label{eq:v5-transition-linking-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0107

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:59`
- Строки: `59--64`

```latex
\begin{equation}
 EE^*=M_{20}(\mathbb C),
 \qquad
 E^*E=M_{15}(\mathbb C).
 \label{eq:v5-transitions-generate-corners}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0108

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:81`
- Строки: `81--83`

```latex
\begin{equation}
 \gamma=e_n\cdots e_2e_1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0109

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:85`
- Строки: `85--88`

```latex
\begin{equation}
 \Omega_\gamma=U_{e_n}\cdots U_{e_2}U_{e_1}.
 \label{eq:v5-transition-holonomy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0110

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:94`
- Строки: `94--96`

```latex
\begin{equation}
 U_e\longmapsto g_yU_eg_x^{-1},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0111

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:111`
- Строки: `111--119`

```latex
\begin{equation}
 W(k)=
 \begin{pmatrix}
 ne^{ik}&-im\\
 -im&ne^{-ik}
 \end{pmatrix},
 \qquad m^2+n^2=1,
 \label{eq:v5-transition-primitive-walk}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0112

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:121`
- Строки: `121--123`

```latex
\begin{equation}
 E^2=p^2+M^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0113

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:149`
- Строки: `149--154`

```latex
\begin{equation}
 P_\lambda=\frac14\sum_{n=0}^3\lambda^{-n}U^n,
 \qquad
 \lambda\in\{1,i,-1,-i\}.
 \label{eq:v5-transition-character-projectors}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-04-0114

- Источник: `s2t/gates/version5_transition_primitive_scientific_language_gate.tex:175`
- Строки: `175--184`

```latex
\begin{equation}
 \boxed{
 \begin{gathered}
 \text{соответствие Мориты --- тип стрелки},\\
 \text{колчан/группоид --- композиция маршрутов},\\
 \text{квантовый автомат --- локальный закон шага},\\
 \text{голономия и индекс --- идентичность дефекта}.
 \end{gathered}}
 \label{eq:v5-transition-language-stack}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]