# Том VI: нерадиальная устойчивость тетраэдрического вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

На декартовых сетках до `48x48` построен калибровочно фиксированный
оператор эффективной подсистемы `delta phi`, `delta b`, `delta A_x`,
`delta A_y`. Десять нижних собственных значений положительны. Над двумя
мягкими решёточными модами находится устойчивый зазор `1.5010738491...`;
его сдвиг между сетками `40` и `48` равен `3.58e-4`.

## Ограничение

Две мягкие моды ещё не отождествлены строго с переносами. Не включены все
компоненты полей спина два и три и полная неабелева семейная связность.
Поэтому полная устойчивость вихря и рождение материи не закрыты.

## Последующая коррекция

Расчёт выполнен на старом профиле с трёхкратно завышенной кинетикой `T`.
После [[version6-bosonic-defect-q-stiffness-parent-normalization-gate]]
его положительность считается условной и должна быть проверена заново на
исправленном фоне.

Проверка выполнена в
[[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]].
Прежний жёсткий зазор не воспроизведён: при сгущении сетки не две, а не
менее восьми мод одновременно смягчаются к нулю. Отрицательная мода пока
не найдена, но сертификат устойчивости снят.

## Следующий вопрос

Нужно построить полный калибровочно фиксированный гессиан `Q+T+B`, найти
ровно две переносные нулевые моды и исключить отрицательные тензорные и
неабелевы каналы.

## Связи

- [[version6-bosonic-defect-q-tetrahedral-vortex-radial-stability-gate]]
- [[version6-bosonic-defect-q-stiffness-parent-normalization-gate]]
- [[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]]
- [[version6-bosonic-defect-q-tetrahedral-coupled-defect-profile-gate]]
- [[so3-z3-vortex-profile-and-stability-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_q_tetrahedral_vortex_angular_stability_gate_results.json`