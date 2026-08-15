import json
from pathlib import Path


AUDIT_FILES = [
    "s2t_c6_formal_gamma_results.json",
    "s2t_c6_ghost_exact_isolation_results.json",
    "s2t_c6_operator_trace_skeleton_results.json",
    "s2t_c6_second_variation_sign_results.json",
    "s2t_c6_scalar_fp_bookkeeping_results.json",
    "s2t_c6_scalar_p02_projection_results.json",
    "s2t_c6_scalar_variation_p02_results.json",
    "s2t_c6_scalar_rescue_routes_results.json",
    "s2t_c6_paired_sector_search_results.json",
    "s2t_c6_l21_low_shell_block_spec_results.json",
    "s2t_c6_l21_n1_to_n3_leakage_results.json",
    "s2t_c6_l21_n3_explicit_basis_gate_results.json",
    "s2t_c6_l21_n3_explicit_projection_results.json",
    "s2t_c6_l21_n3_parity_descent_results.json",
    "s2t_c6_l21_full_operator_rescue_gate_results.json",
    "s2t_c6_l21_n3_finite_counterterm_gate_results.json",
    "s2t_c6_l21_n3_obstruction_scale_results.json",
    "s2t_c6_l21_full_operator_checklist_results.json",
    "s2t_c6_l21_connection_variation_formula_results.json",
    "s2t_c6_l21_ricci_variation_formula_results.json",
    "s2t_c6_l21_projector_variation_formula_results.json",
    "s2t_c6_projector_t5_quotient_contraction_results.json",
    "s2t_c6_l21_hilbert_variation_formula_results.json",
    "s2t_c6_l21_delta2_delta_gate_results.json",
    "s2t_c6_l21_delta2_finite_block_spec_results.json",
    "s2t_c6_l21_delta2_path_choice_gate_results.json",
    "s2t_c6_l21_delta2_ambient_path_formula_results.json",
    "s2t_c6_l21_delta2_operator_decomposition_results.json",
    "s2t_c6_l21_delta2_principal_second_symbol_formula_results.json",
    "s2t_c6_l21_delta2_second_connection_formula_results.json",
    "s2t_c6_l21_delta2_second_ricci_formula_results.json",
    "s2t_c6_l21_delta2_second_projector_formula_results.json",
    "s2t_c6_l21_delta2_second_hilbert_formula_results.json",
    "s2t_c6_l21_delta2_local_counterterm_classifier_results.json",
    "s2t_c6_l21_delta2_skeleton_completion_results.json",
    "s2t_c6_l21_delta2_trace_phase_priority_results.json",
    "s2t_c6_l21_delta2_c11_setup_results.json",
    "s2t_c6_timeboxed_operator_sprint_results.json",
    "s2t_c6_l21_delta2_gamma_expansion_formula_results.json",
    "s2t_c6_l21_delta2_connection_laplacian_insertion_results.json",
    "s2t_c6_l21_delta2_connection_product_terms_results.json",
    "s2t_c6_l21_delta2_connection_product_gamma_inserted_results.json",
    "s2t_c6_l21_delta2_connection_product_ambient_simplified_results.json",
    "s2t_c6_l21_delta2_connection_product_C11_moment_results.json",
    "s2t_c6_l21_delta2_connection_single_gammaAB_ambient_simplified_results.json",
    "s2t_c6_l21_delta2_connection_single_gammaAB_C11_moment_results.json",
    "s2t_c6_l21_delta2_connection_metric_cross_ambient_formula_results.json",
    "s2t_c6_l21_delta2_connection_metric_cross_C11_moment_results.json",
    "s2t_c6_l21_delta2_connection_full_C11_assembly_results.json",
    "s2t_c6_l21_delta2_principal_C11_moment_results.json",
    "s2t_c6_l21_delta2_principal_plus_connection_C11_results.json",
    "s2t_c6_l21_delta2_ricci_C11_gauss_results.json",
    "s2t_c6_same_scheme_final_verdict_results.json",
]


def load_audit(path):
    payload = json.loads(Path(path).read_text())
    return {
        "file": path,
        "status": payload.get("status", "missing_status"),
        "verdict": payload.get("verdict", ""),
    }


audit_registry = [load_audit(path) for path in AUDIT_FILES]

closure_matrix = [
    {
        "node": "C6_formal_decomposition",
        "question": "Can Gamma_Maxwell+ghost be decomposed into coexact, exact, ghost, zero/gauge and local counterterm sectors?",
        "current_result": "yes_as_formal_skeleton",
        "supporting_audits": [
            "s2t_c6_formal_gamma_results.json",
            "s2t_c6_operator_trace_skeleton_results.json",
        ],
        "status": "closed_formally_not_theorem",
        "effect_on_C6": "localizes the missing proof but does not prove the pi^-4 determinant residue",
    },
    {
        "node": "P02_rank_selection",
        "question": "Is the finite first-strain rank naturally P02=Sym^2(R4)=1+9=10?",
        "current_result": "yes_conditionally_from_first_ambient_strain",
        "supporting_audits": [
            "s2t_c6_operator_trace_skeleton_results.json",
            "s2t_c6_second_variation_sign_results.json",
        ],
        "status": "conditional_lead",
        "effect_on_C6": "explains why N=10 is natural, but not why higher/nonzero towers are absent or cancelled",
    },
    {
        "node": "coexact_bosonic_sign",
        "question": "Does the coexact real-bosonic logdet have the sign needed for the suppression factor?",
        "current_result": "formally_compatible",
        "supporting_audits": ["s2t_c6_second_variation_sign_results.json"],
        "status": "closed_as_sign_check_only",
        "effect_on_C6": "supports the direction 1-N/(24 S_geo), but leaves determinant content open",
    },
    {
        "node": "constant_kappa_branch_isolation",
        "question": "Can the retained kappa_Cas=1/24 scalar row be kept out of traceless P02 leakage?",
        "current_result": "yes_for_traceless_RP3_first_strain",
        "supporting_audits": ["s2t_c6_scalar_p02_projection_results.json"],
        "status": "partially_closed",
        "effect_on_C6": "protects the 1/24 branch, but does not remove the nonzero scalar residual tower",
    },
    {
        "node": "standard_FP_scalar_residual",
        "question": "Does bare covariant FP/Hodge bookkeeping cancel scalar nonzero modes automatically?",
        "current_result": "no_leaves_minus_half_scalar_logdet_in_Gamma",
        "supporting_audits": [
            "s2t_c6_scalar_fp_bookkeeping_results.json",
            "s2t_c6_ghost_exact_isolation_results.json",
        ],
        "status": "blocking_gap",
        "effect_on_C6": "if the residual carries P02, the effective rank changes and the pi^-4 match is lost",
    },
    {
        "node": "nonzero_scalar_symmetry_escape",
        "question": "Can the nonzero scalar residual be set to zero by an RP3 parity or P02 selection rule?",
        "current_result": "no_first_even_nonzero_shell_ell2_has_multiplicity_9_and_can_couple",
        "supporting_audits": ["s2t_c6_scalar_variation_p02_results.json"],
        "status": "failed_route",
        "effect_on_C6": "moves the obstruction from bookkeeping into a real nonzero tower cancellation problem",
    },
    {
        "node": "local_or_zero_gauge_rescue",
        "question": "Can local counterterms, zero modes, gauge volume or Jacobians absorb the nonzero scalar tower?",
        "current_result": "not_proven_and_structurally_fails_for_nonlocal_Bessel_tower",
        "supporting_audits": ["s2t_c6_scalar_rescue_routes_results.json"],
        "status": "failed_route",
        "effect_on_C6": "standard FP rescue is blocked unless an equal opposite nonzero determinant is derived",
    },
    {
        "node": "paired_sector_search",
        "question": "Is there a known additional mandatory sector giving +1/2 log det' Delta0_nonzero with the same P02 coupling?",
        "current_result": "no_known_candidate_found",
        "supporting_audits": ["s2t_c6_paired_sector_search_results.json"],
        "status": "failed_route_except_definitional_quotient",
        "effect_on_C6": "known BRST/NK, Hodge-remnant, torsion, duality and Dirac routes do not rescue C6 as theorem",
    },
    {
        "node": "physical_transverse_quotient",
        "question": "Can the determinant be defined directly on the physical coexact quotient before introducing scalar FP residual?",
        "current_result": "viable_as_definitional_scheme_not_derived_cancellation",
        "supporting_audits": [
            "s2t_c6_ghost_exact_isolation_results.json",
            "s2t_c6_paired_sector_search_results.json",
        ],
        "status": "only_surviving_clean_route",
        "effect_on_C6": "keeps C6 open as a definition/theorem obligation, not as a completed standard-FP proof",
    },
    {
        "node": "L21_low_shell_block_spec",
        "question": "What finite low-shell coexact block must be computed before claiming the P02 determinant residue?",
        "current_result": "explicit_blocks_are_1_to_1_1_to_3_3_to_1_and_3_to_3_with_n3_dimension_30",
        "supporting_audits": ["s2t_c6_l21_low_shell_block_spec_results.json"],
        "status": "closed_as_specification_only",
        "effect_on_C6": "turns the vague higher-mode caveat into a concrete finite low-shell calculation",
    },
    {
        "node": "n1_diagonal_cancellation",
        "question": "Does the traceless P02 strain vanish on the first coexact Killing shell after Hodge-filtered projection?",
        "current_result": "yes_on_n1_projection_but_the_image_leaks_to_cubic_content",
        "supporting_audits": ["s2t_c6_l21_n1_to_n3_leakage_results.json"],
        "status": "partial_cancellation_not_closure",
        "effect_on_C6": "removes the naive 1->1 diagonal obstruction but creates a sharper 1->3 obstruction gate",
    },
    {
        "node": "n1_to_n3_coexact_leakage",
        "question": "Do the six n=1 Killing states leak into the allowed n=3 coexact shell under first strain?",
        "current_result": "proxy_image_has_rank_6_trace_norm_96_and_lambda_weighted_trace_6_before_explicit_n3_projection",
        "supporting_audits": [
            "s2t_c6_l21_n1_to_n3_leakage_results.json",
            "s2t_c6_l21_n3_explicit_basis_gate_results.json",
        ],
        "status": "blocking_explicit_projection_gate",
        "effect_on_C6": "rank-10 absorption cannot be claimed until the six leaked vectors are projected into a quotient-normalized 30-dimensional n=3 coexact basis",
    },
    {
        "node": "explicit_n3_coexact_basis",
        "question": "Is there an explicit orthonormal n=3 coexact basis on L(2,1) for the determinant trace?",
        "current_result": "yes_constructed_as_30_dimensional_cubic_tangent_divergence_free_harmonic_vector_polynomial_space",
        "supporting_audits": [
            "s2t_c6_l21_n3_explicit_basis_gate_results.json",
            "s2t_c6_l21_n3_explicit_projection_results.json",
        ],
        "status": "basis_constructed_projection_nonzero",
        "effect_on_C6": "the old hard gate is passed negatively for the clean-rank route: the six leaked images have nonzero projection, so C6 now needs a full-operator cancellation or derived absorption identity",
    },
    {
        "node": "n3_projected_low_shell_obstruction",
        "question": "What happens when the six leaked n=1 images are projected into the explicit n=3 coexact basis?",
        "current_result": "projected_trace_80_rank_6_with_eigenvalues_12_12_14_14_14_14_in_the_modelled_conformal_slice",
        "supporting_audits": ["s2t_c6_l21_n3_explicit_projection_results.json"],
        "status": "concrete_low_shell_obstruction_candidate",
        "effect_on_C6": "proxy warning becomes a concrete finite low-shell obstruction candidate, but the final determinant coefficient still requires all one-form variation terms and Hilbert-metric bookkeeping",
    },
    {
        "node": "n3_L21_parity_descent",
        "question": "Can the explicit cubic n=3 one-form basis descend through the antipodal quotient to L(2,1)?",
        "current_result": "yes_cubic_coefficients_are_odd_and_dx_is_odd_so_the_one_form_is_antipodal_even",
        "supporting_audits": ["s2t_c6_l21_n3_parity_descent_results.json"],
        "status": "closed_normalization_subgate",
        "effect_on_C6": "the nonzero n=3 projection is not removed by RP3 parity and should not be multiplied by an extra cover factor",
    },
    {
        "node": "full_operator_rescue_gate",
        "question": "What must happen after the nonzero n=3 projection for C6 to survive?",
        "current_result": "five_remaining_term_classes_must_cancel_or_absorb_the_rank6_trace80_projection",
        "supporting_audits": [
            "s2t_c6_l21_laplacian_variation_results.json",
            "s2t_c6_l21_full_operator_rescue_gate_results.json",
        ],
        "status": "primary_blocking_gap_after_projection",
        "effect_on_C6": "C6 now requires explicit connection, Ricci, coexact-projector, Hilbert-metric, and delta2-Delta cancellation/absorption; without it pi^-4 is structural compression",
    },
    {
        "node": "n3_finite_counterterm_escape",
        "question": "Can the nonzero n=1<->n=3 projected trace be removed by local counterterms?",
        "current_result": "no_trace80_is_finite_low_shell_global_spectral_data_not_UV_heat_kernel_asymptotic",
        "supporting_audits": [
            "s2t_c6_l21_coexact_locality_gate_results.json",
            "s2t_c6_l21_n3_finite_counterterm_gate_results.json",
        ],
        "status": "failed_rescue_route",
        "effect_on_C6": "local subtraction cannot erase the concrete n3 low-shell trace without a forbidden finite scheme choice",
    },
    {
        "node": "n3_obstruction_scale",
        "question": "Is the nonzero n=3 projection small enough to treat as the N_need-10 scheme gap?",
        "current_result": "no_trace80_is_8_times_rank10_and_trace_over_gap_squared_is_about_55_7_times_Nneed_minus_10",
        "supporting_audits": ["s2t_c6_l21_n3_obstruction_scale_results.json"],
        "status": "failed_small_gap_rescue",
        "effect_on_C6": "the n3 low-shell block requires genuine cancellation or absorption, not a rounding or tiny scheme-gap explanation",
    },
    {
        "node": "full_operator_rescue_checklist",
        "question": "What exact computations remain before C6 can be rescued after the nonzero n=3 obstruction?",
        "current_result": "five_required_blocks_connection_Ricci_projector_Hilbert_metric_delta2_Delta_must_be_derived_and_evaluated",
        "supporting_audits": [
            "s2t_c6_l21_laplacian_variation_results.json",
            "s2t_c6_l21_full_operator_checklist_results.json",
        ],
        "status": "open_computation_checklist_fixed",
        "effect_on_C6": "turns the remaining proof gap into five auditable computations with pass/fail conditions",
    },
    {
        "node": "connection_variation_formula",
        "question": "Is the connection-variation part of the full one-form operator fixed at formula level?",
        "current_result": "yes_for_conformal_slice_delta_Gamma_kij_equals_delta_kj_nabla_i_q_plus_delta_ki_nabla_j_q_minus_g_ij_nabla_k_q",
        "supporting_audits": ["s2t_c6_l21_connection_variation_formula_results.json"],
        "status": "formula_fixed_matrix_missing",
        "effect_on_C6": "first full-operator checklist item advanced from slogan to formula, but C_conn[1,3] matrix evaluation is still required",
    },
    {
        "node": "ricci_variation_formula",
        "question": "Is the Ricci/curvature part of the full one-form operator fixed at formula level?",
        "current_result": "yes_for_conformal_slice_delta_Ric_ab_equals_minus_Hess_ab_q_minus_g_ab_nabla2_q_with_mixed_index_raising_piece_minus4q",
        "supporting_audits": ["s2t_c6_l21_ricci_variation_formula_results.json"],
        "status": "formula_fixed_matrix_missing",
        "effect_on_C6": "second full-operator checklist item advanced from slogan to formula, but C_Ric[1,3] matrix evaluation is still required",
    },
    {
        "node": "coexact_projector_variation_formula",
        "question": "Is the moving coexact-projector part of the full one-form operator fixed at formula level?",
        "current_result": "yes_Pi_coex_equals_I_minus_d_Delta0_inverse_delta_and_delta_Pi_terms_must_enter_delta_Pi_Delta_Pi",
        "supporting_audits": ["s2t_c6_l21_projector_variation_formula_results.json"],
        "status": "formula_fixed_matrix_missing",
        "effect_on_C6": "third full-operator checklist item advanced from slogan to operator formula, but C_proj[1,3] and self-adjointness checks are still required",
    },
    {
        "node": "projector_T5_direct_quotient_contraction",
        "question": "Does the T1/T3 ell=4 scalar leakage survive the outer dG contraction with the quotient-normalized n=1/n=3 coexact bases?",
        "current_result": "no_complete_36_by_25_table_has_numeric_rank_zero_by_exact_coexact_orthogonality",
        "supporting_audits": ["s2t_c6_projector_t5_quotient_contraction_results.json"],
        "status": "closed_direct_channel_cross_return_terms_open",
        "effect_on_C6": "the pure Pi_AB outer-dG higher-shell leakage is removed from coexact matrix elements, but Pi_Delta1A_PiB cross-return terms and Hilbert/self-adjointness corrections remain to be evaluated",
    },
    {
        "node": "hilbert_inner_product_variation_formula",
        "question": "Is the Hilbert inner-product and normalization variation fixed at formula level?",
        "current_result": "yes_delta_inner_product_equals_integral_minus_h_ab_plus_half_trh_g_ab_contracting_one_forms_and_for_h_2qg_in_3d_reduces_to_q_overlap",
        "supporting_audits": ["s2t_c6_l21_hilbert_variation_formula_results.json"],
        "status": "formula_fixed_matrix_missing",
        "effect_on_C6": "fourth full-operator checklist item advanced from slogan to formula, but C_Hilb[1,3], basis-normalization, and self-adjointness checks are still required",
    },
    {
        "node": "delta2_delta_gate",
        "question": "Can Tr(Delta^-1 delta^2 Delta) be dropped, locally subtracted, compensated, or must it be computed as a finite block?",
        "current_result": "gate_fixed_locality_or_exact_compensation_or_finite_C_delta2_required",
        "supporting_audits": ["s2t_c6_l21_delta2_delta_gate_results.json"],
        "status": "blocking_gate_matrix_missing",
        "effect_on_C6": "fifth full-operator checklist item is now explicit; trace-square suppression cannot be promoted to theorem until delta2 Delta is proven local/compensated or evaluated as C_delta2",
    },
    {
        "node": "delta2_finite_block_spec",
        "question": "What finite C_delta2 data must be computed first if delta2 Delta is not proven local or compensated?",
        "current_result": "diagonal_trace_blocks_C_delta2_11_and_33_first_55_symmetric_deformation_pairs_51480_raw_entries_before_reductions",
        "supporting_audits": ["s2t_c6_l21_delta2_finite_block_spec_results.json"],
        "status": "blocking_spec_fixed_path_and_matrix_missing",
        "effect_on_C6": "turns delta2 Delta from a caveat into a scoped finite calculation; path choice and diagonal shell traces are now mandatory before using any cancellation claim",
    },
    {
        "node": "delta2_path_choice_gate",
        "question": "Is the second-variation metric/embedding path fixed before C_delta2 is computed or used for cancellation?",
        "current_result": "gate_identified_preferred_route_is_ambient_linear_embedding_strain",
        "supporting_audits": ["s2t_c6_l21_delta2_path_choice_gate_results.json"],
        "status": "gate_identified_followed_by_formula_node",
        "effect_on_C6": "prevents hidden fitting through g_second_derivative choice; the follow-up ambient formula node fixes the preferred route before numbers",
    },
    {
        "node": "delta2_ambient_path_formula",
        "question": "What are g'(0) and g''(0) for the preferred ambient linear embedding path?",
        "current_result": "fixed_gprime_A_2_uAv_gsecond_A_2_AuAv_mixed_AB_AuBv_plus_BuAv",
        "supporting_audits": ["s2t_c6_l21_delta2_ambient_path_formula_results.json"],
        "status": "formula_fixed_operator_delta2_missing",
        "effect_on_C6": "removes the path-choice ambiguity for the theorem route, but delta2 Delta_1_coex and finite C_delta2 traces remain unevaluated",
    },
    {
        "node": "delta2_operator_decomposition",
        "question": "Which subblocks must be derived to obtain delta2 Delta_1,coex on the fixed ambient path?",
        "current_result": "six_subblocks_fixed_principal_second_symbol_connection2_ricci2_projector2_hilbert2_local_classifier_all_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_operator_decomposition_results.json"],
        "status": "scoped_blocking_formula_and_matrix_missing",
        "effect_on_C6": "turns delta2 Delta_1_coex into six auditable formula tasks; no C6 upgrade until they are derived and diagonal traces evaluated or proven local",
    },
    {
        "node": "delta2_principal_second_symbol_formula",
        "question": "Is the principal second-symbol part of delta2 Delta_1 fixed on the ambient path?",
        "current_result": "formula_fixed_delta2_principal_AB_minus_partialAB_ginv_ij_nabla_i_nabla_j_with_partialAB_ginv_hAhB_plus_hBhA_minus_kAB",
        "supporting_audits": ["s2t_c6_l21_delta2_principal_second_symbol_formula_results.json"],
        "status": "formula_fixed_matrix_missing",
        "effect_on_C6": "one of six delta2 subblock formula gates is advanced, but diagonal C_delta2 traces and all other second-order subblocks remain open",
    },
    {
        "node": "delta2_second_connection_formula",
        "question": "Are the second-connection terms in delta2 Delta_1 located and separated from the principal block?",
        "current_result": "skeleton_fixed_delta2Gamma_inverse_metric_variation_covariant_derivative_variation_and_deltaGamma_deltaGamma_products_identified",
        "supporting_audits": ["s2t_c6_l21_delta2_second_connection_formula_results.json"],
        "status": "skeleton_fixed_full_formula_matrix_missing",
        "effect_on_C6": "second delta2 gear is scoped, but delta2 Gamma expansion and diagonal C_delta2 traces remain missing",
    },
    {
        "node": "delta2_second_ricci_formula",
        "question": "Are the second Ricci/curvature terms in delta2 Delta_1 located and separated from principal/connection blocks?",
        "current_result": "skeleton_fixed_delta2Ricci_mixed_index_raising_first_variation_products_and_background_curvature_terms_identified",
        "supporting_audits": ["s2t_c6_l21_delta2_second_ricci_formula_results.json"],
        "status": "skeleton_fixed_full_formula_matrix_missing",
        "effect_on_C6": "third delta2 gear is scoped, but delta2 Ricci expansion and diagonal C_delta2 traces remain missing",
    },
    {
        "node": "delta2_second_projector_formula",
        "question": "Are the second coexact-projector and reduced-operator side terms located?",
        "current_result": "skeleton_fixed_delta2Pi_inverse_scalar_laplacian_second_variation_side_projector_and_cross_operator_terms_identified",
        "supporting_audits": ["s2t_c6_l21_delta2_second_projector_formula_results.json"],
        "status": "skeleton_fixed_full_formula_self_adjointness_matrix_missing",
        "effect_on_C6": "fourth delta2 gear is scoped, but delta2 Pi expansion, self-adjointness, and diagonal C_delta2 traces remain missing",
    },
    {
        "node": "delta2_second_hilbert_formula",
        "question": "Are the second Hilbert metric and basis-normalization terms located?",
        "current_result": "skeleton_fixed_second_inner_product_volume_basis_transport_degenerate_rotation_and_self_adjoint_representation_terms_identified",
        "supporting_audits": ["s2t_c6_l21_delta2_second_hilbert_formula_results.json"],
        "status": "skeleton_fixed_basis_choice_self_adjointness_matrix_missing",
        "effect_on_C6": "fifth delta2 gear is scoped, but basis transport, second Gram correction, self-adjointness, and diagonal C_delta2 traces remain missing",
    },
    {
        "node": "delta2_local_counterterm_classifier",
        "question": "Which delta2 Delta_1 pieces can be locally subtracted, and which finite low-shell residuals must remain?",
        "current_result": "skeleton_fixed_local_heat_kernel_finite_low_shell_and_same_scheme_compensation_buckets_separated",
        "supporting_audits": ["s2t_c6_l21_delta2_local_counterterm_classifier_results.json"],
        "status": "skeleton_fixed_locality_compensation_finite_table_missing",
        "effect_on_C6": "sixth delta2 gear is scoped; finite C_delta2 residuals cannot be erased by post-hoc local counterterms and must be computed or exactly compensated",
    },
    {
        "node": "delta2_skeleton_completion_gate",
        "question": "Is the delta2 Delta_1 skeleton phase complete, and what phase comes next?",
        "current_result": "six_subblocks_named_all_skeletons_or_formulas_present_but_trace_phase_open",
        "supporting_audits": ["s2t_c6_l21_delta2_skeleton_completion_results.json"],
        "status": "phase_complete_trace_phase_open",
        "effect_on_C6": "delta2 scoping phase is complete, but no status upgrade is allowed until full formulas, self-adjointness, locality/compensation, and diagonal C_delta2 traces are done",
    },
    {
        "node": "delta2_trace_phase_priority",
        "question": "Which C_delta2 traces must be computed first after skeleton completion?",
        "current_result": "priority_fixed_diagonal_C_delta2_11_then_33_before_mixed_archive_blocks_51480_entries",
        "supporting_audits": ["s2t_c6_l21_delta2_trace_phase_priority_results.json"],
        "status": "trace_phase_started_priority_fixed_matrices_missing",
        "effect_on_C6": "starts the measurement phase: direct diagonal traces come before mixed archive blocks, but no C6 upgrade is allowed before actual C_delta2 values or locality/compensation proof",
    },
    {
        "node": "delta2_C11_setup",
        "question": "Are the inputs and conventions for the first diagonal trace block C_delta2[1,1] fixed?",
        "current_result": "setup_fixed_six_n1_Killing_states_55_pairs_1980_raw_entries_but_matrix_not_evaluated",
        "supporting_audits": ["s2t_c6_l21_delta2_c11_setup_results.json"],
        "status": "setup_fixed_operator_pieces_missing_matrix_missing",
        "effect_on_C6": "first trace block is ready as a work package, but C6 cannot move until the missing delta2 operator pieces are expanded and C11 values are computed or compensated",
    },
    {
        "node": "C6_timeboxed_operator_sprint",
        "question": "What is the next allowed C6 step after the direction re-audit?",
        "current_result": "timeboxed_sprint_target_second_connection_delta2Gamma_AB_toward_C11_or_fallback",
        "supporting_audits": ["s2t_c6_timeboxed_operator_sprint_results.json"],
        "status": "sprint_defined_operator_expansion_required",
        "effect_on_C6": "prevents more label-only C6 work; next progress must expand second-connection content toward C11, prove locality/compensation, or trigger external/neutrino fallback",
    },
    {
        "node": "delta2_Gamma_AB_expansion_formula",
        "question": "Is the mixed second-connection tensor delta2 Gamma_AB explicit enough to enter the rough one-form Laplacian?",
        "current_result": "Gamma_AB_formula_fixed_background_nabla_convention_but_laplacian_insertion_and_C11_matrix_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_gamma_expansion_formula_results.json"],
        "status": "operator_formula_fixed_laplacian_insertion_matrix_missing",
        "effect_on_C6": "first timeboxed sprint output gives real operator content, but C6 still needs rough-Laplacian insertion and C11 matrix evaluation or locality/compensation",
    },
    {
        "node": "delta2_connection_laplacian_insertion",
        "question": "Are the second-connection rough-Laplacian insertion slots fixed for C11 work?",
        "current_result": "single_GammaAB_metric_cross_and_GammaA_GammaB_slots_fixed_product_expansion_and_C11_matrix_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_laplacian_insertion_results.json"],
        "status": "operator_slots_fixed_product_expansion_matrix_missing",
        "effect_on_C6": "connection2 is now mounted into rough Laplacian slots, but C6 still needs product expansion and integration against n1 Killing states",
    },
    {
        "node": "delta2_connection_product_terms",
        "question": "Are the Gamma_A Gamma_B product terms organized enough for C11 reduction?",
        "current_result": "product_families_fixed_derivative_index_one_form_component_and_mixed_gradient_bins_integrals_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_product_terms_results.json"],
        "status": "product_families_fixed_index_cleanup_integrals_missing",
        "effect_on_C6": "dirty product slot is decomposed for reduction, but exact index table and C11 product integrals remain missing",
    },
    {
        "node": "delta2_connection_product_gamma_inserted",
        "question": "Has the Gamma_A Gamma_B product slot been rewritten in first-strain C-tensor form for C11 integration?",
        "current_result": "Gamma_products_substituted_by_C_A_C_B_integrand_template_but_C11_integrals_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_product_gamma_inserted_results.json"],
        "status": "Ctensor_integrand_fixed_C11_integrals_missing",
        "effect_on_C6": "moves the product slot closer to explicit C_conn2[1,1] computation, but no trace value or determinant cancellation is established",
    },
    {
        "node": "delta2_connection_product_ambient_simplified",
        "question": "Does the locked ambient strain path simplify the Gamma_A Gamma_B product slot before C11 integration?",
        "current_result": "product_operator_reduced_to_rank_two_aA_aB_contractions_C11_integrals_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_product_ambient_simplified_results.json"],
        "status": "ambient_product_simplified_C11_integrals_missing",
        "effect_on_C6": "turns the product part of C_conn2[1,1] into finite Killing/ambient-gradient moment integrals, but no determinant trace value is computed",
    },
    {
        "node": "delta2_connection_product_C11_moment_table",
        "question": "What is the finite C11 table for the Gamma_A Gamma_B product subslot in the raw ambient strain basis?",
        "current_result": "all_55_symmetric_strain_pairs_nonzero_product_subslot_rank_distribution_1_to_5",
        "supporting_audits": [
            "s2t_c6_l21_delta2_connection_product_C11_moment_results.json",
            "s2t_c6_l21_delta2_connection_product_moment_table_data.json",
        ],
        "status": "first_C11_subslot_table_computed_full_operator_missing",
        "effect_on_C6": "shows the product part of the second-connection C11 block is active and nonzero; cancellation, if any, must come from other slots or blocks",
    },
    {
        "node": "delta2_connection_single_GammaAB_ambient_simplified",
        "question": "Does the locked ambient strain path simplify the single Gamma_AB rough-Laplacian slot?",
        "current_result": "GammaAB_reduced_to_gij_wAB_operator_slot_fixed_C11_integrals_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_single_gammaAB_ambient_simplified_results.json"],
        "status": "single_GammaAB_operator_simplified_C11_integrals_missing",
        "effect_on_C6": "moves the non-product second-connection slot toward finite C11 moments, but no full connection matrix is computed",
    },
    {
        "node": "delta2_connection_single_GammaAB_C11_moment_table",
        "question": "What is the finite C11 table for the single Gamma_AB connection subslot in the raw ambient strain basis?",
        "current_result": "single_GammaAB_nonzero_for_52_of_55_pairs_rank_distribution_0_2_4_6",
        "supporting_audits": [
            "s2t_c6_l21_delta2_connection_single_gammaAB_C11_moment_results.json",
            "s2t_c6_l21_delta2_connection_single_gammaAB_moment_table_data.json",
        ],
        "status": "second_C11_connection_subslot_table_computed_cross_slot_missing",
        "effect_on_C6": "shows the single GammaAB slot is active and structurally different from the product slot; full connection cancellation still requires the metric-cross slot and addition of subslots",
    },
    {
        "node": "delta2_connection_metric_cross_ambient_formula",
        "question": "Is the inverse-metric/first-connection cross slot formula-ready on the locked ambient path?",
        "current_result": "metric_cross_operator_reduced_to_SA_tauA_aB_terms_C11_table_missing",
        "supporting_audits": ["s2t_c6_l21_delta2_connection_metric_cross_ambient_formula_results.json"],
        "status": "metric_cross_formula_fixed_C11_moment_table_missing",
        "effect_on_C6": "completes formula-level triad of connection subslots; full connection C11 still needs metric-cross moments and addition with product/single tables",
    },
    {
        "node": "delta2_connection_metric_cross_C11_moment_table",
        "question": "What is the finite C11 table for the inverse-metric/first-connection metric-cross subslot?",
        "current_result": "metric_cross_nonzero_for_all_55_pairs_rank_distribution_4_and_6_connection_triad_table_complete",
        "supporting_audits": [
            "s2t_c6_l21_delta2_connection_metric_cross_C11_moment_results.json",
            "s2t_c6_l21_delta2_connection_metric_cross_moment_table_data.json",
        ],
        "status": "connection_subslot_triad_table_complete_full_addition_missing",
        "effect_on_C6": "finishes the three second-connection C11 subslot tables; full connection block can now be assembled but C6 still needs non-connection delta2 pieces",
    },
    {
        "node": "delta2_connection_full_C11_assembly",
        "question": "Does the assembled second-connection C11 block cancel internally after adding product, single GammaAB, and metric-cross subslots?",
        "current_result": "assembled_connection_block_nonzero_for_all_55_pairs_rank_distribution_2_4_6",
        "supporting_audits": [
            "s2t_c6_l21_delta2_connection_full_C11_assembly_results.json",
            "s2t_c6_l21_delta2_connection_full_C11_table_data.json",
        ],
        "status": "full_connection_C11_block_computed_nonconnection_blocks_missing",
        "effect_on_C6": "rules out internal cancellation of the second-connection C11 block; full C6 still requires non-connection delta2 pieces",
    },
    {
        "node": "delta2_principal_C11_moment_table",
        "question": "What is the finite C11 table for the principal second-symbol block?",
        "current_result": "principal_block_nonzero_for_all_55_pairs_rank_distribution_4_and_6",
        "supporting_audits": [
            "s2t_c6_l21_delta2_principal_C11_moment_results.json",
            "s2t_c6_l21_delta2_principal_C11_moment_table_data.json",
        ],
        "status": "principal_C11_table_computed_combination_missing",
        "effect_on_C6": "adds the first non-connection C11 table; cancellation with connection and remaining blocks still untested",
    },
    {
        "node": "delta2_principal_plus_connection_C11_assembly",
        "question": "Does the principal second-symbol C11 block cancel the assembled second-connection C11 block?",
        "current_result": "principal_plus_connection_nonzero_for_all_55_pairs_rank_distribution_4_and_6",
        "supporting_audits": [
            "s2t_c6_l21_delta2_principal_plus_connection_C11_results.json",
            "s2t_c6_l21_delta2_principal_plus_connection_C11_table_data.json",
        ],
        "status": "principal_connection_C11_combined_nonzero_remaining_blocks_missing",
        "effect_on_C6": "rules out cancellation between principal and connection blocks alone; remaining rescue requires Ricci/projector/Hilbert/local pieces",
    },
    {
        "node": "delta2_Ricci_C11_Gauss_assembly",
        "question": "Does the exact mixed Ricci block cancel the assembled principal-plus-connection C11 table?",
        "current_result": "no_Ricci_ranks_0_12_4_27_6_16_but_combined_all_55_pairs_nonzero_ranks_4_39_6_16",
        "supporting_audits": [
            "s2t_c6_l21_delta2_ricci_C11_gauss_results.json",
            "s2t_c6_l21_delta2_ricci_C11_gauss_table_data.json",
            "s2t_c6_l21_delta2_principal_connection_ricci_C11_table_data.json",
        ],
        "status": "geometric_C11_cancellation_failed_same_scheme_determinant_gate",
        "effect_on_C6": "projector is closed, Hilbert similarity is determinant-neutral, and Ricci reinforces rather than cancels principal plus connection; only mandatory Maxwell-ghost scheme compensation can still rescue exact pi^-4 absorption",
    },
    {
        "node": "same_scheme_Maxwell_ghost_final_verdict",
        "question": "Does the declared Maxwell-ghost scheme contain a mandatory no-fit compensation for the surviving finite geometric block?",
        "current_result": "no_mandatory_compensation_found_across_scalar_zero_gauge_local_paired_or_transport_sectors",
        "supporting_audits": [
            "s2t_c6_same_scheme_final_verdict_results.json",
            "s2t_c6_scalar_rescue_routes_results.json",
            "s2t_c6_paired_sector_search_results.json",
        ],
        "status": "exact_pi4_determinant_theorem_downgraded",
        "effect_on_C6": "closes the present rescue branch negatively; pi^-4 remains structural compression and S_vac stays conditional",
    },
]

decision_tree = [
    {
        "if": "physical_transverse_quotient_is_adopted_and_external_gate_accepts_it",
        "then": "C6 remains a conditional determinant route with coexact-only P02 absorption",
    },
    {
        "if": "explicit_n3_coexact_projection_of_the_six_leaked_vectors_is_zero",
        "then": "this route would have removed the low-shell coexact obstruction, but the current explicit projection audit does not realize this case",
    },
    {
        "if": "the_current_nonzero_n3_projection_survives_full_one_form_variation_and_is_not_absorbed_by_a_derived_identity",
        "then": "the rank-10 pi^-4 determinant theorem is blocked even in the physical coexact quotient",
    },
    {
        "if": "T1_T3_or_T4_scalar_leakage_enters_only_through_the_outer_dG_of_PiAB",
        "then": "its direct coexact quotient matrix element vanishes exactly, but cross-return terms with deltaDelta1 must still be tested",
    },
    {
        "if": "standard_covariant_FP_is_required_without_new_sector",
        "then": "C6 theorem route is blocked by the nonzero scalar half-determinant residual",
    },
    {
        "if": "new_paired_sector_is_introduced_by_hand",
        "then": "C6 becomes a model-extension assumption unless the sector is mandatory from BRST, topology or EFT",
    },
    {
        "if": "neither_quotient_nor_mandatory_pairing_is_derived",
        "then": "pi^-4 must be classified as strong structural compression, not mature determinant theorem",
    },
    {
        "if": "principal_connection_Ricci_C11_is_nonzero_for_all_55_pairs_and_projector_Hilbert_are_neutral",
        "then": "the final C6 rescue must come from mandatory same-scheme Maxwell-ghost det-prime zero-gauge or scalar-half bookkeeping; otherwise downgrade exact pi^-4",
    },
    {
        "if": "the_final_same_scheme_audit_finds_no_mandatory_nonzero_mode_compensation",
        "then": "close the current C6 rescue branch negatively, downgrade exact pi^-4 to structural compression, and keep independent program successes unchanged",
    },
]

status_counts = {}
for row in closure_matrix:
    status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1

results = {
    "status": "C6_master_closure_matrix_exact_pi4_downgraded",
    "audit_registry": audit_registry,
    "closure_matrix": closure_matrix,
    "decision_tree": decision_tree,
    "status_counts": status_counts,
    "final_verdict": (
        "C6 is now more sharply localized but still not closed as a theorem. The formal Maxwell--ghost decomposition, natural "
        "P02 rank 1+9=10, compatible coexact bosonic sign, and constant kappa_Cas=1/24 isolation remain positive inputs. "
        "The standard covariant FP route is still blocked by the scalar half-determinant residual and its nonzero scalar tower. "
        "Even on the surviving physical coexact quotient route, the low-shell L(2,1) audits now expose a concrete obstruction candidate: the n=1 "
        "diagonal Hodge-filtered projection cancels, but six image vectors leak into cubic content. An explicit quotient-normalized "
        "30-dimensional n=3 coexact basis can be constructed, and the projected trace is nonzero in the modelled conformal slice. "
        "The direct projector T5 table now supplies one exact simplification: the complete 36x25 pairing of outer-dG ell=4 scalar leakage with the n=1/n=3 coexact quotient has rank zero, because exact one-forms are orthogonal to coexact states. This removes the pure Pi_AB T1/T3 channel, but not the cross-return terms where delta Delta1 acts on a first projector variation before the final coexact projection. "
        "The remaining primary gate is now explicit: connection, Ricci, the projector cross-return block, Hilbert-metric, and delta2-Delta terms must cancel or absorb this trace with no fitted coefficient. "
        "A local-counterterm escape is not available for the finite n=1<->n=3 low-shell trace, and the scale is too large to be the tiny N_need-10 scheme gap. The remaining work is now a five-item checklist: connection, Ricci, coexact-projector, Hilbert-metric, and delta2-Delta blocks must be derived and evaluated in the same quotient-normalized bases. The connection, Ricci, coexact-projector, and Hilbert inner-product blocks are fixed at formula/operator-obligation level in the conformal slice, but their n=1<->n=3 matrices and normalization/self-adjointness checks have not yet been evaluated. The delta2-Delta determinant identity is now fixed as a gate, and the finite fallback is scoped: compute diagonal C_delta2[1,1] and C_delta2[3,3] traces over 55 symmetric deformation pairs. The preferred ambient path is now fixed at metric-derivative level with gprime and gsecond formulas, and delta2 Delta_1_coex is decomposed into six mandatory subblocks. The principal second-symbol subblock is fixed at formula level; the second-connection, second-Ricci/curvature, second-projector, second-Hilbert/basis, and local-counterterm classifier subblocks are fixed at skeleton level, and the delta2 skeleton phase is now explicitly complete. The trace phase priority is now fixed: C_delta2[1,1] and C_delta2[3,3] diagonal traces come before mixed archive blocks. The C_delta2[1,1] setup is fixed with six n=1 states and 1,980 raw entries over 55 pairs. The next timeboxed C6 sprint is active: the mixed second-connection tensor delta2 Gamma_AB is now formula-fixed in a background-nabla convention. The rough-Laplacian insertion slots for second-connection are fixed, and the Gamma_A Gamma_B product slot is split into derivative-index, one-form-component, and mixed-gradient families. Exact index cleanup, C11 product integrals, full Ricci/Pi expansions, basis transport, self-adjointness, locality/compensation proof, finite residual table, and finite matrix evaluation remain missing. Until that full-operator rescue is derived, pi^-4 remains strong structural compression rather than a mature determinant theorem."
    ),
}

results["final_verdict"] += (
    " The Gamma_A Gamma_B product slot is rewritten in C_A C_B first-strain tensor form and simplifies on the locked ambient path to finite Killing/ambient-gradient moments."
    " Its C11 table is nonzero for all 55 strain pairs. The single Gamma_AB table is nonzero for 52 of 55 pairs, and the metric-cross table is nonzero for all 55 pairs."
    " Their assembled second-connection block is nonzero for all 55 pairs with rank distribution 2:6, 4:39, 6:10."
    " The principal second-symbol table is also nonzero for all 55 pairs, and the principal-plus-connection assembly remains nonzero with rank distribution 4:39 and 6:16."
    " Projector leakage is removed by exact/coexact orthogonality and Hodge commutation, while Hilbert self-adjoint transport is determinant-neutral by similarity invariance."
    " The exact Gauss-equation Ricci C11 table has ranks 0:12, 4:27, 6:16, but principal-plus-connection-plus-Ricci remains nonzero for all 55 pairs with ranks 4:39 and 6:16."
    " Therefore geometric C11 cancellation has failed; the only remaining exact-pi^-4 rescue class is mandatory same-scheme Maxwell-ghost, det-prime, zero/gauge, scalar-half, or pre-fixed local bookkeeping."
    " The final same-scheme audit finds no such mandatory compensation: standard FP leaves a scalar half-determinant, zero/gauge and det-prime factors do not cancel nonzero towers, local counterterms cannot erase finite low-shell data, and no required paired sector is present. Exact pi^-4 absorption is therefore downgraded to structural compression, while independent non-C6 results remain unchanged."
)

Path("s2t_c6_closure_matrix_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "nodes": len(closure_matrix),
    "blocking_or_failed_nodes": sum("fail" in row["status"] or "blocking" in row["status"] for row in closure_matrix),
    "primary_blocker": "none_current_C6_branch_closed_by_pi4_downgrade",
}, indent=2, ensure_ascii=False))