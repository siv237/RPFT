# Spin-h-связывание ориентации и семейного переноса

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Структура `Spin^h` является точным языком совместного пространственного
спина и полуцелого `SU(2)`-изоспина, но существующая ориентационная `C2`
не может выполнять обе роли. Для двух независимых действий нужен минимум
`C2_spin tensor C2_family`, то есть новый внутренний дублет.

## Key Points

- `Spin^h(n)=(Spin(n) x SU(2))/Z2`; пара центров `(-1,-1)` должна
  действовать тождественно.
- Коммутант фундаментального `SU(2)` на одной `C2` одномерен, поэтому
  второго независимого коммутирующего `SU(2)` там нет.
- Минимальный корректный модуль имеет комплексную размерность четыре.
- Текущий перенос имеет носитель `C2_orientation tensor E300`; настоящий
  `Spin^h` потребовал бы дополнительной `C2_family`.
- Размерность переносного носителя выросла бы с `600` до `1200`.
- Новый дублет не содержится в `H15/M35` и не нормируется следом `M35`.
- Проектор `P=n n^T` ещё не задаёт вспомогательное главное `SO(3)`-
  расслоение и не доказывает условие `w2(Q)=w2(TM)`.
- Универсальное назначение дублета пятнадцати каналам `H15` сохраняет
  необходимость нового глобального аномального аудита.

## Verdict

`Spin^h` не является скрытым спасением версии V. Это содержательный
кандидат языка новой версии, но только после явного добавления семейного
дублета, расширения следа, построения `SO(3)`-расслоения и отмены аномалий.
Автоматического следующего гейта нет.

## Links

- [[version5-su2-family-lift-h15-representation-gate]] — исходное
  представительное препятствие.
- [[version5-local-defect-transfer-operator-gate]] — происхождение
  ориентационной двойки.
- [[version5-projective-hedgehog-point-defect-gate]] — проекторный ёж и
  отсутствующий спинорный знак.
- [[version5-post-conclusion-architecture-decision]] — архитектурная
  развилка после части II.

## Source Notes

- `s2t/gates/version5_spinh_orientation_family_locking_reopening_gate.tex`
- `s2t/audits/s2t_v5_spinh_orientation_family_locking_reopening_gate.py`
- `s2t/results/s2t_v5_spinh_orientation_family_locking_reopening_gate_results.json`
- M. Albanese, A. Milivojević, *Spin^h and Further Generalisations of
  Spin*, Journal of Geometry and Physics 164 (2021) 104174.
- D. Artacho, M. Lawn, *The Geometry of Generalised Spin^r Spinors on
  Projective Spaces*, arXiv:2406.18337.
- C. Gibson et al., *Spin^h Structure, Scalar and Charged Spinor
  Eigenfunctions on the SU(3)/SO(3) Wu Manifold*, arXiv:2512.19497.