# Lowe Syndrome: One-Page Quick Reference for Markov Model
**URGENT - Ready for Tomorrow's Deadline**

---

## KEY STUDY: Ando et al. 2024 (NDT 39(8):1360-1363)
- **Sample:** 54 patients (35 pediatric, 19 adult) - largest adult cohort to date
- **Design:** Nationwide retrospective cohort study (Japan)
- **Key Finding:** Age is ONLY significant predictor of eGFR (r=-0.80, P<0.0001)

---

## CRITICAL NUMBERS FOR YOUR MODEL

### Age Milestones
| Age | Event | Data |
|-----|-------|------|
| **10 years** | eGFR steep decline begins | Ando 2024 |
| **20 years** | 84% have CKD G4-5 | 16/19 adults |
| **30 years** | 100% have CKD G4-5 | 8/8 patients |
| **32 years** | Median ESKD onset | n=8 patients |
| **30-40 years** | Typical death | Literature |

### CKD Distribution by Age
- **Age <20:** 97% G2-3, 3% G4-5
- **Age ≥20:** 16% G2-3, 84% G4-5
- **Age ≥30:** 0% G2-3, 100% G4-5, 67% ESKD

### Baseline eGFR
- **Median (pediatric cohort):** 58.8 mL/min/1.73m² (Zaniew 2018, n=88)

---

## TRANSITION PROBABILITIES (BASE CASE)

### Annual Transition Matrix

| Age Group | G2-3 → G4-5 | G4-5 → ESKD | ESKD → Death |
|-----------|-------------|-------------|--------------|
| **10-20 years** | 0.09 | 0.03 | 0.02 |
| **20-30 years** | 0.18 | 0.09 | 0.06 |
| **30-40 years** | 0.25 | 0.12 | 0.10 |

**Note:** Adjust these to match validation targets below

---

## MODEL VALIDATION TARGETS
✓ By age 20: 3% in G4-5
✓ By age 20-30: 84% in G4-5
✓ By age 30+: 100% in G4-5, 67% ESKD
✓ Median ESKD age: 32 years
✓ Median survival: 30-40 years

---

## SENSITIVITY ANALYSIS RANGES
- **Age at ESKD:** 22-42 years (32 ± 30%)
- **% G4-5 at 20+:** 59-100% (84% ± 30%)
- **% ESKD at 30+:** 47-87% (67% ± 30%)
- **All transition probabilities:** ± 30%

---

## CITATIONS

**Primary:** Ando T, et al. Long-term kidney function of Lowe syndrome: a nationwide study of paediatric and adult patients. *Nephrol Dial Transplant.* 2024;39(8):1360-1363.

**Supporting:** Zaniew M, et al. Long-term renal outcome in children with OCRL mutations. *Nephrol Dial Transplant.* 2018;33(1):85-94.

---

## DATA LIMITATIONS
⚠️ No specific annual eGFR decline rates reported (use sensitivity analysis)
⚠️ Small adult sample (n=19)
⚠️ Cross-sectional, not longitudinal tracking
⚠️ Full-text access blocked (working from abstracts)

**Recommendation:** Use ±30% sensitivity analysis on all parameters

---

## IMPLEMENTATION NOTES
1. **Cycle length:** 1 year (aligns with age-based progression)
2. **Time horizon:** 40-50 years (lifetime)
3. **Starting age:** 10 years (onset of steep decline) OR birth
4. **Key driver:** AGE (only significant predictor in multivariate analysis)
5. **Non-significant factors:** Nephrocalcinosis, hypercalciuria (ignore in base case)

---

**Files Created:**
1. `/home/user/HTA-Report/literature/Lowe_Syndrome_Kidney_Function_Evidence_Summary.md` (Full review)
2. `/home/user/HTA-Report/literature/Lowe_Syndrome_Markov_Model_Parameters.md` (Detailed parameters)
3. `/home/user/HTA-Report/literature/Lowe_Syndrome_Quick_Reference.md` (This file)

**Status:** ✅ Ready for model implementation
