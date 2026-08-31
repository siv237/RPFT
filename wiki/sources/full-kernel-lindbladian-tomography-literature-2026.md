# Полное ядро и томография линдбладовского генератора

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Литература по линдбладовской томографии подтверждает общую идею Тома VIII:
времязависимые данные полного квантового процесса могут определять генератор,
но конечновременной матричный логарифм имеет ветви, а практическая
реконструкция ограничена шумом, подготовкой состояний и разрешением быстрых
мод.

## Key Points

- В непрерывной известной полугруппе производная процесса при нуле задаёт
  генератор.
- Для одной конечновременной карты общий матричный логарифм неоднозначен;
  проект избегает этой проблемы KMS-самосопряжённостью и ветвью от единицы.
- Современная Lindbladian tomography восстанавливает структурированные
  шумовые генераторы из процессных данных.
- Томографическая идентифицируемость не является теорией происхождения:
  физическое ядро должно быть независимо задано или измерено.

## Links

- [[version8-correlation-kernel-short-time-rate-selector-gate]] — проектная
  шестипараметрическая реконструкция.
- [[version8-full-correlation-kernel-locality-reconstruction-gate]] — полное
  операторное ядро и конечная локальность.
- [[covariant-dirichlet-rate-metric-literature-2026]] — формы Дирихле,
  коэффициенты которых требуется восстановить.

## Source Notes

- M. M. Wolf, J. Eisert, T. S. Cubitt, J. I. Cirac, “Assessing
  Non-Markovian Quantum Dynamics”, Phys. Rev. Lett. 101, 150402 (2008),
  arXiv:0711.3172.
- D. Dobrynin, L. Cardarelli, M. Müller, A. Bermudez,
  “Compressed-sensing Lindbladian quantum tomography with trapped ions”,
  arXiv:2403.07462.
- Y. Liu, J. R. Seddon, T. Kohler, E. Onorati, T. S. Cubitt,
  “Robust Lindbladian Estimation for Quantum Dynamics”, arXiv:2507.07912.