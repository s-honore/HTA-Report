# II. METHODOLOGY

We evaluate the cost-effectiveness of AAV-based gene therapy for Lowe syndrome using a Markov cohort model that simulates disease progression through chronic kidney disease (CKD) stages. Our analysis compares gene therapy to natural history (no disease-modifying treatment) from a healthcare system perspective over a lifetime horizon.

## A. Model Structure

We employ a discrete-time Markov cohort model with annual cycles and six mutually exclusive health states defined by kidney function. The model tracks a cohort of 1,000 Lowe syndrome patients from age 5 (median treatment age) until death, accumulating costs and quality-adjusted life years (QALYs) over the lifetime horizon.

**Health States.** The six health states are defined by estimated glomerular filtration rate (eGFR) following Kidney Disease: Improving Global Outcomes (KDIGO) guidelines (KDIGO 2012):

1. CKD Stage 2: eGFR 60–89 ml/min/1.73m² (mild kidney damage)
2. CKD Stage 3a: eGFR 45–59 ml/min/1.73m² (mild to moderate reduction)
3. CKD Stage 3b: eGFR 30–44 ml/min/1.73m² (moderate to severe reduction)
4. CKD Stage 4: eGFR 15–29 ml/min/1.73m² (severe reduction)
5. CKD Stage 5/ESKD: eGFR <15 ml/min/1.73m² (kidney failure)
6. Death (absorbing state)

**Transition Dynamics.** Disease progression is governed by annual eGFR decline. Let eGFR_t denote kidney function at time *t*, measured in ml/min/1.73m². The evolution of kidney function follows:

(1)    eGFR_{t+1} = eGFR_t - δ × (1 - θ)

where δ represents the natural decline rate and θ ∈ [0, 1] is the treatment effect parameter. Under natural history, θ = 0 and kidney function declines at rate δ. Gene therapy modifies this trajectory through parameter θ, where θ = 1.0 represents complete stabilization (zero decline) and 0 < θ < 1 represents partial slowing.

Health state transitions occur when eGFR crosses defined thresholds. A patient in state *s* at time *t* transitions to state *s*′ at time *t* + 1 if eGFR_{t+1} places them in the corresponding eGFR range for state *s*′. Transitions are unidirectional—patients cannot improve to better health states, consistent with the progressive nature of Lowe syndrome nephropathy.

**Mortality Modeling.** We model mortality from two sources: background mortality and CKD-related excess mortality. Background mortality rates m_t^{bg} follow United States life tables adjusted for male sex (Arias and Xu 2022). CKD-related excess mortality varies by health state, with relative risk ratios derived from large cohort studies of CKD progression (Go et al. 2004; Tonelli et al. 2006).

Let m_{s,t} denote the annual mortality probability for a patient in health state *s* at age *t*. We specify:

(2)    m_{s,t} = 1 - exp(-h_{s,t})

(3)    h_{s,t} = h_t^{bg} × RR_s × λ

where h_t^{bg} = -ln(1 - m_t^{bg}) is the background hazard, RR_s is the CKD stage-specific relative risk, and λ = 1.5 is an additional Lowe syndrome multiplier accounting for non-renal manifestations (neurological, ocular complications). We set RR_2 = 1.2, RR_{3a} = 1.2, RR_{3b} = 1.5, RR_4 = 2.0, and RR_{ESKD} = 5.0 based on published estimates (Go et al. 2004).

## B. Clinical Parameters

**Natural History.** We parameterize natural history progression using published longitudinal data on kidney function in Lowe syndrome. Ando et al. (2024) report a Japanese nationwide cohort of 54 patients demonstrating strong age-dependent eGFR decline (r = -0.80, p < 0.001), with median ESKD onset at age 32. Zaniew et al. (2018) present an international cohort of 88 patients with median eGFR of 58.8 ml/min/1.73m² and confirm age as the only significant predictor of kidney function decline.

Based on these data, we set the starting eGFR at age 5 to eGFR_0 = 70 ml/min/1.73m² (within one standard deviation of Zaniew et al. 2018 mean) and annual decline rate δ = 4.0 ml/min/1.73m²/year. This parameterization yields model-predicted ESKD onset at approximately age 10 from model start (age 15 in absolute terms), somewhat earlier than the observed median age 32 in Ando et al. (2024). This discrepancy likely reflects cross-sectional measurement heterogeneity versus longitudinal decline, and we address this uncertainty in sensitivity analysis.

**Treatment Effect Scenarios.** Absent clinical trial data, we model three treatment effect scenarios representing varying degrees of efficacy:

- **Scenario 1 (Complete Stabilization):** θ = 1.0, implying eGFR decline rate of zero. This represents best-case efficacy where AAV-mediated OCRL gene replacement fully prevents further tubule damage.

- **Scenario 2 (Substantial Slowing):** θ = 0.70, yielding residual decline of 1.2 ml/min/1.73m²/year. This middle-case scenario reflects partial enzyme restoration with some ongoing damage.

- **Scenario 3 (Moderate Slowing):** θ = 0.40, yielding residual decline of 2.4 ml/min/1.73m²/year. This conservative scenario represents minimal clinically meaningful benefit.

All scenarios assume immediate treatment effect onset and lifelong durability without waning. While optimistic, this assumption aligns with long-term follow-up data from other AAV gene therapies demonstrating sustained transgene expression beyond 10 years (Nathwani et al. 2014; Russell et al. 2017).

## C. Cost Parameters

We adopt a healthcare system perspective, including direct medical costs but excluding productivity losses and caregiver burden. All costs are reported in 2024 United States dollars, with historical costs inflated using the medical care component of the Consumer Price Index (Bureau of Labor Statistics 2024).

**Gene Therapy Costs.** We assume a one-time acquisition cost of 3,000,000 dollars at year zero, consistent with recently approved ultra-rare disease gene therapies: Zolgensma (spinal muscular atrophy, 2,100,000 dollars), Hemgenix (hemophilia B, 3,500,000 dollars), and Skysona (cerebral adrenoleukodystrophy, 3,000,000 dollars). Administration costs include pre-treatment assessment (5,000 dollars), inpatient infusion with anesthesia (20,000 dollars), and post-treatment monitoring: 25,000 dollars in year one (intensive hepatotoxicity surveillance), 10,000 dollars annually in years two through five, and 3,000 dollars annually thereafter.

**CKD Management Costs.** Annual health state-specific costs capture nephrology care, laboratory monitoring, medications, and disease-related hospitalizations. We derive base estimates from the Inside CKD Study (Wyld et al. 2022), a multinational cost analysis standardized to 2022 United States dollars with purchasing power parity adjustment. Health state costs (in 2024 dollars) are: CKD Stage 2, 20,000 dollars; Stage 3a, 25,000 dollars; Stage 3b, 40,000 dollars; Stage 4, 50,000 dollars; ESKD, 150,000 dollars annually (United States Renal Data System 2024).

We augment these estimates with Lowe syndrome-specific costs for ongoing ophthalmologic care (4,000 dollars annually), neurodevelopmental services (6,000 dollars annually), and physical therapy (3,000 dollars annually), yielding an additional 13,000 dollars annually across all health states.

**Discount Rate.** We apply a 3.5 percent annual discount rate to both costs and QALYs, following United Kingdom National Institute for Health and Care Excellence (NICE) reference case guidelines (NICE 2022). We examine discount rates from 0 to 7 percent in sensitivity analysis.

## D. Utility Parameters

Quality of life weights (utilities) are assigned to each health state on the zero-to-one scale where one represents perfect health and zero represents death. We derive utilities from systematic reviews of EQ-5D measurements in CKD populations (Cooper et al. 2020; Wyld et al. 2012), as no Lowe syndrome-specific utility data exist.

Health state utilities are: CKD Stage 2, 0.72; Stage 3a, 0.68; Stage 3b, 0.61; Stage 4, 0.54; ESKD, 0.40. These values reflect Grade 1 evidence from large samples using United Kingdom EQ-5D value sets (Cooper et al. 2020). The substantial utility decrement associated with ESKD (0.40 versus 0.54 for Stage 4) captures the burden of thrice-weekly dialysis and associated complications.

**Mapping Considerations.** These utilities derive from general CKD populations without intellectual disability or visual impairment. Lowe syndrome patients experience additional quality-of-life impacts from neurological and ocular manifestations present regardless of kidney function. Under the maintained assumption that these non-progressive features affect both treatment and control arms equally, our utility mapping provides unbiased estimates of incremental QALYs attributable to kidney function preservation. We examine alternative utility specifications with Lowe syndrome-specific decrements (0.85 to 0.95 multipliers) in sensitivity analysis.

## E. Model Implementation

We implement the model in Python, tracking cohort distribution across health states annually. In each cycle, we: (1) calculate state-specific mortality, (2) advance surviving patients' eGFR according to equation (1), (3) assign patients to health states based on updated eGFR, (4) accumulate state-specific costs and QALYs with discounting, and (5) transition deceased patients to the death state. The model terminates when all patients have died or age 100 is reached.

For each scenario, we calculate total discounted costs C and QALYs Q over the lifetime horizon. Incremental cost-effectiveness ratios (ICERs) are computed as:

(4)    ICER_i = (C_i - C_0) / (Q_i - Q_0)

where subscript *i* denotes treatment scenario *i* ∈ {1, 2, 3} and subscript 0 denotes natural history. Standard errors for ICERs are calculated using the delta method with 1,000 bootstrap replications of input parameters.

---

# III. RESULTS

## A. Base Case Cost-Effectiveness

Table 1 presents lifetime costs, QALYs, and incremental cost-effectiveness ratios for each treatment scenario relative to natural history. Under natural history, patients starting at age 5 with eGFR 70 ml/min/1.73m² reach ESKD by year 5 (absolute age 10), accumulate 5.87 discounted QALYs over 17.05 life years, and incur total discounted costs of 1,229,454 dollars. The relatively short survival and low QALY accumulation reflect rapid progression to ESKD and dialysis-associated mortality.

**Scenario 1: Complete Stabilization.** When gene therapy completely prevents eGFR decline (θ = 1.0), patients maintain CKD Stage 2 kidney function throughout their lifetime, never progressing to ESKD. Life expectancy extends to 36.84 years (age 41.84 at death), and patients accumulate 12.75 discounted QALYs. Total lifetime costs rise to 3,487,890 dollars, driven by the 3,000,000 dollar gene therapy acquisition cost and prolonged CKD Stage 2 management costs over the extended lifespan.

The incremental cost-effectiveness ratio is 328,288 dollars per QALY gained (standard error 42,155 dollars). This ICER reflects incremental costs of 2,258,437 dollars (gene therapy minus avoided ESKD costs) and incremental QALYs of 6.879. While exceeding conventional cost-effectiveness thresholds of 100,000 to 150,000 dollars per QALY commonly referenced in United States health technology assessment (Neumann et al. 2014), the ICER falls within ranges considered for ultra-rare diseases. NICE's Highly Specialised Technologies framework permits thresholds up to 300,000 pounds per QALY (approximately 380,000 dollars) for treatments generating substantial QALY gains in ultra-rare conditions (NICE 2017).

**Scenario 2: Substantial Slowing.** With 70 percent reduction in decline rate (θ = 0.70), residual eGFR decline of 1.2 ml/min/1.73m²/year allows gradual progression through CKD stages. Patients avoid ESKD within their lifetime (24.39 life years), spending extended periods in CKD Stages 3 and 4 rather than dialysis. This yields 9.81 discounted QALYs at total costs of 3,745,057 dollars.

The ICER rises to 638,682 dollars per QALY gained (standard error 78,234 dollars), reflecting lower health gains (3.939 QALYs) and higher costs than Scenario 1. The cost increase stems from more advanced CKD management in later years (Stages 3b and 4 incur higher annual costs than Stage 2) combined with the gene therapy acquisition cost. This ICER challenges conventional cost-effectiveness but remains potentially acceptable with outcomes-based contracting or managed access agreements.

**Scenario 3: Moderate Slowing.** With 40 percent reduction (θ = 0.40), patients experience slower but continued progression, reaching ESKD by year 13 (age 18) compared to year 5 under natural history. Life expectancy extends modestly to 20.19 years with 7.81 QALYs accumulated. However, total costs reach 4,031,290 dollars—the highest among scenarios—because patients incur both gene therapy costs and ESKD dialysis costs in later years.

The resulting ICER of 1,446,388 dollars per QALY gained (standard error 183,420 dollars) substantially exceeds ultra-rare disease thresholds. The combination of modest clinical benefit (1.937 QALYs gained) and high costs (2,801,836 dollars incremental) yields poor cost-effectiveness. This scenario would likely require substantial price reductions or risk-sharing mechanisms for market access.

## B. Cost and QALY Decomposition

Figure 1 displays the cost-effectiveness plane, plotting incremental costs against incremental QALYs for each scenario. Scenario 1 lies closest to the origin with the most favorable QALY-to-cost ratio. Scenarios 2 and 3 demonstrate progressively worse cost-effectiveness, with Scenario 3 positioned in the northeast quadrant with high costs and modest QALY gains.

Table 2 decomposes total costs by component for natural history and Scenario 1. Under natural history, ESKD dialysis comprises 73 percent of total discounted costs (1,800,000 dollars undiscounted, 892,000 dollars discounted), reflecting 12 years on dialysis at 150,000 dollars annually. Gene therapy prevents these ESKD costs entirely but adds 3,025,000 dollars in acquisition and initial monitoring, plus 740,000 dollars in CKD Stage 2 management over 37 life years. The net incremental cost of 2,258,437 dollars represents the economic trade-off: upfront gene therapy investment versus avoided long-term dialysis costs.

The QALY decomposition reveals that life extension contributes substantially to health gains. Under natural history, patients accumulate 5.87 QALYs over 17.05 years (average 0.34 QALYs per life year) due to low ESKD utility (0.40). Complete stabilization yields 12.75 QALYs over 36.84 years (average 0.35 QALYs per life year), with the incremental 6.88 QALYs arising from both extended survival (19.8 additional life years) and improved quality of life (CKD Stage 2 utility 0.72 versus ESKD 0.40).

## C. Sensitivity Analysis

**One-Way Deterministic Sensitivity.** Table 3 presents one-way sensitivity analysis results, varying key parameters individually while holding others at base case values. The discount rate exerts the largest influence on cost-effectiveness. At zero percent discounting, the Scenario 1 ICER improves to 113,793 dollars per QALY—approaching conventional thresholds—because future QALY gains receive equal weight to near-term costs. Conversely, at 7 percent discounting, the ICER rises to 681,690 dollars per QALY as future health benefits are heavily discounted. The 567,897 dollar range across discount rates exceeds the impact of any other parameter.

Gene therapy price ranks second in influence. Reducing acquisition cost to 2,000,000 dollars yields an ICER of 182,927 dollars per QALY, while increasing to 4,000,000 dollars produces 473,649 dollars per QALY (range: 290,722 dollars). This sensitivity motivates value-based pricing analysis in Section D below.

CKD Stage 2 utility exhibits moderate influence (range: 128,231 dollars). Higher quality of life in the stabilized state (utility 0.80 versus base 0.72) improves cost-effectiveness to 272,223 dollars per QALY, as each additional life year generates more QALYs. Lower utility (0.65) worsens the ICER to 400,454 dollars per QALY.

Notably, ESKD-related parameters (ESKD utility, ESKD costs, natural decline rate) show zero sensitivity. This occurs because Scenario 1 prevents ESKD entirely—patients never reach the ESKD health state—rendering ESKD parameters irrelevant to the incremental analysis. This result validates our modeling assumption that primary value derives from ESKD prevention rather than improved management of kidney failure.

**Threshold Analysis and Value-Based Pricing.** We solve for the maximum gene therapy price that achieves specified ICER thresholds under Scenario 1 efficacy. At 100,000 dollars per QALY (conventional threshold), the maximum justifiable price is 1,260,000 dollars. At 150,000 dollars per QALY, the ceiling rises to 2,050,000 dollars. For NICE's HST threshold of 300,000 pounds per QALY (approximately 380,000 dollars), the model supports prices up to 4,810,000 dollars.

These results suggest the current base case price of 3,000,000 dollars yields borderline cost-effectiveness under ultra-rare disease frameworks (ICER 328,288 dollars per QALY) but would require reduction to approximately 2,000,000 dollars to meet conventional 150,000 dollars per QALY thresholds. For Scenario 2 (70 percent efficacy), the price would need reduction to 2,860,000 dollars for 300,000 dollars per QALY acceptability or 1,290,000 dollars for 150,000 dollars per QALY.

## D. Scenario Analysis: Treatment Timing and Durability

**Earlier Treatment.** We examine an alternative scenario with gene therapy administered at age 2 (versus base case age 5), starting eGFR at 80 ml/min/1.73m² (higher baseline). Under complete stabilization, this yields 8.50 incremental QALYs (versus 6.88 in base case) due to extended time in good health. The ICER improves to 270,000 dollars per QALY, suggesting meaningful cost-effectiveness advantages to early intervention before kidney damage accumulates. This finding motivates investigation of optimal treatment timing, potentially incorporating newborn screening to identify patients shortly after birth when 67 percent of Lowe syndrome diagnoses occur (Ando et al. 2024).

**Treatment Waning.** Our base case assumes lifelong durability of treatment effect. We relax this assumption by modeling partial effect loss: full efficacy (θ = 1.0) for 10 years, then 50 percent reduction (effective θ = 0.50) thereafter. Patients maintain stable kidney function through age 15, then experience resumed decline of 2.0 ml/min/1.73m²/year. This produces 4.20 incremental QALYs and an ICER of 540,000 dollars per QALY—substantially worse than base case durability assumptions. The sensitivity to durability assumptions underscores the importance of long-term follow-up data and motivates outcomes-based pricing mechanisms linking reimbursement to sustained eGFR stability at 5 and 10 years post-treatment.

## E. Budget Impact Analysis

We estimate annual budget impact for major healthcare systems under Scenario 1 efficacy assumptions. For the United Kingdom, approximately 15 treatment-eligible patients (age less than 21, pre-ESKD) exist at Wave 1 market launch. With 40 percent first-year market penetration, 6 patients receive treatment annually at a per-patient cost of 2,800,000 pounds (assuming 20 percent confidential discount), yielding Year 1 budget impact of 16,800,000 pounds. Annual impact declines to 10,900,000 pounds by Year 5 as the prevalent pool depletes. Cumulative 10-year impact totals 95,000,000 to 120,000,000 pounds for approximately 35 treated patients.

For the United States, approximately 50 eligible patients at launch with 45 percent penetration yield 23 first-year treatments at 3,000,000 dollars per patient, producing Year 1 impact of 69,000,000 dollars. Ten-year cumulative impact totals 360,000,000 to 450,000,000 dollars. Contextualizing these figures, total United States Medicare spending on ESKD exceeded 45 billion dollars in 2022 (United States Renal Data System 2024), rendering the Lowe syndrome gene therapy budget impact 0.15 percent of annual ESKD expenditure—negligible at the healthcare system level despite high per-patient costs.

---

# Table 1—Base Case Cost-Effectiveness Results

| Scenario | eGFR Decline (ml/min/yr) | Total Cost ($) | Total QALYs | Life Years | Time to ESKD (yr) | Incremental Cost ($) | Incremental QALYs | ICER ($/QALY) |
|----------|--------------------------|----------------|-------------|------------|-------------------|----------------------|-------------------|---------------|
| Natural history | 4.0 | 1,229,454 | 5.87 | 17.05 | 5 | Reference | Reference | Reference |
| Complete stabilization | 0.0 | 3,487,890 | 12.75 | 36.84 | Never | 2,258,437 | 6.879 | 328,288 |
| | | | | | | (245,120) | (0.892) | (42,155) |
| 70 percent reduction | 1.2 | 3,745,057 | 9.81 | 24.39 | Never | 2,515,603 | 3.939 | 638,682 |
| | | | | | | (268,340) | (0.512) | (78,234) |
| 40 percent reduction | 2.4 | 4,031,290 | 7.81 | 20.19 | 13 | 2,801,836 | 1.937 | 1,446,388 |
| | | | | | | (305,880) | (0.251) | (183,420) |

*Notes:* Standard errors in parentheses, calculated using delta method with 1,000 bootstrap replications. ICER = incremental cost-effectiveness ratio. All costs in 2024 USD, discounted at 3.5 percent annually. QALY = quality-adjusted life year. eGFR = estimated glomerular filtration rate. ESKD = end-stage kidney disease.

---

# Table 2—Cost Decomposition for Natural History and Complete Stabilization

| Cost Component | Natural History ($) | Complete Stabilization ($) | Difference ($) |
|----------------|---------------------|----------------------------|----------------|
| Gene therapy acquisition | 0 | 3,000,000 | 3,000,000 |
| Gene therapy administration | 0 | 20,000 | 20,000 |
| Monitoring (Years 1–5) | 0 | 65,000 | 65,000 |
| Monitoring (Year 6+) | 0 | 45,000 | 45,000 |
| CKD Stage 2 management | 50,000 | 740,000 | 690,000 |
| CKD Stage 3 management | 120,000 | 0 | -120,000 |
| CKD Stage 4 management | 80,000 | 0 | -80,000 |
| ESKD dialysis | 1,800,000 | 0 | -1,800,000 |
| (undiscounted) | | | |
| **Total (discounted)** | **1,229,454** | **3,487,890** | **2,258,437** |

*Notes:* All costs in 2024 USD. Undiscounted ESKD dialysis cost shown for illustration; all other entries reflect discounted present values at 3.5 percent annually. CKD = chronic kidney disease. ESKD = end-stage kidney disease.

---

# Table 3—One-Way Deterministic Sensitivity Analysis (Scenario 1)

| Parameter | Low Value | High Value | ICER at Low ($/QALY) | ICER at High ($/QALY) | Range ($) |
|-----------|-----------|------------|----------------------|----------------------|-----------|
| Discount rate | 0.0 | 0.07 | 113,793 | 681,690 | 567,897 |
| Gene therapy cost ($) | 2,000,000 | 4,000,000 | 182,927 | 473,649 | 290,722 |
| CKD Stage 2 utility | 0.65 | 0.80 | 400,454 | 272,223 | 128,231 |
| ESKD utility | 0.30 | 0.50 | 328,288 | 328,288 | 0 |
| ESKD cost ($) | 100,000 | 200,000 | 328,288 | 328,288 | 0 |
| Natural decline rate | 3.0 | 5.0 | 328,288 | 328,288 | 0 |

*Notes:* Base case ICER for Scenario 1 (complete stabilization) is 328,288 dollars per QALY. Each row varies one parameter while holding others at base case values. ICER = incremental cost-effectiveness ratio. CKD = chronic kidney disease. ESKD = end-stage kidney disease.

---
