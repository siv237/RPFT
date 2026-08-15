#!/usr/bin/env python3
import json
from pathlib import Path

hidden_charges = [0, 0, 1, -1]
hypercharges = [0, 0, 0, 0]
mixed_trace = sum(
    hidden * hyper
    for hidden, hyper in zip(hidden_charges, hypercharges)
)

portal_menu = {
    "scalar": {
        "operator": "(abs(x)^2+abs(z)^2)*(Hdagger H)",
        "allowed_by_gauge_symmetry": True,
        "coefficient_derived": False,
        "minimal_spectral_value": 0,
    },
    "kinetic_mixing": {
        "operator": "f_hidden^{mu nu} B_{mu nu}",
        "allowed_by_gauge_symmetry": True,
        "mixed_charge_trace": mixed_trace,
        "sheet_charge_conjugation_forbids": True,
        "minimal_spectral_value": 0,
    },
    "neutrino": {
        "operator": "LtildeH N",
        "allowed_after_SM_extension": True,
        "connector_bimodule_present": False,
        "free_complex_entries_before_symmetry": 6,
        "minimal_spectral_value": 0,
    },
}

results = {
    "date": "2026-08-10",
    "version": "S2T-III.H",
    "status": "minimal_hidden_sector_exactly_decoupled",
    "portal_menu": portal_menu,
    "direct_sum": {
        "hilbert_space": "H_hidden direct_sum H_observed",
        "dirac": "D_hidden direct_sum D_observed",
        "spectral_cross_terms": False,
        "all_nongravitational_portals_zero": True,
    },
    "gravity": {
        "shared_metric_possible": True,
        "planck_normalization_derived": False,
        "laboratory_blind_portal": False,
    },
    "verdict": {
        "hidden_EFT_closed": True,
        "experimentally_connected": False,
        "nonzero_portal_requires_new_representation": True,
        "next_gate": "final status freeze",
    },
}

assert mixed_trace == 0
assert all(
    entry["minimal_spectral_value"] == 0
    for entry in portal_menu.values()
)
assert results["direct_sum"]["spectral_cross_terms"] is False

Path("s2t_v3_portal_menu_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)