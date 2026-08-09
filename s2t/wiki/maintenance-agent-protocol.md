# Maintenance Agent Protocol

> Status: working
> Type: maintenance
> Updated: 2026-07-09

## Summary

This page records how the assistant should explain work inside the project wiki and repository. The goal is to make every non-trivial action understandable to a department manager: what problem was handled, how a solution was searched, what result was expected, and how compliance was checked.

## Reporting Scheme

Use this four-part structure for task reports and stage summaries:

1. Problem — what issue, gap, or request is being addressed.
2. Search for solution — what files, sources, audits, or alternatives were inspected and what was changed.
3. Expected result — what should be true after the change if the solution is correct.
4. Compliance check — how the result was validated against the expectation.

## Operational Rules

- Keep reports simple, concrete, and manager-friendly.
- Mention changed files and git commits when work is written to the repository.
- Mention validation steps such as wiki-link checks, metadata checks, tests, build commands, or source comparisons.
- Separate completed results from remaining risks or open research gaps.
- Do not present partial success as full closure.
- For wiki maintenance, append a `wiki/log.md` entry when a change is reusable or structural.

## Example Report Shape

- Problem: the wiki listed audit files but did not explain what they proved.
- Search for solution: extracted top-level metrics from JSON result files and compared them with the S2T roadmap.
- Expected result: readers can see which claims are numerically supported and which remain open.
- Compliance check: verified all `double-bracket` wiki links and committed the updated pages.

## Links

- [[project-overview]] — global research map that benefits from clear reporting.
- [[s2t-closure-roadmap]] — example of separating closure status from open gaps.
- [[numerical-audits]] — example of evidence reporting with metrics and limitations.

## Source Notes

- Source path: `AGENTS.md`.
- Related instruction source: `llm-wiki.md`.