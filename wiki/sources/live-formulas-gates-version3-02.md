# Гейты Version 3, часть 2

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **108** блочных формул из **9** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version3_compact_a2_a4_moment_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0001

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:11`
- Строки: `11--16`

```latex
\begin{equation}
 \mathcal D_A
 =
 i\gamma^\mu(\nabla_\mu+A_\mu)
 +\gamma^5\Phi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0002

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 \mathcal D_A^2
 =-(\nabla^2+E)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0003

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:23`
- Строки: `23--30`

```latex
\begin{equation}
 E
 =
 -\frac14R\mathbf1
 -\Phi^2
 -i\gamma^\mu\gamma^5D_\mu\Phi
 -\frac12\gamma^{\mu\nu}F_{\mu\nu}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0004

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:32`
- Строки: `32--49`

```latex
\begin{align}
 a_2
 &=
 \frac1{(4\pi)^2}
 \int_K
 \Tr\left(E+\frac16R\right),
 \\
 a_4
 &=
 \frac1{(4\pi)^2}
 \int_K
 \Tr\left(
 \frac12E^2
 +\frac16RE
 +\frac1{12}\Omega^2
 +\text{pure curvature}
 \right),
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0005

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:55`
- Строки: `55--60`

```latex
\begin{equation}
 E+\frac16R
 =
 -\Phi^2-\frac1{12}R
 +\text{Clifford-odd terms}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0006

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:62`
- Строки: `62--70`

```latex
\begin{equation}
 a_2\big|_{\Phi}
 =
 \frac1{(4\pi)^2}
 \int_K
 \left[
 -4\,\Tr_{\mathrm{orb}}\Phi^2
 \right].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0007

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:77`
- Строки: `77--83`

```latex
\begin{equation}
 a_4\big|_{\Phi^4}
 =
 \frac1{(4\pi)^2}
 \int_K
 2\,\Tr_{\mathrm{orb}}\Phi^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0008

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:85`
- Строки: `85--91`

```latex
\begin{equation}
 a_4\big|_{\mathrm{kin}}
 =
 \frac1{(4\pi)^2}
 \int_K
 2\,\Tr_{\mathrm{orb}}(D_\mu\Phi D^\mu\Phi).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0009

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:98`
- Строки: `98--101`

```latex
\begin{equation}
 -\frac16R\Phi^2+\frac14R\Phi^2
 =\frac1{12}R\Phi^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0010

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:103`
- Строки: `103--109`

```latex
\begin{equation}
 a_4\big|_{R\Phi^2}
 =
 \frac1{(4\pi)^2}
 \int_K
 \frac13R\,\Tr_{\mathrm{orb}}\Phi^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0011

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:113`
- Строки: `113--122`

```latex
\begin{align}
 a_2\big|_\Phi
 &\propto-4\Tr_{\mathrm{orb}}\Phi^2,
 \\
 a_4\big|_\Phi
 &\propto
 2\Tr_{\mathrm{orb}}(D\Phi)^2
 +2\Tr_{\mathrm{orb}}\Phi^4
 +\frac13R\Tr_{\mathrm{orb}}\Phi^2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0012

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:130`
- Строки: `130--134`

```latex
\begin{equation}
 S_{\mathrm{spec}}
 \supset
 f_2\Lambda^2a_2+f_0a_4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0013

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:136`
- Строки: `136--148`

```latex
\begin{align}
 \mathcal L_{\Phi}
 &=
 \Tr_{\mathrm{orb}}(D_\mu\Phi D^\mu\Phi)
 +\Tr_{\mathrm{orb}}\Phi^4
 \\
 &\quad
 +\left(
 -2\frac{f_2}{f_0}\Lambda^2
 +\frac16R
 \right)
 \Tr_{\mathrm{orb}}\Phi^2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0014

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:150`
- Строки: `150--153`

```latex
\begin{equation}
 \Tr_{\mathrm{orb}}
 \left(\Phi^2-\chi^2\mathbf1\right)^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0015

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:155`
- Строки: `155--161`

```latex
\begin{equation}
 \boxed{
 \chi^2
 =
 \frac{f_2}{f_0}\Lambda^2
 -\frac1{12}R.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0016

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:165`
- Строки: `165--167`

```latex
\begin{equation}
 R_K=\frac6{R^2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0017

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:169`
- Строки: `169--175`

```latex
\begin{equation}
 \boxed{
 (\chi R)^2
 =
 \frac{f_2}{f_0}(\Lambda R)^2
 -\frac12.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0018

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:177`
- Строки: `177--179`

```latex
\begin{equation}
 \frac{f_2}{f_0}(\Lambda R)^2>\frac12.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0019

- Источник: `s2t/gates/version3_compact_a2_a4_moment_gate.tex:201`
- Строки: `201--205`

```latex
\begin{equation}
 \zeta_{\mathrm{mom}}
 :=
 \frac{f_2}{f_0}(\Lambda R)^2.
\end{equation}
```

## `s2t/gates/version3_cross_tome_closure_audit.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0020

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:9`
- Строки: `9--11`

```latex
\begin{equation}
 L=A\dot q^2-\frac12Hq^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0021

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 2A\ddot q+Hq=0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0022

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 m^2=\frac{H}{2A}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0023

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 A=\frac{\kappa}{2}G,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0024

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 m^2=(\kappa G)^{-1}H.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0025

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:34`
- Строки: `34--40`

```latex
\begin{equation}
 m_s^2=4\chi^2,
 \qquad
 N_{\mathrm{fin}}=40,
 \qquad
 N_{\mathrm{fin+gauge}}=67.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0026

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:48`
- Строки: `48--54`

```latex
\begin{equation}
 S_{\mathrm{vac}}
 =
 S_{\mathrm{geo}}
 -\frac1{24S_{\mathrm{geo}}}
 -\frac1{\pi^4S_{\mathrm{geo}}^2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0027

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:62`
- Строки: `62--64`

```latex
\begin{equation}
 \Gamma_{\mathrm{hidden}}[\Phi,A,\chi].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0028

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:102`
- Строки: `102--104`

```latex
\begin{equation}
 23+\pi^{-1}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0029

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:110`
- Строки: `110--112`

```latex
\begin{equation}
 184=8\cdot23
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0030

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:126`
- Строки: `126--128`

```latex
\begin{equation}
 \Tr_{\mathrm{orb}}=\frac12\Tr_{H_8}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0031

- Источник: `s2t/gates/version3_cross_tome_closure_audit.tex:145`
- Строки: `145--147`

```latex
\begin{equation}
 \text{единый observed-world parent functional не построен}.
\end{equation}
```

## `s2t/gates/version3_dilaton_radion_transmutation_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0032

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 V_{\mathrm{cl}}(\chi)=\lambda_\chi\chi^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0033

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:22`
- Строки: `22--25`

```latex
\begin{equation}
 V_{\mathrm{ratio}}
 =\lambda\left(\rho^2-\alpha\chi^2\right)^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0034

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 \frac{\rho}{\chi}=\sqrt\alpha,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0035

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:31`
- Строки: `31--33`

```latex
\begin{equation}
 (\chi,\rho)\longmapsto t(\chi,\rho).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0036

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:35`
- Строки: `35--38`

```latex
\begin{equation}
 8\alpha\lambda(\alpha+1),
 \qquad 0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0037

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:51`
- Строки: `51--56`

```latex
\begin{equation}
 V_{\mathrm{dual}}(\varphi)
 =A\left(e^{2\varphi}+e^{-2\varphi}-2\right),
 \qquad
 R=R_0e^\varphi,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0038

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:59`
- Строки: `59--63`

```latex
\begin{equation}
 \varphi\longmapsto-\varphi,
 \qquad
 R\longmapsto\frac{R_0^2}{R}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0039

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:77`
- Строки: `77--84`

```latex
\begin{equation}
 V_{\mathrm{CW}}(\chi)
 =B\chi^4
 \left(
 \log\frac{\chi^2}{\mu^2}-\frac12
 \right),
 \qquad B>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0040

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:86`
- Строки: `86--90`

```latex
\begin{equation}
 V_{\mathrm{CW}}'(\mu)=0,
 \qquad
 V_{\mathrm{CW}}''(\mu)=8B\mu^2>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0041

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:92`
- Строки: `92--100`

```latex
\begin{equation}
 V_{\mathrm{joint}}(\chi,D_F)
 =
 V_{\mathrm{CW}}(\chi)
 +\chi^4\Tr_{\mathrm{orb}}
 \left(
 \frac{D_F^2}{\chi^2}-\mathbf1
 \right)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0042

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:102`
- Строки: `102--108`

```latex
\begin{equation}
 \chi=\mu,
 \qquad
 D_F^2=\mu^2\mathbf1,
 \qquad
 |x|=|z|=\frac{\mu}{\sqrt2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0043

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:110`
- Строки: `110--112`

```latex
\begin{equation}
 R_*=\mu^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0044

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:125`
- Строки: `125--133`

```latex
\begin{equation}
 \Lambda_{\mathrm{DT}}
 =
 \mu
 \exp\left(
 -\int^{g(\mu)}
 \frac{dg}{\beta(g)}
 \right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0045

- Источник: `s2t/gates/version3_dilaton_radion_transmutation_gate.tex:158`
- Строки: `158--161`

```latex
\begin{equation}
 B\propto
 \Str M^4(\chi)/\chi^4.
\end{equation}
```

## `s2t/gates/version3_dual_architecture_verdict_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0046

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:11`
- Строки: `11--19`

```latex
\begin{equation}
 \Gamma_K^{(1)}(\chi)
 =
 \frac12\sum_b n_b\log\det_\zeta
 \bigl(P_b+c_b\chi^2\bigr)
 -
 \frac12\sum_f n_f\log\det_\zeta
 \bigl(P_f+c_f\chi^2\bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0047

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:26`
- Строки: `26--29`

```latex
\begin{equation}
 \delta V_{\mathrm{loc}}(\chi)
 =\lambda_2R_K\chi^2+\lambda_4\chi^4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0048

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:32`
- Строки: `32--36`

```latex
\begin{equation}
 \lambda_2
 =-\frac{F'(\chi_*)+4\lambda_4\chi_*^3}
 {2R_K\chi_*},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0049

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:38`
- Строки: `38--41`

```latex
\begin{equation}
 \frac{d}{d\chi}
 \left(F+\delta V_{\mathrm{loc}}\right)_{\chi=\chi_*}=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0050

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:63`
- Строки: `63--66`

```latex
\begin{equation}
 D_{K,\rho}^2
 =\nabla_\rho^*\nabla_\rho+\frac{R_K}{4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0051

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 R_K=R_{\mathbb{RP}^3}+R_{S^1}=6+0=6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0052

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:72`
- Строки: `72--75`

```latex
\begin{equation}
 \|D_{K,\rho}\psi\|^2
 =\|\nabla_\rho\psi\|^2+\frac32\|\psi\|^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0053

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:77`
- Строки: `77--79`

```latex
\begin{equation}
 \ker D_{K,\rho}=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0054

- Источник: `s2t/gates/version3_dual_architecture_verdict_gate.tex:82`
- Строки: `82--85`

```latex
\begin{equation}
 (\epsilon_{\mathbb{RP}^3},\epsilon_{S^1})
 \in\mathbb Z_2\times\mathbb Z_2
\end{equation}
```

## `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0055

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:4`
- Строки: `4--6`

```latex
\begin{equation}
 B=\frac1{64\pi^2\chi^4}\Str M^4(\chi)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0056

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:13`
- Строки: `13--17`

```latex
\begin{equation}
 x=re^{i\phi/2},
 \qquad
 z=se^{i\phi/2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0057

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:19`
- Строки: `19--22`

```latex
\begin{equation}
 ds^2_{\mathrm{kin}}
 =\Tr_{\mathrm{orb}}(dD_F\,dD_F).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0058

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:24`
- Строки: `24--32`

```latex
\begin{equation}
 G(r,s,\phi)
 =
 \begin{pmatrix}
 4&0&0\\
 0&4&0\\
 0&0&r^2+s^2
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0059

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:34`
- Строки: `34--38`

```latex
\begin{equation}
 r=s=\frac1{\sqrt2},
 \qquad
 \phi=\frac{\pi}{2}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0060

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:40`
- Строки: `40--42`

```latex
\begin{equation}
 G_*=\operatorname{diag}(4,4,1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0061

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 H_*=\operatorname{diag}(32,32,8).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0062

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:51`
- Строки: `51--53`

```latex
\begin{equation}
 H_*v=m^2G_*v.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0063

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:55`
- Строки: `55--57`

```latex
\begin{equation}
 m_{s,1}^2=m_{s,2}^2=m_{s,3}^2=8\chi^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0064

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 B B^\dagger=\chi^2\mathbf1_2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0065

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:73`
- Строки: `73--75`

```latex
\begin{equation}
 m_{f,1}=m_{f,2}=\chi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0066

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:82`
- Строки: `82--87`

```latex
\begin{align}
 \frac{\Str M^4}{\chi^4}
 &=3\cdot8^2-2\cdot4\cdot1^4\\
 &=192-8\\
 &=184=8\cdot23.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0067

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:89`
- Строки: `89--94`

```latex
\begin{equation}
 \boxed{
 B_0^{\mathrm{fin}}
 =\frac{184}{64\pi^2}
 =\frac{23}{8\pi^2}>0.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0068

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:110`
- Строки: `110--114`

```latex
\begin{equation}
 \mathcal L_{\mathrm{kin}}
 =\frac{\kappa}{2}
 \Tr_{\mathrm{orb}}(\partial_\mu D_F\partial^\mu D_F).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0069

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:116`
- Строки: `116--118`

```latex
\begin{equation}
 m_s^2=\frac8\kappa\chi^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0070

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:120`
- Строки: `120--123`

```latex
\begin{equation}
 \frac{\Str M^4}{\chi^4}
 =\frac{192}{\kappa^2}-8.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0071

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:125`
- Строки: `125--127`

```latex
\begin{equation}
 \kappa<\sqrt{24}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0072

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:154`
- Строки: `154--157`

```latex
\begin{equation}
 \Delta B_{\mathrm{KK+gauge}}
 =B_{\mathrm{full}}-B_0^{\mathrm{fin}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0073

- Источник: `s2t/gates/version3_finite_zero_mode_supertrace_gate.tex:159`
- Строки: `159--161`

```latex
\begin{equation}
 B_{\mathrm{full}}>0
\end{equation}
```

## `s2t/gates/version3_one_scale_blind_scorecard_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0074

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:5`
- Строки: `5--8`

```latex
\begin{equation}
 m_{\mathrm{ref}}
 :=m_f=\chi.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0075

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:15`
- Строки: `15--35`

```latex
\begin{align}
 \frac{m_{f,1}}{m_{\mathrm{ref}}}
 &=
 \frac{m_{f,2}}{m_{\mathrm{ref}}}=1,
 \\
 \frac{m_{s,a}^2}{m_{\mathrm{ref}}^2}
 &=4,
 \qquad a=1,2,3,
 \\
 \frac{m_A^2}{m_{\mathrm{ref}}^2}
 &=3,
 \\
 g^2(\mu_{\mathrm{spec}})
 &=\frac38,
 \\
 b_{U(1)}
 &=2,
 \\
 |\sin\phi_{\mathrm{vac}}|
 &=1.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0076

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:50`
- Строки: `50--54`

```latex
\begin{equation}
 \pi^2+2\pi+\frac23,
 \qquad
 23+\pi^{-1}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0077

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:67`
- Строки: `67--75`

```latex
\begin{equation}
 \begin{aligned}
 \mathcal R_{\mathrm{phys}}:\quad
 &\{\text{finite eigenmodes, collective coordinates}\}
 \\
 &\longrightarrow
 \{\text{наблюдаемые particle states и couplings}\}.
 \end{aligned}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0078

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:99`
- Строки: `99--101`

```latex
\begin{equation}
 \frac{m_{\ell_2}}{m_{\ell_1}}=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0079

- Источник: `s2t/gates/version3_one_scale_blind_scorecard_gate.tex:115`
- Строки: `115--117`

```latex
\begin{equation}
 N_\nu=23+\pi^{-1}
\end{equation}
```

## `s2t/gates/version3_real_bimodule_square_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0080

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:5`
- Строки: `5--8`

```latex
\begin{equation}
 H_{ij},
 \qquad i,j\in\{X,C\},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0081

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 (a_i-a_k)(b_j-b_l)D_{ij,kl}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0082

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 H_{XX}\longleftrightarrow H_{XC}
 \longleftrightarrow H_{CC}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0083

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:26`
- Строки: `26--28`

```latex
\begin{equation}
 J:H_{ij}\longmapsto H_{ji}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0084

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 H_{XX}\leftrightarrow H_{XC}\leftrightarrow H_{CC}
 \leftrightarrow H_{CX}\leftrightarrow H_{XX}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0085

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:36`
- Строки: `36--40`

```latex
\begin{equation}
 \gamma=+1\quad\text{на }H_{XX}\oplus H_{CC},
 \qquad
 \gamma=-1\quad\text{на }H_{XC}\oplus H_{CX}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0086

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:55`
- Строки: `55--67`

```latex
\begin{equation}
 D_F=
 \begin{pmatrix}
 0&B\\
 B^\dagger&0
 \end{pmatrix},
 \qquad
 B=
 \begin{pmatrix}
 x&\overline x\\
 \overline z&z
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0087

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:70`
- Строки: `70--73`

```latex
\begin{equation}
 \det B=xz-\overline{xz}
 =2i\,\operatorname{Im}(xz)\ne0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0088

- Источник: `s2t/gates/version3_real_bimodule_square_gate.tex:81`
- Строки: `81--83`

```latex
\begin{equation}
 J\gamma=\gamma J.
\end{equation}
```

## `s2t/gates/version3_role_graded_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0089

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:13`
- Строки: `13--20`

```latex
\begin{align}
 \Xi_\tau
 &=1_{\mathbb{RP}^3}\oplus1_{S^1}\oplus P_{\perp n},\\
 \Xi_\nu
 &=P_H\otimes\widehat 1_{S^1}
   \oplus P_{\ker}\otimes e_1,
 \qquad \oint_\gamma e_1=1.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0090

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:26`
- Строки: `26--31`

```latex
\begin{align}
 \|\Xi_\tau\|^2
 &=w_0\left(\pi^2+2\pi+\frac23\right),\label{eq:V3TauHessian}\\
 \|\Xi_\nu\|^2
 &=23w_0+\frac{w_1}{\pi}.\label{eq:V3NuHessian}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0091

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:33`
- Строки: `33--35`

```latex
\begin{equation}
 w_0=w_1=1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0092

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:44`
- Строки: `44--48`

```latex
\begin{equation}
 \|\Xi_\tau\|^2=\pi^2+2\pi+\frac23,
 \qquad
 \|\Xi_\nu\|^2=23+\pi^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0093

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:58`
- Строки: `58--60`

```latex
\begin{equation}
 \phi_\tau\longmapsto a\phi_\tau.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0094

- Источник: `s2t/gates/version3_role_graded_hessian_gate.tex:69`
- Строки: `69--72`

```latex
\begin{equation}
 \|\Xi_\tau(a_\tau)\|^2
 =a_\tau^2w_0\left(\pi^2+2\pi+\frac23\right).
\end{equation}
```

## `s2t/gates/version3_spectral_function_moment_menu_gate.tex`

### LIVE-FORMULAS-GATES-VERSION3-02-0095

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:4`
- Строки: `4--10`

```latex
\begin{equation}
 \zeta_{\mathrm{mom}}
 =
 \frac{f_2}{f_0}(\Lambda R)^2,
 \qquad
 (\chi R)^2=\zeta_{\mathrm{mom}}-\frac12.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0096

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:17`
- Строки: `17--19`

```latex
\begin{equation}
 \Tr f(\mathcal D^2/\Lambda^2),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0097

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:21`
- Строки: `21--25`

```latex
\begin{equation}
 f_0=f(0),
 \qquad
 f_2=\int_0^\infty f(u)\,du.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0098

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 f_0=1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0099

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:36`
- Строки: `36--48`

```latex
\begin{align}
 f_{\mathrm{sharp}}(u)
 &=\mathbf1_{[0,1]}(u),
 \\
 f_{\mathrm{heat}}(u)
 &=e^{-u},
 \\
 f_{\mathrm{Gauss}}(u)
 &=e^{-u^2},
 \\
 f_{\mathrm{heat2}}(u)
 &=(1+u)e^{-u}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0100

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:50`
- Строки: `50--62`

```latex
\begin{align}
 \frac{f_2}{f_0}\bigg|_{\mathrm{sharp}}
 &=1,
 &
 \frac{f_2}{f_0}\bigg|_{\mathrm{heat}}
 &=1,
 \\
 \frac{f_2}{f_0}\bigg|_{\mathrm{Gauss}}
 &=\frac{\sqrt\pi}{2},
 &
 \frac{f_2}{f_0}\bigg|_{\mathrm{heat2}}
 &=2.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0101

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:67`
- Строки: `67--69`

```latex
\begin{equation}
 \Lambda R=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0102

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:97`
- Строки: `97--100`

```latex
\begin{equation}
 f_a(u)=e^{-au},
 \qquad a>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0103

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:102`
- Строки: `102--106`

```latex
\begin{equation}
 f_a(0)=1,
 \qquad
 \frac{f_2}{f_0}=\frac1a.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0104

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:108`
- Строки: `108--111`

```latex
\begin{equation}
 \zeta_{\mathrm{mom}}
 =\frac{(\Lambda R)^2}{a}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0105

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:113`
- Строки: `113--117`

```latex
\begin{equation}
 a\longmapsto s^2a,
 \qquad
 \Lambda R\longmapsto s\Lambda R
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0106

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:133`
- Строки: `133--135`

```latex
\begin{equation}
 \Lambda R>\frac1{\sqrt{2\rho_f}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0107

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:137`
- Строки: `137--146`

```latex
\begin{align}
 \Lambda R&>\frac1{\sqrt2}
 &&\text{sharp/heat},
 \\
 \Lambda R&>\pi^{-1/4}
 &&\text{Gauss},
 \\
 \Lambda R&>\frac12
 &&\text{heat2}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION3-02-0108

- Источник: `s2t/gates/version3_spectral_function_moment_menu_gate.tex:160`
- Строки: `160--163`

```latex
\begin{equation}
 \zeta_{\mathrm{mom}}
 =(\chi R)^2+\frac12
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]