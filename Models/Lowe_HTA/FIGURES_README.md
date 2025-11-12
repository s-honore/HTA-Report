# Figures for Publication

This directory contains scripts and data for generating publication-ready figures referenced in Section 3 of the HTA report.

## Figure 1: Cost-Effectiveness Plane

**Script:** `generate_figure1_ce_plane.py`
**Data:** `ce_plane_data.csv`
**Output:** `figure1_ce_plane.png` (PNG, 300 DPI) and `figure1_ce_plane.pdf` (PDF, vector)

### Requirements
```bash
pip install matplotlib pandas numpy
```

### Generate Figure
```bash
cd /home/user/HTA-Report/Models/Lowe_HTA
python generate_figure1_ce_plane.py
```

### Description
Cost-effectiveness plane plotting incremental costs (€ millions) against incremental QALYs for three gene therapy scenarios compared to natural history. Includes willingness-to-pay threshold lines at €100K, €150K, and €300K per QALY.

## Data Files

- `ce_plane_data.csv`: Incremental costs, QALYs, and ICERs for scenarios 1-3
- `scenario_results.csv`: Complete model results for all scenarios
- `sensitivity_analysis.csv`: One-way deterministic sensitivity analysis results
- `tornado_diagram_data.csv`: Data formatted for tornado diagram plotting

## Notes

- All figures use 1.5% base case discount rate unless otherwise specified
- Costs in 2024 EUR
- Publication-quality resolution (300 DPI minimum for PNG, vector for PDF)
- Color-blind friendly color palettes used
