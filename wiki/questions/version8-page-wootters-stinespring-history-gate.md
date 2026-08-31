# Конечный Page–Wootters–Stinespring history-мост

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Для точного cross-arrow канала построена конечная стационарная история с
часами `0,1,2`. После условия на показание часов и следа по свежим средам
каждый срез точно равен `Phi_*^n(rho_0)`. Тем самым впервые связаны
стационарная история, дискретные квантовые такты и ранее доказанный
непрерывный collision-limit.

Полный автономный механизм Page–Wootters пока не получен: продолжение
Stinespring-изометрии до унитария оставляет дополнение размерности `252`,
то есть семейство `U(252)`, и канал не выбирает один clock-Hamiltonian.

## Problem

Проверить, можно ли из уже полученного тринадцатиоператорного Kraus-канала
построить глобально стационарный history state, условные срезы которого
возвращают реальную дискретную динамику Тома VIII.

## Search for solution

- В eDSL добавлен тип `KrausHistory`.
- Введено точное действие канала на состояния.
- Развёрнуты слова Крауса для двух тактов: `1,13,169` ветвей.
- Сравнены ветвевое частичное прослеживание и последовательное действие
  канала.
- Построено frustration-free изометрическое history-ядро.
- Посчитана свобода полного унитарного продолжения.
- Результат связан с точным правилом Чернова `p=u/n`.

## Expected result

Условная история должна воспроизводить `rho_n=Phi_*^n(rho_0)` точно, но не
должна автоматически объявляться физическими автономными часами.

## Compliance check

- System dimension: **21**.
- Environment per tick: **13**.
- Clock dimension: **3**.
- Kraus branch bounds: **1, 13, 169**.
- Conditional residuals: **zero**.
- Slice traces: **1, 1, 1**.
- History zero-mode family: **21**.
- Padded data dimension: **3549**.
- Full clock–data dimension: **10647**.
- Unitary-extension complement: **252**.
- Extension family: **U(252)**, `63504` real parameters.
- Canonical autonomous unitary tick: **not derived**.
- Physical time scale: **not derived**.
- LCF registry: **14 gates / 92 obligations** after the extension no-go.
- Tests: **24 passed**.
- Double-run SHA-256:
  `cdf4df46f4a472b346aacbd87b17274322221f054623e9d00fe3c7ad3b71eca3`.
- Tome VIII build: **successful, 144 pages**.

## Key Points

- Получен настоящий математический мост от стационарной истории к
  дискретному открытому процессу.
- Непрерывный предел наследуется от уже проверенного collision-limit.
- Необратимость появляется после следа по среде, а не внутри глобальной
  стационарной истории.
- Следующий вопрос локализован: может ли архитектура выбрать полный
  clock-unitary или его неединственность фундаментальна.

## Links

- [[version6-projective-quench-parent-dynamics-gate]] — ранняя постановка
  Page–Wootters-условий.
- [[version8-minimal-covariant-stinespring-lcf-migration-gate]] — точный
  одношаговый канал и среда размерности 13.
- [[version8-intrinsic-noise-clock-lcf-migration-gate]] — непрерывный
  collision-limit.
- [[version8-dynamic-physical-closure-redteam-gate]] — запрет объявления
  безразмерного history-моста физической секундой.
- [[relational-modular-internal-time-literature-2026]] — литературная база.

## Source Notes

- `s2t/proofdsl/history.py`
- `s2t/proofdsl/examples/version8_page_wootters_history.py`
- `s2t/gates/version8_page_wootters_stinespring_history_gate.tex`
- `s2t/audits/s2t_v8_page_wootters_stinespring_history_gate.py`
- `s2t/results/s2t_v8_page_wootters_stinespring_history_gate_results.json`