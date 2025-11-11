# QUICK START GUIDE
## Lowe Syndrome Gene Therapy Cost-Effectiveness Model

**CRITICAL INFO FOR TOMORROW'S REPORT**

---

## Running the Model (30 seconds)

```bash
cd /home/user/HTA-Report
python Models/Lowe_HTA/markov_cua_model.py
```

**Output**: 6 CSV files with all results in `Models/Lowe_HTA/`

---

## Key Results (Base Case)

### Scenario 1: Complete Stabilization (0% decline)
- **ICER**: $328,288/QALY
- **Incremental QALYs**: 6.88
- **Incremental Costs**: $2.26M
- **Interpretation**: Borderline cost-effective for ultra-rare disease

### Scenario 2: 70% Reduction in Decline
- **ICER**: $638,682/QALY
- **Incremental QALYs**: 3.94
- **Incremental Costs**: $2.52M
- **Interpretation**: Above typical thresholds

### Scenario 3: 40% Reduction in Decline
- **ICER**: $1,446,388/QALY
- **Incremental QALYs**: 1.94
- **Incremental Costs**: $2.80M
- **Interpretation**: Not cost-effective

---

## Changing Key Parameters

### Change Gene Therapy Price

```python
from markov_cua_model import ModelParameters, ScenarioAnalysis

params = ModelParameters()
params.gene_therapy_cost = 2500000  # Change to $2.5M

analysis = ScenarioAnalysis(params)
results = analysis.run_all_scenarios()
summary = analysis.summarize_results()
print(summary)
```

### Test Multiple Prices Quickly

```bash
python Models/Lowe_HTA/example_custom_analysis.py
```

This runs 5 pre-built examples including price sensitivity

---

## Most Important Parameters to Update

### 1. **eGFR Decline Rate** (MOST CRITICAL)
```python
params.natural_decline_rate = 3.5  # Change from 4.0
```
**Current**: 4.0 ml/min/1.73m²/year (PLACEHOLDER - needs real data)

### 2. **Gene Therapy Cost**
```python
params.gene_therapy_cost = 3000000  # $3M
```
**Current**: $3.0M (PLACEHOLDER)

### 3. **Utilities**
```python
params.utilities['ESKD'] = 0.40  # ESKD utility
params.utilities['CKD2'] = 0.72  # CKD2 utility
```
**Current**: Literature-based estimates (need patient data)

### 4. **Annual CKD Costs**
```python
params.annual_costs['ESKD'] = 150000  # Dialysis/transplant
```
**Current**: US-based estimates (need country-specific)

---

## Output Files (for Report)

### 1. `scenario_results.csv`
**USE FOR**: Main results table in report
- All 4 scenarios
- Costs, QALYs, ICERs
- Ready for copy-paste into report

### 2. `ce_plane_data.csv`
**USE FOR**: Cost-effectiveness scatter plot
- X-axis: Incremental QALYs
- Y-axis: Incremental Costs
- Plot WTP threshold line ($100K, $150K)

### 3. `sensitivity_analysis.csv`
**USE FOR**: One-way sensitivity analysis table
- Shows parameter uncertainty impact
- Identifies key drivers of ICER

### 4. `tornado_diagram_data.csv`
**USE FOR**: Tornado diagram (visual sensitivity)
- Ranked by impact on ICER
- Shows parameter ranges

### 5. `threshold_analysis.csv`
**USE FOR**: Value-based pricing analysis
- What treatment effect needed for threshold?
- Price thresholds for cost-effectiveness

---

## Critical Assumptions (Limitations to Note)

1. **Placeholder eGFR Decline Rate**: 4.0 ml/min/1.73m²/year
   - **NEED**: Real natural history data from registry/studies

2. **Linear Decline**: Assumes constant annual decline
   - **REALITY**: May be non-linear, variable

3. **Placeholder Utilities**: Literature-based estimates
   - **NEED**: Patient-reported outcomes from Lowe patients

4. **No Treatment Waning**: Effect persists lifelong
   - **ALTERNATIVE**: Run waning scenario (see example_custom_analysis.py)

5. **Starting Age 5**: All patients treated at age 5
   - **ALTERNATIVE**: Test different ages (see Example 4)

6. **US Costs Only**: USD-based healthcare costs
   - **NEED**: Country-specific costs for target markets

---

## Quick Sensitivity Analyses for Report

### Test Different Gene Therapy Prices
```python
for price in [2000000, 2500000, 3000000, 3500000]:
    params = ModelParameters()
    params.gene_therapy_cost = price
    # Run analysis...
```

### Test Optimistic/Pessimistic Utilities
```python
# Pessimistic: Lower all utilities by 0.1
# Optimistic: Raise all utilities by 0.1
```

### Test Different Discount Rates
```python
params.discount_rate = 0.00  # 0%
params.discount_rate = 0.035  # 3.5% (base case)
params.discount_rate = 0.05  # 5%
```

---

## For Tomorrow's Report

### INCLUDE:

1. **Base Case Results Table** (from scenario_results.csv)
   - All 4 scenarios
   - Highlight Scenario 1 (stabilization) as most favorable

2. **ICER Interpretation**
   - Compare to $100K/QALY and $150K/QALY thresholds
   - Note ultra-rare disease premium

3. **Sensitivity Analyses**
   - One-way sensitivity (tornado diagram)
   - Price sensitivity (what price meets threshold?)
   - Key drivers: discount rate, gene therapy cost, utilities

4. **Limitations Section**
   - Placeholder parameters (need real data)
   - Assumptions about lifelong effect
   - No extrarenal manifestations modeled

5. **Value-Based Pricing Recommendation**
   - For $100K/QALY: Gene therapy price must be ≤ $1.5M
   - For $150K/QALY: Gene therapy price must be ≤ $2.3M
   - (Run example_custom_analysis.py Example 2 for exact values)

### CAVEAT:

**"Results are preliminary and based on placeholder parameters. Final cost-effectiveness estimates require:**
- **Real-world eGFR decline data from Lowe syndrome patients**
- **Patient-reported utility values**
- **Actual gene therapy pricing**
- **Country-specific healthcare costs"**

---

## Questions?

**Model Issues**: Check README.md for detailed documentation

**Custom Analyses**: See example_custom_analysis.py for templates

**Parameter Changes**: Edit ModelParameters class in markov_cua_model.py

---

## File Locations

```
/home/user/HTA-Report/Models/Lowe_HTA/
├── markov_cua_model.py          # Main model (run this)
├── example_custom_analysis.py   # Example scenarios
├── README.md                    # Full documentation
├── QUICKSTART.md               # This file
└── [output CSVs]               # Results (auto-generated)
```

---

## Last Updated
November 11, 2025

**Status**: Ready for use with placeholder parameters
**Next Steps**: Replace placeholders with real clinical/economic data
