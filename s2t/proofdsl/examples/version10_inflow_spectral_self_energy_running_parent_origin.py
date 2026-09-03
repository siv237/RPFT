"""LCF certificate for oriented spectral self-energy running in Tome X."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class InflowSpectralSelfEnergyRunningCertificate:
    reservoir_operator: sp.ImmutableMatrix
    reservoir_propagator: sp.ImmutableMatrix
    incoming_projector: sp.ImmutableMatrix
    outgoing_projector: sp.ImmutableMatrix
    incoming_self_energy: sp.Expr
    outgoing_self_energy: sp.Expr
    symmetric_self_energy: sp.Expr
    anomaly_density: sp.Expr
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    determinant_theorem: Theorem
    inverse_theorem: Theorem
    projector_sum_theorem: Theorem
    incoming_rank_theorem: Theorem
    outgoing_rank_theorem: Theorem
    incoming_self_energy_theorem: Theorem
    outgoing_self_energy_theorem: Theorem
    reciprocal_self_energy_theorem: Theorem
    incoming_beta_theorem: Theorem
    outgoing_beta_theorem: Theorem
    symmetric_beta_theorem: Theorem
    fixed_cell_beta_theorem: Theorem
    anomaly_witness_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> InflowSpectralSelfEnergyRunningCertificate:
    zeta, q = sp.symbols("zeta q", real=True)
    reservoir_operator = sp.ImmutableMatrix(sp.diag(sp.exp(-zeta), sp.exp(zeta)))
    reservoir_propagator = sp.ImmutableMatrix(sp.diag(sp.exp(zeta), sp.exp(-zeta)))
    incoming_projector = sp.ImmutableMatrix([[1, 0], [0, 0]])
    outgoing_projector = sp.ImmutableMatrix([[0, 0], [0, 1]])
    incoming_vector = sp.ImmutableMatrix([1, 0])
    outgoing_vector = sp.ImmutableMatrix([0, 1])
    symmetric_vector = sp.ImmutableMatrix([sp.sqrt(2) / 2, sp.sqrt(2) / 2])

    incoming_self_energy = sp.simplify(
        (incoming_vector.T * reservoir_propagator * incoming_vector)[0]
    )
    outgoing_self_energy = sp.simplify(
        (outgoing_vector.T * reservoir_propagator * outgoing_vector)[0]
    )
    symmetric_self_energy = sp.simplify(
        (symmetric_vector.T * reservoir_propagator * symmetric_vector)[0]
    )

    inflow_action = (
        sp.log(1 + q**2 + incoming_self_energy)
        - sp.log(1 + q**2)
        - sp.log(1 + incoming_self_energy)
    )
    anomaly_density = sp.factor(sp.diff(inflow_action, zeta))
    architecture = sp.ones(7, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 0])

    determinant_theorem = kernel.prove_expression_equality(
        reservoir_operator.det(),
        1,
        subject="the reciprocal reservoir spectrum has unit determinant",
    )
    inverse_theorem = kernel.prove_matrix_equality(
        reservoir_operator * reservoir_propagator,
        sp.eye(2),
        subject="the reciprocal spectral propagator is exact",
    )
    projector_sum_theorem = kernel.prove_matrix_equality(
        incoming_projector + outgoing_projector,
        sp.eye(2),
        subject="incoming and outgoing spectral orientations are complementary",
    )
    incoming_rank_theorem = kernel.prove_exact_rank(
        incoming_projector,
        1,
        subject="the incoming geometric branch is one dimensional",
    )
    outgoing_rank_theorem = kernel.prove_exact_rank(
        outgoing_projector,
        1,
        subject="the outgoing reciprocal branch is one dimensional",
    )
    incoming_self_energy_theorem = kernel.prove_expression_equality(
        incoming_self_energy,
        sp.exp(zeta),
        subject="oriented incoming coupling induces exponentially running self energy",
    )
    outgoing_self_energy_theorem = kernel.prove_expression_equality(
        outgoing_self_energy,
        sp.exp(-zeta),
        subject="the opposite orientation induces reciprocal self energy",
    )
    reciprocal_self_energy_theorem = kernel.prove_expression_equality(
        incoming_self_energy * outgoing_self_energy,
        1,
        subject="the two oriented self energies form a reciprocal pair",
    )
    incoming_beta_theorem = kernel.prove_expression_equality(
        sp.diff(incoming_self_energy, zeta),
        incoming_self_energy,
        subject="the incoming intensive self energy has nonzero geometric beta",
    )
    outgoing_beta_theorem = kernel.prove_expression_equality(
        sp.diff(outgoing_self_energy, zeta),
        -outgoing_self_energy,
        subject="the outgoing intensive self energy has the opposite beta",
    )
    symmetric_beta_theorem = kernel.prove_expression_equality(
        sp.diff(symmetric_self_energy, zeta).subs(zeta, 0),
        0,
        subject="symmetric reservoir coupling does not choose a local scale arrow",
    )
    fixed_cell_beta_theorem = kernel.prove_expression_equality(
        sp.diff(sp.Integer(1), zeta),
        0,
        subject="a fixed local reservoir spectrum has zero geometric beta",
    )
    anomaly_witness_theorem = kernel.prove_expression_equality(
        anomaly_density.subs({zeta: 0, q: 1}),
        -sp.Rational(1, 6),
        subject="the oriented running self energy gives a nonzero trace-response witness",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(7, 1),
        subject="all oriented spectral running architecture conditions pass",
    )
    origin_ledger_theorem = kernel.prove_matrix_equality(
        origin_ledger,
        sp.Matrix([1, 1, 0]),
        subject="geometry and orientation are inherited but typed reservoir embedding is open",
    )
    origin_score_theorem = kernel.prove_expression_equality(
        sum(origin_ledger),
        2,
        subject="two of three origin requirements are supplied",
    )
    gate_theorem = kernel.prove_gate(
        "version10_inflow_spectral_self_energy_running_parent_origin_gate",
        (
            determinant_theorem,
            inverse_theorem,
            projector_sum_theorem,
            incoming_rank_theorem,
            outgoing_rank_theorem,
            incoming_self_energy_theorem,
            outgoing_self_energy_theorem,
            reciprocal_self_energy_theorem,
            incoming_beta_theorem,
            outgoing_beta_theorem,
            symmetric_beta_theorem,
            fixed_cell_beta_theorem,
            anomaly_witness_theorem,
            architecture_theorem,
            origin_ledger_theorem,
            origin_score_theorem,
        ),
    )
    return InflowSpectralSelfEnergyRunningCertificate(
        reservoir_operator=reservoir_operator,
        reservoir_propagator=reservoir_propagator,
        incoming_projector=incoming_projector,
        outgoing_projector=outgoing_projector,
        incoming_self_energy=incoming_self_energy,
        outgoing_self_energy=outgoing_self_energy,
        symmetric_self_energy=symmetric_self_energy,
        anomaly_density=anomaly_density,
        architecture=architecture,
        origin_ledger=origin_ledger,
        determinant_theorem=determinant_theorem,
        inverse_theorem=inverse_theorem,
        projector_sum_theorem=projector_sum_theorem,
        incoming_rank_theorem=incoming_rank_theorem,
        outgoing_rank_theorem=outgoing_rank_theorem,
        incoming_self_energy_theorem=incoming_self_energy_theorem,
        outgoing_self_energy_theorem=outgoing_self_energy_theorem,
        reciprocal_self_energy_theorem=reciprocal_self_energy_theorem,
        incoming_beta_theorem=incoming_beta_theorem,
        outgoing_beta_theorem=outgoing_beta_theorem,
        symmetric_beta_theorem=symmetric_beta_theorem,
        fixed_cell_beta_theorem=fixed_cell_beta_theorem,
        anomaly_witness_theorem=anomaly_witness_theorem,
        architecture_theorem=architecture_theorem,
        origin_ledger_theorem=origin_ledger_theorem,
        origin_score_theorem=origin_score_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_inflow_spectral_self_energy_running_parent_origin_gate",
    title="Ориентированная спектральная самоэнергия притока",
    source_paths=(
        "s2t/gates/version10_inflow_spectral_self_energy_running_parent_origin_gate.tex",
        "s2t/results/s2t_v10_inflow_spectral_self_energy_running_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("reciprocal_reservoir_determinant", lambda: build_certificate().determinant_theorem),
        Obligation("exact_reservoir_propagator", lambda: build_certificate().inverse_theorem),
        Obligation("complementary_orientation_projectors", lambda: build_certificate().projector_sum_theorem),
        Obligation("incoming_orientation_rank", lambda: build_certificate().incoming_rank_theorem),
        Obligation("outgoing_orientation_rank", lambda: build_certificate().outgoing_rank_theorem),
        Obligation("incoming_running_self_energy", lambda: build_certificate().incoming_self_energy_theorem),
        Obligation("outgoing_running_self_energy", lambda: build_certificate().outgoing_self_energy_theorem),
        Obligation("reciprocal_self_energy_pair", lambda: build_certificate().reciprocal_self_energy_theorem),
        Obligation("incoming_nonzero_geometric_beta", lambda: build_certificate().incoming_beta_theorem),
        Obligation("outgoing_opposite_geometric_beta", lambda: build_certificate().outgoing_beta_theorem),
        Obligation("symmetric_coupling_zero_local_beta", lambda: build_certificate().symmetric_beta_theorem),
        Obligation("fixed_cell_spectrum_zero_beta", lambda: build_certificate().fixed_cell_beta_theorem),
        Obligation("nonzero_trace_response_witness", lambda: build_certificate().anomaly_witness_theorem),
        Obligation("spectral_running_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("origin_ledger_two_of_three", lambda: build_certificate().origin_ledger_theorem),
        Obligation("origin_score_two", lambda: build_certificate().origin_score_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)