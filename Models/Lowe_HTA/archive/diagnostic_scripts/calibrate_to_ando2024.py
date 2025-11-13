"""
Comprehensive recalibration to match Ando 2024 natural history data

KEY TARGETS FROM ANDO 2024:
- Median ESKD age: 32 years (range 25-39)
- 67% have ESKD by age 30+
- 84% have severe CKD (stages 4-5) by age 20+

KEY TARGETS FROM MURDOCK 2023:
- Death typically in 2nd-4th decade (ages 20-40)
- Median survival ~30-35 years

COMBINED IMPLICATION:
- Patients reach ESKD at ~age 32
- Patients die at ~age 35-40
- Post-ESKD survival: ~3-8 years (RAPID decline post-ESKD)
"""

import numpy as np
import pandas as pd
from markov_cua_model import ModelParameters, MarkovCohortModel

def test_calibration_combinations():
    """
    Test various combinations to find parameters that match Ando 2024 targets
    """
    print("="*80)
    print("COMPREHENSIVE CALIBRATION TO ANDO 2024 + MURDOCK 2023")
    print("="*80)

    print("\nTARGETS:")
    print("  - Median ESKD age: 32 years (Ando 2024)")
    print("  - Median death age: 30-40 years (Murdock 2023)")
    print("  - Post-ESKD survival: ~3-8 years")
    print("  - Current issue: Model shows 12.5 years post-ESKD survival (too long!)")

    # Test combinations (EXPANDED RANGE to reach ESKD age 32)
    starting_egfrs = [95, 100, 105, 110, 115]
    eskd_mortality_multipliers = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

    results_list = []

    print(f"\n" + "="*80)
    print("CALIBRATION GRID SEARCH")
    print("="*80)
    print(f"\n{'eGFR₀':<8} {'ESKD Mort':<12} {'ESKD Age':<10} {'Death Age':<12} {'Post-ESKD':<12} {'Match?':<10}")
    print("-"*80)

    for egfr_0 in starting_egfrs:
        for eskd_mult in eskd_mortality_multipliers:
            params = ModelParameters()
            params.starting_egfr = egfr_0
            params.mortality_multipliers['ESKD'] = eskd_mult

            model = MarkovCohortModel(params)

            # Run natural history
            nh = model.run_model(
                egfr_decline_rate=params.natural_decline_rate,
                scenario_name="Natural History",
                include_gene_therapy_cost=False
            )

            eskd_age = params.starting_age + nh['time_to_eskd']
            death_age = nh['life_years']
            post_eskd_survival = death_age - eskd_age

            # Check if matches targets
            eskd_match = 30 <= eskd_age <= 34  # Target: 32 ±2
            death_match = 30 <= death_age <= 40  # Target: 30-40
            post_eskd_match = 3 <= post_eskd_survival <= 8  # Target: 3-8 years

            overall_match = eskd_match and death_match and post_eskd_match

            match_str = "✅ YES" if overall_match else ("⚠️ Close" if (eskd_match and death_match) else "❌ No")

            print(f"{egfr_0:<8} {eskd_mult:<12.1f} {eskd_age:<10.1f} {death_age:<12.1f} {post_eskd_survival:<12.1f} {match_str:<10}")

            results_list.append({
                'starting_egfr': egfr_0,
                'eskd_mult': eskd_mult,
                'eskd_age': eskd_age,
                'death_age': death_age,
                'post_eskd_survival': post_eskd_survival,
                'eskd_match': eskd_match,
                'death_match': death_match,
                'post_eskd_match': post_eskd_match,
                'overall_match': overall_match
            })

    df = pd.DataFrame(results_list)

    # Find best matches
    best_matches = df[df['overall_match'] == True]

    if len(best_matches) > 0:
        print(f"\n" + "="*80)
        print("✅ FOUND CALIBRATIONS THAT MATCH ALL TARGETS!")
        print("="*80)
        print(best_matches.to_string(index=False))

        # Select best calibration (closest to ESKD age 32)
        best = best_matches.iloc[(best_matches['eskd_age'] - 32).abs().argsort()[:1]]

        print(f"\n🎯 RECOMMENDED CALIBRATION:")
        print(f"   starting_egfr = {best['starting_egfr'].values[0]:.0f} ml/min/1.73m²")
        print(f"   ESKD mortality multiplier = {best['eskd_mult'].values[0]:.1f}×")
        print(f"\n   Results:")
        print(f"   - ESKD age: {best['eskd_age'].values[0]:.1f} years (target: 32)")
        print(f"   - Death age: {best['death_age'].values[0]:.1f} years (target: 30-40)")
        print(f"   - Post-ESKD survival: {best['post_eskd_survival'].values[0]:.1f} years (target: 3-8)")

        return best['starting_egfr'].values[0], best['eskd_mult'].values[0]

    else:
        print(f"\n" + "="*80)
        print("⚠️ NO PERFECT MATCH FOUND")
        print("="*80)

        # Find closest matches
        close_matches = df[(df['eskd_match']) & (df['death_match'])]

        if len(close_matches) > 0:
            print("\nClosest calibrations (matching ESKD and death ages):")
            print(close_matches[['starting_egfr', 'eskd_mult', 'eskd_age', 'death_age', 'post_eskd_survival']].to_string(index=False))

            # Select closest
            best = close_matches.iloc[(close_matches['eskd_age'] - 32).abs().argsort()[:1]]

            print(f"\n🎯 BEST AVAILABLE CALIBRATION:")
            print(f"   starting_egfr = {best['starting_egfr'].values[0]:.0f} ml/min/1.73m²")
            print(f"   ESKD mortality multiplier = {best['eskd_mult'].values[0]:.1f}×")

            return best['starting_egfr'].values[0], best['eskd_mult'].values[0]
        else:
            print("\nNo calibrations found that match targets. Need to expand search range.")
            return None, None


def test_recommended_calibration(egfr_0, eskd_mult):
    """
    Test the recommended calibration with all scenarios
    """
    print(f"\n" + "="*80)
    print(f"TESTING RECOMMENDED CALIBRATION")
    print(f"  starting_egfr = {egfr_0:.0f} ml/min/1.73m²")
    print(f"  ESKD mortality = {eskd_mult:.1f}× (increased from 4.0× for rapid post-ESKD death)")
    print("="*80)

    params = ModelParameters()
    params.starting_egfr = egfr_0
    params.mortality_multipliers['ESKD'] = eskd_mult

    model = MarkovCohortModel(params)

    # Define scenarios with REVISED framework
    scenarios = {
        'Natural History': {'decline': 1.80, 'theta': 0.0, 'cost': False},
        'Optimistic (θ=1.0)': {'decline': 0.30, 'theta': 1.0, 'cost': True},
        'Realistic (θ=0.75)': {'decline': 0.51, 'theta': 0.75, 'cost': True},  # NEW
        'Conservative (θ=0.5)': {'decline': 0.70, 'theta': 0.5, 'cost': True},
        'Pessimistic (θ=0.3)': {'decline': 0.95, 'theta': 0.3, 'cost': True},
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
    print(f"  ESKD age: {params.starting_age + baseline['time_to_eskd']} (target: 32)")
    print(f"  Death age: {baseline['life_years']:.1f} (target: 30-40)")
    print(f"  Post-ESKD survival: {baseline['life_years'] - (params.starting_age + baseline['time_to_eskd']):.1f} years (target: 3-8)")

    print(f"\n" + "="*80)
    print(f"TREATMENT SCENARIOS WITH CALIBRATED MODEL")
    print(f"="*80)
    print(f"\n{'Scenario':<35} {'θ':<6} {'ESKD Age':<10} {'Death Age':<12} {'Inc QALYs':<12} {'ICER ($/QALY)':<15}")
    print("-"*80)

    for name in list(scenarios.keys())[1:]:  # Skip natural history
        result = results[name]
        theta = scenarios[name]['theta']

        inc_cost = result['total_costs'] - baseline['total_costs']
        inc_qalys = result['total_qalys'] - baseline['total_qalys']
        icer = inc_cost / inc_qalys if inc_qalys > 0 else float('inf')

        eskd_age = params.starting_age + result['time_to_eskd']
        death_age = result['life_years']

        # Assessment
        if icer < 300000:
            status = "✅"
        elif icer < 500000:
            status = "⚠️"
        else:
            status = "❌"

        print(f"{name:<35} {theta:<6.2f} {eskd_age:<10.0f} {death_age:<12.1f} {inc_qalys:<12.2f} ${icer:<14,.0f} {status}")

    print(f"\n" + "="*80)
    print("KEY INSIGHTS FROM CALIBRATED MODEL")
    print("="*80)

    # Compare realistic scenarios
    realistic = results['Realistic (θ=0.75)']
    real_inc_qalys = realistic['total_qalys'] - baseline['total_qalys']
    real_inc_costs = realistic['total_costs'] - baseline['total_costs']
    real_icer = real_inc_costs / real_inc_qalys

    print(f"\nREALISTIC Scenario (θ=0.75, 75% pathological reduction):")
    print(f"  Incremental QALYs: {real_inc_qalys:.2f}")
    print(f"  ICER: ${real_icer:,.0f}/QALY")
    print(f"  Assessment: {'✅ Cost-effective at $300K' if real_icer < 300000 else ('⚠️ Acceptable for ultra-rare at $500K' if real_icer < 500000 else '❌ Poor value')}")

    print(f"\nIMPACT OF MORTALITY RECALIBRATION:")
    print(f"  Higher ESKD mortality (4.0× → {eskd_mult:.1f}×) shortens post-ESKD survival")
    print(f"  This REDUCES incremental life years (patients die sooner in all scenarios)")
    print(f"  BUT improves calibration realism (matches literature)")
    print(f"  Trade-off: Better calibration vs lower incremental benefits")

    return results


def compare_before_after():
    """
    Compare original vs recalibrated model
    """
    print(f"\n" + "="*80)
    print("BEFORE vs AFTER CALIBRATION COMPARISON")
    print("="*80)

    print(f"\n{'Metric':<40} {'ORIGINAL':<20} {'CALIBRATED':<20} {'Change':<15}")
    print("-"*80)

    # Original
    orig_params = ModelParameters()
    orig_params.starting_egfr = 83.0
    orig_params.mortality_multipliers['ESKD'] = 4.0
    orig_model = MarkovCohortModel(orig_params)

    orig_nh = orig_model.run_model(1.80, "NH", False)
    orig_s1 = orig_model.run_model(0.30, "S1", True)
    orig_s2 = orig_model.run_model(0.70, "S2", True)

    # Calibrated
    cal_params = ModelParameters()
    cal_params.starting_egfr = 100.0  # From grid search
    cal_params.mortality_multipliers['ESKD'] = 8.0  # From grid search
    cal_model = MarkovCohortModel(cal_params)

    cal_nh = cal_model.run_model(1.80, "NH", False)
    cal_s1 = cal_model.run_model(0.30, "S1", True)
    cal_s2_new = cal_model.run_model(0.51, "S2_new", True)  # New realistic θ=0.75

    # Natural History
    print(f"{'Natural History ESKD Age':<40} {orig_params.starting_age + orig_nh['time_to_eskd']:<20.1f} {cal_params.starting_age + cal_nh['time_to_eskd']:<20.1f} {'+' if cal_nh['time_to_eskd'] > orig_nh['time_to_eskd'] else ''}{(cal_nh['time_to_eskd'] - orig_nh['time_to_eskd']):<14.1f}")
    print(f"{'Natural History Death Age':<40} {orig_nh['life_years']:<20.1f} {cal_nh['life_years']:<20.1f} {'+' if cal_nh['life_years'] > orig_nh['life_years'] else ''}{(cal_nh['life_years'] - orig_nh['life_years']):<14.1f}")
    print(f"{'Post-ESKD Survival':<40} {orig_nh['life_years'] - (orig_params.starting_age + orig_nh['time_to_eskd']):<20.1f} {cal_nh['life_years'] - (cal_params.starting_age + cal_nh['time_to_eskd']):<20.1f} {(cal_nh['life_years'] - (cal_params.starting_age + cal_nh['time_to_eskd'])) - (orig_nh['life_years'] - (orig_params.starting_age + orig_nh['time_to_eskd'])):<14.1f}")

    # Scenario 1 (Optimistic)
    orig_s1_icer = (orig_s1['total_costs'] - orig_nh['total_costs']) / (orig_s1['total_qalys'] - orig_nh['total_qalys'])
    cal_s1_icer = (cal_s1['total_costs'] - cal_nh['total_costs']) / (cal_s1['total_qalys'] - cal_nh['total_qalys'])

    print(f"\n{'Optimistic (θ=1.0) Inc QALYs':<40} {orig_s1['total_qalys'] - orig_nh['total_qalys']:<20.2f} {cal_s1['total_qalys'] - cal_nh['total_qalys']:<20.2f} {(cal_s1['total_qalys'] - cal_nh['total_qalys']) - (orig_s1['total_qalys'] - orig_nh['total_qalys']):<14.2f}")
    print(f"{'Optimistic (θ=1.0) ICER':<40} ${orig_s1_icer:<19,.0f} ${cal_s1_icer:<19,.0f} ${cal_s1_icer - orig_s1_icer:<13,.0f}")

    # Scenario 2
    orig_s2_icer = (orig_s2['total_costs'] - orig_nh['total_costs']) / (orig_s2['total_qalys'] - orig_nh['total_qalys'])
    cal_s2_icer = (cal_s2_new['total_costs'] - cal_nh['total_costs']) / (cal_s2_new['total_qalys'] - cal_nh['total_qalys'])

    print(f"\n{'Realistic θ=0.5→0.75 Inc QALYs':<40} {orig_s2['total_qalys'] - orig_nh['total_qalys']:<20.2f} {cal_s2_new['total_qalys'] - cal_nh['total_qalys']:<20.2f} {(cal_s2_new['total_qalys'] - cal_nh['total_qalys']) - (orig_s2['total_qalys'] - orig_nh['total_qalys']):<14.2f}")
    print(f"{'Realistic ICER':<40} ${orig_s2_icer:<19,.0f} ${cal_s2_icer:<19,.0f} ${cal_s2_icer - orig_s2_icer:<13,.0f}")


def main():
    """
    Run comprehensive calibration
    """
    print("\n" + "="*80)
    print("LOWE SYNDROME MODEL RECALIBRATION TO ANDO 2024 + MURDOCK 2023")
    print("="*80)
    print("\nPROBLEM: Current model shows:")
    print("  - ESKD at age 19 (vs literature target age 32)")
    print("  - Post-ESKD survival 12.5 years (vs literature 3-8 years)")
    print("\nSOLUTION: Increase starting eGFR AND increase ESKD mortality")
    print("="*80)

    # Find best calibration
    egfr_0, eskd_mult = test_calibration_combinations()

    if egfr_0 is not None and eskd_mult is not None:
        # Test recommended calibration
        results = test_recommended_calibration(egfr_0, eskd_mult)

        # Compare before/after
        compare_before_after()

        print(f"\n" + "="*80)
        print("RECOMMENDED CHANGES TO markov_cua_model.py")
        print("="*80)
        print(f"""
Line 46: Change starting_egfr
    FROM: starting_egfr: float = 83.0
    TO:   starting_egfr: float = {egfr_0:.0f}

Line 114: Change ESKD mortality multiplier
    FROM: 'ESKD': 5.0
    TO:   'ESKD': {eskd_mult:.1f}

Lines 690-708: Redefine scenarios
    Scenario 1: Optimistic (θ=1.0) - KEEP AS IS
    Scenario 2: Realistic (θ=0.75) - CHANGE from θ=0.5, decline_rate=0.51
    Scenario 3: Conservative (θ=0.5) - KEEP but relabel from "Subthreshold"
    Scenario 4: Pessimistic (θ=0.3) - CHANGE from θ=0.2, decline_rate=0.95
        """)
    else:
        print("\n⚠️ Could not find suitable calibration. Try expanding search ranges.")


if __name__ == "__main__":
    main()
