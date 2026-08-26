# Гейты Version 5, часть 6

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **114** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version5_boundary_parent_trace_freeze_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0001

- Источник: `s2t/gates/version5_boundary_parent_trace_freeze_gate.tex:23`
- Строки: `23--26`

```latex
\begin{equation}
 -\frac13\log Z_J
 =\frac8{1-\cos\theta}+\frac83\log(1-\cos\theta)+\text{пост.},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0002

- Источник: `s2t/gates/version5_boundary_parent_trace_freeze_gate.tex:42`
- Строки: `42--44`

```latex
\begin{equation}
 \mathcal A_\partial=\bigoplus_{a=1}^{k}M_{n_a}(\mathbb F_a).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0003

- Источник: `s2t/gates/version5_boundary_parent_trace_freeze_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
 \tau_\partial=\sum_{a=1}^{k}w_a\Tr_a,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0004

- Источник: `s2t/gates/version5_boundary_parent_trace_freeze_gate.tex:61`
- Строки: `61--65`

```latex
\begin{equation}
 P_q=\frac1{2\pi}\int_0^{2\pi}d\alpha\,
 e^{i\alpha(\widehat Q-q)},
 \qquad Z_q=\Tr(P_qe^{-\beta H}).
\end{equation}
```

## `s2t/gates/version5_carrier_measure_freeze_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0005

- Источник: `s2t/gates/version5_carrier_measure_freeze_gate.tex:12`
- Строки: `12--14`

```latex
\begin{equation}
 F=S_{\text{эфф}}-T_{\text{эфф}}S_{\text{инф}},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0006

- Источник: `s2t/gates/version5_carrier_measure_freeze_gate.tex:22`
- Строки: `22--26`

```latex
\begin{equation}
 H_C=-\tau^{-1}\log\widehat C,
 \qquad
 \rho_C=\frac{e^{-\tau H_C}}{\Tr e^{-\tau H_C}}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0007

- Источник: `s2t/gates/version5_carrier_measure_freeze_gate.tex:69`
- Строки: `69--72`

```latex
\begin{equation}
 \text{нормировка состояния: выполнена},\qquad
 \text{родительская мера: не получена}.
\end{equation}
```

## `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0008

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:15`
- Строки: `15--22`

```latex
\begin{equation}
 H_{\rm cl}=I,
 \qquad
 H_{\rm def}=\widehat T_+\widehat T_+^*=I-P_{\rm def},
 \qquad
 P_{\rm def}=|e_0\rangle\langle e_0|\otimes q_0.
 \label{eq:v5-closed-defect-hamiltonians}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0009

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:25`
- Строки: `25--29`

```latex
\begin{equation}
 e^{-tH_{\rm def}}-e^{-tH_{\rm cl}}
 =(1-e^{-t})P_{\rm def}.
 \label{eq:v5-finite-rank-heat-response}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0010

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:31`
- Строки: `31--37`

```latex
\begin{equation}
 K_{\rm def}(t)
 =\frac1{105}\Tr
 \left(e^{-tH_{\rm def}}-e^{-tH_{\rm cl}}\right)
 =\frac17(1-e^{-t}).
 \label{eq:v5-defect-heat-trace}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0011

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:50`
- Строки: `50--54`

```latex
\begin{equation}
 \Gamma_{\rm def}(m)
 =\int_0^\infty\frac{dt}{t}e^{-m^2t}K_{\rm def}(t).
 \label{eq:v5-defect-proper-time-response}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0012

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 \Gamma_{\rm def}(m)
 =\frac17\log\frac{m^2+1}{m^2}.
 \label{eq:v5-defect-relative-determinant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0013

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:73`
- Строки: `73--76`

```latex
\begin{equation}
 \Gamma_{\rm def}(m)\longrightarrow+\infty,
 \qquad m\to0,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0014

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 \Gamma_{\rm def}(m,a)
 =\frac17\log\left(1+\frac{a}{m^2}\right).
 \label{eq:v5-defect-response-general-gap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0015

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:104`
- Строки: `104--108`

```latex
\begin{equation}
 \frac{30}{210}
 \log\left(1+\frac{a}{m^2}\right)
 =\frac17\log\left(1+\frac{a}{m^2}\right).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0016

- Источник: `s2t/gates/version5_closure_deficit_induced_vacuum_response_gate.tex:134`
- Строки: `134--140`

```latex
\begin{equation}
 \text{ненулевой KO-класс}
 \Longrightarrow
 \text{неизбежный дефект}
 \Longrightarrow
 \text{конечный относительный отклик}.
\end{equation}
```

## `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0017

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:23`
- Строки: `23--28`

```latex
\begin{equation}
 V_{15}(z)=\left(
 zq_0+1-q_0,
 z^{-1}\overline q_0+1-\overline q_0
 \right)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0018

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:30`
- Строки: `30--35`

```latex
\begin{equation}
 \operatorname{wind}V_+=15,
 \qquad
 \operatorname{wind}V_-=-15.
 \label{eq:v5-real-pair-windings}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0019

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 \Tr\bigl((V^{-1}dV)^3\bigr)=0,
 \qquad \dim S^1=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0020

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:46`
- Строки: `46--48`

```latex
\begin{equation}
 \frac{1}{2\pi i}\int_{S^1}\Tr(V^{-1}dV)=\pm15.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0021

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:52`
- Строки: `52--57`

```latex
\begin{equation}
 \nu_3(W_+)=15,
 \qquad
 \nu_3(W_-)=-15.
 \label{eq:v5-bott-wzw-charges}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0022

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:60`
- Строки: `60--62`

```latex
\begin{equation}
 \nu_3(W_+)+\nu_3(W_-)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0023

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:68`
- Строки: `68--71`

```latex
\begin{equation}
 \exp\bigl(2\pi i k\nu_3(W_\pm)\bigr)=1.
 \label{eq:v5-integer-wzw-phase-trivial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0024

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:86`
- Строки: `86--89`

```latex
\begin{equation}
 \sigma_+=(-1)^{15}=-1.
 \label{eq:v5-reduced-pfaffian-parity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0025

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:101`
- Строки: `101--103`

```latex
\begin{equation}
 (-1)^{-15}=-1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0026

- Источник: `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex:106`
- Строки: `106--109`

```latex
\begin{equation}
 \sigma_{\rm full}=(-1)^{15}(-1)^{-15}=+1.
 \label{eq:v5-full-real-pfaffian-phase}
\end{equation}
```

## `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0027

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 g(z)=f(z^2)+z h(z^2).
 \label{eq:v5-fermionic-even-odd}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0028

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:22`
- Строки: `22--25`

```latex
\begin{equation}
 \tau_{
m w}=i\sigma_2J,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0029

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 (Y_eY_e^*),(LH)(LH)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0030

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:45`
- Строки: `45--48`

```latex
\begin{equation}
 g_\alpha(z)=z e^{-z^2}+\alpha e^{-z^2}.
 \label{eq:v5-fermionic-function-counterfamily}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0031

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
 \frac{g_\alpha(z)-g_\alpha(-z)}2=z e^{-z^2},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0032

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 \frac{g_\alpha(z)+g_\alpha(-z)}2=\alpha e^{-z^2}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0033

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:75`
- Строки: `75--77`

```latex
\begin{equation}
 K_e=Y_eY_e^*.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0034

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:80`
- Строки: `80--85`

```latex
\begin{equation}
 P_0K_eP_0=\kappa_eP_0,
 \qquad
 \kappa_e=\langle v_0,K_ev_0\rangle.
 \label{eq:v5-charged-lepton-compression}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0035

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:88`
- Строки: `88--90`

```latex
\begin{equation}
 \kappa_e=\frac{d_1+d_2+d_3}{3}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0036

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:103`
- Строки: `103--109`

```latex
\begin{equation}
 S_0=w_0\left[
 Z_\psi\,\overline\psi D\psi
 +\mu\,\psi^TC\psi
 \right].
 \label{eq:v5-common-weight-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0037

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:111`
- Строки: `111--113`

```latex
\begin{equation}
 \psi_c=\sqrt{w_0Z_\psi}\,\psi
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0038

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:115`
- Строки: `115--117`

```latex
\begin{equation}
 m_{\rm phys}=\frac{\mu}{Z_\psi}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0039

- Источник: `s2t/gates/version5_h15_fermionic_spectral_weinberg_measure_gate.tex:130`
- Строки: `130--134`

```latex
\begin{equation}
 m_{\nu,0}\sim
 r_\tau\,\kappa_e\,\frac{v_H^2}{\Lambda},
 \label{eq:v5-weinberg-residual-amplitude}
\end{equation}
```

## `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0040

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 \widehat p_i=p_i\oplus Jp_iJ^{-1}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0041

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:17`
- Строки: `17--23`

```latex
\begin{equation}
 \widehat p_i^2=\widehat p_i,
 \qquad \widehat p_i\widehat p_j=0\quad(i\ne j),
 \qquad \widehat p_L+\widehat p_G+\widehat p_R=I_{18},
 \qquad \rank\widehat p_i=6.
 \label{eq:v5-commutant-vertex-projectors}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0042

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:25`
- Строки: `25--30`

```latex
\begin{equation}
 [\widehat p_i,\pi(a)]=0,
 \qquad
 [\widehat p_i,J\pi(a)J^{-1}]=0
 \label{eq:v5-commutant-double-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0043

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:34`
- Строки: `34--38`

```latex
\begin{equation}
 \mathcal C_{\mathrm{vert}}
 =\operatorname{span}\{\widehat p_L,\widehat p_G,\widehat p_R\}
 \simeq\mathbb C^3
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0044

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:45`
- Строки: `45--47`

```latex
\begin{equation}
 \mathcal C_{\mathrm{mod}}=C^*(L_{\mathrm{fam}})\simeq\mathbb C^3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0045

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 \iota:\mathcal C_{\mathrm{mod}}
 \longrightarrow\mathcal C_{\mathrm{vert}}
 \label{eq:v5-commutant-iota}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0046

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 (0,1,2)\longmapsto(L,G,R),
 \qquad
 (0,1,2)\longmapsto(R,G,L).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0047

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:64`
- Строки: `64--68`

```latex
\begin{equation}
 (-1,0,+1),
 \qquad
 (+1,0,-1)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0048

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:84`
- Строки: `84--88`

```latex
\begin{equation}
 h_p=-p_L+p_R,
 \qquad
 h_F=h_p\oplus(-h_p).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0049

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:90`
- Строки: `90--96`

```latex
\begin{equation}
 Jh_FJ^{-1}=-h_F,
 \qquad
 [h_F,\Gamma_F]=0,
 \qquad
 [h_F,\pi(a)]=[h_F,J\pi(a)J^{-1}]=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0050

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:100`
- Строки: `100--102`

```latex
\begin{equation}
 \mathcal B_{\mathrm{par}}=M_{18}(\mathbb C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0051

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:104`
- Строки: `104--108`

```latex
\begin{equation}
 \rho_\beta
 =\frac{e^{-\beta h_F}}{\Tr e^{-\beta h_F}}.
 \label{eq:v5-commutant-rho}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0052

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:117`
- Строки: `117--122`

```latex
\begin{equation}
 \Delta_\rho(A)=\rho_\beta A\rho_\beta^{-1},
 \qquad
 K_{\text{мод}}=-\log\Delta_\rho
 =\beta\operatorname{ad}_{h_F}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0053

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:126`
- Строки: `126--131`

```latex
\begin{equation}
 d:=\Pi_{+1}(D_F),
 \qquad
 D_F=d+d^\dagger.
 \label{eq:v5-commutant-modular-d}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0054

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:133`
- Строки: `133--135`

```latex
\begin{equation}
 JdJ^{-1}=d^\dagger.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0055

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:152`
- Строки: `152--155`

```latex
\begin{equation}
 [d,d^\dagger]\big|_{V_G}
 =XX^\dagger-Y^\dagger Y.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0056

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:157`
- Строки: `157--159`

```latex
\begin{equation}
 \tau_{18}(A)=\frac1{18}\Tr_{18}A.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0057

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:161`
- Строки: `161--167`

```latex
\begin{equation}
 \frac16\Tr_{18}\!\left(
 \widehat p_G[d,d^\dagger]^2
 \right)
 =\tau_3(XX^\dagger-Y^\dagger Y)^2.
 \label{eq:v5-commutant-trace-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0058

- Источник: `s2t/gates/version5_modular_commutant_parent_correspondence_gate.tex:188`
- Строки: `188--192`

```latex
\begin{equation}
 \boxed{
 M_{18}(\mathbb C),\ \rho_\beta,\ \tau_{18},\ J,\ \Gamma_F,\ D_F
 }
\end{equation}
```

## `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0059

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:15`
- Строки: `15--22`

```latex
\begin{equation}
 H=H_p\oplus H_p^c,
 \qquad
 \gamma=\gamma_p\oplus(-\gamma_p),
 \qquad
 J(\xi,\eta)=(\overline\eta,\overline\xi).
 \label{eq:v5-retro-universal-ko6-doubling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0060

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:34`
- Строки: `34--37`

```latex
\begin{equation}
 JdJ^{-1}=d^\dagger.
 \label{eq:v5-retro-j-d-exchange}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0061

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 T_+=S\otimes q_0,
 \qquad
 T_-=S^*\otimes\overline{q_0}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0062

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:58`
- Строки: `58--63`

```latex
\begin{equation}
 \text{сокращение полного следа или Pfaffian-фазы}
 \ne
 \text{вычисление класса в }KO_6.
 \label{eq:v5-retro-trace-not-kclass}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0063

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:74`
- Строки: `74--78`

```latex
\begin{equation}
 c_1(L)=+1,
 \qquad
 c_1(L^*)=-1,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0064

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:113`
- Строки: `113--118`

```latex
\begin{equation}
 KO_6(\mathbb C_{\mathbb R})
 \longrightarrow
 K_0(\mathbb C\oplus\mathbb C)
 \label{eq:v5-retro-real-complex-comparison}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0065

- Источник: `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex:123`
- Строки: `123--127`

```latex
\begin{equation}
 1\longmapsto(-1,+1)
 \quad\text{с точностью до общего знака}.
 \label{eq:v5-retro-required-antidiagonal}
\end{equation}
```

## `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0066

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:30`
- Строки: `30--35`

```latex
\begin{equation}
 \psi_\lambda(r)=\lambda^2\psi(\lambda r),\qquad
 \Phi_\lambda(r)=\lambda^2\Phi(\lambda r),\qquad
 \epsilon_\lambda=\lambda^2\epsilon.
 \label{eq:v5-sn-scaling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0067

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 d\tau=N(q)\,dt.
 \label{eq:v5-lapse-definition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0068

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:60`
- Строки: `60--63`

```latex
\begin{equation}
 N(q_*)=\frac14.
 \label{eq:v5-quarter-lapse}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0069

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:67`
- Строки: `67--71`

```latex
\begin{equation}
 \Gamma_{\rm ext}=N(q_*)\Gamma_{\rm int},\qquad
 T_{\rm ext}=\frac{1}{N(q_*)\Gamma_{\rm int}}.
 \label{eq:v5-external-lifetime}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0070

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:80`
- Строки: `80--83`

```latex
\begin{equation}
 \mathcal F(q;E)=V(q)+E N(q),
 \label{eq:v5-time-well-functional}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0071

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:87`
- Строки: `87--92`

```latex
\begin{equation}
 V'(q_*)+E N'(q_*)=0,
 \qquad
 V''(q_*)+E N''(q_*)>0.
 \label{eq:v5-time-well-stability}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0072

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:96`
- Строки: `96--101`

```latex
\begin{equation}
 N(q)=\frac14 e^{-a x},\qquad
 V(q)=\frac{Ea}{4}x+\frac{\kappa}{2}x^2+
       \frac{\lambda}{4}x^4,qquad \lambda>0.
 \label{eq:v5-same-lapse-family}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0073

- Источник: `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex:103`
- Строки: `103--106`

```latex
\begin{equation}
 \mathcal F''(q_*)=\kappa+\frac{Ea^2}{4}
 \label{eq:v5-same-lapse-hessian}
\end{equation}
```

## `s2t/gates/version5_self_generated_transition_defect_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0074

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:33`
- Строки: `33--39`

```latex
\begin{equation}
 S_q=\int dt\,dx\left[
 \frac12(\partial_tq)^2-\frac12(\partial_xq)^2
 -\frac14(q^2-1)^2
 \right].
 \label{eq:v5-self-defect-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0075

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:41`
- Строки: `41--44`

```latex
\begin{equation}
 \partial_t^2q-\partial_x^2q+q(q^2-1)=0.
 \label{eq:v5-self-defect-eom}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0076

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:47`
- Строки: `47--52`

```latex
\begin{equation}
 q(-\infty)=-1,
 \qquad
 q(+\infty)=+1
 \label{eq:v5-self-defect-boundary}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0077

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 q_*(x)=\tanh\frac{x-X}{\sqrt2}.
 \label{eq:v5-self-defect-kink}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0078

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:62`
- Строки: `62--67`

```latex
\begin{equation}
 E_{\rm kink}=\int dx\left[
 \frac12(q_*')^2+\frac14(q_*^2-1)^2
 \right]=\frac{2\sqrt2}{3}.
 \label{eq:v5-self-defect-energy}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0079

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:69`
- Строки: `69--72`

```latex
\begin{equation}
 Q=\frac{q(+\infty)-q(-\infty)}2=1
 \label{eq:v5-self-defect-charge}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0080

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:79`
- Строки: `79--82`

```latex
\begin{equation}
 \partial_s q=\partial_x^2q-q(q^2-1)
 \label{eq:v5-self-defect-gradient-flow}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0081

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:96`
- Строки: `96--104`

```latex
\begin{equation}
 q_v(x,t)=
 \tanh\!\left(
 \frac{\gamma(x-vt-X)}{\sqrt2}
 \right),
 \qquad
 \gamma=(1-v^2)^{-1/2},
 \label{eq:v5-self-defect-moving}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0082

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:116`
- Строки: `116--119`

```latex
\begin{equation}
 H_q=-i\sigma_2\partial_x+gq(x)\sigma_1.
 \label{eq:v5-self-defect-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0083

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:121`
- Строки: `121--128`

```latex
\begin{equation}
 \psi_0(x)=\mathcal N
 \begin{pmatrix}
 \cosh^{-g\sqrt2}(x/\sqrt2)\\0
 \end{pmatrix},
 \qquad H_{q_*}\psi_0=0.
 \label{eq:v5-self-defect-zero-mode}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0084

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:133`
- Строки: `133--136`

```latex
\begin{equation}
 \mathbb C^2\otimes E,
 \qquad E=M_{20\times15}(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0085

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:139`
- Строки: `139--141`

```latex
\begin{equation}
 \dim_{\mathbb C}E=300
 \end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0086

- Источник: `s2t/gates/version5_self_generated_transition_defect_gate.tex:156`
- Строки: `156--161`

```latex
\begin{equation}
 V(q)=\frac\lambda4(q^2-v_q^2)^2,
 \qquad
 H_q=-i\sigma_2\partial_x+yq\sigma_1.
 \label{eq:v5-self-defect-dimensional-data}
\end{equation}
```

## `s2t/gates/version5_sm_family_commutant_calculus_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0087

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:6`
- Строки: `6--10`

```latex
\begin{equation}
 \mathcal A_{\mathrm{coord}}=\mathcal A_{\mathrm{SM}}
 =\mathbb C\oplus\mathbb H\oplus M_3(\mathbb C),
 \label{eq:v5-sm-coordinate-algebra}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0088

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 H_p=K_{\mathrm{fam}}\otimes H_{\mathrm{SM}}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0089

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:31`
- Строки: `31--37`

```latex
\begin{equation}
 \pi(a)=I_{10}\otimes\pi_{\mathrm{SM}}(a),
 \qquad
 D=D_{\mathrm{fam}}\otimes I_{15}
   +I_{10}\otimes D_{\mathrm{SM}}.
 \label{eq:v5-sm-family-product}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0090

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 2\cdot10\cdot15=300.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0091

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:43`
- Строки: `43--46`

```latex
\begin{equation}
 [D_{\mathrm{fam}}\otimes I_{15},\pi(a)]=0.
 \label{eq:v5-family-in-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0092

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:49`
- Строки: `49--51`

```latex
\begin{equation}
 \mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak u(1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0093

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:59`
- Строки: `59--63`

```latex
\begin{equation}
 [D,\pi(a)]
 =I_{10}\otimes[D_{\mathrm{SM}},\pi_{\mathrm{SM}}(a)].
 \label{eq:v5-one-form-blindness}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0094

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:65`
- Строки: `65--68`

```latex
\begin{equation}
 \Omega_D^1(\mathcal A_{\mathrm{SM}})
 =\left\{\sum_j\pi(a_j)[D,\pi(b_j)]\right\}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0095

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:95`
- Строки: `95--97`

```latex
\begin{equation}
 \mathcal A_{\mathrm{SM}}\oplus\mathcal A_{\mathrm{fam}}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0096

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:107`
- Строки: `107--110`

```latex
\begin{equation}
 M_3(\mathbb R)\otimes_{\mathbb R}M_3(\mathbb C)
 \simeq M_9(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0097

- Источник: `s2t/gates/version5_sm_family_commutant_calculus_gate.tex:137`
- Строки: `137--142`

```latex
\begin{equation}
 \nabla_{\mathrm{fam}}:
 K_{\mathrm{fam}}\longrightarrow
 K_{\mathrm{fam}}\widehat\otimes_{\mathcal A_{\mathrm{SM}}}
 \Omega^1(\mathcal A_{\mathrm{SM}}),
\end{equation}
```

## `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex`

### LIVE-FORMULAS-GATES-VERSION5-06-0098

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:17`
- Строки: `17--21`

```latex
\begin{equation}
 \mathcal L(E)=
 \begin{pmatrix}M_{20}&E\\E^*&M_{15}\end{pmatrix}
 \simeq M_{35}(\mathbb C)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0099

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:28`
- Строки: `28--32`

```latex
\begin{equation}
 [f(x)I_{35},X]=0,
 \qquad X\in M_{35}(\mathbb C).
 \label{eq:v5-spatial-trace-no-derivative}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0100

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 \text{совместимость с пространственным исчислением}
 \neq
 \text{вывод исчисления из }M_{35}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0101

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:50`
- Строки: `50--52`

```latex
\begin{equation}
 \dim\mathfrak u(35)=1225.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0102

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
 \dim\bigl(\mathfrak u(20)\oplus\mathfrak u(15)\bigr)=625.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0103

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 c_1(L)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0104

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:80`
- Строки: `80--82`

```latex
\begin{equation}
 H^2(B^3,\mathbb Z)=0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0105

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:91`
- Строки: `91--95`

```latex
\begin{equation}
 L\oplus L^*,
 \qquad c_1(L\oplus L^*)=0,
 \label{eq:v5-hopf-pair-trivial-total-chern}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0106

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:106`
- Строки: `106--108`

```latex
\begin{equation}
 \mathbf1\oplus\mathbf3\oplus\mathbf3\oplus\mathbf3,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0107

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:111`
- Строки: `111--114`

```latex
\begin{equation}
 c_1=2j.
 \label{eq:v5-spin-j-chern}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0108

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:116`
- Строки: `116--118`

```latex
\begin{equation}
 (0,2,2,2).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0109

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:141`
- Строки: `141--143`

```latex
\begin{equation}
 \mathbb A=\nabla_A+\Phi
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0110

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:145`
- Строки: `145--147`

```latex
\begin{equation}
 \mathbb F=F_A+D_A\Phi+\Phi^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0111

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:154`
- Строки: `154--156`

```latex
\begin{equation}
 \Phi\longmapsto a\Phi
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0112

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:158`
- Строки: `158--161`

```latex
\begin{equation}
 |F_A|^2+2a^2|D_A\Phi|^2+a^4|\Phi|^4+\cdots.
 \label{eq:v5-superconnection-rescaling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0113

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:184`
- Строки: `184--188`

```latex
\begin{equation}
 \text{локальная }SO(3)\text{-кинематика существует},
 \qquad
 \text{родительская динамика не выведена}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION5-06-0114

- Источник: `s2t/gates/version5_spatial_so3_superconnection_parent_trace_gate.tex:193`
- Строки: `193--201`

```latex
\begin{equation}
 \boxed{
 \begin{gathered}
 \text{граничная хопфова ориентация: выведена},\\
 \text{суперсвязностная упаковка после задания полей: допустима},\\
 \text{пространственное исчисление и }SO(3)\text{-вложение: не выведены},\\
 \text{гладкий единично-индексный дублет в }M_{35}:\text{ отсутствует}.
 \end{gathered}}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]