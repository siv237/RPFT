# Том VI: статусная заморозка дискретной компакттонной ветви

> Status: mature
> Type: question
> Updated: 2026-08-22

## Problem

Сведены восемь гейтов компакттонной ветви и проверен её итоговый допуск
по контракту `R0--R6`. Требовалось отделить точный математический результат
от недоказанного физического механизма рождения.

## Search for solution

Машинный аудит повторно прочитал сертификаты существования, устойчивости,
масштаба, захвата, `C4`-селектора, эта/Pfaffian-фазы, энергетического
вырождения и радиационного форм-фактора. Для каждого пункта `R0--R6`
зафиксированы статус, положительное содержание и стоп-причина.

## Expected result

Ветвь могла остаться кандидатом рождения только при совместном наличии
одного родителя, эндогенного запуска, физической скорости, единственного
устойчивого endpoint и слепого масштаба. Иначе точный compacton следовало
сохранить, но остановить вариации той же архитектуры.

## Compliance check

- сведено `8` машинных гейтов;
- точный compacton при `kappa=2(2m+1)pi` сохранён;
- точное многообразие имеет закон `F²=-1`;
- редуцированных расширяющих Floquet-мод в проверенных объёмах нет;
- захваты общих состояний: `0/36`;
- масштабная нульность равна `1`, абсолютная масса не выведена;
- эта/Pfaffian-скорость равна нулю;
- точный радиационный коэффициент `4*pi²` разрушает ядро и не гасит
  нежелательный характер;
- итог `R0--R6`: `1` пройден, `2` частично, `4` провалены;
- JSON валиден, аудит и Python-компиляция проходят.

## Verdict

Компакттонная ветвь заморожена как автономный механизм рождения материи.
Сохраняются точное двухузловое решение, локальный Floquet-результат,
селектор `D_chi` и аналитический радиационный форм-фактор. Не выведены
trigger, физический rate, единственный устойчивый endpoint и абсолютный
масштаб.

Переоткрытие разрешено только новому единому родителю, который одновременно
даёт масштаб, бассейн захвата, затухание всех поперечных квадратур при
сохранении ядра, производный `C4`-канал и нормированный observable.

## Следующий гейт

[[version6-spectral-transition-post-compacton-program-reprioritization-gate]]
должен выбрать следующий маршрут по полному ledger Тома VI.

## Links

- [[version6-spectral-transition-discrete-compacton-existence-gate]]
- [[version6-spectral-transition-discrete-compacton-stability-quantization-gate]]
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
- [[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
- [[version6-spectral-transition-compacton-c4-affine-selector-admissibility-gate]]
- [[version6-spectral-transition-discrete-compacton-c4-boundary-eta-dissipation-gate]]
- [[version6-spectral-transition-discrete-compacton-energy-degeneracy-boundary-overlap-gate]]
- [[version6-spectral-transition-discrete-compacton-character-resolved-radiation-form-factor-gate]]
- [[version6-spectral-transition-new-model-minimal-requirements-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_compacton_branch_status_freeze_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_compacton_branch_status_freeze_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_compacton_branch_status_freeze_gate_results.json`