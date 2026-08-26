# Гейты Version 3, часть 3

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **107** блочных формул из **9** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version3_base_k_spectral_renormalization_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0001

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:11`
- Строки: `11--20`

```latex
\begin{equation}
 V_{\mathrm{1loop}}(\chi)
 =
 B\chi^4
 \left(
 \log\frac{\chi^2}{\mu^2}-c
 \right),
 \qquad
 B>0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0002

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:22`
- Строки: `22--24`

```latex
\begin{equation}
 B_0=\frac{67}{64\pi^2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0003

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:28`
- Строки: `28--35`

```latex
\begin{equation}
 V_{\mathrm{ren}}(\chi)
 =
 V_{\mathrm{1loop}}(\chi)
 +\lambda_2R_K\chi^2
 +\lambda_4\chi^4
 +\lambda_0R_K^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0004

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 \mu\longmapsto e^t\mu.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0005

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 \log\frac{\chi^2}{e^{2t}\mu^2}
 =
 \log\frac{\chi^2}{\mu^2}-2t,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0006

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:52`
- Строки: `52--54`

```latex
\begin{equation}
 \lambda_4\longmapsto\lambda_4+2Bt.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0007

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:60`
- Строки: `60--64`

```latex
\begin{equation}
 \log\frac{\chi_*^2}{\mu^2}
 =
 c-\frac12-\frac{\lambda_4}{B},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0008

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:66`
- Строки: `66--75`

```latex
\begin{equation}
 \frac{\chi_*}{\mu}
 =
 \exp\left[
 \frac12
 \left(
 c-\frac12-\frac{\lambda_4}{B}
 \right)
 \right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0009

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:88`
- Строки: `88--90`

```latex
\begin{equation}
 \mu=R^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0010

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:93`
- Строки: `93--95`

```latex
\begin{equation}
 R\longmapsto sR
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0011

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:100`
- Строки: `100--109`

```latex
\begin{equation}
 \chi_*R
 =
 \exp\left[
 \frac12
 \left(
 c-\frac12-\frac{\lambda_4}{B}
 \right)
 \right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0012

- Источник: `s2t/gates/version3_base_k_spectral_renormalization_gate.tex:122`
- Строки: `122--126`

```latex
\begin{equation}
 \lambda_2=\lambda_2(f_2,\Lambda),
 \qquad
 \lambda_4=\lambda_4(f_0).
\end{equation}
```

## `s2t/gates/version3_compact_phase_embedding_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0013

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:7`
- Строки: `7--11`

```latex
\begin{equation}
 U=e^{i\vartheta},
 \qquad
 \vartheta\sim\vartheta+2\pi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0014

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 S_{\mathrm{kin}}[\vartheta]
 =\frac{f^2}{2}\int_Y d\vartheta\wedge\star d\vartheta
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0015

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:40`
- Строки: `40--42`

```latex
\begin{equation}
 \Hess_{\vartheta_0}S_{\mathrm{kin}}[1,1]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0016

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:48`
- Строки: `48--51`

```latex
\begin{equation}
 S_{\mathrm{pot}}[\vartheta]
 =\mu^{\dim Y}\int_Y(1-\cos\vartheta)\,d\Vol_Y,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0017

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:53`
- Строки: `53--56`

```latex
\begin{equation}
 \Hess_0S_{\mathrm{pot}}[1,1]
 =\mu^{\dim Y}\Vol(Y).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0018

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:65`
- Строки: `65--67`

```latex
\begin{equation}
 \Vol(K)=2\pi^3,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0019

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:70`
- Строки: `70--73`

```latex
\begin{equation}
 \operatorname{Map}(\mathbb{RP}^3,U(1))
 \oplus\operatorname{Map}(S^1,U(1)),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0020

- Источник: `s2t/gates/version3_compact_phase_embedding_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 \|1_{\mathbb{RP}^3}\|^2+\|1_{S^1}\|^2=\pi^2+2\pi,
\end{equation}
```

## `s2t/gates/version3_conditional_expectation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0021

- Источник: `s2t/gates/version3_conditional_expectation_gate.tex:4`
- Строки: `4--8`

```latex
\begin{equation}
 \tau_X(f)=\pi^{-2}\int_X f,
 \qquad
 \tau_C(g)=(2\pi)^{-1}\int_C g
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0022

- Источник: `s2t/gates/version3_conditional_expectation_gate.tex:11`
- Строки: `11--15`

```latex
\begin{equation}
 \frac1{2\pi}\int_K|f(x)|^2=\int_X|f|^2,
 \qquad
 \frac1{\pi^2}\int_K|g(s)|^2=\int_C|g|^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0023

- Источник: `s2t/gates/version3_conditional_expectation_gate.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 \|(1_X,1_C)\|^2=\pi^2+2\pi
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0024

- Источник: `s2t/gates/version3_conditional_expectation_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 L^2(X)\oplus L^2(C)\oplus\mathbb C^{23}
 \oplus\Omega^1_{\mathrm{int}}(C)
\end{equation}
```

## `s2t/gates/version3_dimensional_product_consistency_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0025

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 \mathcal A=C^\infty(K)\otimes A_F,
 \qquad
 \mathcal H=L^2(K,S)\otimes H_8,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0026

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 B=\frac1{64\pi^2\chi^4}\Str M^4
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0027

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:39`
- Строки: `39--45`

```latex
\begin{align}
 \mathcal A_{\mathrm{tot}}
 &=C^\infty(M_4)\otimes C^\infty(K)\otimes A_F,
 \\
 \mathcal H_{\mathrm{tot}}
 &=L^2(M_4,S_4)\otimes\mathcal H_K\otimes H_8.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0028

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:47`
- Строки: `47--51`

```latex
\begin{equation}
 a_n(\mathcal D_{\mathrm{tot}}^2)
 =\sum_{p+q=n}
 a_p(D_{M_4}^2)\,a_q(D_K^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0029

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 \mathcal H_K=L^2(K,S_K),
 \qquad
 D_K=\text{геометрический Dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0030

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:65`
- Строки: `65--67`

```latex
\begin{equation}
 R_K=6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0031

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 D_K^2=\nabla^*\nabla+\frac{R_K}{4}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0032

- Источник: `s2t/gates/version3_dimensional_product_consistency_gate.tex:86`
- Строки: `86--92`

```latex
\begin{equation}
 \kappa=2,
 \qquad
 g^2=\frac38,
 \qquad
 B_0^{\mathrm{fin+gauge}}=\frac{67}{64\pi^2}
\end{equation}
```

## `s2t/gates/version3_external_redteam_convention_audit.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0033

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:10`
- Строки: `10--13`

```latex
\begin{equation}
 \Tr_{\mathrm{orb}}(d\Phi\,d\Phi)
 =G_{ab}\,dq^a dq^b.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0034

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:15`
- Строки: `15--21`

```latex
\begin{equation}
 \mathcal L
 =
 \frac{\kappa}{2}
 \Tr_{\mathrm{orb}}(\partial_\mu\Phi\partial^\mu\Phi)
 -V(\Phi)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0035

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:23`
- Строки: `23--29`

```latex
\begin{equation}
 H_{ab}
 =
 \left.
 \frac{\partial^2V}{\partial q^a\partial q^b}
 \right|_{q_*}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0036

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:31`
- Строки: `31--41`

```latex
\begin{equation}
 \mathcal L^{(2)}
 =
 \frac12
 \left[
 \kappa G_{ab}\,
 \partial_\mu\eta^a\partial^\mu\eta^b
 -
 H_{ab}\eta^a\eta^b
 \right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0037

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:43`
- Строки: `43--45`

```latex
\begin{equation}
 K_{\mathrm{quad}}=\kappa G,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0038

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 M^2=(\kappa G)^{-1}H.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0039

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 K_{\mathrm{quad}}=2G_*,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0040

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:58`
- Строки: `58--61`

```latex
\begin{equation}
 (2G_*)^{-1}H_*
 =\operatorname{diag}(4,4,4).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0041

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:73`
- Строки: `73--77`

```latex
\begin{equation}
 \frac{m_s^2}{\chi^2}=4,
 \qquad
 N_{\mathrm{fin}}=3\cdot4^2-8=40,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0042

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 N_{\mathrm{fin+gauge}}=40+27=67.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0043

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:88`
- Строки: `88--92`

```latex
\begin{equation}
 D_F^2=\mathbf1,
 \qquad
 BB^\dagger=\mathbf1_2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0044

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:94`
- Строки: `94--96`

```latex
\begin{equation}
 2r^2=2s^2=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0045

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:103`
- Строки: `103--105`

```latex
\begin{equation}
 4+1-2=3
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0046

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:115`
- Строки: `115--120`

```latex
\begin{equation}
 1_{\mathrm{long}}
 +1_{\mathrm{Goldstone}}
 -2_{\mathrm{ghost}}
 =0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0047

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:122`
- Строки: `122--124`

```latex
\begin{equation}
 \Delta N_{\mathrm{gauge+ghost}}=3c_A^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0048

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:136`
- Строки: `136--138`

```latex
\begin{equation}
 E=-\Phi^2+\text{derivative и gauge terms}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0049

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:140`
- Строки: `140--152`

```latex
\begin{align}
 a_0&\sim\Tr\mathbf1,
 \\
 a_2&\sim\Tr\left(-\Phi^2-\frac1{12}R\mathbf1\right),
 \\
 a_4&\sim\Tr\left(
 \frac12\Phi^4
 +(\nabla\Phi)^2
 +F^2
 +\frac1{12}R\Phi^2
 +\text{pure curvature}
 \right).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0050

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:168`
- Строки: `168--173`

```latex
\begin{equation}
 S_{\mathrm{spec}}
 \supset
 f_2\Lambda^2 a_2
 +f_0a_4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0051

- Источник: `s2t/gates/version3_external_redteam_convention_audit.tex:176`
- Строки: `176--181`

```latex
\begin{equation}
 \chi^2
 \sim
 \frac{f_2\Lambda^2}{f_0}
 +\text{curvature correction}.
\end{equation}
```

## `s2t/gates/version3_finite_dirac_parent_potential_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0052

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:6`
- Строки: `6--9`

```latex
\begin{equation}
 V_{\mathrm{flat}}(D_F)
 =\Tr_{\mathrm{orb}}\left(D_F^2-\mathbf1\right)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0053

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:16`
- Строки: `16--22`

```latex
\begin{equation}
 r=|x|,
 \qquad
 s=|z|,
 \qquad
 \phi=\arg(xz),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0054

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 u=r^2+s^2,
 \qquad
 v=r^2s^2\sin^2\phi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0055

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 V_{\mathrm{flat}}
 =8u^2-16v-8u+4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0056

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:36`
- Строки: `36--38`

```latex
\begin{equation}
 D_F^2=\mathbf1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0057

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:41`
- Строки: `41--43`

```latex
\begin{equation}
 BB^\dagger=\mathbf1_2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0058

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:45`
- Строки: `45--51`

```latex
\begin{equation}
 2r^2=1,
 \qquad
 2s^2=1,
 \qquad
 2\operatorname{Re}(xz)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0059

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:53`
- Строки: `53--58`

```latex
\begin{equation}
 \boxed{
 r=s=\frac1{\sqrt2},
 \qquad
 \phi=\pm\frac{\pi}{2}\pmod{\pi}.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0060

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 \left(\frac1{\sqrt2},\frac1{\sqrt2},\frac{\pi}{2}\right)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0061

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:73`
- Строки: `73--81`

```latex
\begin{equation}
 \Hess V_{\mathrm{flat}}
 =
 \begin{pmatrix}
 32&0&0\\
 0&32&0\\
 0&0&8
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0062

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:88`
- Строки: `88--93`

```latex
\begin{equation}
 V_{a,b}
 =a\,\Tr_{\mathrm{orb}}D_F^4
 -b\,\Tr_{\mathrm{orb}}D_F^2,
 \qquad a,b>0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0063

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:95`
- Строки: `95--97`

```latex
\begin{equation}
 u_{\min}=\frac{b}{2a}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0064

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:107`
- Строки: `107--110`

```latex
\begin{equation}
 V_M(D_F)
 =\Tr_{\mathrm{orb}}\left(D_F^2-M^2\mathbf1\right)^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0065

- Источник: `s2t/gates/version3_finite_dirac_parent_potential_gate.tex:112`
- Строки: `112--114`

```latex
\begin{equation}
 |x|=|z|=\frac{M}{\sqrt2}.
\end{equation}
```

## `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0066

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:7`
- Строки: `7--18`

```latex
\begin{align}
 \mathcal A
 &=C^\infty(K)\otimes A_F,
 &
 A_F&=\mathbb C\oplus\mathbb C,
 \\
 \mathcal H
 &=L^2(K,S)\otimes H_8,
 &
 \mathcal D_\chi
 &=D_K\otimes\mathbf1+\gamma_K\otimes\chi D_F^*,
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0067

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 u=(e^{i\alpha_X},e^{i\alpha_C})\in U(A_F)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0068

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:29`
- Строки: `29--31`

```latex
\begin{equation}
 (H_{XX},H_{XC},H_{CX},H_{CC})
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0069

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:34`
- Строки: `34--36`

```latex
\begin{equation}
 q=(0,+1,-1,0).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0070

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 G_F
 =\frac{U(1)_X\times U(1)_C}{U(1)_{\mathrm{diag}}}
 \simeq U(1)_{\mathrm{rel}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0071

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 x\longmapsto e^{-i\theta}x,
 \qquad
 z\longmapsto e^{+i\theta}z,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0072

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:64`
- Строки: `64--68`

```latex
\begin{equation}
 D_\mu x=(\partial_\mu-iA_\mu)x,
 \qquad
 D_\mu z=(\partial_\mu+iA_\mu)z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0073

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:70`
- Строки: `70--72`

```latex
\begin{equation}
 |x|=|z|=\frac{\chi}{\sqrt2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0074

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 \Tr_{\mathrm{orb}}(D_\mu\Phi D^\mu\Phi)
 \supset4\chi^2 A_\mu A^\mu.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0075

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 \frac1{4g^2}F_{\mu\nu}F^{\mu\nu},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0076

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:83`
- Строки: `83--85`

```latex
\begin{equation}
 \frac{m_A^2}{\chi^2}=c_A=8g^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0077

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:92`
- Строки: `92--94`

```latex
\begin{equation}
 (A_\mu,x,z;c,\bar c,b).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0078

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:96`
- Строки: `96--105`

```latex
\begin{align}
 sA_\mu&=\partial_\mu c,
 & sc&=0,
 \\
 sx&=-icx,
 & sz&=+icz,
 \\
 s\bar c&=b,
 & sb&=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0079

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:107`
- Строки: `107--109`

```latex
\begin{equation}
 \Delta_0+\xi m_A^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0080

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:111`
- Строки: `111--113`

```latex
\begin{equation}
 \Delta_1+m_A^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0081

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:117`
- Строки: `117--119`

```latex
\begin{equation}
 4+1-2=3
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0082

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:128`
- Строки: `128--131`

```latex
\begin{equation}
 \Delta N_{\mathrm{gauge+ghost}}
 =3(8g^2)^2=192g^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0083

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:167`
- Строки: `167--172`

```latex
\begin{equation}
 B_{\mathrm{full}}
 =\frac{40+192g^4+c_\sigma^2+\Delta N_{\mathrm{KK}}
 (g,\mathfrak s,\rho_{\mathrm{flat}})}
 {64\pi^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0084

- Источник: `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex:185`
- Строки: `185--187`

```latex
\begin{equation}
 \Tr_{\mathrm{orb}}Q^2=2.
\end{equation}
```

## `s2t/gates/version3_portal_menu_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0085

- Источник: `s2t/gates/version3_portal_menu_gate.tex:10`
- Строки: `10--12`

```latex
\begin{equation}
 \Sigma_h=|x|^2+|z|^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0086

- Источник: `s2t/gates/version3_portal_menu_gate.tex:14`
- Строки: `14--18`

```latex
\begin{equation}
 \mathcal O_S
 =
 \Sigma_h\,H^\dagger H
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0087

- Источник: `s2t/gates/version3_portal_menu_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 \Delta\mathcal L_S
 =
 -\lambda_{hH}\mathcal O_S.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0088

- Источник: `s2t/gates/version3_portal_menu_gate.tex:40`
- Строки: `40--45`

```latex
\begin{equation}
 \Delta\mathcal L_{\mathrm{mix}}
 =
 -\frac{\epsilon}{2}
 f_{\mu\nu}^{h}B^{\mu\nu}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0089

- Источник: `s2t/gates/version3_portal_menu_gate.tex:48`
- Строки: `48--50`

```latex
\begin{equation}
 \Tr(Q_hY).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0090

- Источник: `s2t/gates/version3_portal_menu_gate.tex:53`
- Строки: `53--55`

```latex
\begin{equation}
 \Tr(Q_hY)=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0091

- Источник: `s2t/gates/version3_portal_menu_gate.tex:59`
- Строки: `59--63`

```latex
\begin{equation}
 A_h\longmapsto-A_h,
 \qquad
 x\longleftrightarrow z
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0092

- Источник: `s2t/gates/version3_portal_menu_gate.tex:78`
- Строки: `78--82`

```latex
\begin{equation}
 \mathcal O_{N,ai}
 =
 \overline L_a\widetilde H\,N_i,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0093

- Источник: `s2t/gates/version3_portal_menu_gate.tex:85`
- Строки: `85--87`

```latex
\begin{equation}
 y_{ai}^{N}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0094

- Источник: `s2t/gates/version3_portal_menu_gate.tex:105`
- Строки: `105--113`

```latex
\begin{align}
 \mathcal H_{\mathrm{tot}}
 &=
 \mathcal H_h\oplus\mathcal H_{\mathrm{obs}},
 \\
 \mathcal D_{\mathrm{tot}}
 &=
 \mathcal D_h\oplus\mathcal D_{\mathrm{obs}}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0095

- Источник: `s2t/gates/version3_portal_menu_gate.tex:115`
- Строки: `115--121`

```latex
\begin{equation}
 f(\mathcal D_{\mathrm{tot}}^2)
 =
 f(\mathcal D_h^2)
 \oplus
 f(\mathcal D_{\mathrm{obs}}^2)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0096

- Источник: `s2t/gates/version3_portal_menu_gate.tex:123`
- Строки: `123--129`

```latex
\begin{equation}
 \Tr f(\mathcal D_{\mathrm{tot}}^2)
 =
 \Tr f(\mathcal D_h^2)
 +
 \Tr f(\mathcal D_{\mathrm{obs}}^2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0097

- Источник: `s2t/gates/version3_portal_menu_gate.tex:131`
- Строки: `131--137`

```latex
\begin{equation}
 \lambda_{hH}=0,
 \qquad
 \epsilon=0,
 \qquad
 y^N=0
\end{equation}
```

## `s2t/gates/version3_representation_readout_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-03-0098

- Источник: `s2t/gates/version3_representation_readout_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 q(x)=-1,
 \qquad
 q(z)=+1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0099

- Источник: `s2t/gates/version3_representation_readout_gate.tex:33`
- Строки: `33--39`

```latex
\begin{equation}
 B=
 \begin{pmatrix}
 x&\overline x\\
 \overline z&z
 \end{pmatrix}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0100

- Источник: `s2t/gates/version3_representation_readout_gate.tex:43`
- Строки: `43--55`

```latex
\begin{align}
 H_{XC}(+1)\to H_{XX}(0)
 &:\quad q=-1,
 \\
 H_{CX}(-1)\to H_{XX}(0)
 &:\quad q=+1,
 \\
 H_{XC}(+1)\to H_{CC}(0)
 &:\quad q=-1,
 \\
 H_{CX}(-1)\to H_{CC}(0)
 &:\quad q=+1.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0101

- Источник: `s2t/gates/version3_representation_readout_gate.tex:69`
- Строки: `69--75`

```latex
\begin{align}
 \sum q&=0,
 \\
 \sum q^3&=0,
 \\
 \sum q^2&=2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0102

- Источник: `s2t/gates/version3_representation_readout_gate.tex:89`
- Строки: `89--91`

```latex
\begin{equation}
 |x|=|z|=\frac{\chi}{\sqrt2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0103

- Источник: `s2t/gates/version3_representation_readout_gate.tex:93`
- Строки: `93--95`

```latex
\begin{equation}
 m_A^2=3\chi^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0104

- Источник: `s2t/gates/version3_representation_readout_gate.tex:104`
- Строки: `104--106`

```latex
\begin{equation}
 \mathfrak g_F=\mathfrak u(1)_{\mathrm{rel}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0105

- Источник: `s2t/gates/version3_representation_readout_gate.tex:108`
- Строки: `108--114`

```latex
\begin{equation}
 \mathfrak{su}(3)_{\mathrm{color}},
 \qquad
 \mathfrak{su}(2)_{\mathrm{weak}},
 \qquad
 \mathfrak u(1)_Y
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0106

- Источник: `s2t/gates/version3_representation_readout_gate.tex:142`
- Строки: `142--144`

```latex
\begin{equation}
 \ker D_F=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-03-0107

- Источник: `s2t/gates/version3_representation_readout_gate.tex:157`
- Строки: `157--161`

```latex
\begin{equation}
 \boxed{
 \text{anomaly-free Higgsed hidden }U(1)
 \text{ с двумя mirror chiral pairs}.}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]