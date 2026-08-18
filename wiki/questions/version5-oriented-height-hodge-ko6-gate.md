# Version V oriented height--Hodge KO6 gate

> Status: mature
> Type: question
> Updated: 2026-08-15

## Problem

Does the existing 18-dimensional KO6 family geometry determine the coherent
height `(-1,0,+1)` uniquely, up to global reversal, or is the desired quiver
orientation an external selector?

## Corrections to the colleague review

- The project KO6 signs are `J^2=+1`, `JD=DJ`, `J gamma=-gamma J`.
- A block center of a direct sum can distinguish its summands. The project
  height commutes with both left and opposite algebra actions, although it
  is not necessarily in the image of the left center alone.
- The suggested condition `[[h,a],JbJ^-1]=0` is identically satisfied for
  every block-scalar height because `[h,a]=0`. It cannot prove uniqueness.

## Exact counterexample

On the particle chain consider

- coherent height: `h_chain=(-1,0,+1)`;
- middle-sink height: `h_sink=(-1,0,-1)`.

Complete both on the conjugate chain by `h_F=h_p direct_sum (-h_p)`.
Both heights are self-adjoint, commute with the grading and both algebra
actions, satisfy `J h J^-1=-h`, obey unit absolute edge gaps and give the
same middle projector `I-h^2`.

They are not related by global sign. Nevertheless:

- `h_chain` gives the required middle curvature `XXdagger-YdaggerY`;
- `h_sink` gives the rejected sum `XXdagger+YdaggerY`.

Enumeration of the discrete heights gives four solutions and two orbits
under global reversal: the coherent orbit and the sink/source orbit.

## Trace result

The full KO6 trace contains two conjugate copies. Division by the full
middle dimension six gives exactly the original normalized `tau3`. Thus
the doubling introduces no independent weight, but it cannot select the
orientation.

## Verdict

- height--Hodge algebraic identity: pass;
- coherent-height KO6 compatibility: pass;
- full trace normalization: pass;
- uniqueness of height: fail;
- derivation of orientation from the existing KO6 data: closed;
- physical closure: not passed.

Declaring monotonicity, three distinct levels or coherent orientation would
produce a valid enlarged model, but would add precisely the selector that
was supposed to be derived.

The completed [[version5-twisted-family-automorphism-gate]] finds no
exchange automorphism of the current algebra and sends the route to a
bounded selective-doubling menu.

## Links

- [[version5-nonordinary-architecture-fork-gate]]
- [[version5-twisted-family-automorphism-gate]]
- [[version5-ordinary-spectral-moment-map-no-go-gate]]
- [[version4-family-defect-ko6-quiver-embedding-gate]]
- [[version4-family-defect-quiver-moment-map-gate]]

## Source Notes

- `s2t/gates/version5_oriented_height_hodge_ko6_gate.tex`
- `s2t/audits/s2t_v5_oriented_height_hodge_ko6_gate.py`
- `s2t/results/s2t_v5_oriented_height_hodge_ko6_gate_results.json`
- KO signs: `arXiv:1409.5983`, `arXiv:1601.00219`.
- Quiver moment-map orientation: `arXiv:0807.4734`.
- Fixed height functions for quiver orientations: `arXiv:2410.10070`.
- Krajewski arrow data: `arXiv:hep-th/0501181`.