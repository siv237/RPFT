# Формулы гейтов Version 7 — страница 26

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка четырнадцати новых блочных формул первого спектрального
момента, чувствительного к циклической `U(3)`-голономии, и радиального no-go
масштаба.

## Formula 1 — единственный цикл

$$
C=(Q_L,u_R,X_L,e_R,L_L,Y_R,Q_L).
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:8-11`.

## Formula 2 — блочная смежность

$$
D_{vw}=a_{vw}U_{vw},\qquad
D_{wv}=a_{vw}U_{vw}^\dagger,\qquad
a_{vw}=\begin{cases}1,&vw\in E_0,\\r,&vw\in E_*,\end{cases}
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:19-24`.

## Formula 3 — второй и четвёртый моменты

$$
\operatorname{Tr}D^2=18(2r^2+1),
\qquad
\operatorname{Tr}D^4=6(18r^4+10r^2+5).
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:30-34`.

## Formula 4 — общий шестой момент

$$
\operatorname{Tr}D^6
=54+144r^2+306r^4+324r^6
+12r^4\operatorname{ReTr}W_C.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:36-41`.

## Formula 5 — шестой момент при тривиальной голономии

$$
\operatorname{Tr}D^6\big|_{W_C=I_3}
=18(18r^6+19r^4+8r^2+3).
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:43-47`.

## Formula 6 — первая чувствительная степень

$$
k_{\min}^{\rm hol}=6,
\qquad
\Delta\operatorname{Tr}D^6=12r^4(\operatorname{ReTr}W_C-3).
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:51-55`.

## Formula 7 — голономный потенциал

$$
V_6(W_C)=12c_6r^4\operatorname{ReTr}W_C.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:64-67`.

## Formula 8 — центральные минимумы

$$
W_C^*=\begin{cases}
I_3,&c_6<0,\\
-I_3,&c_6>0,
\end{cases}
\qquad
c_6=0:\quad W_C\ \text{не виден}.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:69-77`.

## Formula 9 — голономный гессиан

$$
\operatorname{Hess}V_6\big|_{W_C^*}=12|c_6|r^4I_9,
\qquad (n_-,n_0,n_+)=(0,0,9).
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:80-84`.

## Formula 10 — усечённый спектральный полином

$$
\mathcal S_{246}(r,W_C)
=c_2\operatorname{Tr}D^2+c_4\operatorname{Tr}D^4
+c_6\operatorname{Tr}D^6.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:93-97`.

## Formula 11 — радиальный полином

$$
\mathcal S_{246}(r)=\mathcal S_{246}(0)
+ar^2+br^4+cr^6.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:99-103`.

## Formula 12 — радиальные коэффициенты

$$
a=36c_2+60c_4+144c_6,
\qquad
b=108c_4+270c_6,
\qquad
c=324c_6.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:105-110`.

## Formula 13 — уравнение масштаба

$$
a+2br^2+3cr^4=0.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:112-115`.

## Formula 14 — положительный профиль сохраняет нуль

$$
a>0,\qquad b>0,\qquad c\ge0,\qquad r_*=0.
$$

Source: `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex:123-126`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-cycle-holonomy-spectral-moment-scale-gate]]

## Source Notes

- `s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`