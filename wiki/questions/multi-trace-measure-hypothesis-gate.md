# Multi-Trace Measure Hypothesis Gate

> Status: restricted pass; primitive independent sector traces fail
> Updated: 2026-08-04

## No-Go

For a finite semisimple algebra

```text
A = direct sum_i M_ni(C),
```

every positive trace is

```text
tau(a)=sum_i w_i Tr_i(a_i).
```

After normalization, `k-1` relative central weights remain. Independent sector traces therefore reintroduce hidden continuous parameters.

## Derived-Trace Version

One parent trace can produce distinct effective measures through fixed projectors and observable type:

- loop trace `Tr(POP)` retains rank/multiplicity;
- normalized sector average `Tr(POP)/Tr(P)` removes rank;
- pure-state expectation uses a normalized wavefunction;
- a holonomy period is topological and is not a Hilbert trace.

## Concrete Passes

- Family menu: the triplet has loop weight `3` but normalized state weight `1`.
- `SU(5)` trace: `kY=5/3`, `sin2(theta_W)=3/8` at unification.
- One `10+bar5` generation has equal normalized indices `(2,2,2)` for `SU3`, `SU2`, and `U1`.

## Old Tau Conflict

Normalized constant particle modes have unit matrix elements on both `RP3` and `S1`. Raw norms `pi^2` and `2pi` belong to backgrounds or loop sums. The hypothesis therefore explains the category error but does not rescue the old tau seed.

## Verdict

Different measures can be derived rather than fitted, but only as reductions of one parent trace. The construction currently organizes normalization; it does not yet predict a new low-energy observable.

The tensor-product completion is carried out in [[parent-trace-tensor-product-gate]] and passes algebraically with zero relative trace parameters.

## Evidence

- `s2t/audits/s2t_multi_trace_measure_hypothesis_audit.py`
- `s2t/results/s2t_multi_trace_measure_hypothesis_results.json`
- `s2t/gates/multi_trace_measure_hypothesis_gate.tex`