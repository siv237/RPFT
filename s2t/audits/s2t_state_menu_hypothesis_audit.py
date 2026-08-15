import json
import math
from pathlib import Path

import numpy as np


def main():
    # Fundamental and first-homology data for K=RP3 x S1.
    fundamental_group = "Z2 x Z"
    torsion_order = 2
    free_rank = 1

    # Flat U(1) characters: Hom(Z2 x Z,U1) = {+1,-1} x U(1).
    flat_components = torsion_order
    flat_component_topology = "S1"
    flat_moduli = "two disjoint circles"

    # Spin structures form a torsor over H^1(K,Z2)=Z2 x Z2.
    spin_structure_count = 2**2
    enlarged_menu_components = flat_components * spin_structure_count

    # Free homotopy classes equal conjugacy classes; the group is abelian.
    loop_labels = "(epsilon,n) in Z2 x Z"

    # Explicit obstruction witness: noncommuting SU(2)-type generators cannot
    # represent the commuting generators of pi1(K).
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    commutator = sigma_x @ sigma_z - sigma_z @ sigma_x
    commutator_frobenius_norm = float(np.linalg.norm(commutator))

    # A valid two-dimensional unitary representation is reducible into
    # one-dimensional characters because both generators commute and are normal.
    torsion_generator = np.diag([1.0, -1.0]).astype(complex)
    circle_generator = np.diag(
        [np.exp(1j * math.pi / 3.0), np.exp(-1j * math.pi / 5.0)]
    )
    valid_commutator_norm = float(
        np.linalg.norm(
            torsion_generator @ circle_generator
            - circle_generator @ torsion_generator
        )
    )

    gates = {
        "coherent_state_menu": {
            "passes": True,
            "finding": (
                "K can consistently be reinterpreted as a label space for global gluing, "
                "spin and holonomy sectors rather than as a literal compact spatial dimension."
            ),
        },
        "discrete_plus_cyclic_labels": {
            "passes": True,
            "finding": (
                "Stable loop classes carry one integer winding and one Z2 torsion label, "
                "matching the minimal idea of charge plus parity."
            ),
        },
        "nonabelian_multiplets_from_base_topology": {
            "passes": False,
            "finding": (
                "pi1(K) is abelian. Every finite-dimensional unitary holonomy representation "
                "decomposes into one-dimensional characters, so irreducible SU(2) doublets and "
                "SU(3) triplets cannot come from base-loop holonomy alone."
            ),
        },
        "three_generation_selection": {
            "passes": False,
            "finding": (
                "The natural discrete counts are 2 flat components, 4 spin structures and 8 "
                "components in the enlarged spin-holonomy menu; none canonically selects 3."
            ),
        },
        "mass_spectrum_from_topology_alone": {
            "passes": False,
            "finding": (
                "Topology labels sectors but supplies no energy, stiffness or transition operator. "
                "Masses require an additional metric/action on the menu."
            ),
        },
    }

    results = {
        "status": "state_menu_hypothesis_passes_as_abelian_kinematic_skeleton_fails_as_standalone_particle_theory",
        "date": "2026-08-04",
        "hypothesis": (
            "K=RP3 x S1 is a configuration/menu space of global gluing and phase sectors, "
            "not necessarily a literal compact spatial manifold."
        ),
        "topological_data": {
            "pi1_K": fundamental_group,
            "H1_K_Z": fundamental_group,
            "flat_U1_moduli": "Hom(Z2 x Z,U1)={+1,-1} x U1",
            "flat_component_count": flat_components,
            "flat_component_topology": flat_component_topology,
            "flat_moduli_plain_language": flat_moduli,
            "spin_structure_torsor": "H1(K,Z2)=Z2 x Z2",
            "spin_structure_count": spin_structure_count,
            "enlarged_spin_holonomy_menu": "eight disjoint circles",
            "enlarged_component_count": enlarged_menu_components,
            "free_homotopy_loop_labels": loop_labels,
        },
        "nonabelian_obstruction": {
            "theorem": (
                "Finite-dimensional unitary representations of the abelian group Z2 x Z are "
                "simultaneously diagonalizable and split into one-dimensional characters."
            ),
            "valid_diagonal_representation_commutator_norm": valid_commutator_norm,
            "attempted_SU2_Pauli_generators_commutator_norm": commutator_frobenius_norm,
            "interpretation": (
                "Using noncommuting Pauli generators violates the defining commutativity relation "
                "of pi1(K); nonabelian particle multiplets require an extra fiber, groupoid or "
                "operator algebra not contained in K alone."
            ),
        },
        "gates": gates,
        "scientific_verdict": {
            "survives": (
                "The hypothesis is mathematically coherent as a kinematic classification of "
                "global phase, torsion and spin sectors."
            ),
            "fails": (
                "It cannot by itself generate nonabelian gauge multiplets, three generations, "
                "masses or dynamics."
            ),
            "minimal_extension": (
                "Replace the bare menu by a nonabelian bundle/groupoid over the two-circle moduli, "
                "with a preregistered transition operator and metric."
            ),
            "next_gate": (
                "Test whether one minimal nonabelian fiber can produce both an SU(2) doublet and "
                "an SU(3) triplet without adding independent sector choices."
            ),
        },
    }

    assert flat_components == 2
    assert spin_structure_count == 4
    assert enlarged_menu_components == 8
    assert valid_commutator_norm < 1e-14
    assert commutator_frobenius_norm > 0.0
    assert gates["coherent_state_menu"]["passes"]
    assert not gates["nonabelian_multiplets_from_base_topology"]["passes"]

    Path("s2t_state_menu_hypothesis_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "flat_moduli": flat_moduli,
                "spin_structures": spin_structure_count,
                "enlarged_menu": "eight disjoint circles",
                "loop_labels": loop_labels,
                "nonabelian_commutator_witness": commutator_frobenius_norm,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()