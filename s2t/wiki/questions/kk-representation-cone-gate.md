# KK Representation Cone Gate

> Status: first inverse diagnostic
> Date: 2026-08-04

## Question

Can a natural representation content produce the direction of the gauge corrections identified by the frozen blind scorecard before any individual threshold masses are adjusted?

## Required Direction

After fixing the common weak scale from `G_F`, the required inverse-coupling shift magnitudes for `(gY,g2,g3)` are

```text
(4.65824, 0.275386, 3.03317),
normalized: (16.91, 1, 11.01).
```

This direction is hypercharge- and color-heavy but strongly suppresses `SU(2)`.

## Frozen Rays

A complete SM generation has one-loop matter direction

```text
(20/9,4/3,4/3).
```

Even after optimizing one common amplitude, it carries more than eight times too much `SU(2)` relative to the target. Replicating complete generations or a universal complete-multiplet tower cannot solve the residual pattern.

The simple split ray

```text
U + 2 D + H = (17/6,1/6,2),
normalized: (17,1,12),
```

matches the required direction within `5.6%` in every component. This is not a prediction: it was found after the residual vector was known. It is a diagnostic of the representation content that a successful sector would need.

## Magnitude Gate

The already frozen shape modulus gives

```text
rho_S2T=0.751824338,
|log rho|/(2 pi)=0.0453994.
```

One split level is much too small. Depending on multiplicities, the required common amplitude corresponds to roughly `7-35` coherent geometric level units. A full regulated KK tower could in principle supply such enhancement, but it cannot be assumed: signs, decoupling and local subtraction must be computed.

## Interpretation

The next viable sector cannot be a tower of complete ordinary generations. It must contain a derived holonomy or boundary projection that suppresses weak doublet partners while retaining hypercharged/color singlets. The parent representation must remain anomaly-free before projection, and the finite tower sum must be predicted without using the gauge controls.

## Stop Rule

`U+2D+H` is only a clue. Adding those fields because they fit the vector would be reverse engineering. The route advances only if the same split follows independently from the existing `Z2`/quarter-holonomy geometry or another frozen symmetry principle.

## Constructive Follow-Up

An anomaly-free parent and phase table now exist; see [[anomaly-free-holonomy-projection]]. The construction uses a vectorlike `SU(5)` parent, the existing `RP3` `Z2` parity, a quarter hypercharge holonomy and conjugate flat characters. It retains exactly `U+2D+H`. The remaining issue is no longer representation consistency but derivation of the character assignment and the finite tower magnitude.