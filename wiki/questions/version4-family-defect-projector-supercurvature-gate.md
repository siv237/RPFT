# Version IV family-defect projector supercurvature gate

> Status: working
> Research status: conditional positive
> Type: question
> Updated: 2026-08-14

## Result

The radial and tetrahedral-axis conditions factor into one equation:

`Q(H)=H^2-H/sqrt(3)-I/4=0`.

Writing `J=sqrt(3)H-I/2` gives `J^2=I`; tracelessness fixes `Tr J=-2`,
so `P=(I+J)/2` is rank one. The four solutions are exactly the four
coordinate projectors of the affine menu.

Each projector chooses a fixed vertex. Unit vortex winding chooses one of
the two inverse cycles on its complement. All eight cycles obey the twisted
covariance law in all 192 tested cases, and every triplet generator has rank
two and nullity one.

## Open point

The projector equation is an explicit shifted-square curvature candidate,
but the cycle is still reconstructed after solving it. A full pass requires
one graded connection whose projected curvature is `Q(H)` and whose actual
holonomy is the corresponding three-cycle.

## Evidence

- `s2t/gates/version4_family_defect_projector_supercurvature_gate.tex`
- `s2t/audits/s2t_v4_family_defect_projector_supercurvature_gate.py`
- `s2t/results/s2t_v4_family_defect_projector_supercurvature_gate_results.json`