# Гейты Version 7, часть 2

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **14** блочных формул из **1** файла.

Страница фиксирует вхождения; доказательный статус читается по первичному гейту и глобальному ledger.

## `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex`

### LIVE-FORMULAS-GATES-VERSION7-02-0001

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:6`
- Строки: `6--12`

```latex
\begin{equation}
 \Phi\in\Gamma\!\left(
 X,E_{\rm aff}\widehat\otimes\mathcal Y_{\rm phys}
 \right),
 \qquad
 E_{\rm aff}=\operatorname{Hom}(\mathbb C^4,\operatorname{im}P_3),
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0002

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:21`
- Строки: `21--25`

```latex
\begin{equation}
 H_{15}=Q_L\oplus L_L\oplus u_R\oplus d_R\oplus e_R,
 \qquad
 15=6+2+3+3+1.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0003

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:27`
- Строки: `27--31`

```latex
\begin{align}
 \lambda_u&\in\operatorname{Hom}_G(Q_L\otimes\widetilde H,u_R),\\
 \lambda_d&\in\operatorname{Hom}_G(Q_L\otimes H,d_R),\\
 \lambda_e&\in\operatorname{Hom}_G(L_L\otimes H,e_R).
\end{align}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0004

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:33`
- Строки: `33--39`

```latex
\begin{equation}
 \Lambda_{\rm ch}\simeq\mathbb C^3,
 \qquad
 \operatorname{End}_{\mathcal A_{\rm SM}-\mathcal A_{\rm SM}}
 (\Lambda_{\rm ch})\simeq\mathbb C^3.
 \label{eq:v7-h15-edge-commutant}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0005

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:42`
- Строки: `42--47`

```latex
\begin{equation}
 \mathcal Y_{\rm phys}
 =\mathcal E_\rho\otimes\Lambda_{\rm ch},
 \qquad
 \dim_{\mathbb C}\mathcal Y_{\rm phys}=12.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0006

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:49`
- Строки: `49--56`

```latex
\begin{equation}
 \dim_{\mathbb C}
 (E_{\rm aff}\otimes\mathcal Y_{\rm phys})
 =12\cdot12=144,
 \qquad
 \dim_{\mathbb R}=288.
 \label{eq:v7-full-rank-field-dimension}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0007

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:68`
- Строки: `68--70`

```latex
\begin{equation}
 \widehat\eta=D_F.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0008

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:76`
- Строки: `76--78`

```latex
\begin{equation}
 \mathbb A(t)=\mathbb A_{\rm sp}+(1+t)D_F.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0009

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:81`
- Строки: `81--85`

```latex
\begin{equation}
 \mathcal S_7(t)
 =\operatorname{tr}_{\rm norm}
 \left((1+t)^4D_F^4\right)+\text{постоянные члены}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0010

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:87`
- Строки: `87--92`

```latex
\begin{equation}
 \left.\frac{d\mathcal S_7}{dt}\right|_{t=0}
 =4\operatorname{tr}_{\rm norm}(D_F^4)>0
 \qquad(D_F\ne0).
 \label{eq:v7-nonzero-df-nonstationarity}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0011

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:110`
- Строки: `110--114`

```latex
\begin{equation}
 \Hess_0\mathcal S_7(\eta,\eta)
 =2\|L_0\eta\|^2\ge0.
 \label{eq:v7-zero-df-positive-hessian}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0012

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:116`
- Строки: `116--118`

```latex
\begin{equation}
 \Hess_0\mathcal S_7=\frac87I_{24}.
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0013

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:139`
- Строки: `139--141`

```latex
\begin{equation}
 \|\mathbb F_\Phi-\mathbb F_{\rm ref}\|^2
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION7-02-0014

- Источник: `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex:148`
- Строки: `148--150`

```latex
\begin{equation}
 \langle D_F,\eta\rangle=0
\end{equation}
```