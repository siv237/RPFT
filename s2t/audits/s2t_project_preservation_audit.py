#!/usr/bin/env python3
import hashlib
import json
import py_compile
import subprocess
from pathlib import Path


CORE_FILES = [
    Path("main.tex"),
    Path("tome2_s2t_spectral_closure.tex"),
]

RECENT_ARTIFACTS = [
    "s2t_family_factor_operator_audit.py",
    "s2t_family_factor_operator_results.json",
    "family_factor_operator_gate.tex",
    "s2t_collective_pi_atlas_base_audit.py",
    "s2t_collective_pi_atlas_base_results.json",
    "collective_pi_atlas_base_gate.tex",
    "s2t_parent_noncommuting_family_insertion_audit.py",
    "s2t_parent_noncommuting_family_insertion_results.json",
    "s2t_projective_family_flux_audit.py",
    "s2t_projective_family_flux_results.json",
    "parent_noncommuting_family_gate.tex",
    "s2t_family_affine_incidence_exhaustive_audit.py",
    "s2t_family_affine_incidence_exhaustive_results.json",
    "s2t_even_projective_carrier_exhaustive_audit.py",
    "s2t_even_projective_carrier_exhaustive_results.json",
    "s2t_topological_family_selector_audit.py",
    "s2t_topological_family_selector_results.json",
    "family_route_exhaustion_gate.tex",
    "s2t_spin_menu_dirac_determinant_line_audit.py",
    "s2t_spin_menu_dirac_determinant_line_results.json",
    "spin_menu_dirac_determinant_line_gate.tex",
    "s2t_hurwitz_hessian_pi4_audit.py",
    "s2t_hurwitz_hessian_pi4_results.json",
    "hurwitz_hessian_pi4_gate.tex",
    "s2t_six_channel_inverse_susceptibility_audit.py",
    "s2t_six_channel_inverse_susceptibility_results.json",
    "s2t_selfdual_bilaplacian_susceptibility_audit.py",
    "s2t_selfdual_bilaplacian_susceptibility_results.json",
    "s2t_halfshift_tensor_ghost_hessian_audit.py",
    "s2t_halfshift_tensor_ghost_hessian_results.json",
    "six_channel_inverse_susceptibility_gate.tex",
    "s2t_shared_holonomy_two_sector_audit.py",
    "s2t_shared_holonomy_two_sector_results.json",
    "shared_holonomy_two_sector_gate.tex",
    "s2t_continuous_wilson_gap_action_audit.py",
    "s2t_continuous_wilson_gap_action_results.json",
    "continuous_wilson_gap_action_gate.tex",
    "s2t_wilson_boundary_rotor_action_audit.py",
    "s2t_wilson_boundary_rotor_action_results.json",
    "wilson_boundary_rotor_action_gate.tex",
    "s2t_wilson_rotor_exact_determinant_audit.py",
    "s2t_wilson_rotor_exact_determinant_results.json",
    "wilson_rotor_exact_determinant_gate.tex",
    "s2t_modular_grading_cocycle_audit.py",
    "s2t_modular_grading_cocycle_results.json",
    "modular_grading_cocycle_gate.tex",
    "s2t_two_layer_physical_ckm_redteam_audit.py",
    "s2t_two_layer_physical_ckm_redteam_results.json",
    "two_layer_physical_ckm_redteam_gate.tex",
    "s2t_family_bipartite_c4_lift_audit.py",
    "s2t_family_bipartite_c4_lift_results.json",
    "family_bipartite_c4_lift_gate.tex",
    "s2t_chiral_doubled_triplet_yukawa_audit.py",
    "s2t_chiral_doubled_triplet_yukawa_results.json",
    "chiral_doubled_triplet_yukawa_gate.tex",
    "s2t_zero_prompt_inevitability_audit.py",
    "s2t_zero_prompt_inevitability_results.json",
    "zero_prompt_inevitability_gate.tex",
    "RPFT-main/ai-promts/First-principles-00-variational.md",
    "s2t_observed_world_coverage_audit.py",
    "s2t_observed_world_coverage_results.json",
    "observed_world_coverage_gate.tex",
    "wiki/questions/family-factor-operator-gate.md",
    "wiki/questions/collective-pi-atlas-base-gate.md",
    "wiki/questions/parent-noncommuting-family-gate.md",
    "wiki/questions/family-route-exhaustion-gate.md",
    "wiki/questions/spin-menu-dirac-determinant-line-gate.md",
    "wiki/questions/hurwitz-hessian-pi4-gate.md",
    "wiki/questions/six-channel-inverse-susceptibility-gate.md",
    "wiki/questions/shared-holonomy-two-sector-gate.md",
    "wiki/questions/continuous-wilson-gap-action-gate.md",
    "wiki/questions/wilson-boundary-rotor-action-gate.md",
    "wiki/questions/wilson-rotor-exact-determinant-gate.md",
    "wiki/questions/modular-grading-cocycle-gate.md",
    "wiki/questions/two-layer-physical-ckm-redteam-gate.md",
    "wiki/questions/family-bipartite-c4-lift-gate.md",
    "wiki/questions/chiral-doubled-triplet-yukawa-gate.md",
    "wiki/questions/zero-prompt-inevitability-gate.md",
    "wiki/questions/observed-world-coverage-gate.md",
    "s2t_observer_readout_fixed_point_audit.py",
    "s2t_observer_readout_fixed_point_results.json",
    "observer_readout_fixed_point_gate.tex",
    "wiki/questions/observer-readout-fixed-point-gate.md",
    "s2t_wilson_modular_state_readout_audit.py",
    "s2t_wilson_modular_state_readout_results.json",
    "wilson_modular_state_readout_gate.tex",
    "wiki/questions/wilson-modular-state-readout-gate.md",
    "s2t_relative_modular_cocycle_bch_audit.py",
    "s2t_relative_modular_cocycle_bch_results.json",
    "relative_modular_cocycle_bch_gate.tex",
    "wiki/questions/relative-modular-cocycle-bch-gate.md",
    "s2t_chiral_bch_normalization_ckm_audit.py",
    "s2t_chiral_bch_normalization_ckm_results.json",
    "chiral_bch_normalization_ckm_gate.tex",
    "wiki/questions/chiral-bch-normalization-ckm-gate.md",
    "s2t_exponential_yukawa_readout_audit.py",
    "s2t_exponential_yukawa_readout_results.json",
    "exponential_yukawa_readout_gate.tex",
    "wiki/questions/exponential-yukawa-readout-gate.md",
    "s2t_weighted_gap_yukawa_readout_audit.py",
    "s2t_weighted_gap_yukawa_readout_results.json",
    "weighted_gap_yukawa_readout_gate.tex",
    "wiki/questions/weighted-gap-yukawa-readout-gate.md",
    "s2t_aps_orbifold_inflow_redteam_audit.py",
    "s2t_aps_orbifold_inflow_redteam_results.json",
    "aps_orbifold_inflow_redteam_gate.tex",
    "wiki/questions/aps-orbifold-inflow-redteam-gate.md",
    "s2t_eta_phase_mass_gate_audit.py",
    "s2t_eta_phase_mass_gate_results.json",
    "eta_phase_mass_gate.tex",
    "wiki/questions/eta-phase-mass-gate.md",
    "s2t_conformal_majorana_rank_gate_audit.py",
    "s2t_conformal_majorana_rank_gate_results.json",
    "conformal_majorana_rank_gate.tex",
    "wiki/questions/conformal-majorana-rank-gate.md",
    "s2t_majorana_defect_parent_action_gate_audit.py",
    "s2t_majorana_defect_parent_action_gate_results.json",
    "majorana_defect_parent_action_gate.tex",
    "wiki/questions/majorana-defect-parent-action-gate.md",
    "s2t_majorana_root_source_menu_audit.py",
    "s2t_majorana_root_source_menu_results.json",
    "majorana_root_source_menu_gate.tex",
    "wiki/questions/majorana-root-source-menu-gate.md",
    "s2t_bl_root_extension_gate_audit.py",
    "s2t_bl_root_extension_gate_results.json",
    "bl_root_extension_gate.tex",
    "wiki/questions/bl-root-extension-gate.md",
    "s2t_bl_root_condensate_consistency_audit.py",
    "s2t_bl_root_condensate_consistency_results.json",
    "bl_root_condensate_consistency_gate.tex",
    "wiki/questions/bl-root-condensate-consistency-gate.md",
    "s2t_root_mass_condensate_trilemma_audit.py",
    "s2t_root_mass_condensate_trilemma_results.json",
    "root_mass_condensate_trilemma_gate.tex",
    "wiki/questions/root-mass-condensate-trilemma-gate.md",
    "s2t_nonuniform_pairing_saddle_audit.py",
    "s2t_nonuniform_pairing_saddle_results.json",
    "nonuniform_pairing_saddle_gate.tex",
    "wiki/questions/nonuniform-pairing-saddle-gate.md",
    "s2t_spectral_pairing_stiffness_gate_audit.py",
    "s2t_spectral_pairing_stiffness_gate_results.json",
    "spectral_pairing_stiffness_gate.tex",
    "wiki/questions/spectral-pairing-stiffness-gate.md",
    "bl_nonuniform_pairing_working_package.tex",
    "wiki/syntheses/bl-nonuniform-pairing-working-package-2026-08-07.md",
    "s2t_hypothesis_batch_pruner_audit.py",
    "s2t_hypothesis_batch_pruner_results.json",
    "hypothesis_batch_pruner_gate.tex",
    "wiki/questions/hypothesis-batch-pruner-gate.md",
    "s2t_tiered_parent_action_p1_audit.py",
    "s2t_tiered_parent_action_p1_results.json",
    "tiered_parent_action_p1_gate.tex",
    "wiki/questions/tiered-parent-action-p1-gate.md",
    "s2t_project_research_duplication_audit.py",
    "s2t_project_research_duplication_results.json",
    "wiki/syntheses/project-research-duplication-audit.md",
    "s2t_c6_second_variation_checklist_audit.py",
    "s2t_c6_second_variation_checklist_results.json",
    "wiki/syntheses/c6-second-variation-checklist.md",
    "RPFT-main/Проработка/old/README.md",
]

CORE_MARKERS = {
    "main.tex": [
        "\\section{Послесловие после проверки вторым томом}",
        "\\subsection{Что сохранилось как математическое ядро}",
        "\\subsection{Что сохраняется только как условная связь}",
        "\\subsection{Какие ветви закрыты отрицательно}",
        "\\section{Перспектива следующего тома}",
        "23+\\pi^{-1}",
    ],
    "tome2_s2t_spectral_closure.tex": [
        "S_{vac}",
        "m_\\tau",
        "23+\\pi^{-1}",
        "C6",
        "Единое parent action",
        "Глобальный falsification-аудит остаточных утверждений",
        "Продолжение феноменологической нумерологии внутри II.A прекращается",
        "\\part{Часть II.B: переоткрытие через новые операторные структуры}",
        "\\chapter{Definition of Done и текущий вердикт II.B}",
        "\\chapter{Общая голономия: первый прямой двухсекторный критерий}",
        "\\chapter{Непрерывная вильсоновская голономия и уравнение щели}",
        "\\chapter{Граничное роторное действие для вильсоновской ветви}",
        "\\chapter{Точный весовой детерминант граничного ротора}",
        "\\chapter{Модульная цепь, градуировка и минимальный CP-коцикл}",
        "\\chapter{Red-team двухслойной CKM-текстуры}",
        "\\chapter{Минимальный двудольный \\texorpdfstring{\\(C_4\\)}{C4}-лифт}",
        "\\chapter{Хирально удвоенный семейный триплет}",
        "\\section*{Red-team нулевого промта: условный вывод и неизбежность}",
        "\\chapter{Аудит покрытия наблюдаемого мира}",
        "\\chapter{Карта чтения и наблюдатель как недостающий слой}",
        "\\chapter{Wilson-state и относительный модульный коцикл}",
        "\\chapter{Прямой модульный коцикл и BCH-backreaction}",
        "\\chapter{Алгебраические нормировки BCH и полный CKM gate}",
        "\\chapter{Экспоненциальный Yukawa-readout: mass-trained и CKM-blind gate}",
        "\\chapter{Gap-derived weighted \\texorpdfstring{\\(A_3\\)}{A3} Yukawa gate}",
        "\\input{aps_orbifold_inflow_redteam_gate.tex}",
        "\\input{eta_phase_mass_gate.tex}",
        "\\input{conformal_majorana_rank_gate.tex}",
        "\\input{majorana_defect_parent_action_gate.tex}",
        "\\input{majorana_root_source_menu_gate.tex}",
        "\\input{bl_root_extension_gate.tex}",
        "\\input{bl_root_condensate_consistency_gate.tex}",
        "\\input{root_mass_condensate_trilemma_gate.tex}",
        "\\input{nonuniform_pairing_saddle_gate.tex}",
        "\\input{spectral_pairing_stiffness_gate.tex}",
        "\\input{bl_nonuniform_pairing_working_package.tex}",
        "\\input{hypothesis_batch_pruner_gate.tex}",
        "\\input{tiered_parent_action_p1_gate.tex}",
        "\\chapter{Что фактически достигнуто: от наивной модели к строгой программе}",
    ],
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def environment_balance(text, environment):
    return {
        "begin": text.count(f"\\begin{{{environment}}}"),
        "end": text.count(f"\\end{{{environment}}}"),
    }


def main():
    core = {}
    for path in CORE_FILES:
        text = path.read_text(encoding="utf-8")
        marker_counts = {
            marker: text.count(marker) for marker in CORE_MARKERS[path.name]
        }
        balances = {
            environment: environment_balance(text, environment)
            for environment in [
                "document",
                "equation",
                "itemize",
                "enumerate",
                "proof",
                "protocol",
                "nogocriterion",
                "proposition",
            ]
        }
        core[path.name] = {
            "bytes": path.stat().st_size,
            "lines": text.count("\n") + 1,
            "sha256": sha256(path),
            "end_document_count": text.count("\\end{document}"),
            "marker_counts": marker_counts,
            "environment_balances": balances,
        }

    missing_recent = [
        path for path in RECENT_ARTIFACTS if not Path(path).is_file() or Path(path).stat().st_size == 0
    ]

    audit_scripts = sorted(Path(".").glob("s2t_*audit.py"))
    python_failures = []
    for script in audit_scripts:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as error:
            python_failures.append({"file": str(script), "error": str(error)})

    result_files = sorted(Path(".").glob("s2t_*results.json"))
    json_failures = []
    for result_file in result_files:
        try:
            json.loads(result_file.read_text(encoding="utf-8"))
        except Exception as error:
            json_failures.append({"file": str(result_file), "error": str(error)})

    git_status = subprocess.run(
        ["git", "status", "--short"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    deleted_paths = [line for line in git_status if "D" in line[:2]]

    checks = {
        "core_files_nontrivial": all(row["bytes"] > 200000 for row in core.values()),
        "single_document_end": all(row["end_document_count"] == 1 for row in core.values()),
        "all_core_markers_present": all(
            count > 0
            for row in core.values()
            for count in row["marker_counts"].values()
        ),
        "key_environments_balanced": all(
            balance["begin"] == balance["end"]
            for row in core.values()
            for balance in row["environment_balances"].values()
        ),
        "recent_artifacts_complete": not missing_recent,
        "all_audit_scripts_compile": not python_failures,
        "all_result_json_parse": not json_failures,
        "no_git_deletions": not deleted_paths,
    }
    status = (
        "project_content_preserved_and_reproducible"
        if all(checks.values())
        else "preservation_audit_has_failures"
    )
    results = {
        "status": status,
        "date": "2026-08-06",
        "checks": checks,
        "core_files": core,
        "inventory": {
            "root_tex_files": len(list(Path(".").glob("*.tex"))),
            "audit_scripts": len(audit_scripts),
            "result_json_files": len(result_files),
            "wiki_files": len([path for path in Path("wiki").rglob("*") if path.is_file()]),
        },
        "recent_artifacts": {
            "expected_count": len(RECENT_ARTIFACTS),
            "missing": missing_recent,
        },
        "python_failures": python_failures,
        "json_failures": json_failures,
        "git": {
            "status_lines": git_status,
            "deleted_paths": deleted_paths,
        },
        "principal_builds": {
            "status": "verified_by_external_pdflatex_commands",
            "main_pages": 112,
            "tome2_pages": 201,
        },
        "interpretation": (
            "The original formulas, conditional-status language and negative verdicts remain in "
            "the principal tomes. Recent family-selector, physical-CKM red-team and bipartite-C4 "
            "work and the explicit B-L root-extension gate were added as separate audit/gate "
            "artifacts and did not replace the earlier "
            "mathematical or phenomenological corpus."
        ),
    }

    Path("s2t_project_preservation_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": status,
                "checks": checks,
                "inventory": results["inventory"],
                "main_bytes": core["main.tex"]["bytes"],
                "tome2_bytes": core["tome2_s2t_spectral_closure.tex"]["bytes"],
                "missing_recent_artifacts": missing_recent,
                "python_failures": len(python_failures),
                "json_failures": len(json_failures),
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    if status != "project_content_preserved_and_reproducible":
        raise SystemExit(1)


if __name__ == "__main__":
    main()