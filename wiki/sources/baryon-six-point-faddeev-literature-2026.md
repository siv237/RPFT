# Шеститочечное барионное ядро и уравнение Фаддеева

> Status: working
> Type: source
> Updated: 2026-08-30

## Итог литературной сверки

В полевой постановке барион определяется не суммой заранее выбранных
одночастичных «пружин», а полюсом функции рассеяния трёх кварков. Вычет в
полюсе задаёт трёхкварковую амплитуду, удовлетворяющую однородному уравнению

$$
 \Psi=K_{(3)}\Psi,
 \qquad
 K_{(3)}=K_{(3)}^{\mathrm{irr}}+\sum_{a=1}^{3}K_{(2)}^{(a)}.
$$

Здесь `K_(2)^(a)` --- попарное ядро при третьем кварке-наблюдателе, а
`K_(3)^irr` --- неприводимая трёхчастичная часть. Поэтому одночастичный
генератор и даже полный набор двухточечных функций в общем случае не
определяют барионный оператор.

## Первичные источники

- O. W. Greenberg, *Spin and Unitary-Spin Independence in a Paraquark Model
  of Baryons and Mesons*, Phys. Rev. Lett. 13, 598 (1964),
  DOI `10.1103/PhysRevLett.13.598`. Источник цветовой антисимметрии как
  разрешения перестановочной структуры барионного состояния.
- A. De Rújula, H. Georgi, S. L. Glashow, *Hadron masses in a gauge
  theory*, Phys. Rev. D 12, 147 (1975), DOI `10.1103/PhysRevD.12.147`.
  Источник эффективного цвето-магнитного сверхтонкого описания; это модель
  низких энергий, а не вывод полного трёхчастичного ядра.
- G. Eichmann, R. Alkofer, A. Krassnigg, D. Nicmorus, *Nucleon mass from a
  covariant three-quark Faddeev equation*, `arXiv:0912.2246`, и
  *Covariant solution of the three-quark problem in quantum field theory:
  the nucleon*, `arXiv:0912.2876`. Барионная амплитуда получается из
  полного трёхкваркового ядра после явно объявленного усечения.
- H. Sanchis-Alepuz, R. Alkofer, G. Eichmann, R. Williams,
  *Delta and Omega masses in a three-quark covariant Faddeev approach*,
  `arXiv:1109.0199`. Трёхкварковая шеститочечная функция задаётся и вне
  массовой оболочки, а однородное уравнение возникает из её полюсной части;
  это подтверждает различие между допуском форм-фактора и выводом
  физического барионного полюса.
- C. Popovici, P. Watson, H. Reinhardt, *Three-quark confinement potential
  from the Faddeev equation*, `arXiv:1010.4254`. Связь конфайнментного
  потенциала с временным глюонным пропагатором выводится только после
  задания динамического двухточечного входа и усечения сектора Янга--Миллса.
- S. Borsanyi et al., *Ab initio calculation of the neutron-proton mass
  difference*, `arXiv:1406.4088`. Наблюдаемая разность возникает из
  конкуренции КХД- и электромагнитного нарушения изоспина в совместной
  КХД+КЭД динамике, а не из одного зарядового тождества.

## Следствие для Тома VIII

Последние барионные гейты правильно обнаружили свободные величины `c`,
`g_bar`, `z` и перестановочный тип. Литературная постановка объясняет их
общее происхождение: они являются разными проекциями ещё не заданного
трёхчастичного ядра. Продолжать подбирать их отдельно означает приближать
неизвестное `K_(3)` несколькими несвязанными числами.

Правильный следующий объект --- связная трёхчастичная корреляция либо
эквивалентное шеститочечное ядро. Только после его происхождения допустимы
координатный предел, сверхтонкое приближение и вычисление
нейтрон-протонной разности.

Гейт [[version8-baryon-nonlocal-six-point-kernel-admission-gate]] теперь
даёт минимальный математический класс такого объекта. Литература не
выбирает для проекта его массы и вычеты автоматически: опубликованные
расчёты явно задают или усекают динамическое ядро.

## Связи

- [[version8-post-electromagnetic-research-fork]]
- [[version8-baryon-common-environment-correlation-origin-gate]]
- [[version8-baryon-electromagnetic-closure-redteam-gate]]
- [[version8-full-correlation-kernel-locality-reconstruction-gate]]
- [[global-formula-atlas]]

## Исходники проекта

- `s2t/gates/version8_full_correlation_kernel_locality_reconstruction_gate.tex`
- `s2t/gates/version8_baryon_common_environment_correlation_origin_gate.tex`
- `s2t/gates/version8_baryon_electromagnetic_closure_redteam_gate.tex`