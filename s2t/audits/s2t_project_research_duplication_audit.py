#!/usr/bin/env python3
import hashlib
import io
import json
import math
import re
import tokenize
from collections import Counter, defaultdict
from pathlib import Path

from scipy.sparse import csr_matrix


TEXT_EXTENSIONS = {".tex", ".md", ".py", ".json", ".txt"}
PROSE_EXTENSIONS = {".tex", ".md"}
STOPWORDS = set(
    "и в во не что он на я с со как а то все она так его но да ты к у же "
    "вы за бы по только было от из ему когда если уже или ни быть был до "
    "там потом себя ничего может они тут где есть для мы их чем была сам "
    "без чего раз тоже под будет кто этот того потому этого какой совсем "
    "здесь этом один почти тем чтобы сейчас были можно при другой после "
    "над больше через эти нас про всего них the and of to in a is for with "
    "on as are be this that from or by an it not at can if then into one "
    "two has have which all only no its their".split()
)


def corpus(extensions):
    return sorted(
        path
        for path in Path(".").rglob("*")
        if path.is_file()
        and path.suffix.lower() in extensions
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
    )


def words(text):
    text = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[^0-9A-Za-zА-Яа-яЁё_+-]+", " ", text.lower())
    return [
        token
        for token in text.split()
        if len(token) >= 3
        and token not in STOPWORDS
        and not token.isdigit()
    ]


def duplicate_groups(paths, payload):
    groups = defaultdict(list)
    for path in paths:
        groups[hashlib.sha256(payload(path)).hexdigest()].append(str(path))
    return sorted(
        [group for group in groups.values() if len(group) > 1],
        key=lambda group: (-len(group), group),
    )


def extract_sections(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    pattern = (
        re.compile(
            r"(?m)^\\(chapter|section|subsection|subsubsection)\*?\{([^}]*)\}"
        )
        if path.suffix.lower() == ".tex"
        else re.compile(r"(?m)^(#{1,4})\s+(.+)$")
    )
    matches = list(pattern.finditer(text))
    rows = []
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        rows.append(
            {
                "path": str(path),
                "line": text.count("\n", 0, match.start()) + 1,
                "title": match.group(2).strip(),
                "body": text[match.end() : stop],
            }
        )
    return rows


def tfidf(texts):
    feature_rows = []
    document_frequency = Counter()
    for text in texts:
        tokens = words(text)
        features = tokens + [
            tokens[index] + "::" + tokens[index + 1]
            for index in range(len(tokens) - 1)
        ]
        feature_rows.append(features)
        document_frequency.update(set(features))
    count = len(texts)
    kept = [
        feature
        for feature, frequency in document_frequency.items()
        if 2 <= frequency <= max(2, int(0.30 * count))
    ]
    vocabulary = {feature: index for index, feature in enumerate(kept)}
    rows = []
    columns = []
    values = []
    for row_index, features in enumerate(feature_rows):
        counts = Counter(feature for feature in features if feature in vocabulary)
        weighted = []
        norm_squared = 0.0
        for feature, frequency in counts.items():
            value = (1.0 + math.log(frequency)) * math.log(
                (count + 1.0) / (document_frequency[feature] + 1.0)
            )
            weighted.append((vocabulary[feature], value))
            norm_squared += value * value
        norm = math.sqrt(norm_squared) or 1.0
        for column, value in weighted:
            rows.append(row_index)
            columns.append(column)
            values.append(value / norm)
    return csr_matrix(
        (values, (rows, columns)),
        shape=(count, len(vocabulary)),
    )


def near_file_pairs(paths):
    labels = []
    texts = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if len(words(text)) >= 100:
            labels.append(str(path))
            texts.append(text)
    matrix = tfidf(texts)
    product = (matrix @ matrix.T).tocoo()
    pairs = []
    for first, second, similarity in zip(product.row, product.col, product.data):
        if first < second and similarity >= 0.55:
            pairs.append(
                {
                    "similarity": float(similarity),
                    "first": labels[first],
                    "second": labels[second],
                }
            )
    return sorted(pairs, key=lambda row: -row["similarity"])


def python_structure(path):
    sequence = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type in {
                tokenize.COMMENT,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.ENCODING,
                tokenize.ENDMARKER,
                tokenize.INDENT,
                tokenize.DEDENT,
            }:
                continue
            if token.type == tokenize.NUMBER:
                sequence.append("<NUMBER>")
            elif token.type == tokenize.STRING:
                sequence.append("<STRING>")
            else:
                sequence.append(token.string)
    except (tokenize.TokenError, IndentationError):
        return b""
    return " ".join(sequence).encode("utf-8")


def near_python_pairs(paths):
    labels = []
    texts = []
    for path in paths:
        text = python_structure(path).decode("utf-8", errors="ignore")
        if len(text.split()) >= 30:
            labels.append(str(path))
            texts.append(text)
    matrix = tfidf(texts)
    product = (matrix @ matrix.T).tocoo()
    pairs = []
    for first, second, similarity in zip(product.row, product.col, product.data):
        if first < second and similarity >= 0.75:
            pairs.append(
                {
                    "similarity": float(similarity),
                    "first": labels[first],
                    "second": labels[second],
                }
            )
    return sorted(pairs, key=lambda row: -row["similarity"])


def c6_fragmentation():
    rows = []
    for path in sorted(Path(".").glob("s2t_c6_*_results.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        status = str(data.get("status", ""))
        text = json.dumps(data, ensure_ascii=False).lower()
        open_formula = (
            ("formula" in status or "skeleton" in status)
            and any(marker in text for marker in ["not_yet", "missing", "open"])
        )
        rows.append((str(path), status, open_formula))
    return {
        "result_files": len(rows),
        "open_formula_skeletons": sum(row[2] for row in rows),
        "open_files": [row[0] for row in rows if row[2]],
    }


def main():
    text_files = corpus(TEXT_EXTENSIONS)
    prose_files = corpus(PROSE_EXTENSIONS)
    python_files = corpus({".py"})
    exact_files = duplicate_groups(text_files, lambda path: path.read_bytes())
    python_clones = duplicate_groups(python_files, python_structure)
    python_near_pairs = near_python_pairs(python_files)

    section_map = defaultdict(list)
    section_count = 0
    for path in prose_files:
        for row in extract_sections(path):
            tokens = words(row["body"])
            if len(tokens) < 70:
                continue
            section_count += 1
            digest = hashlib.sha256(" ".join(tokens).encode("utf-8")).hexdigest()
            section_map[digest].append(
                {
                    "path": row["path"],
                    "line": row["line"],
                    "title": row["title"],
                }
            )
    exact_sections = sorted(
        [group for group in section_map.values() if len(group) > 1],
        key=lambda group: (-len(group), group[0]["path"]),
    )

    archival_exact = [
        group for group in exact_files if any("/old/" in path for path in group)
    ]
    wiki_exact = [
        group
        for group in exact_sections
        if all(row["path"].startswith("wiki/") for row in group)
    ]
    bilingual_clones = [
        group
        for group in python_clones
        if any("RPFT-main/rigorous-en/" in path for path in group)
        and any("RPFT-main/rigorous/" in path for path in group)
    ]
    c6_clones = [
        group
        for group in python_clones
        if all(Path(path).name.startswith("s2t_c6_") for path in group)
    ]
    c6_near_pairs = [
        pair
        for pair in python_near_pairs
        if Path(pair["first"]).name.startswith("s2t_c6_")
        and Path(pair["second"]).name.startswith("s2t_c6_")
    ]
    bilingual_near_pairs = [
        pair
        for pair in python_near_pairs
        if (
            "RPFT-main/rigorous-en/" in pair["first"]
            and "RPFT-main/rigorous/" in pair["second"]
        )
        or (
            "RPFT-main/rigorous/" in pair["first"]
            and "RPFT-main/rigorous-en/" in pair["second"]
        )
    ]
    c6 = c6_fragmentation()
    checklist_path = Path("s2t_c6_second_variation_checklist_results.json")
    checklist = (
        json.loads(checklist_path.read_text(encoding="utf-8"))
        if checklist_path.is_file()
        else None
    )
    c6_reporting_consolidated = bool(
        checklist
        and checklist.get("summary", {}).get("registered_subblocks") == 16
        and checklist.get("summary", {}).get("independent_research_results") == 1
    )

    results = {
        "status": "exact_wiki_duplicates_removed_and_c6_reporting_consolidated",
        "date": "2026-08-06",
        "inventory": {
            "text_and_machine_files": len(text_files),
            "prose_files": len(prose_files),
            "python_files": len(python_files),
            "sections_compared": section_count,
        },
        "exact_file_duplicates": exact_files,
        "exact_section_duplicates": exact_sections,
        "near_file_pairs": near_file_pairs(prose_files)[:40],
        "normalized_python_clone_groups": python_clones,
        "near_python_structure_pairs": python_near_pairs[:80],
        "summary_counts": {
            "exact_file_groups": len(exact_files),
            "archival_exact_groups": len(archival_exact),
            "exact_wiki_section_groups": len(wiki_exact),
            "python_clone_groups": len(python_clones),
            "c6_python_clone_groups": len(c6_clones),
            "bilingual_python_clone_groups": len(bilingual_clones),
            "near_python_structure_pairs": len(python_near_pairs),
            "near_c6_structure_pairs": len(c6_near_pairs),
            "near_bilingual_structure_pairs": len(bilingual_near_pairs),
        },
        "c6_fragmentation": c6,
        "classification": {
            "harmful_or_risky": [
                "Five byte-identical active/archive pairs inflate source counts.",
            ],
            "intentional_and_useful": [
                "Russian and English rigorous scripts are language mirrors.",
                "The B-L, CKM and C6 chains are progressive falsification sequences.",
                "Short theorem summaries in the tomes are legitimate traceability layers.",
            ],
            "cleanup_applied": [
                "The intermediate B-L condensate-holonomy result is now explicitly marked as superseded by the later trilemma.",
                "Seven groups of verbatim C6 wiki sections were replaced by links to one canonical chronology.",
                "Sixteen C6 formula skeletons are now reported through one C6-DELTA2 checklist and count as one research task.",
            ],
        },
        "recommendations": [
            "Exclude old archives and language mirrors from independent-result counts.",
            "Add claim_id, depends_on, supersedes and independent_control to future JSON results.",
            "Use one computation, one canonical JSON and one canonical wiki page.",
        ],
        "overall_verdict": {
            "independent_physical_result_duplication": "low",
            "documentation_duplication": (
                "exact_C6_wiki_duplicates_removed"
                if len(wiki_exact) == 0
                else "remaining_exact_wiki_duplicates"
            ),
            "computational_overfragmentation": (
                "historical_subfiles_retained_but_reporting_consolidated"
                if c6_reporting_consolidated
                else "formula_only_C6_subblocks_not_consolidated"
            ),
            "scientific_interpretation": (
                "The project mostly revisits questions with stricter controls rather than "
                "rediscovering the same physical result. The main duplication is bookkeeping."
            ),
        },
    }

    assert len(exact_files) == 5
    assert len(archival_exact) == 5
    assert c6["result_files"] >= 70
    assert c6["open_formula_skeletons"] >= 10
    assert len(wiki_exact) == 0
    assert c6_reporting_consolidated is True

    Path("s2t_project_research_duplication_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "inventory": results["inventory"],
                "summary_counts": results["summary_counts"],
                "c6_result_files": c6["result_files"],
                "c6_open_formula_skeletons": c6["open_formula_skeletons"],
                "overall_verdict": results["overall_verdict"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()