# LLM Wiki Schema

This project uses the **LLM Wiki** pattern from `llm-wiki.md`: raw research materials remain immutable sources, while the assistant maintains a persistent, interlinked markdown wiki that compounds knowledge across sessions.

## Directory Roles

- `raw/` — future immutable source drops. Do not rewrite source files here; add new files or assets only.
- `raw/assets/` — local images, figures, PDFs, and extracted attachments for sources.
- `wiki/` — LLM-maintained knowledge base. The assistant may create, revise, cross-link, and reorganize pages here.
- `wiki/index.md` — content-oriented navigation catalog; read this first when answering research questions.
- `wiki/log.md` — append-only chronological record of ingests, queries, lint passes, and structural changes.
- `wiki/sources/` — one page per important source document or source cluster.
- `wiki/concepts/` — entity, concept, method, and hypothesis pages.
- `wiki/syntheses/` — higher-level summaries, bridges, comparisons, and evolving theses.
- `wiki/questions/` — filed answers, open problems, and research prompts worth preserving.
- `wiki/lints/` — periodic wiki health checks.

Existing project files such as `*.tex`, `*.json`, `s2t/docs/RESEARCH_CATALOG.md`, and `RPFT-main/` are treated as current source material unless explicitly moved by the user.

## Naming Conventions

Use lowercase kebab-case for wiki filenames:

- `wiki/concepts/spectral-correlational-source.md`
- `wiki/sources/toe-ugsm-unified-shadow-paper.md`
- `wiki/syntheses/project-overview.md`

Prefer stable names over fashionable labels. If a concept is renamed, leave a short redirect note in the old page or update inbound links in the same edit.

## Page Format

Each wiki page should normally include:

```markdown
# Page Title

> Status: draft | working | mature | stale
> Type: source | concept | synthesis | question | lint
> Updated: YYYY-MM-DD

## Summary

Short, direct summary.

## Key Points

- Main claims or facts.

## Links

- [[related-page]] — why it matters.

## Source Notes

- Source paths or evidence used.
```

For Obsidian compatibility, use double-bracket Obsidian links (no `.md` suffix, no directory path), for example:

```text
[[related-page]] -- why it matters
```

Include source file paths in backticks.

## Ingest Workflow

When the user asks to ingest a source:

1. Read `wiki/index.md` and the relevant existing pages.
2. Read the new source without modifying it.
3. Create or update a source page in `wiki/sources/`.
4. Update any affected concept pages in `wiki/concepts/`.
5. If the source changes the global picture, update `wiki/syntheses/project-overview.md` or another synthesis page.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md` using the log format below.

A source can update many wiki pages. Preserve contradictions rather than smoothing them over.

## Query Workflow

When answering research questions:

1. Start from `wiki/index.md`.
2. Read the most relevant wiki pages.
3. Search source files only when the wiki is insufficient or precision is required.
4. Answer with concrete references to wiki pages and source files.
5. If the answer is reusable, ask whether to file it under `wiki/questions/` or create it directly when the user requested wiki maintenance.

## Lint Workflow

Periodically inspect the wiki for:

- orphan pages with no meaningful links;
- concepts mentioned repeatedly but lacking pages;
- stale claims superseded by later sources;
- contradictions between pages;
- missing source attribution;
- unclear status labels;
- research questions that should be promoted to tracked pages.

Save lint results in `wiki/lints/YYYY-MM-DD-lint.md` and append the action to `wiki/log.md`.

## Log Format

Use append-only entries:

```markdown
## [YYYY-MM-DD] action | Short Title

- Files touched: `path`, `path`
- Summary: what changed and why.
- Follow-ups: optional next steps.
```

Recommended actions: `setup`, `ingest`, `query`, `synthesis`, `lint`, `maintenance`.

## Current Research Domain

The current workspace appears to study an RPFT/UGSM/TOE cluster centered on geometry, topology, spectral action, holonomy, operator attribution, and a possible unified spectral-correlational source. Treat this as the initial domain model until the user revises it.