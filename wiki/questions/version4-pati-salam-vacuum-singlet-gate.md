# Version IV: Pati–Salam vacuum and singlet gate

> Status: working
> Research status: universal-singlet route closed negatively
> Type: question
> Updated: 2026-08-13

## Question

Can the project’s existing Coleman–Weinberg dilaton/singlet both stabilize
the Pati–Salam scale and repair the published spectral Pati–Salam vacuum?

## Literature obstruction

arXiv:1905.04533 finds that the canonical spectral Pati–Salam potential does
not provide a suitable Pati–Salam-to-SM vacuum. A required color-triplet
Goldstone remains mass-degenerate with an unwanted scalar mode, producing
extra massless fields; the candidate stationary point is not a local minimum.

## Project cross-check

- The existing Coleman–Weinberg scalar is only a conditional transmutation
  candidate because its full supertrace coefficient and RG scale are open.
- In the minimal direct-sum spectral completion its scalar portal is exactly
  zero.
- A universal norm portal shifts the required and unwanted degenerate modes
  equally. Keeping the Goldstone massless keeps the unwanted mode massless.
- The project’s `M_R^(0)=(23+pi^-1)m_mu=2.4637 GeV` is `10.78–13.31`
  decades below the Pati–Salam scales selected by free one-loop unification.

## Verdict

The existing decoupled singlet and the pure universal-shift ansatz cannot
rescue the bridge. A connected diagonal real singlet is not excluded: the
literature suggests it may generate additional mixed terms in an expanded
geometry. It must be tested together with representation-sensitive diagonal
fields, not reduced to one fitted portal coefficient.

## Next gate

Enumerate diagonal or Clifford-compatible finite blocks and compute their
contribution to the mass difference between the unwanted pseudo-Goldstone
and the required Goldstone. Reject any candidate whose contribution is
universal or zero.

## Sources

- Karimi Khozani, arXiv:1905.04533.
- Kurkov and Lizzi, arXiv:1801.00260.
- `s2t/gates/version4_pati_salam_vacuum_singlet_no_go.tex`
- `s2t/audits/s2t_v4_pati_salam_vacuum_singlet_gate.py`
- `s2t/results/s2t_v4_pati_salam_vacuum_singlet_gate_results.json`