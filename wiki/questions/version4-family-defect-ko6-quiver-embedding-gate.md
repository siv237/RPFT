# Version IV family-defect KO6 quiver embedding gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Can the frozen–gauged–frozen moment-map quiver be realized as an actual KO6 finite geometry, and does its ordinary spectral action reproduce the required incoming-minus-outgoing square?

## Representation result

- Algebraic skeleton: `R0 + M3(R)_G + C2`.
- Particle labels: `(0,0)^3 -> (G,0) -> (G,2)` with grading `(+,-,+)`.
- The conjugate transposed-label chain gives an 18-dimensional KO6 completion.
- Self-adjointness, grading, reality, order-zero and first-order residuals vanish.
- First order forces the second edge to commute with all of `M3(R)`, leaving exactly `Y=Phi I3`.

## Spectral-sign result

On `X=rho I3`, `Phi=r`,

- ordinary `Tr D_p^4 = 6(rho^2+r^2)^2`, with positive mixed coefficient `+12`;
- moment-map norm is `(rho^2-r^2)^2`, with mixed coefficient `-2`;
- `Str D_p^4=0`.

Thus the representation embedding passes, but the ordinary one-trace spectral action cannot generate the moment-map condensate.

## Remaining route

Derive the middle-node square as an auxiliary D-term or relative/mapping-cone curvature norm with the same kinetic normalization. A fitted counterterm or an independently weighted portal is not allowed.

## Files

- `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex`
- `s2t/audits/s2t_v4_family_defect_ko6_quiver_embedding_gate.py`
- `s2t/results/s2t_v4_family_defect_ko6_quiver_embedding_gate_results.json`