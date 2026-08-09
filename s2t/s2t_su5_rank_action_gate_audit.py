import json
import math
from pathlib import Path


def main():
    fundamental_trace = {
        "SU3_generator_squared": 0.5,
        "SU2_generator_squared": 0.5,
        "raw_hypercharge_squared": 5.0 / 6.0,
    }
    hypercharge_normalization = (
        fundamental_trace["raw_hypercharge_squared"]
        / fundamental_trace["SU2_generator_squared"]
    )
    sin2_unification = 1.0 / (1.0 + hypercharge_normalization)

    mixed_single = {
        "representation": "(3,2)_{5/6}",
        "dimension": 6,
        "SU3_Dynkin_index": 2.0 * 0.5,
        "SU2_Dynkin_index": 3.0 * 0.5,
        "U1_GUT_index": (3.0 / 5.0) * (25.0 / 36.0) * 6.0,
    }
    mixed_pair = {
        key: 2.0 * value
        for key, value in mixed_single.items()
        if key.endswith("index")
    }

    adjoint_subgroup_indices = {
        "SU3": 3.0 + mixed_pair["SU3_Dynkin_index"],
        "SU2": 2.0 + mixed_pair["SU2_Dynkin_index"],
        "U1_GUT": mixed_pair["U1_GUT_index"],
    }

    tests = [
        {
            "gate": "canonical_SU5_trace",
            "status": "fail_atlas_low_energy_formula",
            "finding": (
                "A single SU5-invariant quadratic trace fixes kY=5/3 and "
                "sin^2(theta_W)=3/8 at the unification normalization. It does not "
                "produce the atlas value 0.2312 without running or thresholds."
            ),
        },
        {
            "gate": "rank_vs_Dynkin_index",
            "status": "fail_rank_is_not_gauge_kinetic_weight",
            "finding": (
                "The mixed block has dimension 6, but its canonical subgroup indices "
                "are (I1,I2,I3)=(5/2,3/2,1) for one complex block and (5,3,2) for "
                "the conjugate pair. Gauge kinetic and loop coefficients use these "
                "indices, not the raw state count 6."
            ),
        },
        {
            "gate": "single_involution_weight",
            "status": "fail_cannot_separate_C_W_Y",
            "finding": (
                "The torsion involution has only eigenvalues plus and minus. Any weight "
                "f(P) gives one common coefficient to the even C, W and Y blocks and "
                "one coefficient to X/Xbar. It cannot generate the distinct 8, 3 and 1 "
                "roles required by the Weinberg selector."
            ),
        },
        {
            "gate": "involution_plus_hypercharge",
            "status": "fail_still_degenerate_on_unbroken_blocks",
            "finding": (
                "ad(Y)^2 distinguishes the mixed blocks from the unbroken algebra but "
                "vanishes on C, W and Y. Functions of P and ad(Y)^2 still cannot "
                "distinguish the three unbroken sectors."
            ),
        },
        {
            "gate": "most_general_SM_invariant_trace",
            "status": "fail_hidden_weights",
            "finding": (
                "After SU5 breaking, the most general positive SM-invariant gauge "
                "quadratic form has independent coefficients for su3, su2 and u1. "
                "Removing one overall scale leaves two continuous relative weights."
            ),
        },
        {
            "gate": "explicit_block_projectors",
            "status": "tautological_reconstruction",
            "finding": (
                "Projectors P_C, P_W and P_Y can reproduce the atlas coefficients, "
                "but inserting them with separately chosen functions is exactly the "
                "observable-specific selector that the action was supposed to derive."
            ),
        },
        {
            "gate": "mixed_threshold_direction",
            "status": "fail_rank_direction",
            "finding": (
                "A complete X/Xbar threshold contributes in the fixed GUT-normalized "
                "index direction (Delta b1,Delta b2,Delta b3) proportional to (5,3,2), "
                "not a universal rank-six direction. Spin changes the common prefactor, "
                "not this representation-index ratio."
            ),
        },
    ]

    results = {
        "status": "SU5_rank_selector_not_derived_by_canonical_single_trace_action",
        "date": "2026-08-04",
        "canonical_trace": {
            "fundamental_trace": fundamental_trace,
            "kY": hypercharge_normalization,
            "sin2_thetaW_unification": sin2_unification,
            "adjoint_subgroup_indices": adjoint_subgroup_indices,
            "equal_adjoint_index_check": max(adjoint_subgroup_indices.values())
            - min(adjoint_subgroup_indices.values()),
        },
        "mixed_block": {
            "single_complex_block": mixed_single,
            "charge_conjugate_pair_indices": mixed_pair,
            "rank": 6,
            "rank_fraction": 6.0 / 24.0,
            "mismatch": (
                "rank data (6,1/4) and gauge trace data (5/2,3/2,1) are different invariants"
            ),
        },
        "action_classification": {
            "SU5_invariant": "one gauge weight; predicts unified normalization",
            "P_invariant": "two parity weights, but C/W/Y remain degenerate",
            "P_and_adY_invariant": "mixed/unbroken split only; C/W/Y remain degenerate",
            "SM_invariant": "three unbroken gauge weights; two relative continuous parameters",
            "explicit_sector_projectors": "can encode atlas formulas but is not a derived selector",
        },
        "tests": tests,
        "scientific_verdict": {
            "positive": (
                "The rank reconstruction remains an exact and unusually economical "
                "representation-theoretic encoding of the atlas coefficients."
            ),
            "negative": (
                "Canonical gauge actions and one-loop traces use generator norms and "
                "Dynkin indices, not raw block dimensions. The minimal SU5/P/Y action "
                "therefore cannot derive both rank-selector formulas."
            ),
            "status_change": (
                "Downgrade the SU5 rank selector from candidate common action to a "
                "spectral-address mnemonic pending a new noncanonical measure theorem."
            ),
            "surviving_route": (
                "Use representation indices in a scheme-safe relative determinant; "
                "do not promote rank fractions directly to gauge couplings."
            ),
        },
    }

    assert abs(hypercharge_normalization - 5.0 / 3.0) < 1e-14
    assert abs(sin2_unification - 3.0 / 8.0) < 1e-14
    assert results["canonical_trace"]["equal_adjoint_index_check"] < 1e-14
    assert mixed_pair == {
        "SU3_Dynkin_index": 2.0,
        "SU2_Dynkin_index": 3.0,
        "U1_GUT_index": 5.0,
    }

    Path("s2t_su5_rank_action_gate_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "kY": hypercharge_normalization,
                "sin2_unification": sin2_unification,
                "adjoint_indices": adjoint_subgroup_indices,
                "mixed_pair_indices_U1_SU2_SU3": [
                    mixed_pair["U1_GUT_index"],
                    mixed_pair["SU2_Dynkin_index"],
                    mixed_pair["SU3_Dynkin_index"],
                ],
                "failed_gates": len(tests),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()