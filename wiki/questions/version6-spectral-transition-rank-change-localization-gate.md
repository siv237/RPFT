# Том VI: локализация смены ранга нейтринной опоры

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Существующее радиальное сцепление `M300` не создаёт область `H=0` в
ядре вихря. Для `s=|H|^2` точечный минимум равен

`s*(T)=T/6+1/2`, `T>=0`,

и потому имеет нижнюю границу `1/2`. Квадратичная нейтринная опора
`W_nu(H)` сохраняет ранг один как снаружи, так и внутри дефекта.

## Оптимистический контроль

Даже после контрольного единичного ядрового члена `+3 k s`, `0<=k<=1`,
минимум равен

`s*(T;k)=max(0,T/6+1/2-k/4)>=1/4`.

Для достижения `H=0` нужна сила `k>=2+(2/3)T`, которая текущим
родителем не выведена. Контрольный член не добавляется в модель.

## Что закрыто

- радиальная амплитуда `T` не подавляет, а повышает предпочтительную
  норму Хиггса;
- существующий вихрь не локализует смену ранга `0→1`;
- нулевой портал `Tr(Q^2) H^dagger H` нельзя заменять ручным
  ядровым коэффициентом.

## Что остаётся открытым

Следующий гейт должен классифицировать все уже представленные стрелки
между семейным дефектным сектором и слабым дублетом. Ненулевой
бифундаментальный интертвинер мог бы породить требуемый смешанный член
из общего квадрата кривизны. Нулевое пространство интертвинеров закроет
скрытый коннектор и потребует явно признать расширение модели.

Последующий аудит показал, что прямые интертвинеры нулевые. При этом
сохранился непрямой кандидат — двенадцатимерный смешанный модуль одноформ,
для которого ещё нужно вычислить композицию второй степени. См.
[[version6-spectral-transition-radial-bridge-vortex-connector-gate]].

## Links

- [[version6-spectral-transition-weinberg-pairing-parent-gate]]
- [[version6-spectral-transition-neutrino-line-parent-gate]]
- [[version6-bosonic-defect-mass-portal-parent-gate]]
- [[version5-m300-hodge-curvature-hessian-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[transition-primitive]]
- [[version6-spectral-transition-radial-bridge-vortex-connector-gate]]

## Source Notes

- `s2t/gates/version6_spectral_transition_rank_change_localization_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_rank_change_localization_gate.py`
- `s2t/results/s2t_v6_spectral_transition_rank_change_localization_gate_results.json`
- E. Witten, *Superconducting Strings* (1985).
- A. Achucarro, T. Vachaspati, *Semilocal and Electroweak Strings*
  (2000).
- P. Forgacs, A. Lukacs, *Stabilization of Semilocal Strings by Dark
  Scalar Condensates* (2017).