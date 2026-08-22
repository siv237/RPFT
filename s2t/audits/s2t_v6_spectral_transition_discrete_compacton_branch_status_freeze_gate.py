#!/usr/bin/env python3
"""Freeze the compacton branch against the R0--R6 admission contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_discrete_compacton_branch_status_freeze_gate_results.json"


def load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def main() -> None:
    existence = load("s2t_v6_spectral_transition_discrete_compacton_existence_gate_results.json")
    stability = load("s2t_v6_spectral_transition_discrete_compacton_stability_quantization_gate_results.json")
    scale = load("s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate_results.json")
    capture = load("s2t_v6_spectral_transition_discrete_compacton_dynamical_capture_gate_results.json")
    selector = load("s2t_v6_spectral_transition_compacton_c4_affine_selector_admissibility_gate_results.json")
    eta = load("s2t_v6_spectral_transition_discrete_compacton_c4_boundary_eta_dissipation_gate_results.json")
    degeneracy = load("s2t_v6_spectral_transition_discrete_compacton_energy_degeneracy_boundary_overlap_gate_results.json")
    radiation = load("s2t_v6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate_results.json")

    assert existence["interpretation"]["exact_finite_support_compacton_exists"] is True
    assert abs(existence["symmetric_two_site_branch"]["minimal_positive_coupling"] - 2.0 * 3.141592653589793) < 1.0e-12
    assert stability["symmetry_reduction"]["reduced_expanding_multiplier_count"] == 0
    assert stability["interpretation"]["global_nonlinear_stability_proved"] is False
    assert scale["dimensional_rank_test"]["scale_nullity"] == 1
    assert scale["interpretation"]["absolute_mass_derived"] is False
    assert capture["exact_invariant_manifold"]["return_law"] == "F^2(Psi)=-Psi"
    assert capture["generic_capture_protocol"]["total_captures"] == 0
    assert selector["compacton_character_selector"]["zero_phase_points"] == [0.5, 1.5]
    assert selector["verdict"]["autonomous_capture_mechanism_derived"] is False
    assert eta["verdict"]["eta_pfaffian_phase_derives_weak_dissipation"] is False
    assert eta["verdict"]["jump_operator_and_rate_parent_derived"] is False
    assert degeneracy["verdict"]["plus_minus_compacton_real_energies_exactly_degenerate"] is True
    assert degeneracy["verdict"]["scalar_boundary_derivative_generates_transition"] is False
    assert radiation["spectral_form_factor"]["absolutely_continuous_outgoing_channel_detected"] is True
    assert radiation["capture_test"]["undesired_character_is_damped"] is False
    assert radiation["capture_test"]["compacton_core_is_depleted"] is True

    requirements = {
        "R0": {
            "status": "partial",
            "finding": "The chiral walk carrier is explicit, but the selected spatial axis and the S4-to-C4 boundary are conditional choices rather than consequences of the full physical H15 parent.",
        },
        "R1": {
            "status": "partial",
            "finding": "One exact nonlinear unitary walk generates the compacton, but the C4 boundary, affine selector and any open-system law are not derived from the same Real/gauge parent functional.",
        },
        "R2": {
            "status": "failed",
            "finding": "The exact family is not an isolated attractor, its two-step law is F^2=-1, and none of 36 generic localized trials is captured.",
        },
        "R3": {
            "status": "failed",
            "finding": "Eta/Pfaffian data give orientation but zero decay rate. The exact coefficient 4pi^2 measures secular core radiation, not a normalized creation or capture rate.",
        },
        "R4": {
            "status": "failed",
            "finding": "A finite-support solution with locally neutral Floquet spectrum exists, but there is a continuous invariant manifold, a neutral quadrature and finite-amplitude radiative escape rather than a unique stable endpoint.",
        },
        "R5": {
            "status": "failed",
            "finding": "Kappa=2pi and E*L=pi*hbar*c are scale-free lattice relations; no absolute mass, size, lifetime or physical rate is predicted.",
        },
        "R6": {
            "status": "passed",
            "finding": "Existence, stability, scale, capture, symmetry, eta, degeneracy and radiation claims all have reproducible machine certificates and explicit stop criteria.",
        },
    }
    counts = {
        status: sum(item["status"] == status for item in requirements.values())
        for status in ("passed", "partial", "failed")
    }
    assert counts == {"passed": 1, "partial": 2, "failed": 4}

    retained = [
        "exact two-site compactons at kappa=2(2m+1)pi with minimal branch 2pi",
        "the exact continuous two-site manifold with F^2=-1",
        "absence of expanding symmetry-reduced Floquet multipliers in the tested finite volumes",
        "the coefficient-free diagnostic D_chi=4 w_plus w_minus with zero locus plus/minus i",
        "a consistent conditional S4-to-one-C4 boundary construction",
        "the exact outgoing density rho_rad(0)=2pi and coefficient 4pi^2",
        "the compacton as a benchmark for nonlinear localization and radiative escape",
    ]
    rejected = [
        "autonomous formation from generic or vacuum initial data",
        "canonical selection of one plus/minus i branch by the existing parent",
        "eta/Pfaffian-derived amplitude damping or a parent-derived gamma",
        "radiative stabilization through the already present massless continuum",
        "an absolute compacton mass, size or lifetime",
        "identification of the compacton with a physically admitted matter-birth endpoint",
    ]

    result = {
        "gate": "version6_spectral_transition_discrete_compacton_branch_status_freeze_gate",
        "source_gate_count": 8,
        "source_gates": [
            existence["gate"], stability["gate"], scale["gate"], capture["gate"],
            selector["gate"], eta["gate"], degeneracy["gate"], radiation["gate"],
        ],
        "exact_ledger": {
            "minimal_coupling": existence["symmetric_two_site_branch"]["minimal_positive_coupling"],
            "return_law": capture["exact_invariant_manifold"]["return_law"],
            "generic_captures": capture["generic_capture_protocol"]["total_captures"],
            "generic_trials": capture["generic_capture_protocol"]["total_trials"],
            "scale_nullity": scale["dimensional_rank_test"]["scale_nullity"],
            "reduced_expanding_multiplier_count": stability["symmetry_reduction"]["reduced_expanding_multiplier_count"],
            "radiation_density": radiation["spectral_form_factor"]["spectral_density_at_multiplier_one"],
            "radiation_coefficient": radiation["spectral_form_factor"]["golden_rule_coefficient_per_four_step_cycle"],
            "undesired_character_is_damped": radiation["capture_test"]["undesired_character_is_damped"],
        },
        "R0_R6_ledger": requirements,
        "status_counts": counts,
        "retained_results": retained,
        "rejected_claims": rejected,
        "freeze_rule": {
            "same_architecture_variants_allowed": False,
            "reopening_requires_simultaneously": [
                "a parent-derived physical scale",
                "a nonzero basin of capture from generic or vacuum-compatible initial data",
                "negative real decay for every physical transverse character quadrature while the core survives",
                "derivation of the C4 boundary or affine mixer and the open channel from one parent",
                "a normalized physical rate or blind observable",
            ],
        },
        "verdict": {
            "exact_mathematical_branch_retained": True,
            "autonomous_matter_birth_mechanism_admitted": False,
            "compacton_branch_frozen": True,
            "status": "the discrete compacton branch is a genuine exact nonlinear lattice solution and a useful radiation benchmark, but it fails R2--R5 and only partially satisfies R0--R1. It is therefore frozen as an autonomous matter-birth mechanism; further variants are barred unless one new parent simultaneously derives scale, capture, all-quadrature damping, boundary coupling and a physical rate.",
            "next_gate": "version6_spectral_transition_post_compacton_program_reprioritization_gate",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()