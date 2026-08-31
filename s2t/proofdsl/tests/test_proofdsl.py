from __future__ import annotations

import sympy as sp
import pytest

from s2t.proofdsl.examples.version8_connector_no_go import build_certificate
from s2t.proofdsl.examples.version8_fixed_algebra import (
    build_certificate as build_fixed_algebra_certificate,
)
from s2t.proofdsl.examples.version8_linking_qms import (
    build_certificate as build_linking_qms_certificate,
)
from s2t.proofdsl.examples.version8_gauge_twirl_kraus import (
    build_certificate as build_gauge_twirl_kraus_certificate,
)
from s2t.proofdsl.examples.version8_kraus_parent_hessian import (
    build_certificate as build_kraus_parent_hessian_certificate,
)
from s2t.proofdsl.examples.version8_cross_covariance import (
    build_certificate as build_cross_covariance_certificate,
)
from s2t.proofdsl.examples.version8_stinespring import (
    build_certificate as build_stinespring_certificate,
)
from s2t.proofdsl.examples.version8_noise_clock import (
    build_certificate as build_noise_clock_certificate,
)
from s2t.proofdsl.examples.version8_full_primitive import (
    build_certificate as build_full_primitive_certificate,
)
from s2t.proofdsl.examples.version8_kms_selector import (
    build_certificate as build_kms_selector_certificate,
)
from s2t.proofdsl.examples.version8_modular_bohr import build_certificate as build_modular_bohr_certificate
from s2t.proofdsl.examples.version8_page_wootters_history import (
    build_certificate as build_page_wootters_history_certificate,
)
from s2t.proofdsl.examples.version8_autonomous_clock_unitary import (
    build_certificate as build_autonomous_clock_unitary_certificate,
)
from s2t.proofdsl.examples.version8_microscopic_interaction_hamiltonian import (
    build_certificate as build_microscopic_interaction_hamiltonian_certificate,
)
from s2t.proofdsl.examples.version8_trace_dual_cross_coupling import (
    build_certificate as build_trace_dual_cross_coupling_certificate,
)
from s2t.proofdsl.examples.version8_metric_dual_environment_parent_action import (
    build_certificate as build_metric_dual_environment_parent_action_certificate,
)
from s2t.proofdsl.examples.version8_full_noise_cotangent_carrier import (
    build_certificate as build_full_noise_cotangent_carrier_certificate,
)
from s2t.proofdsl.examples.version8_full_noise_trace_frame import (
    build_certificate as build_full_noise_trace_frame_certificate,
)
from s2t.proofdsl.examples.version8_field_to_noise_chain_map_pullback_metric import (
    build_certificate as build_field_to_noise_chain_map_pullback_metric_certificate,
)
from s2t.proofdsl.examples.version8_field_noise_metric_to_parent_hessian_comparison import (
    build_certificate as build_field_noise_metric_to_parent_hessian_comparison_certificate,
)
from s2t.proofdsl.examples.version8_spacetime_kinetic_factorization_and_gauge_fixing import (
    build_certificate as build_spacetime_kinetic_factorization_and_gauge_fixing_certificate,
)
from s2t.proofdsl.examples.version8_transverse_noise_mobility_environment_origin import (
    build_certificate as build_transverse_noise_mobility_environment_origin_certificate,
)
from s2t.proofdsl.examples.version8_full_field_kinetic_supermetric_assembly import (
    build_certificate as build_full_field_kinetic_supermetric_assembly_certificate,
)
from s2t.proofdsl.examples.version8_full_field_kinetic_relative_weight_parent_origin import (
    build_certificate as build_full_field_kinetic_relative_weight_parent_origin_certificate,
)
from s2t.proofdsl.examples.version8_full_field_a4_dirac_lift_origin import (
    build_certificate as build_full_field_a4_dirac_lift_origin_certificate,
)
from s2t.proofdsl.examples.version8_full_42_carrier_base_k_determinant_compatibility import (
    build_certificate as build_full_42_carrier_base_k_determinant_compatibility_certificate,
)
from s2t.proofdsl.examples.version8_full_42_carrier_bv_vacuum_quotient import (
    build_certificate as build_full_42_carrier_bv_vacuum_quotient_certificate,
)
from s2t.proofdsl.examples.version8_gauge_invariant_vacuum_hessian_reconstruction import (
    build_certificate as build_gauge_invariant_vacuum_hessian_reconstruction_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_flat_direction_parent_lift import (
    build_certificate as build_horizontal_flat_direction_parent_lift_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_determinant_line_admission import (
    build_certificate as build_horizontal_phase_determinant_line_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_heavy_arrow_cycle_admission import (
    build_certificate as build_horizontal_phase_heavy_arrow_cycle_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_real_oriented_cycle_admission import (
    build_certificate as build_horizontal_phase_real_oriented_cycle_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_complex_symplectic_polarization_admission import (
    build_certificate as build_horizontal_phase_complex_symplectic_polarization_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission import (
    build_certificate as build_horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_cotangent_doubled_quiver_parent_admission import (
    build_certificate as build_horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate,
)
from s2t.proofdsl.examples.version8_horizontal_phase_cotangent_complex_structure_metric_selector import (
    build_certificate as build_horizontal_phase_cotangent_complex_structure_metric_selector_certificate,
)
from s2t.proofdsl.examples.version8_full_noise_gksl import (
    build_certificate as build_full_noise_gksl_certificate,
)
from s2t.proofdsl.examples.version8_full_noise_repeated_interaction import build_certificate as build_full_noise_repeated_interaction_certificate
from s2t.proofdsl.examples.version8_full_noise_physical_time_scale import build_certificate as build_full_noise_physical_time_scale_certificate
from s2t.proofdsl.examples.version8_full_noise_toeplitz_ancilla_chain import build_certificate as build_full_noise_toeplitz_ancilla_chain_certificate
from s2t.proofdsl.examples.version8_vacuum_chain_parent_state_and_local_hamiltonian_origin import build_certificate as build_vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate
from s2t.proofdsl.examples.version8_index_balanced_ancilla_conveyor import build_certificate as build_index_balanced_ancilla_conveyor_certificate
from s2t.proofdsl.examples.version8_static_local_hamiltonian_embedding_no_go import build_certificate as build_static_local_hamiltonian_embedding_no_go_certificate
from s2t.proofdsl.examples.spinodal_threshold import (
    build_certificate as build_spinodal_certificate,
)
from s2t.proofdsl.gates import GateSpec, Obligation, verify_gate
from s2t.proofdsl.kernel import Proposition, Theorem, kernel
from s2t.proofdsl.lindblad import LindbladGenerator
from s2t.proofdsl.structures import MatrixRepresentation, Morphism, Space
from s2t.proofdsl.sympy_backend import exact_rank, solve_intertwiners
from s2t.proofdsl import z3_backend
from s2t.proofdsl.verify import verify_all


def test_theorem_constructor_is_kernel_private() -> None:
    with pytest.raises(PermissionError):
        Theorem(Proposition.make("fake", "forbidden"), "user_rule")


def test_illegal_morphism_shape_is_unrepresentable() -> None:
    source = Space("A", 2)
    target = Space("B", 3)
    with pytest.raises(ValueError):
        Morphism("bad", source, target, sp.eye(2))


def test_composition_checks_endpoints() -> None:
    a = Space("A", 2)
    b = Space("B", 2)
    c = Space("C", 2)
    f = Morphism("f", a, b, sp.eye(2))
    g = Morphism("g", c, a, sp.eye(2))
    with pytest.raises(TypeError):
        f.then(g)


def test_exact_matrix_equality_and_rank() -> None:
    matrix = sp.Matrix([[sp.Rational(1, 2), 0], [0, 1]])
    theorem = kernel.prove_matrix_equality(
        2 * matrix, sp.diag(1, 2), subject="rational normalization"
    )
    assert theorem.rule == "exact_sympy_reduction"
    assert exact_rank(matrix) == 2
    with pytest.raises(ValueError):
        Morphism("float", Space("F", 1), Space("F", 1), [[0.5]])


def test_exact_intertwiner_solver() -> None:
    source_space = Space("source", 2)
    target_space = Space("target", 2)
    sigma_z = sp.diag(1, -1)
    source = MatrixRepresentation("source_rep", source_space, [("z", sigma_z)])
    target = MatrixRepresentation("target_rep", target_space, [("z", sigma_z)])
    solution = solve_intertwiners(source, target)
    assert solution.dimension == 2
    assert all(sigma_z * item == item * sigma_z for item in solution.basis)
    identity = Morphism("identity", source_space, target_space, sp.eye(2))
    theorem = kernel.prove_intertwiner(identity, source, target)
    assert theorem.proposition.kind == "intertwiner"


def test_version8_rank_no_go_is_exact() -> None:
    certificate = build_certificate()
    assert certificate.endpoint.space.dimension == 21
    assert certificate.transfer.space.dimension == 20
    assert certificate.hom_dimension == 13
    assert certificate.maximum_rank == 9
    assert certificate.theorem.proposition.kind == "intertwiner_rank_no_go"


def test_spinodal_threshold_is_exact() -> None:
    certificate = build_spinodal_certificate()
    assert certificate.curvature == sp.Rational(9, 2) - 3 * sp.Symbol(
        "beta", positive=True
    ) / 7
    assert certificate.threshold == sp.Rational(21, 2)
    assert certificate.threshold_theorem.proposition.kind == "unique_linear_zero"


def test_version8_fixed_algebra_is_exact() -> None:
    certificate = build_fixed_algebra_certificate()
    assert certificate.gauge_commutant_dimension == 13
    assert certificate.one_sided_kernel_dimension == 4
    assert certificate.full_fixed_dimension == 2
    assert certificate.quark_projector_rank == 12
    assert certificate.lepton_projector_rank == 9
    assert certificate.fixed_theorem.proposition.kind == "exact_linear_kernel"


def test_version8_linking_qms_is_exact() -> None:
    certificate = build_linking_qms_certificate()
    assert certificate.incidence_rank == 10
    assert certificate.linking_fixed_dimension == 41
    assert certificate.gksl_theorem.proposition.kind == "gksl_well_formed"
    assert certificate.trace_theorem.proposition.kind == "trace_preserving_generator"
    assert certificate.unital_theorem.proposition.kind == "unital_generator"
    assert certificate.corner_formula_theorem.proposition.data["basis_size"] == 221


def test_version8_gauge_twirl_kraus_bridge_is_exact() -> None:
    certificate = build_gauge_twirl_kraus_certificate()
    assert certificate.cross_real_dimension == 12
    assert certificate.internal_control_dimension == 8
    assert certificate.cross_central_matrix == sp.ImmutableMatrix(
        [[1, -2 / sp.sqrt(3)], [-2 / sp.sqrt(3), sp.Rational(4, 3)]]
    )
    assert certificate.internal_central_matrix == sp.zeros(2)
    assert certificate.gauge_covariance_theorem.proposition.data[
        "invariant_linear_dimension"
    ] == 0
    assert certificate.cross_kernel_theorem.proposition.data["nullity"] == 1


def test_version8_kraus_parent_hessian_is_exact() -> None:
    certificate = build_kraus_parent_hessian_certificate()
    assert certificate.cross_coefficient == sp.Rational(7, 36)
    assert certificate.cross_total_coefficient == sp.Rational(7, 3)
    assert certificate.gaussian_unit_rate == sp.Rational(35, 96)
    assert certificate.bridge_signature_theorem.proposition.data == {
        "negative": 0,
        "zero": 15,
        "positive": 12,
        "dimension": 27,
    }
    assert certificate.origin_signature_theorem.proposition.data["negative"] == 7
    assert certificate.vacuum_signature_theorem.proposition.data["positive"] == 27


def test_version8_cross_covariance_axis_is_exact() -> None:
    certificate = build_cross_covariance_certificate()
    assert certificate.pair_matrix.shape == (2, 2)
    assert certificate.positivity_theorem.proposition.data[
        "distinct_eigenvalues"
    ] is True
    assert certificate.repetition_theorem.proposition.data["shape"] == [12, 12]
    assert certificate.decoupling_theorem.proposition.data["shape"] == [12, 15]
    angle = sp.N(certificate.soft_axis_angle_radians * 180 / sp.pi, 15)
    assert abs(float(angle) - 55.45091552083214) < 1.0e-12


def test_version8_minimal_stinespring_carrier_is_exact() -> None:
    certificate = build_stinespring_certificate()
    assert certificate.gram_spectrum == ((0, 9), (1, 6), (2, 3), (3, 2), (6, 1))
    assert certificate.maximum_step == sp.Rational(1, 6)
    assert certificate.channel_theorem.proposition.kind == "kraus_family_on_window"
    assert certificate.trace_theorem.proposition.kind == (
        "trace_preserving_kraus_family_on_window"
    )
    assert certificate.endpoint_theorem.proposition.data["checked_matrix_units"] == 221
    assert certificate.interior_rank_theorem.proposition.data["rank"] == 13
    assert certificate.minimal_environment_theorem.proposition.data[
        "environment_dimension"
    ] == 13
    assert certificate.semigroup_no_go_theorem.proposition.kind == "matrix_inequality"


def test_version8_intrinsic_noise_clock_is_exact() -> None:
    certificate = build_noise_clock_certificate()
    assert certificate.kernel_dimension == 46
    assert certificate.unit_gap == sp.Rational(1, 2)
    assert certificate.maximum_decay == 8
    assert certificate.dissipative_projector_norm_squared == 72
    assert sum(multiplicity for _, multiplicity in certificate.spectrum) == 221
    assert certificate.semigroup_theorem.proposition.kind == "matrix_exponential_semigroup"
    assert certificate.collision_limit_theorem.proposition.data["scaling"] == "p=u/n"


def test_version8_full_primitive_qms_is_exact() -> None:
    certificate = build_full_primitive_certificate()
    assert certificate.jump_count == 25
    assert certificate.group_sizes == (1, 8, 3, 1, 6, 6)
    assert certificate.endpoint_theorem.proposition.data["checked_matrix_units"] == 221
    assert certificate.scalar_fixed_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.qlyr_closure_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.xldr_closure_theorem.proposition.data["fixed_dimension"] == 1
    assert certificate.positive_weight_theorem.proposition.data[
        "relative_weights_selected"
    ] is False
    assert certificate.gap_theorem.proposition.kind == "strict_finite_dimensional_decay_gap"


def test_version8_kms_selector_no_go_is_exact() -> None:
    certificate = build_kms_selector_certificate()
    assert certificate.transfer_traces == (13, 6, 6)
    assert certificate.transfer_jump_count == 13
    assert certificate.central_state_theorem.proposition.data["condition"] == "a=b=1/21"
    assert certificate.bohr_split_theorem.proposition.data["pair_count"] == 13
    assert certificate.conditional_ratio_theorem.proposition.data["ratio"] == "exp(-beta_Delta)"
    assert certificate.conditional_ratio_theorem.proposition.data["uniquely_selected"] is False

def test_version8_modular_bohr_parent_is_exact() -> None:
    c=build_modular_bohr_certificate()
    assert c.transfer_count == 13
    assert c.forward_ratio == sp.exp(-2) and c.reverse_ratio == sp.exp(2)
    assert c.forward_primitive_theorem.proposition.data["fixed_dimension"] == 1


def test_version8_page_wootters_stinespring_history_is_exact() -> None:
    certificate = build_page_wootters_history_certificate()
    assert certificate.steps == 2
    assert certificate.clock_dimension == 3
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension_per_tick == 13
    assert certificate.branch_count_bounds == (1, 13, 169)
    assert certificate.padded_data_dimension == 3549
    assert certificate.full_history_dimension == 10647
    assert certificate.recovery_theorem.proposition.data["slice_traces"] == (
        "1",
        "1",
        "1",
    )
    assert certificate.history_parent_theorem.proposition.data[
        "zero_mode_family_dimension"
    ] == 21
    assert certificate.extension_freedom_theorem.proposition.data[
        "unconstrained_complement_dimension"
    ] == 252


def test_version8_autonomous_clock_unitary_no_go_is_exact() -> None:
    certificate = build_autonomous_clock_unitary_certificate()
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension == 13
    assert certificate.complement_dimension == 252
    assert certificate.extension_parameter_dimension == 63504
    assert certificate.real_even_extension_count_lower_bound == 2
    assert certificate.ambiguity_theorem.proposition.data[
        "complex_phase_family"
    ] == "U(1)"
    assert certificate.ambiguity_theorem.proposition.data[
        "real_even_surviving_choices"
    ] == ("+1", "-1")
    assert certificate.ambiguity_theorem.proposition.data[
        "unique_covariant_unitary_extension"
    ] is False


def test_version8_microscopic_interaction_hamiltonian_is_exact() -> None:
    certificate = build_microscopic_interaction_hamiltonian_certificate()
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension == 13
    assert certificate.ambient_dimension == 273
    assert certificate.jump_dimension == 12
    assert certificate.full_commutant_dimension == 8
    assert certificate.symmetric_rate_metric_dimension == 4
    assert certificate.finite_step_witness == (0, 0)
    assert certificate.typed_theorem.proposition.data["shape"] == [273, 273]
    assert certificate.tangent_theorem.proposition.kind == "kraus_family_gksl_tangent"
    assert certificate.covariance_theorem.proposition.kind == (
        "orthogonal_star_interaction_covariance"
    )
    assert certificate.coupling_commutant_theorem.proposition.data[
        "symmetric_commutant_dimension"
    ] == 4
    assert certificate.finite_step_no_go_theorem.proposition.kind == (
        "matrix_inequality"
    )


def test_version8_trace_dual_cross_coupling_is_exact() -> None:
    certificate = build_trace_dual_cross_coupling_certificate()
    assert certificate.field_metric_eigenvalue == 3
    assert certificate.canonical_rate_eigenvalue == sp.Rational(1, 3)
    assert certificate.interaction_coupling_eigenvalue == 1 / sp.sqrt(3)
    assert certificate.field_metric_theorem.proposition.data["shape"] == [12, 12]
    assert certificate.generator_scaling_theorem.proposition.data["basis_size"] == 441
    assert certificate.environment_equivalence_theorem.proposition.data[
        "orthogonal_environment_relabelling"
    ] is True
    assert certificate.environment_equivalence_theorem.proposition.data[
        "reduced_channel_unique_up_to_scale"
    ] is True
    assert certificate.polar_axis_compatibility_theorem.proposition.kind == (
        "matrix_equality"
    )


def test_version8_metric_dual_environment_parent_action_no_go_is_exact() -> None:
    certificate = build_metric_dual_environment_parent_action_certificate()
    data = certificate.parent_underdetermination_theorem.proposition.data
    assert data["same_field_restriction"] is True
    assert data["positive_gauge_compatible_completions"] == 2
    assert data["completions_not_scale_equivalent"] is True
    assert data["field_action_selects_unique_bath_rate"] is False
    assert data["riesz_equation_selects_unique_rate"] is True
    assert data["riesz_condition_is_additional"] is True
    assert certificate.dynamical_witness == (0, 8)


def test_version8_full_noise_cotangent_carrier_is_exact() -> None:
    certificate = build_full_noise_cotangent_carrier_certificate()
    assert certificate.mixed_real_dimension == 42
    assert certificate.naive_uniform_complex_real_dimension == 54
    assert certificate.current_jump_dimension == 25
    assert certificate.missing_real_directions == 17


def test_version8_full_noise_trace_frame_is_exact() -> None:
    certificate = build_full_noise_trace_frame_certificate()
    assert certificate.orbit_dimensions == (1, 4, 5, 5)
    assert certificate.full_frame_dimension == 42
    assert certificate.trace_metric.rank() == 42
    assert certificate.added_linking_directions + certificate.added_internal_directions == 17


def test_version8_field_to_noise_chain_map_pullback_metric_is_exact() -> None:
    certificate = build_field_to_noise_chain_map_pullback_metric_certificate()
    assert certificate.map_matrix == sp.eye(42)
    assert certificate.pullback_metric.rank() == 42
    assert certificate.pullback_metric * certificate.pullback_dual == sp.eye(42)
    assert certificate.gauge_action_count == 12
    assert certificate.intertwining_check_count == 504


def test_version8_field_noise_metric_to_parent_hessian_comparison_is_exact() -> None:
    certificate = build_field_noise_metric_to_parent_hessian_comparison_certificate()
    assert certificate.transfer_origin_hessian.rank() == 30
    assert certificate.constant_field_parent_hessian.rank() == 30
    assert certificate.constant_field_parent_hessian[30:, 30:] == sp.zeros(12)
    assert certificate.trace_metric.rank() == 42


def test_version8_spacetime_kinetic_factorization_is_exact() -> None:
    certificate = build_spacetime_kinetic_factorization_and_gauge_fixing_certificate()
    assert certificate.ungauged_hessian.rank() == 36
    assert 48 - certificate.ungauged_hessian.rank() == 12
    assert certificate.gauge_fixed_hessian.rank() == 48
    assert certificate.gauge_fixed_hessian * certificate.gauge_fixed_inverse == sp.eye(48)


def test_version8_transverse_noise_mobility_environment_origin_is_exact() -> None:
    certificate = build_transverse_noise_mobility_environment_origin_certificate()
    assert certificate.canonical_covariance.rank() == 12
    assert certificate.canonical_transverse_mobility.rank() == 36
    assert certificate.rescaled_transverse_mobility == 4 * certificate.canonical_transverse_mobility


def test_version8_full_field_kinetic_supermetric_assembly_is_exact() -> None:
    certificate = build_full_field_kinetic_supermetric_assembly_certificate()
    assert certificate.scalar_principal_symbol.shape == (120, 120)
    assert certificate.gauge_principal_symbol.shape == (48, 48)
    assert certificate.ungauged_supermetric.shape == (168, 168)
    assert certificate.gauge_fixed_supermetric.shape == (168, 168)
    assert certificate.ungauged_rank_theorem.proposition.kind == "expression_equality"
    assert certificate.ungauged_nullity_theorem.proposition.kind == "expression_equality"
    assert certificate.gauge_fixed_rank_theorem.proposition.kind == "expression_equality"
    assert certificate.sector_mixing_block == sp.zeros(120, 48)
    assert not certificate.gauge_fixed_supermetric.atoms(sp.Float)


def test_version8_full_field_kinetic_relative_weight_parent_origin_is_exact() -> None:
    certificate = build_full_field_kinetic_relative_weight_parent_origin_certificate()
    assert certificate.scalar_coefficient == 2
    assert certificate.gauge_coefficient == -sp.Rational(2, 3)
    assert certificate.scalar_to_gauge_ratio == 3
    assert certificate.gamma_five == sp.diag(1, 1, -1, -1)
    assert not any(matrix.atoms(sp.Float) for matrix in certificate.gamma_matrices)


def test_version8_full_field_a4_dirac_lift_origin_is_exact() -> None:
    certificate = build_full_field_a4_dirac_lift_origin_certificate()
    assert certificate.internal_check_count == 42
    assert certificate.external_symbol_one**2 == sp.eye(4)
    assert certificate.external_symbol_two**2 == 4 * sp.eye(4)
    assert not certificate.external_symbol_two.atoms(sp.Float)


def test_version8_full_42_carrier_base_k_determinant_compatibility_is_exact() -> None:
    certificate = build_full_42_carrier_base_k_determinant_compatibility_certificate()
    assert certificate.scalar_hessian.rank() == 28
    assert certificate.gauge_mass_gram.rank() == 3
    assert certificate.bosonic_fourth_moment == sp.Rational(4659176, 3249)
    assert certificate.finite_fermion_fourth_moment == 46
    assert not certificate.scalar_hessian.atoms(sp.Float)


def test_version8_full_42_carrier_bv_vacuum_quotient_is_exact() -> None:
    certificate = build_full_42_carrier_bv_vacuum_quotient_certificate()
    assert certificate.physical_chiral_projector.rank() == 42
    assert certificate.physical_fermion_fourth_moment == 92
    assert certificate.gauge_orbit_coordinates.rank() == 3
    assert certificate.orbit_hessian_restriction.rank() == 3
    assert sp.trace(certificate.orbit_hessian_restriction) == 34
    assert certificate.fixed_background_candidate_numerator == sp.Rational(4360268, 3249)
    assert not certificate.orbit_hessian_restriction.atoms(sp.Float)


def test_version8_gauge_invariant_vacuum_hessian_reconstruction_is_exact() -> None:
    certificate = build_gauge_invariant_vacuum_hessian_reconstruction_certificate()
    assert certificate.orbit_metric == 14 * sp.eye(3)
    assert certificate.orbit_projector.rank() == 3
    assert certificate.horizontal_projector.rank() == 27
    assert certificate.quotient_hessian.rank() == 26
    assert len(certificate.quotient_hessian.nullspace()) == 4
    assert certificate.scalar_fourth_moment == sp.Rational(1118917, 882)
    assert certificate.bosonic_fourth_moment == sp.Rational(226371884, 159201)
    assert certificate.full_quadratic_numerator == sp.Rational(211725392, 159201)
    assert not certificate.quotient_hessian.atoms(sp.Float)


def test_version8_horizontal_flat_direction_parent_lift_is_exact() -> None:
    certificate = build_horizontal_flat_direction_parent_lift_certificate()
    assert certificate.phase_coordinates.rank() == 2
    assert certificate.phase_metric == sp.diag(6, 20)
    assert certificate.orbit_phase_coupling == sp.Matrix([[0, 0], [0, 0], [-6, 8]])
    assert certificate.horizontal_phase_direction == sp.Matrix(
        [0, 3, 0, 0, 0, 0, 0, -sp.Rational(1, 2), 0, sp.Rational(1, 2)] + [0] * 20
    )
    assert not certificate.phase_coordinates.atoms(sp.Float)


def test_version8_horizontal_phase_determinant_line_admission_is_exact() -> None:
    certificate = build_horizontal_phase_determinant_line_admission_certificate()
    assert certificate.cofactor_vector == sp.Matrix(
        [0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0]
    )
    assert certificate.source_determinant_charge == -2
    assert certificate.target_determinant_charge == -2
    assert certificate.relative_determinant_charge == 0
    assert certificate.invariant_functional_dimension == 0
    assert not certificate.cofactor_vector.atoms(sp.Float)


def test_version8_horizontal_phase_heavy_arrow_cycle_admission_is_exact() -> None:
    certificate = build_horizontal_phase_heavy_arrow_cycle_admission_certificate()
    assert certificate.graph_rank == 8
    assert certificate.cycle_rank == 3
    assert certificate.incidence_cycle_rank == 0
    assert certificate.heavy_cycle_rank == 3
    assert certificate.boundary_matrix * certificate.cycle_basis == sp.zeros(9, 3)
    assert certificate.cycle_basis[0, :] == sp.zeros(1, 3)
    assert certificate.target_phase_weights * certificate.cycle_basis == sp.zeros(1, 3)
    assert not certificate.cycle_basis.atoms(sp.Float)


def test_version8_horizontal_phase_real_oriented_cycle_admission_is_exact() -> None:
    certificate = build_horizontal_phase_real_oriented_cycle_admission_certificate()
    assert certificate.raising_operator**2 == sp.zeros(9)
    assert certificate.reverse_operator**2 == sp.zeros(9)
    assert certificate.grading * certificate.real_completion + certificate.real_completion * certificate.grading == sp.zeros(9)
    assert certificate.odd_trace_moments == sp.zeros(1, 3)
    assert certificate.even_trace_moments == sp.Matrix([[22, 110, 682]])
    assert certificate.physical_transfer_real_dimension == 40
    assert certificate.independent_reverse_real_dimension == 80
    assert certificate.independent_reverse_excess == 40
    assert not certificate.phased_real_completion.atoms(sp.Float)


def test_version8_horizontal_phase_complex_symplectic_polarization_admission_is_exact() -> None:
    certificate = build_horizontal_phase_complex_symplectic_polarization_admission_certificate()
    assert certificate.invariant_form_dimension == 11
    assert certificate.maximum_invariant_rank == 14
    assert certificate.minimum_radical_dimension == 6
    assert certificate.first_invariant_form.rank() == 14
    assert certificate.first_invariant_form.T == -certificate.first_invariant_form
    assert certificate.first_invariant_form != certificate.second_invariant_form
    assert certificate.missing_dual_complex_dimension == 6
    assert certificate.completed_complex_dimension == 26
    assert not certificate.first_invariant_form.atoms(sp.Float)


def test_version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_is_exact() -> None:
    certificate = build_horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate()
    assert certificate.completed_complex_dimension == 26
    assert certificate.completed_real_dimension == 52
    assert certificate.invariant_form_dimension == 23
    assert certificate.standard_form.rank() == 26
    assert certificate.standard_form.T == -certificate.standard_form
    assert certificate.standard_form * (-certificate.standard_form) == sp.eye(26)
    assert certificate.standard_form != certificate.alternative_form
    assert certificate.endpoint_multiplicity_deficit == 3
    assert certificate.new_complex_directions == 6
    assert certificate.first_field.T * certificate.standard_form * certificate.second_field == sp.ones(1, 1)
    assert not certificate.standard_form.atoms(sp.Float)


def test_version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_is_exact() -> None:
    certificate = build_horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate()
    assert certificate.symplectic_form.rank() == 26
    assert certificate.moment_span_dimension == 13
    assert certificate.moment_span_matrix * certificate.generator_relation == sp.zeros(676, 1)
    assert all(matrix.T == matrix for matrix in certificate.moment_quadratic_matrices)
    assert certificate.cotangent_phase_action.T * certificate.symplectic_form * certificate.cotangent_phase_action == certificate.symplectic_form
    assert not certificate.moment_vector.atoms(sp.Float)


def test_version8_horizontal_phase_cotangent_complex_structure_metric_selector_is_exact() -> None:
    certificate = build_horizontal_phase_cotangent_complex_structure_metric_selector_certificate()
    assert certificate.pulled_trace_metric.rank() == 42
    assert len(certificate.pulled_trace_metric.nullspace()) == 10
    assert certificate.pulled_transfer_metric.rank() == 30
    assert len(certificate.pulled_transfer_metric.nullspace()) == 22
    assert certificate.first_complex_structure**2 == -sp.eye(52)
    assert certificate.second_complex_structure**2 == -sp.eye(52)
    assert certificate.first_metric_extension != certificate.second_metric_extension
    assert not certificate.second_metric_extension.atoms(sp.Float)


def test_version8_full_noise_42_jump_gksl_is_exact() -> None:
    certificate = build_full_noise_gksl_certificate()
    assert (certificate.jump_count, certificate.base_jump_count, certificate.added_jump_count) == (42, 25, 17)
    assert certificate.scalar_fixed_theorem.proposition.data["fixed_algebra_dimension"] == 1
    assert certificate.scalar_fixed_theorem.proposition.data["primitive"] is True


def test_version8_full_noise_repeated_interaction_is_exact() -> None:
    certificate=build_full_noise_repeated_interaction_certificate()
    assert (certificate.system_dimension,certificate.jump_dimension,certificate.environment_dimension,certificate.ambient_dimension)==(21,42,43,903)
    assert certificate.closure_theorem.proposition.data["closure_checks"]==504


def test_version8_full_noise_physical_time_scale_no_go_is_exact() -> None:
    certificate = build_full_noise_physical_time_scale_certificate()
    data = certificate.physical_time_no_go_theorem.proposition.data
    assert data["invariant_parameter"] == "g^2 t"
    assert data["absolute_seconds_selected"] is False
    assert data["hbar_alone_sufficient"] is False
    assert certificate.coupling_freedom_theorem.certificate["derivative"] == "2*g"
    assert certificate.energy_anchor_theorem.certificate["derivative"] == "-hbar/E_***2"


def test_version8_full_noise_toeplitz_ancilla_chain_is_exact() -> None:
    certificate = build_full_noise_toeplitz_ancilla_chain_certificate()
    assert (certificate.system_dimension, certificate.jump_dimension, certificate.cell_dimension) == (21, 42, 43)
    chain = certificate.chain_theorem.proposition.data
    assert chain["global_step_unitary"] is True
    assert chain["used_cell_revisited"] is False
    assert chain["product_vacuum_supplies_fresh_cells"] is True
    assert certificate.recovery_theorem.proposition.data["valid_steps"] == "all n >= 0"
    boundary = certificate.resource_boundary_theorem.proposition.data
    assert boundary["external_step_by_step_reset_required"] is False
    assert boundary["strong_physical_autonomy"] is False


def test_version8_vacuum_chain_parent_and_local_hamiltonian_origin_is_exact() -> None:
    certificate = build_vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate()
    assert (certificate.cell_dimension, certificate.excitation_dimension) == (43, 42)
    parent = certificate.parent_theorem.proposition.data
    assert parent["finite_volume_ground_dimension"] == 1
    assert parent["finite_volume_gap"] == 1
    assert parent["translation_invariant_interaction"] is True
    assert certificate.shift_index_theorem.proposition.data[
        "multiplicative_index"
    ] == 43
    assert certificate.global_index_theorem.proposition.data[
        "global_step_multiplicative_index"
    ] == 43
    no_go = certificate.local_hamiltonian_no_go_theorem.proposition.data
    assert no_go["hamiltonian_path_multiplicative_index"] == 1
    assert no_go["exact_local_hamiltonian_generator_exists"] is False
    assert no_go["strong_autonomy_closed"] is False


def test_version8_index_balanced_ancilla_conveyor_is_exact() -> None:
    certificate = build_index_balanced_ancilla_conveyor_certificate()
    assert certificate.cell_dimension == 43
    assert certificate.total_index == 1
    circuit = certificate.swap_circuit_theorem.proposition.data
    assert circuit["circuit_depth"] == 2
    assert circuit["nearest_neighbour"] is True
    assert circuit["exact_counterpropagating_shifts"] is True
    hamiltonian = certificate.local_hamiltonian_theorem.proposition.data
    assert hamiltonian["piecewise_time_dependent_local_hamiltonian"] is True
    assert hamiltonian["single_time_independent_local_hamiltonian_derived"] is False
    recovery = certificate.recovery_theorem.proposition.data
    assert recovery["active_chain_supplies_fresh_vacuum"] is True
    assert recovery["valid_steps"] == "all finite n >= 0"


def test_version8_static_local_hamiltonian_embedding_no_go_is_exact() -> None:
    certificate = build_static_local_hamiltonian_embedding_no_go_certificate()
    assert (
        certificate.active_winding,
        certificate.spectator_winding,
        certificate.determinant_winding,
    ) == (-1, 1, 0)
    no_go = certificate.static_no_go_theorem.proposition.data
    assert no_go["periodic_scalar_exponential_winding"] == 0
    assert no_go["exact_static_hamiltonian_exists"] is False
    boundary = certificate.carrier_boundary_theorem.proposition.data
    assert boundary["piecewise_floquet_model_remains_valid"] is True
    assert boundary["clock_augmented_static_hamiltonian_excluded"] is False


def test_gate_template_requires_kernel_theorems() -> None:
    spec = GateSpec(
        "example",
        "Example",
        ("source",),
        (Obligation("identity", lambda: kernel.prove_expression_equality(1, 1, subject="one")),),
    )
    certificate = verify_gate(spec)
    assert certificate.theorem.proposition.kind == "verified_gate"
    bad = GateSpec(
        "bad",
        "Bad",
        ("source",),
        (Obligation("not_a_theorem", lambda: 1),),  # type: ignore[arg-type]
    )
    with pytest.raises(TypeError):
        verify_gate(bad)


def test_registered_gate_registry() -> None:
    result = verify_all()
    assert result["status"] == "lcf-checked"
    assert result["gate_count"] == 48
    assert result["obligation_count"] == 362


def test_lindblad_constructor_and_trace_preservation() -> None:
    space = Space("qubit", 2)
    hamiltonian = Morphism("H", space, space, sp.diag(0, 1))
    lowering = Morphism("L", space, space, sp.Matrix([[0, 1], [0, 0]]))
    generator = LindbladGenerator.make(
        "amplitude_damping", hamiltonian, [lowering], [sp.Rational(1, 3)]
    )
    rho = sp.Matrix(2, 2, sp.symbols("r0:4"))
    assert sp.simplify(sp.trace(generator.act(rho))) == 0
    assert generator.theorem.proposition.kind == "gksl_well_formed"


def test_negative_lindblad_rate_is_rejected() -> None:
    space = Space("one", 1)
    zero = Morphism("zero", space, space, sp.zeros(1))
    with pytest.raises(ValueError):
        LindbladGenerator.make("bad", zero, [zero], [-1])
    with pytest.raises(ValueError):
        LindbladGenerator.make("inexact", zero, [zero], [0.5])


def test_z3_backend_is_optional() -> None:
    assert isinstance(z3_backend.available(), bool)