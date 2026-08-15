# Version IV: three-moment oriented messenger gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Вопрос

Дают ли совместные moments (R_4,R_6,R_8) три выведенные messenger scales,
достаточные для quark masses, CKM и CP?

## Протокол

- Стандартизовать sector operators (R_4,R_6,R_8).
- Диагонализовать их sector-averaged Gram matrix.
- Интерпретировать square roots eigenvalues как conditional messenger scales.
- Перебрать все assignments, orientations, endpoint placements и sign cocycles.
- Обучить только одну общую scale по quark masses.
- Открыть CKM и Jarlskog только после branch freeze.

## Результат

Gram matrix имеет rank 3 и condition number около (2.87\times10^4). Условные
scales равны (1:15.8427:169.435). Лучший mass branch уменьшает maximum mass
error до 29.59, но даёт (s_{12}=0.37579), почти нулевые (s_{23},s_{13}) и

\[
|J_q|=1.96\times10^{-10}.
\]

## Вердикт

Три spectral modes существуют, но минимальный oriented messenger cycle не
закрывает flavour. Следующий гейт должен использовать сами Gram eigenvectors
как endpoint intertwiners, не вводя fitted weights.