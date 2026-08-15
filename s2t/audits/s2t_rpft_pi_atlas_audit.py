import json
from pathlib import Path


CLAIMS = [
    (1, "fine_structure", "anchor", True, False),
    (2, "strong_coupling", "direct", True, True),
    (3, "weinberg_angle", "direct", True, True),
    (4, "z_boson", "chained", True, False),
    (5, "w_boson", "chained", True, False),
    (6, "higgs", "chained", False, False),
    (7, "vacuum_vev", "chained", False, False),
    (8, "top", "chained", False, False),
    (9, "bottom", "direct", True, True),
    (10, "charm", "direct", False, False),
    (11, "strange", "direct", True, True),
    (12, "down", "direct", True, True),
    (13, "up", "direct", True, True),
    (14, "electron", "anchor", False, False),
    (15, "muon", "direct", True, False),
    (16, "tau", "direct", True, True),
    (17, "v_ub", "direct", False, False),
    (18, "v_cb", "direct", True, True),
    (19, "cabibbo", "chained", False, False),
    (20, "ckm_phase", "direct", True, True),
    (21, "neutrino_3", "direct", True, False),
    (22, "neutrino_2", "direct", True, False),
    (23, "neutrino_1", "bound_or_zero", False, False),
    (24, "delta_m31", "chained", False, False),
    (25, "delta_m21", "chained", False, False),
    (26, "neutrino_sum", "chained", False, False),
    (27, "omega_lambda", "direct_correlated", True, True),
    (28, "omega_dm", "direct_correlated", True, True),
    (29, "omega_b", "direct_correlated", True, True),
    (30, "cosmological_constant", "order_only", True, False),
    (31, "theta_qcd", "bound_or_zero", False, False),
]


VERSION_DRIFT = [
    {
        "observable": "Z_boson",
        "earlier": "m_p*S_vac/sqrt(2)*(1+alpha/2)",
        "later": "m_p*pi^4-3*S_vac",
        "sources": [
            "RPFT-main/Проработка/standart_model.md:83",
            "RPFT-main/base/26-stparam.md:53",
        ],
    },
    {
        "observable": "Higgs",
        "earlier": "m_p*(S_vac-(pi+pi^-1))",
        "later": "m_p*(S_vac-e-1)",
        "sources": [
            "RPFT-main/Проработка/standart_model.md:27",
            "RPFT-main/base/26-stparam.md:55",
        ],
    },
    {
        "observable": "top",
        "earlier": "m_p*S_vac*(4/3)*(1+alpha*pi)",
        "later": "m_p*S_vac*(4/3)*(1+alpha)",
        "sources": [
            "RPFT-main/Проработка/standart_model.md:48",
            "RPFT-main/base/26-stparam.md:63",
        ],
    },
    {
        "observable": "charm",
        "earlier": "m_p*(1+pi^-1-alpha)",
        "later": "m_p*(4/3)*(1+alpha)",
        "sources": [
            "RPFT-main/Проработка/standart_model.md:50",
            "RPFT-main/base/26-stparam.md:65",
        ],
    },
    {
        "observable": "muon",
        "earlier": "m_e*(1.5*S_vac+pi-pi^-1)",
        "later": "six-term Laurent polynomial in pi",
        "sources": [
            "RPFT-main/Проработка/standart_model.md:37",
            "RPFT-main/base/26-stparam.md:86",
        ],
    },
    {
        "observable": "tau",
        "earlier": "m_mu*(pi^2+2*pi+2/3*(1+alpha))",
        "later": "m_mu*(pi^2+2*pi+2/3-alpha/3)",
        "sources": [
            "RPFT-main/base/26-stparam.md:87",
            "tome2_s2t_spectral_closure.tex:2159",
        ],
    },
]


def main():
    atlas = Path("RPFT-main/Проработка/atlas.md").read_text()
    master = Path("RPFT-main/base/26-stparam.md").read_text()

    category_counts = {}
    for _, _, category, _, _ in CLAIMS:
        category_counts[category] = category_counts.get(category, 0) + 1

    explicit_pi = [name for _, name, _, has_pi, _ in CLAIMS if has_pi]
    short_pi = [name for _, name, _, _, is_short in CLAIMS if is_short]
    chained = [
        name for _, name, category, _, _ in CLAIMS if category == "chained"
    ]
    correlated_cosmology = ["omega_lambda", "omega_dm", "omega_b"]

    results = {
        "status": "rpft_atlas_contains_real_pi_patterns_but_not_26_independent_predictions",
        "date": "2026-08-04",
        "source_audit": {
            "atlas_path": "RPFT-main/Проработка/atlas.md",
            "master_path_named_by_atlas": "Проработка/26-stparam.md",
            "actual_master_path": "RPFT-main/base/26-stparam.md",
            "atlas_claims_26_parameters": "26 фундаментальных параметров" in atlas,
            "master_numbered_rows": len(CLAIMS),
            "master_status_final_verified": "FINAL VERIFIED" in master,
        },
        "dependency_classification": {
            "category_counts": category_counts,
            "explicit_pi_claim_count": len(explicit_pi),
            "explicit_pi_claims": explicit_pi,
            "short_displayed_pi_candidate_count": len(short_pi),
            "short_displayed_pi_candidates": short_pi,
            "chained_claim_count": len(chained),
            "chained_claims": chained,
            "interpretation": (
                "The 31 table rows cannot be multiplied as 31 independent hits. "
                "Several are anchors, derived identities, upper bounds, or outputs "
                "reusing S_vac, alpha, particle masses and earlier fitted rows."
            ),
        },
        "correlation_witnesses": {
            "cosmology_partition": {
                "claims": correlated_cosmology,
                "identity": (
                    "(1-1/pi)+(1/pi-1/(2*pi^2))+1/(2*pi^2)=1"
                ),
                "independent_degrees_of_freedom_at_most": 2,
            },
            "neutrino_chain": {
                "primary_mass_inputs": ["neutrino_3", "neutrino_2", "neutrino_1"],
                "derived_rows": ["delta_m31", "delta_m21", "neutrino_sum"],
            },
            "electroweak_chain": {
                "derived_rows": ["w_boson", "vacuum_vev"],
                "reused_inputs": ["z_boson", "weinberg_angle", "g2"],
            },
        },
        "version_drift": {
            "changed_formula_family_count": len(VERSION_DRIFT),
            "families": VERSION_DRIFT,
            "interpretation": (
                "Formula replacement after comparison with observables is a "
                "look-elsewhere channel even when every final coefficient is discrete."
            ),
        },
        "preserved_candidates": [
            {
                "observable": "strong_coupling",
                "formula": "1/(pi^2/4+6)",
                "reason": "short, dimensionless and numerically sharp",
            },
            {
                "observable": "weinberg_angle",
                "formula": "(8-3/(4*pi))/(21+4*pi)",
                "reason": "sharp but has a wider integer search grammar",
            },
            {
                "observable": "light_quark_ratios",
                "formula": "pi+1, pi^2-1, 1/(pi^2+1/3)",
                "reason": "simple patterns, limited by mass scheme and uncertainty",
            },
            {
                "observable": "cosmic_composition",
                "formula": "1-1/pi, 1/pi-1/(2*pi^2), 1/(2*pi^2)",
                "reason": "elegant partition, but the three rows sum to one identically",
            },
        ],
        "scientific_verdict": {
            "positive": (
                "The atlas is more interesting than a single tau coincidence: it "
                "contains a reusable family of short pi patterns across sectors."
            ),
            "negative": (
                "It does not provide 26 or 31 independent blind predictions because "
                "the formula grammar changes by observable and by version, while many "
                "rows are chained or correlated."
            ),
            "correct_next_test": (
                "Freeze one universal expression generator and complexity budget, "
                "hide a set of observables, and compare its full multi-target score "
                "against random constants and permuted targets."
            ),
        },
    }

    assert len(CLAIMS) == 31
    assert len(short_pi) == 12
    assert len(chained) == 9
    assert len(VERSION_DRIFT) == 6

    Path("s2t_rpft_pi_atlas_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "numbered_rows": len(CLAIMS),
                "short_pi_candidates": len(short_pi),
                "chained_rows": len(chained),
                "changed_formula_families": len(VERSION_DRIFT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()