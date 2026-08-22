# Spin-cover носитель в теории Каллиаса

> Status: working
> Type: source
> Updated: 2026-08-19

## Вопрос

Создаёт ли индексная теорема необходимую внутреннюю комплексную двойку,
или она только вычисляет индекс уже заданного Dirac--Higgs оператора?

## Первичные источники

### Callias 1978

Constantine Callias, *Axial Anomalies and Index Theorems on Open Spaces*,
Commun. Math. Phys. 62 (1978), 213--234.

Теорема вычисляет индекс дираковского оператора на нечётномерном открытом
пространстве, возмущённого эрмитовым Higgs-полем, обратимым на
бесконечности. Представление фермиона и матричное действие Higgs-поля
являются входом задачи.

### Anghel 1990

Nicolae Anghel, *L2-Index Formulae for Perturbed Dirac Operators*,
Commun. Math. Phys. 128 (1990), 77--97.

В стандартной Callias-конвенции возмущение действует как эндоморфизм
Clifford-модуля и коммутирует с Clifford multiplication. Это обеспечивает
нуль-порядковость коммутатора с оператором Дирака и отделяет
пространственный spin-фактор от внутреннего twist-фактора.

### Jackiw--Rebbi 1976

Roman Jackiw, Claudio Rebbi, *Solitons with Fermion Number 1/2*,
Phys. Rev. D 13 (1976), 3398--3409.

Классический монопольный пример содержит заранее заданный фермионный
isospin-дублет. Нулевая мода возникает при его связи с monopole/Higgs
фоном; сам дублет не выводится индексной теоремой.

### Spin-h

Michael Albanese, Aleksandar Milivojević, *Spin-h and Further
Generalisations of Spin*, J. Geom. Phys. 164 (2021) 104174,
`arXiv:2008.04934`.

`Spin^h=(Spin x Sp(1))/Z2` является точным языком независимого
пространственного spin и кватернионного внутреннего действия. Одна
неприводимая `C2` не несёт двух независимых коммутирующих фундаментальных
`SU(2)`-действий.

## Вывод для проекта

`L direct_sum L*` устраняет топологическое препятствие rank-two bundle,
но не автоматически представительное. Использование particle/conjugate
пары требует комплексно-линейного смешивания сопряжённых gauge-
представлений; обычный Real-оператор `J` для этого недостаточен. Честный
внутренний дублет с одинаковым gauge-действием на обеих компонентах
работает, но является новым модулем, если его кратность не выводится из
существующего двухкопийного родителя.

## Links

- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[version6-callias-toeplitz-index-comparison-gate]]
- [[callias-fredholm-spin-cover-literature-2026]]
- [[version5-spinh-orientation-family-locking-reopening-gate]]