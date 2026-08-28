# Формулы гейтов Version 7 — страница 22

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка десяти блочных формул базисно-укоренённого
примитивного цикла полного колчана.

## Формулы

### 1. Целевой шестикромочный цикл

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:10`
- Строки: `10--13`

$$
\mathcal C_*=Q_L\to u_R\to X_L\to e_R\to L_L\to Y_R\to Q_L.
$$

### 2. Корневые рёбра исходного фона

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:15`
- Строки: `15--18`

$$
e_q=Q_Lu_R,\qquad e_\ell=L_Le_R.
$$

### 3. Обычный шестой след

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:28`
- Строки: `28--34`

$$
\operatorname{Tr}A(x)^6
=\sum_{v_0\sim\cdots\sim v_5\sim v_0}
\prod_{j=0}^{5}x_{\{v_j,v_{j+1}\}},\qquad v_6=v_0.
$$

### 4. Взвешенный оператор Хашимото

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:48`
- Строки: `48--52`

$$
H(x)_{(a,b),(c,d)}
=\delta_{bc}(1-\delta_{ad})x_{\{c,d\}}.
$$

### 5. Небэктрекинговый шестой след

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:58`
- Строки: `58--63`

$$
\operatorname{Tr}H(x)^6
=12\sum_{\mathcal C\in\mathfrak C_6}\prod_{e\in\mathcal C}x_e,
\qquad |\mathfrak C_6|=14.
$$

### 6. Укоренённый циклический отклик

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:71`
- Строки: `71--77`

$$
\mathcal R_6(x)
=\left(x_{e_q}\frac{\partial}{\partial x_{e_q}}\right)
\left(x_{e_\ell}\frac{\partial}{\partial x_{e_\ell}}\right)
\operatorname{Tr}H(x)^6.
$$

### 7. Единственное укоренённое слово

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:79`
- Строки: `79--84`

$$
\mathcal R_6(x)
=12x_{Q_Lu_R}x_{u_RX_L}x_{X_Le_R}
x_{e_RL_L}x_{L_LY_R}x_{Y_RQ_L}.
$$

### 8. Автоморфизмы до и после фиксации фона

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:93`
- Строки: `93--98`

$$
|\operatorname{Aut}_{\rm type}(G)|=4,\qquad
|\operatorname{Stab}_{\rm type}(G,E_{H_{15}})|=1.
$$

### 9. Недостающие вектороподобные массы

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:107`
- Строки: `107--110`

$$
X_LX_R,\qquad Y_LY_R.
$$

### 10. Нулевой квадратичный гессиан

- Источник: `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex:118`
- Строки: `118--121`

$$
\operatorname{Hess}_{z=0}\mathcal R_6=0.
$$

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-baseline-rooted-primitive-cycle-admission-gate]]

## Source Notes

- `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`