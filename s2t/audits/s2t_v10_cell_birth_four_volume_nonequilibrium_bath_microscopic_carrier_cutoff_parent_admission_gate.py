#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_continuum_dispersion_cell_geometry_typed_embedding_gate",
        "cutoffs": {
            "brillouin_momentum_times_length": "pi",
            "corner_frequency_times_length_over_velocity": "2*sqrt(3)",
            "K43_spectral_cutoff_times_length": 42,
            "spectral_to_brillouin_ratio": "42/pi",
            "spectral_energy_to_corner_frequency_ratio_if_vg_eq_c": "7*sqrt(3)",
            "uv_correlation_time_times_frequency": 1,
        },
        "parent": {
            "coordinates": ["k_BZ ell_cell", "omega_UV ell_cell/v_g", "Lambda_43 ell_cell"],
            "minimum": ["pi", "2*sqrt(3)", 42],
            "hessian": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "rank": 3,
            "determinant": 1,
        },
        "scale_audit": {
            "map": [[int(value) for value in row] for row in certificate.scale_map.tolist()],
            "rank_nullity": "3/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
            "after_velocity_anchor": "4/1",
            "after_velocity_and_length_anchors": "5/0",
        },
        "status": {
            "conditional_parent_admission": "9/9",
            "dimensionless_cutoff_bridge": "3/3",
            "microscopic_carrier_origin": "0/1",
            "absolute_cutoff_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "common_dimensionless_cutoff_parent_exists": True,
            "operator_norm_selects_conditional_lattice_cutoff": True,
            "four_volume_derives_microscopic_carrier": False,
            "cutoff_parent_derives_absolute_uv_scale": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()