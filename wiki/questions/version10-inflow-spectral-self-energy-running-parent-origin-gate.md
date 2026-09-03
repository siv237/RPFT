# Том X: ориентированная спектральная самоэнергия притока

> Status: working
> Type: question
> Updated: 2026-09-01

## Summary

Построен минимальный взаимно обратный спектральный резервуар с единичным
определителем. Выбор входящей ориентации превращает его локальное дополнение
Шура в `Sigma_in=exp(zeta)`, создаёт ненулевой интенсивный ход и точный
следовой свидетель `-1/6`. Физическое вложение этого резервуара в
43-мерный носитель программы пока не выведено.

## Key Points

- `K_res=diag(exp(-zeta),exp(zeta))`, `det K_res=1`.
- `Sigma_in=exp(zeta)`, `Sigma_out=exp(-zeta)` и
  `Sigma_in*Sigma_out=1`.
- Входящий и выходящий ходы равны соответственно `+Sigma_in` и
  `-Sigma_out`.
- Симметричная связь даёт `cosh(zeta)` и нулевую производную в начале роста.
- Для нормированного действия `A(1,0)=dGamma/dzeta=-1/6`.
- Архитектура закрыта `7/7`; происхождение геометрии и ориентации условно
  унаследовано `2/2`; типизированное вложение равно `0/1`.

## Open Boundary

Необходимо построить отображение двух ориентированных резервуарных мод в
существующий 43-мерный концевой носитель, проверить совместимость с
шестимерным KMS-сектором и получить тот же блок из общего родительского
функционала. До этого абсолютный масштаб не считается выведенным.

## Links

- [[version10-geometric-scale-beta-trace-anomaly-origin-gate]]
- [[version10-quantum-rg-common-carrier-admission-gate]]
- [[version9-endpoint-creation-kms-logdet-reservoir-spectral-density-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-physical-fermion-loop-parent-origin-gate]]

## Source Notes

- `s2t/gates/version10_inflow_spectral_self_energy_running_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_inflow_spectral_self_energy_running_parent_origin_gate.py`
- `s2t/results/s2t_v10_inflow_spectral_self_energy_running_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_inflow_spectral_self_energy_running_parent_origin.py`