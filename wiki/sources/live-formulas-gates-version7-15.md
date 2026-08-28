# Гейты Version 7, часть 15

> Status: working
> Type: source
> Updated: 2026-08-27

Механически извлечено: **10** блочных формул из **1** файла.

## `s2t/gates/version7_modular_copy_projector_origin_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-15-0001
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:14`
- Строки: `14--19`
```latex
\begin{equation}
 N(L_L)=N(Y_L)=\{e_R,X_R,Y_R\},
 \qquad
 N(e_R)=N(X_R)=\{L_L,X_L,Y_L\}.
 \label{eq:v7-modular-copy-twin-neighbourhoods}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0002
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:29`
- Строки: `29--34`
```latex
\begin{equation}
 q_i A_{\max}^2 q_i
 =3\begin{pmatrix}1&1\\1&1\end{pmatrix},
 \qquad i\in\{L,e\}.
 \label{eq:v7-modular-copy-compressed-square}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0003
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:36`
- Строки: `36--41`
```latex
\begin{equation}
 S_i=\frac13q_iA_{\max}^2q_i-q_i
 =\begin{pmatrix}0&1\\1&0\end{pmatrix},
 \qquad S_i^2=q_i,
 \label{eq:v7-modular-copy-swap}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0004
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:43`
- Строки: `43--46`
```latex
\begin{equation}
 P_{i,\pm}=\frac12(q_i\pm S_i).
 \label{eq:v7-modular-copy-parity-projectors}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0005
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:55`
- Строки: `55--60`
```latex
\begin{equation}
 \rho_\beta=\frac{e^{-\beta h\otimes I_3}}
 {\Tr e^{-\beta h\otimes I_3}},
 \qquad \beta>0.
 \label{eq:v7-modular-copy-state}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0006
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:62`
- Строки: `62--66`
```latex
\begin{equation}
 M_\theta=(\cos\theta\,I_3\ \ \sin\theta\,I_3),
 \qquad M_\theta M_\theta^\dagger=I_3,
 \label{eq:v7-modular-copy-orbit}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0007
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:69`
- Строки: `69--74`
```latex
\begin{equation}
 W_\beta(\theta)
 =\Tr\!\left[\rho_\beta(M_\theta^\dagger M_\theta)^2\right]
 =\frac12\left(1-\tanh\beta\,\sin2\theta\right).
 \label{eq:v7-modular-copy-weighted-moment}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0008
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:76`
- Строки: `76--83`
```latex
\begin{equation}
 \theta=\frac\pi4\pmod\pi,
 \qquad
 W_{\min}=\frac1{1+e^{2\beta}},
 \qquad
 W_{\max}=\frac{e^{2\beta}}{1+e^{2\beta}},
 \label{eq:v7-modular-copy-extrema}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0009
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:85`
- Строки: `85--88`
```latex
\begin{equation}
 W_\beta''\!\left(\frac\pi4\right)=2\tanh\beta>0.
 \label{eq:v7-modular-copy-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-15-0010
- Источник: `s2t/gates/version7_modular_copy_projector_origin_gate.tex:98`
- Строки: `98--101`
```latex
\begin{equation}
 \{L_L-e_R,L_L-X_R,Y_L-e_R,Y_L-X_R\}
 \label{eq:v7-modular-copy-four-edge-orbit}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[version7-modular-copy-projector-origin-gate]]
- [[global-formula-atlas]]