# TOE 6.5 spectral-density roadmap

> Status: working
> Type: source
> Updated: 2026-08-15

## Summary

`s2t/17705966/ТОЕ 6.5.pdf` is a six-page proof roadmap for converting the
DSS/DRU heuristics into thermodynamic theorems. It is not a completed parent
functional or a fixed measure.

## What the source proposes

- `S_eff[rho] = S_spec[rho] + Gamma_fluc[rho]`;
- a free-energy completion `F=S_eff-T_eff S_info`;
- variation of a positive spectral density with a mode-number constraint;
- existence, coercivity, lower-semicontinuity and stationary-equation proofs;
- a positive Hessian and gradient-flow attractor test;
- toy ansätze, numerical minimization and sensitivity scans;
- a later mediator/thermal DRU problem.

## What remains unspecified

- `T_eff` and its relation to the correlation time;
- cutoff profile `f` and regulator scale `sigma`;
- the precise positive-density function space and carrier domain;
- the mode constraint and its multiplier;
- the modified fluctuation kernel;
- a measure on metrics or topologies;
- finite curvature/topology weights and field/BV statistics.

## Consequence

The source correctly anticipates the need for a stationary equation, Hessian
and failure modes. It does not derive the unique measure required by Tome V.
Using Gibbs normalization, a Gaussian bare spectral action or a carrier prior
therefore requires an additional theorem or axiom.

## Links

- [[version5-carrier-measure-freeze-gate]] — direct source-level verdict.
- [[version4-project-retrospective-entropy-measure-gate]] — earlier corpus extraction.
- [[version5-problem-statement-gate]] — parent-architecture requirements.
- [[version5-external-literature-map]] — external context.

## Source Notes

- `s2t/17705966/ТОЕ 6.5.pdf`
- Six pages; full text re-read on 2026-08-15.