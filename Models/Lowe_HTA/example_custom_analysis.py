"""
Example Custom Analysis Script

This script demonstrates how to:
1. Run the model with custom parameters
2. Test different scenarios
3. Perform custom sensitivity analyses
4. Export results for further analysis

Author: HTA Analysis Team
Date: November 2025
"""

import numpy as np
import pandas as pd
from markov_cua_model import ModelParameters, MarkovCohortModel, ScenarioAnalysis, SensitivityAnalysis


def example_1_basic_custom_run():
    """
    Example 1: Run model with custom gene therapy cost
    """
    print("=" * 80)
    print("EXAMPLE 1: Custom Gene Therapy Cost")
    print("=" * 80)

    # Create custom parameters
    params = ModelParameters()
    params.gene_therapy_cost = 2500000  # $2.5M instead of $3M

    print(f"\nCustom Parameters:")
    print(f"  Gene Therapy Cost: ${params.gene_therapy_cost:,.0f}")
    print(f"  Natural Decline Rate: {params.natural_decline_rate} ml/min/1.73m²/year")

    # Run scenario analysis
    scenario_analysis = ScenarioAnalysis(params)
    results = scenario_analysis.run_all_scenarios()

    # Print results
    summary = scenario_analysis.summarize_results()
    print("\nResults:")
    print(summary.to_string(index=False))

    # Export results
    summary.to_csv('/home/user/HTA-Report/Models/Lowe_HTA/example1_results.csv', index=False)
    print("\nResults saved to: example1_results.csv")


def example_2_test_multiple_prices():
    """
    Example 2: Test multiple gene therapy prices
    """
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Price Sensitivity Analysis")
    print("=" * 80)

    prices = [2000000, 2500000, 3000000, 3500000, 4000000]
    results_list = []

    print(f"\nTesting {len(prices)} different prices...")

    for price in prices:
        # Create parameters with this price
        params = ModelParameters()
        params.gene_therapy_cost = price

        # Run stabilization scenario only
        model = MarkovCohortModel(params)

        # Baseline
        baseline = model.run_model(
            egfr_decline_rate=params.natural_decline_rate,
            scenario_name="Baseline",
            include_gene_therapy_cost=False
        )

        # Stabilization
        stabilization = model.run_model(
            egfr_decline_rate=0.0,
            scenario_name="Stabilization",
            include_gene_therapy_cost=True
        )

        # Calculate ICER
        inc_cost = stabilization['total_costs'] - baseline['total_costs']
        inc_qaly = stabilization['total_qalys'] - baseline['total_qalys']
        icer = inc_cost / inc_qaly if inc_qaly > 0 else float('inf')

        results_list.append({
            'Gene_Therapy_Price': price,
            'Total_Costs': stabilization['total_costs'],
            'Total_QALYs': stabilization['total_qalys'],
            'Incremental_Costs': inc_cost,
            'Incremental_QALYs': inc_qaly,
            'ICER': icer,
            'Below_100K_Threshold': icer <= 100000,
            'Below_150K_Threshold': icer <= 150000
        })

    # Create DataFrame
    df = pd.DataFrame(results_list)
    print("\nPrice Sensitivity Results:")
    print(df.to_string(index=False))

    # Save results
    df.to_csv('/home/user/HTA-Report/Models/Lowe_HTA/example2_price_sensitivity.csv', index=False)
    print("\nResults saved to: example2_price_sensitivity.csv")

    # Find threshold price for $100K/QALY
    below_100k = df[df['Below_100K_Threshold'] == True]
    if not below_100k.empty:
        threshold_price = below_100k.iloc[-1]['Gene_Therapy_Price']
        print(f"\nMaximum price for $100K/QALY threshold: ${threshold_price:,.0f}")
    else:
        print(f"\nNo price meets $100K/QALY threshold (tested range: ${min(prices):,.0f} - ${max(prices):,.0f})")


def example_3_custom_utilities():
    """
    Example 3: Test impact of different utility values
    """
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Utility Value Sensitivity")
    print("=" * 80)

    # Base case
    base_params = ModelParameters()

    # Pessimistic utilities (lower quality of life)
    pessimistic_params = ModelParameters()
    pessimistic_params.utilities = {
        'CKD2': 0.65,
        'CKD3a': 0.60,
        'CKD3b': 0.50,
        'CKD4': 0.40,
        'ESKD': 0.30,
        'Death': 0.00
    }

    # Optimistic utilities (higher quality of life)
    optimistic_params = ModelParameters()
    optimistic_params.utilities = {
        'CKD2': 0.80,
        'CKD3a': 0.75,
        'CKD3b': 0.70,
        'CKD4': 0.65,
        'ESKD': 0.50,
        'Death': 0.00
    }

    results_list = []

    for name, params in [
        ('Base Case', base_params),
        ('Pessimistic', pessimistic_params),
        ('Optimistic', optimistic_params)
    ]:
        print(f"\nRunning {name} scenario...")

        scenario_analysis = ScenarioAnalysis(params)
        results = scenario_analysis.run_all_scenarios()

        stab = results['Scenario 1: Stabilization (0%)']

        results_list.append({
            'Utility_Scenario': name,
            'CKD2_Utility': params.utilities['CKD2'],
            'ESKD_Utility': params.utilities['ESKD'],
            'Total_QALYs': stab['total_qalys'],
            'Incremental_QALYs': stab['incremental_qalys'],
            'ICER': stab['icer']
        })

    df = pd.DataFrame(results_list)
    print("\nUtility Sensitivity Results:")
    print(df.to_string(index=False))

    df.to_csv('/home/user/HTA-Report/Models/Lowe_HTA/example3_utility_sensitivity.csv', index=False)
    print("\nResults saved to: example3_utility_sensitivity.csv")


def example_4_age_at_treatment():
    """
    Example 4: Test different ages at treatment initiation
    """
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Age at Treatment Sensitivity")
    print("=" * 80)

    ages = [3, 5, 7, 10, 15]
    # Corresponding starting eGFR (declines from birth)
    starting_egfrs = [80, 70, 60, 50, 40]

    results_list = []

    for age, egfr in zip(ages, starting_egfrs):
        print(f"\nTesting age {age} (starting eGFR {egfr})...")

        params = ModelParameters()
        params.starting_age = age
        params.starting_egfr = egfr

        # Run just stabilization vs baseline
        model = MarkovCohortModel(params)

        baseline = model.run_model(
            egfr_decline_rate=params.natural_decline_rate,
            scenario_name="Baseline",
            include_gene_therapy_cost=False
        )

        stabilization = model.run_model(
            egfr_decline_rate=0.0,
            scenario_name="Stabilization",
            include_gene_therapy_cost=True
        )

        inc_cost = stabilization['total_costs'] - baseline['total_costs']
        inc_qaly = stabilization['total_qalys'] - baseline['total_qalys']
        icer = inc_cost / inc_qaly if inc_qaly > 0 else float('inf')

        results_list.append({
            'Age_at_Treatment': age,
            'Starting_eGFR': egfr,
            'Baseline_QALYs': baseline['total_qalys'],
            'Treatment_QALYs': stabilization['total_qalys'],
            'Incremental_QALYs': inc_qaly,
            'Incremental_Costs': inc_cost,
            'ICER': icer,
            'Time_to_ESKD_Baseline': baseline['time_to_eskd'],
            'Time_to_ESKD_Treatment': stabilization['time_to_eskd']
        })

    df = pd.DataFrame(results_list)
    print("\nAge at Treatment Results:")
    print(df.to_string(index=False))

    df.to_csv('/home/user/HTA-Report/Models/Lowe_HTA/example4_age_sensitivity.csv', index=False)
    print("\nResults saved to: example4_age_sensitivity.csv")

    print("\nInsight: Treating earlier (younger age, higher eGFR) is generally more cost-effective")


def example_5_treatment_waning():
    """
    Example 5: Model treatment effect waning over time
    """
    print("\n\n" + "=" * 80)
    print("EXAMPLE 5: Treatment Waning Scenario")
    print("=" * 80)

    params = ModelParameters()
    model = MarkovCohortModel(params)

    # Baseline (natural history)
    baseline = model.run_model(
        egfr_decline_rate=params.natural_decline_rate,
        scenario_name="Baseline",
        include_gene_therapy_cost=False
    )

    # Permanent stabilization (no waning)
    permanent = model.run_model(
        egfr_decline_rate=0.0,
        scenario_name="Permanent Effect",
        include_gene_therapy_cost=True
    )

    # Waning: Start with stabilization, then gradually returns to natural decline
    # Simplified: Average decline rate over lifetime
    # Years 0-10: 0% decline
    # Years 10-20: 2% decline
    # Years 20+: 4% decline (back to natural)
    # Average over 30 years: (10*0 + 10*2 + 10*4) / 30 = 2.0 ml/min/year
    waning = model.run_model(
        egfr_decline_rate=2.0,  # Average waning effect
        scenario_name="Waning Effect",
        include_gene_therapy_cost=True
    )

    results_list = []
    for name, result in [
        ('Baseline (Natural History)', baseline),
        ('Permanent Stabilization', permanent),
        ('Waning Effect (Average)', waning)
    ]:
        if name == 'Baseline (Natural History)':
            results_list.append({
                'Scenario': name,
                'Total_Costs': result['total_costs'],
                'Total_QALYs': result['total_qalys'],
                'Life_Years': result['life_years'],
                'Incremental_Costs': 0,
                'Incremental_QALYs': 0,
                'ICER': 'Reference'
            })
        else:
            inc_cost = result['total_costs'] - baseline['total_costs']
            inc_qaly = result['total_qalys'] - baseline['total_qalys']
            icer = inc_cost / inc_qaly if inc_qaly > 0 else float('inf')

            results_list.append({
                'Scenario': name,
                'Total_Costs': result['total_costs'],
                'Total_QALYs': result['total_qalys'],
                'Life_Years': result['life_years'],
                'Incremental_Costs': inc_cost,
                'Incremental_QALYs': inc_qaly,
                'ICER': f"${icer:,.0f}/QALY" if icer != float('inf') else 'Infinity'
            })

    df = pd.DataFrame(results_list)
    print("\nTreatment Waning Results:")
    print(df.to_string(index=False))

    df.to_csv('/home/user/HTA-Report/Models/Lowe_HTA/example5_waning_scenario.csv', index=False)
    print("\nResults saved to: example5_waning_scenario.csv")

    print("\nInsight: Treatment waning significantly impacts cost-effectiveness")


def main():
    """
    Run all examples
    """
    print("\n")
    print("=" * 80)
    print(" CUSTOM ANALYSIS EXAMPLES FOR LOWE SYNDROME HTA MODEL")
    print("=" * 80)
    print("\nThis script demonstrates various custom analyses you can perform")
    print("with the Markov cohort model.")
    print("\nRunning 5 examples...")

    # Run all examples
    example_1_basic_custom_run()
    example_2_test_multiple_prices()
    example_3_custom_utilities()
    example_4_age_at_treatment()
    example_5_treatment_waning()

    print("\n\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nOutput files created:")
    print("  - example1_results.csv")
    print("  - example2_price_sensitivity.csv")
    print("  - example3_utility_sensitivity.csv")
    print("  - example4_age_sensitivity.csv")
    print("  - example5_waning_scenario.csv")
    print("\nYou can modify these examples to test your own scenarios!")


if __name__ == "__main__":
    main()
