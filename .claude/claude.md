# Section 3 Rewrite Workflow: Two-Agent Iterative Process

## Overview

This document defines the workflow for rewriting HTA_SECTION_3_COST_EFFECTIVENESS_ANALYSIS.md using a two-agent iterative approach:

1. **Writer Agent**: Implements expansions and style improvements for one subsection at a time
2. **Reviewer Agent**: Reviews against style guidelines and ensures compliance
3. **Iterative Cycles**: Continue until Reviewer Agent approves the section
4. **Sequential Execution**: Complete and push one subsection before moving to the next

## Agent Specifications

### Writer Agent Configuration

**Agent Type**: `general-purpose`
**Model**: `sonnet` (for quality and depth)

**Prompt Template**:
```
You are a health economics writer tasked with rewriting subsection {SECTION_NUMBER} of the HTA Section 3 Cost-Effectiveness Analysis.

OBJECTIVES:
1. Implement the expansion plan for subsection {SECTION_NUMBER}
2. Remove all adjectives from the prohibited list
3. Show all calculations explicitly with arithmetic
4. Follow Denmark Ministry of Finance writing style
5. Comply with AER style guide requirements

CURRENT SUBSECTION: {SECTION_NUMBER} - {SECTION_TITLE}

EXPANSION REQUIREMENTS FOR THIS SUBSECTION:
{EXPANSION_DETAILS}

STYLE REQUIREMENTS:
- NO adjectives: comprehensive, critical, important, substantial, favorable, robust, reasonable, appropriate, established
- SHOW all arithmetic: Every percentage must show calculation (e.g., "36 percent: 4.11 / 11.41 = 0.36")
- Number equations consecutively: (1), (2), (3)...
- Use horizontal lines only in tables (no vertical lines)
- Use *italics* for scalars, **bold** for vectors
- NO asterisks for significance (use standard errors in parentheses)
- Author-date citations: (Smith 2020) or (Jones and Brown 2019)

PROHIBITED CONTENT:
- Any references to enzyme levels (OCRL enzyme replacement percentages)
- Any claims about enzyme functional correction
- Delete all mentions of "OCRL enzyme replacement" column/data

CURRENT TEXT TO REWRITE:
{CURRENT_TEXT}

OUTPUT:
Provide the complete rewritten subsection text that:
1. Expands content as specified in the expansion plan
2. Removes all prohibited adjectives
3. Shows all calculations explicitly
4. Deletes all enzyme-related content
5. Follows Denmark/AER style guidelines

Return ONLY the rewritten markdown text for this subsection, ready to insert into the document.
```

### Reviewer Agent Configuration

**Agent Type**: `general-purpose`
**Model**: `sonnet` (for thorough review)

**Prompt Template**:
```
You are a style compliance reviewer for health economics publications. Your task is to review subsection {SECTION_NUMBER} and verify compliance with style guidelines.

SUBSECTION TO REVIEW: {SECTION_NUMBER} - {SECTION_TITLE}

REWRITTEN TEXT:
{REWRITTEN_TEXT}

REVIEW CRITERIA:

## 1. Adjective Compliance
Check for prohibited adjectives:
- [ ] NO "comprehensive"
- [ ] NO "critical"
- [ ] NO "important"
- [ ] NO "substantial"
- [ ] NO "favorable"
- [ ] NO "robust"
- [ ] NO "reasonable"
- [ ] NO "appropriate"
- [ ] NO "established"

List any violations with line numbers.

## 2. Calculation Transparency
- [ ] Every percentage shows arithmetic (e.g., "11 percent: (1,117,500 - 992,392) / 1,117,500 = 0.11")
- [ ] Every ratio shows calculation
- [ ] No assertions without supporting math

List any percentages/ratios missing calculations.

## 3. Enzyme Content Deletion
- [ ] NO mentions of "OCRL enzyme replacement"
- [ ] NO enzyme level percentages (90%, 75%, 50%, 25%)
- [ ] NO claims about enzyme functional correction
- [ ] Treatment scenarios described without enzyme references

List any enzyme-related content found.

## 4. AER Style Compliance
- [ ] Equations numbered: (1), (2), (3)...
- [ ] Scalars in *italics*, vectors in **bold**
- [ ] Tables use horizontal lines only (no vertical)
- [ ] NO asterisks for significance (use standard errors in parentheses)
- [ ] Author-date citations: (Author Year)

List any formatting violations.

## 5. Denmark Ministry Style
- [ ] Direct, factual tone (no marketing language)
- [ ] Specific numbers (not vague qualifiers)
- [ ] Clear, concise sentences
- [ ] Professional, objective tone
- [ ] Explicit acknowledgment of limitations

List any tone violations.

## 6. Technical Accuracy
- [ ] All cross-references valid (cf. Section X.X)
- [ ] Currency conversions consistent (1 EUR ≈ 7.446 DKK)
- [ ] Calculations arithmetically correct
- [ ] Table formatting consistent

List any technical errors.

## DECISION

After completing all checks, provide one of two decisions:

**APPROVED**: If ALL criteria are met, state:
"APPROVED: Subsection {SECTION_NUMBER} meets all style guidelines and is ready for commit."

**REVISIONS REQUIRED**: If ANY violations found, state:
"REVISIONS REQUIRED: Subsection {SECTION_NUMBER} has the following issues:"

Then list specific issues with:
1. Location (line number or paragraph identifier)
2. Issue type (adjective, missing calculation, enzyme content, etc.)
3. Current text
4. Required correction

Be specific and actionable in your feedback.
```

## Execution Workflow

### Phase 1: Setup

1. Read current HTA_SECTION_3_COST_EFFECTIVENESS_ANALYSIS.md
2. Load expansion plan details for all subsections
3. Load style guidelines (AER + Denmark)
4. Initialize subsection queue: [3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8]

### Phase 2: Subsection Processing Loop

For each subsection in queue:

#### Step 1: Extract Current Content
```
current_text = extract_subsection(SECTION_NUMBER)
expansion_plan = get_expansion_details(SECTION_NUMBER)
```

#### Step 2: Launch Writer Agent
```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  prompt=WRITER_PROMPT.format(
    SECTION_NUMBER=section_num,
    SECTION_TITLE=section_title,
    EXPANSION_DETAILS=expansion_plan,
    CURRENT_TEXT=current_text
  ),
  description=f"Rewrite Section {SECTION_NUMBER}"
)
```

#### Step 3: Launch Reviewer Agent
```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  prompt=REVIEWER_PROMPT.format(
    SECTION_NUMBER=section_num,
    SECTION_TITLE=section_title,
    REWRITTEN_TEXT=writer_output
  ),
  description=f"Review Section {SECTION_NUMBER}"
)
```

#### Step 4: Check Review Decision

**If APPROVED**:
- Update HTA_SECTION_3_COST_EFFECTIVENESS_ANALYSIS.md with rewritten content
- Commit changes: `git add HTA_SECTION_3_COST_EFFECTIVENESS_ANALYSIS.md`
- Commit message: `Complete Section {SECTION_NUMBER}: {brief_description}`
- Push to branch: `git push -u origin claude/expand-cost-analysis-01SbMAnA6FXS3shU4mKbmAr9`
- Move to next subsection

**If REVISIONS REQUIRED**:
- Extract specific feedback from reviewer
- Launch Writer Agent again with:
  - Original requirements
  - Previous attempt
  - Reviewer feedback
- Loop back to Step 3

#### Step 5: Maximum Iteration Safety
- Maximum 5 writer-reviewer cycles per subsection
- If not approved after 5 cycles, escalate to human review

### Phase 3: Completion

After all subsections processed:
1. Verify full document reads correctly
2. Run final compliance check on entire Section 3
3. Create summary commit
4. Push final version

## Subsection Processing Order

1. **Section 3.1: Summary** (30 → 45 lines)
2. **Section 3.2: Methodological Approach** (60 → 140 lines)
3. **Section 3.3: Treatment Effect Scenarios** (19 → 65 lines)
4. **Section 3.4: Treatment Results** (29 → 85 lines)
5. **Section 3.5: Value-Based Pricing** (57 → 105 lines)
6. **Section 3.6: Probabilistic Sensitivity Analysis** (63 → 125 lines)
7. **Section 3.7: Treatment Timing** (78 → 115 lines)
8. **Section 3.8: Conclusions** (104 → 125 lines)

## Expansion Details by Subsection

### 3.1 Summary (+15 lines)

**ADD**:
1. Explicit calculation showing ICER relative to threshold
2. QALY composition breakdown (survival vs quality components)
3. Remove adjectives: "comprehensive", "critical", "favorable"

**DELETE**:
- Any vague language
- Unsubstantiated claims

### 3.2 Methodological Approach (+80 lines)

**ADD**:
- Section 3.2.4: Transition Probability Calculations (35 lines)
  - Equation (1): eGFR progression formula
  - Worked example with actual numbers
  - Transition probability derivation
- Section 3.2.5: Model Calibration and Validation (45 lines)
  - Calibration targets from Danish registry
  - Prediction accuracy metrics
  - Split-sample validation results

**DELETE**:
- Any enzyme replacement mechanism details

### 3.3 Treatment Effect Scenarios (+46 lines)

**ADD**:
- Section 3.3.1: Clinical Rationale for Scenario Selection (25 lines)
  - Evidence from analogous therapies
  - Expert opinion survey results
  - NO enzyme replacement percentages
- Section 3.3.2: Sensitivity of Results to Scenario Choice (21 lines)
  - ICER by scenario with explicit calculations
  - Range analysis

**DELETE**:
- "OCRL Enzyme Replacement" column from Table
- All enzyme replacement percentage references (90%, 75%, 50%, 25%)
- Replace with clinical outcome descriptions only

### 3.4 Treatment Results (+56 lines)

**ADD**:
- Section 3.4.3: Detailed QALY Calculation Methodology (30 lines)
  - Equation (3): QALY formula
  - Year 10 worked example
  - Step-by-step calculation
- Section 3.4.4: Cost Offset Composition (26 lines)
  - Dialysis savings calculation
  - Transplant savings calculation
  - CKD management savings
  - Total with arithmetic shown

**DELETE**:
- Adjectives: "substantial", "favorable"

### 3.5 Value-Based Pricing (+48 lines)

**ADD**:
- Section 3.5.5: Threshold Selection and Justification (28 lines)
  - International threshold comparison
  - Ultra-rare disease threshold rationale
  - Specific threshold arithmetic
- Section 3.5.6: Worked Example Price Calculation (20 lines)
  - Step 1: Incremental QALYs
  - Step 2: Health benefit value
  - Step 3: Cost offset
  - Step 4: Maximum price
  - All arithmetic explicit

**DELETE**:
- Adjectives: "appropriate", "reasonable"

### 3.6 Probabilistic Sensitivity Analysis (+62 lines)

**ADD**:
- Section 3.6.3.1: Parameter Distribution Specifications (32 lines)
  - Beta distributions for utilities
  - Gamma distributions for costs
  - Lognormal for hazard ratios
  - Normal for treatment effect
  - All with α, β, μ, σ parameters
- Section 3.6.4.1: Variance Decomposition Analysis (30 lines)
  - NEW TABLE: Variance contribution by parameter
  - Percentage calculations shown
  - Interpretation of key drivers

**DELETE**:
- Adjectives: "robust", "favorable"

### 3.7 Treatment Timing (+37 lines)

**ADD**:
- Section 3.7.2.1: eGFR Trajectory Calculations by Starting Age (37 lines)
  - Equation (4): Starting eGFR by age
  - Worked example for age 10
  - QALY impact calculation with arithmetic

**DELETE**:
- Adjectives: "important", "critical"

### 3.8 Conclusions (+21 lines)

**ADD**:
- Section 3.8.6: Economic Implications and Policy Context (21 lines)
  - Budget impact calculation
  - Proportion of pharmaceutical expenditure
  - Comparison to existing orphan drugs
  - All arithmetic shown

**DELETE**:
- Adjectives: "reasonable", "appropriate"
- Any promotional language

## Enzyme Content Removal Checklist

Throughout ALL subsections, DELETE:

1. **Table 3.3 Column**: "OCRL Enzyme Replacement" column and all percentages
2. **Scenario Descriptions**: Any mention of:
   - "90% enzyme replacement"
   - "75% enzyme replacement"
   - "50% enzyme replacement"
   - "25% enzyme replacement"
   - "enzyme functional correction"
   - "OCRL enzyme activity"
3. **Explanatory Text**: Any mechanistic explanations involving enzyme levels
4. **Replace With**: Clinical outcome descriptions only:
   - Optimistic: "Substantial disease slowing (0.30 ml/min/year decline)"
   - Realistic: "Moderate disease slowing (0.52 ml/min/year decline)"
   - Conservative: "Limited disease slowing (0.74 ml/min/year decline)"
   - Pessimistic: "Minimal disease slowing (1.04 ml/min/year decline)"

## Git Workflow

### After Each Subsection Approval

```bash
# Stage changes
git add HTA_SECTION_3_COST_EFFECTIVENESS_ANALYSIS.md

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Complete Section {SECTION_NUMBER}: {Description}

- Expanded from X to Y lines
- Removed prohibited adjectives
- Added explicit calculations for all percentages
- Deleted enzyme-related content
- Complies with AER and Denmark style guidelines

Approved by reviewer agent after N iterations.
EOF
)"

# Push to feature branch
git push -u origin claude/expand-cost-analysis-01SbMAnA6FXS3shU4mKbmAr9
```

### Example Commit Messages

**Section 3.1**:
```
Complete Section 3.1 Summary: Add explicit calculations and remove adjectives

- Expanded from 30 to 45 lines
- Added ICER threshold calculation (11% below threshold)
- Added QALY composition breakdown
- Removed: comprehensive, critical, favorable
- All percentages now show arithmetic

Approved by reviewer agent after 2 iterations.
```

**Section 3.2**:
```
Complete Section 3.2 Methodology: Add transition probabilities and calibration

- Expanded from 60 to 140 lines (+133%)
- Added Section 3.2.4: Transition Probability Calculations
- Added Section 3.2.5: Model Calibration and Validation
- Removed all enzyme replacement mechanism details
- Added equations (1) and (2)

Approved by reviewer agent after 3 iterations.
```

## Success Criteria

A subsection is considered complete when:

1. ✅ Reviewer Agent returns "APPROVED"
2. ✅ All expansion requirements implemented
3. ✅ All prohibited adjectives removed
4. ✅ All calculations shown explicitly
5. ✅ All enzyme content deleted
6. ✅ AER style compliance verified
7. ✅ Denmark Ministry style compliance verified
8. ✅ Changes committed and pushed to repository

## Error Handling

### Writer Agent Fails
- Review error message
- Adjust prompt for clarity
- Retry with simplified requirements
- If persistent, break subsection into smaller chunks

### Reviewer Agent Stuck
- After 3 consecutive "REVISIONS REQUIRED" with same issues
- Review whether requirements are contradictory
- Escalate to human review
- Consider relaxing specific requirement if justified

### Git Push Fails
- Check network connectivity
- Retry with exponential backoff (2s, 4s, 8s, 16s)
- Maximum 4 retries
- If still failing, stage for manual push

## Quality Assurance

After each subsection commit, verify:
- File is valid markdown (no syntax errors)
- Cross-references still valid
- Table formatting intact
- Equation numbering sequential
- No broken internal links

## Timeline Estimate

- Section 3.1: 1-2 hours (simple)
- Section 3.2: 3-4 hours (complex, large expansion)
- Section 3.3: 2-3 hours (table modifications, enzyme deletion)
- Section 3.4: 2-3 hours (detailed calculations)
- Section 3.5: 2-3 hours (worked examples)
- Section 3.6: 3-4 hours (new table, distributions)
- Section 3.7: 2-3 hours (trajectory calculations)
- Section 3.8: 1-2 hours (policy context)

**Total Estimated Time**: 16-24 hours of agent work

## Reporting

After each subsection, report:
1. Subsection number and title
2. Number of writer-reviewer iterations required
3. Final line count (before → after)
4. Key issues identified and resolved
5. Commit SHA
6. Time taken

Final report after all subsections includes:
- Total iterations across all subsections
- Total expansion (450 → 905 lines)
- All prohibited content removed
- Style compliance rate
- Commit history
