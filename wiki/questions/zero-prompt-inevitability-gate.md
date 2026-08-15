# Zero Prompt Inevitability Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Source

The audited source is
`RPFT-main/ai-promts/First-principles-00.md`.

It conditionally reconstructs `RP3 x S1`, but the target geometry is partly
encoded in the questions.

## Deduction Ledger

- Unit quaternions give `SU(2) ~= S3`, but dimension three, simple
  connectivity, and the group-manifold requirement are assumed.
- The quotient `SU(2)/Z2 ~= RP3` is correct after declaring the center
  physically trivial. The real structure `J` alone does not quotient base
  points.
- Tomita–Takesaki modular flow is an `R`-parameter automorphism group. A
  finite KMS system need not have periodic real modular time.
- Combining a spatial base and a circle as a direct product is an additional
  synthesis axiom.
- No vacuum-energy functional, competitor class, radius equation, or spectral
  density functional is specified.

## Exact Counterexample

For

`rho = Z^(-1) diag(1, exp(-1), exp(-sqrt(2)))`,

the modular frequencies include `1` and `sqrt(2)`. A common period would
make `sqrt(2)` rational. Thus finite dimensionality and KMS equilibrium do
not force a real-time circle.

## Bundle Ambiguity

`H^2(RP3;Z)=Z2`, so a circle fiber over `RP3` has a trivial and a
nontrivial principal `U(1)` bundle class. The product is not topologically
automatic.

## Corrected Status

`RP3 x S1` remains a coherent working carrier and can be conditionally
selected inside the later restricted S2T class. It is not yet proven to be the
unique vacuum implied by NCG and KMS.

The replacement prompt is
`RPFT-main/ai-promts/First-principles-00-variational.md`.

## Evidence

- `s2t/audits/s2t_zero_prompt_inevitability_audit.py`
- `s2t/results/s2t_zero_prompt_inevitability_results.json`
- `s2t/gates/zero_prompt_inevitability_gate.tex`
