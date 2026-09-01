"""Curated registry of project results already migrated to the proof eDSL."""

from __future__ import annotations

from .examples.spinodal_threshold import build_certificate as spinodal_certificate
from .examples.version8_connector_no_go import (
    build_certificate as connector_certificate,
)
from .examples.version8_fixed_algebra import (
    build_certificate as fixed_algebra_certificate,
)
from .examples.version8_linking_qms import build_certificate as linking_qms_certificate
from .examples.version8_gauge_twirl_kraus import (
    build_certificate as gauge_twirl_kraus_certificate,
)
from .examples.version8_kraus_parent_hessian import (
    build_certificate as kraus_parent_hessian_certificate,
)
from .examples.version8_cross_covariance import (
    build_certificate as cross_covariance_certificate,
)
from .examples.version8_stinespring import (
    build_certificate as stinespring_certificate,
)
from .examples.version8_noise_clock import (
    build_certificate as noise_clock_certificate,
)
from .examples.version8_full_primitive import (
    build_certificate as full_primitive_certificate,
)
from .examples.version8_kms_selector import (
    build_certificate as kms_selector_certificate,
)
from .examples.version8_modular_bohr import build_certificate as modular_bohr_certificate
from .examples.version8_page_wootters_history import (
    build_certificate as page_wootters_history_certificate,
)
from .examples.version8_autonomous_clock_unitary import (
    build_certificate as autonomous_clock_unitary_certificate,
)
from .examples.version8_microscopic_interaction_hamiltonian import (
    build_certificate as microscopic_interaction_hamiltonian_certificate,
)
from .examples.version8_trace_dual_cross_coupling import (
    build_certificate as trace_dual_cross_coupling_certificate,
)
from .examples.version8_metric_dual_environment_parent_action import (
    build_certificate as metric_dual_environment_parent_action_certificate,
)
from .examples.version8_full_noise_cotangent_carrier import (
    build_certificate as full_noise_cotangent_carrier_certificate,
)
from .examples.version8_full_noise_trace_frame import (
    build_certificate as full_noise_trace_frame_certificate,
)
from .examples.version8_field_to_noise_chain_map_pullback_metric import (
    build_certificate as field_to_noise_chain_map_pullback_metric_certificate,
)
from .examples.version8_field_noise_metric_to_parent_hessian_comparison import (
    build_certificate as field_noise_metric_to_parent_hessian_comparison_certificate,
)
from .examples.version8_spacetime_kinetic_factorization_and_gauge_fixing import (
    build_certificate as spacetime_kinetic_factorization_and_gauge_fixing_certificate,
)
from .examples.version8_transverse_noise_mobility_environment_origin import (
    build_certificate as transverse_noise_mobility_environment_origin_certificate,
)
from .examples.version8_full_field_kinetic_supermetric_assembly import (
    build_certificate as full_field_kinetic_supermetric_assembly_certificate,
)
from .examples.version8_full_field_kinetic_relative_weight_parent_origin import (
    build_certificate as full_field_kinetic_relative_weight_parent_origin_certificate,
)
from .examples.version8_full_field_a4_dirac_lift_origin import (
    build_certificate as full_field_a4_dirac_lift_origin_certificate,
)
from .examples.version8_full_42_carrier_base_k_determinant_compatibility import (
    build_certificate as full_42_carrier_base_k_determinant_compatibility_certificate,
)
from .examples.version8_full_42_carrier_bv_vacuum_quotient import (
    build_certificate as full_42_carrier_bv_vacuum_quotient_certificate,
)
from .examples.version8_gauge_invariant_vacuum_hessian_reconstruction import (
    build_certificate as gauge_invariant_vacuum_hessian_reconstruction_certificate,
)
from .examples.version8_horizontal_flat_direction_parent_lift import (
    build_certificate as horizontal_flat_direction_parent_lift_certificate,
)
from .examples.version8_horizontal_phase_determinant_line_admission import (
    build_certificate as horizontal_phase_determinant_line_admission_certificate,
)
from .examples.version8_horizontal_phase_heavy_arrow_cycle_admission import (
    build_certificate as horizontal_phase_heavy_arrow_cycle_admission_certificate,
)
from .examples.version8_horizontal_phase_real_oriented_cycle_admission import (
    build_certificate as horizontal_phase_real_oriented_cycle_admission_certificate,
)
from .examples.version8_horizontal_phase_complex_symplectic_polarization_admission import (
    build_certificate as horizontal_phase_complex_symplectic_polarization_admission_certificate,
)
from .examples.version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission import (
    build_certificate as horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate,
)
from .examples.version8_horizontal_phase_cotangent_doubled_quiver_parent_admission import (
    build_certificate as horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate,
)
from .examples.version8_horizontal_phase_cotangent_complex_structure_metric_selector import (
    build_certificate as horizontal_phase_cotangent_complex_structure_metric_selector_certificate,
)
from .examples.version8_full_noise_gksl import build_certificate as full_noise_gksl_certificate
from .examples.version8_full_noise_repeated_interaction import build_certificate as full_noise_repeated_interaction_certificate
from .examples.version8_full_noise_physical_time_scale import build_certificate as full_noise_physical_time_scale_certificate
from .examples.version8_full_noise_toeplitz_ancilla_chain import build_certificate as full_noise_toeplitz_ancilla_chain_certificate
from .examples.version8_vacuum_chain_parent_state_and_local_hamiltonian_origin import build_certificate as vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate
from .examples.version8_index_balanced_ancilla_conveyor import build_certificate as index_balanced_ancilla_conveyor_certificate
from .examples.version8_static_local_hamiltonian_embedding_no_go import build_certificate as static_local_hamiltonian_embedding_no_go_certificate
from .examples.version8_clock_augmented_static_hamiltonian_conveyor import build_certificate as clock_augmented_static_hamiltonian_conveyor_certificate
from .examples.version8_bounded_strength_autonomous_clock_thermodynamic_limit import build_certificate as bounded_strength_autonomous_clock_thermodynamic_limit_certificate
from .examples.version8_local_observable_clocked_qms_limit_and_time_anchor import build_certificate as local_observable_clocked_qms_limit_and_time_anchor_certificate
from .examples.version8_typed_clock_energy_to_noise_rate_anchor import build_certificate as typed_clock_energy_to_noise_rate_anchor_certificate
from .examples.version9_kms_relative_shape_invariant_parent import (
    SPEC as version9_kms_relative_shape_invariant_parent_spec,
)
from .examples.version9_kms_logdet_measure_origin import (
    SPEC as version9_kms_logdet_measure_origin_spec,
)
from .examples.version9_kms_auxiliary_fermion_module_admission import (
    SPEC as version9_kms_auxiliary_fermion_module_admission_spec,
)
from .examples.version9_kms_auxiliary_fermion_statistics_origin import (
    SPEC as version9_kms_auxiliary_fermion_statistics_origin_spec,
)
from .examples.version9_kms_minimal_brst_complex import (
    SPEC as version9_kms_minimal_brst_complex_spec,
)
from .examples.version9_kms_brst_shift_symmetry_origin import (
    SPEC as version9_kms_brst_shift_symmetry_origin_spec,
)
from .examples.version9_kms_minimal_stueckelberg_shift_parent import (
    SPEC as version9_kms_minimal_stueckelberg_shift_parent_spec,
)
from .examples.version9_kms_physical_fermion_loop_origin import (
    SPEC as version9_kms_physical_fermion_loop_origin_spec,
)
from .examples.version9_kms_minimal_fermion_bath import (
    SPEC as version9_kms_minimal_fermion_bath_spec,
)
from .examples.version9_kms_keldysh_influence_functional import (
    SPEC as version9_kms_keldysh_influence_functional_spec,
)
from .examples.version9_kms_reservoir_spectral_density_origin import (
    SPEC as version9_kms_reservoir_spectral_density_origin_spec,
)
from .examples.version9_kms_reservoir_measure_anomaly_origin import (
    SPEC as version9_kms_reservoir_measure_anomaly_origin_spec,
)
from .examples.version9_kms_minimal_new_parent_axiom import (
    SPEC as version9_kms_minimal_new_parent_axiom_spec,
)
from .examples.version9_kms_axiom_augmented_common_parent import (
    SPEC as version9_kms_axiom_augmented_common_parent_spec,
)
from .examples.version9_kms_axiom_augmented_blind_prediction import (
    SPEC as version9_kms_axiom_augmented_blind_prediction_spec,
)
from .examples.version9_kms_conditional_program_status import (
    SPEC as version9_kms_conditional_program_status_spec,
)
from .examples.version9_physical_origin_reopening_criterion import (
    SPEC as version9_physical_origin_reopening_criterion_spec,
)
from .examples.version9_physical_reopening_common_origin_carrier import (
    SPEC as version9_physical_reopening_common_origin_carrier_spec,
)
from .examples.version9_gaussian_reference_state_parent_origin import (
    SPEC as version9_gaussian_reference_state_parent_origin_spec,
)
from .examples.version9_reference_scale_mu_parent_origin import (
    SPEC as version9_reference_scale_mu_parent_origin_spec,
)
from .examples.version9_final_conclusion_tome10_program import (
    SPEC as version9_final_conclusion_tome10_program_spec,
)
from .gates import GateSpec, Obligation


def registered_gates() -> tuple[GateSpec, ...]:
    return (
        version9_final_conclusion_tome10_program_spec,
        version9_reference_scale_mu_parent_origin_spec,
        version9_gaussian_reference_state_parent_origin_spec,
        version9_physical_reopening_common_origin_carrier_spec,
        version9_physical_origin_reopening_criterion_spec,
        version9_kms_conditional_program_status_spec,
        version9_kms_axiom_augmented_blind_prediction_spec,
        version9_kms_axiom_augmented_common_parent_spec,
        version9_kms_minimal_new_parent_axiom_spec,
        version9_kms_reservoir_measure_anomaly_origin_spec,
        version9_kms_reservoir_spectral_density_origin_spec,
        version9_kms_keldysh_influence_functional_spec,
        version9_kms_minimal_fermion_bath_spec,
        version9_kms_physical_fermion_loop_origin_spec,
        version9_kms_minimal_stueckelberg_shift_parent_spec,
        version9_kms_brst_shift_symmetry_origin_spec,
        version9_kms_minimal_brst_complex_spec,
        version9_kms_auxiliary_fermion_statistics_origin_spec,
        version9_kms_auxiliary_fermion_module_admission_spec,
        version9_kms_logdet_measure_origin_spec,
        version9_kms_relative_shape_invariant_parent_spec,
        GateSpec(
            "version8_bimodule_common_curvature_relative_weight_gate",
            "No-go полнорангового endpoint/transfer-коннектора",
            (
                "s2t/gates/version8_bimodule_common_curvature_relative_weight_gate.tex",
                "s2t/results/s2t_v8_bimodule_common_curvature_relative_weight_gate_results.json",
            ),
            (
                Obligation(
                    "full_rank_connector_is_impossible",
                    lambda: connector_certificate().theorem,
                ),
            ),
        ),
        GateSpec(
            "spinodal_threshold",
            "Точный спинодальный порог beta=21/2",
            (
                "formalization_candidates/spinodal_threshold/definitions.md",
                "formalization_candidates/spinodal_threshold/theorem.md",
            ),
            (
                Obligation(
                    "curvature_formula",
                    lambda: spinodal_certificate().curvature_theorem,
                ),
                Obligation(
                    "unique_threshold",
                    lambda: spinodal_certificate().threshold_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_markov_fixed_algebra_selector_gate",
            "Точная двухмерная неподвижная endpoint-алгебра",
            (
                "s2t/gates/version8_markov_fixed_algebra_selector_gate.tex",
                "s2t/results/s2t_v8_markov_fixed_algebra_selector_gate_results.json",
            ),
            (
                Obligation(
                    "endpoint_gauge_commutant_dimension",
                    lambda: fixed_algebra_certificate().gauge_theorem,
                ),
                Obligation(
                    "joint_linking_fixed_algebra_dimension",
                    lambda: fixed_algebra_certificate().fixed_theorem,
                ),
                Obligation(
                    "quark_lepton_projector_partition",
                    lambda: fixed_algebra_certificate().projector_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_linking_dirichlet_quantum_markov_semigroup_gate",
            "Точный linking GKSL/QMS-конструктор",
            (
                "s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex",
                "s2t/results/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate_results.json",
            ),
            (
                Obligation(
                    "finite_dimensional_gksl_form",
                    lambda: linking_qms_certificate().gksl_theorem,
                ),
                Obligation(
                    "trace_preservation",
                    lambda: linking_qms_certificate().trace_theorem,
                ),
                Obligation(
                    "unitality",
                    lambda: linking_qms_certificate().unital_theorem,
                ),
                Obligation(
                    "endpoint_corner_invariance",
                    lambda: linking_qms_certificate().corner_invariance_theorem,
                ),
                Obligation(
                    "explicit_corner_formula",
                    lambda: linking_qms_certificate().corner_formula_theorem,
                ),
                Obligation(
                    "linking_fixed_dimension_41",
                    lambda: linking_qms_certificate().fixed_dimension_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_gauge_twirl_cross_sector_kraus_bridge_gate",
            "Точный gauge-twirl межсекторного Kraus-моста",
            (
                "s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex",
                "s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json",
            ),
            (
                Obligation(
                    "finite_dimensional_gksl_form",
                    lambda: gauge_twirl_kraus_certificate().gksl_theorem,
                ),
                Obligation(
                    "unitality",
                    lambda: gauge_twirl_kraus_certificate().unital_theorem,
                ),
                Obligation(
                    "orthogonal_kraus_basis_independence",
                    lambda: gauge_twirl_kraus_certificate().basis_invariance_theorem,
                ),
                Obligation(
                    "exact_gauge_frame_covariance_and_no_linear_singlet",
                    lambda: gauge_twirl_kraus_certificate().gauge_covariance_theorem,
                ),
                Obligation(
                    "QLYR_central_restriction",
                    lambda: gauge_twirl_kraus_certificate().qlyr_central_theorem,
                ),
                Obligation(
                    "XLdR_central_restriction",
                    lambda: gauge_twirl_kraus_certificate().xldr_central_theorem,
                ),
                Obligation(
                    "combined_central_restriction",
                    lambda: gauge_twirl_kraus_certificate().cross_central_theorem,
                ),
                Obligation(
                    "one_dimensional_central_fixed_line",
                    lambda: gauge_twirl_kraus_certificate().cross_kernel_theorem,
                ),
                Obligation(
                    "internal_lepton_control_is_zero",
                    lambda: gauge_twirl_kraus_certificate().internal_control_theorem,
                ),
                Obligation(
                    "positive_rate_robustness",
                    lambda: gauge_twirl_kraus_certificate().positive_rate_kernel_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_kraus_bridge_parent_action_hessian_gate",
            "Точный parent-action и гессиан Kraus-моста",
            (
                "s2t/gates/version8_kraus_bridge_parent_action_hessian_gate.tex",
                "s2t/results/s2t_v8_kraus_bridge_parent_action_hessian_gate_results.json",
            ),
            (
                Obligation(
                    "individual_cross_coefficients",
                    lambda: kraus_parent_hessian_certificate().coefficient_theorem,
                ),
                Obligation(
                    "internal_control_coefficients",
                    lambda: kraus_parent_hessian_certificate().control_theorem,
                ),
                Obligation(
                    "field_dirichlet_hessian",
                    lambda: kraus_parent_hessian_certificate().hessian_theorem,
                ),
                Obligation(
                    "bridge_hessian_signature",
                    lambda: kraus_parent_hessian_certificate().bridge_signature_theorem,
                ),
                Obligation(
                    "origin_signature_for_all_nonnegative_weights",
                    lambda: kraus_parent_hessian_certificate().origin_signature_theorem,
                ),
                Obligation(
                    "vacuum_signature_for_all_nonnegative_weights",
                    lambda: kraus_parent_hessian_certificate().vacuum_signature_theorem,
                ),
                Obligation(
                    "zero_tree_energy",
                    lambda: kraus_parent_hessian_certificate().zero_energy_theorem,
                ),
                Obligation(
                    "zero_tree_gradient",
                    lambda: kraus_parent_hessian_certificate().zero_gradient_theorem,
                ),
                Obligation(
                    "zero_tree_kraus_weights",
                    lambda: kraus_parent_hessian_certificate().zero_jump_weights_theorem,
                ),
                Obligation(
                    "two_family_covariance_rate",
                    lambda: kraus_parent_hessian_certificate().covariance_rate_theorem,
                ),
                Obligation(
                    "gaussian_probe_rate",
                    lambda: kraus_parent_hessian_certificate().gaussian_rate_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_cross_arrow_covariance_origin_gate",
            "Точная полярная ось cross-ковариации",
            (
                "s2t/gates/version8_cross_arrow_covariance_origin_gate.tex",
                "s2t/results/s2t_v8_cross_arrow_covariance_origin_gate_results.json",
            ),
            (
                Obligation(
                    "physical_polar_coisometry",
                    lambda: cross_covariance_certificate().polar_theorem,
                ),
                Obligation(
                    "exact_cross_pair_formula",
                    lambda: cross_covariance_certificate().pair_formula_theorem,
                ),
                Obligation(
                    "six_identical_pairs",
                    lambda: cross_covariance_certificate().repetition_theorem,
                ),
                Obligation(
                    "decoupling_from_other_directions",
                    lambda: cross_covariance_certificate().decoupling_theorem,
                ),
                Obligation(
                    "positive_distinct_pair_spectrum",
                    lambda: cross_covariance_certificate().positivity_theorem,
                ),
                Obligation(
                    "common_axis_for_positive_eta",
                    lambda: cross_covariance_certificate().common_axis_theorem,
                ),
                Obligation(
                    "eta_dependent_anisotropy",
                    lambda: cross_covariance_certificate().anisotropy_theorem,
                ),
                Obligation(
                    "classical_scale_remains_free",
                    lambda: cross_covariance_certificate().classical_scale_theorem,
                ),
                Obligation(
                    "quantum_scale_remains_free",
                    lambda: cross_covariance_certificate().quantum_scale_theorem,
                ),
                Obligation(
                    "heat_time_remains_free",
                    lambda: cross_covariance_certificate().heat_time_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_minimal_covariant_stinespring_carrier_gate",
            "Точная минимальная Stinespring-дилатация cross-канала",
            (
                "s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex",
                "s2t/results/s2t_v8_minimal_covariant_stinespring_carrier_gate_results.json",
            ),
            (
                Obligation(
                    "cross_jump_hilbert_schmidt_gram",
                    lambda: stinespring_certificate().jump_gram_theorem,
                ),
                Obligation(
                    "cross_gram_spectrum",
                    lambda: stinespring_certificate().gram_spectrum_theorem,
                ),
                Obligation(
                    "exact_step_window",
                    lambda: stinespring_certificate().step_window_theorem,
                ),
                Obligation(
                    "kraus_channel_completeness",
                    lambda: stinespring_certificate().channel_theorem,
                ),
                Obligation(
                    "trace_preservation",
                    lambda: stinespring_certificate().trace_theorem,
                ),
                Obligation(
                    "endpoint_algebra_invariance",
                    lambda: stinespring_certificate().endpoint_theorem,
                ),
                Obligation(
                    "interior_kraus_rank_13",
                    lambda: stinespring_certificate().interior_rank_theorem,
                ),
                Obligation(
                    "minimal_environment_dimension_13",
                    lambda: stinespring_certificate().minimal_environment_theorem,
                ),
                Obligation(
                    "gauge_covariance",
                    lambda: stinespring_certificate().covariance_theorem,
                ),
                Obligation(
                    "gksl_tangent_at_zero",
                    lambda: stinespring_certificate().tangent_theorem,
                ),
                Obligation(
                    "finite_step_semigroup_no_go",
                    lambda: stinespring_certificate().semigroup_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_intrinsic_noise_clock_dilation_gate",
            "Точное безразмерное шумовое время и collision-limit",
            (
                "s2t/gates/version8_intrinsic_noise_clock_dilation_gate.tex",
                "s2t/results/s2t_v8_intrinsic_noise_clock_dilation_gate_results.json",
            ),
            (
                Obligation("cross_gksl_generator", lambda: noise_clock_certificate().gksl_theorem),
                Obligation("exact_decay_spectrum", lambda: noise_clock_certificate().spectrum_theorem),
                Obligation("dimensionless_semigroup", lambda: noise_clock_certificate().semigroup_theorem),
                Obligation("positive_rate_scaling", lambda: noise_clock_certificate().rate_scaling_theorem),
                Obligation("uniform_modular_flow_is_trivial", lambda: noise_clock_certificate().uniform_modular_theorem),
                Obligation("central_modular_flow_fixes_populations", lambda: noise_clock_certificate().central_modular_theorem),
                Obligation("cross_dissipation_moves_population", lambda: noise_clock_certificate().dissipative_motion_theorem),
                Obligation("fresh_ancilla_collision_limit", lambda: noise_clock_certificate().collision_limit_theorem),
            ),
        ),
        GateSpec(
            "version8_full_primitive_markov_generator_assembly_gate",
            "Точная сборка полного примитивного QMS",
            (
                "s2t/gates/version8_full_primitive_markov_generator_assembly_gate.tex",
                "s2t/results/s2t_v8_full_primitive_markov_generator_assembly_gate_results.json",
            ),
            (
                Obligation("full_gksl_generator", lambda: full_primitive_certificate().gksl_theorem),
                Obligation("trace_preservation", lambda: full_primitive_certificate().trace_theorem),
                Obligation("unitality", lambda: full_primitive_certificate().unital_theorem),
                Obligation("endpoint_invariance", lambda: full_primitive_certificate().endpoint_theorem),
                Obligation("scalar_fixed_algebra", lambda: full_primitive_certificate().scalar_fixed_theorem),
                Obligation("qlyr_alone_closes_C2", lambda: full_primitive_certificate().qlyr_closure_theorem),
                Obligation("xldr_alone_closes_C2", lambda: full_primitive_certificate().xldr_closure_theorem),
                Obligation("all_positive_weights_primitive", lambda: full_primitive_certificate().positive_weight_theorem),
                Obligation("strict_decay_gap", lambda: full_primitive_certificate().gap_theorem),
            ),
        ),
        GateSpec(
            "version8_kms_nontracial_relative_rate_selector_gate",
            "Точный no-go нетривиального KMS-селектора",
            (
                "s2t/gates/version8_kms_nontracial_relative_rate_selector_gate.tex",
                "s2t/results/s2t_v8_kms_nontracial_relative_rate_selector_gate_results.json",
            ),
            (
                Obligation("unique_trace_state", lambda: kms_selector_certificate().unique_state_theorem),
                Obligation("central_nontracial_state_no_go", lambda: kms_selector_certificate().central_state_theorem),
                Obligation("positive_rate_no_cancellation", lambda: kms_selector_certificate().positive_no_cancellation_theorem),
                Obligation("directed_bohr_split", lambda: kms_selector_certificate().bohr_split_theorem),
                Obligation("selfadjoint_jump_bohr_no_go", lambda: kms_selector_certificate().selfadjoint_bohr_no_go_theorem),
                Obligation("conditional_kms_ratio", lambda: kms_selector_certificate().conditional_ratio_theorem),
            ),
        ),
        GateSpec(
            "version8_modular_bohr_parent_origin_gate",
            "Точный цепно-модульный боровский родитель",
            ("s2t/gates/version8_modular_bohr_parent_origin_gate.tex", "s2t/results/s2t_v8_modular_bohr_parent_origin_gate_results.json"),
            (
                Obligation("forward_bohr_grading",lambda: modular_bohr_certificate().forward_bohr_theorem),
                Obligation("reverse_bohr_grading",lambda: modular_bohr_certificate().reverse_bohr_theorem),
                Obligation("gauge_invariance",lambda: modular_bohr_certificate().gauge_invariance_theorem),
                Obligation("forward_primitivity",lambda: modular_bohr_certificate().forward_primitive_theorem),
                Obligation("reverse_primitivity",lambda: modular_bohr_certificate().reverse_primitive_theorem),
                Obligation("orientation_no_go",lambda: modular_bohr_certificate().orientation_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_page_wootters_stinespring_history_gate",
            "Точный Page--Wootters--Stinespring history-мост",
            (
                "s2t/gates/version8_page_wootters_stinespring_history_gate.tex",
                "s2t/results/s2t_v8_page_wootters_stinespring_history_gate_results.json",
            ),
            (
                Obligation(
                    "conditional_clock_slice_recovery",
                    lambda: page_wootters_history_certificate().recovery_theorem,
                ),
                Obligation(
                    "stationary_frustration_free_history_parent",
                    lambda: page_wootters_history_certificate().history_parent_theorem,
                ),
                Obligation(
                    "nonunique_full_unitary_extension",
                    lambda: page_wootters_history_certificate().extension_freedom_theorem,
                ),
                Obligation(
                    "fresh_ancilla_collision_limit",
                    lambda: page_wootters_history_certificate().collision_limit_theorem,
                ),
                Obligation(
                    "physical_clock_boundary",
                    lambda: page_wootters_history_certificate().physical_clock_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_canonical_autonomous_clock_unitary_extension_no_go_gate",
            "No-go канонического автономного clock-unitary",
            (
                "s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex",
                "s2t/results/s2t_v8_canonical_autonomous_clock_unitary_extension_no_go_gate_results.json",
            ),
            (
                Obligation(
                    "minimal_environment_dimension",
                    lambda: autonomous_clock_unitary_certificate().minimal_environment_theorem,
                ),
                Obligation(
                    "gauge_covariant_stinespring_isometry",
                    lambda: autonomous_clock_unitary_certificate().covariance_theorem,
                ),
                Obligation(
                    "covariant_complement_phase_ambiguity",
                    lambda: autonomous_clock_unitary_certificate().ambiguity_theorem,
                ),
                Obligation(
                    "canonical_autonomous_clock_no_go",
                    lambda: autonomous_clock_unitary_certificate().autonomous_clock_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_microscopic_repeated_interaction_hamiltonian_gate",
            "Микроскопический Hamiltonian повторных взаимодействий",
            (
                "s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex",
                "s2t/results/s2t_v8_microscopic_repeated_interaction_hamiltonian_gate_results.json",
            ),
            (
                Obligation(
                    "well_typed_interaction_hamiltonian",
                    lambda: microscopic_interaction_hamiltonian_certificate().typed_theorem,
                ),
                Obligation(
                    "self_adjoint_star_interaction",
                    lambda: microscopic_interaction_hamiltonian_certificate().hermiticity_theorem,
                ),
                Obligation(
                    "vacuum_second_moment",
                    lambda: microscopic_interaction_hamiltonian_certificate().vacuum_second_moment_theorem,
                ),
                Obligation(
                    "gksl_weak_collision_tangent",
                    lambda: microscopic_interaction_hamiltonian_certificate().tangent_theorem,
                ),
                Obligation(
                    "gauge_covariant_dual_frame_contraction",
                    lambda: microscopic_interaction_hamiltonian_certificate().covariance_theorem,
                ),
                Obligation(
                    "eight_dimensional_interaction_and_four_dimensional_rate_commutants",
                    lambda: microscopic_interaction_hamiltonian_certificate().coupling_commutant_theorem,
                ),
                Obligation(
                    "exact_finite_step_second_order_no_go",
                    lambda: microscopic_interaction_hamiltonian_certificate().finite_step_no_go_theorem,
                ),
                Obligation(
                    "absolute_rate_scale_no_go",
                    lambda: microscopic_interaction_hamiltonian_certificate().scale_no_go_theorem,
                ),
                Obligation(
                    "fresh_ancilla_collision_limit",
                    lambda: microscopic_interaction_hamiltonian_certificate().collision_limit_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_trace_dual_cross_interaction_selector_gate",
            "Следово-двойственный селектор cross-взаимодействия",
            (
                "s2t/gates/version8_trace_dual_cross_interaction_selector_gate.tex",
                "s2t/results/s2t_v8_trace_dual_cross_interaction_selector_gate_results.json",
            ),
            (
                Obligation(
                    "exact_cross_field_trace_metric",
                    lambda: trace_dual_cross_coupling_certificate().field_metric_theorem,
                ),
                Obligation(
                    "exact_metric_dual_rate_tensor",
                    lambda: trace_dual_cross_coupling_certificate().dual_metric_theorem,
                ),
                Obligation(
                    "canonical_coupling_gram",
                    lambda: trace_dual_cross_coupling_certificate().coupling_gram_theorem,
                ),
                Obligation(
                    "trace_dual_repeated_interaction_tangent",
                    lambda: trace_dual_cross_coupling_certificate().tangent_theorem,
                ),
                Obligation(
                    "one_third_cross_generator",
                    lambda: trace_dual_cross_coupling_certificate().generator_scaling_theorem,
                ),
                Obligation(
                    "orthogonal_environment_frame_equivalence",
                    lambda: trace_dual_cross_coupling_certificate().environment_equivalence_theorem,
                ),
                Obligation(
                    "polar_axis_compatibility",
                    lambda: trace_dual_cross_coupling_certificate().polar_axis_compatibility_theorem,
                ),
                Obligation(
                    "microscopic_coupling_commutant_boundary",
                    lambda: trace_dual_cross_coupling_certificate().coupling_freedom_theorem,
                ),
                Obligation(
                    "absolute_time_scale_no_go",
                    lambda: trace_dual_cross_coupling_certificate().absolute_scale_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_metric_dual_environment_parent_action_origin_gate",
            "No-go происхождения метрически двойственной среды из старого действия",
            (
                "s2t/gates/version8_metric_dual_environment_parent_action_origin_gate.tex",
                "s2t/results/s2t_v8_metric_dual_environment_parent_action_origin_gate_results.json",
            ),
            (
                Obligation(
                    "exact_cross_field_metric",
                    lambda: metric_dual_environment_parent_action_certificate().field_metric_theorem,
                ),
                Obligation(
                    "exact_riesz_dual_rate",
                    lambda: metric_dual_environment_parent_action_certificate().dual_metric_theorem,
                ),
                Obligation(
                    "two_positive_gauge_parent_completions",
                    lambda: metric_dual_environment_parent_action_certificate().parent_underdetermination_theorem,
                ),
                Obligation(
                    "distinct_reduced_dynamics",
                    lambda: metric_dual_environment_parent_action_certificate().distinct_dynamics_theorem,
                ),
                Obligation(
                    "absolute_rate_scale_no_go",
                    lambda: metric_dual_environment_parent_action_certificate().absolute_scale_no_go_theorem,
                ),
                Obligation(
                    "parent_action_origin_no_go",
                    lambda: metric_dual_environment_parent_action_certificate().parent_origin_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_full_noise_cotangent_carrier_admission_gate",
            "Допуск полного смешанно-вещественного шумового cotangent-носителя",
            ("s2t/gates/version8_full_noise_cotangent_carrier_admission_gate.tex", "s2t/results/s2t_v8_full_noise_cotangent_carrier_admission_gate_results.json"),
            (
                Obligation("current_full_qms", lambda: full_noise_cotangent_carrier_certificate().full_qms_theorem),
                Obligation("mixed_real_dimension", lambda: full_noise_cotangent_carrier_certificate().mixed_dimension_theorem),
                Obligation("uniform_complexification_no_go", lambda: full_noise_cotangent_carrier_certificate().naive_complexification_no_go_theorem),
                Obligation("current_jump_deficit_17", lambda: full_noise_cotangent_carrier_certificate().current_deficit_theorem),
                Obligation("parent_origin_boundary", lambda: full_noise_cotangent_carrier_certificate().parent_origin_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_full_noise_trace_frame_metric_gate",
            "Полный 42-мерный шумовой кадр и trace-метрика",
            ("s2t/gates/version8_full_noise_trace_frame_metric_gate.tex", "s2t/results/s2t_v8_full_noise_trace_frame_metric_gate_results.json"),
            (
                Obligation("linking_orbit_dimension_5", lambda: full_noise_trace_frame_certificate().orbit_dimension_theorem),
                Obligation("transfer_complex_rank_15", lambda: full_noise_trace_frame_certificate().transfer_rank_theorem),
                Obligation("full_real_frame_rank_42", lambda: full_noise_trace_frame_certificate().full_frame_rank_theorem),
                Obligation("trace_metric_rank_42", lambda: full_noise_trace_frame_certificate().trace_metric_rank_theorem),
                Obligation("transfer_gauge_orthogonality", lambda: full_noise_trace_frame_certificate().transfer_gauge_orthogonality_theorem),
                Obligation("trace_dual_identity", lambda: full_noise_trace_frame_certificate().trace_dual_identity_theorem),
                Obligation("missing_direction_decomposition", lambda: full_noise_trace_frame_certificate().missing_direction_decomposition_theorem),
            ),
        ),
        GateSpec(
            "version8_field_to_noise_chain_map_pullback_metric_gate",
            "Полево-шумовое отображение и обратный перенос следовой метрики",
            (
                "s2t/gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex",
                "s2t/results/s2t_v8_field_to_noise_chain_map_pullback_metric_gate_results.json",
            ),
            (
                Obligation("block_embedding_rank_42", lambda: field_to_noise_chain_map_pullback_metric_certificate().map_rank_theorem),
                Obligation("canonical_block_coordinates", lambda: field_to_noise_chain_map_pullback_metric_certificate().block_embedding_theorem),
                Obligation("gauge_intertwining", lambda: field_to_noise_chain_map_pullback_metric_certificate().gauge_intertwining_theorem),
                Obligation("transfer_gauge_sector_preservation", lambda: field_to_noise_chain_map_pullback_metric_certificate().sector_preservation_theorem),
                Obligation("trace_metric_pullback", lambda: field_to_noise_chain_map_pullback_metric_certificate().pullback_metric_theorem),
                Obligation("inverse_metric_pullback", lambda: field_to_noise_chain_map_pullback_metric_certificate().pullback_dual_theorem),
                Obligation("sector_rescaling_freedom", lambda: field_to_noise_chain_map_pullback_metric_certificate().sector_rescaling_theorem),
                Obligation("dynamical_origin_boundary", lambda: field_to_noise_chain_map_pullback_metric_certificate().dynamical_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_field_noise_metric_to_parent_hessian_comparison_gate",
            "Сравнение следовой метрики с родительским гессианом",
            (
                "s2t/gates/version8_field_noise_metric_to_parent_hessian_comparison_gate.tex",
                "s2t/results/s2t_v8_field_noise_metric_to_parent_hessian_comparison_gate_results.json",
            ),
            (
                Obligation("full_trace_metric_rank_42", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().gate_theorem),
                Obligation("transfer_parent_hessian_rank_30", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().transfer_hessian_rank_theorem),
                Obligation("constant_gauge_hessian_zero", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().gauge_hessian_zero_theorem),
                Obligation("constant_parent_hessian_rank_30", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().constant_parent_rank_theorem),
                Obligation("gauge_trace_metric_rank_12", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().gauge_trace_metric_rank_theorem),
                Obligation("trace_parent_rank_mismatch", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().trace_parent_rank_mismatch_theorem),
                Obligation("nonzero_gauge_trace", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().nonzero_gauge_trace_theorem),
                Obligation("parent_hessian_identification_no_go", lambda: field_noise_metric_to_parent_hessian_comparison_certificate().parent_hessian_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_spacetime_kinetic_factorization_and_gauge_fixing_gate",
            "Пространственно-временная кинетическая факторизация",
            (
                "s2t/gates/version8_spacetime_kinetic_factorization_and_gauge_fixing_gate.tex",
                "s2t/results/s2t_v8_spacetime_kinetic_factorization_and_gauge_fixing_gate_results.json",
            ),
            (
                Obligation("transverse_longitudinal_projectors", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().projector_theorem),
                Obligation("ungauged_rank_36", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().ungauged_rank_theorem),
                Obligation("ungauged_nullity_12", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().ungauged_nullity_theorem),
                Obligation("gauge_fixed_rank_48", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().gauge_fixed_rank_theorem),
                Obligation("factorized_inverse", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().inverse_theorem),
                Obligation("transverse_gauge_parameter_independence", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().transverse_independence_theorem),
                Obligation("longitudinal_gauge_parameter_dependence", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().longitudinal_dependence_theorem),
                Obligation("physical_mobility_boundary", lambda: spacetime_kinetic_factorization_and_gauge_fixing_certificate().dynamical_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_transverse_noise_mobility_environment_origin_gate",
            "Происхождение поперечной шумовой мобильности из среды",
            (
                "s2t/gates/version8_transverse_noise_mobility_environment_origin_gate.tex",
                "s2t/results/s2t_v8_transverse_noise_mobility_environment_origin_gate_results.json",
            ),
            (
                Obligation("environment_covariance_rank_12", lambda: transverse_noise_mobility_environment_origin_certificate().covariance_rank_theorem),
                Obligation("transverse_mobility_rank_36", lambda: transverse_noise_mobility_environment_origin_certificate().transverse_rank_theorem),
                Obligation("common_longitudinal_kernel", lambda: transverse_noise_mobility_environment_origin_certificate().common_kernel_theorem),
                Obligation("normalized_shape_invariance", lambda: transverse_noise_mobility_environment_origin_certificate().normalized_shape_theorem),
                Obligation("mobility_scale_dependence", lambda: transverse_noise_mobility_environment_origin_certificate().scale_dependence_theorem),
                Obligation("time_scale_compensation", lambda: transverse_noise_mobility_environment_origin_certificate().time_compensation_theorem),
                Obligation("absolute_scale_boundary", lambda: transverse_noise_mobility_environment_origin_certificate().physical_scale_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_full_field_kinetic_supermetric_assembly_gate",
            "Полная главная кинетическая суперметрика поля",
            (
                "s2t/gates/version8_full_field_kinetic_supermetric_assembly_gate.tex",
                "s2t/results/s2t_v8_full_field_kinetic_supermetric_assembly_gate_results.json",
            ),
            (
                Obligation("scalar_principal_rank_120", lambda: full_field_kinetic_supermetric_assembly_certificate().scalar_rank_theorem),
                Obligation("gauge_transverse_rank_36", lambda: full_field_kinetic_supermetric_assembly_certificate().gauge_rank_theorem),
                Obligation("zero_principal_type_mixing", lambda: full_field_kinetic_supermetric_assembly_certificate().type_separation_theorem),
                Obligation("ungauged_full_rank_156", lambda: full_field_kinetic_supermetric_assembly_certificate().ungauged_rank_theorem),
                Obligation("ungauged_longitudinal_nullity_12", lambda: full_field_kinetic_supermetric_assembly_certificate().ungauged_nullity_theorem),
                Obligation("gauge_fixed_full_rank_168", lambda: full_field_kinetic_supermetric_assembly_certificate().gauge_fixed_rank_theorem),
                Obligation("exact_block_inverse", lambda: full_field_kinetic_supermetric_assembly_certificate().inverse_theorem),
                Obligation("relative_sector_weight_freedom", lambda: full_field_kinetic_supermetric_assembly_certificate().relative_weight_freedom_theorem),
                Obligation("lower_order_and_time_boundary", lambda: full_field_kinetic_supermetric_assembly_certificate().lower_order_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_full_field_kinetic_relative_weight_parent_origin_gate",
            "Относительный кинетический вес общего a4-родителя",
            (
                "s2t/gates/version8_full_field_kinetic_relative_weight_parent_origin_gate.tex",
                "s2t/results/s2t_v8_full_field_kinetic_relative_weight_parent_origin_gate_results.json",
            ),
            (
                Obligation("euclidean_clifford_relations", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().clifford_theorem),
                Obligation("scalar_spin_trace_coefficient_2", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().scalar_trace_theorem),
                Obligation("antihermitian_gauge_coefficient_minus_two_thirds", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().gauge_trace_theorem),
                Obligation("positive_gauge_coefficient_two_thirds", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().positive_gauge_theorem),
                Obligation("relative_kinetic_weight_three", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().relative_weight_theorem),
                Obligation("common_finite_trace_rank_42", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().common_trace_theorem),
                Obligation("dirac_lift_origin_boundary", lambda: full_field_kinetic_relative_weight_parent_origin_certificate().lift_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_full_field_a4_dirac_lift_origin_gate",
            "Граница происхождения общего дираковского подъёма",
            (
                "s2t/gates/version8_full_field_a4_dirac_lift_origin_gate.tex",
                "s2t/results/s2t_v8_full_field_a4_dirac_lift_origin_gate_results.json",
            ),
            (
                Obligation("external_chirality", lambda: full_field_a4_dirac_lift_origin_certificate().chirality_theorem),
                Obligation("all_internal_commutators_scale_invariant", lambda: full_field_a4_dirac_lift_origin_certificate().internal_calculus_theorem),
                Obligation("unit_external_symbol_square", lambda: full_field_a4_dirac_lift_origin_certificate().first_symbol_theorem),
                Obligation("rescaled_external_symbol_square", lambda: full_field_a4_dirac_lift_origin_certificate().second_symbol_theorem),
                Obligation("external_metric_scale_nonuniqueness", lambda: full_field_a4_dirac_lift_origin_certificate().symbol_scale_theorem),
                Obligation("relative_a4_weight_stability", lambda: full_field_a4_dirac_lift_origin_certificate().relative_weight_stability_theorem),
                Obligation("finite_parent_lift_no_go", lambda: full_field_a4_dirac_lift_origin_certificate().lift_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_full_42_carrier_base_k_determinant_compatibility_gate",
            "Совместимость полного носителя с base-K determinant",
            (
                "s2t/gates/version8_full_42_carrier_base_k_determinant_compatibility_gate.tex",
                "s2t/results/s2t_v8_full_42_carrier_base_k_determinant_compatibility_gate_results.json",
            ),
            (
                Obligation("vacuum_transfer_rank_28", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().scalar_rank_theorem),
                Obligation("vacuum_transfer_nullity_2", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().scalar_nullity_theorem),
                Obligation("broken_gauge_rank_3", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().gauge_rank_theorem),
                Obligation("unbroken_gauge_nullity_9", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().gauge_nullity_theorem),
                Obligation("scalar_fourth_moment", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().scalar_fourth_theorem),
                Obligation("gauge_fourth_moment", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().gauge_fourth_theorem),
                Obligation("bosonic_cw_numerator", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().bosonic_ledger_theorem),
                Obligation("finite_fermion_fourth_moment", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().fermion_moment_theorem),
                Obligation("full_supertrace_boundary", lambda: full_42_carrier_base_k_determinant_compatibility_certificate().full_ledger_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_full_42_carrier_bv_vacuum_quotient_gate",
            "BV-вакуумный quotient полного 42-мерного носителя",
            (
                "s2t/gates/version8_full_42_carrier_bv_vacuum_quotient_gate.tex",
                "s2t/results/s2t_v8_full_42_carrier_bv_vacuum_quotient_gate_results.json",
            ),
            (
                Obligation("odd_finite_grading", lambda: full_42_carrier_bv_vacuum_quotient_certificate().grading_theorem),
                Obligation("physical_chiral_projector", lambda: full_42_carrier_bv_vacuum_quotient_certificate().projector_theorem),
                Obligation("physical_chiral_rank_42", lambda: full_42_carrier_bv_vacuum_quotient_certificate().projector_rank_theorem),
                Obligation("physical_fermion_fourth_moment_92", lambda: full_42_carrier_bv_vacuum_quotient_certificate().fermion_multiplicity_theorem),
                Obligation("broken_gauge_orbit_rank_3", lambda: full_42_carrier_bv_vacuum_quotient_certificate().gauge_orbit_rank_theorem),
                Obligation("orbit_hessian_rank_3", lambda: full_42_carrier_bv_vacuum_quotient_certificate().orbit_hessian_rank_theorem),
                Obligation("orbit_hessian_trace_34", lambda: full_42_carrier_bv_vacuum_quotient_certificate().orbit_hessian_trace_theorem),
                Obligation("goldstone_kernel_no_go", lambda: full_42_carrier_bv_vacuum_quotient_certificate().goldstone_no_go_theorem),
                Obligation("fixed_background_candidate_numerator", lambda: full_42_carrier_bv_vacuum_quotient_certificate().candidate_numerator_theorem),
                Obligation("physical_bv_ledger_boundary", lambda: full_42_carrier_bv_vacuum_quotient_certificate().physical_ledger_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_gauge_invariant_vacuum_hessian_reconstruction_gate",
            "Горизонтальная реконструкция вакуумного гессиана",
            (
                "s2t/gates/version8_gauge_invariant_vacuum_hessian_reconstruction_gate.tex",
                "s2t/results/s2t_v8_gauge_invariant_vacuum_hessian_reconstruction_gate_results.json",
            ),
            (
                Obligation("orbit_trace_metric_14I3", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().orbit_metric_theorem),
                Obligation("orbit_projector_idempotent", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().projector_theorem),
                Obligation("orbit_projector_metric_self_adjoint", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().metric_orthogonality_theorem),
                Obligation("horizontal_rank_27", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().horizontal_rank_theorem),
                Obligation("goldstone_orbit_in_quotient_kernel", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().goldstone_kernel_theorem),
                Obligation("quotient_hessian_rank_26", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().quotient_rank_theorem),
                Obligation("quotient_hessian_nullity_4", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().quotient_nullity_theorem),
                Obligation("three_goldstones_plus_one_horizontal_flat_mode", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().kernel_decomposition_theorem),
                Obligation("quotient_scalar_fourth_moment", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().scalar_fourth_theorem),
                Obligation("quadratic_bv_bosonic_ledger", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().bosonic_fourth_theorem),
                Obligation("quadratic_bv_full_numerator", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().full_numerator_theorem),
                Obligation("nonlinear_parent_boundary", lambda: gauge_invariant_vacuum_hessian_reconstruction_certificate().nonlinear_parent_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_flat_direction_parent_lift_gate",
            "Происхождение горизонтальной плоской моды",
            (
                "s2t/gates/version8_horizontal_flat_direction_parent_lift_gate.tex",
                "s2t/results/s2t_v8_horizontal_flat_direction_parent_lift_gate_results.json",
            ),
            (
                Obligation("up_rest_phase_tangents", lambda: horizontal_flat_direction_parent_lift_certificate().phase_reconstruction_theorem),
                Obligation("phase_plane_metric", lambda: horizontal_flat_direction_parent_lift_certificate().phase_metric_theorem),
                Obligation("phase_plane_gram_kernel", lambda: horizontal_flat_direction_parent_lift_certificate().gram_hessian_phase_kernel_theorem),
                Obligation("phase_orbit_coupling", lambda: horizontal_flat_direction_parent_lift_certificate().orbit_phase_coupling_theorem),
                Obligation("horizontal_phase_four_to_three", lambda: horizontal_flat_direction_parent_lift_certificate().horizontal_phase_theorem),
                Obligation("horizontal_phase_quotient_flat", lambda: horizontal_flat_direction_parent_lift_certificate().quotient_flat_theorem),
                Obligation("left_gram_all_order_invariance", lambda: horizontal_flat_direction_parent_lift_certificate().left_gram_invariance_theorem),
                Obligation("right_gram_all_order_invariance", lambda: horizontal_flat_direction_parent_lift_certificate().right_gram_invariance_theorem),
                Obligation("maximal_minor_carrier_dimension_11", lambda: horizontal_flat_direction_parent_lift_certificate().maximal_minor_carrier_theorem),
                Obligation("gram_trace_parent_lift_no_go", lambda: horizontal_flat_direction_parent_lift_certificate().trace_parent_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_determinant_line_admission_gate",
            "Допуск determinant-line свёртки горизонтальной фазы",
            (
                "s2t/gates/version8_horizontal_phase_determinant_line_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_determinant_line_admission_gate_results.json",
            ),
            (
                Obligation("cofactor_spans_incidence_kernel", lambda: horizontal_phase_determinant_line_admission_certificate().cofactor_kernel_theorem),
                Obligation("primitive_cofactor_norm_two", lambda: horizontal_phase_determinant_line_admission_certificate().cofactor_norm_theorem),
                Obligation("cofactor_phase_weight_33", lambda: horizontal_phase_determinant_line_admission_certificate().cofactor_phase_theorem),
                Obligation("determinant_character_exponent_33", lambda: horizontal_phase_determinant_line_admission_certificate().phase_exponent_theorem),
                Obligation("source_determinant_hypercharge_minus_two", lambda: horizontal_phase_determinant_line_admission_certificate().source_charge_theorem),
                Obligation("target_determinant_hypercharge_minus_two", lambda: horizontal_phase_determinant_line_admission_certificate().target_charge_theorem),
                Obligation("relative_determinant_hypercharge_zero", lambda: horizontal_phase_determinant_line_admission_certificate().relative_charge_theorem),
                Obligation("no_invariant_linear_functional", lambda: horizontal_phase_determinant_line_admission_certificate().invariant_functional_no_go_theorem),
                Obligation("real_pair_modulus_phase_blind", lambda: horizontal_phase_determinant_line_admission_certificate().real_pair_modulus_theorem),
                Obligation("two_vacuum_normalized_contractions", lambda: horizontal_phase_determinant_line_admission_certificate().background_contraction_theorem),
                Obligation("background_contraction_nonunique", lambda: horizontal_phase_determinant_line_admission_certificate().contraction_nonuniqueness_theorem),
                Obligation("determinant_line_scalar_trivialization_no_go", lambda: horizontal_phase_determinant_line_admission_certificate().determinant_line_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_heavy_arrow_cycle_admission_gate",
            "Допуск тяжёлых стрелочных циклов горизонтальной фазы",
            (
                "s2t/gates/version8_horizontal_phase_heavy_arrow_cycle_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_heavy_arrow_cycle_admission_gate_results.json",
            ),
            (
                Obligation("connected_support_graph_rank_8", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().graph_rank_theorem),
                Obligation("full_cycle_rank_3", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().cycle_rank_theorem),
                Obligation("incidence_support_is_a_forest", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().incidence_forest_theorem),
                Obligation("explicit_three_cycle_basis", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().cycle_basis_theorem),
                Obligation("cycle_basis_rank_3", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().cycle_basis_rank_theorem),
                Obligation("heavy_projection_rank_3", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().heavy_cycle_rank_theorem),
                Obligation("up_sector_edge_is_a_leaf", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().up_edge_leaf_theorem),
                Obligation("all_cycle_horizontal_charges_vanish", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().cycle_phase_charge_theorem),
                Obligation("heavy_cycle_phase_lift_no_go", lambda: horizontal_phase_heavy_arrow_cycle_admission_certificate().heavy_cycle_phase_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_real_oriented_cycle_admission_gate",
            "Допуск Real-ориентированного голоморфного цикла",
            (
                "s2t/gates/version8_horizontal_phase_real_oriented_cycle_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_real_oriented_cycle_admission_gate_results.json",
            ),
            (
                Obligation("holomorphic_raising_square_zero", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().raising_nilpotence_theorem),
                Obligation("real_reverse_square_zero", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().reverse_nilpotence_theorem),
                Obligation("real_completion_is_odd", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().odd_grading_theorem),
                Obligation("reverse_arrows_have_opposite_phase_weights", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().real_reverse_covariance_theorem),
                Obligation("horizontal_phase_is_similarity", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().phase_similarity_theorem),
                Obligation("odd_trace_moments_vanish", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().odd_trace_theorem),
                Obligation("even_trace_moments_are_phase_blind", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().even_trace_theorem),
                Obligation("forward_reverse_charges_cancel", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().reverse_charge_cancellation_theorem),
                Obligation("physical_transfer_real_dimension_40", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().physical_dimension_theorem),
                Obligation("independent_reverse_real_dimension_80", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().independent_reverse_dimension_theorem),
                Obligation("independent_reverse_adds_40_real_directions", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().independent_reverse_excess_theorem),
                Obligation("positive_involution_orientation_no_go", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().positive_involution_orientation_no_go_theorem),
                Obligation("real_oriented_cycle_no_go", lambda: horizontal_phase_real_oriented_cycle_admission_certificate().real_oriented_cycle_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_complex_symplectic_polarization_admission_gate",
            "Допуск комплексной симплектической поляризации",
            (
                "s2t/gates/version8_horizontal_phase_complex_symplectic_polarization_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_complex_symplectic_polarization_admission_gate_results.json",
            ),
            (
                Obligation("typed_transfer_dimension_20", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().representation_dimension_theorem),
                Obligation("invariant_alternating_form_dimension_11", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().invariant_form_dimension_theorem),
                Obligation("first_form_is_alternating", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().first_skew_theorem),
                Obligation("second_form_is_alternating", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().second_skew_theorem),
                Obligation("first_form_is_gauge_invariant", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().first_invariance_theorem),
                Obligation("second_form_is_gauge_invariant", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().second_invariance_theorem),
                Obligation("maximum_invariant_rank_14", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().maximum_rank_theorem),
                Obligation("minimum_radical_dimension_6", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().radical_dimension_theorem),
                Obligation("polarization_is_nonunique", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().nonuniqueness_theorem),
                Obligation("bosonic_self_contraction_zero", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().bosonic_self_contraction_theorem),
                Obligation("missing_dual_complex_dimension_6", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().missing_dual_dimension_theorem),
                Obligation("minimal_completed_complex_dimension_26", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().completed_carrier_dimension_theorem),
                Obligation("symplectic_polarization_no_go", lambda: horizontal_phase_complex_symplectic_polarization_admission_certificate().symplectic_polarization_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate",
            "Концевой допуск минимальной симплектической достройки",
            (
                "s2t/gates/version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate_results.json",
            ),
            (
                Obligation("completed_complex_dimension_26", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().completed_dimension_theorem),
                Obligation("completed_real_dimension_52", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().completed_real_dimension_theorem),
                Obligation("invariant_alternating_form_dimension_23", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().invariant_form_dimension_theorem),
                Obligation("standard_form_is_alternating", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().skew_theorem),
                Obligation("standard_form_is_gauge_invariant", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().invariance_theorem),
                Obligation("standard_form_rank_26", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().nondegeneracy_theorem),
                Obligation("standard_form_exact_inverse", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().inverse_theorem),
                Obligation("alternative_form_is_alternating", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().alternative_skew_theorem),
                Obligation("alternative_form_is_gauge_invariant", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().alternative_invariance_theorem),
                Obligation("completed_polarization_is_nonunique", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().nonuniqueness_theorem),
                Obligation("single_bosonic_self_contraction_zero", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().self_contraction_theorem),
                Obligation("two_field_symplectic_contraction_nonzero", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().two_field_contraction_theorem),
                Obligation("endpoint_multiplicity_deficit_3", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().endpoint_deficit_theorem),
                Obligation("new_complex_direction_count_6", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().new_direction_theorem),
                Obligation("endpoint_origin_no_go", lambda: horizontal_phase_minimal_symplectic_completion_endpoint_admission_certificate().endpoint_origin_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate",
            "Допуск котангенциального удвоенного колчанного родителя",
            (
                "s2t/gates/version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate_results.json",
            ),
            (
                Obligation("symplectic_carrier_rank_26", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().symplectic_theorem),
                Obligation("moment_quadratic_matrices_symmetric", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().moment_symmetry_theorem),
                Obligation("moment_component_span_dimension_13", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().moment_span_theorem),
                Obligation("single_central_generator_relation", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().generator_relation_theorem),
                Obligation("nonzero_moment_map_witness", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().nonzero_moment_witness_theorem),
                Obligation("cotangent_phase_is_symplectic", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().phase_symplectic_theorem),
                Obligation("cotangent_phase_commutes_with_gauge", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().phase_gauge_commutant_theorem),
                Obligation("moment_map_is_phase_invariant", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().moment_phase_invariance_theorem),
                Obligation("moment_parent_is_phase_invariant", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().parent_phase_invariance_theorem),
                Obligation("parent_coupling_is_free", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().parent_scale_freedom_theorem),
                Obligation("stability_level_is_free", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().stability_level_freedom_theorem),
                Obligation("cotangent_parent_phase_no_go", lambda: horizontal_phase_cotangent_doubled_quiver_parent_admission_certificate().cotangent_parent_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate",
            "Селектор совместимой комплексной структуры и положительной метрики",
            (
                "s2t/gates/version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate.tex",
                "s2t/results/s2t_v8_horizontal_phase_cotangent_complex_structure_metric_selector_gate_results.json",
            ),
            (
                Obligation("completed_real_dimension_52", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().full_dimension_theorem),
                Obligation("full_trace_pullback_rank_42", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().trace_pullback_rank_theorem),
                Obligation("full_trace_pullback_nullity_10", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().trace_pullback_nullity_theorem),
                Obligation("transfer_trace_pullback_rank_30", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().transfer_pullback_rank_theorem),
                Obligation("transfer_trace_pullback_nullity_22", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().transfer_pullback_nullity_theorem),
                Obligation("first_compatible_complex_structure", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().first_complex_structure_theorem),
                Obligation("second_compatible_complex_structure", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().second_complex_structure_theorem),
                Obligation("first_metric_equals_Omega_J", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().first_compatibility_theorem),
                Obligation("second_metric_equals_Omega_J", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().second_compatibility_theorem),
                Obligation("old_trace_metric_is_preserved", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().trace_restriction_theorem),
                Obligation("compatible_extension_is_nonunique", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().extension_nonuniqueness_theorem),
                Obligation("trace_metric_selector_no_go", lambda: horizontal_phase_cotangent_complex_structure_metric_selector_certificate().trace_metric_selector_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_full_noise_42_jump_gksl_fixed_algebra_gate",
            "Полный 42-jump GKSL и scalar fixed algebra",
            ("s2t/gates/version8_full_noise_42_jump_gksl_fixed_algebra_gate.tex", "s2t/results/s2t_v8_full_noise_42_jump_gksl_fixed_algebra_gate_results.json"),
            (
                Obligation("gksl_form", lambda: full_noise_gksl_certificate().gksl_theorem),
                Obligation("trace_preservation", lambda: full_noise_gksl_certificate().trace_theorem),
                Obligation("unitality", lambda: full_noise_gksl_certificate().unital_theorem),
                Obligation("endpoint_invariance", lambda: full_noise_gksl_certificate().endpoint_theorem),
                Obligation("scalar_fixed_algebra", lambda: full_noise_gksl_certificate().scalar_fixed_theorem),
                Obligation("trace_dual_span_invertibility", lambda: full_noise_gksl_certificate().trace_dual_span_theorem),
            ),
        ),
        GateSpec(
            "version8_full_noise_repeated_interaction_hamiltonian_gate",
            "Полный 42-jump repeated-interaction Hamiltonian",
            ("s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex","s2t/results/s2t_v8_full_noise_repeated_interaction_hamiltonian_gate_results.json"),
            (
                Obligation("gauge_closed_42_frame",lambda:full_noise_repeated_interaction_certificate().closure_theorem),
                Obligation("structural_star_hamiltonian",lambda:full_noise_repeated_interaction_certificate().star_theorem),
                Obligation("minimal_environment_43",lambda:full_noise_repeated_interaction_certificate().minimality_theorem),
                Obligation("collision_limit",lambda:full_noise_repeated_interaction_certificate().collision_limit_theorem),
                Obligation("scalar_fixed_algebra",lambda:full_noise_repeated_interaction_certificate().fixed_algebra_theorem),
                Obligation("absolute_scale_no_go",lambda:full_noise_repeated_interaction_certificate().scale_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_full_noise_physical_time_scale_no_go_gate",
            "No-go абсолютного масштаба времени полного шумового процесса",
            ("s2t/gates/version8_full_noise_physical_time_scale_no_go_gate.tex", "s2t/results/s2t_v8_full_noise_physical_time_scale_no_go_gate_results.json"),
            (
                Obligation("quadratic_collision_rate_scaling", lambda: full_noise_physical_time_scale_certificate().rate_scale_theorem),
                Obligation("coupling_time_orbit_invariance", lambda: full_noise_physical_time_scale_certificate().orbit_invariance_theorem),
                Obligation("free_coupling_changes_rate", lambda: full_noise_physical_time_scale_certificate().coupling_freedom_theorem),
                Obligation("energy_time_calibration_identity", lambda: full_noise_physical_time_scale_certificate().energy_time_theorem),
                Obligation("time_unit_depends_on_energy_anchor", lambda: full_noise_physical_time_scale_certificate().energy_anchor_theorem),
                Obligation("absolute_physical_time_no_go", lambda: full_noise_physical_time_scale_certificate().physical_time_no_go_theorem),
            ),
        ),
        GateSpec(
            "version8_full_noise_toeplitz_ancilla_chain_dilation_gate",
            "Toeplitz-конвейер свежих ancilla полного шумового процесса",
            ("s2t/gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex", "s2t/results/s2t_v8_full_noise_toeplitz_ancilla_chain_dilation_gate_results.json"),
            (
                Obligation("absolute_integer_shift_counter", lambda: full_noise_toeplitz_ancilla_chain_certificate().counter_theorem),
                Obligation("cell_dimension_43", lambda: full_noise_toeplitz_ancilla_chain_certificate().cell_dimension_theorem),
                Obligation("fixed_global_floquet_step", lambda: full_noise_toeplitz_ancilla_chain_certificate().chain_theorem),
                Obligation("exact_reduced_iteration", lambda: full_noise_toeplitz_ancilla_chain_certificate().recovery_theorem),
                Obligation("cellwise_gauge_covariance", lambda: full_noise_toeplitz_ancilla_chain_certificate().gauge_theorem),
                Obligation("continuous_collision_limit", lambda: full_noise_toeplitz_ancilla_chain_certificate().collision_limit_theorem),
                Obligation("preloaded_reservoir_boundary", lambda: full_noise_toeplitz_ancilla_chain_certificate().resource_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate",
            "Parent вакуумной ancilla-цепи и индексный запрет локального Hamiltonian сдвига",
            (
                "s2t/gates/version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate.tex",
                "s2t/results/s2t_v8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate_results.json",
            ),
            (
                Obligation(
                    "local_commuting_projector_vacuum_parent",
                    lambda: vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate().parent_theorem,
                ),
                Obligation(
                    "one_cell_shift_gnvw_index_43",
                    lambda: vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate().shift_index_theorem,
                ),
                Obligation(
                    "localized_collision_preserves_flow_index",
                    lambda: vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate().global_index_theorem,
                ),
                Obligation(
                    "local_hamiltonian_origin_no_go",
                    lambda: vacuum_chain_parent_state_and_local_hamiltonian_origin_certificate().local_hamiltonian_no_go_theorem,
                ),
            ),
        ),
        GateSpec(
            "version8_index_balanced_ancilla_conveyor_gate",
            "Индексно-сбалансированный ancilla-конвейер",
            (
                "s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex",
                "s2t/results/s2t_v8_index_balanced_ancilla_conveyor_gate_results.json",
            ),
            (
                Obligation("opposite_shift_index_cancellation", lambda: index_balanced_ancilla_conveyor_certificate().counterflow_theorem),
                Obligation("two_layer_nearest_neighbour_swap_circuit", lambda: index_balanced_ancilla_conveyor_certificate().swap_circuit_theorem),
                Obligation("piecewise_local_swap_hamiltonian", lambda: index_balanced_ancilla_conveyor_certificate().local_hamiltonian_theorem),
                Obligation("exact_fresh_ancilla_reduced_iteration", lambda: index_balanced_ancilla_conveyor_certificate().recovery_theorem),
                Obligation("stationary_autonomy_boundary", lambda: index_balanced_ancilla_conveyor_certificate().autonomy_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_static_local_hamiltonian_embedding_or_no_go_gate",
            "No-Go статического Hamiltonian на минимальном двухцепочечном носителе",
            (
                "s2t/gates/version8_static_local_hamiltonian_embedding_or_no_go_gate.tex",
                "s2t/results/s2t_v8_static_local_hamiltonian_embedding_or_no_go_gate_results.json",
            ),
            (
                Obligation("exact_bloch_eigenchannel_windings", lambda: static_local_hamiltonian_embedding_no_go_certificate().winding_theorem),
                Obligation("periodic_static_logarithm_no_go", lambda: static_local_hamiltonian_embedding_no_go_certificate().static_no_go_theorem),
                Obligation("minimal_carrier_scope_boundary", lambda: static_local_hamiltonian_embedding_no_go_certificate().carrier_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_clock_augmented_static_hamiltonian_conveyor_gate",
            "Часовое расширение стационарного гамильтониана конвейера",
            (
                "s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex",
                "s2t/results/s2t_v8_clock_augmented_static_hamiltonian_conveyor_gate_results.json",
            ),
            (
                Obligation("three_site_perfect_clock_transfer", lambda: clock_augmented_static_hamiltonian_conveyor_certificate().transfer_theorem),
                Obligation("exact_dressed_history_execution", lambda: clock_augmented_static_hamiltonian_conveyor_certificate().execution_theorem),
                Obligation("uniform_locality_resource_boundary", lambda: clock_augmented_static_hamiltonian_conveyor_certificate().locality_theorem),
                Obligation("thermodynamic_autonomy_boundary", lambda: clock_augmented_static_hamiltonian_conveyor_certificate().boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate",
            "Термодинамическая ресурсная граница автономных квантовых часов",
            (
                "s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex",
                "s2t/results/s2t_v8_bounded_strength_autonomous_clock_thermodynamic_limit_gate_results.json",
            ),
            (
                Obligation("finite_volume_error_bound", lambda: bounded_strength_autonomous_clock_thermodynamic_limit_certificate().finite_volume_theorem),
                Obligation("logarithmic_clock_resource_schedule", lambda: bounded_strength_autonomous_clock_thermodynamic_limit_certificate().resource_schedule_theorem),
                Obligation("fixed_clock_global_uniformity_boundary", lambda: bounded_strength_autonomous_clock_thermodynamic_limit_certificate().global_boundary_theorem),
                Obligation("local_observable_limit_admission", lambda: bounded_strength_autonomous_clock_thermodynamic_limit_certificate().local_limit_theorem),
            ),
        ),
        GateSpec(
            "version8_local_observable_clocked_qms_limit_and_time_anchor_gate",
            "Локальный предел часового квантового марковского процесса",
            (
                "s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex",
                "s2t/results/s2t_v8_local_observable_clocked_qms_limit_and_time_anchor_gate_results.json",
            ),
            (
                Obligation("clocked_collision_error_decomposition", lambda: local_observable_clocked_qms_limit_and_time_anchor_certificate().error_theorem),
                Obligation("joint_clock_collision_continuum_limit", lambda: local_observable_clocked_qms_limit_and_time_anchor_certificate().joint_limit_theorem),
                Obligation("reduced_observable_qms_limit", lambda: local_observable_clocked_qms_limit_and_time_anchor_certificate().reduced_limit_theorem),
                Obligation("common_clock_rate_scale_boundary", lambda: local_observable_clocked_qms_limit_and_time_anchor_certificate().time_boundary_theorem),
            ),
        ),
        GateSpec(
            "version8_typed_clock_energy_to_noise_rate_anchor_gate",
            "Типизированный мост энергии часов к скорости полного шума",
            (
                "s2t/gates/version8_typed_clock_energy_to_noise_rate_anchor_gate.tex",
                "s2t/results/s2t_v8_typed_clock_energy_to_noise_rate_anchor_gate_results.json",
            ),
            (
                Obligation("typed_collision_rate_identity", lambda: typed_clock_energy_to_noise_rate_anchor_certificate().rate_identity_theorem),
                Obligation("relative_clock_rate_calibration", lambda: typed_clock_energy_to_noise_rate_anchor_certificate().relative_calibration_theorem),
                Obligation("dimensionless_coupling_underdetermination", lambda: typed_clock_energy_to_noise_rate_anchor_certificate().underdetermination_theorem),
                Obligation("typed_energy_anchor_no_go", lambda: typed_clock_energy_to_noise_rate_anchor_certificate().anchor_no_go_theorem),
            ),
        ),
    )