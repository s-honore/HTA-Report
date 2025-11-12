"""
Quick test: What if we recalibrate with starting eGFR = 95?
"""

import numpy as np
import pandas as pd
from markov_cua_model import ModelParameters, MarkovCohortModel

def test_recalibration():
    print("="*80)
    print("RECALIBRATION TEST: Starting eGFR = 95 ml/min/1.73m²")
    print("="*80)

    # Create modified parameters
    params = ModelParameters()
    params.starting_egfr = 95.0  # INCREASE from 83 to 95

    model = MarkovCohortModel(params)

    # Run all scenarios
    scenarios = {
        'Natural History': {'decline': 1.80, 'cost': False},
        'Carrier-Equivalent (θ=1.0)': {'decline': 0.30, 'cost': True},
        'Intermediate (θ=0.7)': {'decline': 0.55, 'cost': True},  # NEW realistic
        'Subthreshold (θ=0.5)': {'decline': 0.70, 'cost': True},
        'Minimal (θ=0.3)': {'decline': 1.00, 'cost': True},
    }

    results = {}
    for name, config in scenarios.items():
        result = model.run_model(
            egfr_decline_rate=config['decline'],
            scenario_name=name,
            include_gene_therapy_cost=config['cost']
        )
        results[name] = result

    # Calculate ICERs
    baseline = results['Natural History']

    print(f"\nNATURAL HISTORY VALIDATION:")
    print(f"  ESKD age: {params.starting_age + baseline['time_to_eskd']}")
    print(f"  Life expectancy: {baseline['life_years']:.1f} years")
    print(f"  Target ESKD age: 32 (from Ando 2024)")

    print(f"\n" + "="*80)
    print(f"TREATMENT SCENARIOS WITH RECALIBRATED MODEL")
    print(f"="*80)
    print(f"\n{'Scenario':<35} {'ESKD Age':<10} {'Life Years':<12} {'Inc QALYs':<12} {'ICER ($/QALY)':<15}")
    print("-"*80)

    for name in list(scenarios.keys())[1:]:  # Skip natural history
        result = results[name]

        inc_cost = result['total_costs'] - baseline['total_costs']
        inc_qalys = result['total_qalys'] - baseline['total_qalys']
        icer = inc_cost / inc_qalys if inc_qalys > 0 else float('inf')

        eskd_age = params.starting_age + result['time_to_eskd']
        life_years = result['life_years']

        # Assessment
        if icer < 300000:
            status = "✅"
        elif icer < 600000:
            status = "⚠️"
        else:
            status = "❌"

        print(f"{name:<35} {eskd_age:<10.0f} {life_years:<12.1f} {inc_qalys:<12.2f} ${icer:<14,.0f} {status}")

    print("\n" + "="*80)
    print("IMPROVEMENT vs ORIGINAL CALIBRATION (eGFR₀=83)")
    print("="*80)

    # Compare to original
    orig_params = ModelParameters()
    orig_params.starting_egfr = 83.0
    orig_model = MarkovCohortModel(orig_params)

    orig_nh = orig_model.run_model(1.80, "NH", False)
    orig_s2 = orig_model.run_model(0.70, "S2", True)

    orig_inc_qalys = orig_s2['total_qalys'] - orig_nh['total_qalys']
    orig_inc_costs = orig_s2['total_costs'] - orig_nh['total_costs']
    orig_icer = orig_inc_costs / orig_inc_qalys

    new_s2 = results['Subthreshold (θ=0.5)']
    new_inc_qalys = new_s2['total_qalys'] - baseline['total_qalys']
    new_inc_costs = new_s2['total_costs'] - baseline['total_costs']
    new_icer = new_inc_costs / new_inc_qalys

    print(f"\nSubthreshold Scenario (θ=0.5):")
    print(f"  ORIGINAL (eGFR₀=83): {orig_inc_qalys:.2f} QALYs, ICER ${orig_icer:,.0f}")
    print(f"  RECALIBRATED (eGFR₀=95): {new_inc_qalys:.2f} QALYs, ICER ${new_icer:,.0f}")
    print(f"  IMPROVEMENT: {(orig_icer - new_icer)/orig_icer*100:.1f}% better ICER")

    # Test new "realistic" scenario
    new_realistic = results['Intermediate (θ=0.7)']
    real_inc_qalys = new_realistic['total_qalys'] - baseline['total_qalys']
    real_inc_costs = new_realistic['total_costs'] - baseline['total_costs']
    real_icer = real_inc_costs / real_inc_qalys

    print(f"\nNEW Realistic Scenario (θ=0.7):")
    print(f"  Inc QALYs: {real_inc_qalys:.2f}")
    print(f"  ICER: ${real_icer:,.0f}/QALY")
    print(f"  Assessment: {'✅ Cost-effective at €300K' if real_icer < 300000 else '⚠️ Marginal at €300K'}")

if __name__ == "__main__":
    test_recalibration()
