# Chiral Doubled Triplet Yukawa Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Correct Finite Operator

The canonical family triplet is preserved by doubling chirality rather than
adding a fourth family state:

`H_F = V3_left direct_sum V3_right`,

`Gamma_F = diag(-I3,+I3)`,

`D_F(Y) = [[0,Y],[Y^dagger,0]]`.

For every complex `3 x 3` block `Y`, the operator is self-adjoint and odd,
and its square contains the physical left squared-mass operator `Y Y^dagger`.

## Physical Menu Rescan

The previously declared discrete menu was rescanned by diagonalizing
`Y Y^dagger`, with an independent SVD control.

For the raw inverse-length branch:

- 54 sector candidates and 51 distinct Yukawa blocks;
- all 54 have nondegenerate squared masses;
- 2916 ordered sector pairs;
- 2748 full-mixing pairs;
- 2352 pairs with nonzero CP;
- 534 absolute CP signatures.

The squared singular values agree to `5.33e-15`; the left singular directions
agree to `6.66e-16`.

## Selector Failure

Chiral grading permits every complex `3 x 3` Yukawa block, an 18-real-
dimensional space per sector. It does not select distinct `Y_u` and `Y_d`,
their coefficients, normalization, or CP orientation.

Restricting to the existing discrete menu still leaves hundreds of inequivalent
physical CP signatures. Chiral doubling is therefore a correct kinematic
container, not a CKM prediction.

## Next Gate

Specify the represented finite algebra, real structure, and first-order
condition, then classify the surviving Yukawa blocks before using quark data.

## Evidence

- `s2t/audits/s2t_chiral_doubled_triplet_yukawa_audit.py`
- `s2t/results/s2t_chiral_doubled_triplet_yukawa_results.json`
- `s2t/gates/chiral_doubled_triplet_yukawa_gate.tex`
