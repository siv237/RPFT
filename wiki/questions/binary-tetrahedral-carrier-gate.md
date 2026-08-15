# Binary Tetrahedral Carrier Gate
> Status: working
> Type: question
> Updated: 2026-08-15

The proposed replacement `RP3 -> S3/2T` fails the locked carrier tests.

- `Vol(S3/2T)=pi^2/12`, not `pi^2`.
- `H1(S3/2T)=Z3`, so the flat-character step is `2*pi/3`, not `pi`.
- The round systole is `pi/3`.
- Direct substitution gives `S_vac=125.8944396939`, differing from the
  train anchor by `-11.1415594831`.

Character averaging over the 24 Hurwitz units gives scalar invariant degrees
`0,6,8,12,...`. The first positive scalar eigenvalue is `48` with quotient
multiplicity `7`.

For coexact one-forms,

```text
d_n = n*m_(n+1) + (n+2)*m_(n-1).
```

The `n=1` level survives with multiplicity `3`. Hence
`T_coex^(2T)=7.6133956135e-6>0`; C6 is not rescued.

Although `C[2T]=1+I_aug` and `dim I_aug=23`, the quotient spectrum keeps
`2T`-invariant states rather than the augmentation ideal. The latter would
require a separately postulated internal finite fiber. Also `Q8` acts on the
regular representation; its invariant dimensions are `3` in `C[2T]` and `2`
in `I_aug`.

Verdict: closed as a direct geometric carrier. It can reopen only as a new
model with a parent-derived internal `C[2T]` fiber.