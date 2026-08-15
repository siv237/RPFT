# Version IV: Gram eigenvector endpoint gate

## Вопрос

Могут ли eigenvectors Gram matrix моментов (R_4,R_6,R_8), а не только её
eigenvalues, породить fermion hierarchy и CKM?

## Конструкция

Для каждого sector построены whitened operators

\[
Q_{a,s}=\lambda_a^{-1/2}\sum_n V_{na}Z_{n,s}.
\]

Знаки eigenvectors фиксируются по наибольшей компоненте. Messenger scale
обучается только по quark masses; CKM и CP остаются blind.

## Результат

- Maximum mass error: `77.64`.
- Cabibbo angle: `0.01936`.
- Другие CKM planes имеют порядок `1e-5`.
- `|J_q| = 8.77e-15`.

## Вердикт

Gram eigenmodes почти одновременно диагонализуют up/down sectors. Прямой
linear eigenvector endpoint закрыт как отрицательная ветвь.