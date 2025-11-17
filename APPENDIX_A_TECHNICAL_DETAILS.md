# Appendix A: Technical Documentation

## A.1 Model Structure

This appendix provides detailed technical specifications for the Markov cohort model used to evaluate the cost-effectiveness of gene therapy for Lowe syndrome. The model tracks disease progression through chronic kidney disease (CKD) stages based on estimated glomerular filtration rate (*eGFR*) decline, accumulating costs and quality-adjusted life years (QALYs) over the patient lifetime.

### A.1.1 Health State Definitions

The model comprises seven mutually exclusive and collectively exhaustive health states defined by kidney function level. Health state assignment is determined by *eGFR* measured in ml/min/1.73m², following Kidney Disease: Improving Global Outcomes (KDIGO) classification criteria for CKD staging (KDIGO 2012).

**Health State Definitions:**

Let *S* denote the set of health states, where *S* = {Normal, CKD2, CKD3a, CKD3b, CKD4, ESKD, Death}. For patient *i* at time *t*, health state assignment *s*_{*i*,*t*} ∈ *S* is determined by *eGFR*_{*i*,*t*} according to the following classification function:

(1)    *s*_{*i*,*t*} = Normal     if *eGFR*_{*i*,*t*} > 90
              = CKD2       if 60 ≤ *eGFR*_{*i*,*t*} ≤ 90
              = CKD3a      if 45 ≤ *eGFR*_{*i*,*t*} < 60
              = CKD3b      if 30 ≤ *eGFR*_{*i*,*t*} < 45
              = CKD4       if 15 ≤ *eGFR*_{*i*,*t*} < 30
              = ESKD       if *eGFR*_{*i*,*t*} < 15
              = Death      if deceased

where *eGFR*_{*i*,*t*} is the estimated glomerular filtration rate for patient *i* at time *t*.

**State-Specific Characteristics:**

Each health state *s* ∈ *S* is associated with three fundamental parameters: annual healthcare cost *c*_{*s*}, health-related quality of life (utility weight) *u*_{*s*}, and mortality hazard *λ*_{*s*}. Table A.1 presents these parameters for the base case analysis.

**Table A.1—Health State Parameters**

| State | eGFR Range | Utility *u*_{*s*} | Annual Cost *c*_{*s*} (DKK) | Mortality Multiplier |
|-------|------------|-------------------|------------------------------|----------------------|
| Normal | >90 | 0.72 | 209,000 | 1.0 |
| CKD Stage 2 | 60-90 | 0.72 | 209,000 | 1.0 |
| CKD Stage 3a | 45-59 | 0.68 | 265,000 | 1.2 |
| CKD Stage 3b | 30-44 | 0.61 | 417,000 | 1.5 |
| CKD Stage 4 | 15-29 | 0.54 | 521,000 | 2.0 |
| ESKD | <15 | 0.40 | 1,217,000 | 3.0 |
| Death | - | 0.00 | 0 | - |

Notes: DKK = Danish Kroner; 1 EUR ≈ 7.446 DKK. Utility weights from Wyld et al. (2012). Costs include CKD management, medications, monitoring, and dialysis (ESKD state). Mortality multipliers applied to age-specific background mortality rates.

**Clinical Interpretation:**

The Normal state represents preserved kidney function with *eGFR* exceeding 90 ml/min/1.73m². CKD Stages 2 through 4 represent progressive kidney function decline with increasing clinical burden, medication requirements, and comorbidity risk. The ESKD state represents end-stage kidney disease requiring renal replacement therapy (dialysis or transplantation). Death is an absorbing state.

### A.1.2 Markov Cohort Framework

The model employs a discrete-time Markov cohort structure with annual cycle length. Let **M**(*t*) denote the cohort distribution vector at time *t*, where **M**(*t*) = [*m*_{Normal}(*t*), *m*_{CKD2}(*t*), *m*_{CKD3a}(*t*), *m*_{CKD3b}(*t*), *m*_{CKD4}(*t*), *m*_{ESKD}(*t*), *m*_{Death}(*t*)]^T and *m*_{*s*}(*t*) represents the proportion of the cohort in state *s* at time *t*.

**Cohort Evolution:**

The cohort evolves over discrete time periods according to:

(2)    **M**(*t*+1) = **P**(*t*) × **M**(*t*)

where **P**(*t*) is the 7×7 transition probability matrix at time *t*, with element *p*_{*ij*}(*t*) representing the probability of transition from state *i* to state *j* during cycle *t*.

**Initial Distribution:**

The cohort begins at time *t* = 0 with initial distribution **M**(0) determined by the patient's age and baseline *eGFR* at treatment initiation. For a patient aged *a*_{0} years with baseline *eGFR*_{0}, the initial state assignment follows equation (1). The base case analysis assumes treatment initiation at age 5 years with *eGFR*_{0} = 70 ml/min/1.73m², placing all patients initially in CKD Stage 2:

(3)    **M**(0) = [0, 1, 0, 0, 0, 0, 0]^T

where the vector elements correspond to [Normal, CKD2, CKD3a, CKD3b, CKD4, ESKD, Death]^T.

**Time Horizon:**

The model employs a lifetime time horizon, defined as *T* = 100 cycles (years), sufficient to capture mortality for all cohort members. The time horizon extends from treatment initiation at age *a*_{0} until age *a*_{0} + *T*, ensuring complete follow-up through death for all patients.

**Markov Assumption:**

The model satisfies the Markov property: future states depend only on the current state and time, not on prior disease history. Formally, for patient *i*:

(4)    P(*s*_{*i*,*t*+1} | *s*_{*i*,*t*}, *s*_{*i*,*t*-1}, ..., *s*_{*i*,0}) = P(*s*_{*i*,*t*+1} | *s*_{*i*,*t*}, *t*)

where time *t* serves as a proxy for age, capturing age-dependent disease progression and mortality risk.

### A.1.3 Transition Dynamics

Transitions between health states are determined by two mechanisms: *eGFR*-driven disease progression and mortality. These processes operate sequentially within each annual cycle.

**eGFR Decline Model:**

Kidney function declines according to a linear annual decline rate *δ* (ml/min/1.73m²/year). For patient *i* in the natural history (untreated) scenario:

(5)    *eGFR*_{*i*,*t*+1} = *eGFR*_{*i*,*t*} - *δ*

where *δ* represents the annual *eGFR* decline rate. The base case natural history assumes *δ* = 4.0 ml/min/1.73m²/year, calibrated to achieve median ESKD onset at age 32 years, consistent with Ando et al. (2024).

**Treatment Effect:**

Gene therapy modifies the *eGFR* decline rate through treatment effect parameter *θ* ∈ [0, 1], representing the proportional reduction in decline rate:

(6)    *eGFR*_{*i*,*t*+1} = *eGFR*_{*i*,*t*} - *δ* × (1 - *θ*)

where *θ* = 0 represents no treatment effect (natural history), *θ* = 0.70 represents 70 percent reduction in decline rate, and *θ* = 1.0 represents complete stabilization (zero decline). The base case realistic scenario assumes *θ* = 0.75, corresponding to annual decline of 0.52 ml/min/1.73m²/year.

**State Transition Probabilities:**

Given *eGFR* decline, transition probabilities from state *i* to state *j* are deterministic for disease progression:

(7)    *p*_{*ij*}(*t*) = 1    if *eGFR*_{*t*+1} ∈ Range(*j*) and *eGFR*_{*t*} ∈ Range(*i*)
                   = 0    otherwise

where Range(*s*) denotes the *eGFR* interval [*lower*_{*s*}, *upper*_{*s*}] defining state *s* according to equation (1). This deterministic assignment ensures that patients transition to the appropriate CKD stage based on their updated *eGFR* value.

**Mortality Transitions:**

All non-death states face positive probability of transition to death. The annual mortality probability for state *s* at age *a* is:

(8)    *p*_{*s*,Death}(*a*) = 1 - exp(-*λ*_{*s*}(*a*))

where *λ*_{*s*}(*a*) is the state-specific mortality hazard at age *a*, defined as:

(9)    *λ*_{*s*}(*a*) = *λ*_{0}(*a*) × *r*_{*s*}

where *λ*_{0}(*a*) is the age-specific background mortality rate from Danish life tables and *r*_{*s*} is the mortality multiplier for state *s* (Table A.1). Background mortality increases exponentially with age:

(10)   *λ*_{0}(*a*) = *λ*_{base} × exp(*γ* × *a*)

where *λ*_{base} = 0.0001 (baseline hazard at age 0) and *γ* = 0.08 (annual hazard growth rate).

**Transition Probability Matrix:**

The complete transition probability matrix **P**(*t*) at time *t* (corresponding to age *a* = *a*_{0} + *t*) has the structure:

(11)   **P**(*t*) = [**P**_{progression}(*t*)] × [1 - **p**_{mortality}(*t*)] + [**P**_{mortality}(*t*)]

where **P**_{progression}(*t*) contains *eGFR*-driven transition probabilities (equation 7), **p**_{mortality}(*t*) is the vector of state-specific mortality probabilities (equation 8), and **P**_{mortality}(*t*) is a matrix with death transitions.

**No Backward Transitions:**

The model structure prohibits transitions to states with higher *eGFR* (kidney function improvement), reflecting the irreversible progressive nature of Lowe syndrome nephropathy. Formally:

(12)   *p*_{*ij*}(*t*) = 0    for all *i*, *j* where *eGFR* range of *j* > *eGFR* range of *i*

This constraint ensures clinical plausibility and aligns with natural history evidence from Ando et al. (2024) and Zaniew et al. (2018).

### A.1.4 Time Horizon and Cycle Length

**Cycle Length:**

The model employs annual (1-year) cycles, balancing computational tractability with clinical relevance for chronic disease progression. Annual cycles align with:

1. Clinical monitoring intervals for CKD patients
2. Typical *eGFR* measurement frequency in Lowe syndrome management
3. Annual periodicity of healthcare costs and utility assessments
4. Standard practice in cost-effectiveness analysis of chronic kidney disease (NICE 2022)

**Time Horizon:**

A lifetime time horizon (*T* = 100 years) ensures capture of all relevant costs and health outcomes. The time horizon extends from treatment initiation at age *a*_{0} until age *a*_{0} + 100, by which point survival probability approaches zero for all cohort members.

**Justification for Lifetime Horizon:**

Lowe syndrome patients treated in early childhood (age 1-5 years) may survive 40-50 years with successful intervention. The extended time horizon captures:

1. Long-term treatment durability effects
2. Delayed or prevented ESKD onset
3. Extended survival and quality of life
4. Full lifetime cost offsets from avoided dialysis and transplantation

Sensitivity analysis examines time horizons of 20, 40, and 60 years (Appendix A.3).

**Discounting:**

Future costs and QALYs are discounted to present value using annual discount rate *r*. For outcomes at time *t*, the discount factor is:

(13)   *d*_{*t*} = (1 + *r*)^(-*t*)

The base case applies *r* = 0.015 (1.5 percent annually) for both costs and health effects, consistent with Danish health economic guidelines (Danish Medicines Agency 2024). Sensitivity analysis examines discount rates from 0 to 5 percent.

**Total Discounted Outcomes:**

Total discounted QALYs and costs are calculated as:

(14)   QALY_{total} = Σ_{*t*=0}^{*T*} *d*_{*t*} × Σ_{*s*∈*S*} *m*_{*s*}(*t*) × *u*_{*s*}

(15)   Cost_{total} = Σ_{*t*=0}^{*T*} *d*_{*t*} × Σ_{*s*∈*S*} *m*_{*s*}(*t*) × *c*_{*s*}

where *m*_{*s*}(*t*) is the proportion of cohort in state *s* at time *t*, *u*_{*s*} is the utility weight for state *s*, and *c*_{*s*} is the annual cost for state *s*.

### A.1.5 Half-Cycle Correction

The discrete-time Markov model assumes all transitions occur at cycle boundaries. In reality, transitions occur continuously throughout each cycle. Half-cycle correction adjusts for this discrete approximation by assigning transitions average value across the cycle.

**Half-Cycle Correction Method:**

The model applies the standard half-cycle correction approach, adjusting costs and QALYs accrued in each cycle by assuming transitions occur on average at the cycle midpoint. For time *t*, the corrected cohort distribution for outcome accumulation is:

(16)   **M**_{corrected}(*t*) = 0.5 × [**M**(*t*) + **M**(*t*+1)]

The correction applies to all cycles except the initial cycle (*t* = 0) and final cycle (*t* = *T*), where half weighting is applied:

(17)   QALY_{total} = 0.5 × *d*_{0} × Σ_{*s*∈*S*} *m*_{*s*}(0) × *u*_{*s*}
                     + Σ_{*t*=1}^{*T*-1} *d*_{*t*} × Σ_{*s*∈*S*} [0.5 × (*m*_{*s*}(*t*) + *m*_{*s*}(*t*+1))] × *u*_{*s*}
                     + 0.5 × *d*_{*T*} × Σ_{*s*∈*S*} *m*_{*s*}(*T*) × *u*_{*s*}

with analogous correction for total costs.

**Impact of Half-Cycle Correction:**

The half-cycle correction typically increases total QALYs and costs by 3-5 percent compared to uncorrected calculations, with larger impact when state transitions are frequent. For Lowe syndrome with gradual *eGFR* decline (4.0 ml/min/year from baseline 70 ml/min/1.73m²), transitions occur approximately every 2-3 years, yielding moderate correction impact.

**Alternative Correction Methods:**

The half-cycle correction represents a first-order approximation. Higher-order methods (Simpson's rule, trapezoid rule with substeps) yield similar results but increase computational complexity. Sensitivity analysis confirms that alternative correction methods produce ICERs within 2 percent of the base case half-cycle correction (Appendix A.3).

**Mathematical Justification:**

Let *f*(*t*) represent the instantaneous rate of outcome accrual at time *t* within a cycle. The true integral over cycle [*t*, *t*+1] is:

(18)   ∫_{*t*}^{*t*+1} *f*(*τ*) dτ

The half-cycle correction approximates this integral using the trapezoid rule:

(19)   ∫_{*t*}^{*t*+1} *f*(*τ*) dτ ≈ 0.5 × [*f*(*t*) + *f*(*t*+1)]

This approximation introduces error of order *O*(Δ*t*³) for smooth functions *f*, where Δ*t* = 1 year. Given gradual disease progression, the approximation error is negligible relative to parameter uncertainty.

---

**References**

Ando T, Miura K, Yabuuchi T, Ichikawa D, Yamamoto T, Ashida A. 2024. "Long-term Kidney Function of Lowe Syndrome: A Nationwide Study of Paediatric and Adult Patients." *Nephrology Dialysis Transplantation* 39 (8): 1360–63.

Danish Medicines Agency. 2024. "Guidelines for Health Economic Evaluations in Denmark." Copenhagen: Danish Medicines Agency.

KDIGO (Kidney Disease: Improving Global Outcomes). 2012. "KDIGO Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease." *Kidney International Supplements* 3 (1): 1–150.

NICE (National Institute for Health and Care Excellence). 2022. "NICE Health Technology Evaluations: The Manual." Process and methods PMG36. London: NICE.

Wyld M, Morton RL, Hayen A, Howard K, Webster AC. 2012. "A Systematic Review and Meta-Analysis of Utility-Based Quality of Life in Chronic Kidney Disease Treatments." *American Journal of Kidney Diseases* 60 (2): 253–65.

Zaniew M, Bökenkamp A, Kołbuc M, La Scola C, Baronio F, Niemirska A, Szczepańska M, Peco-Antić A, Paripović D, Besouw M, Klaus G, Hyla-Klekot L, Konrad M, Emma F. 2018. "Long-Term Renal Outcome in Children with OCRL Mutations: Retrospective Analysis of a Large International Cohort." *Nephrology Dialysis Transplantation* 33 (1): 85–94.
