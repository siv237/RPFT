# Происхождение космологической связи из эйнштейновского отклика

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Может ли эйнштейновский отклик вывести связь между энтропийным сквозным
потоком и космологической кривизной без отдельного постулата
`Lambda proportional sigma²`?

## Результат

Производство энтропии само по себе не является плотностью энергии. После
введения энергии на единицу энтропии `Theta`, времени удержания
`tau_res=1/kappa` и объёма ячейки получается

$$
\rho_{\rm flow}
=\frac{\Theta\sigma\tau_{\rm res}}{v_{\rm cell}}
=\frac{\Theta\log2}{v_{\rm cell}}.
$$

Эйнштейновский отклик и совпадение с динамической кривизной дают

$$
\Lambda_E=\frac{8\pi G\Theta\log2}{c^4v_{\rm cell}},
\qquad
\boxed{\kappa^2=
\frac{24\pi G\Theta\log2}{c^2v_{\rm cell}}}.
$$

Это уже не круговое тождество: при независимо известных `G`, `Theta` и
`v_cell` формула действительно выбирает абсолютную проводимость.
Трёхпеременный положительный родитель имеет гессиан ранга `3`, определитель
`1` и ведущие миноры `(2,3,1)`.

Но одна масштабная формула на четыре величины имеет ранг `1` и ядро
размерности `3`. В проекте пока не выведены независимые `G`, `Theta`,
абсолютный `v_cell` и вакуумоподобный тензор энергии сквозного потока.

## Статус

- архитектура: `10/10`;
- условное эйнштейновское замыкание: `5/5`;
- унаследованные источники: `3/7`;
- физический пакет якорей: `0/4`;
- абсолютная проводимость: `0/1`;
- ProofDSL: `21/21`, общий реестр `90/969`.

Следующий вопрос — аудит доступных кандидатов на четыре компонента
эйнштейновского пакета якорей.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-cosmological-constant-throughflow-parent-origin-gate]].
- Кривизненный сектор: [[version10-cell-birth-four-volume-curvature-density-parent-origin-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр статусов: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate_results.json`.