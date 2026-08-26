# Гейты Version 7, часть 8

> Status: working
> Type: source
> Updated: 2026-08-26

Механически извлечено: **9** блочных формул из **1** файла.

## `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-08-0001

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:13`
- Строки: `13--15`

```latex
\begin{equation}
 L=\{Q_L,L_L\},\qquad R=\{u_R,d_R,e_R\},
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0002

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:17`
- Строки: `17--20`

```latex
\begin{equation}
 E_0=\{Q_Lu_R,Q_Ld_R,L_Le_R\}.
 \label{eq:v7-existing-h15-forest}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0003

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:30`
- Строки: `30--32`

```latex
\begin{equation}
 E_{\rm miss}=\{L_Lu_R,L_Ld_R,Q_Le_R\}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0004

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:35`
- Строки: `35--40`

```latex
\begin{align}
 \{L_Lu_R,L_Ld_R\}&:\quad \{u_R,d_R\},\nonumber\\
 \{L_Lu_R,Q_Le_R\}&:\quad \{u_R,e_R\},
 \label{eq:v7-three-minimal-rectangles}\\
 \{L_Ld_R,Q_Le_R\}&:\quad \{d_R,e_R\}.\nonumber
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0005

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:46`
- Строки: `46--52`

```latex
\begin{align}
 Q_L&\sim(\mathbf3,\mathbf2)_{1/6},&
 L_L&\sim(\mathbf1,\mathbf2)_{-1/2},\nonumber\\
 u_R&\sim(\mathbf3,\mathbf1)_{2/3},&
 d_R&\sim(\mathbf3,\mathbf1)_{-1/3},&
 e_R&\sim(\mathbf1,\mathbf1)_{-1}.
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0006

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:54`
- Строки: `54--57`

```latex
\begin{equation}
 Y_S=Y_L-Y_R.
 \label{eq:v7-scalar-hypercharge-rule}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0007

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:59`
- Строки: `59--64`

```latex
\begin{align}
 L_Lu_R&:\quad S\sim(\overline{\mathbf3},\mathbf2)_{-7/6},\nonumber\\
 L_Ld_R&:\quad S\sim(\overline{\mathbf3},\mathbf2)_{-1/6},
 \label{eq:v7-missing-edge-scalars}\\
 Q_Le_R&:\quad S\sim(\mathbf3,\mathbf2)_{7/6}.\nonumber
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0008

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:67`
- Строки: `67--70`

```latex
\begin{equation}
 R_2\sim(\mathbf3,\mathbf2)_{7/6}.
 \label{eq:v7-r2-candidate}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-08-0009

- Источник: `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex:72`
- Строки: `72--77`

```latex
\begin{equation}
 \overline Q_LR_2e_R,
 \qquad
 \overline u_RR_2^Ti\sigma_2L_L+\mathrm{h.c.}
 \label{eq:v7-r2-two-edges}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[version7-minimal-h15-mixed-connector-admission-gate]]
- [[global-formula-atlas]]