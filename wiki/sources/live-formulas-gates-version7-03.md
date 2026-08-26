# Гейты Version 7, часть 3

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **13** блочных формул из **1** файла.

## `s2t/gates/version7_chiral_hodge_index_instability_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-03-0001

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:10`
- Строки: `10--17`

```latex
\begin{equation}
 H_{15}=H_L\oplus H_R,
 \qquad
 \dim_{\mathbb C}H_L=8,
 \qquad
 \dim_{\mathbb C}H_R=7.
 \label{eq:v7-h15-chiral-dimensions}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0002

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:22`
- Строки: `22--28`

```latex
\begin{equation}
 d_Y=
 \begin{pmatrix}0&0\\Y&0\end{pmatrix},
 \qquad
 \Gamma_{15}=
 \begin{pmatrix}-I_8&0\\0&I_7\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0003

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:30`
- Строки: `30--33`

```latex
\begin{equation}
 [d_Y,d_Y^\dagger]
 =\begin{pmatrix}-Y^\dagger Y&0\\0&YY^\dagger\end{pmatrix}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0004

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:38`
- Строки: `38--43`

```latex
\begin{equation}
 \mathcal S_{\rm ch}(Y)
 =\frac1{15}\Tr_{H_{15}}
 \left([d_Y,d_Y^\dagger]-\Gamma_{15}\right)^2.
 \label{eq:v7-chiral-hodge-parent}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0005

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:49`
- Строки: `49--56`

```latex
\begin{equation}
 \mathcal S_{\rm ch}(Y)
 =\frac1{15}\left\{
 \Tr_8(I_8-Y^\dagger Y)^2
 +\Tr_7(YY^\dagger-I_7)^2
 \right\}.
 \label{eq:v7-chiral-hodge-block-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0006

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:58`
- Строки: `58--64`

```latex
\begin{equation}
 \mathcal S_{\rm ch}(Y)
 =\frac1{15}\left[
 1+2\sum_{j=1}^7(1-\sigma_j^2)^2
 \right]\ge\frac1{15}.
 \label{eq:v7-chiral-singular-value-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0007

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:69`
- Строки: `69--76`

```latex
\begin{equation}
 YY^\dagger=I_7,
 \qquad
 Y^\dagger Y=P_7,
 \qquad
 \rank P_7=7.
 \label{eq:v7-chiral-coisometry-vacuum}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0008

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:78`
- Строки: `78--83`

```latex
\begin{equation}
 \dim_{\mathbb C}\ker Y=1,
 \qquad
 \min\mathcal S_{\rm ch}=\frac1{15}.
 \label{eq:v7-chiral-kernel-one}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0009

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:92`
- Строки: `92--97`

```latex
\begin{equation}
 \mathcal S_{\rm ch}(Y)
 =1-\frac4{15}\|Y\|_{\rm HS}^2
 +\frac2{15}\Tr_8(Y^\dagger Y)^2.
 \label{eq:v7-chiral-zero-expansion}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0010

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:100`
- Строки: `100--104`

```latex
\begin{equation}
 \Hess_0\mathcal S_{\rm ch}
 =-\frac8{15}I_{112}.
 \label{eq:v7-chiral-negative-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0011

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:109`
- Строки: `109--113`

```latex
\begin{equation}
 \mathcal S_{\rm ch}(tY_\star)
 =\frac1{15}\left[1+14(1-t^2)^2\right].
 \label{eq:v7-chiral-radial-path}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0012

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:120`
- Строки: `120--124`

```latex
\begin{equation}
 H_L=Q_L^{(6)}\oplus L_L^{(2)},
 \qquad
 H_R=u_R^{(3)}\oplus d_R^{(3)}\oplus e_R^{(1)}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-03-0013

- Источник: `s2t/gates/version7_chiral_hodge_index_instability_gate.tex:130`
- Строки: `130--135`

```latex
\begin{equation}
 Y_\star Y_\star^\dagger=I_7,
 \qquad
 \ker Y_\star=\mathbb C\nu_L.
 \label{eq:v7-physical-edge-coisometry}
\end{equation}
```