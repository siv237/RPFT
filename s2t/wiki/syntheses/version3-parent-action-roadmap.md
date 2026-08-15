# Version III Parent Action Roadmap

Version III starts from the two-sector parent-action gate rather than a new
numerical relation.

## Frozen Objective

One action, one measure and field-redefinition-covariant embedding maps must
produce at least two independent normalization-sensitive sectors without
sector coefficients.

## First Candidate

A role-graded embedding uses the same Hodge metric for:

```text
Xi_tau = 1_RP3 + 1_S1 + P_perp,
Xi_nu  = P_H tensor normalized_1_S1 + P_ker tensor integral_e1.
```

With unit form-degree weights this gives both
`pi^2+2*pi+2/3` and `23+1/pi`. Thus there is no purely algebraic
incompatibility if backgrounds and quantum states are embedded differently.

## Remaining Obstruction

The neutrino cycle scale is fixed by an integral period. The ordinary tau
zero-form background can be rescaled continuously, so its unit amplitude is
not field-redefinition invariant. The numerical pass is not yet a parent
action.

Next gate: derive the tau scale from a compact phase, defect symplectic form,
boundary/AKSZ pairing, or finite spectral triple. The compact-phase route is
tested first.

## Compact-Phase Gate

A primitive compact `U(1)` phase removes continuous rescaling of the
collective coordinate: its period and integer charge lattice fix the
coordinate up to sign. This closes the kinematic part of the embedding gap.

The minimal local sigma-model still fails dynamically. Its derivative
action has zero Hessian on a constant phase, a periodic potential introduces
an unfixed scale, and one local field on `RP3 x S1` produces the product
volume rather than the required sum of factor volumes. A stratified
boundary/defect pairing remains open as the next candidate.

## Recovered BF/AKSZ and Conditional-Expectation Gates

Pure BF/AKSZ pairing fixes brackets but not a positive metric. Canonical
conditional expectations then recover the two factor measures without free
weights. The active obstruction is no longer the measure: it is the origin
of the doubled factor module.

## Minimal Finite Algebra Gate

The algebra C plus C and its minimal faithful representation derive the
doubled factor module and equal finite trace weights. Normalized spectator
zero modes then produce the exact own-factor volumes. This is the first
simultaneous pass of coordinate scale, factor measure and module
multiplicity.

The minimal diagonal real triple still fails dynamically: the first-order
condition forces the off-diagonal finite Dirac mixing to zero. The active
problem has moved from normalization to the classification of real graded
bimodules with an allowed odd vertex.

## Real Bimodule Square Gate

The first-order condition forces Dirac edges to preserve one bimodule index.
Reality closure therefore enlarges the two diagonal factor sectors to the
minimal four-sector Krajewski square. This square admits a nonzero odd
operator, so the vertex-existence obstruction is closed.

Two stronger gaps remain. The natural square has the wrong J--grading sign
for finite KO dimension 6 and must be particle--antiparticle doubled. Its
Dirac block also retains two complex edge parameters; full rank requires a
relative phase. The next gate is the automorphism orbit, orientability and
physical half-trace audit.

## Automorphism and KO6 Half-Trace Gate

Reality-compatible basis changes leave three continuous orbit invariants:
the two edge moduli and the phase of their product modulo pi. Sheet exchange
only removes their ordering. The finite Dirac block is therefore not fixed
by automorphisms.

KO6 doubling is explicit and preserves the required J--grading sign. A
trace normalized by the size of each reality orbit restores the original
factor weights and rank 23, but the parent measure has not yet selected this
half-trace instead of the full bosonic spectral trace. The next gate is a
finite-Dirac parent potential plus orbit-trace derivation.

## Finite Dirac Parent Potential Gate

The orbit-trace flattening potential Tr((D_F^2-I)^2) has an exact stable
minimum. It selects equal edge moduli and a maximal product phase, leaving
only two CP-conjugate branches. The Hessian on the quotient coordinates is
strictly positive.

This closes the continuous direction-orbit problem but not the physical
scale. For a dimensionful Dirac block the unit must be replaced by M^2, and
M is not fixed by the finite algebra. A real even potential also cannot
choose between the two CP signs. The next gate must derive a geometric scale
and an orientation-odd selector while retaining the orbit half-trace.

## Absolute Scale No-Go

The current parent architecture determines dimensionless combinations such
as M R but cannot select an absolute mass. Global homothety preserves the
topology, finite algebra, first-order constraints and normalized finite
potential while rescaling every Dirac eigenvalue.

The spectral cutoff is therefore a dimensionful anchor unless promoted to a
dilaton/radion field. A two-term radion potential selects a radius only
through a coefficient ratio that must itself be derived. Until that sector
exists, Version III must either use one explicit scale-setting input or
restrict blind tests to dimensionless observables.

## Dilaton--Radion Transmutation Gate

The minimal classical scale-invariant sector fails: one quartic dilaton has
only the zero vacuum, while a two-field potential fixes only a ratio and
retains an exact flat scale direction. A self-dual radius potential would
work algebraically but requires an R to 1/R symmetry absent from the current
momentum-only field menu.

The surviving architecture is quantum dimensional transmutation. A
Coleman--Weinberg dilaton potential coupled to the flattened finite Dirac
operator produces a joint radion and finite-mass vacuum if its supertrace
coefficient B is positive. The next computation is therefore no longer a
free-form model search: it is the full KO6 plus KK spectrum ledger and the
sign of B.

## Finite Zero-Mode Supertrace Gate

The first explicit Coleman--Weinberg ledger is positive. The trace kinetic
metric and flattening Hessian produce three real scalar modes with mass
squared 8 chi squared, while the finite block contains two Dirac pairs of
mass chi. The canonical numerator is 184 = 8*23, giving
B0 = 23/(8 pi^2).

This is a finite-sector seed, not the full quantum result. A relative
kinetic coefficient kappa changes the numerator to 192/kappa^2 - 8, and the
gauge/ghost, dilaton and KK towers remain absent. The next gate must derive
kappa from one product spectral action and compute the regulated tower
correction.

## Product Heat-Kernel Kappa Gate

The flat product heat-kernel coefficient a4 fixes the relative scalar
kinetic and quartic normalization. In the previous convention this gives
kappa=2, not kappa=1. The three scalar masses become m^2=4 chi^2.

The finite Coleman--Weinberg seed remains positive but is corrected from
23/(8 pi^2) to 5/(8 pi^2). The earlier appearance of 23 was normalization
dependent and is explicitly removed from the structural claims. The next
gate is now a genuine completion problem: gauge/ghost plus nonzero KK
contributions in the same scheme.

## Gauge--Ghost and KK Completion Gate

The unitary massive-vector, Goldstone and ghost complex would contribute
`3 c_A^2`, hence a nonnegative correction. The existing finite data do not
yet select the physical gauge quotient or canonical coupling, so `c_A` is
not fixed.

More decisively, the Version III factor module is a zero-spectator spectral
projection rather than a full local field space on `RP3 x S1`. Tome II
scalar, coexact, spinor and ghost towers therefore cannot be inherited
without a full fluctuated product Dirac/BV construction. The exact current
ledger is `B_full=(40+3 c_A^2+c_sigma^2+Delta N_KK)/(64 pi^2)`, with only
the finite numerator `40` derived. The next gate is the local product lift.

## Fluctuated Product and BV Complex Gate

The finite KO6 square now has an explicit almost-commutative lift on K.
Its bimodule charges are (0,+1,-1,0), so the diagonal U(1) is trivial and
the unique faithful continuous gauge group is the relative U(1).

The equal-modulus vacuum gives m_A^2/chi^2=8 g^2. The vector, Goldstone
and complex ghost ledger reduces to three physical massive-vector degrees
of freedom and contributes 192 g^4 to the zero-mode numerator. The gauge
quotient and BV complex are therefore closed; the next gate must derive the
canonical coupling from the same a4 normalization before any KK sum.

## a4 Gauge Coupling Gate

The Clifford traces in the common heat-kernel a4 block fix the scalar-to-
gauge kinetic ratio. With the derived orbit charge trace Tr Q^2=2, the
normalized gauge coefficient is 2/3 and matching to (1/4g^2)F^2 gives
g^2=3/8.

The relative vector then has m_A^2/chi^2=3. Its complete vector, Goldstone
and ghost numerator is 27, so the gauge-completed zero-mode result is
B_zero=67/(64 pi^2)>0. The coupling is no longer a free input. The next
gate is the spin and flat-character KK branch audit.

## Dimensional Product Consistency Gate

Before summing KK branches, the project must choose whether K is the
four-dimensional Euclidean base or an internal compact factor. In the
base-K reading, a second KK sum would double count spacetime determinant
modes. In the internal-K reading, the geometry is M4 x K and the flat
external a4 calculation is only a zero-mode truncation.

The naive internal spinorial lift has no fermion zero modes: R_K=6 gives
a positive Lichnerowicz bound R_K/4=3/2. Therefore kappa=2, g^2=3/8 and
B_zero=67/(64 pi^2) are retained as a closed 4D zero-mode effective block,
not yet as a derived eight-dimensional compactification. The next gate is
an explicit architecture choice and zero-mode-preserving UV lift.

## Dual Architecture Verdict

Both dimensional paths have now been tested. The base-K determinant is a
valid four-dimensional effective functional, but its vacuum can be moved
by the allowed finite terms lambda2 R chi^2 and lambda4 chi^4. It is not
parameter-free until one subtraction condition fixes those finite parts.

The internal-K path fails more sharply for the frozen field menu. The
round carrier has R_K=6, so every spin structure and every unitary flat
twist obeys D_K^2 >= 3/2 and has an empty geometric Dirac kernel. It cannot
produce the required two four-dimensional Dirac pairs. The next priority
is therefore the base-K spectral renormalization gate; a nonflat internal
lift is a separate new model.

## Base-K Spectral Renormalization Gate

The zeta determinant, geometric choice mu=1/R and ordinary spectral cutoff
have all been tested. A change mu -> exp(t)mu is exactly equivalent to a
finite quartic shift lambda4 -> lambda4+2Bt, so even chi/mu is not fixed
without a subtraction condition.

The geometric scale removes a new dimensional input but leaves lambda4 and
the homothety modulus. The cutoff branch replaces them with Lambda, f0 and
f2. The base-K result is therefore a renormalizable 4D effective parent
action with one explicit open scale-setting datum, not an absolute vacuum
prediction.

## RG and Anomaly Scale-Setting Gate

The minimal charge ledger gives the abelian one-loop coefficient b=2.
There is no nonzero perturbative one-loop fixed point, so g^2=3/8 is a
matching condition at mu_spec, not a scale-independent constant.

The matching relation predicts the dimensionless hierarchy
log(Lambda_L/mu_spec)=32 pi^2/3. Dimensional transmutation and trace
anomaly still leave one RG integration scale. Version III must therefore
use one preregistered mass or length input and test independent
dimensionless predictions blindly.

## One-Scale Blind Scorecard Gate

One abstract train scale m_ref=chi has been preregistered without assigning
a particle identity. The model then predicts fermion ratios (1,1), three
scalar ratios 2, a vector ratio sqrt(3), g^2=3/8 at matching, b=2 and a
maximal CP-phase magnitude.

The tau-like and neutrino-like norms were construction targets and are not
counted as blind observables. A direct mapping of the two finite Dirac
pairs to two charged-lepton generations fails because it predicts exact
degeneracy, while no neutrino mass operator/readout exists. The physical
two-sector Definition of Done remains open at the representation-readout
level.

## External Red-Team Convention Audit

The proposed replacement 2G -> G was rejected after writing the full
quadratic action. For L=(kappa/2)G dq dq-V and H=d2V, the canonical matrix
inside (1/2)[K dq dq-H qq] is K=kappa G. Thus kappa=2 gives K=2G, scalar
mass squared 4 chi^2, finite numerator 40 and gauge-completed numerator 67.

The current flattening equation already uses B Bdagger=I. The gauge
numerator 27 is retained and now stated through a general R_xi quartet
cancellation. The suggested spectral closure route was corrected:
Phi^2 belongs to a2 and Phi^4 to a4; a0 has no Phi dependence. An explicit
compact a2/a4 spectral-moment audit remains the next calculation.

## Compact a2/a4 Spectral-Moment Gate

The curved Dirac calculation gives spin-traced coefficients -4 Tr Phi^2
in a2 and 2 Tr(DPhi)^2 + 2 Tr Phi^4 + (R/3)Tr Phi^2 in a4. After
canonical scalar normalization,

    chi^2 = (f2/f0)Lambda^2 - R/12,

and for RP3_R x S1_R,

    (chi R)^2 = (f2/f0)(Lambda R)^2 - 1/2.

This removes independent bare lambda2/lambda4 choices and replaces them
with one spectral-moment combination. It is a genuine partial pass of the
external proposal, but the moment ratio, cutoff-radius relation and finite
quantum matching shift remain open.

## Spectral-Function Moment Menu Gate

Sharp, heat, Gaussian and second-heat profiles give moment ratios 1, 1,
sqrt(pi)/2 and 2. At Lambda R=1 they all pass the nonzero-vacuum gate but
predict different chi R values.

The continuous family exp(-a u) proves that spectral width and cutoff
normalization form one rescaling orbit: only
zeta_mom=(f2/f0)(Lambda R)^2 is physical in the current action. The
minimal spectral-function selector route is therefore closed. One train
scale must fix zeta_mom, and the main priority returns to the physical
representation/readout gate.

## Representation-Level Readout Gate

The finite charge table is (0,0,+1,-1), with scalar charges (-1,+1). All
Dirac edges are covariant, and the linear and cubic U(1) anomalies cancel.
The flattened block has full rank, two degenerate massive Dirac pairs and
no neutral fermion zero mode.

The current algebra has only one relative U(1) and contains no SU(3),
SU(2), independent hypercharge table, quarks or weak-current vertices.
A direct Standard Model readout is therefore closed. The complete positive
interpretation is an anomaly-free Higgsed hidden U(1) EFT. The next choice
is a derived portal or a genuinely new observed-sector finite algebra.

## Cross-Tome Closure Audit

Tome II is now imported with its final statuses: S_vac is a structural
compression, C6 and the minimal EW/QCD repair routes are negative, and the
neutrino 23 remains selector-conditional. Version III does not derive
these sectors from its hidden Coleman--Weinberg functional.

The factor-two challenge remains rejected by the elementary equation
2A qddot+Hq=0. The hidden parent action is genuine mathematical progress
but not an observed-world unification. Future work is split into III.H
for orbit-measure and portal closure, and a separate IV.SM finite-algebra
reconstruction.

## Orbit Measure and Pfaffian Gate

The universal orbit half-trace has been replaced by a precise trace
dictionary. The bosonic spectral action uses the full H8 trace, while the
fermion half-count follows from the Pfaffian reality measure. H4 is only a
reduced computational representative.

Full KO6 doubling multiplies bosonic kinetic and Hessian matrices together
and doubles charge and scalar traces together. Scalar masses, the gauge
ratio, g^2=3/8 and the physical supertrace numerator 67 are unchanged.
Absolute role-rank norms remain conditional, but the hidden-sector measure
gate is closed. The next step is the portal menu.

## Portal Menu Gate

Scalar, kinetic-mixing and neutrino portals have been exhausted. The
sheet-symmetric scalar portal is allowed but has a free coefficient.
Kinetic mixing vanishes because there are no bi-charged states and sheet
charge conjugation forbids it. The neutrino portal requires a new connector
bimodule and a free complex matrix.

For the minimal direct-sum hidden/observed completion, the spectral action
is additive and all nongravitational portals vanish. Version III.H is
therefore a mathematically closed but experimentally disconnected hidden
EFT. The next step is the final status freeze.

## Final Status Freeze

Version III.H is frozen as a mathematically closed one-scale anomaly-free
hidden U(1) EFT. It retains kappa=2, g^2=3/8, the fixed mass ratios,
positive supertrace numerator 67, Pfaffian fermion counting and full
bosonic spectral trace.

Two CP-conjugate vacua remain degenerate. Exact direct-sum decoupling
removes nongravitational laboratory portals. No Standard Model, neutrino,
EW/QCD or S_vac prediction is claimed. The tome title has been revised to
remove the unified-action overclaim, and observed-sector reconstruction is
reserved for Version IV.SM.