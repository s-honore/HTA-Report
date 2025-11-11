# Lowe Syndrome Gene Therapy Cost-Effectiveness Analysis

## Markov Cohort Model for Cost-Utility Analysis

This directory contains a comprehensive Markov cohort model for evaluating the cost-effectiveness of gene therapy for Lowe syndrome.

---

## Model Overview

### Structure
- **Health States**: CKD Stage 2, 3a, 3b, 4, 5/ESKD, Death
- **Cycle Length**: Annual (1 year)
- **Time Horizon**: Lifetime (100 years)
- **Starting Age**: 5 years (median treatment age)
- **Perspective**: Healthcare system
- **Discount Rate**: 3.5% (base case)

### Model Logic
The model tracks a cohort of Lowe syndrome patients through chronic kidney disease (CKD) stages based on estimated glomerular filtration rate (eGFR) decline. The model:

1. Starts with all patients at eGFR 70 ml/min/1.73m² (CKD Stage 2)
2. Applies annual eGFR decline based on scenario
3. Transitions patients between CKD stages as eGFR declines
4. Accumulates costs and quality-adjusted life years (QALYs)
5. Calculates incremental cost-effectiveness ratios (ICERs)

---

## Scenarios

### Scenario 0: Natural History (Baseline)
- **eGFR Decline**: 4.0 ml/min/1.73m²/year
- **Description**: No treatment, disease progresses naturally
- **Use**: Reference comparator for all interventions

### Scenario 1: Stabilization
- **eGFR Decline**: 0.0 ml/min/1.73m²/year (complete stabilization)
- **Description**: Gene therapy completely prevents kidney function decline
- **Gene Therapy Cost**: $3.0M + monitoring
- **Result**: ICER ~$328K/QALY vs natural history

### Scenario 2: 70% Reduction
- **eGFR Decline**: 1.2 ml/min/1.73m²/year (70% reduction from baseline)
- **Description**: Gene therapy reduces decline rate by 70%
- **Gene Therapy Cost**: $3.0M + monitoring
- **Result**: ICER ~$639K/QALY vs natural history

### Scenario 3: 40% Reduction
- **eGFR Decline**: 2.4 ml/min/1.73m²/year (40% reduction from baseline)
- **Description**: Gene therapy reduces decline rate by 40%
- **Gene Therapy Cost**: $3.0M + monitoring
- **Result**: ICER ~$1.45M/QALY vs natural history

---

## Key Parameters

### Clinical Parameters

#### eGFR and Disease Progression
```python
starting_egfr = 70.0  # ml/min/1.73m² at age 5
natural_decline_rate = 4.0  # ml/min/1.73m²/year (natural history)
starting_age = 5  # years
time_horizon_years = 100  # lifetime horizon
```

#### CKD Stage Definitions (eGFR ml/min/1.73m²)
```python
ckd_thresholds = {
    'CKD2': (60, 90),   # Stage 2: 60-89
    'CKD3a': (45, 60),  # Stage 3a: 45-59
    'CKD3b': (30, 45),  # Stage 3b: 30-44
    'CKD4': (15, 30),   # Stage 4: 15-29
    'ESKD': (0, 15),    # Stage 5/ESKD: <15
}
```

### Health State Utilities (QALY Weights)
```python
utilities = {
    'CKD2': 0.72,   # Mild CKD
    'CKD3a': 0.68,  # Moderate CKD
    'CKD3b': 0.61,  # Moderate-severe CKD
    'CKD4': 0.54,   # Severe CKD
    'ESKD': 0.40,   # End-stage kidney disease
    'Death': 0.00
}
```

**Sources**: Based on published EQ-5D utilities for CKD stages (Wyld et al. 2012, Am J Kidney Dis)

### Annual Costs by CKD Stage (USD)
```python
annual_costs = {
    'CKD2': 20000,    # $20K/year
    'CKD3a': 25000,   # $25K/year
    'CKD3b': 40000,   # $40K/year
    'CKD4': 50000,    # $50K/year
    'ESKD': 150000,   # $150K/year (dialysis/transplant)
    'Death': 0
}
```

**Note**: Costs include all CKD-related healthcare costs (medications, monitoring, hospitalizations, dialysis, etc.)

### Gene Therapy Costs (USD)
```python
gene_therapy_cost = 3000000  # $3.0M one-time cost
monitoring_year1 = 25000     # $25K in year 1
monitoring_year2_5 = 10000   # $10K in years 2-5
monitoring_ongoing = 3000    # $3K in years 6+
```

### Mortality Parameters
```python
base_mortality_rate = 0.02  # 2% base annual mortality rate

mortality_multipliers = {
    'CKD2': 1.0,    # No excess mortality
    'CKD3a': 1.2,   # 20% increased mortality
    'CKD3b': 1.5,   # 50% increased mortality
    'CKD4': 2.0,    # 2x mortality
    'ESKD': 3.0,    # 3x mortality
}
```

**Note**: Mortality increases with age (1% per year) and CKD severity

### Economic Parameters
```python
discount_rate = 0.035  # 3.5% for costs and QALYs
```

---

## Usage

### Basic Usage

#### 1. Run the Full Analysis
```bash
python markov_cua_model.py
```

This will:
- Run all 4 scenarios
- Calculate ICERs
- Perform one-way sensitivity analysis
- Run threshold analysis
- Generate tornado diagram data
- Save all results to CSV files

#### 2. Use in Python Script
```python
from markov_cua_model import ModelParameters, ScenarioAnalysis, SensitivityAnalysis

# Create parameters
params = ModelParameters()

# Run scenarios
scenario_analysis = ScenarioAnalysis(params)
results = scenario_analysis.run_all_scenarios()

# Get summary table
summary = scenario_analysis.summarize_results()
print(summary)

# Access specific scenario results
baseline = results['Scenario 0: Natural History']
stabilization = results['Scenario 1: Stabilization (0%)']

print(f"Baseline QALYs: {baseline['total_qalys']:.2f}")
print(f"Stabilization QALYs: {stabilization['total_qalys']:.2f}")
print(f"ICER: ${stabilization['icer']:,.0f}/QALY")
```

---

## Modifying Parameters

### Option 1: Modify in Code

Edit the `ModelParameters` class defaults in `markov_cua_model.py`:

```python
@dataclass
class ModelParameters:
    # Change any parameter here
    starting_egfr: float = 70.0
    natural_decline_rate: float = 4.0
    gene_therapy_cost: float = 3000000
    discount_rate: float = 0.035
    # ... etc
```

### Option 2: Override at Runtime

```python
from markov_cua_model import ModelParameters, MarkovCohortModel

# Create custom parameters
params = ModelParameters()
params.gene_therapy_cost = 2500000  # Change to $2.5M
params.discount_rate = 0.05  # Change to 5%
params.natural_decline_rate = 3.5  # Change baseline decline

# Update utilities
params.utilities['ESKD'] = 0.35  # Lower ESKD utility

# Update costs
params.annual_costs['ESKD'] = 180000  # Higher dialysis costs

# Run model with custom parameters
model = MarkovCohortModel(params)
results = model.run_model(
    egfr_decline_rate=0.0,
    scenario_name="Custom Scenario",
    include_gene_therapy_cost=True
)

print(f"Total QALYs: {results['total_qalys']:.2f}")
print(f"Total Costs: ${results['total_costs']:,.0f}")
```

### Option 3: Batch Parameter Variations

```python
# Test different gene therapy prices
gt_costs = [2000000, 2500000, 3000000, 3500000, 4000000]

for cost in gt_costs:
    params = ModelParameters()
    params.gene_therapy_cost = cost

    scenario_analysis = ScenarioAnalysis(params)
    results = scenario_analysis.run_all_scenarios()

    stab = results['Scenario 1: Stabilization (0%)']
    print(f"GT Cost: ${cost:,.0f} -> ICER: ${stab['icer']:,.0f}/QALY")
```

---

## Output Files

All output files are saved to `/home/user/HTA-Report/Models/Lowe_HTA/`

### 1. `scenario_results.csv`
Summary table of all 4 scenarios with costs, QALYs, ICERs

**Columns**:
- Scenario name
- eGFR Decline Rate
- Total Costs ($)
- Total QALYs
- Life Years
- Time to ESKD (years)
- Incremental Costs ($)
- Incremental QALYs
- ICER ($/QALY)

### 2. `sensitivity_analysis.csv`
One-way sensitivity analysis results

**Columns**:
- Parameter name
- Low Value
- High Value
- ICER at Low
- ICER at Base
- ICER at High
- Range (total variation)
- Base to Low Change
- Base to High Change

### 3. `tornado_diagram_data.csv`
Data formatted for creating tornado diagrams

**Use**: Import into plotting software or use with matplotlib to create tornado diagram showing parameter uncertainty impact

### 4. `threshold_analysis.csv`
Threshold analysis testing different decline reduction levels

**Purpose**: Find the minimum treatment effect (decline reduction) needed to meet cost-effectiveness thresholds

### 5. `ce_plane_data.csv`
Cost-effectiveness plane data

**Columns**:
- Scenario
- Incremental_Costs
- Incremental_QALYs
- ICER

**Use**: Plot on cost-effectiveness plane (scatter plot with WTP threshold line)

---

## Interpreting Results

### ICER Thresholds

**Common willingness-to-pay (WTP) thresholds**:
- **$50,000/QALY**: Traditional US threshold
- **$100,000/QALY**: Modern US threshold for rare diseases
- **$150,000/QALY**: High-value threshold
- **£20,000-30,000/QALY**: UK NICE threshold
- **£100,000/QALY**: UK NICE threshold for ultra-rare diseases

### Example Results Interpretation

**Scenario 1: Stabilization**
- ICER: $328,288/QALY
- **Interpretation**: Above typical thresholds but potentially acceptable for ultra-rare disease with severe outcomes
- **Decision**: Borderline cost-effective; may require price negotiation or value-based agreements

**Scenario 2: 70% Reduction**
- ICER: $638,682/QALY
- **Interpretation**: High ICER, unlikely to be cost-effective at standard thresholds
- **Decision**: Would need substantial price reduction or additional value evidence

**Scenario 3: 40% Reduction**
- ICER: $1,446,388/QALY
- **Interpretation**: Very high ICER, dominated strategy
- **Decision**: Not cost-effective; insufficient treatment effect

---

## Sensitivity Analyses

### One-Way Sensitivity Analysis

Tests impact of parameter uncertainty on ICER:

**Most Influential Parameters** (from base case):
1. **Discount Rate** (0% to 7%): Range of $568K in ICER
2. **Gene Therapy Cost** ($2M to $4M): Range of $291K in ICER
3. **Utility CKD2** (0.65 to 0.80): Range of $128K in ICER

**Interpretation**: Model is most sensitive to discount rate and gene therapy price

### Threshold Analysis

Finds the minimum treatment effect needed for cost-effectiveness:

**Example Question**: What decline reduction is needed for $100K/QALY threshold?

Run threshold analysis and check results:
```python
threshold_results = sensitivity.threshold_analysis(
    target_icer=100000,
    decline_range=(0.0, 4.0),
    n_points=50
)
```

---

## Validation

### Model Validation Steps

1. **Face Validity**: Clinical experts review model structure and parameters
2. **Internal Validity**:
   - Extreme value testing (e.g., 0% decline should maximize QALYs)
   - Conservation of cohort (sum of proportions = 1)
   - Monotonicity (better treatment → better outcomes)
3. **External Validity**: Compare results to published CKD models

### Verification Checks

```python
# Check cohort conservation
assert np.allclose(trace.sum(axis=1), 1.0), "Cohort proportions don't sum to 1"

# Check monotonicity
assert stabilization['total_qalys'] >= baseline['total_qalys'], "Treatment worse than baseline"

# Check costs are positive
assert all(costs >= 0 for costs in results['costs_by_cycle']), "Negative costs detected"
```

---

## Assumptions and Limitations

### Key Assumptions

1. **Linear eGFR Decline**: Assumes constant annual decline rate
   - Reality: Decline may be non-linear or variable

2. **One-Time Gene Therapy**: Assumes single administration with permanent effect
   - Reality: May need re-dosing or booster treatments

3. **Homogeneous Cohort**: All patients start at same age/eGFR
   - Reality: Patient heterogeneity in baseline characteristics

4. **No Treatment Waning**: Effect persists lifelong
   - Reality: Treatment effect may diminish over time

5. **Perfect Adherence**: All patients receive full monitoring
   - Reality: Real-world adherence may be lower

### Limitations

1. **Placeholder Utilities**: Current utilities are estimates; need patient-reported data
2. **Mortality Model**: Simple age/stage-based; could use survival data from registries
3. **Costs**: US-centric; need country-specific cost inputs
4. **No Adverse Events**: Model doesn't include treatment-related AEs
5. **No Extrarenal Manifestations**: Lowe syndrome affects eyes, brain, bones - not captured

---

## Future Enhancements

### Planned Updates

1. **Real Clinical Data**: Replace placeholder parameters with trial/registry data
2. **Probabilistic Sensitivity Analysis (PSA)**: Add Monte Carlo simulation for uncertainty
3. **Scenario Manager**: Web interface for parameter modification
4. **Visualization Module**: Automated generation of publication-quality figures
5. **Multi-Country Adaptation**: Add cost/utility inputs for multiple countries
6. **Extrarenal Costs**: Incorporate non-renal Lowe syndrome costs
7. **Budget Impact Analysis**: Add population-level budget impact model

### Enhancement Priorities

**High Priority**:
- Real eGFR decline data from natural history studies
- Validated utility values from patient surveys
- Country-specific cost inputs

**Medium Priority**:
- PSA with parameter distributions
- Scenario analysis for different starting ages
- Treatment waning scenarios

**Low Priority**:
- Complex comorbidity modeling
- Competing risk mortality
- Healthcare system capacity constraints

---

## References

### Model Structure
- Briggs A, Claxton K, Sculpher M. Decision Modelling for Health Economic Evaluation. Oxford University Press, 2006.

### CKD Utilities
- Wyld M, et al. A systematic review and meta-analysis of utility-based quality of life in chronic kidney disease treatments. Am J Kidney Dis. 2012;60(2):253-265.

### CKD Costs
- Honeycutt AA, et al. Medical costs of CKD in the Medicare population. J Am Soc Nephrol. 2013;24(9):1478-1483.

### Gene Therapy Economics
- Hampson G, et al. Gene therapy for rare diseases: Making value assessment fit for purpose. Health Policy. 2020;124(9):912-919.

---

## Contact

For questions about the model or to report issues:
- Model Developer: HTA Analysis Team
- Date: November 2025
- Repository: `/home/user/HTA-Report/Models/Lowe_HTA/`

---

## Version History

### Version 1.0 (November 11, 2025)
- Initial release
- 4 scenarios implemented
- One-way sensitivity analysis
- Threshold analysis
- Comprehensive documentation

---

## License

This model is proprietary to the HTA Analysis Team. Internal use only.
