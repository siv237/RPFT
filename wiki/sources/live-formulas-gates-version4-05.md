# Гейты Version 4, часть 5

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **111** блочных формул из **12** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0001

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:13`
- Строки: `13--18`

```latex
\begin{align}
 U_A&=I_3,&
 U_B&=\operatorname{diag}(-1,1,1),\\
 U_C&=\operatorname{diag}(1,-1,1),&
 U_D&=-I_3.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0002

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 U^T D_-U=D_+.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0003

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:25`
- Строки: `25--29`

```latex
\begin{equation}
 P_-H_uH_d^-
 =
 -P_-H_uH_d^+.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0004

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 \det U=-1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0005

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 T_p,\qquad T_q,\qquad S,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0006

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 \left\{
 \operatorname{diag}(\alpha,\beta,\beta)
 \right\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0007

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:72`
- Строки: `72--79`

```latex
\begin{align}
 \Tr(\rho(S)D_-^4)&=\frac{13}{2},
 &
 \Tr(\rho(S)D_+^4)&=\frac{17}{2},\\
 \Tr(\rho(P_-)D_-^4)&=\frac{83}{4},
 &
 \Tr(\rho(P_-)D_+^4)&=\frac{79}{4}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0008

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 V_{\rm emb}(D)=
 \lambda\,\Tr(\rho(P_-)D^4),
 \qquad \lambda>0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0009

- Источник: `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex:99`
- Строки: `99--101`

```latex
\begin{equation}
 \omega_-(X)=\Tr(\rho(P_-)X)
\end{equation}
```

## `s2t/gates/version4_base_k_zeta_determinant_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0010

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:13`
- Строки: `13--19`

```latex
\begin{equation}
 m_s^2=4\chi^2,
 \qquad
 m_A^2=3\chi^2,
 \qquad
 m_f^2=\chi^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0011

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:22`
- Строки: `22--31`

```latex
\begin{align}
 \Gamma_{K,\mathfrak s,\rho}^{(1)}(\chi)
 ={}&\frac32\log\det_{\zeta,\mu}(\Delta_0+4\chi^2)
 \\
 &+\frac12\log\det_{\zeta,\mu}(\Delta_1+3\chi^2)
 -\frac12\log\det_{\zeta,\mu}(\Delta_0+3\chi^2)
 \\
 &-\log\det_{\zeta,\mu}(D_{K,\mathfrak s,\rho}^2+\chi^2).
 \label{eq:base-k-full-determinant}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0012

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:39`
- Строки: `39--44`

```latex
\begin{equation}
 N_0
 =3\cdot4^2-2\cdot4\cdot1^2+3\cdot3^2
 =48-8+27
 =67.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0013

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
 B_0=\frac{67}{64\pi^2}>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0014

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:53`
- Строки: `53--55`

```latex
\begin{equation}
 (b_0,b_1,b_2,b_3,b_4)=(1,1,0,1,1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0015

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:60`
- Строки: `60--66`

```latex
\begin{align}
 &\log\det(\Delta_1+M^2)-\log\det(\Delta_0+M^2)
 \\
 &\qquad=
 \log\det(\Delta_{1,\mathrm{coex}}^{\mathrm{nh}}+M^2)
 +(b_1-b_0)\log M^2,
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0016

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:71`
- Строки: `71--75`

```latex
\begin{equation}
 \Gamma_A^{(1)}
 =\frac12\log\det_{\zeta,\mu}
 (\Delta_{1,\mathrm{coex}}^{\mathrm{nh}}+3\chi^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0017

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:86`
- Строки: `86--93`

```latex
\begin{equation}
 \lambda_{\ell,m}^{(0)}
 =\frac{\ell(\ell+2)+m^2}{R^2},
 \qquad
 \ell=0,2,4,\ldots,
 \qquad
 m\in\mathbb Z,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0018

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:97`
- Строки: `97--105`

```latex
\begin{equation}
 \zeta_0(s;c)
 =\sum_{\substack{\ell\ge0\\ \ell\ \mathrm{even}}}
 (\ell+1)^2
 \sum_{m\in\mathbb Z}
 \left[
 \frac{\ell(\ell+2)+m^2}{R^2}+c\chi^2
 \right]^{-s}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0019

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:114`
- Строки: `114--117`

```latex
\begin{equation}
 \log\det_{\zeta,\mu}P
 =-\zeta_P'(0)-\zeta_P(0)\log\mu^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0020

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:121`
- Строки: `121--124`

```latex
\begin{equation}
 \mu\frac{d}{d\mu}\Gamma_K^{(1)}
 =C_0R_K^2+C_2R_K\chi^2+C_4\chi^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0021

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:126`
- Строки: `126--134`

```latex
\begin{equation}
 \Gamma_K^{\mathrm{ren}}
 =\Gamma_K^{(1)}
 +\int_Kd\operatorname{vol}
 \left(
 \lambda_0R_K^2+\lambda_2R_K\chi^2+\lambda_4\chi^4
 \right).
 \label{eq:base-k-local-completion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0022

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:142`
- Строки: `142--146`

```latex
\begin{equation}
 \lambda_2
 =-\frac{F'(\chi_*)+4\lambda_4\chi_*^3}
 {2R_K\chi_*}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0023

- Источник: `s2t/gates/version4_base_k_zeta_determinant_gate.tex:150`
- Строки: `150--152`

```latex
\begin{equation}
 \lambda_4\mapsto\lambda_4+2B_0t.
\end{equation}
```

## `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0024

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:4`
- Строки: `4--6`

```latex
\begin{equation}
 \lambda_{0D}=2\pi^3\simeq62.01255.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0025

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:15`
- Строки: `15--21`

```latex
\begin{equation}
 \Gamma_{0D}(r,\theta)
 =
 2\pi^3V_B(r,\theta)
 +\Gamma_{\rm Pf}(r,\theta)
 +\Gamma_{\rm matter}(r\sin\theta).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0026

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:27`
- Строки: `27--31`

```latex
\begin{equation}
 r_\star=1.000413,
 \qquad
 \theta_\star\simeq0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0027

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 495.851,\qquad6464.465.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0028

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:41`
- Строки: `41--45`

```latex
\begin{equation}
 r_\star=1.000825,
 \qquad
 \theta_\star\simeq0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0029

- Источник: `s2t/gates/version4_corrected_zero_mode_pfaffian_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 496.277,\qquad6479.617.
\end{equation}
```

## `s2t/gates/version4_cross_sector_cp_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0030

- Источник: `s2t/gates/version4_cross_sector_cp_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
\mathcal C(H_u,H_d)=\|[H_u,H_d]\|_F^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0031

- Источник: `s2t/gates/version4_cross_sector_cp_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
\mathcal C_{\max}=6
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0032

- Источник: `s2t/gates/version4_cross_sector_cp_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
\Tr[H_u,H_d]^3=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0033

- Источник: `s2t/gates/version4_cross_sector_cp_gate.tex:61`
- Строки: `61--63`

```latex
\begin{equation}
K_P=\frac{P-P^\dagger}{2i}.
\end{equation}
```

## `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0034

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:14`
- Строки: `14--20`

```latex
\begin{equation}
 n_a=B^T\operatorname{diag}\!\left[
 \frac{2}{\sqrt3}\left(P_a-\frac14I_4\right)
 \right],
 \qquad a=1,\ldots,4.
 \label{eq:project-tetrahedral-axes}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0035

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:22`
- Строки: `22--28`

```latex
\begin{equation}
 \|n_a\|=1,
 \qquad
 \sum_an_a=0,
 \qquad
 n_a\cdot n_b=-\frac13\quad(a\ne b).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0036

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:33`
- Строки: `33--36`

```latex
\begin{equation}
 \mathcal T_{ijk}=\sum_{a=1}^4(n_a)_i(n_a)_j(n_a)_k.
 \label{eq:project-spin-three-tensor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0037

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 \mathcal T_{iik}=\sum_a\|n_a\|^2(n_a)_k=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0038

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:46`
- Строки: `46--49`

```latex
\begin{equation}
 \operatorname{Stab}_{SO(3)}(\mathcal T)=A_4.
 \label{eq:so3-to-a4-breaking}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0039

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:67`
- Строки: `67--72`

```latex
\begin{equation}
 \operatorname{Stab}_{A_4}(n_a)
 =\{1,C_{a,+},C_{a,-}\}
 \simeq\mathbb Z_3.
 \label{eq:projector-z3-stabilizer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0040

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:74`
- Строки: `74--80`

```latex
\begin{equation}
 |A_4|=12,
 \qquad
 |\operatorname{Orb}(n_a)|=4,
 \qquad
 |\operatorname{Stab}(n_a)|=3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0041

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:85`
- Строки: `85--89`

```latex
\begin{equation}
 [A_4,A_4]=V_4,
 \qquad
 A_4^{\rm ab}=A_4/V_4\simeq\mathbb Z_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0042

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:97`
- Строки: `97--102`

```latex
\begin{equation}
 \widetilde C_{a,\nu}^{,3}=-1,
 \qquad
 \widetilde C_{a,\nu}^{,6}=1.
 \label{eq:binary-z6-lift}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0043

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:123`
- Строки: `123--125`

```latex
\begin{equation}
 U(1)_{B-L}\longrightarrow\mathbb Z_2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0044

- Источник: `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex:130`
- Строки: `130--141`

```latex
\begin{equation}
 \boxed{
 \begin{aligned}
 \text{ordinary charge-two }B-L\text{ texture}
 &\quad\Rightarrow\quad
 \text{Majorana pairing и unit vortex},\\
 \text{tetrahedral family carrier}+P_a
 &\quad\Rightarrow\quad
 \text{residual }\mathbb Z_3\text{ frame holonomy}.
 \end{aligned}}
 \label{eq:two-role-root-architecture}
\end{equation}
```

## `s2t/gates/version4_family_square_spectral_selector_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0045

- Источник: `s2t/gates/version4_family_square_spectral_selector_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 D_A=aP_-,
 \qquad
 D_B=b e^{i\phi}H,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0046

- Источник: `s2t/gates/version4_family_square_spectral_selector_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 V_F=-\mu^2\Tr D_F^2+\lambda\Tr D_F^4,
 \qquad \lambda>0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0047

- Источник: `s2t/gates/version4_family_square_spectral_selector_gate.tex:26`
- Строки: `26--28`

```latex
\begin{equation}
 \phi=\pm\frac{\pi}{2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0048

- Источник: `s2t/gates/version4_family_square_spectral_selector_gate.tex:34`
- Строки: `34--38`

```latex
\begin{align}
 \Tr D_F^2&=4a^2+12b^2,\\
 \Tr D_F^4\big|_{\phi=\pm\pi/2}&=8a^4+24b^4,\\
 V_{\min}&=-2\,\frac{\mu^4}{\lambda}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0049

- Источник: `s2t/gates/version4_family_square_spectral_selector_gate.tex:40`
- Строки: `40--44`

```latex
\begin{align}
 \Tr D_F^2&=4a^2+6b^2,\\
 \Tr D_F^4\big|_{\phi=\pm\pi/2}&=8a^4+9b^4,\\
 V_{\min}&=-\frac32\,\frac{\mu^4}{\lambda}.
\end{align}
```

## `s2t/gates/version4_orientation_odd_cp_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0050

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:5`
- Строки: `5--9`

```latex
\begin{equation}
H_P=\frac{P+P^\dagger}{2},
\qquad
K_P=\frac{P-P^\dagger}{2i},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0051

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:12`
- Строки: `12--15`

```latex
\begin{equation}
X_P(r)=H_P+rK_P,
\qquad r\in\mathbb R.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0052

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:20`
- Строки: `20--27`

```latex
\begin{equation}
\Spec X_P(r)=
\left(
1,
-\frac12+\frac{\sqrt3}{2}r,
-\frac12-\frac{\sqrt3}{2}r
\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0053

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
\mathcal H_u=X_u^2,
\qquad
\mathcal H_d=X_d^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0054

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
\Tr[\mathcal H_u,\mathcal H_d]^3\ne0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0055

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
\boxed{\Tr[\mathcal H_u,\mathcal H_d]^3\equiv0.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0056

- Источник: `s2t/gates/version4_orientation_odd_cp_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
\left\{\frac13,\frac23\right\}
\end{equation}
```

## `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0057

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:10`
- Строки: `10--12`

```latex
\begin{equation}
 \mathcal A_F^{PS}=\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0058

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:14`
- Строки: `14--18`

```latex
\begin{equation}
 V_R=(2_R,1_L,4_4),
 \qquad
 V_L=(1_R,2_L,4_4),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0059

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 \dim_\mathbb C V_R=8,
 \qquad
 \dim_\mathbb C V_L=8.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0060

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 \mathcal H_F=V_R\oplus V_L\oplus V_R^c\oplus V_L^c
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0061

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 \Gamma_F=\operatorname{diag}(+I_8,-I_8,-I_8,+I_8),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0062

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:37`
- Строки: `37--41`

```latex
\begin{equation}
 R\leftrightarrow R^c,
 \qquad
 L\leftrightarrow L^c.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0063

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:47`
- Строки: `47--56`

```latex
\begin{equation}
 D_F=
 \begin{pmatrix}
 0&Y&M_R&0\\
 Y^\dagger&0&0&M_L\\
 M_R^\dagger&0&0&\bar Y\\
 0&M_L^\dagger&Y^T&0
 \end{pmatrix},
 \label{eq:ps-explicit-df}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0064

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 M_R^T=M_R,
 \qquad
 M_L^T=M_L.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0065

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:64`
- Строки: `64--72`

```latex
\begin{equation}
 D_F=D_F^\dagger,
 \qquad
 \{D_F,\Gamma_F\}=0,
 \qquad
 D_FP_J=P_J\bar D_F,
 \qquad
 \{P_J,\Gamma_F\}=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0066

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:77`
- Строки: `77--80`

```latex
\begin{equation}
 \operatorname{Hom}(V_L,V_R)
 =(2_R,2_L,1_4)\oplus(2_R,2_L,15_4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0067

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:82`
- Строки: `82--88`

```latex
\begin{align}
 \operatorname{Sym}^2(2_R\otimes4_4)
 &=(\operatorname{Sym}^22_R\otimes\operatorname{Sym}^24_4)
 \\&\quad\oplus
 (\Lambda^22_R\otimes\Lambda^24_4)\\
 &=(3_R,1_L,10_4)\oplus(1_R,1_L,6_4),
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0068

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:90`
- Строки: `90--92`

```latex
\begin{equation}
 M_L:\quad(1_R,3_L,10_4)\oplus(1_R,1_L,6_4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0069

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:95`
- Строки: `95--97`

```latex
\begin{equation}
 64+36+36=136.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0070

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:110`
- Строки: `110--116`

```latex
\begin{equation}
 \phi\sim(2_R,2_L,1_4),
 \qquad
 \Delta\sim(2_R,1_L,4_4),
 \qquad
 \Sigma_4\sim(1_R,1_L,15_4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0071

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:118`
- Строки: `118--123`

```latex
\begin{align}
 Y={}&(k_\nu\phi+k_e\widetilde\phi)\otimes\Sigma_4
 +(k_u\phi+k_d\widetilde\phi)\otimes(I_4-\Sigma_4),\\
 (M_R)_{\dot aI,\dot bJ}={}&
 k_{\nu_R}^*\Delta_{\dot aJ}\Delta_{\dot bI}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0072

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:126`
- Строки: `126--128`

```latex
\begin{equation}
 4_\phi+8_\Delta+15_{\Sigma_4}=27
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0073

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:131`
- Строки: `131--133`

```latex
\begin{equation}
 8_\phi+16_\Delta+15_{\Sigma_4}=39
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0074

- Источник: `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex:155`
- Строки: `155--157`

```latex
\begin{equation}
 [[D_F,\pi(a)],J\pi(b)J^{-1}]=0.
\end{equation}
```

## `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0075

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 h=\operatorname{diag}(-I_4,0_2,I_4)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0076

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:16`
- Строки: `16--18`

```latex
\begin{equation}
 \alpha_t(X)=e^{ith}Xe^{-ith}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0077

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:21`
- Строки: `21--26`

```latex
\begin{equation}
 \mathcal B_h=\operatorname{Fix}(\alpha)
 =\operatorname{End}(\bar4)\oplus
  \operatorname{End}(2_R)\oplus\operatorname{End}(4).
 \label{eq:ps-relative-fixed-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0078

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:29`
- Строки: `29--32`

```latex
\begin{equation}
 E_h(X)=\frac1{2\pi}\int_0^{2\pi}\alpha_t(X)\,dt.
 \label{eq:ps-relative-expectation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0079

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 S_{\rm quot}[F]
 =\inf_{C\in\mathcal B_h}\|F-C\|_F^2.
 \label{eq:ps-relative-quotient-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0080

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 \|F-C\|_F^2
 =\|F-E_h(F)\|_F^2+\|E_h(F)-C\|_F^2.
 \label{eq:ps-relative-pythagoras}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0081

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 C_\star=E_h(F),
 \qquad
 \boxed{S_{\rm quot}[F]=\|F-E_h(F)\|_F^2.}
 \label{eq:ps-relative-auxiliary-elimination}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0082

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 Q_h=\frac14\operatorname{ad}_h^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0083

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:73`
- Строки: `73--79`

```latex
\begin{align}
 F-E_h(F)&=Q_hF,\\
 S_{\rm quot}[F]
 &=\langle F,Q_hF\rangle_F
 =\left\|\frac12[h,F]\right\|_F^2.
 \label{eq:ps-relative-quotient-dirichlet}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0084

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:84`
- Строки: `84--89`

```latex
\begin{equation}
 \boxed{
 S_{\rm quot}[\mathcal D_\Delta^2]
 =4\det(\Delta\Delta^\dagger).}
 \label{eq:ps-relative-quotient-selector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0085

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:103`
- Строки: `103--105`

```latex
\begin{equation}
 E_h(UFU^\dagger)=UE_h(F)U^\dagger
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0086

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:116`
- Строки: `116--119`

```latex
\begin{equation}
 V_\Delta=-\rho^2+\tau^2
 +4\lambda_{\rm rel}\det(\Delta\Delta^\dagger).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0087

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:121`
- Строки: `121--128`

```latex
\begin{equation}
 8\sqrt2\ (1),
 \qquad
 0\ (9),
 \qquad
 \sqrt2(4\lambda_{\rm rel}-2)\ (6).
 \label{eq:ps-relative-parent-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0088

- Источник: `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex:130`
- Строки: `130--132`

```latex
\begin{equation}
 \lambda_{\rm rel}>\frac12.
\end{equation}
```

## `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0089

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:13`
- Строки: `13--16`

```latex
\begin{equation}
 V_{\rm conn}=\zeta\|Y(\phi,\Sigma_4)\|_F^2.
 \label{eq:ps-connected-scalar-channel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0090

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:20`
- Строки: `20--22`

```latex
\begin{equation}
 H_\phi(\zeta)=H_\phi(0)+2\zeta G_Y.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0091

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:25`
- Строки: `25--29`

```latex
\begin{equation}
 1.99\ (4),
 \qquad
 9.27\ (4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0092

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 -H_\phi(0)v=2\zeta G_Yv
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0093

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:35`
- Строки: `35--39`

```latex
\begin{equation}
 1.72905791\ (4),
 \qquad
 2\ (4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0094

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 \boxed{\zeta_{\rm crit}=2.}
 \label{eq:ps-connector-critical-zeta}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0095

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:47`
- Строки: `47--50`

```latex
\begin{equation}
 \boxed{\zeta>2.}
 \label{eq:ps-connector-strict-threshold}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0096

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 Y(0,\Sigma_4)=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0097

- Источник: `s2t/gates/version4_pati_salam_twisted_connector_threshold_gate.tex:118`
- Строки: `118--123`

```latex
\begin{equation}
 \zeta_{\rm twist}>2,
 \qquad
 \rank H_{\Sigma,\rm twist}=15.
 \label{eq:ps-twisted-next-pass}
\end{equation}
```

## `s2t/gates/version4_sector_torsor_incidence_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0098

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:4`
- Строки: `4--6`

```latex
\begin{equation}
 (q,h)\in\mathbb F_2^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0099

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:9`
- Строки: `9--11`

```latex
\begin{equation}
 e=(0,0),\quad\nu=(0,1),\quad d=(1,0),\quad u=(1,1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0100

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 \nu d,\qquad\nu u,\qquad ed,\qquad eu.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0101

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 K_{2,2}=\{e,\nu\}\star\{d,u\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0102

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:39`
- Строки: `39--42`

```latex
\begin{align}
 H_{\ell}&=-\frac12\sum_q\epsilon_{\ell q}E_{\ell q},\\
 H_q&=\frac12\sum_\ell\epsilon_{\ell q}E_{\ell q}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0103

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:54`
- Строки: `54--59`

```latex
\begin{equation}
 (\epsilon_{00},\epsilon_{01},\epsilon_{10},\epsilon_{11})
 =(-1,-1,+1,+1),
 \qquad
 t=19.944681.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0104

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:61`
- Строки: `61--64`

```latex
\begin{align}
 u&=(1.47982\times10^{-5},\,0.186971,\,1),\\
 d&=(0.000567355,\,0.179519,\,1),
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0105

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:66`
- Строки: `66--68`

```latex
\begin{equation}
 (1.18,\,25.40,\,1.97,\,8.03).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0106

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:75`
- Строки: `75--82`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.96068&0.25521&0.10940\\
 0.25773&0.67639&0.68998\\
 0.10334&0.69091&0.71551
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0107

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:84`
- Строки: `84--86`

```latex
\begin{equation}
 \frac{s_{12}}{s_{12}^{\rm CKM}}=1.14.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0108

- Источник: `s2t/gates/version4_sector_torsor_incidence_gate.tex:88`
- Строки: `88--90`

```latex
\begin{equation}
 \frac{|J_q|}{J_{\rm CKM}}=58.39.
\end{equation}
```

## `s2t/gates/version4_spectral_pati_salam_bridge_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-05-0109

- Источник: `s2t/gates/version4_spectral_pati_salam_bridge_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 SU(2)_R\times SU(2)_L\times SU(4),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0110

- Источник: `s2t/gates/version4_spectral_pati_salam_bridge_gate.tex:18`
- Строки: `18--24`

```latex
\begin{equation}
 g_3=g_4,
 \qquad g_2=g_L,
 \qquad
 \frac{1}{g_Y^2}=\frac{1}{g_R^2}+\frac{2}{3g_4^2}.
 \label{eq:ps-bridge-matching}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-05-0111

- Источник: `s2t/gates/version4_spectral_pati_salam_bridge_gate.tex:32`
- Строки: `32--34`

```latex
\begin{equation}
 m_R=1.0317137\times10^{13}\,\mathrm{GeV},
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]