# Version IV: Gaussian bare spectral topology gate

> Status: working
> Research status: conditional topology-measure pass; cutoff identification open
> Type: question
> Updated: 2026-08-11

## Candidate

Interpret the Gaussian spectral action as the fundamental bare Wilsonian
action at cutoff Lambda: S_bare = Tr exp(-D^2/Lambda^2).
This fixes the heat-kernel moments and the finite Weyl-squared-to-Euler ratio
instead of treating them as arbitrary renormalized counterterms.

## Exact result

For unit-volume S4 and S2 x S2, exact spin-Dirac heat traces cross once:

    t_* = Lambda^-2 = 0.124153169935769.

- For t below t_*, S4 has lower positive Gaussian spectral action.
- For t above t_*, S2 x S2 has lower action.

The isolated a4 term prefers S2 x S2; the exact action reverses this in the
ultraviolet because lower heat coefficients remain important.

## Finite-space stability

At a constant almost-commutative vacuum,
Tr exp(-t D_total^2) factorizes into spacetime and finite heat traces.
The finite factor is positive, so finite algebra multiplicities and constant
Yukawa masses do not change the carrier ordering.

## Compatibility

The previous correlation-cell result a/sigma=1.3513921957 maps, after
unit-volume rescaling, to

    t_corr = 0.106734039959646 < t_*.

At this point the independent Dirac trace also selects S4, with difference
-0.034581798856.

## Remaining gaps

- Lambda sigma=1 is not yet independently derived.
- Quantum running shifts the bare spectral boundary coefficients.
- The field ledger has Str 1=-2, Str M^2=13 chi^2, and
  Str M^4=67 chi^4; no supersymmetric cancellation occurs.
- The massive-vector completion remains external to the three physical
  scalar modes.

## Sources

- version4_gaussian_bare_spectral_topology_gate.tex
- s2t_v4_gaussian_bare_spectral_topology_gate.py
- s2t_v4_gaussian_bare_spectral_topology_gate_results.json
- Chamseddine and Connes, arXiv:hep-th/9606001
- Chamseddine, arXiv:0812.0165
- Sakellariadou, arXiv:1101.2174