# Гейты Version 4, часть 4

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **109** блочных формул из **11** файлов.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version4_common_updown_krajewski_loop_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0001

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 A=(L_0,R_0),\quad B=(L_0,R_1),\quad
 C=(L_1,R_1),\quad D=(L_1,R_0).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0002

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:22`
- Строки: `22--30`

```latex
\begin{equation}
 AB:P_-,
 \qquad
 BC:H_u,
 \qquad
 CD:H_d,
 \qquad
 DA:e^{i\theta}I_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0003

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:39`
- Строки: `39--43`

```latex
\begin{equation}
 \Tr D_F^4
 =
 104+16\cos\theta\,\Tr(P_-H_uH_d).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0004

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:48`
- Строки: `48--52`

```latex
\begin{align}
 W=-\frac12:&\quad \Tr D_F^4=104-8\cos\theta,\\
 W=0:&\quad \Tr D_F^4=104,\\
 W=+\frac12:&\quad \Tr D_F^4=104+8\cos\theta.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0005

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:54`
- Строки: `54--59`

```latex
\begin{equation}
 (W,\theta)=
 \left(-\frac12,0\right)
 \quad\text{или}\quad
 \left(+\frac12,\pi\right),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0006

- Источник: `s2t/gates/version4_common_updown_krajewski_loop_gate.tex:74`
- Строки: `74--76`

```latex
\begin{equation}
 (W,\theta)\longmapsto(-W,\theta+\pi)
\end{equation}
```

## `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0007

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:4`
- Строки: `4--6`

```latex
\begin{equation}
 \left(|\Phi|^2-\frac13\Tr X^TX\right)^2,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0008

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:15`
- Строки: `15--18`

```latex
\begin{equation}
 V_L\xrightarrow{\ X\ }V_G\xrightarrow{\ Y\ }V_R.
 \label{eq:family-moment-map-quiver}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0009

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:27`
- Строки: `27--29`

```latex
\begin{equation}
 \dim_{\mathbb R}\operatorname{End}_{A_4}(\mathbb R^3)=1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0010

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:31`
- Строки: `31--34`

```latex
\begin{equation}
 Y=\Phi I_3.
 \label{eq:a4-schur-pairing-connector}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0011

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:42`
- Строки: `42--48`

```latex
\begin{equation}
 \mu_G
 =[d,d^\dagger]\big|_{V_G}
 =XX^T-Y^\dagger Y
 =XX^T-|\Phi|^2I_3.
 \label{eq:middle-quiver-moment-map}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0012

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:51`
- Строки: `51--56`

```latex
\begin{equation}
 S_\mu=\tau_3(\mu_G^2),
 \qquad
 \tau_3(M)=\frac13\Tr M.
 \label{eq:normalized-middle-moment-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0013

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:70`
- Строки: `70--76`

```latex
\begin{equation}
 G=XX^T,
 \qquad
 \bar g=\tau_3(G),
 \qquad
 G_0=G-\bar gI_3.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0014

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:78`
- Строки: `78--84`

```latex
\begin{equation}
 \boxed{
 \tau_3(\mu_G^2)
 =\left(|\Phi|^2-\frac13\Tr XX^T\right)^2
 +\frac13\Tr G_0^2.}
 \label{eq:moment-map-central-shape-decomposition}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0015

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:89`
- Строки: `89--95`

```latex
\begin{equation}
 |\Phi|^4:
 |\Phi|^2\Tr XX^T:
 (\Tr XX^T)^2
 =1:-\frac23:\frac19.
 \label{eq:derived-pairing-ratio}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0016

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:111`
- Строки: `111--115`

```latex
\begin{equation}
 V_{\rm lock}
 =\frac14\|X^TX-I_3\|_F^2
 +\frac14(\det X-1)^2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0017

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:117`
- Строки: `117--121`

```latex
\begin{equation}
 X_\star=I_3,
 \qquad
 |\Phi_\star|=1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0018

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:123`
- Строки: `123--125`

```latex
\begin{equation}
 (7_+,4_0,0_-).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0019

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:134`
- Строки: `134--138`

```latex
\begin{equation}
 X=\rho I_3,
 \qquad
 \Phi=r e^{i\varphi},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0020

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:140`
- Строки: `140--145`

```latex
\begin{equation}
 V_{\rm rad}(\rho,r)
 =V_{\rm lock}(\rho I_3)
 +(\rho^2-r^2)^2+r^2.
 \label{eq:joint-moment-map-defect-radial}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0021

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:147`
- Строки: `147--153`

```latex
\begin{equation}
 \rho_\star=0.7432242844,
 \qquad
 r_\star=0.2288718801,
 \qquad
 V_\star=0.5395181198.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0022

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:155`
- Строки: `155--161`

```latex
\begin{equation}
 r=0,
 \qquad
 \rho=0.72442382,
 \qquad
 V_{\rm normal}=0.5408201282.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0023

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:163`
- Строки: `163--165`

```latex
\begin{equation}
 \Delta V=0.0013020084.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0024

- Источник: `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex:167`
- Строки: `167--171`

```latex
\begin{equation}
 0.19471629,
 \qquad
 8.67361589,
\end{equation}
```

## `s2t/gates/version4_hessian_principle_sign_trilemma.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0025

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:11`
- Строки: `11--15`

```latex
\begin{equation}
 D_{\rm KL}(\varepsilon\|0)
 =\frac{\varepsilon^2}{4}\Tr A^2+O(\varepsilon^3).
 \label{eq:gaussian-kl-positive-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0026

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:22`
- Строки: `22--25`

```latex
\begin{equation}
 [\varepsilon^2]D_{\rm KL}
 =+\frac{1-c}{45},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0027

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:29`
- Строки: `29--31`

```latex
\begin{equation}
 \Gamma(\varepsilon)=\frac12\log\det K_\varepsilon
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0028

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:33`
- Строки: `33--37`

```latex
\begin{equation}
 [\varepsilon^2]\Gamma
 =-\frac14\Tr A^2
 =-\frac{1-c}{45},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0029

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:39`
- Строки: `39--42`

```latex
\begin{equation}
 [\varepsilon^4]\Gamma
 =-\frac{(1-c)^2}{4725}\ne0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0030

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:80`
- Строки: `80--84`

```latex
\begin{equation}
 F''(0)=-\chi,
 \qquad
 \chi\ge0.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0031

- Источник: `s2t/gates/version4_hessian_principle_sign_trilemma.tex:92`
- Строки: `92--96`

```latex
\begin{equation}
 \left.\frac12\frac{d^2}{d\varepsilon^2}
 \log\det K_\varepsilon\right|_{\varepsilon=0}
 =-\frac{1-c}{45}
\end{equation}
```

## `s2t/gates/version4_hessian_two_scale_messenger_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0032

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:6`
- Строки: `6--8`

```latex
\begin{equation}
 m_\sigma^2:m_\theta^2=104:8=13:1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0033

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:10`
- Строки: `10--12`

```latex
\begin{equation}
 \frac{M_\sigma}{M_\theta}=\sqrt{13}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0034

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:17`
- Строки: `17--25`

```latex
\begin{equation}
 \mathcal M(t)=
 \begin{pmatrix}
 t m_1 I&iI\\
 -iI&t m_2 I
 \end{pmatrix},
 \qquad
 \{m_1,m_2\}=\{\sqrt{13},1\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0035

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:41`
- Строки: `41--43`

```latex
\begin{equation}
 t=147.0565.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0036

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:45`
- Строки: `45--48`

```latex
\begin{align}
 u&=(0.00054008,\,0.00231337,\,1),\\
 d&=(0.00101118,\,0.00182242,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0037

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:56`
- Строки: `56--63`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.97176&0.23596&0.000345\\
 0.23596&0.97176&0.000272\\
 0.000271&0.000345&1
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0038

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:65`
- Строки: `65--69`

```latex
\begin{equation}
 s_{12}=0.23596,
 \qquad
 \frac{s_{12}}{s_{12}^{\rm CKM}}=1.0487.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0039

- Источник: `s2t/gates/version4_hessian_two_scale_messenger_gate.tex:74`
- Строки: `74--80`

```latex
\begin{equation}
 s_{23}=2.72\times10^{-4},
 \qquad
 s_{13}=3.45\times10^{-4},
 \qquad
 |J_q|=9.84\times10^{-11},
\end{equation}
```

## `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0040

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:11`
- Строки: `11--13`

```latex
\begin{equation}
 \widehat R_s=\frac{3R_{4,s}}{\Tr R_{4,s}},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0041

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:15`
- Строки: `15--17`

```latex
\begin{equation}
 \rho_s=\frac{e^{-\widehat R_s}}{\Tr e^{-\widehat R_s}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0042

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:22`
- Строки: `22--25`

```latex
\begin{align}
 \Spec\rho_u&=(0.2184,\,0.3602,\,0.4214),\\
 \Spec\rho_d&=(0.2169,\,0.3620,\,0.4210).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0043

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:32`
- Строки: `32--36`

```latex
\begin{align}
 L_s^{L}&=(S_sA_s,S_sB_s),\\
 L_s^{R}&=(A_sS_s,B_sS_s),\\
 L_s^{KMS}&=(S_sA_sS_s,S_sB_sS_s).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0044

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:39`
- Строки: `39--41`

```latex
\begin{equation}
 L_s^L(L_s^L)^\dagger=2\rho_s,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0045

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:56`
- Строки: `56--60`

```latex
\begin{equation}
 (\epsilon_{00},\epsilon_{01},\epsilon_{10},\epsilon_{11})
 =(-1,-1,-1,-1),
 \qquad t=205.3797.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0046

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:62`
- Строки: `62--65`

```latex
\begin{align}
 u&=(0.00111544,\,0.00137766,\,1),\\
 d&=(0.00112270,\,0.00133565,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0047

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:73`
- Строки: `73--80`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.98988&0.14187&0.000320\\
 0.14187&0.98988&0.0000747\\
 0.000327&0.0000304&1
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0048

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:82`
- Строки: `82--84`

```latex
\begin{equation}
 s_{12}=0.1419\simeq0.63\,s_{12}^{\rm CKM}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0049

- Источник: `s2t/gates/version4_modular_endpoint_intertwiner_gate.tex:87`
- Строки: `87--89`

```latex
\begin{equation}
 |J_q|\simeq5.98\times10^{-10}
\end{equation}
```

## `s2t/gates/version4_pati_salam_associative_node_no_go.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0050

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:28`
- Строки: `28--30`

```latex
\begin{equation}
 \Lambda^2(gh)=\Lambda^2(g)\Lambda^2(h).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0051

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:32`
- Строки: `32--35`

```latex
\begin{equation}
 d\Lambda^2([X,Y])
 =[d\Lambda^2(X),d\Lambda^2(Y)].
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0052

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:40`
- Строки: `40--44`

```latex
\begin{equation}
 \Lambda^2(A+B)\ne\Lambda^2A+\Lambda^2B,
 \qquad
 \Lambda^2(\lambda I_4)=\lambda^2I_6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0053

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:46`
- Строки: `46--50`

```latex
\begin{equation}
 d\Lambda^2(I_4)=2I_6,
 \qquad
 d\Lambda^2(AB)\ne d\Lambda^2(A)d\Lambda^2(B).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0054

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:58`
- Строки: `58--62`

```latex
\begin{equation}
 \|\Lambda^2(2I_4)-2I_6\|_F=2\sqrt6,
 \qquad
 \|d\Lambda^2(I_4)-I_6\|_F=\sqrt6.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0055

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
 \mathcal A_F^{PS}
 =\mathbb H_R\oplus\mathbb H_L\oplus M_4(\mathbb C).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0056

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 2,\qquad2,\qquad4.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0057

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:79`
- Строки: `79--81`

```latex
\begin{equation}
 \mathbb C\longrightarrow(2,4)\longrightarrow(1,6)
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0058

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:92`
- Строки: `92--95`

```latex
\begin{equation}
 \operatorname{Hom}((2,4),(1,6))
 \cong(2,4)\oplus(2,\overline{20}).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0059

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:97`
- Строки: `97--99`

```latex
\begin{equation}
 \Delta\longmapsto B_\Delta
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0060

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:108`
- Строки: `108--110`

```latex
\begin{equation}
 \mathcal H_F=V_R\oplus V_L\oplus V_R^c\oplus V_L^c
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0061

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:112`
- Строки: `112--115`

```latex
\begin{equation}
 \operatorname{Sym}^2(2_R\otimes4_4)
 =(3_R,10_4)\oplus(1_R,6_4),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0062

- Источник: `s2t/gates/version4_pati_salam_associative_node_no_go.tex:118`
- Строки: `118--121`

```latex
\begin{equation}
 \Omega^2_{D_F}(\mathcal A_F)
 =\pi_D(\Omega^2\mathcal A_F)/\pi_D(J^2)
\end{equation}
```

## `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0063

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:13`
- Строки: `13--20`

```latex
\begin{equation}
 \mathbb C
 \xrightarrow{\ A_\Delta\ }
 \mathbb C^2\otimes\mathbb C^4
 \xrightarrow{\ B_\Delta\ }
 \Lambda^2\mathbb C^2\otimes\Lambda^2\mathbb C^4.
 \label{eq:ps-three-node-chain}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0064

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 A_\Delta(1)=\operatorname{vec}\Delta.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0065

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:34`
- Строки: `34--42`

```latex
\begin{equation}
 (B_\Delta x)_{IJ}
 =\frac{c}{2}\left(
 \Delta_{0I}x_{1J}-\Delta_{1I}x_{0J}
 -\Delta_{0J}x_{1I}+\Delta_{1J}x_{0I}
 \right),
 \qquad I<J.
 \label{eq:ps-second-wedge-edge}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0066

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:46`
- Строки: `46--52`

```latex
\begin{equation}
 \boxed{B_\Delta A_\Delta=c\,\Lambda^2\Delta},
 \qquad
 \|\Lambda^2\Delta\|^2
 =\det(\Delta\Delta^\dagger).
 \label{eq:ps-three-node-minor-identity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0067

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:57`
- Строки: `57--65`

```latex
\begin{equation}
 D_\Delta=
 \begin{pmatrix}
 0&A_\Delta^\dagger&0\\
 A_\Delta&0&B_\Delta^\dagger\\
 0&B_\Delta&0
 \end{pmatrix}.
 \label{eq:ps-three-node-dirac}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0068

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:67`
- Строки: `67--71`

```latex
\begin{equation}
 \rho=\Tr(\Delta\Delta^\dagger),\qquad
 \tau=\Tr[(\Delta\Delta^\dagger)^2],\qquad
 d=\det(\Delta\Delta^\dagger).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0069

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:73`
- Строки: `73--82`

```latex
\begin{align}
 \Tr D_\Delta^2
 &=\left(2+\frac32c^2\right)\rho,\\
 \Tr D_\Delta^4
 &=2\rho^2+c^4\left(\frac38\tau+\frac14d\right)
   +4c^2d\\
 &=\left(2+\frac38c^4\right)\rho^2
   +\left(4c^2-\frac12c^4\right)d.
 \label{eq:ps-three-node-traces}
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0070

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:86`
- Строки: `86--89`

```latex
\begin{equation}
 \boxed{0<c^2<8.}
 \label{eq:ps-three-node-stability-window}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0071

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:92`
- Строки: `92--97`

```latex
\begin{equation}
 \frac12\Tr D_F^2=\frac72\rho,
 \qquad
 \frac12\Tr D_F^4=\frac{19}{8}\rho^2+\frac72d.
 \label{eq:ps-three-node-canonical-traces}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0072

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:104`
- Строки: `104--108`

```latex
\begin{equation}
 V=-\frac12\Tr D_F^2+\frac12\Tr D_F^4
 =-\frac72\rho+\frac{19}{8}\rho^2+\frac72d
 \label{eq:ps-three-node-potential}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0073

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:110`
- Строки: `110--114`

```latex
\begin{equation}
 \rho_*=\frac{14}{19},
 \qquad
 V_*=-\frac{49}{38}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0074

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:116`
- Строки: `116--120`

```latex
\begin{equation}
 p=q=\frac7{26},
 \qquad
 V_{(2)}=-\frac{49}{52}>V_*.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0075

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:122`
- Строки: `122--128`

```latex
\begin{equation}
 \boxed{
 14\ (1),\qquad
 0\ (9),\qquad
 \frac{98}{19}\ (6).}
 \label{eq:ps-three-node-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0076

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:138`
- Строки: `138--143`

```latex
\begin{equation}
 D_F=D_F^\dagger,\qquad
 \{D_F,\Gamma_F\}=0,\qquad
 [D_F,J_F]=0,\qquad
 \{J_F,\Gamma_F\}=0
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0077

- Источник: `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex:147`
- Строки: `147--149`

```latex
\begin{equation}
 (0,0)\longrightarrow(0,1)\longrightarrow(1,1),
\end{equation}
```

## `s2t/gates/version4_pfaffian_stiffness_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0078

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:11`
- Строки: `11--14`

```latex
\begin{equation}
 |\operatorname{Pf}\mathcal A_{\rm red}(\theta)|^2
 =\frac{5+4\cos\theta}{4}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0079

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:16`
- Строки: `16--19`

```latex
\begin{equation}
 \Gamma_{\rm red}(\theta)
 =-\frac12\log\frac{5+4\cos\theta}{9},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0080

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:21`
- Строки: `21--23`

```latex
\begin{equation}
 \Gamma_{\rm red}''(0)=\frac29.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0081

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:25`
- Строки: `25--27`

```latex
\begin{equation}
 g_{\rm red}=\frac92>g_c.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0082

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:29`
- Строки: `29--31`

```latex
\begin{equation}
 g_{\rm full}=\frac94>g_c.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0083

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:48`
- Строки: `48--50`

```latex
\begin{equation}
 H_s(\theta)=Z_s-\sin\theta\,K_s.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0084

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:52`
- Строки: `52--55`

```latex
\begin{equation}
 \Phi_{\rm Pf}(\theta)=\Gamma_{\rm Pf}(\theta)
 -\frac14\sum_s\log\Tr e^{-H_s(\theta)}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0085

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:61`
- Строки: `61--66`

```latex
\begin{align}
 \theta_{\rm red}^\star&=\pm1.08516,
 &|\sin\theta_{\rm red}^\star|&=0.88438,\\
 \theta_{\rm full}^\star&=\pm0.69762,
 &|\sin\theta_{\rm full}^\star|&=0.64240.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0086

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:72`
- Строки: `72--74`

```latex
\begin{equation}
 t=485.5962,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0087

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:76`
- Строки: `76--81`

```latex
\begin{equation}
 s_{12}=0.98368,
 \quad s_{23}=8.45\times10^{-4},
 \quad s_{13}=7.80\times10^{-4},
 \quad |J_q|=7.34\times10^{-8}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0088

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:84`
- Строки: `84--86`

```latex
\begin{equation}
 t=1.00241,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0089

- Источник: `s2t/gates/version4_pfaffian_stiffness_gate.tex:88`
- Строки: `88--91`

```latex
\begin{equation}
 (s_{12},s_{23},s_{13})=(0.4867,\,0.4249,\,0.2650),
 \qquad |J_q|=0.0299.
\end{equation}
```

## `s2t/gates/version4_three_moment_oriented_messenger_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0090

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:12`
- Строки: `12--16`

```latex
\begin{equation}
 Z_{2n,s}=\frac{R_{2n,s}-\frac13\Tr(R_{2n,s})I}
 {\sqrt{\frac13\Tr\left(R_{2n,s}-\frac13\Tr(R_{2n,s})I\right)^2}},
 \qquad 2n\in\{4,6,8\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0091

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:18`
- Строки: `18--26`

```latex
\begin{equation}
 G=\frac14\sum_s\left(\frac13\Tr(Z_{2m,s}Z_{2n,s})\right)_{m,n}
 \simeq
 \begin{pmatrix}
 1&0.986699&0.975839\\
 0.986699&1&0.998264\\
 0.975839&0.998264&1
 \end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0092

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:28`
- Строки: `28--31`

```latex
\begin{equation}
 \Spec(G)=
 \left(1.03590\times10^{-4},\;0.0260003,\;2.97390\right),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0093

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:38`
- Строки: `38--40`

```latex
\begin{equation}
 m_1:m_2:m_3=1:15.8427:169.435.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0094

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:51`
- Строки: `51--54`

```latex
\begin{equation}
 C_s=\frac{(A_sB_s-B_sA_s)/(2i)}
 {\sqrt{\Tr(((A_sB_s-B_sA_s)/(2i))^2)/3}}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0095

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:56`
- Строки: `56--65`

```latex
\begin{equation}
 \mathcal M(t)=t\,\operatorname{diag}(m_{\pi(1)},m_{\pi(2)},m_{\pi(3)})
 +i\varepsilon
 \begin{pmatrix}
 0&1&-1\\
 -1&0&1\\
 1&-1&0
 \end{pmatrix},
 \qquad \varepsilon=\pm1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0096

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:74`
- Строки: `74--77`

```latex
\begin{equation}
 (m_A,m_B,m_C)=(15.8427,1,169.435),
 \qquad t=111.6408,
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0097

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:79`
- Строки: `79--82`

```latex
\begin{align}
 u&=(0.00037055,\,0.00279404,\,1),\\
 d&=(0.00099057,\,0.00224475,\,1).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0098

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:88`
- Строки: `88--95`

```latex
\begin{equation}
 |V_q|\simeq
 \begin{pmatrix}
 0.926705&0.375790&0.000336\\
 0.375790&0.926705&0.000346\\
 0.000181&0.000447&1
 \end{pmatrix},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0099

- Источник: `s2t/gates/version4_three_moment_oriented_messenger_gate.tex:97`
- Строки: `97--101`

```latex
\begin{equation}
 (s_{12},s_{23},s_{13})
 =(0.375790,\,3.4644\times10^{-4},\,3.3608\times10^{-4}),
 \qquad |J_q|=1.96\times10^{-10}.
\end{equation}
```

## `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0100

- Источник: `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex:7`
- Строки: `7--9`

```latex
\begin{equation}
 \widehat C_\sigma=e^{-\sigma^2\Delta_M}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0101

- Источник: `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex:74`
- Строки: `74--76`

```latex
\begin{equation}
 \frac{4(4+1)}2=10.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0102

- Источник: `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex:92`
- Строки: `92--105`

```latex
\begin{equation}
 \begin{aligned}
 \mathcal A_{\rm parent}
   &=C^\infty(S^4)\otimes
     \bigl(\mathbb C\oplus\mathbb H\oplus M_3(\mathbb C)\bigr),\\
 \mathcal H_{\rm parent}
   &=L^2(S^4,S)\otimes\mathcal H_F,\\
 D_{\rm parent}
   &=D_{S^4}\otimes1+\gamma_5\otimes D_F,\\
 \widehat C_\sigma
   &=e^{-\sigma^2D_{\rm parent}^2}.
 \end{aligned}
 \label{eq:toe-native-s4-parent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0103

- Источник: `s2t/gates/version4_toe_native_s4_carrier_candidate_gate.tex:140`
- Строки: `140--147`

```latex
\begin{equation}
 \widehat C_\tau(M)=e^{-\tau\Delta_M},
 \qquad
 \mathcal P_\tau(M)=
 \frac{\Tr\widehat C_\tau(M)^2}
      {\bigl(\Tr\widehat C_\tau(M)\bigr)^2}.
 \label{eq:carrier-correlation-purity}
\end{equation}
```

## `s2t/gates/version4_unified_messenger_gate.tex`

### LIVE-FORMULAS-GATES-VERSION4-04-0104

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:10`
- Строки: `10--12`

```latex
\begin{equation}
\mathbf{10}\oplus\overline{\mathbf5}\oplus\mathbf1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0105

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:14`
- Строки: `14--20`

```latex
\begin{equation}
(\mathbf{10}\oplus\overline{\mathbf{10}}),
\quad
(\mathbf5\oplus\overline{\mathbf5}),
\quad
(\mathbf1\oplus\mathbf1).
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0106

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:23`
- Строки: `23--25`

```latex
\begin{equation}
\mathbf{16}=\mathbf{10}\oplus\overline{\mathbf5}\oplus\mathbf1
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0107

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:43`
- Строки: `43--45`

```latex
\begin{equation}
C_1=C_2=C_3=2.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0108

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:47`
- Строки: `47--51`

```latex
\begin{align}
\mathbf{10}:&\quad C_1=C_2=C_3=\frac32,\\
\overline{\mathbf5}:&\quad C_1=C_2=C_3=\frac12,\\
\mathbf1:&\quad C_1=C_2=C_3=0.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION4-04-0109

- Источник: `s2t/gates/version4_unified_messenger_gate.tex:54`
- Строки: `54--56`

```latex
\begin{equation}
\Delta b_1=\Delta b_2=\Delta b_3=\frac83.
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]