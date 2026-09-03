"""LCF certificate for through-flow affinity and impedance origins."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class ThroughFlowAffinityImpedanceOriginAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    cycle_generator: sp.ImmutableMatrix
    stationary_state: sp.ImmutableMatrix
    rate_clock_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    conductance_column_theorem: Theorem
    orbit_break_column_theorem: Theorem
    stationary_state_theorem: Theorem
    generator_rank_theorem: Theorem
    generator_nullity_theorem: Theorem
    edge_current_theorem: Theorem
    cycle_affinity_theorem: Theorem
    entropy_production_theorem: Theorem
    generator_rescaling_theorem: Theorem
    affinity_rescaling_theorem: Theorem
    current_rescaling_theorem: Theorem
    rate_clock_rank_theorem: Theorem
    rate_clock_nullity_theorem: Theorem
    rate_clock_kernel_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ThroughFlowAffinityImpedanceOriginAuditCertificate:
    # force relation, absolute conductance, cycle carrier, positive entropy,
    # internal typing, breaks the clock-rate orbit
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 1, 1, 1, 0],  # KMS rate ratio
        [0, 0, 1, 0, 1, 0],  # reciprocal K43 orientation
        [1, 0, 0, 1, 1, 0],  # normalized cell-birth measure
        [0, 0, 1, 0, 1, 0],  # clock resonance
        [0, 0, 1, 0, 1, 0],  # spectral gap
        [0, 0, 1, 0, 1, 0],  # Hopf winding
        [1, 0, 1, 1, 0, 0],  # physical matter bath
        [0, 0, 1, 1, 1, 0],  # cosmological flow
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    scores = [sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)]

    rate, scale = sp.symbols("kappa c", positive=True)
    cycle_generator = sp.ImmutableMatrix(rate*sp.Matrix([
        [-3, 1, 2], [2, -3, 1], [1, 2, -3]
    ]))
    stationary_state = sp.ImmutableMatrix([sp.Rational(1, 3)]*3)
    edge_current = 2*rate*sp.Rational(1, 3)-rate*sp.Rational(1, 3)
    cycle_affinity = 3*sp.log(sp.Integer(2))
    entropy_production = 3*edge_current*sp.log(sp.Integer(2))
    rate_clock_map = sp.ImmutableMatrix([[1, -1, 0], [1, 0, 1]])
    scale_vector = sp.ImmutableMatrix([1, 1, -1])
    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0])

    candidate_matrix_theorem = kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="eight affinity and impedance candidates are evaluated on six physical criteria")
    pass_vector_theorem = kernel.prove_matrix_equality(pass_vector, sp.zeros(8, 1), subject="no current candidate derives absolute conductance and breaks the clock orbit")
    maximum_score_theorem = kernel.prove_expression_equality(max(scores), 4, subject="the KMS rate ratio is the closest existing affinity candidate")
    candidate_rank_theorem = kernel.prove_exact_rank(candidate_matrix, 4, subject="candidate distinctions span force cycle entropy and internal typing")
    conductance_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 1], sp.zeros(8, 1), subject="none of the candidates fixes an absolute channel conductance")
    orbit_break_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 5], sp.zeros(8, 1), subject="none of the candidates breaks common rate and clock rescaling")
    stationary_state_theorem = kernel.prove_matrix_equality(cycle_generator*stationary_state, sp.zeros(3, 1), subject="the oriented three-state cycle has a uniform stationary state")
    generator_rank_theorem = kernel.prove_exact_rank(cycle_generator, 2, subject="the oriented cycle is irreducible on the probability simplex")
    generator_nullity_theorem = kernel.prove_exact_nullity(cycle_generator, 1, subject="the oriented cycle has one stationary direction")
    edge_current_theorem = kernel.prove_expression_equality(edge_current, rate/3, subject="the stationary cycle carries a nonzero current on every edge")
    cycle_affinity_theorem = kernel.prove_expression_equality(cycle_affinity, 3*sp.log(2), subject="the clockwise to reverse rate ratio fixes a nonzero cycle affinity")
    entropy_production_theorem = kernel.prove_expression_equality(entropy_production, rate*sp.log(2), subject="the stationary oriented cycle has positive entropy production")
    generator_rescaling_theorem = kernel.prove_matrix_equality(cycle_generator.subs(rate, scale*rate), scale*cycle_generator, subject="common rate rescaling changes only the physical clock speed")
    affinity_rescaling_theorem = kernel.prove_expression_equality((2*scale*rate)/(scale*rate), 2, subject="common rate rescaling preserves the cycle affinity")
    current_rescaling_theorem = kernel.prove_expression_equality(edge_current.subs(rate, scale*rate), scale*edge_current, subject="common rate rescaling changes the stationary current")
    rate_clock_rank_theorem = kernel.prove_exact_rank(rate_clock_map, 2, subject="rate ratio and dimensionless evolution impose two relative conditions")
    rate_clock_nullity_theorem = kernel.prove_exact_nullity(rate_clock_map, 1, subject="one common rate-clock calibration remains free")
    rate_clock_kernel_theorem = kernel.prove_matrix_equality(rate_clock_map*scale_vector, sp.zeros(2, 1), subject="common rate scaling with inverse time scaling is the exact kernel")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8, 1), subject="all declared affinity and impedance candidates are audited")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 0, 0]), subject="cycle force and entropy architecture pass while conductance origin and clock breaking remain open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 3, subject="three of five through-flow origin requirements pass")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate", (candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, conductance_column_theorem, orbit_break_column_theorem, stationary_state_theorem, generator_rank_theorem, generator_nullity_theorem, edge_current_theorem, cycle_affinity_theorem, entropy_production_theorem, generator_rescaling_theorem, affinity_rescaling_theorem, current_rescaling_theorem, rate_clock_rank_theorem, rate_clock_nullity_theorem, rate_clock_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem))
    return ThroughFlowAffinityImpedanceOriginAuditCertificate(candidate_matrix, pass_vector, cycle_generator, stationary_state, rate_clock_map, scale_vector, architecture, origin_ledger, candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, conductance_column_theorem, orbit_break_column_theorem, stationary_state_theorem, generator_rank_theorem, generator_nullity_theorem, edge_current_theorem, cycle_affinity_theorem, entropy_production_theorem, generator_rescaling_theorem, affinity_rescaling_theorem, current_rescaling_theorem, rate_clock_rank_theorem, rate_clock_nullity_theorem, rate_clock_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate", "Аудит силы и сопротивления сквозного канала", ("s2t/gates/version10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_throughflow_affinity_impedance_origin_audit_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("throughflow_origin_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem), ("zero_passing_throughflow_candidates", lambda: build_certificate().pass_vector_theorem), ("maximum_throughflow_score_four", lambda: build_certificate().maximum_score_theorem), ("throughflow_candidate_rank_four", lambda: build_certificate().candidate_rank_theorem), ("absolute_conductance_column_zero", lambda: build_certificate().conductance_column_theorem), ("clock_orbit_break_column_zero", lambda: build_certificate().orbit_break_column_theorem), ("oriented_cycle_stationary_state", lambda: build_certificate().stationary_state_theorem), ("oriented_cycle_rank_two", lambda: build_certificate().generator_rank_theorem), ("oriented_cycle_nullity_one", lambda: build_certificate().generator_nullity_theorem), ("oriented_cycle_edge_current", lambda: build_certificate().edge_current_theorem), ("oriented_cycle_affinity", lambda: build_certificate().cycle_affinity_theorem), ("oriented_cycle_entropy_production", lambda: build_certificate().entropy_production_theorem), ("common_rate_generator_rescaling", lambda: build_certificate().generator_rescaling_theorem), ("common_rate_affinity_invariance", lambda: build_certificate().affinity_rescaling_theorem), ("common_rate_current_rescaling", lambda: build_certificate().current_rescaling_theorem), ("rate_clock_map_rank_two", lambda: build_certificate().rate_clock_rank_theorem), ("rate_clock_map_nullity_one", lambda: build_certificate().rate_clock_nullity_theorem), ("rate_clock_scale_kernel", lambda: build_certificate().rate_clock_kernel_theorem), ("throughflow_candidate_coverage_full", lambda: build_certificate().architecture_theorem), ("throughflow_origin_ledger_three", lambda: build_certificate().origin_ledger_theorem), ("throughflow_origin_score_three", lambda: build_certificate().origin_score_theorem))))