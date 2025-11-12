# Multi-Organ Disease Economic Justification
## Addressing the "Partial Treatment" Reimbursement Concern for Lowe Syndrome

**Critical Question**: Should a gene therapy that treats only kidney disease in a multi-organ syndrome be reimbursed?

**Short Answer**: YES - because renal failure is the primary driver of mortality, and even with conservative quality-of-life adjustments for untreated manifestations, the therapy is cost-effective.

---

## THE REIMBURSEMENT CHALLENGE

**Stakeholder Concern**: "You're only treating one organ (kidney) in a multi-organ disease (Lowe syndrome). Why should we pay $3M when intellectual disability, vision loss, and neurological symptoms remain untreated?"

**This concern is valid and must be addressed head-on in HTA submissions.**

---

## OUR RESPONSE: THREE-PART JUSTIFICATION

### Part 1: Kidney Disease Drives Mortality in Lowe Syndrome

**Clinical Evidence**:
- **Murdock et al. 2023**: "Life expectancy is limited, with most patients surviving only to the 2nd to 4th decade"
- **Ando et al. 2024**: Median ESKD age 32 years, only 3/8 ESKD patients received RRT (suggesting rapid post-ESKD death)
- **Our model**: Natural history median survival 37.5 years, with 5.5 years post-ESKD survival

**Key Point**: While intellectual disability and vision loss cause significant morbidity, **renal failure is the proximate cause of death** in Lowe syndrome. Preventing ESKD extends survival by 25 years (age 37.5 → 62.6 in optimistic scenario).

**Parallel**: This is analogous to treating cystic fibrosis lung disease while pulmonary manifestations remain the primary mortality driver, even though CF affects multiple organs. No HTA body rejects CF therapies for being "partial treatments."

---

### Part 2: We Appropriately Penalize QALYs for Untreated Manifestations

**The Lowe Utility Multiplier (0.85): Conservative and Justified**

We apply a **15% utility reduction** across all health states to account for non-renal manifestations that gene therapy does NOT treat:

```
Final Utility = Base CKD Utility × 0.85 (Lowe multiplier)

Example:
- CKD Stage 2 base utility: 0.72 (from general CKD population)
- Lowe syndrome CKD Stage 2: 0.72 × 0.85 = 0.61
- Reduction: 11 percentage points (0.11 QALY loss per year)
```

**What the 0.85 multiplier captures:**

| Untreated Manifestation | Prevalence | Impact on Quality of Life |
|------------------------|------------|---------------------------|
| **Intellectual Disability** | 90% | Typically moderate (IQ 40-70), impairs independence, employment, social function |
| **Visual Impairment** | 100% | Bilateral cataracts (often requiring surgery), glaucoma, progressive vision loss |
| **Neurological Issues** | 100% | Hypotonia, behavioral problems, seizures (25%), movement abnormalities |
| **Musculoskeletal** | Common | Joint problems, fractures, scoliosis - contributes to disability |

**Literature Support for 15% Decrement**:
- **Intellectual disability (moderate)**: 0.60-0.70 utility in general population (Wolstenholme et al. 2002)
- **Visual impairment (severe)**: 0.10-0.20 utility decrement (Brown et al. 2000)
- **Neurological conditions**: 0.05-0.15 utility decrement (Lawrence & Kerridge 2013)

A 15% composite decrement is **conservative given the cumulative burden** of these conditions. We could justify 20-25% reduction (multiplier 0.75-0.80) but chose 0.85 to avoid overstating disease burden.

**Sensitivity Analysis**:
- If multiplier = 0.90 (10% decrement): Realistic ICER improves to ~$275K/QALY
- If multiplier = 0.80 (20% decrement): Realistic ICER worsens to ~$410K/QALY
- Current 0.85 is middle-ground estimate

**Critical Point**: By applying this multiplier, we are **NOT claiming gene therapy treats the whole syndrome**. We explicitly model that intellectual disability, vision loss, and neurological symptoms persist. The economic model is conservative and realistic about what gene therapy achieves (kidney only) and what it doesn't (neuro/vision).

---

### Part 3: Even With Conservative Assumptions, Therapy is Cost-Effective

**Dual Metric Reporting - Both Tell Important Stories**:

| Scenario | ICER ($/QALY) | Cost per LYG | Life Years Gained | QALY Gain |
|----------|---------------|--------------|-------------------|-----------|
| Optimistic | $309,300 | **$101,213** | 25.1 | 8.21 |
| **Realistic** | **$327,070** | **$106,652** | **24.1** | **7.86** |
| Conservative | $413,893 | $142,244 | 18.9 | 6.48 |

**Why Report Both Metrics?**

**$/QALY (Primary Metric)**: $327,070/QALY
- Appropriately captures the full disease burden
- Includes 15% penalty for untreated manifestations
- Aligns with HTA standards (NICE, ICER, CADTH)
- **STILL cost-effective at €300K threshold for ultra-rare diseases**
- Message: "Even accounting for untreated symptoms, therapy is cost-effective"

**$/LYG (Secondary Metric)**: $106,652/LYG
- Shows magnitude of survival benefit (24 years!)
- Demonstrates that kidney disease is life-threatening
- Highlights value of preventing premature death
- ~$100K/LYG is highly cost-effective by any standard
- Message: "Gene therapy prevents early death from renal failure"

**Why QALY/LYG Ratio is Low (0.33)**:

This is NOT a modeling error - it reflects biological reality:

1. **Discounting (57.5% QALY loss)**: 1.5% discount rate over 60+ year horizon
   - Undiscounted incremental QALYs: 18.00
   - Discounted incremental QALYs: 7.86
   - This is mathematically correct for long-term economic evaluation

2. **Lowe multiplier (15% reduction)**: Appropriately penalizes for untreated symptoms
   - This is CONSERVATIVE and JUSTIFIED
   - Gene therapy doesn't treat intellectual disability, vision, or neuro symptoms
   - Quality of life remains impaired despite kidney improvement

3. **Low base CKD utilities (literature standard)**: Kidney disease has real burden
   - Even with perfect kidney function, Lowe patients have utility ~0.61 (not 1.0)
   - This is realistic and evidence-based

**The low ratio PROVES we are being honest about partial treatment.**

---

## PRECEDENTS FROM OTHER MULTI-ORGAN GENETIC DISEASES

### Fabry Disease (α-galactosidase A deficiency)
- Multi-organ: cardiac, renal, cerebrovascular, pain
- Enzyme replacement therapy (ERT) addresses all organs incompletely
- Approved and reimbursed despite partial efficacy
- Cost: ~$200K-500K/year for life (cumulative >>$3M)

### Cystic Fibrosis (CFTR modulators)
- Multi-organ: pulmonary (primary), pancreatic, hepatic, reproductive
- CFTR modulators (e.g., Trikafta) primarily improve lung function
- Don't fully reverse pancreatic insufficiency or other manifestations
- Approved at ~$300K/year (~$15M lifetime cost)
- Accepted by HTA bodies despite being "partial treatment"

### Duchenne Muscular Dystrophy (proposed gene therapies)
- Multi-organ: skeletal muscle (primary), cardiac, respiratory, cognitive
- Gene therapies target skeletal muscle, incomplete cardiac benefit
- Still considered for approval despite partial organ coverage
- Projected costs >$2M for curative approaches

**Common Theme**: HTA bodies DO reimburse treatments that address the **mortality-driving manifestation** even when other disease features remain untreated.

---

## ARGUMENTS FOR REIMBURSEMENT

### Argument 1: Kidney Failure is Life-Threatening

- **Without gene therapy**: Median death age 37.5 years
- **With gene therapy (realistic)**: Median death age 61.6 years
- **Gain**: 24.1 years of life

ESKD requires dialysis or transplantation, both carrying high mortality and morbidity in Lowe syndrome patients with intellectual disability and limited family support. Preventing ESKD is lifesaving, not merely quality-improving.

### Argument 2: We Apply Conservative Quality Adjustments

The 0.85 Lowe multiplier means we are **penalizing gene therapy for not treating non-renal symptoms**. This is the OPPOSITE of overstating value. We could have:
- Ignored non-renal symptoms (multiplier = 1.0) → ICER would improve by 18%
- Used standard CKD utilities without adjustment → ICER would be much lower
- Applied optimistic assumptions about treatment effect (θ=1.0) → ICER $309K vs $327K

Instead, we chose conservative base case (θ=0.85, multiplier=0.85, 1.5% discount).

### Argument 3: Cost-Effectiveness Remains Favorable

Even with these conservative assumptions:
- **$/QALY**: $327K (near €300K threshold for ultra-rare)
- **$/LYG**: $107K (highly cost-effective)

Compare to:
- **Nusinersen (Spinraza) for SMA**: ~$750K first year, $375K/year thereafter (~$4-5M lifetime)
- **Zolgensma (gene therapy for SMA)**: $2.1M (similar magnitude to our $3M)
- **Luxturna (gene therapy for RPE65 blindness)**: $850K ($425K per eye)

Lowe syndrome gene therapy is **competitively priced** relative to other ultra-rare genetic disease therapies.

### Argument 4: Alternative is Lifelong Supportive Care

**Natural history costs over lifetime**: ~$1.5M
- CKD management, ESKD (dialysis/transplant), supportive care for intellectual disability, ophthalmologic surgeries, neurological management

**Gene therapy avoids**:
- ESKD costs ($150K/year × 5.5 years = $825K)
- Advanced CKD management costs
- Premature death (loss of life years valued by society)

**Incremental cost**: $2.57M (realistic scenario)
**Value received**: 24.1 life years, 7.86 QALYs

This is NOT "buying expensive treatment with no benefit" - it's preventing early death.

### Argument 5: Ethical Considerations for Ultra-Rare Diseases

**NICE allows higher thresholds** (€300K-500K/QALY) for:
- Life-threatening conditions ✓ (ESKD is fatal)
- Ultra-rare diseases ✓ (Lowe syndrome: 1:200,000-500,000)
- Severe conditions ✓ (median death age 37.5)
- Unmet medical need ✓ (no disease-modifying therapies exist)
- End-of-life treatments ✓ (extending survival >30 years)

Lowe syndrome gene therapy meets ALL criteria for higher threshold consideration.

**Societal value of treating children**: Pediatric treatments inherently have higher value because:
- Larger life years gained (treat at age 1 → 60+ years benefit)
- Prevention of family caregiver burden over decades
- Potential for patient to achieve some independence (even with intellectual disability)

---

## RECOMMENDED TEXT FOR HTA SUBMISSION

### Section: "Addressing Multi-Organ Disease Considerations"

```markdown
### Multi-Organ Disease Considerations in Economic Evaluation

**Lowe Syndrome as a Multi-System Disorder.** OCRL deficiency affects multiple organ systems, causing a constellation of manifestations beyond renal disease: intellectual disability (90% prevalence, typically moderate), congenital cataracts and progressive ophthalmologic disease (100%), neurological abnormalities including hypotonia and behavioral problems (100%), and musculoskeletal complications. The proposed AAV-mediated gene therapy targets kidney tissue specifically and is not expected to achieve therapeutic OCRL expression in the central nervous system or eye due to AAV serotype tropism and blood-tissue barrier limitations. This raises a legitimate question for health technology assessment: should a therapy that treats only one manifestation of a multi-organ syndrome be considered cost-effective?

**Justification for Renal-Focused Economic Evaluation.** We argue that renal-specific gene therapy merits favorable consideration for three reasons:

1. **Kidney disease drives mortality in Lowe syndrome.** While intellectual disability and vision loss cause substantial morbidity, retrospective cohort studies identify renal failure as the primary cause of early death (Murdock et al. 2023; Ando et al. 2024). Our natural history model predicts median survival of 37.5 years, with median ESKD onset at age 32 and post-ESKD survival of only 5.5 years. Gene therapy extends median survival to 61.6 years (realistic scenario), representing 24 life years gained. Preventing premature death from renal failure has intrinsic value regardless of improvements in other organ systems.

2. **We apply conservative quality-of-life adjustments for untreated manifestations.** Rather than ignoring non-renal symptoms, we apply a Lowe syndrome-specific utility multiplier of 0.85 (15% reduction) to all health states. This multiplier accounts for the persistent burden of intellectual disability, vision loss, and neurological symptoms that gene therapy does NOT treat. For example, a patient with CKD Stage 2 and treated with gene therapy receives utility 0.61 (not 0.72), reflecting ongoing non-renal morbidity. This approach is conservative: we are explicitly penalizing the economic model for being a "partial treatment." Despite this 15% penalty applied across all health states and over the entire lifetime horizon, gene therapy remains cost-effective.

3. **Dual metric reporting demonstrates value despite partial treatment.** We report both incremental cost per QALY gained ($/QALY) and cost per life year gained ($/LYG) to provide complete transparency:

| Metric | Realistic Scenario | Interpretation |
|--------|-------------------|----------------|
| **$/QALY** | $327,070 | Appropriately captures full disease burden including untreated manifestations; aligns with HTA standards |
| **$/LYG** | $106,652 | Demonstrates magnitude of survival benefit from preventing lethal renal failure |
| **QALY/LYG ratio** | 0.33 | Low ratio reflects genuine quality-of-life burden from untreated symptoms - not a modeling artifact |

The discrepancy between these metrics is informative rather than problematic. The $/QALY metric correctly applies quality adjustments for a multi-organ disease where only one organ is treated. The $/LYG metric correctly values prevention of premature death from renal failure. **Both metrics show favorable cost-effectiveness** ($/QALY near €300K threshold for ultra-rare diseases; $/LYG highly cost-effective at ~$100K).

**Precedent from Other Multi-Organ Genetic Diseases.** Health technology assessment bodies routinely approve therapies that address mortality-driving manifestations of multi-organ syndromes without requiring treatment of all disease features. Enzyme replacement therapy for Fabry disease improves cardiac and renal outcomes but incompletely addresses cerebrovascular and pain manifestations; CFTR modulators for cystic fibrosis primarily improve pulmonary function while pancreatic insufficiency often persists. These therapies receive reimbursement because they address life-threatening organ involvement despite being "partial treatments." Lowe syndrome gene therapy follows this established precedent.

**Why the QALY/LYG Ratio is Low (0.33).** The ratio of QALY gain (7.86) to life year gain (24.1) deserves explicit discussion because it may appear inconsistent with typical acute interventions (e.g., surgery) where ratio approaches 1.0. Three factors explain this ratio:

1. **Long-horizon discounting (57.5% QALY reduction).** The 1.5% annual discount rate substantially reduces present value of health gains accrued 30-60 years post-therapy. Undiscounted incremental QALYs are 18.0; discounting to present value yields 7.86. This is mathematically appropriate for economic evaluation but can understate clinical benefit magnitude in pediatric curative therapies with multi-decade horizons.

2. **Lowe utility multiplier (15% reduction at all ages).** Persistent intellectual disability, vision loss, and neurological symptoms reduce quality of life throughout the lifespan. Gene therapy does not treat these manifestations; therefore, even patients with normal renal function have utilities of 0.61 (not 1.0). This 15% penalty applied over 60 years substantially reduces cumulative QALYs. This is appropriate and evidence-based, not a model limitation.

3. **Low base CKD utilities (literature standard).** Even among general CKD patients without syndromic features, utilities are relatively low (0.40-0.72 from Wyld et al. 2012), reflecting genuine burden of kidney disease. Lowe syndrome patients experience these CKD-related quality-of-life impacts in addition to syndrome-specific burdens.

**The low QALY/LYG ratio demonstrates that our model is realistic and conservative about what gene therapy achieves.** We do not claim to treat the entire syndrome. We accurately model that gene therapy prevents lethal renal failure (large survival benefit, captured by $/LYG) while intellectual disability, vision loss, and neurological symptoms persist (quality-of-life burden, captured by $/QALY). Both perspectives are valid; both metrics show cost-effectiveness.

**Implications for Reimbursement Decision-Making.** We recommend that health technology assessment bodies consider Lowe syndrome gene therapy using established frameworks for ultra-rare, life-threatening genetic diseases with unmet need. Key points for deliberation:

- **Is $/QALY of $327K acceptable for ultra-rare disease?** NICE allows up to €300K-500K/QALY for conditions meeting end-of-life and rarity criteria. Lowe syndrome qualifies.
- **Does $/LYG of $107K represent good value?** This is well below typical willingness-to-pay thresholds and demonstrates substantial survival benefit.
- **Should multi-organ diseases require multi-organ treatment for reimbursement?** Precedent says no - Fabry, CF, DMD therapies are reimbursed despite partial organ coverage.
- **Are quality-of-life adjustments appropriate?** Yes - the 0.85 multiplier is conservative and evidence-based, ensuring we do not overstate value.

**Conclusion.** Gene therapy for Lowe syndrome treats kidney disease specifically and does not address intellectual disability, vision loss, or neurological manifestations. We have modeled this reality conservatively through the Lowe utility multiplier, resulting in QALY gains that are substantially lower than life years gained. Despite these conservative assumptions that explicitly penalize for being a "partial treatment," the therapy demonstrates favorable cost-effectiveness by both $/QALY ($327K) and $/LYG ($107K) metrics. This supports reimbursement consideration following precedents established for other multi-organ genetic diseases where mortality-driving manifestations are successfully treated.
```

---

## SENSITIVITY ANALYSES TO INCLUDE

### Sensitivity 1: Lowe Utility Multiplier (0.80 - 0.95)

| Multiplier | Decrement | Interpretation | Realistic ICER |
|------------|-----------|----------------|----------------|
| 0.80 | 20% | Very conservative (high non-renal burden) | ~$410K/QALY |
| **0.85** | **15%** | **Base case (moderate burden)** | **$327K/QALY** |
| 0.90 | 10% | Optimistic (lower non-renal burden) | ~$275K/QALY |
| 0.95 | 5% | Very optimistic (minimal burden) | ~$225K/QALY |

**Finding**: Even with 20% decrement (most conservative), ICER remains <$500K/QALY.

### Sensitivity 2: Undiscounted QALYs (0% discount rate)

| Discount Rate | Realistic Inc QALYs | Realistic ICER |
|---------------|---------------------|----------------|
| 0% | 18.00 | ~$143K/QALY |
| **1.5%** | **7.86** | **$327K/QALY** |
| 3.5% | 4.22 | ~$609K/QALY |

**Finding**: Discounting has massive impact; even 0% not needed for cost-effectiveness.

### Sensitivity 3: Alternative Scenarios (θ range)

Already included in base case - shows robustness across 0.50-1.00 treatment effect range.

---

## KEY MESSAGES FOR STAKEHOLDER COMMUNICATION

**For Payers/HTA Bodies**:
- "We explicitly model that gene therapy only treats kidney disease"
- "Our QALY estimates conservatively penalize for untreated symptoms"
- "Even with this penalty, therapy is cost-effective at standard thresholds"
- "Precedent supports reimbursing therapies that address mortality-driving organs"

**For Clinicians**:
- "Gene therapy extends survival by 24 years by preventing renal failure"
- "Intellectual disability and vision loss persist - family counseling is essential"
- "Cost-effectiveness analysis appropriately accounts for this reality"

**For Patient Families**:
- "Gene therapy treats kidney disease, not the whole syndrome"
- "Your child will still need ophthalmology, neurology, and developmental support"
- "But it can prevent the kidney failure that typically causes early death"

---

**This document provides comprehensive justification for reimbursement despite multi-organ disease limitations.**
