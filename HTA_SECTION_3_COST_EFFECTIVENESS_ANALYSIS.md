# Section 3: Cost-Effectiveness Analysis

# 3.1 Summary

This section presents the results of a comprehensive health economic evaluation of gene therapy for Lowe syndrome, conducted from a Danish healthcare perspective. The analysis aims to determine the maximum justifiable reimbursement price for this intervention based on established cost-effectiveness thresholds and epidemiological considerations.

## Objective and Scope

The primary objective of this analysis is to establish the maximum justifiable reimbursement price for gene therapy in Lowe syndrome by evaluating the intervention's cost-effectiveness relative to standard care. The evaluation employs a validated disease progression model to project health outcomes and healthcare costs over the patient lifetime (assumed 60-year time horizon from treatment initiation).

## Key Economic Findings

The analysis yields several critical findings regarding the value proposition for gene therapy in Lowe syndrome:

**Reimbursement Value**: Applying a willingness-to-pay threshold of DKK 1.12 million (approx. EUR 150,000) per quality-adjusted life year (QALY) gained, the maximum justifiable reimbursement price is estimated at DKK 10.7 million (approx. EUR 1,440,144) per treatment course. This valuation reflects the health benefits attributable to early intervention in this serious genetic condition.

**Clinical Effectiveness**: The base case analysis demonstrates an incremental gain of 7.72 QALYs per treated patient (11.06 undiscounted life years), with an associated incremental life expectancy gain of 17.45 years. These benefits reflect both the extended survival and improved quality of life achieved through early intervention.

**Cost-Effectiveness**: The mean incremental cost-effectiveness ratio (ICER) derived from probabilistic sensitivity analysis is DKK 992,392 (approx. EUR 133,207) per QALY gained, with a 95 percent confidence interval of DKK 498,079 to DKK 1,539,842 (approx. EUR 66,843 to EUR 206,690). The probability that gene therapy meets the DKK 1.12 million (approx. EUR 150,000) per QALY cost-effectiveness threshold is 70.7 percent, indicating favorable value at the established reimbursement threshold.

**Treatment Timing**: Stratified analysis by age at treatment initiation reveals that earlier intervention (age 1 to 5 years) yields 15 to 20 percent greater health gains compared with delayed treatment (age 10 to 15 years). This finding has important implications for optimal treatment sequencing and reimbursement policy.

## Limitations

The analysis is subject to several key uncertainties, including long-term treatment durability assumptions, extrapolation of survival and quality of life outcomes beyond the clinical trial period, and limited real-world evidence on adverse event rates. These limitations are addressed through comprehensive sensitivity analyses presented in subsequent sections.

## Structure of This Section

The detailed results and methodological underpinnings of this evaluation are presented across the following subsections. Cf. section 3.2 for the methodological approach and the rationale for the disease progression simulation framework. Cf. section 3.3 for the treatment effect scenarios evaluated. Cf. section 3.4 for the base case results and sensitivity analyses. Cf. section 3.5 for the value-based pricing analysis. Cf. section 3.6 for the results of probabilistic sensitivity analysis. Cf. section 3.7 for sub-population analysis stratified by treatment timing. Cf. section 3.8 for integration of findings into conclusions regarding the cost-effectiveness of gene therapy for Lowe syndrome and implications for reimbursement decision-making. Comprehensive technical details regarding model structure, parameter sources, and validation procedures are provided in cf. appendix A.

# 3.2 Methodological Approach

## 3.2.1 The Reimbursement Question

Gene therapy for Lowe syndrome represents a novel intervention at the pre-clinical stage, with limited long-term efficacy data from clinical trials. Against this backdrop of therapeutic uncertainty, the reimbursement question to be addressed is: What is the maximum price the Danish healthcare system should pay for this intervention, given current evidence regarding treatment effectiveness?

Traditional cost-effectiveness analyses typically treat price as a fixed input, deriving incremental cost-effectiveness ratios (ICERs) based on existing therapy costs and efficacy data. However, for emerging therapies with substantial uncertainty around clinical benefit, this approach is inappropriate. Instead, a value-based pricing framework offers a more suitable methodology: we estimate the price threshold at which the therapy becomes cost-effective relative to a given willingness-to-pay (WTP) threshold. This approach allows decision-makers to explicitly consider the relationship between therapeutic value and affordability within the constraints of the Danish healthcare system.

## 3.2.2 Need for Simulation

The absence of clinical trial data in Lowe syndrome necessitated the development of a simulation-based analytical approach. Rather than relying on observed clinical outcomes, we constructed a model-based framework incorporating the best available evidence on disease natural history, expert clinical input regarding treatment mechanisms, and probabilistic characterization of key uncertainties.

Specifically, our approach comprised the following elements:

- **Markov cohort model**: We developed a state-transition model to project long-term disease progression and health outcomes over the lifetime of treated patients.

- **Scenario analysis**: To address uncertainty in treatment effect magnitude, we modeled multiple plausible treatment efficacy scenarios, representing disease slowing rates of 70%, 75%, 82%, and 90% relative to untreated disease progression.

- **Probabilistic sensitivity analysis**: We conducted 1,000 Monte Carlo iterations to quantify and propagate parameter uncertainty throughout the model, generating a distribution of cost-effectiveness outcomes and establishing confidence intervals around key findings.

- **Sub-group analysis**: We stratified analyses by treatment timing, modeling initiation at ages 1, 3, 5, 7, 10, and 15 years to assess how age at intervention influences long-term value.

- **Lifetime disease trajectory**: The model simulates kidney function decline (measured by estimated glomerular filtration rate [eGFR]), progression through chronic kidney disease (CKD) stages, all-cause mortality, cumulative healthcare costs, and quality-adjusted life years (QALYs) accrued over a patient's lifetime.

## 3.2.3 Model Overview (Non-Technical)

The analysis employs a cohort-based Markov model that tracks Lowe syndrome patients through seven mutually exclusive health states based on kidney function level:

- Normal kidney function (eGFR >90 ml/min/1.73m²)
- CKD Stage 2 (eGFR 60-89)
- CKD Stage 3a (eGFR 45-59)
- CKD Stage 3b (eGFR 30-44)
- CKD Stage 4 (eGFR 15-29)
- End-stage kidney disease (ESKD; eGFR <15, including dialysis and transplantation)
- Death

Patients transition between these health states according to disease-specific transition probabilities, which are determined by:

- **Age-specific eGFR decline rates**: Drawing from the natural history of Lowe syndrome, annual kidney function decline varies by age and current CKD stage, with rates ranging from 1.4 to 4.2 ml/min/year depending on disease severity. These estimates were calibrated against published longitudinal follow-up data.

- **Treatment effect**: When therapy is initiated, the rate of kidney function decline is reduced according to the assumed treatment efficacy scenario (70%-90% slowing of disease progression).

- **Stage-specific mortality risks**: Patients transitioning to more advanced CKD stages incur increasing risks of death. Mortality risk in ESKD is substantially elevated, approximately 18-fold higher compared to patients with normal kidney function, reflecting the clinical burden of advanced renal disease.

Each health state is associated with:

- **Annual healthcare costs**: Ranging from DKK 209,000 (approx. EUR 28,000) in early CKD stages to DKK 1,217,000 (approx. EUR 163,000) in ESKD, reflecting increasing resource utilization and complex management requirements as disease advances.

- **Health-related quality of life (utility weights)**: Declining from 0.68 in normal kidney function to 0.40 in ESKD, capturing the progressive impact of kidney disease on patients' functional status and well-being.

- **Caregiver burden**: Recognized and incorporated in the base-case analysis, given the significant care demands associated with Lowe syndrome and advanced kidney disease.

The model employs the following analytical parameters:

- **Cycle length**: 1-year cycles to balance computational tractability with clinical relevance
- **Time horizon**: Lifetime (until death of all cohort members)
- **Discount rate**: 1.5% for both costs and health effects, consistent with Danish health economic guidelines (cf. Danish Medicines Agency guidelines for health economic evaluations)
- **Perspective**: Danish healthcare system and social perspective

For comprehensive technical specifications, including detailed model structure, transition probability calculations, data sources and assumptions, model validation against external data, and sensitivity analyses, the reader is directed to Appendix A.

# 3.3 Treatment Effect Scenarios

Uncertainty in gene therapy efficacy for Lowe syndrome required modeling multiple scenarios representing different degrees of disease modification. These scenarios allowed evaluation of the robustness of findings across a range of plausible treatment effects, reflecting current evidence and clinical expectations for gene therapy in genetic kidney diseases.

The analysis modeled four treatment effect scenarios, each defined by distinct annual estimated glomerular filtration rate (eGFR) decline rates, alongside the natural history baseline:

| Scenario | eGFR Decline Rate | OCRL Enzyme Replacement | Interpretation |
|----------|-------------------|-------------------------|----------------|
| Natural History | 1.4–4.2 ml/min/year (age-dependent) | 0% | No treatment |
| Optimistic | 0.30 ml/min/year | 90% | Substantial functional correction |
| Realistic | 0.52 ml/min/year | 75% | Incomplete but substantial correction (base case) |
| Conservative | 0.74 ml/min/year | 50% | Moderate functional correction |
| Pessimistic | 1.04 ml/min/year | 25% | Minimal functional correction |

*Note: OCRL enzyme replacement percentages represent assumed functional correction of the deficient enzyme in Lowe syndrome. Natural history decline rates based on Danish patient registry data (2015-2024). Treatment effect estimates derived from gene therapy outcomes in related genetic kidney diseases.*

The realistic scenario served as the base case for primary analysis. This scenario assumed OCRL enzyme replacement of 75 percent, representing incomplete but substantial functional correction. This assumption is consistent with outcomes observed in successful gene therapy trials for related genetic kidney diseases. The realistic scenario reflects a middle-ground approach: more conservative than optimistic estimates based on best-case trial outcomes, yet more clinically plausible than pessimistic projections that assume minimal therapeutic benefit. The conservative scenario represents a moderately reduced treatment effect, while the pessimistic scenario reflects minimal benefit above natural disease progression, providing bounds for sensitivity analysis.

Figure 2 presents projected eGFR trajectories across all treatment effect scenarios over a 50-year time horizon from 2024 to 2074 (cf. figure 2), illustrating the temporal impact of differential disease modification rates on estimated kidney function.
