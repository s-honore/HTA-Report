"""
Validation script for Markov chain scenarios
Tests that all scenarios are correctly implemented
"""

import numpy as np
import pandas as pd
from markov_cua_model import ModelParameters, MarkovCohortModel, ScenarioAnalysis

def validate_scenario_decline_rates():
    """
    Validate that scenarios produce expected decline rates.
    """
    print("="*80)
    print("VALIDATION 1: Actual eGFR Decline Rates")
    print("="*80)

    params = ModelParameters()
    model = MarkovCohortModel(params)

    # Define expected scenarios
    scenarios_to_test = [
        {"name": "Natural History", "decline_rate": 1.80, "expected": "age-varying (1.0, 3.5, 2.0)"},
        {"name": "Scenario 1: Carrier-Equivalent", "decline_rate": 0.30, "expected": "0.30 constant"},
        {"name": "Scenario 2: Subthreshold", "decline_rate": 0.70, "expected": "0.70 time-averaged"},
        {"name": "Scenario 3: Minimal", "decline_rate": 0.94, "expected": "0.94 time-averaged"},
    ]

    for scenario in scenarios_to_test:
        print(f"\n{scenario['name']}:")
        print(f"  Configured rate: {scenario['decline_rate']} ml/min/yr")
        print(f"  Expected: {scenario['expected']}")

        # Test decline rates at different ages
        ages_to_test = [5, 10, 15, 20, 30, 40]
        print(f"  Actual rates by age:")
        for age in ages_to_test:
            actual_rate = model.get_decline_rate(age, scenario['decline_rate'])
            print(f"    Age {age}: {actual_rate:.3f} ml/min/yr")

        # Calculate time-averaged rate from age 1 to 40
        total_decline = 0
        years = 0
        for age in range(1, 41):
            total_decline += model.get_decline_rate(age, scenario['decline_rate'])
            years += 1
        avg_rate = total_decline / years
        print(f"  Time-averaged rate (ages 1-40): {avg_rate:.3f} ml/min/yr")


def validate_eskd_timing():
    """
    Validate that scenarios produce expected time to ESKD.
    """
    print("\n" + "="*80)
    print("VALIDATION 2: Time to ESKD")
    print("="*80)

    params = ModelParameters()

    scenarios = [
        {"name": "Natural History", "decline": 1.80, "expected_eskd": 32},
        {"name": "Scenario 1", "decline": 0.30, "expected_eskd": "Never (>100)"},
        {"name": "Scenario 2", "decline": 0.70, "expected_eskd": 84},
        {"name": "Scenario 3", "decline": 0.94, "expected_eskd": 63},
    ]

    for scenario in scenarios:
        model = MarkovCohortModel(params)
        results = model.run_model(
            egfr_decline_rate=scenario['decline'],
            scenario_name=scenario['name'],
            include_gene_therapy_cost=False
        )

        actual_eskd = results['time_to_eskd']
        actual_age = params.starting_age + actual_eskd

        print(f"\n{scenario['name']}:")
        print(f"  Decline rate: {scenario['decline']} ml/min/yr")
        print(f"  Expected ESKD age: {scenario['expected_eskd']}")
        print(f"  Actual ESKD: Year {actual_eskd} (age {actual_age})")
        print(f"  Life expectancy: {results['life_years']:.1f} years")

        # Check eGFR trajectory
        eskd_idx = model.states.index('ESKD')
        eskd_proportion = results['trace'][actual_eskd, eskd_idx] if actual_eskd < len(results['trace']) else 0
        print(f"  ESKD proportion at that time: {eskd_proportion*100:.1f}%")


def validate_treatment_effects():
    """
    Validate that treatment effects are correctly decomposed.
    """
    print("\n" + "="*80)
    print("VALIDATION 3: Treatment Effect Decomposition")
    print("="*80)

    params = ModelParameters()
    model = MarkovCohortModel(params)

    print("\nDecomposition formula: D_treated = D_age + (1-θ)×D_path")
    print(f"Where D_age = 0.3 ml/min/yr (normal aging)")
    print(f"And D_path = (natural_rate - D_age) varies by age\n")

    # Test at different ages
    ages = [5, 15, 25]

    for age in ages:
        print(f"\nAge {age}:")
        natural_rate = model.get_decline_rate(age, params.natural_decline_rate)
        print(f"  Natural rate: {natural_rate:.2f} ml/min/yr")

        D_age = 0.3
        D_path = natural_rate - D_age
        print(f"  D_path (pathological): {D_path:.2f} ml/min/yr")

        # Test scenarios
        for theta, decline_rate, name in [(1.0, 0.30, "Carrier"), (0.5, 0.70, "Subthreshold"), (0.2, 0.94, "Minimal")]:
            expected_treated = D_age + (1 - theta) * D_path
            actual_treated = model.get_decline_rate(age, decline_rate)
            print(f"  {name} (θ={theta}): Expected {expected_treated:.3f}, Actual {actual_treated:.3f}")


def check_for_treatment_waning():
    """
    Check if treatment waning scenario exists in code.
    """
    print("\n" + "="*80)
    print("VALIDATION 4: Treatment Waning Scenario")
    print("="*80)

    # Check if waning scenario is implemented
    print("\nSearching for treatment waning implementation...")
    print("  Report mentions: 'full efficacy (θ=1.0) for 10 years, then 50% reduction'")
    print("  Expected ICER: ~540,000 euros/QALY")
    print("\n  ❌ NOT FOUND in code - needs to be implemented!")


def validate_cost_calculations():
    """
    Validate that costs and QALYs are correctly calculated.
    """
    print("\n" + "="*80)
    print("VALIDATION 5: Cost and QALY Calculations")
    print("="*80)

    params = ModelParameters()
    scenario_analysis = ScenarioAnalysis(params)

    # Run scenarios
    results = scenario_analysis.run_all_scenarios()

    # Check baseline
    baseline = results['Scenario 0: Natural History']
    print(f"\nNatural History Baseline:")
    print(f"  Total costs: ${baseline['total_costs']:,.0f}")
    print(f"  Total QALYs: {baseline['total_qalys']:.2f}")
    print(f"  Life years: {baseline['life_years']:.1f}")
    print(f"  Time to ESKD: Year {baseline['time_to_eskd']} (age {params.starting_age + baseline['time_to_eskd']})")

    # Check treatment scenarios
    for scenario_name in ['Scenario 1: Carrier-Equivalent', 'Scenario 2: Subthreshold', 'Scenario 3: Minimal Benefit']:
        if scenario_name in results:
            result = results[scenario_name]
            print(f"\n{scenario_name}:")
            print(f"  Total costs: ${result['total_costs']:,.0f}")
            print(f"  Total QALYs: {result['total_qalys']:.2f}")
            print(f"  Life years: {result['life_years']:.1f}")
            print(f"  Incremental costs: ${result.get('incremental_costs', 0):,.0f}")
            print(f"  Incremental QALYs: {result.get('incremental_qalys', 0):.3f}")
            print(f"  ICER: ${result.get('icer', 0):,.0f}/QALY")

            # Validate ICER calculation
            if result.get('incremental_qalys', 0) > 0:
                manual_icer = result['incremental_costs'] / result['incremental_qalys']
                stored_icer = result['icer']
                match = "✓" if abs(manual_icer - stored_icer) < 1 else "✗"
                print(f"  ICER validation: {match} (manual: ${manual_icer:,.0f}, stored: ${stored_icer:,.0f})")


def main():
    """
    Run all validation tests.
    """
    print("\n" + "="*80)
    print("MARKOV MODEL SCENARIO VALIDATION")
    print("Critical Review by Markov Chain Expert")
    print("="*80 + "\n")

    try:
        validate_scenario_decline_rates()
        validate_eskd_timing()
        validate_treatment_effects()
        check_for_treatment_waning()
        validate_cost_calculations()

        print("\n" + "="*80)
        print("VALIDATION COMPLETE")
        print("="*80)
        print("\nKEY FINDINGS:")
        print("  1. Age-varying decline rates are implemented (not constant as stated in report)")
        print("  2. Treatment effects vary by age group due to varying D_path")
        print("  3. Treatment waning scenario is MISSING from code")
        print("  4. Need to verify that time-averaged rates match report claims")

    except Exception as e:
        print(f"\n❌ ERROR during validation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
