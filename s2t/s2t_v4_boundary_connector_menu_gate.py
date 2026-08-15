import json


requirements = [
    "off_diagonal_finite_edge",
    "nonzero_portal_possible",
    "family_triplet_breaking",
    "rephasing_invariant_oriented_cycle",
    "local_anomaly_safe",
]

packages = [
    {
        "name": "direct_sum",
        "new_field_orbits": 0,
        "off_diagonal_finite_edge": False,
        "nonzero_portal_possible": False,
        "family_triplet_breaking": False,
        "rephasing_invariant_oriented_cycle": False,
        "local_anomaly_safe": True,
        "reason": "block diagonal spectral action has no cross terms",
    },
    {
        "name": "single_scalar_family_triplet",
        "new_field_orbits": 1,
        "off_diagonal_finite_edge": False,
        "nonzero_portal_possible": True,
        "family_triplet_breaking": True,
        "rephasing_invariant_oriented_cycle": False,
        "local_anomaly_safe": True,
        "reason": "a scalar portal is allowed, but no spectral connector edge or physical CP loop is generated",
    },
    {
        "name": "single_vectorlike_messenger_pair",
        "new_field_orbits": 1,
        "off_diagonal_finite_edge": True,
        "nonzero_portal_possible": True,
        "family_triplet_breaking": False,
        "rephasing_invariant_oriented_cycle": False,
        "local_anomaly_safe": True,
        "reason": "the pair can bridge charges, but one mass path is family blind and its phase is removable",
    },
    {
        "name": "family_triplet_single_messenger_chain",
        "new_field_orbits": 2,
        "off_diagonal_finite_edge": True,
        "nonzero_portal_possible": True,
        "family_triplet_breaking": True,
        "rephasing_invariant_oriented_cycle": False,
        "local_anomaly_safe": True,
        "reason": "one open chain can transmit family breaking, but all edge phases can be rephased away",
    },
    {
        "name": "two_path_vectorlike_triplet_cycle",
        "new_field_orbits": 3,
        "off_diagonal_finite_edge": True,
        "nonzero_portal_possible": True,
        "family_triplet_breaking": True,
        "rephasing_invariant_oriented_cycle": True,
        "local_anomaly_safe": True,
        "reason": "two vectorlike messenger paths and one family-triplet connector can form a closed oriented loop",
    },
]

for package in packages:
    package["passes_all_requirements"] = all(package[requirement] for requirement in requirements)

passing = [package for package in packages if package["passes_all_requirements"]]
minimum_orbits = min(package["new_field_orbits"] for package in passing)
minimal_passing = [package for package in passing if package["new_field_orbits"] == minimum_orbits]

result = {
    "gate": "version4_boundary_connector_menu",
    "requirements": requirements,
    "packages": packages,
    "single_new_orbit_can_pass": any(
        package["passes_all_requirements"] and package["new_field_orbits"] == 1
        for package in packages
    ),
    "minimal_passing_packages": minimal_passing,
    "restricted_minimum_new_field_orbits": minimum_orbits,
    "status": "single-field and single-chain packages fail; the first structurally capable menu element is a two-path vectorlike triplet cycle",
    "open_mathematical_gates": [
        "real-structure and order-one compatibility",
        "explicit Standard Model and hidden charge assignment",
        "survival of a non-removable loop phase after all rephasings",
        "spectral fixing of relative coefficients",
        "absence of arbitrary M3 family matrices after messenger integration",
    ],
}

with open("s2t_v4_boundary_connector_menu_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))