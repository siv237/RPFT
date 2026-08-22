# Рамированные узлы и исключённый объём нити

> Status: working
> Type: source
> Updated: 2026-08-21

## Summary

Первичная литература разделяет три разных уровня, которые нельзя
отождествлять: замкнутость осевой кривой, топологию рамированной ленты и
геометрический запрет самопересечения нити конечной толщины.

## Key Points

- Теорема Кэлугэряну--Уайта связывает самозацепление рамированной
  замкнутой кривой со скручиванием рамки и изгибом осевой линии.
- Эта формула предполагает уже заданную рамированную кривую; она сама не
  строит вложение и не задаёт радиус трубки.
- Континуальная модель исключённого объёма вводит отдельное нелокальное
  взаимодействие различных участков цепи.
- Поэтому абстрактное циклическое слово и равенство числа входов и
  выходов являются необходимыми, но недостаточными условиями
  неразрывности толстой нити.
- Геометрическая толщина кривой ограничивается одновременно кривизной и
  глобальным самоконтактом; ropelength объединяет длину с этим
  ограничением.
- Энергии О'Хары и Мёбиуса дают примеры нелокального самоотталкивания,
  которого нет в одном локальном натяжении.
- Полевые вихревые струны Абеля--Хиггса могут пересоединяться при
  столкновении; топологический сектор не равен материальной
  неразрезаемости.

## Значение для проекта

Real-удвоение решает ориентированный баланс проходов, но простейший
обратный маршрут повторяет те же рёбра. Для превращения маршрута в
физический узел проект должен вывести либо положительный радиус
инъективности трубки, либо энергию, расходящуюся при сближении несоседних
участков. В имеющемся родительском действии такой член пока не найден.
Последующий прямой аудит подтвердил эту границу: локальная энергия двух
параллельных участков остаётся конечной при контакте, тогда как
двухточечное ядро второго порядка расходится. См.
[[version6-single-thread-excluded-volume-reconnection-barrier-gate]].

## Links

- [[version6-single-thread-framed-winding-embedding-gate]]
- [[version6-single-thread-c4-suspension-parent-gate]]
- [[eulerian-cycle-and-knot-isotopy-literature-2026]]
- [[vortex-string-curvature-effective-action-literature-2026]]
- [[version6-single-thread-excluded-volume-reconnection-barrier-gate]]

## Source Notes

- J. H. White, *Self-Linking and the Gauss Integral in Higher
  Dimensions*, American Journal of Mathematics 91 (1969), 693--728.
- M. R. Dennis, J. H. Hannay, *Geometry of Călugăreanu's theorem*,
  Proceedings of the Royal Society A 461 (2005), 3245--3254;
  arXiv:math-ph/0503012.
- S. F. Edwards, *The statistical mechanics of polymers with excluded
  volume*, Proceedings of the Physical Society 85 (1965), 613--624.
- O. Gonzalez, J. H. Maddocks, *Global Curvature, Thickness, and the Ideal
  Shapes of Knots*, PNAS 96 (1999), 4769--4773.
- J. Cantarella, J. H. G. Fu, R. Kusner, J. M. Sullivan, *Ropelength
  Criticality*, Geometry & Topology 18 (2014), 1973--2043.
- J. O'Hara, *Energy of a Knot*, Topology 30 (1991), 241--247.
- M. H. Freedman, Z.-X. He, Z. Wang, *Möbius Energy of Knots and
  Unknots*, Annals of Mathematics 139 (1994), 1--50.
- A. Hanany, K. Hashimoto, *Reconnection of Colliding Cosmic Strings*,
  JHEP 06 (2005), 021; arXiv:hep-th/0501031.
- L. Faddeev, A. J. Niemi, *Stable Knot-Like Structures in Classical
  Field Theory*, Nature 387 (1997), 58--61.