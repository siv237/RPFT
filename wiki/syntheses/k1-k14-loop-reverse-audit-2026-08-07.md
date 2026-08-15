# K1--K14 And Loop-Reverse Audit

> Status: working
> Research status: priority batch completed
> Type: synthesis
> Updated: 2026-08-07

## Executive Verdict

The expanded search mostly reopens already audited mechanisms. The batch
adds no closed physical prediction.

- K1 passes the doubled-eta arithmetic but fails the real-mass gate.
- K2 leaves the canonical vertex unchanged because sqrt(2)^2/2=1.
- K6 remains the strongest live action-level route.
- K12 matches pi^4 only in six selected reversed-statistics zero shells.
- K13 retains an exact inverse-susceptibility identity but lacks a source
  map and carrier.
- The proposed inverse powers of S_geo are ansatz powers, not loop orders.

The current status remains R_sci=5/10 and N_closed_physical=0.

## K1 Doubled Eta

Two identical eta=-1/4 blocks give eta=-1/2, so

    -eta/2 + 1/12 = 1/3.

This is exact arithmetic. It doubles a determinant phase rather than
creating a real mass shift. A physical conjugate/vectorlike doubling cancels
eta, while same-chirality doubling requires a new chiral CP mechanism.

Verdict: arithmetic pass, phase-to-mass fail.

## K2 Two-Vertex Normalization

The proposed normalization is

    sqrt(2)^2 times 1/2 = 1.

It therefore preserves the canonical J=1 rather than producing
J_required=5.4027533071. Any additional rank division must be defined by a
vertex operator before further numerical screening.

## K6 Defect Index

The conditional defect model consistently supplies one real Majorana kernel
and a rank-23 complement. The open problem is no longer the local index. It
is the derivation of the global BdG operator, condensation and quotient
stiffness from one parent action.

Verdict: highest-value live gate.

## K12 And K13

K12:

- one statistics-reversed complete two-form complex gives +pi^4/6 only in
  the spatial zero shell;
- six copies give +pi^4 arithmetically;
- the full four-dimensional trace diverges;
- the sixfold multiplicity and statistics reversal are not symmetry-derived.

K13:

- Var(xbar)=1/pi^4 is exact;
- J=sqrt(2) gives J^2/2=1 arithmetically;
- no bosonic half-shifted six-channel carrier, ordinary-trace source map or
  equal-weight parent action has been derived.

K12 is a possible new graded theory, not a rescue. K13 remains a precise
parent-action candidate.

## Full BV Follow-Up

The collaborator subsequently wrote the complete reducible two-form BV
complex. Its determinant powers leave one physical bosonic degree of freedom,
as required by four-dimensional two-form/scalar duality.

The follow-up confirms:

- one complete complex gives -pi^4/6 on the spatial zero shell;
- complete statistics reversal gives +pi^4/6, not +pi^4;
- six independent reversed complexes are still an added multiplicity;
- zeta(4,1/2) arises only as a second variation Tr(K^-2) for an explicitly
  declared additive source deformation;
- the first variation Tr(K^-1) must be removed by a derived stationary or
  subtraction condition;
- Fourier conjugation and the BV quotient do not provide six independent
  physical Gaussian channels;
- a Grassmann determinant does not define a positive commuting variance
  without an additional bosonization/readout construction;
- J^2/2=1 and a second independent normalization-sensitive sector remain
  absent.

This closes the proposed tensor parent action at
algebraic-identity-pass / parent-action-fail. Reopening requires a new
symmetry-derived graded theory rather than another sixfold copy.

## Other Candidates

- K3, K8 and K11 remain closed pruners.
- K4 is numerical screening without an operator.
- K5 has no derived WZW level k=22.
- K7 confuses the order of S4 with a physical representation; only its
  regular representation has dimension 24.
- K9 is algebraically feasible but physically infeasible in the allowed
  threshold interval.
- K10 cannot supply the missing SU2 and SU3 directions.
- K14 inserts an extra alpha/(4pi), suppressing the existing conditional
  m_D target by a factor about 1722.

## Loop-Reverse Correction

For the frozen residual,

    c3=Delta S_geo^3=0.00894938,
    c4=Delta S_geo^4=1.22639016.

These are coefficients of chosen inverse-power fits. They are not identified
three- and four-loop coefficients. Loop order must follow from coupling
counting and an effective-action expansion.

Likewise, n and winding q enumerate modes inside one determinant. The small
n=3 tower contribution rules out a higher-shell explanation of the residual
in the same absorption normalization, but does not prove that all higher-loop
physics vanishes.

No uncertainty for the frozen alpha anchor was propagated in this test, so
the residual cannot yet be classified as anchor noise.

## Recommended Work

1. Derive K6 from one defect/BdG parent action.
2. Develop K13 only with a derived six-channel carrier and source map.
3. Treat K12 as a new graded model requiring a complete BV restart.
4. Define K2 as a finite vertex algebra before numerical searches.
5. Prioritize external reproduction of R1 over more constant matching.

## Evidence

- s2t_k1_k14_loop_reverse_audit.py
- s2t_k1_k14_loop_reverse_results.json
- k1_k14_loop_reverse_gate.tex
- [[hypothesis-batch-pruner-gate]]
- [[canonical-measure-vertex-localization-gate]]
- [[bl-nonuniform-pairing-working-package-2026-08-07]]
- [[six-channel-inverse-susceptibility-gate]]