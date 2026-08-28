# Формулы гейтов Version 7 — страница 27

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Механическая выписка пятнадцати формул высших циклических характеров,
условия настраиваемого нецентрального минимума и классового no-go семейных
осей.

## Formula 1 — разложение по собственным фазам

$$
W_C=V\operatorname{diag}(e^{i\theta_1},e^{i\theta_2},e^{i\theta_3})V^\dagger,
\qquad
D(r,W_C)\simeq\bigoplus_{j=1}^3D(r,e^{i\theta_j}).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:9-14`.

## Formula 2 — общее характерное разложение

$$
\operatorname{Tr}D^{2n}=A_{2n}(r)+
\sum_{m=1}^{\lfloor n/3\rfloor}
a_{2n,m}(r)\operatorname{ReTr}W_C^m,
\qquad a_{2n,m}(r)\in\mathbb Z_{\ge0}[r].
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:20-27`.

## Formula 3 — первая степень оборота

$$
k_{\min}(m)=6m,
\qquad m=1,2,3,4,5.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:30-34`.

## Formula 4 — шестой момент

$$
[\operatorname{Tr}D^6]_{\rm hol}=12r^4\chi_1(W_C).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:43-46`.

## Formula 5 — восьмой момент

$$
[\operatorname{Tr}D^8]_{\rm hol}=(48r^4+96r^6)\chi_1(W_C).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:47-50`.

## Formula 6 — десятый момент

$$
[\operatorname{Tr}D^{10}]_{\rm hol}
=(140r^4+460r^6+540r^8)\chi_1(W_C).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:51-55`.

## Formula 7 — двенадцатый момент

$$
[\operatorname{Tr}D^{12}]_{\rm hol}
=(360r^4+1560r^6+3072r^8+2592r^{10})\chi_1(W_C)
+12r^8\chi_2(W_C).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:57-63`.

## Formula 8 — первое появление третьего характера

$$
[\chi_3]\operatorname{Tr}D^{18}=12r^{12}.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:66-69`.

## Formula 9 — минимумы индивидуальных моментов

$$
\theta_{2n}^*(r)=\pi,
\qquad 2n=6,8,\ldots,30,
\qquad 0.05\le r\le20.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:75-81`.

## Formula 10 — двухгармонический потенциал

$$
V_{12}(W_C)=a\operatorname{ReTr}W_C+b\operatorname{ReTr}W_C^2.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:90-93`.

## Formula 11 — стационарность собственной фазы

$$
\sin\theta\,(a+4b\cos\theta)=0.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:95-98`.

## Formula 12 — условие внутреннего минимума

$$
b>0,
\qquad |a|<4b,
\qquad \cos\theta_*=-\frac{a}{4b}.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:100-106`.

## Formula 13 — требуемая настройка профиля

$$
a=12c_6+7584c_{12},
\qquad b=12c_{12},
\qquad -636<\frac{c_6}{c_{12}}<-628.
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:108-114`.

## Formula 14 — разделимый классовый функционал

$$
\mathcal S_f(W_C)=\sum_{j=1}^3F_f(\theta_j).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:123-126`.

## Formula 15 — сопряжённая инвариантность

$$
\mathcal S_f(UW_CU^\dagger)=\mathcal S_f(W_C)
\qquad\text{для всех }U\in U(3).
$$

Source: `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex:128-132`.

## Links

- [[live-formula-source-index]]
- [[global-formula-atlas]]
- [[version7-higher-cycle-character-mixing-freeze-gate]]

## Source Notes

- `s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex`