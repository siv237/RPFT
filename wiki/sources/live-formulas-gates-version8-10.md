# Гейты Version 8 — часть 10

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **8** блочных формул из **1** файла.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному реестру.

## `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0001

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 Q=\operatorname{diag}\!\left(\frac23,-\frac13\right).
 \label{eq:v8-baryon-em-one-particle-charge}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0002

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:16`
- Строки: `16--23`

```latex
\begin{equation}
 A=\sum_{r=1}^{3}(Q^{(r)})^2,
 \qquad
 C=\sum_{r\ne s}Q^{(r)}Q^{(s)},
 \qquad
 Q_{\rm tot}=\sum_{r=1}^{3}Q^{(r)}.
 \label{eq:v8-baryon-em-self-pair-total}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0003

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:25`
- Строки: `25--28`

```latex
\begin{equation}
 A+C=Q_{\rm tot}^2.
 \label{eq:v8-baryon-em-total-charge-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0004

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:32`
- Строки: `32--39`

```latex
\begin{equation}
 Q_{\rm tot}=2-n_d,
 \qquad
 A=\frac{4-n_d}{3},
 \qquad
 C=(2-n_d)^2-\frac{4-n_d}{3}.
 \label{eq:v8-baryon-em-epsilon-pattern}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0005

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:53`
- Строки: `53--57`

```latex
\begin{equation}
 T=\Tr(\rho Q^2)=\frac{14}{3}(a+b)
 =\frac{14(1+x)}{3(11+10x)}.
 \label{eq:v8-baryon-em-common-trace-norm}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0006

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:65`
- Строки: `65--68`

```latex
\begin{equation}
 H_{\mu,\lambda}=\frac1T(\mu A+\lambda C).
 \label{eq:v8-baryon-em-two-coefficient-form}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0007

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:71`
- Строки: `71--76`

```latex
\begin{equation}
 \mu=1,
 \qquad
 \lambda=1.
 \label{eq:v8-baryon-em-collapse-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0008

- Источник: `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex:92`
- Строки: `92--99`

```latex
\begin{equation}
 E_p=\frac{\mu}{T},
 \qquad
 E_n=\frac{2(\mu-\lambda)}{3T},
 \qquad
 E_n-E_p=-\frac{\mu+2\lambda}{3T}.
 \label{eq:v8-baryon-em-neutron-proton-sign}
\end{equation}
```

## `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0009

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:12`
- Строки: `12--18`

```latex
\begin{equation}
 H_{\rm el}=\frac1T\left[
 \mu\sum_{r=1}^{3}Q_r^2
 +2\sum_{1\le r<s\le3}g_{rs}Q_rQ_s
 \right].
 \label{eq:v8-baryon-em-spatial-general-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0010

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:24`
- Строки: `24--28`

```latex
\begin{equation}
 T(E_n-E_p)
 =-\frac{\mu}{3}+\frac{2}{3}(g_{23}-2g_{12}).
 \label{eq:v8-baryon-em-labelled-spatial-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0011

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:31`
- Строки: `31--36`

```latex
\begin{equation}
 \mu=1,\qquad g_{12}=g_{13}=1,\qquad g_{23}=3
 \quad\Longrightarrow\quad
 T(E_n-E_p)=\frac13>0.
 \label{eq:v8-baryon-em-positive-kernel-sign-counterexample}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0012

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \left\langle Q_rQ_s\right\rangle_p=0,
 \qquad
 \left\langle Q_rQ_s\right\rangle_n=-\frac19.
 \label{eq:v8-baryon-em-pair-charge-permutation-average}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0013

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:49`
- Строки: `49--52`

```latex
\begin{equation}
 \bar g=\frac{g_{12}+g_{13}+g_{23}}{3},
 \label{eq:v8-baryon-em-spatial-kernel-average}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0014

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 T(E_n-E_p)=-\frac{\mu+2\bar g}{3}.
 \label{eq:v8-baryon-em-symmetrized-spatial-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0015

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:73`
- Строки: `73--77`

```latex
\begin{equation}
 \psi_s(r_1,r_2,r_3)=s^{3d/2}\psi(sr_1,sr_2,sr_3),
 \qquad s>0.
 \label{eq:v8-baryon-em-wavefunction-dilation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0016

- Источник: `s2t/gates/version8_baryon_em_spatial_kernel_origin_gate.tex:79`
- Строки: `79--83`

```latex
\begin{equation}
 \left\langle\frac1{|r_i-r_j|}\right\rangle_{\psi_s}
 =s\left\langle\frac1{|r_i-r_j|}\right\rangle_{\psi}.
 \label{eq:v8-baryon-em-coulomb-dilation}
\end{equation}
```

## `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0017

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:12`
- Строки: `12--17`

```latex
\begin{equation}
 \mathcal H_{q}=\mathbb C^2_{\rm aroma}\otimes\mathbb C^2_{\rm spin},
 \qquad
 \mathcal H_{3q}=\mathcal H_q^{\otimes3}.
 \label{eq:v8-baryon-em-spin-flavor-carrier}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0018

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:21`
- Строки: `21--26`

```latex
\begin{equation}
 H_{\rm mag}=\frac{\zeta}{T}
 \sum_{1\le r<s\le3}h_{rs}Q_rQ_s\,
 \boldsymbol\Sigma_r\!\cdot\!\boldsymbol\Sigma_s.
 \label{eq:v8-baryon-em-magnetic-contact-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0019

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:34`
- Строки: `34--42`

```latex
\begin{equation}
 \chi_0=\frac{|\uparrow\downarrow\uparrow\rangle
 -|\downarrow\uparrow\uparrow\rangle}{\sqrt2},
 \qquad
 \chi_1=\sqrt{\frac23}|\uparrow\uparrow\downarrow\rangle
 -\frac{|\uparrow\downarrow\uparrow\rangle
 +|\downarrow\uparrow\uparrow\rangle}{\sqrt6}.
 \label{eq:v8-baryon-em-two-spin-half-couplings}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0020

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:44`
- Строки: `44--50`

```latex
\begin{equation}
 \bigl(\langle\Sigma_1\!\cdot\!\Sigma_2\rangle,
 \langle\Sigma_1\!\cdot\!\Sigma_3\rangle,
 \langle\Sigma_2\!\cdot\!\Sigma_3\rangle\bigr)
 =(-3,0,0),\quad(1,-2,-2).
 \label{eq:v8-baryon-em-spin-half-pair-correlations}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0021

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:55`
- Строки: `55--62`

```latex
\begin{equation}
 \begin{array}{c|cc|c}
  &O_p&O_n&O_n-O_p\\ \hline
  \chi_0&-4/3&2/3&2\\
  \chi_1& 4/3&0&-4/3
 \end{array}.
 \label{eq:v8-baryon-em-spin-coupling-sign-countermodels}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0022

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:72`
- Строки: `72--76`

```latex
\begin{equation}
 P_{\rm sf}=\frac1{6}\sum_{\pi\in S_3}U_\pi^{\rm aroma}
 \otimes U_\pi^{\rm spin}.
 \label{eq:v8-baryon-em-spin-flavor-symmetrizer}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0023

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:80`
- Строки: `80--87`

```latex
\begin{equation}
 O_p=\frac43,
 \qquad
 O_n=1,
 \qquad
 O_n-O_p=-\frac13.
 \label{eq:v8-baryon-em-symmetric-spin-flavor-magnetic-values}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0024

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:93`
- Строки: `93--96`

```latex
\begin{equation}
 E_n^{\rm mag}-E_p^{\rm mag}=-\frac{\zeta h}{3T}.
 \label{eq:v8-baryon-em-conditional-magnetic-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0025

- Источник: `s2t/gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex:111`
- Строки: `111--115`

```latex
\begin{equation}
 \left\langle\delta^{(d)}(r_i-r_j)\right\rangle_{\psi_s}
 =s^d\left\langle\delta^{(d)}(r_i-r_j)\right\rangle_{\psi}.
 \label{eq:v8-baryon-em-contact-density-dilation}
\end{equation}
```

## `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0026

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 U_\pi^{\rm color}|\varepsilon\rangle
 =\operatorname{sgn}(\pi)|\varepsilon\rangle.
 \label{eq:v8-baryon-color-sign-representation}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0027

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:25`
- Строки: `25--32`

```latex
\begin{equation}
 m_{\lambda\mu}
 =\frac16\left[
 \chi_\lambda(e)\chi_\mu(e)
 +3\chi_\lambda(12)\chi_\mu(12)
 +2\chi_\lambda(123)\chi_\mu(123)\right].
 \label{eq:v8-baryon-s3-invariant-multiplicity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0028

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:34`
- Строки: `34--38`

```latex
\begin{equation}
 (m_{\lambda\mu})_{\lambda,\mu\in
 \{\mathbf1,\mathbf1_{\rm sgn},\mathbf2\}}=I_3.
 \label{eq:v8-baryon-s3-matching-matrix}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0029

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:40`
- Строки: `40--46`

```latex
\begin{equation}
 (\mathcal H_{\rm space},\mathcal H_{\rm sf})
 \sim(\mathbf1,\mathbf1),\quad
 (\mathbf1_{\rm sgn},\mathbf1_{\rm sgn}),\quad
 (\mathbf2,\mathbf2).
 \label{eq:v8-baryon-three-permutation-branches}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0030

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:55`
- Строки: `55--59`

```latex
\begin{equation}
 \mathcal H_{I=S=1/2}
 \cong\mathbf1\oplus\mathbf1_{\rm sgn}\oplus\mathbf2.
 \label{eq:v8-baryon-nucleon-s3-decomposition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0031

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:66`
- Строки: `66--74`

```latex
\begin{equation}
 \begin{array}{c|ccc}
 \text{тип }S_3&O_p&O_n&O_n-O_p\\ \hline
 \mathbf1&4/3&1&-1/3\\
 \mathbf1_{\rm sgn}&-4/3&-1/3&1\\
 \mathbf2&0&1/3&1/3
 \end{array}.
 \label{eq:v8-baryon-s3-magnetic-branch-table}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0032

- Источник: `s2t/gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex:88`
- Строки: `88--91`

```latex
\begin{equation}
 \ker(H_{\rm space}-E_0)=\mathbf1,
 \label{eq:v8-baryon-symmetric-spatial-ground-condition}
\end{equation}
```

## `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0033

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 T_2=U_{(12)}+U_{(13)}+U_{(23)},\qquad
 T_3=U_{(123)}+U_{(132)}.
 \label{eq:v8-baryon-spatial-s3-class-sums}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0034

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:18`
- Строки: `18--21`

```latex
\begin{equation}
 H_{\alpha,\beta}=\alpha T_2+\beta T_3
 \label{eq:v8-baryon-spatial-central-hamiltonian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0035

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:24`
- Строки: `24--29`

```latex
\begin{equation}
 E_{\mathbf1}=3\alpha+2\beta,\qquad
 E_{\mathbf1_{\rm sgn}}=-3\alpha+2\beta,\qquad
 E_{\mathbf2}=-\beta.
 \label{eq:v8-baryon-spatial-s3-levels}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0036

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:31`
- Строки: `31--40`

```latex
\begin{equation}
 \begin{array}{c|ccc|c}
 (\alpha,\beta)&E_{\mathbf1}&E_{\mathbf1_{\rm sgn}}&E_{\mathbf2}
 &\text{основной тип}\\ \hline
 (-1,0)&-3&3&0&\mathbf1\\
 (1,0)&3&-3&0&\mathbf1_{\rm sgn}\\
 (0,1)&2&2&-1&\mathbf2
 \end{array}.
 \label{eq:v8-baryon-spatial-ground-branch-countermodels}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0037

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:51`
- Строки: `51--57`

```latex
\begin{equation}
 f\ge0,\ f\ne0
 \quad\Longrightarrow\quad
 e^{-tH_{\rm space}}f>0
 \quad(t>0).
 \label{eq:v8-baryon-spatial-positivity-improving-condition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0038

- Источник: `s2t/gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex:61`
- Строки: `61--65`

```latex
\begin{equation}
 U_\pi\psi_0=\psi_0
 \qquad\text{для всех }\pi\in S_3.
 \label{eq:v8-baryon-spatial-positive-ground-symmetry}
\end{equation}
```

## `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-10-0039
- Источник: `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex:10`
- Строки: `10--13`
```latex
\begin{equation}
 A_{\rm el}=\mu+2\bar g>0,\qquad z=\zeta h.
 \label{eq:v8-baryon-em-closure-parameters}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0040
- Источник: `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex:16`
- Строки: `16--24`
```latex
\begin{equation}
 3T(E_n-E_p)=
 \begin{cases}
  -A_{\rm el}-z,&\mathbf1,\\
  -A_{\rm el}+3z,&\mathbf1_{\rm sgn},\\
  -A_{\rm el}+z,&\mathbf2.
 \end{cases}
 \label{eq:v8-baryon-em-three-branch-total-splitting}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0041
- Источник: `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex:26`
- Строки: `26--31`
```latex
\begin{equation}
 z>-A_{\rm el},\qquad
 z<\frac{A_{\rm el}}3,\qquad
 z<A_{\rm el}.
 \label{eq:v8-baryon-em-branch-sign-conditions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0042
- Источник: `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex:33`
- Строки: `33--36`
```latex
\begin{equation}
 -A_{\rm el}<z<\frac{A_{\rm el}}3.
 \label{eq:v8-baryon-em-common-negative-strip}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0043
- Источник: `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex:42`
- Строки: `42--50`
```latex
\begin{equation}
 \begin{array}{c|c|c}
 \text{ветвь}&z&3T(E_n-E_p)\\ \hline
 \mathbf1&-2A_{\rm el}&A_{\rm el}\\
 \mathbf1_{\rm sgn}&A_{\rm el}&2A_{\rm el}\\
 \mathbf2&2A_{\rm el}&A_{\rm el}
 \end{array}.
 \label{eq:v8-baryon-em-closure-sign-countermodels}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Инкремент связного трёхчастичного ядра

### LIVE-FORMULAS-GATES-VERSION8-10-0044
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:12`
- Строки: `12--17`
```latex
\begin{equation}
 p_\theta(x_1,x_2,x_3)
 =\frac18\bigl(1+\theta x_1x_2x_3\bigr),
 \qquad -1\leq\theta\leq1.
 \label{eq:v8-baryon-three-body-parity-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0045
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:20`
- Строки: `20--25`
```latex
\begin{equation}
 \mathbb E_\theta[x_i]=0,
 \qquad
 \mathbb E_\theta[x_ix_j]=0\quad(i\ne j),
 \label{eq:v8-baryon-three-body-lower-moments}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0046
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:27`
- Строки: `27--30`
```latex
\begin{equation}
 \mathbb E_\theta[x_1x_2x_3]=\theta.
 \label{eq:v8-baryon-three-body-connected-moment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0047
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:35`
- Строки: `35--39`
```latex
\begin{equation}
 \ker M_{\leq2}
 =\operatorname{span}\{(x_1x_2x_3)_{(x_1,x_2,x_3)}\}.
 \label{eq:v8-baryon-pair-marginal-kernel}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0048
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:53`
- Строки: `53--57`
```latex
\begin{equation}
 H_{\rm int}=\sum_{a=1}^{42}F_a\otimes
 \bigl(|a\rangle\langle0|+|0\rangle\langle a|\bigr).
 \label{eq:v8-baryon-star-interaction-recall}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0049
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:60`
- Строки: `60--65`
```latex
\begin{equation}
 \Pi H_{\rm int}\Pi=-H_{\rm int},
 \qquad
 \langle0|H_{\rm int}^{2m+1}|0\rangle=0.
 \label{eq:v8-baryon-star-odd-moment-zero}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0050
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:72`
- Строки: `72--77`
```latex
\begin{equation}
 n h=u,
 \qquad
 n h^{3/2}\kappa_3=u\varepsilon\kappa_3\longrightarrow0.
 \label{eq:v8-baryon-third-cumulant-collision-scaling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0051
- Источник: `s2t/gates/version8_baryon_connected_three_body_kernel_admission_gate.tex:85`
- Строки: `85--90`
```latex
\begin{equation}
 \Psi=K_{(3)}\Psi,
 \qquad
 K_{(3)}=K_{(3)}^{\rm irr}+\sum_{a=1}^{3}K_{(2)}^{(a)}.
 \label{eq:v8-baryon-faddeev-kernel-target}
\end{equation}
```

## Инкремент кубического следового оператора

### LIVE-FORMULAS-GATES-VERSION8-10-0052
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:13`
- Строки: `13--16`
```latex
\begin{equation}
 \widehat F_a=F_a-\frac{\Tr F_a}{21}I_{21}.
 \label{eq:v8-baryon-centered-noise-frame}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0053
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:19`
- Строки: `19--22`
```latex
\begin{equation}
 [\widehat F_a,[\widehat F_a,X]]=[F_a,[F_a,X]].
 \label{eq:v8-baryon-centering-preserves-generator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0054
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:25`
- Строки: `25--28`
```latex
\begin{equation}
 \widehat K_{ab}=\Tr(\widehat F_a\widehat F_b)
 \label{eq:v8-baryon-centered-trace-metric}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0055
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:34`
- Строки: `34--38`
```latex
\begin{equation}
 d_{abc}=\frac12\Tr\!\left(
 \widehat F_a\{\widehat F_b,\widehat F_c\}\right).
 \label{eq:v8-baryon-cubic-trace-tensor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0056
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:42`
- Строки: `42--46`
```latex
\begin{equation}
 N_{TTT}=0,\qquad N_{TTG}=140,\qquad
 N_{TGG}=0,\qquad N_{GGG}=28,
 \label{eq:v8-baryon-cubic-trace-support}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0057
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:54`
- Строки: `54--59`
```latex
\begin{equation}
 W_3=d^{abc}\widehat F_a\otimes\widehat F_b\otimes\widehat F_c,
 \qquad
 d^{abc}=\widehat K^{aa'}\widehat K^{bb'}\widehat K^{cc'}d_{a'b'c'}.
 \label{eq:v8-baryon-connected-cubic-operator}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0058
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:63`
- Строки: `63--66`
```latex
\begin{equation}
 \Tr_1W_3=\Tr_2W_3=\Tr_3W_3=0.
 \label{eq:v8-baryon-connected-cubic-partial-traces}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0059
- Источник: `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex:83`
- Строки: `83--86`
```latex
\begin{equation}
 H_{(3)}=\lambda_3W_3.
 \label{eq:v8-baryon-cubic-parent-term}
\end{equation}
```

## Инкремент происхождения кубического коэффициента

### LIVE-FORMULAS-GATES-VERSION8-10-0060
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:11`
- Строки: `11--14`
```latex
\begin{equation}
 A=\widehat F_0+\widehat F_{40}.
 \label{eq:v8-baryon-cubic-coefficient-test-ray}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0061
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:16`
- Строки: `16--19`
```latex
\begin{equation}
 \Tr A^2=38,\qquad \Tr A^3=-3,\qquad \Tr A^4=134.
 \label{eq:v8-baryon-cubic-coefficient-ray-moments}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0062
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:26`
- Строки: `26--30`
```latex
\begin{equation}
 S(t)=38\alpha t^2-3\lambda_3t^3+134\beta t^4,
 \qquad \alpha>0,\quad\beta>0.
 \label{eq:v8-baryon-cubic-coefficient-ray-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0063
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:33`
- Строки: `33--36`
```latex
\begin{equation}
 S'''(0)=-18\lambda_3.
 \label{eq:v8-baryon-cubic-coefficient-third-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0064
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:49`
- Строки: `49--54`
```latex
\begin{equation}
 S'(1)=0
 \quad\Longleftrightarrow\quad
 \lambda_3=\frac{76\alpha+536\beta}{9}.
 \label{eq:v8-baryon-cubic-coefficient-stationarity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0065
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:56`
- Строки: `56--61`
```latex
\begin{equation}
 S''(1)=-76\alpha+536\beta,
 \qquad
 S''(1)>0\Longleftrightarrow\beta>\frac{19}{134}\alpha.
 \label{eq:v8-baryon-cubic-coefficient-stability}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0066
- Источник: `s2t/gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex:64`
- Строки: `64--67`
```latex
\begin{equation}
 \frac{\lambda_3^2}{\alpha\beta}
 \label{eq:v8-baryon-cubic-coefficient-shape-ratio}
\end{equation}
```

## Инкремент сдвинутой суперкривизны

### LIVE-FORMULAS-GATES-VERSION8-10-0067
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:14`
- Строки: `14--18`
```latex
\begin{equation}
 Z=z^a\widehat F_a,\qquad
 M=\frac m2I_{21}.
 \label{eq:v8-baryon-shifted-supercurvature-field}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0068
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:20`
- Строки: `20--23`
```latex
\begin{equation}
 \mathcal R_m(Z)=(M+Z)^2-M^2=mZ+Z^2.
 \label{eq:v8-baryon-shifted-supercurvature}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0069
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:29`
- Строки: `29--33`
```latex
\begin{equation}
 \Tr\mathcal R_m(Z)^2
 =m^2\Tr Z^2+2m\Tr Z^3+\Tr Z^4.
 \label{eq:v8-baryon-shifted-supercurvature-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0070
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:35`
- Строки: `35--39`
```latex
\begin{equation}
 \alpha=m^2,\qquad \lambda_3=2m,\qquad \beta=1,
 \qquad \frac{\lambda_3^2}{\alpha\beta}=4.
 \label{eq:v8-baryon-shifted-supercurvature-shape}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0071
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:46`
- Строки: `46--49`
```latex
\begin{equation}
 \Tr Z^3=d_{abc}z^az^bz^c.
 \label{eq:v8-baryon-cubic-trace-polynomial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0072
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:51`
- Строки: `51--56`
```latex
\begin{equation}
 S^{(3)}(Z)=2m\,d_{abc}z^az^bz^c,
 \qquad
 \delta^3S\big|_0=12m\,d_{abc}.
 \label{eq:v8-baryon-supercurvature-cubic-projection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0073
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:64`
- Строки: `64--67`
```latex
\begin{equation}
 S_m(t)=38m^2t^2-6mt^3+134t^4.
 \label{eq:v8-baryon-shifted-supercurvature-ray-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0074
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:69`
- Строки: `69--74`
```latex
\begin{equation}
 S_m'(t)=2t\left(38m^2-9mt+268t^2\right),
 \qquad
 \Delta=-40655m^2.
 \label{eq:v8-baryon-shifted-supercurvature-ray-stationarity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0075
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:89`
- Строки: `89--92`
```latex
\begin{equation}
 \Tr M=\frac{21}{2}m.
 \label{eq:v8-baryon-central-background-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0076
- Источник: `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex:103`
- Строки: `103--106`
```latex
\begin{equation}
 \Gamma M+M\Gamma=m\Gamma.
 \label{eq:v8-baryon-central-background-parity-defect}
\end{equation}
```

## Инкремент нечётного фонового запрета

### LIVE-FORMULAS-GATES-VERSION8-10-0077
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:12`
- Строки: `12--18`
```latex
\begin{equation}
 \Gamma=I_{11}\oplus(-I_{10}),\qquad
 \Gamma\widehat F_a\Gamma=(-1)^{p_a}\widehat F_a,
 \quad
 p_a=\begin{cases}1,&a<30,\\0,&a\ge30.\end{cases}
 \label{eq:v8-baryon-full-frame-finite-parity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0078
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:21`
- Строки: `21--25`
```latex
\begin{equation}
 D=\begin{pmatrix}0&B^*\\B&0\end{pmatrix},
 \qquad \Gamma D\Gamma=-D.
 \label{eq:v8-baryon-general-odd-dirac-background}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0079
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:30`
- Строки: `30--33`
```latex
\begin{equation}
 \operatorname{supp}d=140\,TTG+28\,GGG.
 \label{eq:v8-baryon-canonical-cubic-even-support}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0080
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:38`
- Строки: `38--43`
```latex
\begin{equation}
 c^{D}_{abc}
 =\operatorname{Sym}_{abc}\Tr
 \left(D\widehat F_a\widehat F_b\widehat F_c\right).
 \label{eq:v8-baryon-odd-background-cubic-tensor}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0081
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:45`
- Строки: `45--48`
```latex
\begin{equation}
 \Tr(D_{\rm odd}S_{\rm even})=0.
 \label{eq:v8-baryon-odd-even-trace-orthogonality}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0082
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:53`
- Строки: `53--58`
```latex
\begin{equation}
 \operatorname{supp}c^{D_0}=130\,TTT+35\,TGG,
 \qquad
 c^{D_0}_{TTG}=c^{D_0}_{GGG}=0.
 \label{eq:v8-baryon-incidence-odd-background-support}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0083
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:74`
- Строки: `74--78`
```latex
\begin{equation}
 \mathbb A=d+A^{(1)}_{\rm even}+\Phi^{(0)}_{\rm odd},
 \qquad |\mathbb A|_{\rm total}=1.
 \label{eq:v8-baryon-total-odd-superconnection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0084
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:80`
- Строки: `80--83`
```latex
\begin{equation}
 \mathbb F=F_A+D_A\Phi+\Phi^2.
 \label{eq:v8-baryon-full-supercurvature-decomposition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0085
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:86`
- Строки: `86--91`
```latex
\begin{equation}
 2\langle dA,A^2\rangle,\qquad
 2\langle dA,\Phi^2\rangle
 +2\langle d\Phi,[A,\Phi]\rangle.
 \label{eq:v8-baryon-derivative-cubic-supercurvature-vertices}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-10-0086
- Источник: `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex:94`
- Строки: `94--99`
```latex
\begin{equation}
 dA=d\Phi=0
 \quad\Longrightarrow\quad
 S^{(3)}_{\rm supercurvature}=0.
 \label{eq:v8-baryon-zero-momentum-supercurvature-cubic-vanishing}
\end{equation}
```