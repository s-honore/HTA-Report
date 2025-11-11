# Lowe Syndrome: Markov Model Parameters
## Ready-to-Use Quantitative Data for Economic Modeling

**Date:** 2025-11-11
**Source:** Ando et al. 2024 (NDT) + Zaniew et al. 2018 (NDT)
**Status:** URGENT - For immediate model implementation

---

## EXECUTIVE SUMMARY - KEY PARAMETERS

| Parameter | Value | Source |
|-----------|-------|--------|
| **Median age at ESKD** | 32 years | Ando 2024 |
| **Life expectancy** | 30-40 years | Literature consensus |
| **Age at steep eGFR decline** | 10 years | Ando 2024 |
| **Baseline eGFR (pediatric)** | 58.8 mL/min/1.73 m² | Zaniew 2018 |
| **Correlation age-eGFR** | r = -0.80 (P<0.0001) | Ando 2024 |
| **Sample size (adults)** | n=19 | Ando 2024 |

---

## SECTION 1: AGE-STRATIFIED CKD PROGRESSION

### Table 1A: CKD Stage Distribution by Age (Ando 2024, n=54)

| Age Group | CKD G2-3 | CKD G4-5 | ESKD (G5) | Sample Size |
|-----------|----------|----------|-----------|-------------|
| **<20 years** | 97% (34/35) | 3% (1/35) | - | n=35 |
| **≥20 years** | 16% (3/19) | 84% (16/19) | - | n=19 |
| **≥30 years** | 0% (0/8) | 100% (8/8) | 67% (6/9)* | n=8-9* |

*Note: 67% ESKD calculated from n=9 patients ≥30 years in separate analysis

### Table 1B: Key Transition Ages

| Milestone | Age (years) | Proportion | Evidence |
|-----------|-------------|------------|----------|
| Onset of glomerular decline | 10 | - | eGFR "deteriorates steeply after 10 years" |
| Progression to G4-5 | 20-30 | 84% by age 20+ | 84% (16/19) adults have G4-5 |
| Universal G4-5 | 30 | 100% | All patients ≥30 have G4-5 |
| Median ESKD onset | 32 | 50% | 8 patients reached ESKD, median age 32 |
| ESKD prevalence in 30+ | 30-40 | 67% | 6/9 patients ≥30 have ESKD |

---

## SECTION 2: BASELINE eGFR VALUES

### Table 2A: eGFR by Disease Subtype (Zaniew 2018, n=106)

| Group | Median eGFR (mL/min/1.73 m²) | IQR/Range | CKD G3-5 | Sample |
|-------|------------------------------|-----------|----------|--------|
| **Lowe Syndrome** | 58.8 | Not reported | 58% moderate-severe | n=88 |
| Dent Disease 2 (comparison) | 87.4 | Not reported | 28% moderate-severe | n=18 |
| **P-value** | <0.01 | - | - | - |

### Table 2B: Estimated eGFR by Age Group (Derived)*

| Age Range | Estimated eGFR Range | CKD Stage | Notes |
|-----------|----------------------|-----------|-------|
| 0-10 years | 70-90 | G1-G2 | Before steep decline |
| 10-20 years | 40-70 | G2-G3 | During steep decline, 97% still G2-3 |
| 20-30 years | 20-40 | G3b-G4 | 84% reach G4-5 |
| 30-40 years | <20 | G4-G5 | 100% G4-5, 67% ESKD (<15) |

*Derived from age-stratified CKD distributions and median eGFR of 58.8 in pediatric cohort

---

## SECTION 3: ANNUAL TRANSITION PROBABILITIES

### Table 3A: Health State Transitions (Model-Ready Estimates)

| From State | To State | Age 0-10 | Age 10-20 | Age 20-30 | Age 30+ |
|------------|----------|----------|-----------|-----------|---------|
| **G1-G2** → G2-G3 | | High | Very High | - | - |
| **G2-G3** → G4-G5 | | Low (~0.3%) | Moderate (~9-10%)** | Very High | 100% |
| **G4-G5** → ESKD | | Very Low | Low | Moderate-High | High (~7-10%/yr)*** |
| **ESKD** → Death | | Low | Low | Moderate | High |

**Annual probability estimated: If 97% remain <G4 by age 20, and decline starts at age 10, approximately 3%/10 years = 0.3%/year before age 10, then accelerating 10-20.

***If 67% reach ESKD by age 30-40, over ~10-year period = ~6.7%/year baseline, higher in later years

### Table 3B: Suggested Model Cycle Transition Probabilities

**RECOMMENDED FOR BASE CASE:**

#### Ages 0-10 years (Early Phase)
- G1-G2 → G2-G3: 0.10 per year
- G2-G3 → G4-G5: 0.003 per year
- G4-G5 → ESKD: 0.01 per year

#### Ages 10-20 years (Steep Decline Phase)
- G1-G2 → G2-G3: 0.25 per year
- G2-G3 → G4-G5: 0.08-0.10 per year
- G4-G5 → ESKD: 0.03 per year

#### Ages 20-30 years (Advanced CKD Phase)
- G2-G3 → G4-G5: 0.15-0.20 per year
- G4-G5 → ESKD: 0.08-0.10 per year
- ESKD → Death: 0.05-0.08 per year

#### Ages 30-40 years (ESKD Phase)
- G2-G3 → G4-G5: 0.25 per year (residual 16%)
- G4-G5 → ESKD: 0.10-0.15 per year
- ESKD → Death: 0.08-0.12 per year

**NOTES FOR MODELER:**
1. These are derived estimates - apply ±30% in sensitivity analysis
2. Should sum to match observed prevalences (84% G4-5 at 20+, 100% at 30+)
3. Consider tunnel states for age-specific transitions
4. Background mortality should be added to all states

---

## SECTION 4: STATISTICAL RELATIONSHIPS

### Table 4: Predictors of eGFR in Multivariate Analysis

| Factor | Ando 2024 | Zaniew 2018 | Significance |
|--------|-----------|-------------|--------------|
| **Age** | Significant (r=-0.80, P<0.0001) | Significant (β=-0.46, P<0.001) | **PRIMARY DRIVER** |
| Nephrocalcinosis | Not significant | Not significant | - |
| Hypercalciuria | Not significant | Not significant | - |
| Proteinuria | Not reported | Not significant | - |
| Genetic factors | Not reported | Localization trend (NS) | - |

**Key Insight:** Age is the only significant predictor - model can focus on age-based progression

---

## SECTION 5: SURVIVAL PARAMETERS

### Table 5A: Survival and Mortality Data

| Parameter | Value | Source |
|-----------|-------|--------|
| **Median age at death** | 30-40 years | Literature consensus |
| **Median age at ESKD** | 32 years | Ando 2024 |
| **Longest survival** | 54 years | Case report |
| **Typical death occurs** | End of 2nd to start of 4th decade | Multiple sources |
| **Life expectancy** | Approximately 30-40 years | Charnas 1991, others |

### Table 5B: Causes of Death (Non-Renal)

| Cause | Frequency | Notes |
|-------|-----------|-------|
| Renal failure | Primary | Most common cause |
| Respiratory illness | Frequent | Important contributor |
| Seizures | Frequent | Neurological complications |
| Infections | Frequent | Immunological factors |

**For Model:** Incorporate age-dependent all-cause mortality increasing after ESKD

---

## SECTION 6: MODEL VALIDATION TARGETS

### Target Outputs Your Model Should Reproduce:

1. **By age 20:**
   - 3% in CKD G4-5
   - 97% in CKD G2-3

2. **By age 20-30:**
   - 84% in CKD G4-5
   - 16% in CKD G2-3

3. **By age 30+:**
   - 100% in CKD G4-5
   - 67% in ESKD (G5)

4. **Median age at ESKD:** 32 years

5. **Median survival:** 30-40 years

6. **eGFR correlation with age:** r = -0.80 (very strong negative)

---

## SECTION 7: SENSITIVITY ANALYSIS PARAMETERS

### Table 7: Parameter Ranges for Probabilistic Sensitivity Analysis

| Parameter | Base Case | Lower Bound (-30%) | Upper Bound (+30%) | Distribution |
|-----------|-----------|-------------------|-------------------|--------------|
| Age at ESKD (median) | 32 years | 22 years | 42 years | Gamma |
| % G4-5 at age 20+ | 84% | 59% | 100% | Beta |
| % ESKD at age 30+ | 67% | 47% | 87% | Beta |
| Annual G2-G3→G4-5 (age 20-30) | 0.15 | 0.11 | 0.20 | Beta |
| Annual G4-G5→ESKD (age 30+) | 0.10 | 0.07 | 0.13 | Beta |
| Life expectancy | 35 years | 30 years | 40 years | Gamma |

**Recommended Distributions:**
- **Proportions/probabilities:** Beta distribution
- **Time-to-event:** Gamma or Weibull distribution
- **Correlation with age:** Fixed at -0.80 (well-established)

---

## SECTION 8: QUALITY OF LIFE CONSIDERATIONS

### Clinical Burden by CKD Stage (For QoL Weighting)

| Stage | Clinical Features | Treatment Burden |
|-------|------------------|------------------|
| **G1-G2** | Fanconi syndrome | Daily supplements (K, PO4, Ca, carnitine), alkalinization |
| **G2-G3** | Above + progressive proteinuria | Increased monitoring, dietary modifications |
| **G4-G5** | Above + uremic symptoms | Pre-dialysis preparation, frequent clinic visits |
| **ESKD** | Above + kidney failure | Dialysis 3x/week OR transplant workup |

**Additional QoL Factors:**
- Congenital cataracts (all patients)
- Intellectual disability (variable severity)
- Seizures (many patients)
- Growth impairment
- Behavioral problems

---

## SECTION 9: STUDY QUALITY ASSESSMENT

### Ando et al. 2024 (Primary Study)

**Strengths:**
- Largest adult Lowe syndrome cohort (n=19)
- Nationwide coverage (Japan)
- Clear age-stratified analysis
- Strong statistical correlation (r=-0.80)
- Multivariate analysis performed
- Recent publication (2024)

**Limitations:**
- Retrospective design
- Relatively small sample (n=54 total)
- Cross-sectional eGFR measurements
- Limited longitudinal follow-up data reported
- Specific annual decline rates not calculated

**Quality Rating:** ⭐⭐⭐⭐ (4/5) - High quality for rare disease

### Zaniew et al. 2018 (Supporting Study)

**Strengths:**
- Large international cohort (n=88 LS patients)
- Includes comparison group (DD2)
- Multivariate analysis
- Specific median eGFR values reported

**Limitations:**
- Pediatric focus only
- Age-specific eGFR not stratified
- Retrospective design

**Quality Rating:** ⭐⭐⭐⭐ (4/5) - High quality for rare disease

---

## SECTION 10: IMPLEMENTATION CHECKLIST

### For Your Markov Model - Step-by-Step

- [ ] **Define Health States:**
  - [ ] CKD G1-G2 (eGFR ≥60)
  - [ ] CKD G2-G3 (eGFR 30-90)
  - [ ] CKD G4-G5 (eGFR 15-29)
  - [ ] ESKD (eGFR <15)
  - [ ] Death

- [ ] **Set Cycle Length:**
  - [ ] Recommended: 1 year (aligns with age-based progression)

- [ ] **Input Transition Probabilities:**
  - [ ] Use Table 3B values as base case
  - [ ] Make age-dependent (use tunnel states or tracker)
  - [ ] Add background mortality by age

- [ ] **Input Baseline Parameters:**
  - [ ] Starting age: Use cohort starting age or model from birth
  - [ ] Starting eGFR: Use age-appropriate value from Table 2B
  - [ ] Starting distribution: Adjust based on age

- [ ] **Set Time Horizon:**
  - [ ] Recommended: Lifetime (40-50 years to capture mortality)
  - [ ] Alternative: 20 years (captures most ESKD onset)

- [ ] **Validation Targets:**
  - [ ] Check model outputs against Section 6 targets
  - [ ] Adjust transition probabilities if needed
  - [ ] Ensure median ESKD age ≈ 32 years

- [ ] **Sensitivity Analysis:**
  - [ ] One-way SA on key parameters (Table 7)
  - [ ] Probabilistic SA with Beta/Gamma distributions
  - [ ] Scenario analysis: early vs. late progression

- [ ] **Calibration:**
  - [ ] If targets not met, calibrate transition probabilities
  - [ ] Ensure clinical plausibility
  - [ ] Document any adjustments

---

## SECTION 11: QUICK REFERENCE - MODEL INPUTS

### Base Case Scenario (Most Likely Values)

```
# Starting Cohort
Age at model entry: 10 years (start of steep decline)
Starting distribution: 95% G2-G3, 5% G1-G2, 0% G4+

# Annual Transition Probabilities (Age 10-20)
P(G1-G2 → G2-G3) = 0.25
P(G2-G3 → G4-G5) = 0.09
P(G4-G5 → ESKD) = 0.03
P(ESKD → Death) = 0.02

# Annual Transition Probabilities (Age 20-30)
P(G2-G3 → G4-G5) = 0.18
P(G4-G5 → ESKD) = 0.09
P(ESKD → Death) = 0.06

# Annual Transition Probabilities (Age 30-40)
P(G2-G3 → G4-G5) = 0.25 (for remaining 16%)
P(G4-G5 → ESKD) = 0.12
P(ESKD → Death) = 0.10

# Key Validation Targets
Target: 84% G4-5 by age 20-30
Target: 67% ESKD by age 30-40
Target: Median ESKD age = 32 years
Target: Median death age = 35 years

# Discount Rate (Standard)
Costs: 3% per year
QALYs: 3% per year
```

---

## SECTION 12: CITATIONS FOR METHODS SECTION

### Primary Reference (Must Cite)

**Ando T, Miura K, Yabuuchi T, Shirai Y, Ishizuka K, Kanda S, Harita Y, Hirasawa K, Hamada R, Ishikura K, Inoue E, Hattori M.** Long-term kidney function of Lowe syndrome: a nationwide study of paediatric and adult patients. *Nephrol Dial Transplant.* 2024 Aug;39(8):1360-1363. doi: 10.1093/ndt/gfae080. PMID: Not yet available.

### Supporting References (Should Cite)

**Zaniew M, Bökenkamp A, Kolbuc M, et al.** Long-term renal outcome in children with OCRL mutations: retrospective analysis of a large international cohort. *Nephrol Dial Transplant.* 2018 Jan 1;33(1):85-94. doi: 10.1093/ndt/gfw350. PMID: 27708066.

**Charnas LR, Bernardini I, Rader D, Hoeg JM, Gahl WA.** Clinical and laboratory findings in the oculocerebrorenal syndrome of Lowe, with special reference to growth and renal function. *N Engl J Med.* 1991 May 9;324(19):1318-25. doi: 10.1056/NEJM199105093241904. PMID: 2017228.

### Example Methods Text

"Natural history data for kidney disease progression in Lowe syndrome were derived from a nationwide Japanese study of 54 patients (Ando et al., 2024), the largest cohort of adult patients reported to date. Age-stratified chronic kidney disease (CKD) stage distributions showed that 84% of patients aged ≥20 years had CKD stages G4-5, increasing to 100% in patients aged ≥30 years, with a median age at end-stage kidney disease (ESKD) of 32 years. The strong negative correlation between age and estimated glomerular filtration rate (eGFR) (r=-0.80, P<0.0001) supported age-based modeling of disease progression. Baseline eGFR values were informed by Zaniew et al. (2018), who reported a median eGFR of 58.8 mL/min/1.73m² in a cohort of 88 Lowe syndrome patients."

---

## CONTACT FOR QUESTIONS

**Primary Study Authors (Ando 2024):**
- For data requests, consider contacting corresponding author through journal
- Institution: Multiple Japanese centers (details in supplementary materials)

**Alternative Experts:**
- Lowe Syndrome Association (patient advocacy group)
- Pediatric nephrology centers with rare disease experience

---

## DOCUMENT METADATA

**Created:** 2025-11-11
**Version:** 1.0
**Status:** Ready for model implementation
**Urgency:** HIGH (deadline tomorrow)
**File Path:** /home/user/HTA-Report/literature/Lowe_Syndrome_Markov_Model_Parameters.md

**Recommended Workflow:**
1. Import Table 3B (transition probabilities) into model
2. Validate against Section 6 targets
3. Run base case analysis
4. Perform sensitivity analysis using Table 7
5. Document using citations in Section 12

**Questions or Issues:**
- Contact study authors for supplementary data
- Consider expert clinical input for validation
- Use sensitivity analysis to address uncertainty

---

**END OF PARAMETER SHEET**
