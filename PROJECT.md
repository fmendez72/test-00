# test-00

## Stack
- **Python 3.12** — data generation (`pandas`, `numpy`, `matplotlib`, `seaborn`)
- **R 4.4** — data generation (`tidyverse`, `ggplot2`, `patchwork`)
- **Quarto 1.6** — reports rendered to self-contained HTML
- **venv** at `.venv/` for Python dependencies

## Status
Template / Reference — completed scaffold, not under active development

## Description
A template data science project demonstrating the standard workspace scaffold.
Generates a synthetic VAA (Voting Advice Application) dataset — 500 respondents,
10 policy issues, 6 parties — using a proximity voting model. Produces exploratory
reports in both Python and R via Quarto. Serves as a reference implementation for
future projects.

## Key Files
- `src/generate_data.py` — generates `data/vaa_respondents.csv` + `data/vaa_party_positions.csv`
- `src/generate_data.R` — same output via R/tidyverse
- `notebooks/report_python.qmd` — Quarto report, Python kernel
- `notebooks/report_r.qmd` — Quarto report, R kernel
- `reports/` — rendered HTML outputs (gitignored)

## Active Goals
- [x] Python data generator
- [x] R data generator
- [x] Quarto report (Python)
- [x] Quarto report (R)
- [ ] Parameterise N_RESPONDENTS, N_PARTIES via CLI args (future)
- [ ] Add a `_quarto.yml` project file to render both reports in one command (future)
