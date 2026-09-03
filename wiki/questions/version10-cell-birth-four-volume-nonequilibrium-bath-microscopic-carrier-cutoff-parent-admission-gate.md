# Родитель микроскопического обрезания неравновесного носителя

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Образуют ли зона Бриллюэна клеточной дисперсии и 43-уровневое спектральное
обрезание общий физический cutoff, способный зафиксировать абсолютный
микроскопический масштаб?

## Результат

Условная клеточная геометрия даёт

$$
k_{\rm BZ}\ell_{\rm cell}=\pi,\qquad
\omega_{\rm UV}\ell_{\rm cell}/v_g=2\sqrt3,
$$

а спектральная мера — `Lambda_43 ell_cell=42`. Поэтому точное слепое
отношение равно `Lambda_43/k_BZ=42/pi`; при `v_g=c` отношение энергий равно
`7 sqrt(3)`. Положительный трёхкоординатный родитель имеет единичный
гессиан и единственный условный минимум.

Размерная карта сохраняет ядро `3/2`. Фиксация скорости оставляет одну
орбиту длины; абсолютный cutoff появляется только после независимого
якоря `ell_cell`. Компактность зоны импульсов не является происхождением
физического метра.

## Статус

- условный родитель: `9/9`;
- безразмерный cutoff-мост: `3/3`;
- происхождение носителя и абсолютного обрезания: `0/2`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-nonequilibrium-bath-continuum-dispersion-cell-geometry-typed-embedding-gate]]
- [[version10-cell-birth-four-volume-spectral-counting-measure-origin-gate]]
- [[version10-cell-birth-intrinsic-four-volume-parent-origin-gate]]