# Гейты Version 4, часть 8

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **110** блочных формул из **12** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_affine_modular_temperature_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0001

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:11`
- Строки: `11--15`

```latex
\begin{align}
 \mu_s&=\frac13\Tr R_{4,s},\\
 \sigma_s^2&=\frac13\Tr(R_{4,s}-\mu_sI)^2,\\
 Z_s&=\frac{R_{4,s}-\mu_sI}{\sigma_s}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0002

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:20`
- Строки: `20--23`

```latex
\begin{equation}
 \mathcal F_s(\rho)=\Tr(\rho Z_s)+\Tr(\rho\log\rho),
 \qquad \Tr\rho=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0003

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 \rho_s^\star=\frac{e^{-Z_s}}{\Tr e^{-Z_s}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0004

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:39`
- Строки: `39--42`

```latex
\begin{align}
 \Spec\rho_u&=(0.05749,\,0.34272,\,0.59979),\\
 \Spec\rho_d&=(0.05739,\,0.34886,\,0.59375).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0005

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:48`
- Строки: `48--54`

```latex
\begin{equation}
 L_s^{KMS},
 \qquad
 (\epsilon_{00},\epsilon_{01},\epsilon_{10},\epsilon_{11})=(-1,-1,-1,-1),
 \qquad
 t=243.2865.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0006

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:56`
- Строки: `56--59`

```latex
\begin{align}
 u&=(0.00086849,\,0.00180844,\,1),\\
 d&=(0.00092143,\,0.00159191,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0007

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:66`
- Строки: `66--73`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.96287&0.26998&0.000403\\
 0.26998&0.96287&0.000173\\
 0.000435&0.0000584&1
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0008

- Источник: `s2t/gates/version4_affine_modular_temperature_gate.tex:75`
- Строки: `75--77`

```latex
\begin{equation}
 \frac{s_{12}}{s_{12}^{\rm CKM}}=1.20.
\end{equation}
```

## `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0009

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:12`
- Строки: `12--20`

```latex
\begin{equation}
 X\in\operatorname{Mat}_3(\mathbb R),
 \qquad
 X\longmapsto gXf^{-1},
 \qquad
 g\in SO(3)_{\rm gauge},\quad
 f\in SO(3)_{\rm family}^{\rm global}.
 \label{eq:gauge-family-bifundamental}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0010

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:22`
- Строки: `22--27`

```latex
\begin{equation}
 V_{\rm lock}(X)
 =\frac14\|X^TX-I_3\|_F^2
 +\frac14(\det X-1)^2.
 \label{eq:real-bifundamental-locking-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0011

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 X_\star=I_3,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0012

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 SO(3)_{g+f}=\{(g,f):g=f\}.
 \label{eq:diagonal-family-group}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0013

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:40`
- Строки: `40--42`

```latex
\begin{equation}
 (6_+,3_0,0_-).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0014

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
 (2,2,2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0015

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:74`
- Строки: `74--83`

```latex
\begin{equation}
 SO(3)_{\rm gauge}\times SO(3)_{\rm family}^{\rm global}
 \xrightarrow{\langle X\rangle}
 SO(3)_{g+f}
 \xrightarrow{\langle\mathcal T\rangle}
 A_4
 \xrightarrow{\langle P_a\rangle}
 \mathbb Z_3.
 \label{eq:locked-tetrahedral-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0016

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:94`
- Строки: `94--101`

```latex
\begin{equation}
 V_\Phi
 =m_\Phi^2|\Phi|^2
 +\frac{\lambda_\Phi}{2}|\Phi|^4
 +\kappa|\Phi|^2\Tr(X^TX),
 \qquad \lambda_\Phi>0.
 \label{eq:generic-locking-pairing-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0017

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:103`
- Строки: `103--105`

```latex
\begin{equation}
 m_{\rm eff}^2=m_\Phi^2+3\kappa.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0018

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:107`
- Строки: `107--112`

```latex
\begin{align}
 (m_\Phi^2,\lambda_\Phi,\kappa)&=(1,1,0),
 &|\Phi_\star|^2&=0,\\
 (m_\Phi^2,\lambda_\Phi,\kappa)&=(1,1,-1),
 &|\Phi_\star|^2&=2
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0019

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:125`
- Строки: `125--131`

```latex
\begin{equation}
 V_\mu(X,\Phi)
 =\left(
 |\Phi|^2-\frac13\Tr X^TX
 \right)^2.
 \label{eq:norm-locking-moment-map-square}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0020

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:133`
- Строки: `133--137`

```latex
\begin{equation}
 |\Phi_\star|=1,
 \qquad
 \partial_{|\Phi|}^2V_\mu\big|_\star=8.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0021

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:142`
- Строки: `142--148`

```latex
\begin{equation}
 |\Phi|^4,
 \qquad
 |\Phi|^2\Tr X^TX,
 \qquad
 (\Tr X^TX)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0022

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:150`
- Строки: `150--152`

```latex
\begin{equation}
 1:-\frac23:\frac19
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0023

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:166`
- Строки: `166--168`

```latex
\begin{equation}
 \Phi\sim\det X.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0024

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:171`
- Строки: `171--173`

```latex
\begin{equation}
 (\det X)N^cN^c
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0025

- Источник: `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex:183`
- Строки: `183--189`

```latex
\begin{equation}
 \boxed{
 \begin{gathered}
 \text{вывести }V_\mu\text{ или эквивалентный}\\
 \text{negative pairing Hessian из одного finite graded supertrace}
 \end{gathered}}
\end{equation}
```

## `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0026

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 \rho_\tau(M)=\frac{e^{-\tau\Delta_M}}{Z_M(\tau)},
 \qquad
 Z_M(\tau)=\Tr e^{-\tau\Delta_M},
 \qquad \tau=\sigma^2>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0027

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:20`
- Строки: `20--26`

```latex
\begin{equation}
 \Phi_\tau[\rho;M]
 =\Tr(\rho\Delta_M)
 +\frac1\tau\Tr(\rho\log\rho)
 =E_M(\rho)-\frac1\tau S_{\rm vN}(\rho).
 \label{eq:gibbs-carrier-functional}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0028

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:32`
- Строки: `32--37`

```latex
\begin{equation}
 \Phi_\tau[\rho;M]-F_\tau(M)
 =\frac1\tau
 D\!\left(\rho\middle\|\rho_\tau(M)\right)\ge0,
 \label{eq:gibbs-relative-entropy-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0029

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 F_\tau(M)=-\frac1\tau\log Z_M(\tau)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0030

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 \log\rho_\tau=-\tau\Delta_M-\log Z_M,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0031

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 M_*\in\operatorname*{argmin}_{\operatorname{Vol}(M)=1}F_\tau(M)
 =\operatorname*{argmax}_{\operatorname{Vol}(M)=1}\log Z_M(\tau).
 \label{eq:gibbs-carrier-selection}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0032

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
 \Delta\log Z(\tau)
 =\log Z_{S^4}(\tau)-\log Z_{S^2\times S^2}(\tau).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0033

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:72`
- Строки: `72--77`

```latex
\begin{equation}
 \Delta\log Z(\tau)
 =\frac{R_{S^4}-R_{S^2\times S^2}}6\tau+O(\tau^2)
 =\frac{4\pi}{3}(\sqrt6-2)\tau+O(\tau^2)>0.
 \label{eq:gibbs-small-tau-sign}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0034

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:79`
- Строки: `79--82`

```latex
\begin{equation}
 \Delta\log Z(\tau)
 \sim5e^{-4\tau/a^2}-6e^{-2\tau/b^2}>0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0035

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:89`
- Строки: `89--92`

```latex
\begin{equation}
 \Delta\log Z(0.0957664505\ldots)
 =0.1079375302\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0036

- Источник: `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex:94`
- Строки: `94--98`

```latex
\begin{equation}
 \Delta F_\tau
 =F_\tau(S^4)-F_\tau(S^2\times S^2)
 =-\frac{\Delta\log Z(\tau)}\tau<0
\end{equation}
```

## `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0037

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 Gv_a=\lambda_av_a.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0038

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:17`
- Строки: `17--24`

```latex
\begin{equation}
 V\simeq
 \begin{pmatrix}
 -0.205814&0.791747&0.575132\\
 0.785619&-0.216738&0.579506\\
 -0.583475&-0.571105&0.577404
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0039

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:27`
- Строки: `27--30`

```latex
\begin{equation}
 Q_{a,s}=\frac1{\sqrt{\lambda_a}}
 \sum_{n\in\{4,6,8\}}V_{n a}Z_{n,s}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0040

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 m_a=\sqrt{\lambda_a/\lambda_1}
 =(1,15.8427,169.435).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0041

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 L_s=(Q_{1,s}\;Q_{2,s}\;Q_{3,s}),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0042

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:57`
- Строки: `57--59`

```latex
\begin{equation}
 t=655.7588
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0043

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:61`
- Строки: `61--64`

```latex
\begin{align}
 u&=(0.00097216,\,0.00119007,\,1),\\
 d&=(0.00126128,\,0.00157721,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0044

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:70`
- Строки: `70--77`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.999813&0.0193620&2.6424\times10^{-5}\\
 0.0193620&0.999813&1.0738\times10^{-5}\\
 2.6211\times10^{-5}&1.1248\times10^{-5}&1
 \end{pmatrix},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0045

- Источник: `s2t/gates/version4_gram_eigenvector_endpoint_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 |J_q|=8.77\times10^{-15}.
\end{equation}
```

## `s2t/gates/version4_hypercharge_anomaly_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0046

- Источник: `s2t/gates/version4_hypercharge_anomaly_gate.tex:7`
- Строки: `7--12`

```latex
\begin{equation}
\begin{gathered}
Y(Q_L)=q,\quad Y(u_R)=u,\quad Y(d_R)=d,\quad Y(L_L)=\ell,\\
Y(e_R)=e,\quad Y(\nu_R)=n,\quad Y(H)=h.
\end{gathered}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0047

- Источник: `s2t/gates/version4_hypercharge_anomaly_gate.tex:14`
- Строки: `14--16`

```latex
\begin{equation}
u=q+h,\qquad d=q-h,\qquad e=\ell-h,\qquad n=\ell+h.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0048

- Источник: `s2t/gates/version4_hypercharge_anomaly_gate.tex:18`
- Строки: `18--23`

```latex
\begin{align}
\mathcal A_{331}&=2q-u-d,\\
\mathcal A_{221}&=3q+\ell,\\
\mathcal A_{\mathrm{grav}^2 1}&=6q-3u-3d+2\ell-e-n,\\
\mathcal A_{111}&=6q^3-3u^3-3d^3+2\ell^3-e^3-n^3.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0049

- Источник: `s2t/gates/version4_hypercharge_anomaly_gate.tex:29`
- Строки: `29--32`

```latex
\begin{equation}
\boxed{(q,u,d,\ell,e,n,h)=
\left(\frac16,\frac23,-\frac13,-\frac12,-1,0,\frac12\right).}
\end{equation}
```

## `s2t/gates/version4_incidence_operator_menu_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0050

- Источник: `s2t/gates/version4_incidence_operator_menu_gate.tex:15`
- Строки: `15--17`

```latex
\begin{equation}
H_g=\frac{P_g+P_g^\dagger}{2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0051

- Источник: `s2t/gates/version4_incidence_operator_menu_gate.tex:36`
- Строки: `36--38`

```latex
\begin{equation}
M_3(\mathbb C)
\end{equation}
```

## `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0052

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 V_R=(2_R,4),\qquad V_L=(2_L,4)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0053

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 \bar4\longrightarrow2_R\longrightarrow4
 \label{eq:ps-bv-relative-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0054

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:32`
- Строки: `32--34`

```latex
\begin{equation}
 4\lambda_{\rm rel}\det(\Delta\Delta^\dagger)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0055

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:47`
- Строки: `47--49`

```latex
\begin{equation}
 (\Delta b_R,\Delta b_L,\Delta b_4)=(-2/3,0,-4/3).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0056

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:51`
- Строки: `51--56`

```latex
\begin{equation}
 3.127\%\to2.157\%,\quad
 2.923\%\to1.732\%,\quad
 2.631\%\to3.952\%,\quad
 4.902\%\to4.291\%.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0057

- Источник: `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex:63`
- Строки: `63--65`

```latex
\begin{equation}
 8\sqrt2\ (1),\qquad0\ (9),\qquad\sqrt2(4k-2)\ (6).
\end{equation}
```

## `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0058

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:12`
- Строки: `12--17`

```latex
\begin{equation}
 \mathcal H_1=\bar4\oplus2_R\oplus4,
 \qquad
 \mathcal B_h=M_4(\mathbb C)\oplus M_2(\mathbb C)
 \,\oplus M_4(\mathbb C),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0059

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 \mathcal B_h'
 =\{\alpha I_4\oplus\beta I_2\oplus\gamma I_4\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0060

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:27`
- Строки: `27--30`

```latex
\begin{equation}
 \boxed{\{\mathcal B_h,\mathcal D_\Delta\}'=\mathbb C I_{10}.}
 \label{eq:ps-relative-one-copy-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0061

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:37`
- Строки: `37--43`

```latex
\begin{equation}
 \mathcal H_k=\mathcal H_1\otimes\mathbb C^k,
 \qquad
 \mathcal B_{h,k}=\mathcal B_h\otimes I_k,
 \qquad
 \mathcal D_{\Delta,k}=\mathcal D_\Delta\otimes I_k.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0062

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:45`
- Строки: `45--52`

```latex
\begin{equation}
 \boxed{
 \{\mathcal B_{h,k},\mathcal D_{\Delta,k}\}'
 =I_{10}\otimes M_k(\mathbb C),
 \qquad
 \dim_\mathbb C=k^2.}
 \label{eq:ps-relative-k-copy-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0063

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 k=1,
 \qquad
 \boxed{\lambda_{\rm rel}=1.}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0064

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:69`
- Строки: `69--71`

```latex
\begin{equation}
 1,\ 4,\ 9,\ 16,\ 25,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0065

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:93`
- Строки: `93--99`

```latex
\begin{equation}
 V(\Delta,C)=-\rho^2+\tau^2
 +\|\mathcal D_\Delta^2-C\|_F^2,
 \qquad
 C\in\mathcal B_h^{\rm sa}.
 \label{eq:ps-relative-uneliminated-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0066

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:101`
- Строки: `101--103`

```latex
\begin{equation}
 4^2+2^2+4^2=36.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0067

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:108`
- Строки: `108--115`

```latex
\begin{equation}
 H_{\rm full}=
 \begin{pmatrix}
 H_{\rm eff}+2J_E^TJ_E&-2J_E^T\\
 -2J_E&2I_{36}
 \end{pmatrix}.
 \label{eq:ps-relative-full-hessian-block}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0068

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:117`
- Строки: `117--119`

```latex
\begin{equation}
 H_{\rm full}/(2I_{36})=H_{\rm eff}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0069

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:121`
- Строки: `121--124`

```latex
\begin{equation}
 \Spec H_{\rm eff}
 =\{8\sqrt2\ (1),\ 2\sqrt2\ (6),\ 0\ (9)\},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0070

- Источник: `s2t/gates/version4_pati_salam_irreducible_relative_cycle_gate.tex:126`
- Строки: `126--129`

```latex
\begin{equation}
 \boxed{(43_+,9_0,0_-).}
 \label{eq:ps-relative-full-hessian-inertia}
\end{equation}
```

## `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0071

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 \mathcal H_{\rm ch}=\bar4^+\oplus2_R^-\oplus4^+.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0072

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:16`
- Строки: `16--23`

```latex
\begin{align}
 \mathcal H_{\rm rel}&=\mathcal H_{\rm ch}\oplus\mathcal H_{\rm ch}^c,\\
 D_{\rm rel}&=D_{\rm ch}\oplus\overline{D_{\rm ch}},\\
 \Gamma_{\rm rel}&=\Gamma_{\rm ch}\oplus(-\Gamma_{\rm ch}),\\
 J_{\rm rel}&=
 \begin{pmatrix}0&I_{10}\\I_{10}&0\end{pmatrix}K.
 \label{eq:ps-relative-ko6-completion}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0073

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:25`
- Строки: `25--31`

```latex
\begin{equation}
 D_{\rm rel}=D_{\rm rel}^\dagger,
 \qquad
 \{D_{\rm rel},\Gamma_{\rm rel}\}=0,
 \qquad
 J_{\rm rel}D_{\rm rel}=D_{\rm rel}J_{\rm rel},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0074

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:32`
- Строки: `32--36`

```latex
\begin{equation}
 J_{\rm rel}^2=1,
 \qquad
 \{J_{\rm rel},\Gamma_{\rm rel}\}=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0075

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 \frac12\left\|\frac12[h,D_{\rm rel}^2]\right\|_F^2
 =4\det(\Delta\Delta^\dagger).
 \label{eq:ps-relative-ko6-selector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0076

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:73`
- Строки: `73--75`

```latex
\begin{equation}
 D_F(Y,M_R,0)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0077

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:77`
- Строки: `77--80`

```latex
\begin{equation}
 V_{\rm fin}=-\frac12\Tr D_F^2+\frac12\Tr D_F^4.
 \label{eq:ps-full-composite-finite-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0078

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:82`
- Строки: `82--87`

```latex
\begin{align}
 Y={}&(k^\nu\phi+k^e\widetilde\phi)\otimes\Sigma_4
 +(k^u\phi+k^d\widetilde\phi)\otimes(I_4-\Sigma_4),\\
 (M_R)_{\dot aI,\dot bJ}={}&
 k_{\nu_R}^*\Delta_{\dot aJ}\Delta_{\dot bI}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0079

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:89`
- Строки: `89--95`

```latex
\begin{equation}
 \Delta_{\dot1,1}=2^{-1/4},
 \qquad
 \|M_R\|_{\rm op}^2=\frac12,
 \qquad
 \phi=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0080

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:103`
- Строки: `103--107`

```latex
\begin{equation}
 \boxed{
 H_Y(Y)=-4\|Y\|_F^2+8\|M_R^\dagger Y\|_F^2.}
 \label{eq:ps-general-yukawa-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0081

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:109`
- Строки: `109--111`

```latex
\begin{equation}
 H_Y(Y)\le0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0082

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:118`
- Строки: `118--120`

```latex
\begin{equation}
 (k^\nu,k^e,k^u,k^d)=(0.7,0.2,1.1,0.4)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0083

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:122`
- Строки: `122--124`

```latex
\begin{equation}
 \Sigma_{B-L}=\operatorname{diag}(3/4,-1/4,-1/4,-1/4)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0084

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:126`
- Строки: `126--131`

```latex
\begin{equation}
 -34.92338966\ (4),
 \qquad
 -7.30661034\ (4).
 \label{eq:ps-phi-negative-spectrum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0085

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:138`
- Строки: `138--140`

```latex
\begin{equation}
 H_{\Delta\phi}=H_{\Delta\Sigma}=H_{\phi\Sigma}=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0086

- Источник: `s2t/gates/version4_pati_salam_ko6_phi_sigma_hessian_gate.tex:166`
- Строки: `166--168`

```latex
\begin{equation}
 \boxed{(43_+,24_0,8_-).}
\end{equation}
```

## `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0087

- Источник: `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex:6`
- Строки: `6--14`

```latex
\begin{equation}
 P=\frac{\Delta^\dagger\Delta}
 {\Tr(\Delta^\dagger\Delta)},
 \qquad
 P^2=P,
 \qquad
 \rank P=1.
 \label{eq:ps-rank-one-color-projector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0088

- Источник: `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex:23`
- Строки: `23--30`

```latex
\begin{equation}
 \Tr(P\Sigma^2),
 \qquad
 \Tr(P\Sigma P\Sigma),
 \qquad
 \bigl(\Tr(P\Sigma)\bigr)^2.
 \label{eq:ps-connected-sigma-word-basis}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0089

- Источник: `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex:32`
- Строки: `32--38`

```latex
\begin{equation}
 P\Sigma,\quad
 \Sigma P,\quad
 [P,\Sigma],\quad
 \{P,\Sigma\},\quad
 \Tr(P\Sigma).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0090

- Источник: `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex:43`
- Строки: `43--47`

```latex
\begin{equation}
 \Sigma_8=Q\Sigma_8Q,
 \qquad
 \Sigma_8\in\mathfrak{su}(3),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0091

- Источник: `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex:101`
- Строки: `101--108`

```latex
\begin{equation}
 M_R^\dagger Y,\quad
 YM_R^\dagger,\quad
 P_LY,\quad
 YP_R,\quad
 [M_R^\dagger,Y],\quad
 \{M_R^\dagger,Y\}
\end{equation}
```

## `s2t/gates/version4_spin_structure_relative_determinant_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0092

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:13`
- Строки: `13--18`

```latex
\begin{equation}
 |\lambda_k|=\frac{k+3/2}{R_3},
 \qquad
 d_k=(k+1)(k+2),
 \qquad k\ge0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0093

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:21`
- Строки: `21--24`

```latex
\begin{equation}
 \Spec D_{\mathbb{RP}^3,\tau_+}^2
 =\Spec D_{\mathbb{RP}^3,\tau_-}^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0094

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 \eta_D(\tau_\pm)=\pm\frac14
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0095

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:45`
- Строки: `45--49`

```latex
\begin{equation}
 p_m=\frac{m+\beta}{R_1},
 \qquad
 \beta\in\mathbb R/\mathbb Z.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0096

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:52`
- Строки: `52--56`

```latex
\begin{equation}
 \rho_k
 =\frac{R_1}{R_3}
 \sqrt{(k+3/2)^2+(\chi R_3)^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0097

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:58`
- Строки: `58--63`

```latex
\begin{equation}
 \mathcal I_{\rho_k}(\beta)
 =\log
 \frac{\cosh(2\pi\rho_k)-\cos(2\pi\beta)}
 {\cosh(2\pi\rho_k)-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0098

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:67`
- Строки: `67--72`

```latex
\begin{equation}
 \Delta\Gamma_f(\beta)
 =-2\sum_{k=0}^{\infty}
 (k+1)(k+2)\,\mathcal I_{\rho_k}(\beta).
 \label{eq:fermion-spin-relative-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0099

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 \mathcal I_\rho(\beta)\ge0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0100

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:85`
- Строки: `85--87`

```latex
\begin{equation}
 \Delta\Gamma_f(1/2)<\Delta\Gamma_f(0)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0101

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 \Delta\Gamma_f(1/2)
 =-0.0001948280\ldots.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0102

- Источник: `s2t/gates/version4_spin_structure_relative_determinant_gate.tex:119`
- Строки: `119--121`

```latex
\begin{equation}
 \boxed{\beta_{S^1}=\frac12.}
\end{equation}
```

## `s2t/gates/version4_variational_family_state_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-08-0103

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:9`
- Строки: `9--11`

```latex
\begin{equation}
 R_{2n}(D)=\sum_{v=1}^{4}(D^{2n})_{vv}\in M_3(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0104

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 V_{2n}(D,\rho)=\Tr_{\rm fam}\bigl(\rho R_{2n}(D)\bigr).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0105

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:23`
- Строки: `23--36`

```latex
\begin{align}
 R_4^-&=
 \begin{pmatrix}
 27/2&0&1/2\\
 0&35/2&-7/2\\
 1/2&-7/2&17
 \end{pmatrix},\\
 R_4^+&=
 \begin{pmatrix}
 27/2&-2&3/2\\
 -2&35/2&-5/2\\
 3/2&-5/2&17
 \end{pmatrix}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0106

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 17-\frac{\sqrt{57}}2\approx13.225083>13.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0107

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 4x^3-192x^2+3003x-15358
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0108

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 12.5<\lambda_{\min}(R_4^+)<13,
 \qquad
 \lambda_{\min}(R_4^+)\approx12.608881.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0109

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:61`
- Строки: `61--63`

```latex
\begin{equation}
 (0.939575,\;0.310502,\;-0.144179)^T.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-08-0110

- Источник: `s2t/gates/version4_variational_family_state_gate.tex:67`
- Строки: `67--69`

```latex
\begin{equation}
 27.505248<32.742926.
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]