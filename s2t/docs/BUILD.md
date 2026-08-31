# LaTeX Build

> Status: working
> Type: build
> Updated: 2026-08-29

The Prism workspace preserves Markdown and TeX sources but may discard ignored
helper files such as an untracked root `Makefile`. Build the documents directly
from the repository root with `latexmk -cd`; `s2t_paths.tex` supplies the
`s2t/gates/` lookup path and the document preambles supply `s2t/assets/`.

## Build all primary documents

```bash
for doc in \
  tome1_s2t_research_program \
  tome2_s2t_spectral_closure \
  tome3_s2t_parent_action \
  tome4_s2t_observed_reconstruction \
  tome5_s2t_parent_architecture \
  tome6_s2t_matter_birth \
  tome7_s2t_rank_change_parent \
  tome8_s2t_correlation_transition \
  toe_ugsm_unified_shadow_paper
do
  latexmk -cd -pdf -interaction=nonstopmode -halt-on-error "s2t/docs/${doc}.tex"
done
```

## Clean generated files

```bash
for doc in \
  tome1_s2t_research_program \
  tome2_s2t_spectral_closure \
  tome3_s2t_parent_action \
  tome4_s2t_observed_reconstruction \
  tome5_s2t_parent_architecture \
  tome6_s2t_matter_birth \
  tome7_s2t_rank_change_parent \
  tome8_s2t_correlation_transition \
  toe_ugsm_unified_shadow_paper
do
  latexmk -cd -C "s2t/docs/${doc}.tex"
done
```

Generated PDFs and auxiliary files are intentionally not part of the source
inventory. The canonical build inputs are the TeX/Markdown files under
`s2t/docs/`, gates under `s2t/gates/`, and figures under `s2t/assets/`.