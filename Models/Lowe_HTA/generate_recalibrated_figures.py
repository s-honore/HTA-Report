"""
Generate visualization figures for recalibrated Markov model

Creates 4 publication-quality figures:
1. Age-varying decline rates by scenario
2. eGFR trajectories through CKD stages
3. Treatment waning effect comparison
4. Cost-effectiveness plane
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markov_cua_model import ModelParameters, MarkovCohortModel, ScenarioAnalysis

# Publication-quality plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['lines.linewidth'] = 2.5


def generate_figure1_decline_rates():
    """
    Figure 1: Age-varying decline rates for all scenarios
    """
    print("\nGenerating Figure 1: Age-varying decline rates...")

    params = ModelParameters()
    model = MarkovCohortModel(params)

    ages = np.arange(1, 61)  # Ages 1-60

    # Calculate decline rates for each scenario at each age
    scenarios = {
        'Natural History': params.natural_decline_rate,
        'Optimistic (θ=1.0)': 0.30,
        'Realistic (θ=0.85)': 0.52,
        'Conservative (θ=0.70)': 0.74,
        'Pessimistic (θ=0.50)': 1.04
    }

    fig, ax = plt.subplots(figsize=(12, 8))

    colors = {
        'Natural History': '#d62728',  # Red
        'Optimistic (θ=1.0)': '#2ca02c',  # Green
        'Realistic (θ=0.85)': '#1f77b4',  # Blue
        'Conservative (θ=0.70)': '#ff7f0e',  # Orange
        'Pessimistic (θ=0.50)': '#9467bd'   # Purple
    }

    line_styles = {
        'Natural History': '--',
        'Optimistic (θ=1.0)': '-',
        'Realistic (θ=0.85)': '-',
        'Conservative (θ=0.70)': '-',
        'Pessimistic (θ=0.50)': '-'
    }

    for scenario_name, base_decline in scenarios.items():
        rates = [model.get_decline_rate(age, base_decline) for age in ages]
        ax.plot(ages, rates,
                label=scenario_name,
                color=colors[scenario_name],
                linestyle=line_styles[scenario_name],
                linewidth=2.5 if 'Realistic' in scenario_name else 2.0,
                alpha=0.9)

    # Add vertical lines for age transitions
    ax.axvline(x=10, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    ax.axvline(x=20, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    ax.text(10, ax.get_ylim()[1]*0.95, 'Age 10\n(Adolescent\nacceleration)',
            ha='center', va='top', fontsize=9, color='gray')
    ax.text(20, ax.get_ylim()[1]*0.95, 'Age 20\n(Moderation)',
            ha='center', va='top', fontsize=9, color='gray')

    ax.set_xlabel('Age (years)', fontweight='bold')
    ax.set_ylabel('eGFR Decline Rate (ml/min/1.73m²/year)', fontweight='bold')
    ax.set_title('Age-Varying eGFR Decline Rates by Treatment Scenario\n(Recalibrated Model)',
                 fontweight='bold', fontsize=14)
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 3.5)

    plt.tight_layout()
    plt.savefig('figure1_age_varying_rates_recalibrated.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved: figure1_age_varying_rates_recalibrated.png")
    plt.close()


def generate_figure2_egfr_trajectories():
    """
    Figure 2: eGFR trajectories showing progression through CKD stages
    """
    print("\nGenerating Figure 2: eGFR trajectories...")

    params = ModelParameters()
    model = MarkovCohortModel(params)

    scenarios = {
        'Natural History': (params.natural_decline_rate, False),
        'Optimistic (θ=1.0)': (0.30, True),
        'Realistic (θ=0.85)': (0.52, True),
        'Conservative (θ=0.70)': (0.74, True),
        'Pessimistic (θ=0.50)': (1.04, True)
    }

    fig, ax = plt.subplots(figsize=(14, 9))

    colors = {
        'Natural History': '#d62728',
        'Optimistic (θ=1.0)': '#2ca02c',
        'Realistic (θ=0.85)': '#1f77b4',
        'Conservative (θ=0.70)': '#ff7f0e',
        'Pessimistic (θ=0.50)': '#9467bd'
    }

    for scenario_name, (decline_rate, include_cost) in scenarios.items():
        result = model.run_model(decline_rate, scenario_name, include_cost)

        # Plot eGFR trajectory
        ages = params.starting_age + np.arange(len(result['egfr_track']))
        ax.plot(ages, result['egfr_track'],
                label=scenario_name,
                color=colors[scenario_name],
                linewidth=3.0 if 'Realistic' in scenario_name else 2.0,
                alpha=0.85)

    # Add CKD stage thresholds
    ckd_stages = [
        (90, 'CKD Stage 1/2 boundary', '#e0e0e0'),
        (60, 'CKD Stage 3a', '#ffeb99'),
        (45, 'CKD Stage 3b', '#ffc266'),
        (30, 'CKD Stage 4', '#ff9933'),
        (15, 'ESKD', '#ff4d4d')
    ]

    for threshold, label, color in ckd_stages:
        ax.axhline(y=threshold, color='gray', linestyle='--', alpha=0.4, linewidth=1)
        ax.text(params.starting_age + 1, threshold + 1, label,
                fontsize=9, color='gray', va='bottom')

    # Shade CKD stage regions
    ax.axhspan(60, 90, alpha=0.05, color='yellow', label='CKD 2')
    ax.axhspan(45, 60, alpha=0.07, color='orange', label='CKD 3a')
    ax.axhspan(30, 45, alpha=0.09, color='orange', label='CKD 3b')
    ax.axhspan(15, 30, alpha=0.11, color='red', label='CKD 4')
    ax.axhspan(0, 15, alpha=0.13, color='darkred', label='ESKD')

    ax.set_xlabel('Age (years)', fontweight='bold')
    ax.set_ylabel('eGFR (ml/min/1.73m²)', fontweight='bold')
    ax.set_title('eGFR Trajectories Through CKD Stages by Treatment Scenario\n(Recalibrated Model)',
                 fontweight='bold', fontsize=14)
    ax.legend(loc='upper right', frameon=True, shadow=True, ncol=1)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(params.starting_age, 70)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig('figure2_egfr_trajectories_recalibrated.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved: figure2_egfr_trajectories_recalibrated.png")
    plt.close()


def generate_figure3_waning_effect():
    """
    Figure 3: Treatment waning effect - comparing sustained vs waning treatment
    """
    print("\nGenerating Figure 3: Treatment waning effect...")

    params = ModelParameters()
    model = MarkovCohortModel(params)

    # Run sustained optimistic scenario
    sustained = model.run_model(0.30, "Sustained Optimistic", True)

    # Run waning scenario
    waning = model.run_model(
        egfr_decline_rate=0.30,
        scenario_name="Treatment Waning",
        include_gene_therapy_cost=True,
        treatment_waning=True,
        waning_start_year=10,
        waning_decline_rate=0.74  # Wanes to conservative (θ=0.70)
    )

    # Also run natural history for reference
    nh = model.run_model(params.natural_decline_rate, "Natural History", False)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    ages = params.starting_age + np.arange(len(sustained['egfr_track']))

    # Panel 1: eGFR trajectories
    ax1.plot(ages, nh['egfr_track'], label='Natural History',
             color='#d62728', linestyle='--', linewidth=2.5, alpha=0.7)
    ax1.plot(ages, sustained['egfr_track'], label='Sustained Optimistic (θ=1.0)',
             color='#2ca02c', linewidth=2.5, alpha=0.85)
    ax1.plot(ages, waning['egfr_track'], label='Waning (θ=1.0 → 0.70 over years 10-20)',
             color='#1f77b4', linewidth=2.5, alpha=0.85)

    # Add waning period indicator
    waning_start_age = params.starting_age + 10
    waning_end_age = params.starting_age + 20
    ax1.axvspan(waning_start_age, waning_end_age, alpha=0.15, color='orange',
                label='Waning Period (10 years)')

    # Add CKD stage thresholds
    for threshold, label in [(90, 'CKD 2'), (60, 'CKD 3a'), (30, 'CKD 4'), (15, 'ESKD')]:
        ax1.axhline(y=threshold, color='gray', linestyle=':', alpha=0.3, linewidth=1)

    ax1.set_xlabel('Age (years)', fontweight='bold')
    ax1.set_ylabel('eGFR (ml/min/1.73m²)', fontweight='bold')
    ax1.set_title('Treatment Waning Effect on eGFR Trajectory', fontweight='bold', fontsize=14)
    ax1.legend(loc='upper right', frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(params.starting_age, 70)
    ax1.set_ylim(0, 100)

    # Panel 2: Decline rates over time
    decline_rates_sustained = [model.get_decline_rate(age, 0.30) for age in ages]

    # Calculate waning decline rates
    decline_rates_waning = []
    for cycle, age in enumerate(ages):
        if cycle < 10:
            rate = model.get_decline_rate(age, 0.30)  # Full effect
        elif cycle < 20:
            # Gradual waning
            waning_fraction = (cycle - 10) / 10
            initial_rate = model.get_decline_rate(age, 0.30)
            final_rate = model.get_decline_rate(age, 0.74)
            rate = initial_rate + waning_fraction * (final_rate - initial_rate)
        else:
            rate = model.get_decline_rate(age, 0.74)  # Fully waned
        decline_rates_waning.append(rate)

    decline_rates_nh = [model.get_decline_rate(age, params.natural_decline_rate) for age in ages]

    ax2.plot(ages, decline_rates_nh, label='Natural History',
             color='#d62728', linestyle='--', linewidth=2.5, alpha=0.7)
    ax2.plot(ages, decline_rates_sustained, label='Sustained Optimistic',
             color='#2ca02c', linewidth=2.5, alpha=0.85)
    ax2.plot(ages, decline_rates_waning, label='Waning Treatment',
             color='#1f77b4', linewidth=2.5, alpha=0.85)

    # Add waning period indicator
    ax2.axvspan(waning_start_age, waning_end_age, alpha=0.15, color='orange')

    ax2.set_xlabel('Age (years)', fontweight='bold')
    ax2.set_ylabel('eGFR Decline Rate (ml/min/1.73m²/year)', fontweight='bold')
    ax2.set_title('Decline Rates During Treatment Waning', fontweight='bold', fontsize=14)
    ax2.legend(loc='upper right', frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(params.starting_age, 70)
    ax2.set_ylim(0, 3.5)

    plt.tight_layout()
    plt.savefig('figure3_waning_effect_recalibrated.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved: figure3_waning_effect_recalibrated.png")
    plt.close()


def generate_figure4_ce_plane():
    """
    Figure 4: Cost-effectiveness plane with all scenarios
    """
    print("\nGenerating Figure 4: Cost-effectiveness plane...")

    params = ModelParameters()
    analysis = ScenarioAnalysis(params)
    all_results = analysis.run_all_scenarios()

    # Get baseline
    baseline = all_results['Scenario 0: Natural History']

    # Calculate incremental outcomes
    scenarios_data = []

    scenario_info = {
        'Scenario 1: Optimistic': ('Optimistic\n(θ=1.0)', '#2ca02c', 'o', 200),
        'Scenario 2: Realistic': ('Realistic\n(θ=0.85)', '#1f77b4', 's', 250),
        'Scenario 3: Conservative': ('Conservative\n(θ=0.70)', '#ff7f0e', '^', 200),
        'Scenario 4: Pessimistic': ('Pessimistic\n(θ=0.50)', '#9467bd', 'v', 200),
        'Scenario 5: Treatment Waning': ('Treatment\nWaning', '#e377c2', 'D', 200)
    }

    for scenario_name, (label, color, marker, size) in scenario_info.items():
        if scenario_name in all_results:
            result = all_results[scenario_name]
            inc_qalys = result['total_qalys'] - baseline['total_qalys']
            inc_costs = result['total_costs'] - baseline['total_costs']

            scenarios_data.append({
                'name': label,
                'inc_qalys': inc_qalys,
                'inc_costs': inc_costs,
                'icer': inc_costs / inc_qalys if inc_qalys > 0 else 0,
                'color': color,
                'marker': marker,
                'size': size
            })

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 9))

    # Plot origin (natural history)
    ax.scatter([0], [0], s=200, c='red', marker='X',
               label='Natural History\n(Reference)', zorder=5, edgecolors='black', linewidths=1.5)

    # Plot scenarios
    for scenario in scenarios_data:
        ax.scatter([scenario['inc_qalys']], [scenario['inc_costs']/1e6],
                  s=scenario['size'], c=scenario['color'], marker=scenario['marker'],
                  label=scenario['name'], zorder=4, edgecolors='black', linewidths=1.5, alpha=0.85)

    # Add willingness-to-pay threshold lines
    max_qalys = max([s['inc_qalys'] for s in scenarios_data]) * 1.1

    # $300,000/QALY threshold
    qalys_300k = np.linspace(0, max_qalys, 100)
    costs_300k = 300000 * qalys_300k / 1e6
    ax.plot(qalys_300k, costs_300k, 'g--', linewidth=2, alpha=0.6,
            label='WTP: $300K/QALY')

    # $500,000/QALY threshold
    costs_500k = 500000 * qalys_300k / 1e6
    ax.plot(qalys_300k, costs_500k, 'orange', linestyle='--', linewidth=2, alpha=0.6,
            label='WTP: $500K/QALY')

    # Annotations
    for scenario in scenarios_data:
        if 'Realistic' in scenario['name']:
            ax.annotate(f"ICER: ${scenario['icer']:,.0f}/QALY",
                       xy=(scenario['inc_qalys'], scenario['inc_costs']/1e6),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1.5))

    ax.set_xlabel('Incremental QALYs vs Natural History', fontweight='bold', fontsize=13)
    ax.set_ylabel('Incremental Costs vs Natural History ($ Millions)', fontweight='bold', fontsize=13)
    ax.set_title('Cost-Effectiveness Plane: Gene Therapy Scenarios\n(Recalibrated Model, 1.5% Discount Rate)',
                 fontweight='bold', fontsize=14)
    ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, max_qalys)
    ax.set_ylim(-0.5, max([s['inc_costs'] for s in scenarios_data])/1e6 * 1.1)

    plt.tight_layout()
    plt.savefig('figure4_ce_plane_recalibrated.png', dpi=300, bbox_inches='tight')
    print("  ✓ Saved: figure4_ce_plane_recalibrated.png")
    plt.close()


def main():
    """Generate all figures"""
    print("="*80)
    print("GENERATING VISUALIZATION FIGURES (RECALIBRATED MODEL)")
    print("="*80)
    print("\nParameters:")
    params = ModelParameters()
    print(f"  Starting eGFR: {params.starting_egfr} ml/min/1.73m²")
    print(f"  Decline rates: {params.decline_rate_early}, {params.decline_rate_middle}, {params.decline_rate_late} ml/min/yr")
    print(f"  Discount rate: {params.discount_rate*100}%")
    print("\nGenerating 4 publication-quality figures...")

    generate_figure1_decline_rates()
    generate_figure2_egfr_trajectories()
    generate_figure3_waning_effect()
    generate_figure4_ce_plane()

    print("\n" + "="*80)
    print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
    print("="*80)
    print("\nFiles created:")
    print("  1. figure1_age_varying_rates_recalibrated.png")
    print("  2. figure2_egfr_trajectories_recalibrated.png")
    print("  3. figure3_waning_effect_recalibrated.png")
    print("  4. figure4_ce_plane_recalibrated.png")
    print("\nThese figures reflect the recalibrated model with:")
    print("  • eGFR₀ = 95 ml/min/1.73m²")
    print("  • Moderated decline rates (3.5→3.0, 2.0→1.5)")
    print("  • Realistic scenario: θ=0.85 (85% pathological reduction)")
    print("  • Discount rate: 1.5%")


if __name__ == "__main__":
    main()
