"""
Test treatment waning scenario and generate visualization figures
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from markov_cua_model import ModelParameters, MarkovCohortModel, ScenarioAnalysis

# Set publication-quality plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

def test_waning_scenario():
    """Test the treatment waning scenario."""
    print("="*80)
    print("TESTING TREATMENT WANING SCENARIO")
    print("="*80)

    params = ModelParameters()
    scenario_analysis = ScenarioAnalysis(params)

    # Run all scenarios including waning
    results = scenario_analysis.run_all_scenarios()

    # Check waning scenario results
    if 'Scenario 4: Treatment Waning' in results:
        waning = results['Scenario 4: Treatment Waning']
        baseline = results['Scenario 0: Natural History']

        print(f"\n✓ Treatment Waning Scenario Found!")
        print(f"\n  Clinical Outcomes:")
        print(f"    Total costs: ${waning['total_costs']:,.0f}")
        print(f"    Total QALYs: {waning['total_qalys']:.2f}")
        print(f"    Life years: {waning['life_years']:.1f}")
        print(f"    Time to ESKD: Year {waning['time_to_eskd']} (age {params.starting_age + waning['time_to_eskd']})")

        print(f"\n  Incremental vs Natural History:")
        print(f"    Incremental costs: ${waning.get('incremental_costs', 0):,.0f}")
        print(f"    Incremental QALYs: {waning.get('incremental_qalys', 0):.3f}")
        print(f"    ICER: ${waning.get('icer', 0):,.0f}/QALY")
        print(f"    Life years gained: {waning.get('incremental_life_years', 0):.1f}")

        print(f"\n  Report Target Validation:")
        print(f"    Expected incremental QALYs: ~4.20")
        print(f"    Actual incremental QALYs: {waning.get('incremental_qalys', 0):.2f}")
        print(f"    Expected ICER: ~€540,000/QALY")
        print(f"    Actual ICER: ${waning.get('icer', 0):,.0f}/QALY")

        match_qaly = "✓" if abs(waning.get('incremental_qalys', 0) - 4.20) < 1.0 else "✗"
        match_icer = "✓" if abs(waning.get('icer', 0) - 540000) < 100000 else "⚠"

        print(f"\n  Validation: {match_qaly} QALYs, {match_icer} ICER")

        return results
    else:
        print("\n✗ Treatment Waning Scenario NOT FOUND!")
        return results


def generate_figure1_age_varying_rates(results, output_dir='/home/user/HTA-Report/Models/Lowe_HTA'):
    """
    Figure 1: Age-varying decline rates by scenario
    Shows that treatment effects vary by age group
    """
    print(f"\nGenerating Figure 1: Age-Varying Decline Rates...")

    params = ModelParameters()
    model = MarkovCohortModel(params)

    # Define scenarios with their decline rate parameters
    scenarios = [
        ("Natural History", 1.80, 'red', '-'),
        ("Carrier-Equivalent", 0.30, 'green', '-'),
        ("Subthreshold", 0.70, 'blue', '--'),
        ("Minimal", 0.94, 'orange', ':'),
        ("Treatment Waning (Y0-10)", 0.30, 'purple', '-'),
        ("Treatment Waning (Y10+)", 0.70, 'purple', '--')
    ]

    ages = range(1, 61)

    fig, ax = plt.subplots(figsize=(14, 8))

    for scenario_name, decline_param, color, style in scenarios:
        rates = [model.get_decline_rate(age, decline_param) for age in ages]
        ax.plot(ages, rates, label=scenario_name, color=color, linestyle=style, linewidth=2)

    # Add shaded regions for age groups
    ax.axvspan(1, 10, alpha=0.1, color='gray', label='Age Group 1-10')
    ax.axvspan(10, 20, alpha=0.15, color='gray', label='Age Group 10-20')
    ax.axvspan(20, 60, alpha=0.1, color='gray', label='Age Group 20+')

    ax.set_xlabel('Age (years)', fontsize=14)
    ax.set_ylabel('eGFR Decline Rate (ml/min/1.73m²/year)', fontsize=14)
    ax.set_title('Age-Varying eGFR Decline Rates by Treatment Scenario\n(Critical Issue: Treatment Effects Vary by Age)',
                 fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 4)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure1_age_varying_rates.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved to {output_dir}/figure1_age_varying_rates.png")
    plt.close()


def generate_figure2_egfr_trajectories(results, output_dir='/home/user/HTA-Report/Models/Lowe_HTA'):
    """
    Figure 2: eGFR trajectories over time for all scenarios
    """
    print(f"\nGenerating Figure 2: eGFR Trajectories...")

    params = ModelParameters()

    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot each scenario
    scenario_colors = {
        'Scenario 0: Natural History': ('red', '-', 3),
        'Scenario 1: Carrier-Equivalent': ('green', '-', 2),
        'Scenario 2: Subthreshold': ('blue', '--', 2),
        'Scenario 3: Minimal Benefit': ('orange', ':', 2),
        'Scenario 4: Treatment Waning': ('purple', '-.', 2.5)
    }

    for scenario_name, (color, style, width) in scenario_colors.items():
        if scenario_name in results:
            egfr_track = results[scenario_name]['egfr_track']
            ages = [params.starting_age + i for i in range(len(egfr_track))]

            # Only plot until death or age 80
            max_idx = min(80 - params.starting_age, len(egfr_track))
            ax.plot(ages[:max_idx], egfr_track[:max_idx],
                   label=scenario_name.replace('Scenario ', 'S').replace(': ', ': '),
                   color=color, linestyle=style, linewidth=width)

    # Add ESKD threshold line
    ax.axhline(y=15, color='black', linestyle='--', linewidth=2, label='ESKD Threshold (15 ml/min/1.73m²)')

    # Add CKD stage regions
    ax.axhspan(0, 15, alpha=0.1, color='red', label='Stage 5: ESKD')
    ax.axhspan(15, 30, alpha=0.1, color='orange', label='Stage 4')
    ax.axhspan(30, 45, alpha=0.1, color='yellow', label='Stage 3b')
    ax.axhspan(45, 60, alpha=0.1, color='lightgreen', label='Stage 3a')
    ax.axhspan(60, 90, alpha=0.1, color='green', label='Stage 2')

    ax.set_xlabel('Age (years)', fontsize=14)
    ax.set_ylabel('eGFR (ml/min/1.73m²)', fontsize=14)
    ax.set_title('eGFR Trajectories by Treatment Scenario\nShowing Progression Through CKD Stages',
                 fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 90)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure2_egfr_trajectories.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved to {output_dir}/figure2_egfr_trajectories.png")
    plt.close()


def generate_figure3_waning_effect(results, output_dir='/home/user/HTA-Report/Models/Lowe_HTA'):
    """
    Figure 3: Treatment waning effect comparison
    """
    print(f"\nGenerating Figure 3: Treatment Waning Effect...")

    if 'Scenario 4: Treatment Waning' not in results:
        print("  ✗ Waning scenario not found, skipping...")
        return

    params = ModelParameters()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Panel A: eGFR trajectory comparison
    for scenario_name, color, style, label in [
        ('Scenario 1: Carrier-Equivalent', 'green', '-', 'No Waning (Sustained Effect)'),
        ('Scenario 4: Treatment Waning', 'purple', '-.', 'With Waning (Effect Reduces at Year 10)')
    ]:
        if scenario_name in results:
            egfr_track = results[scenario_name]['egfr_track']
            ages = [params.starting_age + i for i in range(len(egfr_track))]
            max_idx = min(60 - params.starting_age, len(egfr_track))
            ax1.plot(ages[:max_idx], egfr_track[:max_idx],
                    color=color, linestyle=style, linewidth=3, label=label)

    # Mark waning point
    ax1.axvline(x=params.starting_age + 10, color='red', linestyle='--', linewidth=2,
                label='Waning Begins (Year 10)', alpha=0.7)
    ax1.axhline(y=15, color='black', linestyle=':', linewidth=1, alpha=0.5)

    ax1.set_xlabel('Age (years)', fontsize=13)
    ax1.set_ylabel('eGFR (ml/min/1.73m²)', fontsize=13)
    ax1.set_title('Panel A: Impact of Treatment Waning on eGFR Trajectory', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 60)

    # Panel B: Cost-effectiveness comparison
    scenarios_for_bar = [
        ('Scenario 0: Natural History', 'Reference'),
        ('Scenario 1: Carrier-Equivalent', 'No Waning'),
        ('Scenario 4: Treatment Waning', 'With Waning')
    ]

    icers = []
    qalys = []
    labels = []

    baseline = results['Scenario 0: Natural History']

    for scenario_name, label in scenarios_for_bar:
        if scenario_name in results and scenario_name != 'Scenario 0: Natural History':
            result = results[scenario_name]
            icers.append(result.get('icer', 0) / 1000)  # Convert to thousands
            qalys.append(result.get('incremental_qalys', 0))
            labels.append(label)

    x = np.arange(len(labels))
    width = 0.35

    ax2_twin = ax2.twinx()
    bars1 = ax2.bar(x - width/2, qalys, width, label='Incremental QALYs', color='lightblue', edgecolor='black')
    bars2 = ax2_twin.bar(x + width/2, icers, width, label='ICER ($/1000 per QALY)', color='lightcoral', edgecolor='black')

    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars1, qalys)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    for i, (bar, val) in enumerate(zip(bars2, icers)):
        ax2_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                     f'${val:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_xlabel('Scenario', fontsize=13)
    ax2.set_ylabel('Incremental QALYs', fontsize=13, color='blue')
    ax2_twin.set_ylabel('ICER ($/1000 per QALY)', fontsize=13, color='red')
    ax2.set_title('Panel B: Clinical and Economic Impact of Waning', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2_twin.tick_params(axis='y', labelcolor='red')
    ax2.legend(loc='upper left', fontsize=10)
    ax2_twin.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure3_waning_effect.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved to {output_dir}/figure3_waning_effect.png")
    plt.close()


def generate_figure4_ce_plane(results, output_dir='/home/user/HTA-Report/Models/Lowe_HTA'):
    """
    Figure 4: Cost-effectiveness plane with all scenarios
    """
    print(f"\nGenerating Figure 4: Cost-Effectiveness Plane...")

    fig, ax = plt.subplots(figsize=(12, 10))

    baseline = results['Scenario 0: Natural History']

    scenarios_to_plot = [
        ('Scenario 1: Carrier-Equivalent', 'green', 'o', 150),
        ('Scenario 2: Subthreshold', 'blue', 's', 150),
        ('Scenario 3: Minimal Benefit', 'orange', '^', 150),
        ('Scenario 4: Treatment Waning', 'purple', 'D', 200)
    ]

    for scenario_name, color, marker, size in scenarios_to_plot:
        if scenario_name in results:
            result = results[scenario_name]
            inc_qalys = result.get('incremental_qalys', 0)
            inc_costs = result.get('incremental_costs', 0) / 1000  # Convert to thousands

            ax.scatter(inc_qalys, inc_costs, color=color, marker=marker, s=size,
                      edgecolor='black', linewidth=2, label=scenario_name.replace('Scenario ', 'S'),
                      alpha=0.8, zorder=5)

            # Add labels
            ax.annotate(scenario_name.split(': ')[1],
                       xy=(inc_qalys, inc_costs),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.3))

    # Add ICER threshold lines
    max_qaly = max([results[s[0]].get('incremental_qalys', 0)
                    for s in scenarios_to_plot if s[0] in results]) * 1.1

    thresholds = [
        (100000, 'red', '--', '$100K/QALY'),
        (150000, 'orange', '--', '$150K/QALY'),
        (300000, 'green', '--', '$300K/QALY (Ultra-rare)')
    ]

    for threshold, color, style, label in thresholds:
        qalys_line = np.linspace(0, max_qaly, 100)
        costs_line = (threshold * qalys_line) / 1000
        ax.plot(qalys_line, costs_line, color=color, linestyle=style,
               linewidth=2, label=label, alpha=0.7)

    ax.set_xlabel('Incremental QALYs vs Natural History', fontsize=14)
    ax.set_ylabel('Incremental Costs vs Natural History ($1000s)', fontsize=14)
    ax.set_title('Cost-Effectiveness Plane: All Treatment Scenarios\nIncluding Treatment Waning',
                fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, max_qaly * 1.05)
    ax.set_ylim(0, None)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure4_ce_plane.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved to {output_dir}/figure4_ce_plane.png")
    plt.close()


def generate_summary_table(results, output_dir='/home/user/HTA-Report/Models/Lowe_HTA'):
    """
    Generate comprehensive summary table of all scenarios
    """
    print(f"\nGenerating Summary Table...")

    params = ModelParameters()
    baseline = results['Scenario 0: Natural History']

    summary_data = []

    for scenario_name in sorted(results.keys()):
        result = results[scenario_name]

        row = {
            'Scenario': scenario_name.replace('Scenario ', ''),
            'Total Cost ($)': f"${result['total_costs']:,.0f}",
            'Total QALYs': f"{result['total_qalys']:.2f}",
            'Life Years': f"{result['life_years']:.1f}",
            'Time to ESKD (years)': f"{result['time_to_eskd']}",
            'ESKD Age': f"{params.starting_age + result['time_to_eskd']}"
        }

        if scenario_name != 'Scenario 0: Natural History':
            row['Inc. Cost ($)'] = f"${result.get('incremental_costs', 0):,.0f}"
            row['Inc. QALYs'] = f"{result.get('incremental_qalys', 0):.3f}"
            row['LYG'] = f"{result.get('incremental_life_years', 0):.1f}"
            row['ICER ($/QALY)'] = f"${result.get('icer', 0):,.0f}"
        else:
            row['Inc. Cost ($)'] = 'Reference'
            row['Inc. QALYs'] = 'Reference'
            row['LYG'] = 'Reference'
            row['ICER ($/QALY)'] = 'Reference'

        summary_data.append(row)

    df = pd.DataFrame(summary_data)

    # Save to CSV
    df.to_csv(f'{output_dir}/summary_all_scenarios.csv', index=False)
    print(f"  ✓ Saved to {output_dir}/summary_all_scenarios.csv")

    # Print to console
    print(f"\n" + "="*80)
    print("COMPREHENSIVE SCENARIO SUMMARY")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80)

    return df


def main():
    """
    Main execution: test waning scenario and generate all figures
    """
    print("\n" + "="*80)
    print("TREATMENT WANING IMPLEMENTATION & FIGURE GENERATION")
    print("="*80 + "\n")

    # Test waning scenario
    results = test_waning_scenario()

    if results:
        print(f"\n" + "="*80)
        print("GENERATING VISUALIZATION FIGURES")
        print("="*80)

        # Generate all figures
        generate_figure1_age_varying_rates(results)
        generate_figure2_egfr_trajectories(results)
        generate_figure3_waning_effect(results)
        generate_figure4_ce_plane(results)

        # Generate summary table
        generate_summary_table(results)

        print(f"\n" + "="*80)
        print("✓ ALL FIGURES AND TABLES GENERATED SUCCESSFULLY")
        print("="*80)
        print(f"\nOutput files created in: /home/user/HTA-Report/Models/Lowe_HTA/")
        print(f"  - figure1_age_varying_rates.png")
        print(f"  - figure2_egfr_trajectories.png")
        print(f"  - figure3_waning_effect.png")
        print(f"  - figure4_ce_plane.png")
        print(f"  - summary_all_scenarios.csv")

    else:
        print(f"\n✗ Failed to generate results")


if __name__ == "__main__":
    main()
