import json
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUTPUT_STEM = "fig_project_success_tree_v4_current_2026-08-15"

COLORS = {
    "proved": {
        "face": "#d8f3dc",
        "edge": "#2d6a4f",
        "label": "ДОКАЗАНО / УСТОЙЧИВО",
    },
    "conditional": {
        "face": "#fff3bf",
        "edge": "#b08900",
        "label": "УСЛОВНЫЙ РЕЗУЛЬТАТ",
    },
    "failed": {
        "face": "#ffd6d6",
        "edge": "#b02a37",
        "label": "ЗАКРЫТАЯ РЕАЛИЗАЦИЯ / NO-GO",
    },
    "open": {
        "face": "#dbeafe",
        "edge": "#1d4ed8",
        "label": "ОТКРЫТЫЙ РЕШАЮЩИЙ ТЕСТ",
    },
    "correction": {
        "face": "#eadcff",
        "edge": "#6f42c1",
        "label": "КОРРЕКЦИЯ АРХИТЕКТУРЫ",
    },
    "neutral": {
        "face": "#eeeeee",
        "edge": "#555555",
        "label": "СВОДНЫЙ УЗЕЛ",
    },
}


nodes = {
    "root": (19.0, 20.0, "neutral", "RPFT → S2T → TOE\nединая исследовательская программа"),
    "core": (3.2, 17.2, "proved", "МАТЕМАТИЧЕСКОЕ ЯДРО"),
    "t2": (10.2, 17.2, "failed", "ТОМ II\nfixed-K физическое замыкание"),
    "t3": (17.2, 17.2, "failed", "ТОМ III\nminimal parent action"),
    "t4_geometry": (24.7, 17.2, "conditional", "ТОМ IV-A\nгеометрический carrier"),
    "t4_ps": (33.0, 17.2, "conditional", "ТОМ IV-B\nPati–Salam reconstruction"),

    "core_geometry": (1.8, 14.2, "proved", "RP³×S¹: quotient, объём, систола"),
    "core_spectra": (5.0, 14.2, "proved", "Scalar, Dirac и coexact spectra"),
    "core_status": (3.4, 11.2, "proved", "Воспроизводимое ядро\nR_sci = 4/10"),

    "t2_c6": (8.5, 14.2, "failed", "C6 exact absorption\nstandard routes closed"),
    "t2_wilson": (11.9, 14.2, "conditional", "Wilson coefficients\noperator-level reconstruction"),
    "t2_source": (11.9, 11.2, "open", "Вывести gauge-invariant\ndefect source"),
    "t2_status": (8.5, 11.2, "failed", "Fixed-K predictive closure\nN_closed physical = 0"),

    "t3_finite": (15.5, 14.2, "proved", "Finite NCG algebra\nи SM representation"),
    "t3_flavour": (18.9, 14.2, "failed", "Family, CKM, Yukawa\nblind tests failed"),
    "t3_status": (17.2, 11.2, "failed", "Minimal parent action\nисчерпан"),

    "family_projector": (14.9, 8.2, "proved", "Projector Q(H)=0\n4 оси, 8 three-cycles"),
    "family_holonomy": (18.6, 8.2, "proved", "Flat A(H,nu)\nточная holonomy"),
    "family_action": (15.5, 4.8, "conditional", "Cubic-root action\ndelta_A S выводит connection"),
    "family_bundle": (20.1, 4.8, "proved", "Z3 = Stab_A4(P_a)\nresidual bundle origin"),
    "family_parent": (18.0, 2.0, "proved", "Bifundamental SO3 lock\nphysical family frame"),
    "family_condensate": (21.7, 2.0, "failed", "Ordinary ΩD²/J:\nparticle middle is junk"),
    "family_measure": (24.5, 2.0, "failed", "Gaussian Pfaffian/HS:\nsum-only measure no-go"),

    "k_origin": (22.9, 14.2, "correction", "K=RP³×S¹\nне выведен из TOE"),
    "s4": (26.5, 14.2, "conditional", "S⁴ carrier candidate"),
    "gibbs": (23.0, 11.2, "proved", "Correlation-cell Gibbs minimum\na/σ = 1.351392…"),
    "absolute": (26.6, 11.2, "failed", "Absolute EFT scale\nне контролируется"),
    "fisher": (23.0, 8.2, "proved", "Gibbs–Fisher radial measure\nS⁴ устойчивее"),
    "shape": (26.6, 8.2, "open", "Full-shape Hessian\nи vector/gauge completion"),

    "ps_seed": (30.7, 14.2, "proved", "SM-kernel и generalized fluctuation\nдают composite Pati–Salam branch"),
    "ps_hessian": (35.4, 14.2, "failed", "Исходный rank-one vacuum\nимеет 6 отрицательных мод"),
    "ps_identity": (30.7, 11.2, "proved", "Rank selector identity\n4 det(ΔΔ†), c=1"),
    "ps_nogo": (35.4, 11.2, "failed", "Color-six node и ordinary junk\nне реализуют selector"),
    "ps_relative": (30.7, 8.2, "proved", "Canonical quotient norm\nrelative curvature = 4 det(ΔΔ†)"),
    "ps_action": (35.4, 8.2, "proved", "Irreducible cycle: k=1\nDelta+C Hessian устойчив"),

    "geometry_final": (25.0, 4.8, "open", "Геометрический решающий тест:\nfull-shape stability и gauge sector"),
    "ps_final": (33.2, 4.8, "failed", "Rank-one connected no-go:\n8 Sigma + 2 phi flat"),
    "final_cycle": (29.1, 2.0, "open", "ОГРАНИЧЕННЫЙ ЦИКЛ ПРОВЕРКИ\nбез новых fitted coefficients"),

    "keep_math": (13.2, 0.2, "proved", "Математическая программа\nсохраняется"),
    "physics": (25.0, 0.2, "failed", "Единая предсказательная физика\nпока не построена"),
    "decision": (34.0, 0.2, "open", "Pass → версия V\nFail → закрыть физическую ветвь"),
}


edges = [
    ("root", "core"),
    ("root", "t2"),
    ("root", "t3"),
    ("root", "t4_geometry"),
    ("root", "t4_ps"),
    ("core", "core_geometry"),
    ("core", "core_spectra"),
    ("core_geometry", "core_status"),
    ("core_spectra", "core_status"),
    ("t2", "t2_c6"),
    ("t2", "t2_wilson"),
    ("t2_c6", "t2_status"),
    ("t2_wilson", "t2_source"),
    ("t3", "t3_finite"),
    ("t3", "t3_flavour"),
    ("t3_finite", "t3_status"),
    ("t3_flavour", "t3_status"),
    ("t3_finite", "family_projector"),
    ("family_projector", "family_holonomy"),
    ("family_holonomy", "family_action"),
    ("family_action", "family_bundle"),
    ("family_bundle", "family_parent"),
    ("family_parent", "family_condensate"),
    ("family_condensate", "family_measure"),
    ("t4_geometry", "k_origin"),
    ("t4_geometry", "s4"),
    ("k_origin", "gibbs"),
    ("s4", "gibbs"),
    ("s4", "absolute"),
    ("gibbs", "fisher"),
    ("absolute", "shape"),
    ("fisher", "shape"),
    ("t4_ps", "ps_seed"),
    ("t4_ps", "ps_hessian"),
    ("ps_seed", "ps_identity"),
    ("ps_hessian", "ps_nogo"),
    ("ps_identity", "ps_relative"),
    ("ps_nogo", "ps_relative"),
    ("ps_relative", "ps_action"),
    ("fisher", "geometry_final"),
    ("shape", "geometry_final"),
    ("ps_relative", "ps_final"),
    ("ps_action", "ps_final"),
    ("geometry_final", "final_cycle"),
    ("ps_final", "final_cycle"),
    ("t2_source", "final_cycle"),
    ("family_measure", "final_cycle"),
    ("core_status", "keep_math"),
    ("t2_status", "physics"),
    ("t3_status", "physics"),
    ("final_cycle", "physics"),
    ("final_cycle", "decision"),
]


def wrapped(text, width):
    lines = []
    for line in text.split("\n"):
        lines.extend(textwrap.wrap(line, width=width) or [""])
    return "\n".join(lines)


def node_size(key):
    if key == "root":
        return 4.7, 1.45
    if key in {"final_cycle", "keep_math", "physics", "decision"}:
        return 4.55, 1.42
    if key in {"t4_ps", "ps_seed", "ps_hessian", "ps_identity", "ps_nogo", "ps_relative", "ps_action"}:
        return 3.95, 1.52
    if key in {"family_projector", "family_holonomy", "family_action", "family_bundle", "family_parent", "family_condensate", "family_measure"}:
        return 3.45, 1.45
    if key in {"core", "t2", "t3", "t4_geometry"}:
        return 3.65, 1.38
    return 3.05, 1.38


fig, ax = plt.subplots(figsize=(31, 18), dpi=180)
ax.set_xlim(-0.3, 38.0)
ax.set_ylim(-1.9, 21.7)
ax.axis("off")

for source, target in edges:
    x1, y1, _, _ = nodes[source]
    x2, y2, target_status, _ = nodes[target]
    _, source_height = node_size(source)
    _, target_height = node_size(target)
    color = COLORS[target_status]["edge"] if target_status != "proved" else "#78828a"
    linestyle = "--" if target_status in {"conditional", "open"} else "-"
    horizontal_offset = x2 - x1
    if abs(horizontal_offset) < 4.8:
        connection = "arc3,rad=0.0"
    else:
        connection = f"arc3,rad={0.08 if horizontal_offset > 0 else -0.08}"
    arrow = FancyArrowPatch(
        (x1, y1 - source_height / 2),
        (x2, y2 + target_height / 2),
        arrowstyle="-|>",
        mutation_scale=11,
        linewidth=1.15,
        linestyle=linestyle,
        color=color,
        alpha=0.72,
        connectionstyle=connection,
        shrinkA=2,
        shrinkB=2,
        zorder=1,
    )
    ax.add_patch(arrow)

for key, (x, y, status, label) in nodes.items():
    width, height = node_size(key)
    style = COLORS[status]
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.08,rounding_size=0.12",
        facecolor=style["face"],
        edgecolor=style["edge"],
        linewidth=2.2 if key in {"root", "final_cycle"} else 1.65,
        zorder=2,
    )
    ax.add_patch(box)
    font_size = 10.4 if key == "root" else 7.6
    if key in {"core", "t2", "t3", "t4_geometry", "t4_ps", "final_cycle"}:
        font_size = 9.3
    ax.text(
        x,
        y,
        wrapped(label, 32 if width >= 4.5 else 24),
        ha="center",
        va="center",
        fontsize=font_size,
        fontweight="bold" if key in {"root", "core", "t2", "t3", "t4_geometry", "t4_ps", "final_cycle"} else "normal",
        color="#171717",
        zorder=3,
    )

ax.text(
    18.5,
    21.35,
    "Дерево доказательных статусов программы — 15 августа 2026 года",
    ha="center",
    va="center",
    fontsize=19,
    fontweight="bold",
)
ax.text(
    18.5,
    20.9,
    "Сплошная стрелка: установленный переход · пунктир: условный результат или открытый тест",
    ha="center",
    va="center",
    fontsize=10.2,
    color="#555555",
)

legend_statuses = ["proved", "conditional", "failed", "open", "correction"]
legend_y = -1.55
for index, status in enumerate(legend_statuses):
    style = COLORS[status]
    x = 0.0 + index * 7.15
    patch = FancyBboxPatch(
        (x, legend_y),
        0.52,
        0.36,
        boxstyle="round,pad=0.02",
        facecolor=style["face"],
        edgecolor=style["edge"],
        linewidth=1.35,
    )
    ax.add_patch(patch)
    ax.text(x + 0.68, legend_y + 0.18, style["label"], va="center", fontsize=8.1)

fig.savefig(f"{OUTPUT_STEM}.png", bbox_inches="tight", facecolor="white")
fig.savefig(f"{OUTPUT_STEM}.pdf", bbox_inches="tight", facecolor="white")
plt.close(fig)

result = {
    "date": "2026-08-15",
    "figure_png": f"{OUTPUT_STEM}.png",
    "figure_pdf": f"{OUTPUT_STEM}.pdf",
    "status_colors": {key: value["label"] for key, value in COLORS.items()},
    "nodes": {
        key: {"x": value[0], "y": value[1], "status": value[2], "label": value[3]}
        for key, value in nodes.items()
    },
    "edges": edges,
    "summary": {
        "R_sci": "4/10",
        "N_closed_physical": 0,
        "mathematical_program": "retain",
        "physical_program": "limited_decisive_cycle",
        "latest_proved": [
            "pati_salam_rank_selector_identity_4det",
            "canonical_edge_normalization_c_equals_1",
            "canonical_graph_coordinate_projector",
            "relative_fixed_point_quotient_identity",
            "irreducible_relative_cycle_k_equals_1",
            "delta_auxiliary_schur_hessian_no_negative_modes",
            "relative_cycle_algebraic_KO6_completion",
        ],
        "latest_closed": [
            "literal_color_six_associative_node",
            "ordinary_degree_two_junk_selector",
            "raw_spectral_trace_rank_selection",
            "standard_bv_gauge_fixing_auxiliary_origin",
            "identical_copy_multiplicity_k_greater_than_1",
            "current_full_composite_pati_salam_vacuum",
            "scalar_only_pati_salam_connector",
            "common_spectral_scale_rescue",
            "pati_salam_like_twist_as_SU4_adjoint",
            "quartic_tensor_product_strict_stability",
            "higher_even_spectral_moment_product_rescue",
            "weighted_nonidentical_auxiliary_product_rescue",
            "rank_one_connected_curvature_full_vacuum",
            "family_quiver_ordinary_spectral_mixed_sign",
            "family_quiver_mapping_cone_endpoint_only",
            "family_quiver_strict_so3_adjoint_D_term",
            "family_self_adjoint_real_auxiliary_wrong_sign",
            "family_ordinary_degree_two_Sym3_origin",
            "family_Gaussian_Pfaffian_HS_origin",
        ],
        "decisive_gates": [
            "version_V_rank_ge3_diagonal_or_noncommuting_projectors",
            "full_shape_carrier_hessian_and_gauge_sector",
            "gauge_invariant_defect_source_origin",
        ],
        "rotation_priority": [
            "full_shape_carrier_hessian_and_gauge_sector",
            "full_field_carrier_parent_counterterms",
            "standalone_affine_family_selector",
        ],
        "latest_conditional_positive": [
            "vortex_oriented_S4_three_cycle_zero_locus",
            "three_cycle_exact_one_majorana_kernel",
            "projector_shifted_square_supercurvature",
            "twisted_S4_cycle_covariance_192_of_192",
            "projector_flat_connection_exact_holonomy",
            "projector_connection_commuting_superconnection_saddle",
            "cubic_root_variational_connection_in_fixed_condensed_sector",
            "profile_independent_three_cycle_holonomy",
            "projector_residual_Z3_inside_A4",
            "order_six_binary_lift_of_family_holonomy",
            "real_bifundamental_gauge_family_diagonal_lock",
            "positive_three_direction_gauge_mass_matrix",
            "a4_schur_pairing_arrow_phi_identity",
            "quiver_moment_map_ratio_1_minus_2over3_1over9",
            "stable_unit_momentum_pairing_condensate",
            "family_quiver_KO6_order_zero_first_order_embedding",
            "first_order_pairing_arrow_phi_identity",
            "family_Sym3_algebraic_polarization_identity",
        ],
    },
}

with open("project_success_tree_v4_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result["summary"], ensure_ascii=False, indent=2))