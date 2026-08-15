#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np


def finite_modular_counterexample():
    logarithmic_weights = np.array([0.0, -1.0, -math.sqrt(2.0)])
    frequencies = sorted(
        {
            abs(float(left - right))
            for left in logarithmic_weights
            for right in logarithmic_weights
            if abs(left - right) > 1e-14
        }
    )
    return {
        "faithful_density_matrix": (
            "rho=Z^(-1) diag(1,exp(-1),exp(-sqrt(2)))"
        ),
        "modular_action_on_matrix_units": (
            "sigma_t(E_ij)=exp[i t(log p_i-log p_j)] E_ij"
        ),
        "positive_frequencies": frequencies,
        "periodicity_requirement": (
            "A common T would require T=2*pi*m and T*sqrt(2)=2*pi*n."
        ),
        "contradiction": "sqrt(2)=n/m would be rational",
        "finite_system_periodic": False,
        "finding": (
            "Finite dimensionality and the KMS property do not force periodic "
            "real modular time."
        ),
    }


def main():
    prompt = Path("RPFT-main/ai-promts/First-principles-00.md")
    text = prompt.read_text(encoding="utf-8")
    required_markers = [
        "Spin(3)",
        "SU(2)",
        "Z_2",
        "Томиты",
        "KMS",
        "периодич",
        "многообразие-продукт",
    ]
    marker_counts = {marker: text.count(marker) for marker in required_markers}
    modular_counterexample = finite_modular_counterexample()
    results = {
        "status": "zero_prompt_conditionally_reconstructs_RP3_times_S1_but_does_not_make_it_an_inevitable_vacuum",
        "date": "2026-08-06",
        "source": str(prompt),
        "source_markers": marker_counts,
        "deduction_ledger": [
            {
                "step": "unit quaternion group manifold",
                "input": (
                    "compact, simply connected, three-dimensional group manifold "
                    "of unit quaternions"
                ),
                "output": "SU(2) is diffeomorphic to S3",
                "status": "valid conditional deduction",
                "hidden_choice": (
                    "Dimension three, simple connectivity, group-manifold form and "
                    "quaternionic symmetry were assumed rather than minimized."
                ),
            },
            {
                "step": "central quotient",
                "input": "identify the central action {+1,-1} on SU(2)",
                "output": "SU(2)/Z2=SO(3) is diffeomorphic to RP3",
                "status": "valid conditional deduction",
                "hidden_choice": (
                    "A real structure J does not by itself identify antipodal base "
                    "points; physical triviality of the center is an extra axiom."
                ),
            },
            {
                "step": "modular time",
                "input": "finite equilibrium KMS state",
                "output": "periodic time S1",
                "status": "invalid as a general deduction",
                "hidden_choice": (
                    "Tomita-Takesaki gives an R-parameter automorphism group. "
                    "Periodicity requires commensurate modular frequencies or an "
                    "additional Euclidean thermal-circle postulate."
                ),
            },
            {
                "step": "four-dimensional synthesis",
                "input": "RP3 spatial sector and an assumed circle",
                "output": "RP3 times S1",
                "status": "valid only after a product axiom",
                "hidden_choice": (
                    "The prompt excludes warped products and nontrivial circle "
                    "bundles without a dynamical or spectral argument."
                ),
            },
            {
                "step": "vacuum and spectral density",
                "input": "the resulting compact manifold",
                "output": "minimum-energy spectrally dense vacuum",
                "status": "not established",
                "hidden_choice": (
                    "No energy functional, comparison class, radius equation or "
                    "definition of spectral density is supplied."
                ),
            },
        ],
        "exact_conditional_result": {
            "manifold": "RP3 times S1",
            "fundamental_group": "Z2 times Z",
            "valid_if": [
                "the quaternionic S3 spatial group manifold is fixed",
                "the center acts trivially on physical base points",
                "a periodic circle is independently required",
                "the total geometry is a direct product",
            ],
        },
        "modular_periodicity_counterexample": modular_counterexample,
        "bundle_nonuniqueness_gate": {
            "classification": (
                "principal U(1) bundles over RP3 are classified by H^2(RP3;Z)"
            ),
            "cohomology_group": "Z2",
            "bundle_classes": 2,
            "finding": (
                "Even after selecting RP3 and a circle fiber, topology alone leaves "
                "a trivial and a nontrivial circle-bundle class; the direct product "
                "is not automatic."
            ),
        },
        "scale_gate": {
            "radius_fixed_by_zero_prompt": False,
            "finding": (
                "The zero prompt selects no metric radius. The later value r=1 is a "
                "normalization convention until a spectral action fixes the scale."
            ),
        },
        "inevitability_definition_of_done": [
            "define a candidate class without inserting RP3 or S1",
            "define one normalized spectral or free-energy functional",
            "derive the center quotient from algebra and real structure",
            "derive or reject periodic modular spectrum",
            "compare product and nontrivial circle-bundle sectors",
            "prove a unique stable minimizer modulo isometry and scale",
        ],
        "scientific_verdict": {
            "survives": (
                "RP3 times S1 is a coherent minimal candidate and conditional "
                "calculations based on it remain valid."
            ),
            "corrected_status": (
                "The zero prompt does not derive this carrier as the unique vacuum. "
                "It encodes the quaternionic spatial choice, center quotient, periodic "
                "circle and product structure in the questions."
            ),
            "next_gate": (
                "Replace the target-loaded prompt by a variational classification "
                "problem and test whether RP3 times S1 is a unique stable minimizer."
            ),
        },
    }
    assert all(count > 0 for count in marker_counts.values())
    assert not modular_counterexample["finite_system_periodic"]
    assert results["bundle_nonuniqueness_gate"]["bundle_classes"] == 2
    Path("s2t_zero_prompt_inevitability_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "conditional_manifold": results["exact_conditional_result"][
                    "manifold"
                ],
                "modular_time_forced_periodic": False,
                "circle_bundle_classes": 2,
                "radius_derived": False,
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()