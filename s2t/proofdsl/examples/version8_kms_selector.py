"""Exact KMS no-go certificate for the current primitive unital QMS."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_primitive import _jumps, build_certificate as build_full_certificate


@dataclass(frozen=True, slots=True)
class KMSSelectorCertificate:
    transfer_traces: tuple[sp.Expr, ...]
    transfer_jump_count: int
    unique_state_theorem: Theorem
    central_state_theorem: Theorem
    positive_no_cancellation_theorem: Theorem
    bohr_split_theorem: Theorem
    selfadjoint_bohr_no_go_theorem: Theorem
    conditional_ratio_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> KMSSelectorCertificate:
    full = build_full_certificate()
    unique = kernel.prove_unique_trace_state_from_scalar_fixed_algebra(
        full.scalar_fixed_theorem, 21, subject="unique faithful state of the primitive unital QMS"
    )
    central = kernel.prove_central_state_equals_normalized_trace(
        unique,
        11,
        10,
        subject="a I11 direct_sum b I10 is stationary only at the normalized trace",
    )

    jumps = _jumps()
    source = sp.diag(sp.eye(11), sp.zeros(10))
    target = sp.eye(21) - source
    transfer_groups = ((jumps[0],), jumps[13:19], jumps[19:25])
    traces = []
    for group in transfer_groups:
        value = sp.Integer(0)
        for jump in group:
            forward = target * jump * source
            value += sp.trace(forward * forward.H)
        traces.append(sp.simplify(value))
    k_link, k_q, k_x = sp.symbols("kappa_link kappa_QLYR kappa_XLdR", positive=True)
    no_cancellation = kernel.prove_positive_expression(
        traces[0] * k_link + traces[1] * k_q + traces[2] * k_x,
        subject="positive transfer weights cannot support a nontracial central state",
        premises=(central,),
    )

    delta = sp.Symbol("Delta", real=True, nonzero=True)
    hamiltonian = delta * target
    transfer = (jumps[0],) + jumps[13:]
    forward = tuple(sp.ImmutableMatrix(target * jump * source) for jump in transfer)
    reverse = tuple(sp.ImmutableMatrix(source * jump * target) for jump in transfer)
    split = kernel.prove_opposite_bohr_split(
        hamiltonian,
        forward,
        reverse,
        delta,
        subject="directed halves of all linking and cross transfer jumps",
    )
    selfadjoint_no_go = kernel.prove_matrix_inequality(
        hamiltonian * transfer[0] - transfer[0] * hamiltonian,
        delta * transfer[0],
        subject="a selfadjoint transfer jump is not one nonzero Bohr mode",
    )
    beta_delta = sp.Symbol("beta_Delta", real=True)
    ratio = kernel.prove_conditional_kms_rate_ratio(
        beta_delta,
        subject="directed upward/downward KMS rate ratio",
        premises=(split,),
    )
    return KMSSelectorCertificate(
        transfer_traces=tuple(traces),
        transfer_jump_count=len(transfer),
        unique_state_theorem=unique,
        central_state_theorem=central,
        positive_no_cancellation_theorem=no_cancellation,
        bohr_split_theorem=split,
        selfadjoint_bohr_no_go_theorem=selfadjoint_no_go,
        conditional_ratio_theorem=ratio,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.transfer_traces)
    print(certificate.conditional_ratio_theorem.proposition)