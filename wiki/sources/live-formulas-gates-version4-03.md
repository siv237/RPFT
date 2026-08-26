# Гейты Version 4, часть 3

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **109** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_casimir_messenger_propagator_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0001

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:12`
- Строки: `12--15`

```latex
\begin{align}
 C(Q_L)&=\frac{21}{10},& C(u_R)&=\frac85,& C(d_R)&=\frac75,\\
 C(L_L)&=\frac9{10},& C(e_R)&=\frac35,& C(\nu_R)&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0002

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:20`
- Строки: `20--26`

```latex
\begin{equation}
 \mathcal M_s(t)=
 \begin{pmatrix}
 (t+C_L^s)I&iI\\
 -iI&(t+C_R^s)I
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0003

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:33`
- Строки: `33--37`

```latex
\begin{equation}
 Y_s=P_--\frac{
 (t+C_R^s)A_s^2+(t+C_L^s)B_s^2+i(B_sA_s-A_sB_s)
 }{(t+C_L^s)(t+C_R^s)-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0004

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 (\epsilon_{00},\epsilon_{01},\epsilon_{10},\epsilon_{11})
 =(-1,-1,-1,-1),
 \qquad t=1622.2774.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0005

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:57`
- Строки: `57--60`

```latex
\begin{align}
 u&=(0.00123241,\,0.00123349,\,1),\\
 d&=(0.00123249,\,0.00123356,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0006

- Источник: `s2t/gates/version4_casimir_messenger_propagator_gate.tex:65`
- Строки: `65--67`

```latex
\begin{equation}
 5.37\times10^{-7},
\end{equation}
```

## `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0007

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:13`
- Строки: `13--17`

```latex
\begin{equation}
 \mathcal A_{\rm q}
 =\mathbb R_0\oplus M_3(\mathbb R)_G\oplus\mathbb C_2.
 \label{eq:family-quiver-finite-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0008

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:19`
- Строки: `19--26`

```latex
\begin{equation}
 (0,0)^{\oplus3}
 \xrightarrow{\ X\ }
 (G,0)
 \xrightarrow{\ Y\ }
 (G,2).
 \label{eq:family-krajewski-label-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0009

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:34`
- Строки: `34--36`

```latex
\begin{equation}
 X\in M_3(\mathbb R).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0010

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:40`
- Строки: `40--45`

```latex
\begin{equation}
 [Y,A]=0\quad\forall A\in M_3(\mathbb R)
 \qquad\Longrightarrow\qquad
 Y=\Phi I_3.
 \label{eq:first-order-schur-pairing}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0011

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:55`
- Строки: `55--57`

```latex
\begin{equation}
 \dim_{\mathbb C}\mathcal H_F=18.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0012

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:59`
- Строки: `59--69`

```latex
\begin{equation}
 D_p=
 \begin{pmatrix}
 0&X^\dagger&0\\
 X&0&\bar\Phi I_3\\
 0&\Phi I_3&0
 \end{pmatrix},
 \qquad
 D_F=D_p\oplus\bar D_p,
 \label{eq:family-quiver-ko6-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0013

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:71`
- Строки: `71--76`

```latex
\begin{align}
 D_F&=D_F^\dagger,\\
 \{D_F,\Gamma_F\}&=0,\\
 [D_F,J_F]&=0,\\
 \{J_F,\Gamma_F\}&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0014

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:79`
- Строки: `79--82`

```latex
\begin{align}
 [\pi(a),J\pi(b)J^{-1}]&=0,\\
 [[D_F,\pi(a)],J\pi(b)J^{-1}]&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0015

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:102`
- Строки: `102--106`

```latex
\begin{equation}
 X=\rho I_3,
 \qquad
 \Phi=r\in\mathbb R
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0016

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:108`
- Строки: `108--112`

```latex
\begin{align}
 \Tr D_p^2&=6(\rho^2+r^2),\\
 \Tr D_p^4&=6(\rho^2+r^2)^2.
 \label{eq:family-quiver-ordinary-traces}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0017

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:114`
- Строки: `114--116`

```latex
\begin{equation}
 +12\rho^2r^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0018

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:118`
- Строки: `118--123`

```latex
\begin{equation}
 \tau_3(\mu_G^2)
 =(\rho^2-r^2)^2
 =\rho^4-2\rho^2r^2+r^4.
 \label{eq:family-quiver-moment-sign}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0019

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:129`
- Строки: `129--131`

```latex
\begin{equation}
 \Str D_p^4=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0020

- Источник: `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex:173`
- Строки: `173--175`

```latex
\begin{equation}
 S_{\rm rel}=\tau_3([d,d^\dagger]_G^2),
\end{equation}
```

## `s2t/gates/version4_full_field_carrier_counterterm_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0021

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:12`
- Строки: `12--18`

```latex
\begin{equation}
 \Gamma_{\rm 1loop}[M]
 =\frac12\sum_b n_b\log\det\mathcal L_b[M]
 -\frac12\sum_f n_f\log\det\mathcal D_f^2[M]
 +\Gamma_{\rm ghost}[M].
 \label{eq:full-field-one-loop-ledger}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0022

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 \operatorname{Str}M^4=67\chi^4
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0023

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:27`
- Строки: `27--33`

```latex
\begin{equation}
 \Gamma_{\rm local}^{\rm ren}[M]
 =c_0\int1+c_R\int R
 +c_{R^2}\int R^2+c_{\rm Ric}\int R_{\mu\nu}R^{\mu\nu}
 +c_{\rm Riem}\int R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}.
 \label{eq:curved-counterterm-basis}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0024

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:42`
- Строки: `42--46`

```latex
\begin{equation}
 \operatorname{Vol}(S^4_a)=1,
 \qquad
 \operatorname{Vol}(S^2_b\times S^2_b)=1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0025

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:48`
- Строки: `48--52`

```latex
\begin{equation}
 a=0.441502208724\ldots,
 \qquad
 b=0.282094791774\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0026

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:74`
- Строки: `74--76`

```latex
\begin{equation}
 \Gamma\longmapsto\Gamma+c_W\int W^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0027

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:78`
- Строки: `78--81`

```latex
\begin{equation}
 \Delta\Gamma\longmapsto
 \Delta\Gamma-c_W\frac{256\pi^2}{3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0028

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:85`
- Строки: `85--87`

```latex
\begin{equation}
 c_E\int E_4
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0029

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:116`
- Строки: `116--119`

```latex
\begin{equation}
 \frac12\log\det(\Delta_1+3\chi^2)
 -\frac12\log\det(\Delta_0+3\chi^2)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0030

- Источник: `s2t/gates/version4_full_field_carrier_counterterm_gate.tex:137`
- Строки: `137--140`

```latex
\begin{equation}
 \Gamma_{\rm nonlocal}^{\rm ren}[S^4]
 -\Gamma_{\rm nonlocal}^{\rm ren}[S^2\times S^2]
\end{equation}
```

## `s2t/gates/version4_full_profile_radial_vacuum_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0031

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:7`
- Строки: `7--9`

```latex
\begin{equation}
 S_\star(r,\theta)=\Tr f_\star(D_F(r,\theta)^2),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0032

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 f_\star(u)
 =\frac{e^{-u^2/100}+\frac1{12}e^{-10u^2}}{13/12}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0033

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:19`
- Строки: `19--21`

```latex
\begin{equation}
 \theta_{\rm slice}=1.227311.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0034

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:23`
- Строки: `23--28`

```latex
\begin{equation}
 \left.
 \partial_\sigma S_\star
 \right|_{r=1,\theta=\theta_{\rm slice}}
 =-0.755503.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0035

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:35`
- Строки: `35--39`

```latex
\begin{equation}
 r_\star=5.773295,
 \qquad
 \theta_\star\simeq0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0036

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:41`
- Строки: `41--43`

```latex
\begin{equation}
 S_\star(r_\star,\theta_\star)=5.479335.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0037

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:45`
- Строки: `45--52`

```latex
\begin{equation}
 \operatorname{Hess}S_\star
 \simeq
 \begin{pmatrix}
 0.0720145&0\\
 0&0.00709530
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0038

- Источник: `s2t/gates/version4_full_profile_radial_vacuum_gate.tex:67`
- Строки: `67--73`

```latex
\begin{equation}
 \partial_r S_f=\partial_\theta S_f=0,
 \qquad
 \operatorname{Hess}S_f>0,
 \qquad
 \theta_\star\notin\{0,\pi\}.
\end{equation}
```

## `s2t/gates/version4_gauge_casimir_family_split_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0039

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 C_s=g_3^2C_3(s)+g_2^2C_2(s)+g_1^2T_1(s)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0040

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 R_{4,s}=C_{s,L}(R_{4,A}+R_{4,D})
 +C_{s,R}(R_{4,B}+R_{4,C}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0041

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:25`
- Строки: `25--32`

```latex
\begin{align}
 C_{u,L}=C_{d,L}&=\frac43g_3^2+\frac34g_2^2+\frac1{60}g_1^2,\\
 C_{u,R}&=\frac43g_3^2+\frac4{15}g_1^2,
 &C_{d,R}&=\frac43g_3^2+\frac1{15}g_1^2,\\
 C_{\nu,L}=C_{e,L}&=\frac34g_2^2+\frac3{20}g_1^2,\\
 C_{\nu,R}&=0,
 &C_{e,R}&=\frac35g_1^2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0042

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:38`
- Строки: `38--43`

```latex
\begin{equation}
 C_{d,R}C_{e,L}-C_{e,R}C_{d,L}
 =-\frac15\left(
 2g_1^2g_2^2+3g_1^2g_3^2-5g_2^2g_3^2
 \right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0043

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 g_1=0.461423,
 \qquad g_2=0.651724,
 \qquad g_3=1.217716.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0044

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:63`
- Строки: `63--68`

```latex
\begin{align}
 u:&\quad(0.187192,\,0.378318,\,1),\\
 d:&\quad(0.128103,\,0.423190,\,1),\\
 \nu:&\quad(0,\,0.399664,\,1),\\
 e:&\quad(0.179730,\,0.342420,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0045

- Источник: `s2t/gates/version4_gauge_casimir_family_split_gate.tex:73`
- Строки: `73--80`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.3864&0.8672&0.3141\\
 0.8551&0.4453&0.2653\\
 0.3455&0.2228&0.9116
 \end{pmatrix},
\end{equation}
```

## `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0046

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:7`
- Строки: `7--11`

```latex
\begin{equation}
 S_{\rm bare}[D;\Lambda]
 =\Tr f(D^2/\Lambda^2).
 \label{eq:gaussian-bare-spectral-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0047

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 f(u)=e^{-u}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0048

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 f_2=\int_0^\infty e^{-u}\,du=1,
 \qquad
 f_0=f(0)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0049

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:32`
- Строки: `32--37`

```latex
\begin{equation}
 a_4(D_M^2)
 =\frac1{360(4\pi)^2}
 \int_M\left(11E_4-18W^2\right).
 \label{eq:dirac-a4-ew-ledger}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0050

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \Delta a_4
 :=a_4(S^4)-a_4(S^2\times S^2)
 =\frac{13}{90}>0.
 \label{eq:dirac-a4-carrier-difference}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0051

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:55`
- Строки: `55--61`

```latex
\begin{equation}
 \lambda_\ell(D)=\pm\frac{\ell+2}{a},
 \qquad
 d_\ell(D^2)=8\binom{\ell+3}{3},
 \qquad \ell=0,1,\ldots.
 \label{eq:s4-dirac-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0052

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:66`
- Строки: `66--70`

```latex
\begin{equation}
 \lambda_\ell(D)=\pm\frac{\ell+1}{b},
 \qquad
 d_\ell(D^2)=4(\ell+1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0053

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 D_{22}^2=D_1^2\otimes1+1\otimes D_2^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0054

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:78`
- Строки: `78--82`

```latex
\begin{equation}
 a=\left(\frac3{8\pi^2}\right)^{1/4},
 \qquad
 b=\left(\frac1{16\pi^2}\right)^{1/4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0055

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:84`
- Строки: `84--88`

```latex
\begin{equation}
 \Delta_D(t)
 =\Tr_{S^4}e^{-tD^2}
 -\Tr_{S^2\times S^2}e^{-tD^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0056

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:90`
- Строки: `90--93`

```latex
\begin{equation}
 \boxed{t_*=0.124153169935769\ldots.}
 \label{eq:gaussian-dirac-crossing}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0057

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:95`
- Строки: `95--100`

```latex
\begin{equation}
 \begin{cases}
 \Delta_D(t)<0,&0<t<t_*,\quad S^4\text{ preferred},\\
 \Delta_D(t)>0,&t>t_*,\quad S^2\times S^2\text{ preferred}.
 \end{cases}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0058

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:122`
- Строки: `122--124`

```latex
\begin{equation}
 D=D_M\otimes1+\gamma^5\otimes D_F
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0059

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:126`
- Строки: `126--128`

```latex
\begin{equation}
 D^2=D_M^2\otimes1+1\otimes D_F^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0060

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:130`
- Строки: `130--135`

```latex
\begin{equation}
 \Tr e^{-tD^2}
 =\Tr e^{-tD_M^2}\,
  \Tr e^{-tD_F^2}.
 \label{eq:almost-commutative-heat-factorization}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0061

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:144`
- Строки: `144--146`

```latex
\begin{equation}
 \frac a\sigma=1.35139219568654\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0062

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:148`
- Строки: `148--152`

```latex
\begin{equation}
 t_{\rm corr}=\sigma^2
 =\left(\frac{a}{1.35139219568654\ldots}\right)^2
 =0.106734039959646\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0063

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:154`
- Строки: `154--156`

```latex
\begin{equation}
 t_{\rm corr}<t_*,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0064

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:158`
- Строки: `158--160`

```latex
\begin{equation}
 \Delta_D(t_{\rm corr})=-0.034581798856\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0065

- Источник: `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex:174`
- Строки: `174--180`

```latex
\begin{equation}
 \Str\mathbf1=6-8=-2,
 \qquad
 \frac{\Str M^2}{\chi^2}=13,
 \qquad
 \frac{\Str M^4}{\chi^4}=67.
\end{equation}
```

## `s2t/gates/version4_one_ratio_family_functional_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0066

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:6`
- Строки: `6--9`

```latex
\begin{equation}
 R_s(t)=R_{4,s}-tR_{2,s},
 \qquad t\ge0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0067

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:16`
- Строки: `16--19`

```latex
\begin{align}
 u_{\rm target}&=(1.25217\times10^{-5},\,0.00736232,\,1),\\
 d_{\rm target}&=(0.00111722,\,0.0223445,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0068

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 t_{\rm mass}=4.093172,
 \qquad
 \operatorname{RMS}_{\log}=1.912066.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0069

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:30`
- Строки: `30--33`

```latex
\begin{align}
 u&=(1.35416\times10^{-5},\,0.166551,\,1),\\
 d&=(0.000609176,\,0.187383,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0070

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:35`
- Строки: `35--37`

```latex
\begin{equation}
 (1.08,\,22.62,\,1.83,\,8.39).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0071

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:44`
- Строки: `44--51`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.998769&0.044790&0.021328\\
 0.045259&0.998730&0.022126\\
 0.020315&0.023060&0.999528
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0072

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:53`
- Строки: `53--56`

```latex
\begin{equation}
 (s_{12},s_{23},s_{13})
 =(0.044800,\,0.022131,\,0.021328),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0073

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 (0.22501,\,0.04183,\,0.003732).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0074

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:62`
- Строки: `62--64`

```latex
\begin{equation}
 (0.199,\,0.529,\,5.715),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0075

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:66`
- Строки: `66--68`

```latex
\begin{equation}
 \frac{|J_q|}{J_{\rm CKM}}=0.0630.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0076

- Источник: `s2t/gates/version4_one_ratio_family_functional_gate.tex:80`
- Строки: `80--82`

```latex
\begin{equation}
 21.84
\end{equation}
```

## `s2t/gates/version4_quadratic_parent_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0077

- Источник: `s2t/gates/version4_quadratic_parent_selector_gate.tex:11`
- Строки: `11--19`

```latex
\begin{equation}
\mathcal S(H)=
\left(
\|[H,T_p]\|_F^2,
\|[H,T_q]\|_F^2,
\|[H,S]\|_F^2,
\|[H,P_-]\|_F^2
\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0078

- Источник: `s2t/gates/version4_quadratic_parent_selector_gate.tex:38`
- Строки: `38--43`

```latex
\begin{equation}
V_{\rm quad}(H)=
\|[H,T_p]\|_F^2
+\frac14\|[H,T_q]\|_F^2
+\frac15\|[H,S]\|_F^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0079

- Источник: `s2t/gates/version4_quadratic_parent_selector_gate.tex:45`
- Строки: `45--47`

```latex
\begin{equation}
V_{\rm quad}^{\min}=\frac{16}{5}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0080

- Источник: `s2t/gates/version4_quadratic_parent_selector_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
[H_A,H_B]=0.
\end{equation}
```

## `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0081

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:7`
- Строки: `7--14`

```latex
\begin{equation}
 S_{\rm raw}[\widehat C]
 =\Tr f\!\left(\frac{\widehat C}{\Lambda^2}\right),
 \qquad
 \widehat C=e^{-\tau\Delta},
 \qquad \tau=\sigma^2.
 \label{eq:toe-raw-spectral-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0082

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:23`
- Строки: `23--25`

```latex
\begin{equation}
 f(c_n/\Lambda^2)\longrightarrow f(0)\ne0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0083

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:61`
- Строки: `61--64`

```latex
\begin{equation}
 H_C:=-\frac1\tau\log\widehat C=\Delta
 \label{eq:correlation-log-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0084

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:67`
- Строки: `67--74`

```latex
\begin{equation}
 S_{\rm EFT}[\widehat C]
 =\Tr f\!\left(
 -\frac{\log\widehat C}{\tau\Lambda^2}
 \right)
 =\Tr f\!\left(\frac{\Delta}{\Lambda^2}\right).
 \label{eq:corrected-correlation-spectral-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0085

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:82`
- Строки: `82--88`

```latex
\begin{equation}
 \widehat C
 \longleftrightarrow
 H_C=-\tau^{-1}\log\widehat C
 \longleftrightarrow
 \Tr f(H_C/\Lambda^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0086

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:97`
- Строки: `97--99`

```latex
\begin{equation}
 S_f(C_1\oplus C_2)=S_f(C_1)+S_f(C_2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0087

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:101`
- Строки: `101--104`

```latex
\begin{equation}
 F_\tau(C_1\oplus C_2)
 =-\frac1\tau\log\bigl(\Tr C_1+\Tr C_2\bigr),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0088

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:106`
- Строки: `106--109`

```latex
\begin{equation}
 F_\tau(C_1)+F_\tau(C_2)
 =-\frac1\tau\log\bigl((\Tr C_1)(\Tr C_2)\bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0089

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:122`
- Строки: `122--126`

```latex
\begin{equation}
 S_{\rm state}[\widehat C]
 =-\frac1\tau\log\Tr\widehat C.
 \label{eq:outer-log-state-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0090

- Источник: `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex:155`
- Строки: `155--163`

```latex
\begin{equation}
 \boxed{
 \begin{aligned}
 S_{\rm EFT}[C]
 &=\Tr f\!\left(-\frac{\log C}{\tau\Lambda^2}\right),\\
 S_{\rm state}[C]
 &=-\frac1\tau\log\Tr C.
 \end{aligned}}
\end{equation}
```

## `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0091

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:6`
- Строки: `6--9`

```latex
\begin{equation}
 \frac{\partial}{\partial\chi}
 \Delta\Gamma_{\rm AP-P}(\chi)=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0092

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:16`
- Строки: `16--20`

```latex
\begin{equation}
 x\mapsto e^{-i\theta}x,
 \qquad
 z\mapsto e^{+i\theta}z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0093

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 |x|=|z|=\frac{\chi}{\sqrt2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0094

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:26`
- Строки: `26--29`

```latex
\begin{equation}
 \Tr_{\rm orb}(D_\mu\Phi D^\mu\Phi)
 \supset4\chi^2A_\mu A^\mu.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0095

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 \frac{m_A^2}{\chi^2}=8g^2=3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0096

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 \Delta_0+\xi m_A^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0097

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:53`
- Строки: `53--61`

```latex
\begin{equation}
 x=\chi R_3,
 \qquad
 r=\frac{R_1}{R_3},
 \qquad
 a_k=k+\frac32,
 \qquad
 d_k=(k+1)(k+2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0098

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:63`
- Строки: `63--69`

```latex
\begin{equation}
 \Delta\Gamma_{\rm AP-P}(x;r)
 =-2\sum_{k=0}^\infty d_k\,mathcal I(\rho_k),
 \qquad
 \rho_k=r\sqrt{a_k^2+x^2},
 \label{eq:spin-branch-mass-ratio}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0099

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:71`
- Строки: `71--75`

```latex
\begin{equation}
 \mathcal I(\rho)
 =\log\frac{\cosh(2\pi\rho)+1}{\cosh(2\pi\rho)-1}
 =2\log\coth(\pi\rho)>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0100

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:83`
- Строки: `83--86`

```latex
\begin{equation}
 \mathcal I'(\rho)
 =-\frac{4\pi}{\sinh(2\pi\rho)},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0101

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:88`
- Строки: `88--96`

```latex
\begin{equation}
 \frac{\partial\Delta\Gamma_{\rm AP-P}}{\partial x}
 =8\pi r x
 \sum_{k=0}^\infty
 \frac{d_k}
 {\sqrt{a_k^2+x^2}\,
  \sinh\left(2\pi r\sqrt{a_k^2+x^2}\right)}.
 \label{eq:spin-branch-positive-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0102

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:98`
- Строки: `98--101`

```latex
\begin{equation}
 \frac{\partial\Delta\Gamma_{\rm AP-P}}{\partial x}>0
 \qquad(x>0).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0103

- Источник: `s2t/gates/version4_spin_branch_mass_stationarity_gate.tex:104`
- Строки: `104--106`

```latex
\begin{equation}
 \Delta\Gamma_{\rm AP-P}(x;r)\longrightarrow0^{-}.
\end{equation}
```

## `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-03-0104

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 \lambda_{\mathrm{HK}}=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0105

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:15`
- Строки: `15--17`

```latex
\begin{equation}
 V_B=-\mu^2\Tr D_F^2+\lambda_{\mathrm{tr}}\Tr D_F^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0106

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 \lambda_{\mathrm{tr}}
 =c_{\mathrm{HK}}\lambda_{\mathrm{HK}},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0107

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:30`
- Строки: `30--35`

```latex
\begin{align}
 \lambda_{\mathrm{tr}}&<0.056684
 &&\text{для reduced measure},\\
 \lambda_{\mathrm{tr}}&<0.028906
 &&\text{для full KO6 measure}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0108

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:37`
- Строки: `37--39`

```latex
\begin{equation}
 17.64,\qquad 34.59,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-03-0109

- Источник: `s2t/gates/version4_stationary_endpoint_obstruction_gate.tex:41`
- Строки: `41--44`

```latex
\begin{align}
 m_{\theta,\rm red}^2&=7.54653,\\
 m_{\theta,\rm full}^2&=7.76875.
\end{align}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]