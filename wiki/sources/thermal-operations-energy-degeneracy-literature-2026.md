# Тепловые операции, когерентность и энергетическая кратность

> Status: working
> Type: source
> Updated: 2026-08-19

## Scope

Литературная база для проверки, может ли четырёхтактный носитель автономно
охладить одноосный qutrit при строгом сохранении полной энергии.

## Thermal Operations and Microscopic Second Laws

- M. Horodecki, J. Oppenheim, *Fundamental Limitations for Quantum and
  Nanoscale Thermodynamics*, Nature Communications 4 (2013) 2059, DOI
  `10.1038/ncomms3059`.
- F. G. S. L. Brandão, M. Horodecki, N. H. Y. Ng, J. Oppenheim,
  S. Wehner, *The Second Laws of Quantum Thermodynamics*, PNAS 112 (2015)
  3275--3279, DOI `10.1073/pnas.1411728112`, `arXiv:1305.5278`.

В микроскопической термодинамике сохранение средней энергии и обычной
свободной энергии недостаточно. Тепловые операции задаются
энергосохраняющими унитариями, а переходы ограничиваются набором
монотонностей и структурой энергетических блоков.

## Coherence as a Separate Resource

- M. Lostaglio, D. Jennings, T. Rudolph, *Description of Quantum
  Coherence in Thermodynamic Processes Requires Constraints Beyond Free
  Energy*, Nature Communications 6 (2015) 6383, DOI
  `10.1038/ncomms7383`, `arXiv:1405.2188`.

Когерентность между разными энергиями является ресурсом асимметрии и не
снимает автоматически ограничения на населённости внутри энергетических
блоков. Поэтому чистое tick-состояние часов не гарантирует охлаждение
qutrit до произвольного спектра.

## Minimal Refrigerators

- N. Linden, S. Popescu, P. Skrzypczyk, *How Small Can Thermal Machines
  Be? The Smallest Possible Refrigerator*, Physical Review Letters 105
  (2010) 130401, DOI `10.1103/PhysRevLett.105.130401`.

Малая автономная холодильная машина требует резонансной структуры
нескольких подсистем. Энергетическая кратность и совпадение разрывов имеют
физическое содержание и не заменяются одной достаточной размерностью
гильбертова пространства.

## Project Consequence

Для `Hs=epsilon diag(0,1,1)` и невырожденной лестницы
`Hc=epsilon diag(0,1,2,3)` максимальная ground-населённость после любого
энергосохраняющего унитария равна `2/3`. Кристаллическая фаза требует
`0.9121665963...`. Недостающий ресурс --- две ортогональные clock-моды на
одном резонансном разрыве, а не дополнительная энтропийная ёмкость.

## Links

- [[version6-clock-controlled-energy-conserving-quench-gate]]
- [[version6-internal-entropy-transfer-cooling-gate]]
- [[closed-subsystem-cooling-and-finite-clock-literature-2026]]
- [[version6-matter-birth-program]]