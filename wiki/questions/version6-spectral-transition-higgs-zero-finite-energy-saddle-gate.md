# Том VI: конечная конфигурация с нулём Хиггса

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

После отсутствия топологической защиты проверено, может ли уже имеющийся
хиггсовский или полный электрослабый сектор создать конечную стационарную
конфигурацию с `H(0)=0`, локализующую `rank W_nu:0→1`.

## Search for solution

Для чистого Хиггса масштабирование `H_R(x)=H(x/R)` даёт

`E(R)=R T_H+R^3 V_H`.

Условие стационарности равно `T_H+3V_H=0` и несовместимо с положительной
энергией нетривиальной конфигурации. Фиксированно-направленный гладкий
радиальный профиль с `f(0)=f'(0)=0` также имеет только локальную ветвь
`f=0`.

После включения gauge-поля масштабирование меняется:

`E_EW(R)=E_F/R+R E_D+R^3 E_V`.

Вириальное условие `E_F=E_D+3E_V` допустимо. Его реализует
электрослабый сфалерон с `H(0)=0`.

## Expected result

Успех как частицы требовал конечного стационарного решения и
неотрицательного физического гессиана после удаления симметрий.

## Compliance check

Чисто скалярный комок закрыт теоремой Деррика. Gauge--Higgs сфалерон
конечен и действительно создаёт ядро `rank W_nu=0`, но является седлом с
отрицательной модой. Поэтому он описывает переход между вакуумами, а не
устойчивую материю.

Численная энергия сфалерона из наблюдаемых параметров не объявляется
предсказанием проекта: его абсолютные электрослабые нормировки имеют
отдельный ledger.

## Следующий гейт

[[version6-spectral-transition-sphaleron-spectral-flow-gate]] показал,
что стандартный поток равен `3+1=4` на поколение, а не `15`. Сфалерон
видит левые слабые дублеты; проектный `q0` считает полный коэффициентный
носитель вместе с правыми синглетами. Открыта только явная операторная
карта, а не числовое отождествление.

## Links

- [[version6-spectral-transition-higgs-vacuum-topology-localization-gate]]
- [[version6-spectral-transition-neutrino-line-parent-gate]]
- [[version6-callias-toeplitz-index-comparison-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_higgs_zero_finite_energy_saddle_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_higgs_zero_finite_energy_saddle_gate.py`
- `s2t/results/s2t_v6_spectral_transition_higgs_zero_finite_energy_saddle_gate_results.json`
- G. H. Derrick, *Comments on Nonlinear Wave Equations as Models for Elementary Particles* (1964).
- F. R. Klinkhamer, N. S. Manton, *A Saddle-Point Solution in the Weinberg–Salam Theory* (1984).
- K. T. Matchev, S. Verner, *The Electroweak Sphaleron Revisited I* (2025).