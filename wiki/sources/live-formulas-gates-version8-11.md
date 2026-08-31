# Гейты Version 8 — часть 11

> Status: working
> Type: source
> Updated: 2026-08-30

Механически извлечено: **8** блочных формул из **1** файла.

## `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex`

### LIVE-FORMULAS-GATES-VERSION8-11-0001

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:9`
- Строки: `9--16`

```latex
\begin{equation}
 \mathcal J(\delta A,\delta B_s,\delta B_t)
 =\begin{pmatrix}
   \delta B_s&\delta A^*\\
   \delta A&\delta B_t
  \end{pmatrix}.
 \label{eq:v8-field-noise-canonical-block-map}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0002

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:20`
- Строки: `20--24`

```latex
\begin{equation}
 \rank_{\mathbb R}\mathcal J=42,
 \qquad \ker\mathcal J=0.
 \label{eq:v8-field-noise-map-rank}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0003

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:32`
- Строки: `32--37`

```latex
\begin{equation}
 \delta_X\delta A=i(X_t\delta A-\delta A X_s),
 \qquad
 \delta_X\delta B_{s,t}=i[X_{s,t},\delta B_{s,t}].
 \label{eq:v8-field-side-gauge-action}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0004

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:40`
- Строки: `40--43`

```latex
\begin{equation}
 \mathcal J\,\delta_X=i\operatorname{ad}_X\,\mathcal J.
 \label{eq:v8-field-noise-gauge-intertwining}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0005

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:51`
- Строки: `51--55`

```latex
\begin{equation}
 G_{\text{поле}}=\mathcal J^*K\mathcal J=K,
 \qquad \rank G_{\text{поле}}=42.
 \label{eq:v8-field-noise-pullback-metric}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0006

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:57`
- Строки: `57--61`

```latex
\begin{equation}
 R_{\text{поле}}=G_{\text{поле}}^{-1}=K^{-1},
 \qquad G_{\text{поле}}R_{\text{поле}}=I_{42}.
 \label{eq:v8-field-noise-pullback-dual}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0007

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:71`
- Строки: `71--76`

```latex
\begin{equation}
 S(s_{\text{п}},s_{\text{к}})
 =\operatorname{diag}(s_{\text{п}}I_{30},s_{\text{к}}I_{12}),
 \qquad s_{\text{п}}s_{\text{к}}\ne0,
 \label{eq:v8-field-noise-sector-rescaling}
\end{equation}
```

### LIVE-FORMULAS-GATES-VERSION8-11-0008

- Источник: `s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex:78`
- Строки: `78--83`

```latex
\begin{equation}
 S^*KS
 =\operatorname{diag}
 \bigl(s_{\text{п}}^2K_{\text{п}},s_{\text{к}}^2K_{\text{к}}\bigr).
 \label{eq:v8-field-noise-rescaled-pullback}
\end{equation}
```

## Links

- [[live-formula-source-index]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[global-formula-atlas]]