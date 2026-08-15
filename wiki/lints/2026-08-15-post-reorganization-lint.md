# Post-Reorganization Consistency Lint — 2026-08-15

> Status: mature
> Type: lint
> Updated: 2026-08-15

## Problem

Recheck the repository after restoring the split `docs/`, `gates/`, `assets/`
and reproduction-package paths, including a clean LaTeX build and wiki schema
compliance.

## Search for Solution

- rebuilt Tomes I--IV and the TOE--UGSM integration paper from a clean state;
- checked every audit with Python AST parsing and every result JSON with a JSON parser;
- verified every path and SHA-256 entry in `s2t/reproduction_package/FREEZE_MANIFEST.json`;
- audited all wiki content pages for `Status`, `Type` and `Updated` metadata;
- checked index coverage, duplicate page identifiers and Obsidian targets;
- compared README counters with the filesystem.

## Result

- five primary PDFs build without fatal errors or undefined references;
- 336/336 audit files parse and 358/358 result files are valid JSON;
- 8/8 manifest files exist and match their recorded hashes;
- 121 pages required metadata normalization; all 267 pre-existing content pages now comply with the schema without losing descriptive research statuses;
- three matrix expressions that looked like Obsidian links were rewritten unambiguously;
- every wiki content page is indexed and page identifiers are unique.

## Compliance Check

Final automated state after adding this lint page:

- metadata violations: `0`;
- broken Obsidian targets: `0`;
- broken local Markdown links and images: `0`;
- pages missing from `wiki/index.md`: `0`;
- duplicate wiki identifiers: `0`;
- `git diff --check`: pass.

Historical gate/audit/result naming exceptions were not renamed because those
filenames are immutable source identifiers. They remain outside the scope of
the build repair.

## Connectivity Note

All pages are reachable through `wiki/index.md`, but 133 content pages have no
incoming Obsidian link from another content page. This is navigation debt, not
link breakage: identifiers resolve uniquely and the pages remain catalogued.
Future synthesis work should add meaningful cross-links instead of creating
links mechanically.