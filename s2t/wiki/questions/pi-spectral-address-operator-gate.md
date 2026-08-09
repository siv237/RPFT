# Pi Spectral Address Operator Gate

## Hypothesis

The short RPFT formulas are matrix elements of one dilation operator rather
than unrelated expressions.

## Common algebra

Eleven selected formulas lie in the fraction field of
`A_24 = Z[1/24][Pi, Pi^-1]`. Substituting the declared `S_vac(pi)` also places
`alpha` in the same field. The selected CKM phase `pi/e` is the exception.

## Operator realization

On the basis `|k>`, `k=-4,...,3`, define `D|k>=k|k>` and
`Pi=exp(log(pi)D)`. Every tested formula is reproduced as

`Tr(C_num Pi) / Tr(C_den Pi)`.

All eleven identities were verified numerically below `1e-13`.

## Rank-24 lead

The fractions `1/4, 1/3, 1/2, 2/3, 3/4` equal normalized ranks
`6/24, 8/24, 12/24, 16/24, 18/24`. The number 24 also occurs as the SU(5)
adjoint dimension and in the declared Casimir correction.

## No-go

The construction still uses 22 observable-specific coefficient matrices and
34 nonzero coefficient slots. Without a representation-theoretic rule that
selects each matrix before data comparison, this is an exact encoding rather
than a prediction.

## Evidence

- `s2t_pi_spectral_address_operator_audit.py`
- `s2t_pi_spectral_address_operator_results.json`
- `pi_spectral_address_operator_gate.tex`