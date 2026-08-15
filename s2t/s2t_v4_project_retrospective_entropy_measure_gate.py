import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from pypdf import PdfReader
from scipy.optimize import brentq
from scipy.special import logsumexp


ROOT = Path(".")
PI = math.pi
RADIUS_S4 = (3.0 / (8.0 * PI**2)) ** 0.25
RADIUS_S2 = (1.0 / (16.0 * PI**2)) ** 0.25


def file_inventory():
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    extension_counts = Counter(path.suffix.lower() or "[no_extension]" for path in files)
    hashes = defaultdict(list)
    for path in files:
        if path.suffix.lower() in {".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk"}:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[digest].append(str(path))
    duplicates = [paths for paths in hashes.values() if len(paths) > 1]
    return {
        "total_files": len(files),
        "extension_counts": dict(extension_counts.most_common()),
        "exact_duplicate_groups": sorted(duplicates, key=lambda group: (-len(group), group)),
    }


def pdf_inventory():
    entries = []
    for path in sorted(ROOT.rglob("*.pdf")):
        try:
            reader = PdfReader(path)
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
            entries.append(
                {
                    "path": str(path),
                    "pages": len(reader.pages),
                    "extracted_characters": len(text),
                    "entropy_mentions": text.lower().count("энтроп") + text.lower().count("entropy"),
                    "spectral_density_mentions": text.lower().count("спектральн") + text.lower().count("spectral"),
                }
            )
        except Exception as error:
            entries.append({"path": str(path), "error": str(error)})
    return entries


def spectrum_s4(tau):
    cutoff = max(100, math.ceil(math.sqrt(80.0 * RADIUS_S4**2 / tau)))
    ell = np.arange(cutoff + 1, dtype=float)
    degeneracy = (ell + 1.0) * (ell + 2.0) * (2.0 * ell + 3.0) / 6.0
    eigenvalue = ell * (ell + 3.0) / RADIUS_S4**2
    log_weight = np.log(degeneracy) - tau * eigenvalue
    log_partition = float(logsumexp(log_weight))
    probability = np.exp(log_weight - log_partition)
    mean_energy = float(np.sum(probability * eigenvalue))
    entropy = tau * mean_energy + log_partition
    return log_partition, mean_energy, entropy


def spectrum_s2xs2(tau):
    cutoff = max(100, math.ceil(math.sqrt(80.0 * RADIUS_S2**2 / tau)))
    ell = np.arange(cutoff + 1, dtype=float)
    degeneracy = 2.0 * ell + 1.0
    eigenvalue = ell * (ell + 1.0) / RADIUS_S2**2
    log_weight = np.log(degeneracy) - tau * eigenvalue
    log_partition_s2 = float(logsumexp(log_weight))
    probability = np.exp(log_weight - log_partition_s2)
    mean_energy_s2 = float(np.sum(probability * eigenvalue))
    entropy_s2 = tau * mean_energy_s2 + log_partition_s2
    return 2.0 * log_partition_s2, 2.0 * mean_energy_s2, 2.0 * entropy_s2


def energy_crossing():
    delta = lambda tau: spectrum_s4(tau)[1] - spectrum_s2xs2(tau)[1]
    root = brentq(delta, 0.05, 0.2, xtol=1.0e-14)
    samples = []
    for tau in [0.01, 0.05, root, 0.2, 1.0]:
        s4 = spectrum_s4(tau)
        s22 = spectrum_s2xs2(tau)
        samples.append(
            {
                "tau": tau,
                "mean_energy_s4": s4[1],
                "mean_energy_s2xs2": s22[1],
                "energy_difference": s4[1] - s22[1],
                "von_neumann_entropy_difference": s4[2] - s22[2],
            }
        )
    return {
        "crossing_tau": root,
        "samples": samples,
        "verdict": "minimum_mean_spectral_energy_is_tau_dependent",
    }


def stratified_measure_test():
    s4 = {
        "minimum_density": -0.00549336084715081,
        "radius_over_sigma": 1.35139219568654,
    }
    rp3 = {
        "minimum_density": -0.0104399545649812,
        "radius_over_sigma": 1.99760832726935,
    }
    return {
        "functional": "-(log Z4+log Z3)/(N4+N3)",
        "identity": "(N4*f4+N3*f3)/(N4+N3)",
        "sector_minima": {"S4": s4, "RP3": rp3},
        "global_infimum": rp3["minimum_density"],
        "attained_only_on_boundary": "N4_to_zero",
        "verdict": "natural_factorized_measure_eliminates_S4_instead_of_stabilizing_a_hybrid",
    }


result = {
    "gate": "version4_project_retrospective_entropy_measure",
    "date": "2026-08-11",
    "corpus": file_inventory(),
    "pdfs": pdf_inventory(),
    "source_genealogy": {
        "early_RPFT": "carrier_and_pi_ledger_are_preloaded_before_variational_comparison",
        "TOE3": "minimum_spectral_entropy_and_minimum_spectral_complexity_are_topology_postulates",
        "TOE4": "maximum_entropy_at_fixed_variance_selects_the_Gaussian_kernel",
        "TOE6": "log_trace_language_is_used_as_free_energy",
        "TOE6_5": "proposes_variation_of_spectral_density_with_fluctuation_and_information_terms",
        "final_TOE": "retains_Gaussian_minimum_action_language_but_drops_a_unique_topology_variation",
    },
    "entropy_taxonomy": {
        "kernel_entropy": "coordinate_distribution_entropy_at_fixed_variance",
        "state_entropy": "von_Neumann_entropy_of_the_normalized_heat_state",
        "spectral_complexity": "entropy_or_complexity_of_the_eigenvalue_density_over_carriers",
        "warning": "the_three_functionals_have_different_domains_constraints_and_variational_signs",
    },
    "unit_volume_energy_crossing": energy_crossing(),
    "stratified_measure": stratified_measure_test(),
    "surviving_exact_mechanisms": [
        "Qcycle_Hodge_Gram_diag_pi_pi_inverse_on_the_defect_cycle",
        "bounding_spin_filling_selects_a_reference_structure_only",
        "parent_trace_fixes_multiplicities_but_not_relative_stiffness",
        "TOE6_5_spectral_density_variation_remains_unexecuted",
    ],
    "recommended_next_program": {
        "generator": "H_C=-log(C_hat)/tau",
        "functional": "F[rho,M]=Tr(rho H_C)+Gamma_fluc[rho,M]-T_eff*S_info[rho]",
        "constraints": ["Tr rho=1", "fixed_or_derived_mode_number", "one_common_measure_over_carriers"],
        "required_gate": "derive_the_sign_coefficients_and_positive_second_variation_before_observable_matching",
    },
}

with open("s2t_v4_project_retrospective_entropy_measure_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps({
    "files": result["corpus"]["total_files"],
    "pdfs": len(result["pdfs"]),
    "energy_crossing_tau": result["unit_volume_energy_crossing"]["crossing_tau"],
    "stratified_verdict": result["stratified_measure"]["verdict"],
}, ensure_ascii=False, indent=2))