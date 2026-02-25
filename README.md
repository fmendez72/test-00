# test-00

Template data science project. Generates a synthetic VAA (Voting Advice Application)
dataset and produces exploratory reports in both Python and R via Quarto.

## Setup

**Python**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib seaborn jupyter ipykernel
python -m ipykernel install --user --name test-00 --display-name "Python (test-00)"
```

**R** — requires `tidyverse` and `patchwork` (installed system-wide or via `renv`).

## Usage

**Generate data**
```bash
# Python
python src/generate_data.py

# R
Rscript src/generate_data.R
```

Both write to `data/vaa_respondents.csv` and `data/vaa_party_positions.csv`.

**Render reports**
```bash
quarto render notebooks/report_python.qmd --output-dir reports
quarto render notebooks/report_r.qmd --output-dir reports
```

Outputs: `reports/report_python.html`, `reports/report_r.html`

## Structure

```
test-00/
├── src/
│   ├── generate_data.py   # Synthetic VAA data generator (Python)
│   └── generate_data.R    # Synthetic VAA data generator (R)
├── data/                  # Generated CSVs (gitignored)
├── notebooks/
│   ├── report_python.qmd  # Quarto report — Python kernel
│   └── report_r.qmd       # Quarto report — R kernel
├── reports/               # Rendered HTML (gitignored)
├── PROJECT.md             # Canonical project context
└── CLAUDE.md              # Claude Code adapter
```

## Dataset

| File | Rows | Description |
|---|---|---|
| `vaa_respondents.csv` | 500 | Respondent positions (−2 to +2) on 10 issues + demographics + vote choice |
| `vaa_party_positions.csv` | 60 | Tidy table of 6 parties × 10 issues |

Vote choice is assigned via minimum Manhattan distance (proximity voting) with small random noise to break ties.
