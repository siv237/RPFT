# Том VI: Real-парный радиационный ток и родитель охлаждения

> Status: working
> Type: question
> Updated: 2026-08-22

## Problem

Проверено, переживает ли радиационный ток компакттона полную Real/KO6-пару
и выводит ли существующая архитектура его связь с проекторным внутренним
охлаждением.

## Search for solution

Построены исходящие пакеты около обеих сопряжённых ветвей `±i`.
Сопоставлены ориентационно нечётная амплитуда и положительная квадратичная
норма после физического полуследа. Затем радиационный поток сравнен с
энергетическим и энтропийным бюджетами проекторного перехода.

## Expected result

Для успеха требовались ненулевой Real-чётный поток, общий носитель и
действие для семейного `R` и пространственно-хирального блуждания,
родительская конверсия норм в энергию, выведенная амплитуда `delta`,
физический частичный след и монотонный закон `beta(tau)`.

## Compliance check

- сопряжённость пакетов подтверждена с остатком `2.63e-10`;
- ориентационно нечётная амплитуда сокращается;
- физический полуслед положительного потока равен `4*pi²` с остатком
  `2.87e-9`;
- условный баланс фиксирует только произведение
  `chi*N*4*pi²*abs(delta)²`, но не `chi`, `N` и `delta` отдельно;
- глобальная унитарная радиация сама не увеличивает энтропию чистого
  состояния;
- общий носитель, взаимодействие и частичный след с проекторным `R` не
  выведены;
- родительский ledger проходит `1/7` пунктов;
- JSON валиден, аудит и Python-компиляция проходят.

## Verdict

Первый запрет снят: положительный ток Real-пары не сокращается. Но
радиационная норма пока не является проекторным тепловым током. Между
двумя секторами отсутствуют общий носитель, одна энергетическая
нормировка, взаимодействие и физическое крупнозернение; `delta`, шаг
времени и `beta(tau)` остаются свободными.

## Следующий гейт

[[version6-spectral-transition-radiative-cooling-common-carrier-attribution-gate]]
должен проверить полный `M300`-носитель и возможный канонический
intertwiner между семейным, хиральным и пространственным секторами.

## Links

- [[version6-spectral-transition-post-compacton-program-reprioritization-gate]]
- [[version6-spectral-transition-discrete-compacton-character-resolved-radiation-form-factor-gate]]
- [[version6-modular-cooling-projective-transition-gate]]
- [[version6-internal-entropy-transfer-cooling-gate]]
- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_real_pair_radiative_cooling_parent_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_real_pair_radiative_cooling_parent_gate.py`
- `s2t/results/s2t_v6_spectral_transition_real_pair_radiative_cooling_parent_gate_results.json`