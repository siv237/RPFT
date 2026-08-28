#!/usr/bin/env python3
"""Audit whether existing reductions derive the one-copy quotient metric."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    physical_hessians,
    signature,
)
from s2t_v7_incidence_transfer_markov_weight_gate import (
    polar_coisometry,
    quotient_hessians,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_index_defect_reduced_linking_quotient_gate_results.json"


def load_result(name: str) -> dict:
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, support, defect = polar_coisometry(reference)
    physical_origin, physical_vacuum = physical_hessians(reference, variations)
    quotient_origin, quotient_vacuum = quotient_hessians(
        reference, variations, transfer
    )
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))

    # A diagonal matched curvature (Z,Z) has squared norm 2||Z||^2 in the
    # original two-corner carrier.  The pre-existing 1/2 Hodge trace therefore
    # induces ||Z||^2 on the quotient, i.e. twice the raw one-corner action
    # 1/2||Z||^2 used in the previous local pass.
    inherited_origin = 2.0 * quotient_origin
    inherited_vacuum = 2.0 * quotient_vacuum
    inherited_origin_residual = float(np.linalg.norm(
        inherited_origin - physical_origin
    ))

    raw_origin_values = eigvalsh(edge_origin + quotient_origin)
    raw_vacuum_values = eigvalsh(edge_vacuum + quotient_vacuum)
    inherited_origin_values = eigvalsh(edge_origin + inherited_origin)
    inherited_vacuum_values = eigvalsh(edge_vacuum + inherited_vacuum)

    def heavy_minimum(metric_scale: float) -> float:
        values = eigvalsh(edge_origin + metric_scale * quotient_origin)
        return float(values[7])

    critical_metric_scale = brentq(heavy_minimum, 1.0, 2.0)

    forest = load_result("s2t_v7_real_arrow_bimodule_forest_quotient_gate_results.json")
    real_half = load_result("s2t_v7_real_half_trace_curvature_weight_gate_results.json")

    # At the zero field, every infinitesimal vertex-gauge variation is
    # delta A = xi_t A - A xi_s = 0.  Hence a nonzero negative Hessian mode
    # cannot be removed as a vertical gauge direction at the origin.
    rng = np.random.default_rng(20260828)
    xi_source = rng.normal(size=(11, 11))
    xi_target = rng.normal(size=(10, 10))
    zero_field = np.zeros((10, 11))
    zero_gauge_variation = xi_target @ zero_field - zero_field @ xi_source
    zero_gauge_orbit_residual = float(np.linalg.norm(zero_gauge_variation))

    assert np.linalg.matrix_rank(support, 1.0e-10) == 10
    assert np.linalg.matrix_rank(defect, 1.0e-10) == 1
    assert inherited_origin_residual < 1.0e-12
    assert signature(raw_origin_values) == [7, 0, 20]
    assert signature(inherited_origin_values) == [21, 0, 6]
    assert signature(raw_vacuum_values) == [0, 0, 27]
    assert signature(inherited_vacuum_values) == [0, 0, 27]
    assert abs(critical_metric_scale - 16.0 / 15.0) < 1.0e-10
    assert forest["ordinary_inner_fluctuation_test"][
        "is_standard_finite_Dirac_inner_fluctuation"
    ] is False
    assert forest["family_frame_quotient"][
        "relative_cycle_zero_modes"
    ] == 9
    assert real_half["verdict"]["beta_half_derived"] is False
    assert zero_gauge_orbit_residual == 0.0

    result = {
        "gate": "version7_index_defect_reduced_linking_quotient_gate",
        "matched_carrier": {
            "source_support_rank": 10,
            "target_rank": 10,
            "index_defect_rank": 1,
            "polar_transfer_is_coisometry": True,
        },
        "quotient_metric_comparison": {
            "raw_one_corner_action": "1/2 ||Z||^2",
            "inherited_two_corner_action": "||Z||^2",
            "inherited_metric_scale_relative_to_raw": 2,
            "inherited_origin_equals_old_physical_origin_residual": inherited_origin_residual,
            "critical_metric_scale": critical_metric_scale,
            "exact_critical_metric_scale": "16/15",
            "allowed_metric_scale_window": "0 <= c < 16/15",
            "raw_origin_signature": signature(raw_origin_values),
            "raw_origin_heavy_gap": float(raw_origin_values[7]),
            "raw_vacuum_signature": signature(raw_vacuum_values),
            "raw_vacuum_minimum_eigenvalue": float(raw_vacuum_values[0]),
            "inherited_origin_signature": signature(inherited_origin_values),
            "inherited_origin_heavy_gap": float(inherited_origin_values[7]),
            "inherited_vacuum_signature": signature(inherited_vacuum_values),
            "inherited_vacuum_minimum_eigenvalue": float(inherited_vacuum_values[0]),
        },
        "existing_reductions": {
            "real_half_trace_derives_raw_metric": False,
            "arrow_module_ordinary_inner_fluctuation_available": False,
            "forest_quotient_relative_moduli_dimension": 9,
            "forest_quotient_acts_on_endpoint_gram_duplication": False,
            "zero_field_gauge_orbit_residual": zero_gauge_orbit_residual,
            "brst_can_remove_extra_origin_negative_mode_as_gauge": False,
            "represented_junk_derives_metric_rescaling": False,
        },
        "verdict": {
            "raw_quotient_local_pass_is_reproducible": True,
            "raw_quotient_metric_is_inherited_from_current_parent": False,
            "existing_real_junk_forest_brst_reduction_derives_half": False,
            "status": "raw_quotient_metric_not_derived_existing_reductions_no_go",
            "next_gate": "version7_polar_transfer_cross_curvature_origin_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()