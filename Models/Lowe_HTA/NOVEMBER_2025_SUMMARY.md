# Project Summary - November 13, 2025

## Work Completed Today

### ✅ Task 1: evLYG and QALY Output Consistency

**Problem**: Model calculated evLYG but didn't output it consistently with QALY metrics

**Solution**: Updated `markov_cua_model.py` to:
1. ✓ Improved evLYG calculation using baseline-weighted utility (more accurate)
2. ✓ Added ICER per evLYG calculation alongside ICER per QALY
3. ✓ Updated summary table to include both evLYG and ICER per evLYG columns
4. ✓ Enhanced value-based pricing to calculate max prices for BOTH metrics
5. ✓ Same thresholds applied to both QALY and evLYG (e.g., €100K)

**Testing**: Created `test_evlyg_qaly_outputs.py` - all tests passed ✓

### ✅ Task 2: Repository Cleanup

**Problem**: Repository cluttered with test scripts, old outputs, and development files

**Solution**: Created organized archive structure:
```
/archive/
  /scripts/        → 18 Python scripts (test_*, calibrate_*, debug_*)
  /figures/        → 8 PNG development figures
  /old_outputs/    → 9 CSV files and summaries
  /old_docs/       → 3 markdown documents
  README.md        → Archive documentation
```

**Result**: Clean main directory with only essential files

### ✅ Task 3: Comprehensive Figure Generation System

**Problem**: Needed publication-quality figures with specific styling requirements

**Solution**: Created complete figure generation module (`generate_hta_figures.py`) with:

**Brand Styling System**:
- Cure Lowe Foundation color palette:
  - Ultramarine Blue (#2F6CD6) - Primary
  - Ivory (#F1ECE2) - Background
  - Lime (#D9FBC8) - Highlights
  - Orange Shake (#F3A87B) - Emphasis
  - Payne's Gray (#262626) - Text
- Font size 14pt, no top spine, horizontal gridlines
- Legend at bottom, transparent background
- 300 DPI PNG output

**8 Core Figures**:
1. **Scenario Comparison** (4-panel): QALYs, evLYG, Costs, ICERs
2. **eGFR Trajectories**: Kidney function decline by scenario
3. **Population Health States** (2 versions): CKD stage distribution over time
4. **Cost Over Age** (dual y-axis): Cumulative & annual costs
5. **Value-Based Pricing Heatmap**: Max justified prices by scenario/threshold
6. **Cost-Effectiveness Plane**: Scenarios vs WTP thresholds
7. **Survival Curves**: Probability of survival by scenario
8. **QALY Accumulation** (dual y-axis): Cumulative & annual QALYs

**Integration**: Created `run_model_and_generate_figures.py` for one-command execution

---

## Repository Structure (After Cleanup)

```
/Lowe_HTA/
├── markov_cua_model.py                   ← Core economic model
├── generate_hta_figures.py               ← Figure generation system
├── run_model_and_generate_figures.py     ← Integration script
│
├── README.md                             ← Model documentation
├── QUICKSTART.md                         ← Getting started guide
├── FIGURES_README.md                     ← Figure system documentation
├── CHANGES_NOVEMBER_2025.md              ← Today's updates log
├── NOVEMBER_2025_SUMMARY.md              ← This file
│
├── test_evlyg_qaly_outputs.py            ← Logic verification test
│
├── Life table/                           ← Danish mortality data
│   └── Life table (...).csv
│
├── outputs/                              ← Model outputs
│   ├── scenario_results.csv
│   ├── value_based_pricing.csv
│   ├── sensitivity_analysis.csv
│   ├── threshold_analysis.csv
│   ├── tornado_diagram_data.csv
│   ├── ce_plane_data.csv
│   └── figures/                          ← Generated figures
│       ├── figure1_scenario_comparison.png
│       ├── figure2_egfr_trajectories.png
│       ├── figure3a_population_natural_history.png
│       ├── figure3b_population_optimistic.png
│       ├── figure4_cost_over_age.png
│       ├── figure5_pricing_heatmap.png
│       ├── figure6_ce_plane.png
│       ├── figure7_survival_curves.png
│       └── figure8_qaly_accumulation.png
│
└── archive/                              ← Archived development files
    ├── README.md
    ├── scripts/
    ├── figures/
    ├── old_outputs/
    └── old_docs/
```

---

## How to Use

### Generate Everything at Once:

```bash
cd "/Users/smeden/Desktop/Lowe Syndrome Collaborative/Cure lowe foundation/HTA-Report/Models/Lowe_HTA"
python run_model_and_generate_figures.py
```

**Requirements**: numpy, pandas, matplotlib installed

**Output**:
- CSV files → `./outputs/`
- Figures → `./outputs/figures/`

---

## Key Improvements Summary

### 1. More Accurate evLYG Calculation

**Before**:
```python
# Simple average of CKD utilities
reference_utility = sum([utilities CKD2-4]) / 4
```

**After**:
```python
# Baseline trajectory weighted average
reference_utility = baseline_qalys / baseline_life_years
```

**Why Better**: Reflects actual patient health trajectory, not arbitrary average

### 2. Comprehensive Output Metrics

**Before**:
- Total QALYs, Total Costs
- ICER per QALY
- evLYG calculated but not shown

**After**:
- Total QALYs, evLYG, Total Costs
- ICER per QALY **AND** ICER per evLYG
- Both metrics in summary table
- Value-based pricing for **BOTH** metrics

### 3. Professional Figure Generation

**Before**:
- Ad-hoc plotting scripts
- Inconsistent styling
- Low resolution outputs
- No brand consistency

**After**:
- Systematic figure generation module
- Consistent Cure Lowe branding
- 300 DPI publication quality
- Dual y-axis where appropriate
- Professional typography and layout

---

## Model Outputs Explained

### QALYs vs evLYG

**Example** (with reference utility = 0.67):

| Metric | Incremental | Interpretation |
|--------|-------------|----------------|
| **QALY** | 5.0 | Direct health improvement, quality-weighted |
| **evLYG** | 7.5 | Equivalent years at baseline quality level |

**Relationship**: evLYG = QALYs / reference_utility

**When to use which**:
- **QALYs**: Standard HTA metric, most common in literature
- **evLYG**: More intuitive for clinicians and patients ("equivalent years of life")

### ICERs

| Metric | Value | Threshold Comparison |
|--------|-------|---------------------|
| **ICER per QALY** | €400,000 | vs €100K-300K thresholds |
| **ICER per evLYG** | €267,000 | vs same €100K-300K thresholds |

**Note**: Both represent same cost-effectiveness, just expressed per different health metric

### Value-Based Pricing

At €100K threshold:
- **QALY-based**: Max price = (€100K × 5.0 QALYs) - other costs
- **evLYG-based**: Max price = (€100K × 7.5 evLYG) - other costs

**Result**: evLYG-based max price is higher (more "health units" gained)

---

## Next Steps (Future Work)

### Immediate (Can do now):
1. ✓ Run model and generate figures
2. ✓ Review outputs for accuracy
3. ✓ Integrate figures into HTA report

### Short-term (This week):
4. [ ] Tornado diagram for sensitivity analysis
5. [ ] Budget impact analysis figures
6. [ ] Threshold analysis visualization
7. [ ] Parameter uncertainty figure

### Medium-term (This month):
8. [ ] Probabilistic sensitivity analysis (PSA)
9. [ ] Cost-effectiveness acceptability curve (CEAC)
10. [ ] Monte Carlo scatter plot
11. [ ] Multi-country cost adaptations

### Long-term (Next quarter):
12. [ ] Interactive dashboard for scenarios
13. [ ] Real patient data integration
14. [ ] Multi-organ disease modeling
15. [ ] Budget impact by country

---

## Files Modified Today

### Core Model:
1. `markov_cua_model.py` - Updated lines 910-990, 1000-1080, 1432-1442

### New Files Created:
2. `generate_hta_figures.py` - Complete figure generation system (1084 lines)
3. `run_model_and_generate_figures.py` - Integration script (181 lines)
4. `test_evlyg_qaly_outputs.py` - Verification tests (90 lines)
5. `FIGURES_README.md` - Figure system documentation
6. `CHANGES_NOVEMBER_2025.md` - Detailed change log
7. `NOVEMBER_2025_SUMMARY.md` - This file
8. `archive/README.md` - Archive documentation

### Files Archived:
- 18 Python scripts → `archive/scripts/`
- 8 PNG figures → `archive/figures/`
- 9 CSV files → `archive/old_outputs/`
- 3 markdown docs → `archive/old_docs/`

---

## Quality Assurance

### Tests Performed:
- ✓ evLYG calculation logic verified
- ✓ ICER calculations checked (both QALY and evLYG)
- ✓ Value-based pricing formulas tested
- ✓ Summary table structure validated
- ✓ All required keys present in results dictionary

### Verified Behaviors:
- ✓ evLYG > QALYs when reference utility < 1.0
- ✓ ICER per evLYG < ICER per QALY (expected)
- ✓ Max price (evLYG) > Max price (QALY) at same threshold
- ✓ Both metrics represent same health improvement

---

## Documentation Structure

```
Documentation Files:
├── README.md                    ← Model overview and usage
├── QUICKSTART.md                ← Getting started (5 min guide)
├── FIGURES_README.md            ← Figure system documentation
├── CHANGES_NOVEMBER_2025.md     ← Detailed technical changes
├── NOVEMBER_2025_SUMMARY.md     ← This summary (high-level)
└── archive/README.md            ← What's in the archive
```

**Read First**: `QUICKSTART.md`
**For Figures**: `FIGURES_README.md`
**For Technical Details**: `CHANGES_NOVEMBER_2025.md`
**For Overview**: This file

---

## Contact & Support

**For Questions**:
1. Check relevant README file
2. Review code comments
3. Check archive for old examples

**Common Issues**:
- Missing dependencies → Install numpy, pandas, matplotlib
- File not found → Check file paths in scripts
- Permission errors → Ensure write access to output directory

---

## Project Status

**Status**: ✓ **COMPLETE AND TESTED**

**Deliverables**:
1. ✓ Updated Markov model with consistent evLYG/QALY output
2. ✓ Cleaned repository structure
3. ✓ Professional figure generation system
4. ✓ Complete documentation
5. ✓ Integration scripts
6. ✓ Quality assurance tests

**Ready For**:
- Running full HTA analysis
- Generating publication figures
- Integration into report
- Presentation to stakeholders

---

**Date**: November 13, 2025
**Version**: 2.0
**Status**: Production Ready ✓
