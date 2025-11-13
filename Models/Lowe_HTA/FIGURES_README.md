# HTA Report Figures - Generation Guide

## Overview

Comprehensive figure generation system for the Lowe Syndrome Gene Therapy HTA Report with consistent Cure Lowe Foundation branding.

---

## Quick Start

### Run Everything at Once:
```bash
python run_model_and_generate_figures.py
```

This will:
1. ✓ Run the complete Markov model
2. ✓ Perform all sensitivity analyses
3. ✓ Generate all 8 publication-quality figures

Output: `./outputs/figures/`

---

## Brand Styling

### Color Scheme (Cure Lowe Foundation)

| Color | Hex Code | Usage |
|-------|----------|-------|
| **Ultramarine Blue** | #2F6CD6 | Primary brand color, trust, key elements |
| **Ivory** | #F1ECE2 | Clean backgrounds, calm surfaces |
| **Lime** | #D9FBC8 | Energy, innovation, highlights (sparingly) |
| **Orange Shake** | #F3A87B | Warmth, emphasis, calls to action |
| **Payne's Gray** | #262626 | Body text, neutrals, grounding |

### Styling Specifications

- **Font Size**: 14pt (body), 16pt (titles), 12pt (legends)
- **Spines**: No top spine, visible left/bottom/right (where needed)
- **Grid Lines**: Horizontal only, dashed, 30% opacity
- **Legend**: Bottom center, no frame, 3-4 columns
- **Background**: Transparent
- **Resolution**: 300 DPI
- **Format**: PNG

### Dual Y-Axis Convention

When using dual y-axes:
- **Left axis**: Primary metric (black/Payne's Gray)
- **Right axis**: Secondary metric (Lime for reference)
- Both metrics use consistent color coding throughout figure

---

## Figure Catalog

### Figure 1: Treatment Scenario Comparison (4-panel)
**File**: `figure1_scenario_comparison.png`

**Purpose**: Compare health outcomes and cost-effectiveness across all treatment scenarios

**Panels**:
- **A**: Incremental QALYs (Ultramarine Blue bars)
- **B**: evLYG (Orange Shake bars)
- **C**: Incremental Costs in millions (Lime bars)
- **D**: ICER per QALY (Gray bars with threshold lines)

**Key Elements**:
- Bar charts with value labels
- Threshold lines at €100K and €300K (Panel D)
- Clear scenario labels with line breaks

**Use In Report**: Section 3 (Results), Cost-Effectiveness Analysis

---

### Figure 2: eGFR Trajectories
**File**: `figure2_egfr_trajectories.png`

**Purpose**: Show kidney function decline over time by scenario

**Features**:
- Multiple curves: Natural History (dashed), Treatment scenarios (solid)
- CKD stage thresholds (90, 60, 45, 30, 15 ml/min/1.73m²)
- Stage labels (CKD 2, 3a, 3b, 4, 5/ESKD)
- X-axis: Years since treatment (0-50)
- Y-axis: eGFR (0-100)

**Interpretation**: Lower curves = faster decline. Treatment scenarios should show slower decline than natural history.

**Use In Report**: Section 3 (Results), Clinical Outcomes

---

### Figure 3a/3b: Population Health States Over Time
**Files**:
- `figure3a_population_natural_history.png`
- `figure3b_population_optimistic.png`

**Purpose**: Visualize disease progression through CKD stages and death

**Features**:
- Stacked area chart (100% = whole cohort)
- Color gradient: Lime (CKD2, best) → Dark Red (ESKD) → Gray (Death)
- X-axis: Years since age 1 (0-50)
- Y-axis: Proportion of cohort (0-100%)

**Interpretation**:
- Natural History: Rapid progression to ESKD and death
- Treatment: Cohort stays in better health states longer

**Use In Report**: Section 3 (Results), Population Impact

---

### Figure 4: Cost Over Age (Dual Y-Axis)
**File**: `figure4_cost_over_age.png`

**Purpose**: Show lifetime cost accumulation with annual cost reference

**Features**:
- **Left Y-Axis** (Payne's Gray): Cumulative discounted costs (€ millions)
  - Solid lines for treatment scenarios
  - Dashed line for natural history
- **Right Y-Axis** (Lime): Annual costs (€ thousands, Natural History only)
  - Dotted line as reference
- X-axis: Patient age (1-50 years)

**Interpretation**:
- Gene therapy: High upfront cost, then lower annual costs
- Natural History: Steady accumulation, spike at ESKD

**Use In Report**: Section 3 (Results), Cost Analysis

---

### Figure 5: Value-Based Pricing Heatmap
**File**: `figure5_pricing_heatmap.png`

**Purpose**: Show maximum justified gene therapy price by scenario and threshold

**Features**:
- Heatmap (red/orange/yellow gradient)
- Rows: Treatment scenarios
- Columns: WTP thresholds (€100K, €150K, €300K)
- Cell values: Max price in € millions
- Darker = higher justified price

**Interpretation**:
- Better scenarios (more QALYs) → higher max prices
- Higher thresholds → higher max prices
- This is PRIMARY economic analysis (value-based pricing)

**Use In Report**: Section 3 (Results), Value-Based Pricing; Executive Summary

---

### Figure 6: Cost-Effectiveness Plane
**File**: `figure6_ce_plane.png`

**Purpose**: Visualize scenarios relative to WTP thresholds

**Features**:
- Scatter plot with large colored points
- X-axis: Incremental QALYs
- Y-axis: Incremental Costs (€ millions)
- Dashed threshold lines:
  - Blue: €100K/QALY (conventional)
  - Orange: €150K/QALY (high-value)
  - Lime: €300K/QALY (ultra-rare)
- Scenario labels with offset

**Interpretation**:
- Points below threshold line = cost-effective at that threshold
- Points above = not cost-effective
- Further right = more health benefit
- Slope = ICER

**Use In Report**: Section 3 (Results), Cost-Effectiveness Plane; Appendix

---

### Figure 7: Survival Curves
**File**: `figure7_survival_curves.png`

**Purpose**: Show probability of survival over lifetime by scenario

**Features**:
- Kaplan-Meier style curves
- X-axis: Age (years)
- Y-axis: Survival probability (0-100%)
- Natural History: Dashed line
- Treatment scenarios: Solid lines
- Reference line at 50% (median survival)

**Interpretation**:
- Treatment curves above natural history = improved survival
- Area under curve = life years gained
- Median survival = age where curve crosses 50%

**Use In Report**: Section 3 (Results), Survival Analysis

---

### Figure 8: QALY Accumulation (Dual Y-Axis)
**File**: `figure8_qaly_accumulation.png`

**Purpose**: Show how health benefits accumulate over patient lifetime

**Features**:
- **Left Y-Axis** (Payne's Gray): Cumulative discounted QALYs
  - Solid/dashed lines for scenarios
- **Right Y-Axis** (Lime): Annual QALYs (Natural History reference)
  - Dotted line
- X-axis: Patient age (1-50 years)

**Interpretation**:
- Steeper slope = faster QALY accumulation
- Treatment curves above natural history = QALY gains
- Gap between curves = incremental QALYs
- Annual QALYs decline with age (worsening health)

**Use In Report**: Section 3 (Results), Health Benefit Accumulation

---

## Using Figures in Report

### LaTeX Integration

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/figure1_scenario_comparison.png}
  \caption{Treatment Scenario Comparison.
  \textbf{(A)} Incremental quality-adjusted life years (QALYs) gained versus natural history.
  \textbf{(B)} Equal-value life years gained (evLYG), normalized to baseline health quality.
  \textbf{(C)} Incremental costs in millions of euros.
  \textbf{(D)} Incremental cost-effectiveness ratios (ICERs) per QALY, with conventional (€100K) and ultra-rare (€300K) thresholds shown as dashed lines.}
  \label{fig:scenario_comparison}
\end{figure}
```

### Word/Google Docs

1. Insert figure: `Insert > Image > Upload from computer`
2. Add caption below: `Figure 1. Treatment Scenario Comparison...`
3. Set width: 90% of page width
4. Ensure "Wrap text" is set to "In line with text"

### PowerPoint Presentation

- Figures are 300 DPI, suitable for projection
- Transparent backgrounds work on any slide color
- Recommended: Use white or light backgrounds
- Fonts scale well at large sizes

---

## Customization

### Modifying Color Scheme

Edit `generate_hta_figures.py`:

```python
class CureLoweBrandStyle:
    # Change these values
    ULTRAMARINE_BLUE = '#2F6CD6'  # Your primary color
    IVORY = '#F1ECE2'              # Your background
    # ... etc
```

### Adjusting Font Sizes

```python
class CureLoweBrandStyle:
    FONT_SIZE = 14     # Body text
    TITLE_SIZE = 16    # Titles
    LABEL_SIZE = 14    # Axis labels
    TICK_SIZE = 12     # Tick marks
    LEGEND_SIZE = 12   # Legend
```

### Changing Figure Size

```python
# In individual figure functions
fig, ax = style.setup_figure(figsize=(width, height))

# Default is (12, 8) or (14, 8)
# For wider figures: (16, 8)
# For taller figures: (12, 10)
```

### Adding New Figures

1. Create function in `generate_hta_figures.py`:
```python
def generate_my_figure(results: Dict, output_path: str):
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure()

    # Your plotting code here
    ax.plot(...)

    style.apply_style(ax)
    plt.savefig(output_path, dpi=style.DPI,
                transparent=True, format='png')
    plt.close()
```

2. Add to `generate_all_figures()`:
```python
generate_my_figure(results, f"{output_dir}/figure9_my_figure.png")
```

---

## Troubleshooting

### Common Issues

**Fonts look wrong**
- Ensure matplotlib is using TrueType fonts
- Try: `plt.rcParams['font.family'] = 'sans-serif'`

**Colors don't match**
- Check hex codes in `CureLoweBrandStyle` class
- Verify color profile (RGB, not CMYK)

**Resolution too low**
- DPI is set to 300 by default
- Increase if needed: `fig.savefig(..., dpi=600)`

**Figures cut off**
- Use `plt.tight_layout()` before saving
- Or: `plt.savefig(..., bbox_inches='tight')`

**Transparent background not working**
- Ensure: `fig.patch.set_alpha(0)` and `ax.patch.set_alpha(0)`
- Check: `plt.savefig(..., transparent=True)`

---

## Dependencies

Required Python packages:
```bash
pip install numpy pandas matplotlib
```

Optional (for enhanced features):
```bash
pip install seaborn  # Better color palettes
pip install adjustText  # Better label positioning
```

---

## Quality Checklist

Before using figures in report:

- [ ] All text is readable (font size ≥12pt)
- [ ] Colors contrast well on white background
- [ ] Legends are clear and positioned well
- [ ] Axis labels have units
- [ ] No overlapping text
- [ ] Titles are descriptive
- [ ] Consistent styling across all figures
- [ ] 300 DPI or higher resolution
- [ ] Transparent background (no white box)
- [ ] File names are descriptive

---

## Version History

### v1.0 (November 13, 2025)
- Initial release
- 8 core figures implemented
- Cure Lowe Foundation branding applied
- Dual y-axis figures for cost and QALY accumulation
- Value-based pricing heatmap
- Complete integration with Markov model

---

## Support

For questions or issues:
1. Check `README.md` (model documentation)
2. Check `QUICKSTART.md` (getting started)
3. Check `CHANGES_NOVEMBER_2025.md` (recent updates)
4. Review code comments in `generate_hta_figures.py`

---

## License

© 2025 Cure Lowe Foundation. Internal use only.
