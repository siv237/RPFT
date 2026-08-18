# Version V reduction-triangle cocycle gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Can the correlation reading reconstruct the geometric reading without a
chosen topology prior, observed data or a freely selected counterterm
trivialization?

## Exact obstruction

The connected star `K_1,4` and the disconnected graph `C4 + point` have the
same adjacency characteristic polynomial and therefore the same spectrum.
After the common positive shift `H=3I-A`, both have generator spectrum
`(1,3,3,3,5)` and identical heat traces for every positive time, although
their connectivity and degree sequences differ.

Thus a correlation spectrum, heat trace or scalar spectral functional does
not determine even finite connectivity. Full correlation matrices still
need a represented coordinate/locality algebra to acquire geometric
meaning. For heat data built from `D^2`, the sign/orientation ambiguity
`D <-> -D` is also exact.

## Candidate classification

- `C -> -tau^-1 log C` recovers a positive generator, not geometry.
- GNS and modular constructions require an algebra-state pair and do not
  select a Dirac/locality operator.
- inverse spectral reconstruction is non-unique globally;
- full spectral-triple reconstruction works only after the algebra, Dirac
  and orientation axioms have been supplied;
- entropy/Bayesian selection introduces the missing prior;
- boundary/superconnection data are an independent architecture to test.

## Verdict

The minimal reduction triangle fails. The weak correlation object
underdetermines geometry; enriching it with a full spectral triple makes the
return edge tautological. Hence the nontrivial `T_cg` fails and the loop
defect `Omega_gsc` remains undefined.

The relative/coboundary language remains useful for local morphisms, but it
is not yet a generative parent architecture.

## Next gate

[[version5-boundary-parent-trace-freeze-gate]] tested one boundary Hilbert
space and trace. Exact local Wilson, family and defect modules survive, but
their symmetry-preserving direct sum retains central weights and neither the
fixed-charge projector nor the coherent source is derived. The current
boundary parent realization therefore fails.

## Links

- [[version5-foundational-relative-architecture-gate]] — hypothesis being tested.
- [[version5-carrier-measure-freeze-gate]] — missing absolute carrier prior.
- [[spectral-correlational-source]] — common-source concept.
- [[formalize-common-source]] — refined open question.
- [[version4-modular-endpoint-intertwiner-gate]] — modular data already tested.

## Source Notes

- `s2t/gates/version5_reduction_triangle_cocycle_gate.tex`
- `s2t/audits/s2t_v5_reduction_triangle_cocycle_gate.py`
- `s2t/results/s2t_v5_reduction_triangle_cocycle_gate_results.json`
- Reconstruction references: `arXiv:math/0610418`, `arXiv:1101.5908`.
- Isospectral counterexamples: `arXiv:math/0003007`.