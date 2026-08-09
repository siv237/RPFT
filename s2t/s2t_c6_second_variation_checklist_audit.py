#!/usr/bin/env python3
import json
from pathlib import Path


SUBBLOCKS = [
    ("A0", "исходная схема операторного следа", "s2t_c6_operator_trace_skeleton_results.json"),
    ("A1", "первая вариация связности", "s2t_c6_l21_connection_variation_formula_results.json"),
    ("A2", "первая вариация кривизны Риччи", "s2t_c6_l21_ricci_variation_formula_results.json"),
    ("A3", "первая вариация проектора на ко-точные формы", "s2t_c6_l21_projector_variation_formula_results.json"),
    ("A4", "первая вариация гильбертовой метрики", "s2t_c6_l21_hilbert_variation_formula_results.json"),
    ("B0", "выбор пути второй вариации метрики", "s2t_c6_l21_delta2_ambient_path_formula_results.json"),
    ("B1", "сводная схема второй вариации", "s2t_c6_l21_delta2_skeleton_completion_results.json"),
    ("B2", "главный символ второго порядка", "s2t_c6_l21_delta2_principal_second_symbol_formula_results.json"),
    ("B3", "вторая вариация связности", "s2t_c6_l21_delta2_second_connection_formula_results.json"),
    ("B4", "вторая вариация кривизны Риччи", "s2t_c6_l21_delta2_second_ricci_formula_results.json"),
    ("B5", "вторая вариация проектора", "s2t_c6_l21_delta2_second_projector_formula_results.json"),
    ("B6", "вторая вариация гильбертовой метрики", "s2t_c6_l21_delta2_second_hilbert_formula_results.json"),
    ("C1", "разложение смешанной вариации связности", "s2t_c6_l21_delta2_gamma_expansion_formula_results.json"),
    ("C2", "смешанный член метрики и связности", "s2t_c6_l21_delta2_connection_metric_cross_ambient_formula_results.json"),
    ("C3", "произведение первых вариаций связности", "s2t_c6_l21_delta2_connection_product_gamma_inserted_results.json"),
    ("D1", "классификация локальных контрчленов", "s2t_c6_l21_delta2_local_counterterm_classifier_results.json"),
]


def true_matrix_evaluation(value, key=""):
    if isinstance(value, dict):
        return any(
            true_matrix_evaluation(child, child_key)
            for child_key, child in value.items()
        )
    if isinstance(value, list):
        return any(true_matrix_evaluation(child, key) for child in value)
    return (
        isinstance(value, bool)
        and value
        and "matrix" in key.lower()
        and ("evaluat" in key.lower() or "comput" in key.lower())
    )


def main():
    rows = []
    for identifier, name, filename in SUBBLOCKS:
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        rows.append(
            {
                "id": identifier,
                "name_ru": name,
                "source": filename,
                "source_status": data.get("status", ""),
                "formula_registered": True,
                "matrix_evaluation_complete": true_matrix_evaluation(data),
                "canonical_status": "формула зафиксирована; матричное вычисление открыто",
            }
        )

    results = {
        "claim_id": "C6-DELTA2",
        "status": "single_second_variation_calculation_decomposed_into_sixteen_open_subblocks",
        "date": "2026-08-06",
        "canonical_question": (
            "Вычислить полную вторую вариацию калибровочно фиксированного "
            "определителя Максвелла--Фаддеева--Попова на L(2,1) x S1."
        ),
        "subblocks": rows,
        "summary": {
            "registered_subblocks": len(rows),
            "formula_level_complete": sum(row["formula_registered"] for row in rows),
            "matrix_level_complete": sum(
                row["matrix_evaluation_complete"] for row in rows
            ),
            "independent_research_results": 1,
        },
        "reporting_rule": (
            "Подблоки A0--D1 являются строками одного вычисления и не должны "
            "учитываться как независимые физические результаты."
        ),
        "closure_condition": (
            "Для закрытия C6 требуется единая самосопряжённая матрица второй "
            "вариации, её след на проекции P02, полный вклад духов и доказанная "
            "классификация локальных и конечных частей."
        ),
    }

    assert results["summary"]["registered_subblocks"] == 16
    assert results["summary"]["matrix_level_complete"] == 0
    assert results["summary"]["independent_research_results"] == 1

    Path("s2t_c6_second_variation_checklist_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()