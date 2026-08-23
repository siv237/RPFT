# Проверка навигации Тома I и программы S2T

> Status: mature
> Type: lint
> Updated: 2026-08-22

## Summary

Проверена структура всей вики после уточнения места Тома I и программы S2T.
Канонические исходники найдены, новые страницы включены в индекс, метаблоки и
имена страниц однозначны. Две ранее существовавшие битые Obsidian-ссылки
исправлены.

## Результаты

- страниц Markdown в `wiki/`: `559`;
- нарушений метаблока `Status / Type / Updated`: `0`;
- повторяющихся идентификаторов страниц: `0`;
- проверенных Obsidian-ссылок вне блоков кода: `3367`;
- неразрешимых Obsidian-ссылок после исправления: `0`;
- страниц без входящих ссылок: `0`.

## Исправленные структурные дефекты

- Ссылка `version4-pati-salam-rank-selector-archaeology-gate` заменена на
  существующую сводку [[pati-salam-rank-selector-archaeology]].
- Ссылка `version5-ordinary-spectral-moment-map-no-go` исправлена на
  [[version5-ordinary-spectral-moment-map-no-go-gate]].
- Том I добавлен в верхний уровень `wiki/index.md` и таблицу томов README.
- Для S2T создан отдельный источник-паспорт [[s2t-research-program]], а для
  серии — [[treatise-volume-systematics]].
- Wiki-паспорт приведён к системному имени [[tome1-s2t-research-program]].
- Для TeX создана отдельная полная Prism-safe копия
  `tome1_s2t_research_program.tex`; ключевой `main.tex` не изменяется.

## Открытые замечания

- `s2t/docs/RESEARCH_CATALOG.md` остаётся неизменяемым историческим источником
  и содержит устаревшую фразу о некаталогизированных S2T-материалах; её статус
  явно пояснён в [[research-catalog]].
- Бинарные PDF не переименовываются и не создаются: Prism не сохраняет такие
  операции. Их существующие пути закреплены как физические канонические пути.

## Links

- [[tome1-s2t-research-program]] — паспорт первого тома.
- [[s2t-research-program]] — паспорт программы S2T.
- [[treatise-volume-systematics]] — карта томов I–VI.
- [[maintenance-agent-protocol]] — протокол отчётности.

## Source Notes

- `wiki/index.md`
- `README.md`
- `s2t/docs/tome1_s2t_research_program.tex`
- `corpus/Трактат 1 том.pdf`
- `s2t/docs/theory_completion_program.tex`
- `corpus/S2T_FINAL_PAPER.md`
- `s2t/docs/version6_final_conclusion_and_next_program.tex`