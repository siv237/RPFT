# Разведка следующего KMS--Keldysh гейта

> Status: mature
> Type: synthesis
> Updated: 2026-09-01

## Summary

Следующий гейт следует уточнить как
`version9_endpoint_creation_kms_logdet_keldysh_influence_functional_admission_gate`.
Его предмет — не существование triangular kernel само по себе, а
совместимость четырёх требований: causal SK structure, nonzero bath
self-energy, fermionic KMS/FDT и нескомпенсированный target logdet после
closed-contour normalization.

## Наследуемая граница программы

- Том II уже запрещает повышать determinant coincidence до physical
  functional без точного measure/normalization bookkeeping.
- Тома V--VII повторяют одну границу: carrier и qualitative architecture
  недостаточны без одной меры, одного parent и физического масштаба.
- Том VIII вывел QMS и repeated-interaction dilation условно, но не вывел
  bath state, absolute clock и rate scale.
- Текущий Том IX показал, что Hermitian coupling создаёт self-energy, но
  деформирует target determinant; zero coupling сохраняет determinant, но
  выключает dynamics.

## Ключевая формула

Для fermionic Keldysh basis causal inverse kernel имеет вид

```text
K_SK(omega) = pmatrix(K^R(omega), K^K(omega); 0, K^A(omega)).
```

Алгебраически

```text
det K_SK = det K^R det K^A,
```

но physical contour одновременно требует

```text
Z_SK[J,J] = 1,
G^K = (G^R-G^A) tanh((omega-mu)/(2T)).
```

Следовательно, triangular factorization не доказывает появление
`B_target=-log det R_theta-log det R_kappa`: сначала нужно вычислить
normalized ratio `Z_SK[J_+,J_-]/Z_SK[J,J]` и показать, что target остаётся
в его source-independent parent sector, а не сокращается до нуля.

## Точные obligations следующего гейта

1. Построить doubled system+bath carrier и фиксировать Keldysh rotation.
2. Вывести retarded, advanced и Keldysh blocks из одного microscopic
   coupling, без ручной triangularization.
3. Проверить causality и exact normalization `Z_SK[J,J]=1`.
4. Проверить fermionic KMS/FDT между spectral и noise blocks.
5. Доказать nonzero dissipative self-energy и положительность/noise
   admissibility.
6. Вычислить determinant до и после contour normalization.
7. Сравнить surviving effective action с
   `-log det R_theta-log det R_kappa`.
8. Запретить target-loaded counterterm, вторую independent species и
   decoupled bath.
9. Отдельно зарегистрировать, выводится ли reservoir/repeated-probe limit,
   необходимый для primitive Markov conductance.

## Полученный исход

Предсказанный частичный результат подтверждён. Keldysh architecture
согласует causality, full-rank dissipation/noise и KMS, но retarded/advanced
adjointness даёт determinant
`product(theta_alpha^2+kappa_alpha^2)^m_alpha`, а normalized closed contour
устраняет standalone vacuum logdet. Следующий gate проверяет microscopic
reservoir spectral density как возможный общий origin conductance и
остаточного measure term.

## Links

- [[kms-keldysh-influence-functional-sources-2026]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]
- [[current-status-and-next-vectors]]
- [[treatise-volume-systematics]]

## Source Notes

- `s2t/docs/tome2_s2t_spectral_closure.tex`
- `s2t/docs/version5_final_conclusion_and_next_program.tex`
- `s2t/docs/version6_final_conclusion_and_next_program.tex`
- `s2t/docs/version7_final_conclusion_and_next_program.tex`
- `s2t/docs/version8_final_conclusion_and_next_program.tex`
- `s2t/docs/version9_introduction_and_problem_statement.tex`
- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_fermion_bath_architecture_gate.tex`