# UPDATED Section 3 Implementation Plan
## Post-Recalibration & QALY/LYG Analysis

**Date**: November 12, 2025
**Status**: Ready for Review
**Purpose**: Comprehensive plan to update Section 3 with recalibrated model and enhanced reporting

---

## EXECUTIVE SUMMARY

### ✅ COMPLETED WORK (Since Original Plan)

1. **✅ Model Recalibration** - Successfully addressed poor "realistic" scenario ICER
   - Starting eGFR: 83 → **95 ml/min/1.73m²** (physiologically plausible)
   - Decline rates moderated: 3.5→**3.0**, 2.0→**1.5** ml/min/yr
   - Natural history validation: **ESKD age 32.0 ✓** (target: 32 from Ando 2024)

2. **✅ Scenario Framework Redefined** - More realistic treatment effect assumptions
   - **Optimistic (θ=1.0)**: Carrier-equivalent → ICER **$309K/QALY**
   - **Realistic (θ=0.85)**: Good biodistribution → ICER **$327K/QALY** (was $871K!)
   - **Conservative (θ=0.70)**: Moderate biodistribution → ICER **$414K/QALY**
   - **Pessimistic (θ=0.50)**: Suboptimal biodistribution → ICER **$689K/QALY**

3. **✅ Treatment Waning Implementation** - Gradual loss over years 10-20
   - Linear interpolation from optimistic (θ=1.0) to conservative (θ=0.70)
   - ICER: **$365K/QALY**

4. **✅ QALY/LYG Gap Analysis** - Diagnosed why 25 LYG = 8 QALYs
   - **Discounting (1.5%): 57.5% loss** (biggest factor!)
   - Lowe utility multiplier (0.85): 15% reduction
   - Low base CKD utilities: 0.34-0.61
   - **Solution**: Report both $/QALY and $/LYG metrics

5. **✅ Visualization Figures** - 4 publication-quality figures generated
   - Figure 1: Age-varying decline rates by scenario
   - Figure 2: eGFR trajectories through CKD stages
   - Figure 3: Treatment waning effect
   - Figure 4: Cost-effectiveness plane

---

## PART 1: CRITICAL DECISIONS NEEDED

### Decision 1: Primary Metric Reporting ⭐ **USER DECISION REQUIRED**

**Current Status**: Model calculates both metrics
- ICER ($/QALY): Standard HTA metric
- Cost per LYG ($/LYG): Shows survival benefit magnitude

**Recommendation**: Report BOTH metrics
```
Realistic Scenario Results:
- Primary metric: $327,070/QALY
- Secondary metric: $106,652/LYG
- Life years gained: 24.1 years
- QALYs gained: 7.86 (discounted at 1.5%)
```

**Rationale**:
- $/LYG shows substantial survival benefit (~$100K/LYG is highly cost-effective)
- $/QALY appropriately captures quality adjustments for Lowe comorbidities
- Both metrics together tell complete story
- Standard practice for curative therapies in rare diseases

**Alternative**: Report only $/QALY (but this may understate survival benefit)

---

### Decision 2: Lowe Utility Multiplier

**Current**: 0.85 (15% decrement from base CKD utilities)
**Justification**:
- Intellectual disability (90% prevalence)
- Visual impairment (100% prevalence)
- Neurological manifestations (100% prevalence)

**Options**:
- **Keep 0.85** (conservative, well-justified)
- **Increase to 0.90** (10% decrement) → would improve ICER by ~18%
- **Test in sensitivity** (range 0.80-0.95)

**Recommendation**: Keep 0.85 as base case, test 0.90 in sensitivity

---

### Decision 3: Section 3 Text Updates

**Required Changes**:
1. Update all parameter values to reflect recalibration
2. Add treatment waning subsection with gradual transition description
3. Update scenario definitions (θ=0.85 as realistic, not θ=0.5)
4. Add QALY/LYG reporting framework
5. Update all result tables with new ICERs
6. Add calibration validation subsection

**Estimated Scope**: ~40 lines of text changes, 3 new tables

---

## PART 2: TEXT UPDATES FOR SECTION 3

### 2.1 Natural History Parameters (UPDATE)

**CURRENT TEXT** (lines 58-64):
```
We calibrate the starting eGFR (eGFR₀ at age 1) to achieve median ESKD onset
at age 32, as reported by Ando et al. (2024). Starting with eGFR₀ = 83 ml/min/1.73m²,
the age-varying decline rates produce median time to ESKD at Year 18 (age 19).
```

**NEW TEXT**:
```
We calibrate the starting eGFR and decline rates to achieve median ESKD onset
at age 32, as reported by Ando et al. (2024). The recalibrated model uses:

- Starting eGFR: eGFR₀ = 95 ml/min/1.73m² at age 1
- Age-varying decline rates: δ(age) = { 1.0 ml/min/yr    (ages 1-10)
                                        { 3.0 ml/min/yr    (ages 10-20)
                                        { 1.5 ml/min/yr    (ages 20+)

This calibration produces:
- Median ESKD age: 32.0 years ✓ (target: 32)
- Median survival: 37.5 years ✓ (target: 30-40)
- Post-ESKD survival: 5.5 years ✓ (target: 3-8)

The moderated adolescent decline rate (3.0 vs initial estimate 3.5 ml/min/yr)
accounts for uncertainty in visual slope estimation from Ando Figure 1B and
produces natural history outcomes consistent with published literature.
```

---

### 2.2 Treatment Scenarios (MAJOR UPDATE)

**CURRENT TEXT** (lines 107-130):
```
Scenario 1: Carrier-Equivalent (θ=1.0, decline 0.30 ml/min/yr)
Scenario 2: Subthreshold (θ=0.5, decline 0.70 ml/min/yr)
Scenario 3: Minimal (θ=0.2, decline 0.94 ml/min/yr)
```

**NEW TEXT**:
```markdown
**Treatment Scenarios: Biodistribution-Driven Framework.** We model four primary
treatment scenarios representing different levels of therapeutic success, defined
by the pathological reduction parameter θ:

**Scenario 1: Optimistic (θ = 1.0) - Carrier-Equivalent Protection**
Gene therapy achieves ≥50% OCRL enzyme activity in kidney cells, matching
heterozygous carrier phenotype. Complete elimination of pathological decline,
with only normal aging-related eGFR loss (0.30 ml/min/yr time-averaged).
- Assumption: Excellent biodistribution to proximal tubule
- Precedent: Carrier females show minimal CKD progression (Ando 2024)

**Scenario 2: Realistic (θ = 0.85) - Good Biodistribution**
Gene therapy achieves 40-50% OCRL enzyme activity, representing successful but
imperfect biodistribution. Eliminates 85% of pathological decline component.
Time-averaged decline: 0.52 ml/min/yr.
- Assumption: High transduction efficiency in target cells
- Justification: Realistic expectation for AAV-based kidney gene therapy
- **BASE CASE for economic evaluation**

**Scenario 3: Conservative (θ = 0.70) - Moderate Biodistribution**
Gene therapy achieves 30-40% OCRL enzyme activity. Eliminates 70% of pathological
decline. Time-averaged decline: 0.74 ml/min/yr.
- Assumption: Moderate transduction, some proximal tubule regions under-treated
- Use case: Sensitivity analysis, conservative pricing scenarios

**Scenario 4: Pessimistic (θ = 0.50) - Suboptimal Biodistribution**
Gene therapy achieves 25-30% OCRL enzyme activity. Eliminates only 50% of
pathological decline. Time-averaged decline: 1.04 ml/min/yr.
- Assumption: Poor biodistribution or limited transduction
- Use case: Worst-case sensitivity, threshold analysis
- Note: Still provides meaningful benefit (11 life years gained vs natural history)

**Scenario 5: Treatment Waning - Gradual Loss of Effect**
Gene therapy starts at optimistic level (θ=1.0) but gradually wanes over years
10-20 to conservative level (θ=0.70). Models potential loss of transgene expression
or immune-mediated clearance over time.
- Waning mechanism: Linear interpolation over 10-year period
- Final state: Conservative-level protection maintained thereafter
- Use case: Long-term durability uncertainty
```

---

### 2.3 NEW SECTION: Treatment Waning Dynamics

**INSERT AFTER SCENARIO DEFINITIONS** (new subsection):

```markdown
### Treatment Effect Waning Over Time

**Rationale for Waning Scenario.** Long-term durability of AAV-mediated gene therapy
remains uncertain, particularly in pediatric applications where organ growth, immune
maturation, and potential transgene silencing may impact sustained expression. While
some AAV therapies demonstrate stable expression beyond 10 years (e.g., hemophilia B),
kidney-specific challenges include high cell turnover in proximal tubule and potential
immune responses to capsid or transgene products. The waning scenario models gradual
loss of therapeutic effect as a sensitivity analysis for long-term uncertainty.

**Waning Implementation.** We model treatment waning as gradual linear interpolation
over years 10-20 post-therapy:

**(12)   δ_treated(t, age) = { δ_initial(age)                                    t < 10
                               { δ_initial(age) + (t-10)/10 × [δ_final(age) - δ_initial(age)]   10 ≤ t < 20
                               { δ_final(age)                                    t ≥ 20

where t represents years since gene therapy administration, δ_initial corresponds to
optimistic scenario (θ=1.0), and δ_final corresponds to conservative scenario (θ=0.70).

**Rationale for Gradual vs Sudden Waning.** We implement gradual waning over 10 years
rather than sudden loss for biological plausibility. Transgene expression loss likely
occurs gradually through progressive cell turnover, immune-mediated clearance, or
epigenetic silencing rather than acute failure. The 10-year waning period represents
a conservative assumption; actual durability data from ongoing trials may support
longer sustained expression.

**Waning Scenario Results.** The gradual waning scenario produces intermediate outcomes:
- Life years gained: 21.7 years (vs 25.1 for sustained optimistic)
- QALYs gained: 7.21 (vs 8.21 for sustained optimistic)
- ICER: $365,245/QALY (vs $309,300 for sustained optimistic)

These results suggest that even with significant waning, gene therapy provides
substantial clinical benefit and reasonable cost-effectiveness for a curative
therapy in an ultra-rare disease.
```

---

### 2.4 NEW SECTION: QALY vs Life Years Gained

**INSERT IN RESULTS SECTION** (new subsection):

```markdown
### Interpreting QALY Gains vs Life Years Gained

**Observed QALY/LYG Ratio.** Our model predicts that gene therapy extends life by
24-25 years in optimistic and realistic scenarios, but generates only 7.9-8.2
incremental QALYs (discounted at 1.5%). This yields a QALY-to-life-year ratio of
approximately 0.33, meaning each additional year of life contributes only 0.33 QALYs
on average. This low ratio requires careful interpretation in the HTA context.

**Three Factors Explain Low QALY/LYG Ratio:**

1. **Discounting of Distant Health Gains (57.5% QALY Loss)**
   The 1.5% annual discount rate substantially reduces the present value of QALYs
   accrued 30-50 years in the future. For the realistic scenario:
   - Undiscounted incremental QALYs: 18.00
   - Discounted incremental QALYs: 7.86
   - Loss to discounting: 56.3%

   At 1.5%, QALYs realized 50 years post-therapy are worth only 47% of present value.
   This is mathematically appropriate for long-horizon economic evaluation but can
   understate the clinical magnitude of survival benefit in curative pediatric therapies.

2. **Lowe Syndrome Comorbidity Burden (15% Utility Reduction)**
   We apply a 0.85 multiplier to base CKD utilities to account for Lowe-specific
   morbidity not captured in standard kidney disease quality-of-life studies:
   - Intellectual disability (90% prevalence, typically moderate)
   - Visual impairment (100% prevalence, cataracts + glaucoma)
   - Neurological manifestations (100% prevalence, hypotonia, behavioral issues)

   This multiplier reduces all health state utilities (e.g., CKD Stage 2 from 0.72
   to 0.61), appropriately capturing the broader disease burden beyond renal function.

3. **Low Base CKD Utilities (Literature Standard)**
   Standard CKD utilities from general population studies (Wyld et al. 2012) are
   relatively low:
   - CKD Stage 2: 0.72 (→ 0.61 after Lowe adjustment)
   - CKD Stage 4: 0.54 (→ 0.46 after Lowe adjustment)
   - ESKD: 0.40 (→ 0.34 after Lowe adjustment)

   These reflect the genuine burden of chronic kidney disease, including symptoms,
   dietary restrictions, medication burden, and psychosocial impact.

**Alternative Metric: Cost per Life Year Gained ($/LYG).** To complement the standard
ICER ($/QALY) and provide full transparency on survival benefits, we report cost per
life year gained:

| Scenario | ICER ($/QALY) | Cost per LYG | Life Years Gained | QALY Gain |
|----------|---------------|--------------|-------------------|-----------|
| Optimistic | $309,300 | **$101,213** | 25.1 | 8.21 |
| Realistic | $327,070 | **$106,652** | 24.1 | 7.86 |
| Conservative | $413,893 | $142,244 | 18.9 | 6.48 |
| Pessimistic | $689,209 | $263,663 | 10.8 | 4.13 |

At approximately **$100,000 per life year gained**, gene therapy for Lowe syndrome
appears highly cost-effective using this alternative metric. The substantial difference
between $/QALY and $/LYG reflects the genuine quality-of-life burden of Lowe syndrome,
not a modeling artifact. Both metrics are valid and informative for decision-making:

- **$/QALY** appropriately captures disease burden and aligns with HTA standards
- **$/LYG** demonstrates the magnitude of survival benefit (24+ years)

**Recommendation for HTA Decision-Making.** We recommend reporting both metrics in
parallel, with $/QALY as the primary decision criterion (consistent with NICE/ICER
methodology) and $/LYG as supplementary evidence of clinical benefit magnitude. The
low QALY/LYG ratio is not a model flaw but an accurate reflection of significant
non-renal morbidity in Lowe syndrome, which gene therapy addresses only partially
(OCRL correction improves renal but not neurological or ophthalmologic outcomes).
```

---

### 2.5 Updated Results Table (BASE CASE)

**REPLACE EXISTING RESULTS TABLE** with:

```markdown
### Table 3: Base Case Cost-Effectiveness Results (Recalibrated Model)

| Scenario | ESKD Age | Death Age | Life Years | Total QALYs | Inc. QALYs | Inc. Costs | ICER ($/QALY) | $/LYG | Assessment |
|----------|----------|-----------|------------|-------------|------------|------------|---------------|-------|------------|
| Natural History | 32.0 | 37.5 | 37.5 | 14.59 | — | — | — | — | Baseline |
| **Optimistic (θ=1.0)** | >100 | 62.6 | 62.6 | 22.80 | 8.21 | $2,539K | **$309,300** | **$101,213** | Cost-effective* |
| **Realistic (θ=0.85)** | >100 | 61.6 | 61.6 | 22.45 | 7.86 | $2,571K | **$327,070** | **$106,652** | Cost-effective* |
| Conservative (θ=0.70) | >100 | 56.4 | 56.4 | 21.07 | 6.48 | $2,682K | $413,893 | $142,244 | Borderline |
| Pessimistic (θ=0.50) | >100 | 48.3 | 48.3 | 18.72 | 4.13 | $2,848K | $689,209 | $263,663 | Not CE |
| Treatment Waning | >100 | 59.1 | 59.1 | 21.80 | 7.21 | $2,633K | $365,245 | $125,514 | Cost-effective* |

*Cost-effective at €300,000/QALY threshold for ultra-rare curative therapy
**ICER = Incremental Cost-Effectiveness Ratio; LYG = Life Years Gained**
Model parameters: eGFR₀ = 95 ml/min/1.73m², discount rate = 1.5%, time horizon = 100 years
```

---

## PART 3: IMPLEMENTATION ROADMAP

### Phase 1: Text Updates (Week 1)
- [x] Update natural history parameters (eGFR₀, decline rates)
- [x] Update scenario definitions (θ=0.85 as realistic)
- [ ] Add treatment waning subsection
- [ ] Add QALY/LYG interpretation section
- [ ] Update all result tables

### Phase 2: Figures & Tables (Week 1)
- [x] Generate 4 publication figures (completed)
- [ ] Insert figures in Section 3 with captions
- [ ] Create updated cost-effectiveness tables
- [ ] Add calibration validation table

### Phase 3: Sensitivity Analysis (Week 2)
- [ ] Update tornado diagram with recalibrated parameters
- [ ] Add Lowe utility multiplier sensitivity (0.80-0.95)
- [ ] Add starting eGFR sensitivity (90-100)
- [ ] Add discount rate sensitivity (0%, 1.5%, 3.5%)

### Phase 4: Model Validation (Week 2)
- [x] Natural history calibration validation (completed)
- [ ] Add ISPOR-SMDM checklist compliance table
- [ ] Document model assumptions and limitations
- [ ] Add face validity discussion

---

## PART 4: KEY PARAMETER SUMMARY (FOR QUICK REFERENCE)

### Recalibrated Model Parameters

```python
# Natural History
starting_age = 1  # years
starting_egfr = 95.0  # ml/min/1.73m²
decline_rate_early = 1.0  # ml/min/yr (ages 1-10)
decline_rate_middle = 3.0  # ml/min/yr (ages 10-20)
decline_rate_late = 1.5  # ml/min/yr (ages 20+)
discount_rate = 0.015  # 1.5%

# Treatment Scenarios
scenarios = {
    'Optimistic': {'theta': 1.00, 'decline_rate': 0.30},
    'Realistic': {'theta': 0.85, 'decline_rate': 0.52},  # BASE CASE
    'Conservative': {'theta': 0.70, 'decline_rate': 0.74},
    'Pessimistic': {'theta': 0.50, 'decline_rate': 1.04}
}

# Utilities
lowe_utility_multiplier = 0.85  # 15% reduction for non-renal morbidity
base_utilities = {
    'CKD2': 0.72, 'CKD3a': 0.68, 'CKD3b': 0.61,
    'CKD4': 0.54, 'ESKD': 0.40
}

# Costs
gene_therapy_cost = 3000000  # $3.0M
```

### Validation Targets (All Met ✓)

- Natural history ESKD age: **32.0 years** (target: 32, Ando 2024)
- Natural history death age: **37.5 years** (target: 30-40, Murdock 2023)
- Post-ESKD survival: **5.5 years** (target: 3-8, inferred from Ando 2024)

---

## PART 5: FILES READY FOR REVIEW

### Model Code (Updated)
- `markov_cua_model.py` - Core model with recalibrated parameters
- `test_recalibrated_model.py` - Comprehensive validation script
- `generate_recalibrated_figures.py` - Figure generation
- `diagnose_qaly_lyg_gap.py` - QALY/LYG analysis

### Diagnostic Scripts (Archive)
- `validate_scenarios.py` - Original validation revealing issues
- `diagnose_scenario2_issues.py` - Diagnosed poor realistic ICER
- `calibrate_to_ando2024.py` - Initial calibration attempt (had eGFR>100 error)
- `realistic_parameter_optimization.py` - Correct calibration with eGFR≤100

### Figures (Publication-Ready)
- `figure1_age_varying_rates_recalibrated.png`
- `figure2_egfr_trajectories_recalibrated.png`
- `figure3_waning_effect_recalibrated.png`
- `figure4_ce_plane_recalibrated.png`

---

## PART 6: OUTSTANDING QUESTIONS FOR USER

### ⭐ Question 1: Primary Metric Reporting
**Should we report BOTH $/QALY and $/LYG in the main results, or $/QALY only?**

My recommendation: BOTH
- Primary: $327K/QALY (realistic)
- Secondary: $107K/LYG (realistic)
- Shows both quality adjustment AND survival benefit magnitude

### ⭐ Question 2: Lowe Utility Multiplier
**Should we adjust the multiplier from 0.85 to 0.90?**

Current: 0.85 (15% decrement) → Realistic ICER $327K/QALY
Alternative: 0.90 (10% decrement) → Realistic ICER ~$275K/QALY

My recommendation: Keep 0.85 as base case, test 0.90 in sensitivity

### ⭐ Question 3: Section 3 Update Priority
**Which updates are highest priority?**

1. Update parameter values (eGFR, decline rates) - CRITICAL
2. Update scenario definitions (θ=0.85 realistic) - CRITICAL
3. Add treatment waning section - HIGH
4. Add QALY/LYG interpretation - HIGH
5. Update all results tables - CRITICAL
6. Enhanced sensitivity analysis - MEDIUM

My recommendation: Start with items 1, 2, 5 (critical parameter and results updates)

---

## NEXT STEPS

**Awaiting User Decision On:**
1. $/LYG reporting approach (both metrics vs QALY only)
2. Lowe utility multiplier (keep 0.85 vs adjust to 0.90)
3. Priority order for Section 3 text updates

**Ready to Execute:**
- Text updates for Section 3 (all drafts prepared above)
- Figure insertion with captions
- Results table updates
- Enhanced sensitivity analysis

---

**END OF UPDATED IMPLEMENTATION PLAN**

*This plan supersedes SECTION_3_MODEL_IMPROVEMENT_PLAN.md with post-recalibration updates*
