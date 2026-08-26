# Документы Тома VII, часть 9

> Status: working
> Type: source
> Updated: 2026-08-25

Механически извлечено: **12** блочных формул из **1** файла.

Страница фиксирует вхождения; доказательный статус читается по первичному документе и глобальному ledger.

## `s2t/docs/version7_introduction_and_problem_statement.tex`

### LIVE-FORMULAS-DOCS-09-0001

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:16`
- Строки: `16--27`

```latex
\begin{equation}
 \Phi(x)\in
 \Gamma\!\left(
 X,
 \operatorname{Hom}(\mathbb C^4,\operatorname{im}P_3)
 \widehat\otimes
 \mathcal Y_{\rm phys}
 \right),
 \qquad
 P_3=I_4-\frac14J_4,
 \label{eq:v7-fundamental-rank-field}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0002

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:45`
- Строки: `45--51`

```latex
 \begin{equation}
  \mathbb C^4=\operatorname{im}P_1\oplus\operatorname{im}P_3,
  \qquad
  P_1=\frac14J_4,
  \qquad
  \rank P_3=3.
 \end{equation}
```

### LIVE-FORMULAS-DOCS-09-0003

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:72`
- Строки: `72--80`

```latex
\begin{equation}
 E_{\rm aff}
 :=\operatorname{Hom}(\mathbb C^4,\operatorname{im}P_3),
 \qquad
 \mathcal E_7
 :=S_X\widehat\otimes E_{\rm aff}
 \widehat\otimes\mathcal Y_{\rm phys},
 \label{eq:v7-common-carrier}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0004

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:86`
- Строки: `86--92`

```latex
\begin{equation}
 \widehat\Phi
 =\Phi+\varepsilon'J\Phi J^{-1},
 \qquad
 \widehat\Phi^*=\widehat\Phi.
 \label{eq:v7-real-completion}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0005

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:98`
- Строки: `98--105`

```latex
\begin{equation}
 R_\Phi
 =\frac{\Tr_{\mathcal Y_{\rm phys}}(\Phi\Phi^*)}
 {\Tr(\Phi\Phi^*)},
 \qquad
 Q_\Phi=R_\Phi-\frac13I_3.
 \label{eq:v7-derived-order-parameter}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0006

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:113`
- Строки: `113--119`

```latex
\begin{equation}
 \mathbb A_\Phi
 =\mathbb A_0+\widehat\Phi,
 \qquad
 \mathbb A_0=\nabla_X\widehat\otimes1+1\widehat\otimes D_F,
 \label{eq:v7-parent-superconnection}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0007

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:121`
- Строки: `121--123`

```latex
\begin{equation}
 \mathbb F_\Phi=\mathbb A_\Phi^2.
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0008

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:125`
- Строки: `125--131`

```latex
\begin{equation}
 \mathcal S_7[\Phi,\nabla_X]
 =\int_X
 \operatorname{tr}_{\rm norm}
 \left(\mathbb F_\Phi^*\mathbb F_\Phi\right)d\mu_X.
 \label{eq:v7-parent-action}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0009

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:145`
- Строки: `145--147`

```latex
\begin{equation}
 L_0\eta=[\mathbb A_0,\widehat\eta]_{\rm s}.
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0010

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:149`
- Строки: `149--152`

```latex
\begin{equation}
 \mathbb F_{t\eta}
 =\mathbb F_0+tL_0\eta+t^2\widehat\eta^{2}.
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0011

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:154`
- Строки: `154--159`

```latex
\begin{equation}
 \operatorname{Re}\langle\mathbb F_0,L_0\eta\rangle=0
 \quad
 \text{для всех физических }\eta,
 \label{eq:v7-vacuum-stationarity}
\end{equation}
```

### LIVE-FORMULAS-DOCS-09-0012

- Источник: `s2t/docs/version7_introduction_and_problem_statement.tex:161`
- Строки: `161--167`

```latex
\begin{equation}
 \Hess_0\mathcal S_7(\eta,\eta)
 =2\|L_0\eta\|^2
 +4\operatorname{Re}
 \langle\mathbb F_0,\widehat\eta^{2}\rangle.
 \label{eq:v7-vacuum-hessian}
\end{equation}
```