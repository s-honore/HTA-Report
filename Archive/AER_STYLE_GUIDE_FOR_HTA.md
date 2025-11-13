# AMERICAN ECONOMIC REVIEW STYLE GUIDE FOR HTA REPORT

## Purpose
This document synthesizes AER writing style guidelines to adapt the Lowe syndrome HTA report for academic/economic journal publication quality.

---

## I. STRUCTURAL FORMATTING

### A. Section Headings (Traditional Outline Format)

**Major sections:** Roman numerals (I., II., III., IV., etc.)
**First subsections:** Capital letters (A., B., C., etc.)
**Second subsections:** Arabic numerals (1., 2., 3., etc.)
**Third subsections:** Lowercase letters (a., b., c., etc.)

**CRITICAL:** The introductory section receives NO heading. Begin content directly after title/abstract.

**Example Structure:**
```
[TITLE]
[Author byline]
[Abstract - 100 words max]

[Introductory material begins here without "Introduction" heading]

I. Background and Disease Characteristics
   A. Lowe Syndrome Pathophysiology
   B. Natural History
      1. Renal manifestations
      2. Neurological manifestations

II. Epidemiological Framework
   A. Prevalence Estimation Methodology
      1. Zero-Inflated Poisson model
      2. HDI adjustment
   B. Target Population
```

---

## II. WRITING TONE AND STYLE

### A. General Principles

**1. Clarity Above All**
- Avoid jargon; if not in a newspaper regularly, suspect
- Economists value clear, direct writing
- Be taken seriously by using accepted economics writing conventions

**2. Conciseness**
- Change "in order to" → "to"
- Change "whether or not" → "whether"
- Change "is equal to" → "equals"
- Eliminate unnecessary words

**3. Analytical Tone**
- NOT journalistic or opinion-page style
- Present evidence, cite literature
- Explain economic trade-offs analytically
- Avoid casual language or marketing tone

**4. Structure Main Arguments**
- Introduction can mirror newspaper article structure (inverted pyramid)
- Lead with key findings
- Build analytic case systematically

### B. Economics-Specific Language

**Appropriate terms:**
- "We estimate..."
- "The model predicts..."
- "Results suggest..."
- "Controlling for..."
- "The incremental cost-effectiveness ratio..."

**Avoid:**
- "Our amazing findings..."
- "Groundbreaking therapy..."
- Marketing language
- Excessive hedging ("it might possibly perhaps...")

---

## III. CITATIONS AND REFERENCES

### A. Format: Chicago Manual Author-Date

**In-text citations:**
- 1-3 authors: List all names (Smith 2020; Jones and Brown 2019; Smith, Jones, and Lee 2021)
- 4+ authors: First author et al. (Anderson et al. 2020)

**Reference list:**
- 1-10 authors: List all names
- 11+ authors: First seven, then "et al."

**Example citations:**
```
The natural history of Lowe syndrome demonstrates progressive renal decline
(Ando et al. 2024; Zaniew et al. 2018), with median ESKD onset at age 32
(Ando et al. 2024).
```

**Reference list format:**
```
Ando, Taro, Koichi Miura, Tomoko Yabuuchi, et al. 2024. "Long-term Kidney
   Function of Lowe Syndrome: A Nationwide Study of Paediatric and Adult
   Patients." Nephrology Dialysis Transplantation 39 (8): 1360–63.

Cooper, Neil R., Katherine Bartlett, Sarah R. Laramee, et al. 2020.
   "Health State Utility Values in Advanced Chronic Kidney Disease."
   Health and Quality of Life Outcomes 18: 175.
```

### B. Data Sources and Registered Studies

**Must be included in reference list:**
```
USRDS (United States Renal Data System). 2024. "USRDS Annual Data Report:
   Epidemiology of Kidney Disease in the United States." National Institutes
   of Health, National Institute of Diabetes and Digestive and Kidney Diseases.
```

---

## IV. MATHEMATICAL CONTENT

### A. Equations

**Placement:** Separate lines, numbered consecutively at left margin
**Numbering:** Arabic numerals in parentheses: (1), (2), (3)...

**Formatting:**
- Scalars: *italic* (e.g., *eGFR*, *t*, *c*)
- Vectors: **boldface** (e.g., **x**, **β**)
- Matrices: **boldface** (e.g., **X**, **Σ**)
- Sets: script (e.g., 𝒮, 𝒳)

**Example:**
```
The annual eGFR decline follows:

(1)    eGFR_{t+1} = eGFR_t - δ × (1 - θ)

where δ is the natural decline rate and θ is the treatment effect parameter.

The transition probability to ESKD is:

(2)    P(ESKD_t) = 1   if eGFR_t < 15
                 = 0   otherwise
```

**In-text fractions:** Use slash with clear parentheses
- Example: "The ratio (a + b)/(c + d) represents..."
- Complex fractions: Display on separate line

**Blackboard font:** Only for ℝ (real numbers), ℤ (integers), ℕ (natural numbers)

### B. Subscripts and Superscripts

- Must be easily distinguished from regular variables
- Maximum two levels of sub/superscripts
- Example: *x*_{*i*,*t*} acceptable; *x*_{*i*,*t*,*j*}^{*k*,*l*} too complex

---

## V. TABLES

### A. Structure Requirements

**Dimensions:**
- Portrait (vertical) orientation ONLY
- Maximum 9 columns (including row headings)
- Number consecutively with Arabic numerals: Table 1, Table 2, etc.

**Lines:**
- Use ONLY horizontal lines
- Use additional blank space for visual separation
- NO vertical lines
- NO shading or cell fills

**Formatting:**
- Do NOT abbreviate in column headings
- Place zero before decimal: 0.357 not .357
- Panels: Use "Panel A," "Panel B," etc.

### B. Significance Testing

**CRITICAL:** Do NOT use asterisks (*, **, ***) for significance levels

**Correct approach:** Report standard errors in parentheses below estimates

**Example:**
```
Table 1—Base Case Cost-Effectiveness Results

Scenario                        Incremental     Incremental    ICER
                               Cost ($)         QALYs        ($/QALY)

Complete Stabilization         2,258,437        6.879        328,288
                              (245,000)        (0.892)       (42,155)

70% Reduction                  2,515,603        3.939        638,682
                              (268,000)        (0.512)       (78,234)

Notes: Standard errors in parentheses. ICER = incremental cost-effectiveness
ratio. All costs in 2024 USD, discounted at 3.5% annually.
```

### C. Footnotes

**Use lowercase letters** (a, b, c) for table-specific footnotes
**Placement:** Below table
**Order:** Table-specific notes, then source note

**Example:**
```
Notes: Standard errors in parentheses.
^a Treatment effect parameter θ = 1.0 (complete stabilization).
^b Scenario assumes lifelong durability of treatment effect.
Source: Authors' calculations based on Ando et al. (2024) and Wyld et al. (2012).
```

---

## VI. FIGURES

### A. Technical Requirements

**Format:** Vector-based graphics only
- Acceptable: PDF, EPS, AI, WMF, PPT
- NOT acceptable: JPG, PNG, BMP (raster formats)

**Variables in figures:**
- Use *italics* for variables
- Use **boldface** for vectors/matrices
- Maintain mathematical notation consistency

**File naming:**
- Clear labels with panel letters
- Example: Figure1a.pdf, Figure1b.pdf, Figure2.eps

### B. Captions and Notes

**Placement:** Captions go BELOW figures (opposite of tables)

**Example:**
```
[Figure displays here]

Figure 1. Cost-Effectiveness Plane: Gene Therapy vs Natural History

Notes: Each point represents one treatment scenario. Dashed line indicates
$300,000/QALY threshold (NICE HST). QALY = quality-adjusted life year.
Source: Authors' calculations.
```

---

## VII. MANUSCRIPT STRUCTURE

### A. Front Matter

**NO separate title page**
- Title at top of first page
- Author byline immediately below title
- Author affiliations in footnote
- Abstract (100 words max) on first page

**Example:**
```
Cost-Effectiveness of Gene Therapy for Lowe Syndrome:
A Scenario-Based Economic Evaluation

[Author Names]^a

^a [Institution], [Email]

Abstract (100 words): We evaluate the cost-effectiveness of AAV-based
gene therapy for Lowe syndrome, an X-linked disorder causing progressive
kidney failure. Using a Markov cohort model, we estimate incremental
cost-effectiveness ratios under three efficacy scenarios. Complete eGFR
stabilization yields an ICER of $328,288/QALY, within ultra-rare disease
thresholds. Results are sensitive to treatment durability and discount
rates. Our findings suggest gene therapy may be cost-effective under
optimistic scenarios with outcomes-based pricing mechanisms.

[Introductory content begins here without "Introduction" heading]

Lowe syndrome affects approximately 1 in 500,000 individuals...
```

### B. Section Order (Typical Economics Paper)

1. [Introductory material - NO HEADING]
2. I. Background and Institutional Context
3. II. Data and Methodology
4. III. Results
5. IV. Discussion
6. V. Conclusion (or combined with Discussion)
7. References
8. Appendices (if needed)

---

## VIII. SPECIFIC ADAPTATIONS FOR HTA REPORT

### A. Rename Sections to Economics Style

**Current HTA Style → AER Style**

| Current | AER Equivalent |
|---------|----------------|
| Executive Summary | Abstract (100 words, on first page) |
| Section 1: Disease Background | [Introductory material - no heading] |
| Section 2: Epidemiology | I. Epidemiological Framework |
| Section 3: Economic Modeling | II. Methodology<br>   A. Model Structure<br>   B. Parameter Inputs<br>III. Results<br>   A. Base Case<br>   B. Sensitivity Analysis |
| Section 4: Broader Value | IV. Extensions: Broader Value Considerations |
| Section 5: Strategic Landscape | IV. Discussion (subsection B) |
| Section 6: Evidence Development | V. Implications for Future Research |
| Section 7: Conclusions | V. Conclusion |

### B. Condense Content

**HTA report:** 60-80 pages
**AER article:** 30-40 pages typical (including tables/figures)

**Strategy:**
- Move detailed parameter tables to appendix
- Keep main text focused on methodology, key results, interpretation
- Reference appendix tables in main text: "Table A1 in the appendix..."
- Reduce literature review to essential citations only

### C. Adjust Tone

**Remove:**
- "This report is for investor due diligence..."
- "We recommend proceeding with investment..."
- Marketing language about "first-mover advantage"
- Explicit pricing recommendations

**Retain:**
- Analytical findings
- Economic interpretation
- Policy implications
- Scientific uncertainty acknowledgment

**Reframe:**
- "Strategic recommendations" → "Implications for policy and pricing"
- "Investor value proposition" → "Economic considerations for technology adoption"
- "Risk mitigation" → "Uncertainty management in economic evaluation"

---

## IX. DATA AND REPRODUCIBILITY

### A. Data Availability Statement

**Required at end of article:**
```
Data Availability: The code and data underlying this analysis are available
from the authors upon request. The Markov model is implemented in Python and
available at [GitHub repository]. Input parameters are documented in Online
Appendix B.
```

### B. Replication Package

**AER requires:**
- Code to replicate all tables and figures
- Data files (or instructions to obtain restricted data)
- README file with instructions
- Hosted on AEA Data and Code Repository

---

## X. CHECKLIST FOR SECTION 3 REWRITE

### Before Starting:
- [ ] Review Section 3 plan
- [ ] Identify content for main text vs appendix
- [ ] Prepare equation numbering system
- [ ] Plan table formatting (no shading, horizontal lines only)

### Writing:
- [ ] Use Roman numeral section headers (II. for Methodology, III. for Results)
- [ ] Number equations consecutively
- [ ] Format all math: *italics* for scalars, **bold** for vectors
- [ ] Remove asterisks from tables, use standard errors in parentheses
- [ ] Use author-date citations throughout

### Review:
- [ ] Check: No asterisks for significance
- [ ] Check: Zero before decimals (0.357 not .357)
- [ ] Check: Horizontal lines only in tables
- [ ] Check: Captions below figures, above tables
- [ ] Check: Maximum 9 columns per table
- [ ] Check: All equations on separate lines with numbers

---

## XI. EXAMPLE: BEFORE AND AFTER

### BEFORE (HTA Style):
```
**3.6.1 Base Case Results**

Table: Base Case Cost-Effectiveness Results

| Scenario | ICER | p-value |
|----------|------|---------|
| Stabilization | $328,288/QALY | p<0.001*** |
| 70% Reduction | $638,682/QALY | p<0.01** |

*** = p<0.001, ** = p<0.01
```

### AFTER (AER Style):
```
III. Results

A. Base Case Cost-Effectiveness

Table 3 presents the base case cost-effectiveness results for each treatment
scenario relative to natural history.

Table 3—Base Case Cost-Effectiveness Results

Scenario                    Incremental      Incremental      ICER
                           cost ($)          QALYs         ($/QALY)

Complete stabilization     2,258,437         6.879          328,288
                          (245,120)         (0.892)        (42,155)

70 percent reduction       2,515,603         3.939          638,682
                          (268,340)         (0.512)        (78,234)

Notes: Standard errors in parentheses, calculated using delta method with
1,000 bootstrap replications. ICER = incremental cost-effectiveness ratio.
All costs in 2024 USD, discounted at 3.5 percent annually. QALY = quality-
adjusted life year.
```

---

## XII. FINAL REMINDERS

1. **Abstract:** Must be exactly 100 words or fewer
2. **No "Introduction" heading:** Start content directly
3. **Tables:** Horizontal lines only, no shading, no asterisks
4. **Figures:** Vector format required (PDF, EPS)
5. **Citations:** Author-date style (Chicago Manual)
6. **Equations:** Numbered at left margin, *italic* scalars
7. **Tone:** Analytical, clear, avoid jargon
8. **Length:** Aim for 30-40 pages including tables/figures

---

**References for This Style Guide:**
- American Economic Association. "AER Style Guide." https://www.aeaweb.org/journals/aer/style-guide
- Bellemare, Marc F. 2020. "How to Write Applied Papers in Economics." University of Minnesota.
- Chicago Manual of Style, 17th edition. Author-Date System.
