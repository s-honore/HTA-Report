"""
HTA Report Figure Generation Module

Generates publication-quality figures for Lowe Syndrome Gene Therapy HTA Report
with consistent styling and branding.

Author: Sebastian Honoré
Date: November 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# STYLE CONFIGURATION
# ============================================================================

class CureLoweBrandStyle:
    """Cure Lowe Foundation brand colors and styling configuration."""

    # Core Brand Colors (3-color palette as requested)
    ULTRAMARINE_BLUE = '#2F6CD6'  # Primary: Trust, reliability, best outcomes
    ORANGE_SHAKE = '#F3A87B'       # Emphasis: Warmth, worst outcomes
    PAYNES_GRAY = '#262626'        # Text: Body text, baseline/reference

    # Keep secondary colors for specific uses only
    IVORY = '#F1ECE2'              # Background (not for data)
    LIME = '#D9FBC8'               # Removed from primary use - was unreadable

    # Gradient from Ultramarine (best) to Orange (worst) for treatment scenarios
    # Created by interpolating between Ultramarine and Orange in color space
    COLOR_1_ULTRAMARINE = '#2F6CD6'    # Best scenario
    COLOR_2_BLUE_ORANGE = '#4B7AC9'    # Blend: mostly blue
    COLOR_3_MID_BLEND = '#678ABD'      # Middle blend
    COLOR_4_ORANGE_BLUE = '#8E96AA'    # Blend: mostly orange
    COLOR_5_ORANGE = '#F3A87B'         # Worst scenario

    # Accent colors for secondary y-axis and highlights
    ACCENT_BLUE_LIGHT = '#7AA5E8'      # Lighter blue for secondary axis
    ACCENT_ORANGE_LIGHT = '#F5B896'    # Lighter orange for secondary axis

    # Scenario colors: Gradient from best (blue) to worst (orange)
    SCENARIO_COLORS = {
        'Natural History': PAYNES_GRAY,      # Dark gray for baseline
        'Optimistic': COLOR_1_ULTRAMARINE,   # Best: Pure Ultramarine
        'Realistic': COLOR_2_BLUE_ORANGE,    # Good: Mostly blue
        'Conservative': COLOR_3_MID_BLEND,   # Moderate: Mid blend
        'Pessimistic': COLOR_5_ORANGE,       # Worst: Orange Shake
        'Waning': COLOR_4_ORANGE_BLUE        # Variable: Orange-leaning blend
    }

    # Typography
    FONT_SIZE = 14
    TITLE_SIZE = 16
    LABEL_SIZE = 14
    TICK_SIZE = 12
    LEGEND_SIZE = 12

    # Layout
    DPI = 300
    FIGURE_WIDTH = 12
    FIGURE_HEIGHT = 8

    @staticmethod
    def apply_style(ax, show_top_spine=False):
        """
        Apply consistent styling to matplotlib axes.

        Args:
            ax: Matplotlib axes object
            show_top_spine: Whether to show top spine (default: False)
        """
        # Remove top and right spines
        ax.spines['top'].set_visible(show_top_spine)
        ax.spines['right'].set_visible(False)

        # Style remaining spines
        ax.spines['left'].set_color(CureLoweBrandStyle.PAYNES_GRAY)
        ax.spines['bottom'].set_color(CureLoweBrandStyle.PAYNES_GRAY)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

        # Grid lines (horizontal only)
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8,
                color=CureLoweBrandStyle.PAYNES_GRAY)
        ax.set_axisbelow(True)

        # Tick parameters
        ax.tick_params(colors=CureLoweBrandStyle.PAYNES_GRAY,
                      labelsize=CureLoweBrandStyle.TICK_SIZE)

        # Labels
        ax.xaxis.label.set_color(CureLoweBrandStyle.PAYNES_GRAY)
        ax.yaxis.label.set_color(CureLoweBrandStyle.PAYNES_GRAY)
        ax.xaxis.label.set_size(CureLoweBrandStyle.LABEL_SIZE)
        ax.yaxis.label.set_size(CureLoweBrandStyle.LABEL_SIZE)

    @staticmethod
    def setup_figure(figsize=None, transparent=True):
        """
        Create figure with brand styling.

        Args:
            figsize: Tuple of (width, height). Default uses brand standard.
            transparent: Whether to use transparent background.

        Returns:
            Figure and axes objects
        """
        if figsize is None:
            figsize = (CureLoweBrandStyle.FIGURE_WIDTH,
                      CureLoweBrandStyle.FIGURE_HEIGHT)

        fig, ax = plt.subplots(figsize=figsize, dpi=CureLoweBrandStyle.DPI)

        # Transparent background
        if transparent:
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)

        return fig, ax

    @staticmethod
    def add_legend(ax, **kwargs):
        """Add legend with consistent styling at bottom."""
        legend_defaults = {
            'loc': 'upper center',
            'bbox_to_anchor': (0.5, -0.12),
            'ncol': 3,
            'frameon': False,
            'fontsize': CureLoweBrandStyle.LEGEND_SIZE
        }
        legend_defaults.update(kwargs)
        return ax.legend(**legend_defaults)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_currency(value, decimals=0):
    """Format value as euros."""
    if abs(value) >= 1e6:
        return f"€{value/1e6:.{decimals}f}M"
    elif abs(value) >= 1e3:
        return f"€{value/1e3:.{decimals}f}K"
    else:
        return f"€{value:.{decimals}f}"


def add_value_labels(ax, bars, format_func=None, fontsize=10):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            label = format_func(height) if format_func else f'{height:.1f}'
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   label, ha='center', va='bottom',
                   fontsize=fontsize,
                   color=CureLoweBrandStyle.PAYNES_GRAY)


# ============================================================================
# FIGURE 1: TREATMENT SCENARIOS COMPARISON
# ============================================================================

def generate_scenario_comparison(results: Dict, output_path: str):
    """
    Generate multi-panel comparison of treatment scenarios.

    Shows QALYs, evLYG, Costs, and ICERs across all scenarios.

    Args:
        results: Dictionary of scenario results from model
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()

    # Extract data
    scenarios = []
    qalys = []
    evlygs = []
    costs = []
    icers_qaly = []

    for name, res in results.items():
        if 'Natural History' in name:
            continue  # Skip baseline

        scenario_short = name.replace('Scenario ', '').replace(': ', '\n')
        scenarios.append(scenario_short)
        qalys.append(res.get('incremental_qalys', 0))
        evlygs.append(res.get('evlyg', 0))
        costs.append(res.get('incremental_costs', 0))
        icers_qaly.append(res.get('icer_qaly', 0))

    # Create figure with 2x2 subplots
    fig = plt.figure(figsize=(14, 10), dpi=style.DPI)
    fig.patch.set_alpha(0)
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Incremental QALYs
    ax1 = fig.add_subplot(gs[0, 0])
    bars1 = ax1.bar(range(len(scenarios)), qalys,
                    color=style.ULTRAMARINE_BLUE, alpha=0.8)
    ax1.set_ylabel('Incremental QALYs', fontsize=style.LABEL_SIZE,
                   color=style.PAYNES_GRAY)
    ax1.set_title('A. Quality-Adjusted Life Years Gained',
                  fontsize=style.TITLE_SIZE, color=style.PAYNES_GRAY,
                  loc='left', fontweight='bold')
    ax1.set_xticks(range(len(scenarios)))
    ax1.set_xticklabels(scenarios, fontsize=style.TICK_SIZE)
    style.apply_style(ax1)
    add_value_labels(ax1, bars1, lambda x: f'{x:.2f}', fontsize=11)

    # Panel B: evLYG
    ax2 = fig.add_subplot(gs[0, 1])
    bars2 = ax2.bar(range(len(scenarios)), evlygs,
                    color=style.ORANGE_SHAKE, alpha=0.8)
    ax2.set_ylabel('Equal-Value Life Years Gained', fontsize=style.LABEL_SIZE,
                   color=style.PAYNES_GRAY)
    ax2.set_title('B. Normalized Life Years Gained',
                  fontsize=style.TITLE_SIZE, color=style.PAYNES_GRAY,
                  loc='left', fontweight='bold')
    ax2.set_xticks(range(len(scenarios)))
    ax2.set_xticklabels(scenarios, fontsize=style.TICK_SIZE)
    style.apply_style(ax2)
    add_value_labels(ax2, bars2, lambda x: f'{x:.2f}', fontsize=11)

    # Panel C: Incremental Costs
    ax3 = fig.add_subplot(gs[1, 0])
    bars3 = ax3.bar(range(len(scenarios)),
                    [c/1e6 for c in costs],  # Convert to millions
                    color=style.ACCENT_ORANGE_LIGHT, alpha=0.8)
    ax3.set_ylabel('Incremental Costs (€ millions)', fontsize=style.LABEL_SIZE,
                   color=style.PAYNES_GRAY)
    ax3.set_title('C. Additional Costs vs Natural History',
                  fontsize=style.TITLE_SIZE, color=style.PAYNES_GRAY,
                  loc='left', fontweight='bold')
    ax3.set_xticks(range(len(scenarios)))
    ax3.set_xticklabels(scenarios, fontsize=style.TICK_SIZE)
    style.apply_style(ax3)
    add_value_labels(ax3, bars3, lambda x: f'€{x:.2f}M', fontsize=11)

    # Panel D: ICER per QALY
    ax4 = fig.add_subplot(gs[1, 1])

    # Filter out infinite ICERs
    icer_vals = [i/1e3 if abs(i) < 1e10 else 0 for i in icers_qaly]
    bars4 = ax4.bar(range(len(scenarios)), icer_vals,
                    color=style.PAYNES_GRAY, alpha=0.8)

    # Add threshold lines
    ax4.axhline(y=100, color=style.ULTRAMARINE_BLUE, linestyle='--',
                linewidth=2, alpha=0.7, label='€100K threshold')
    ax4.axhline(y=300, color=style.ORANGE_SHAKE, linestyle='--',
                linewidth=2, alpha=0.7, label='€300K threshold (ultra-rare)')

    ax4.set_ylabel('ICER (€ thousands per QALY)', fontsize=style.LABEL_SIZE,
                   color=style.PAYNES_GRAY)
    ax4.set_title('D. Cost-Effectiveness Ratios',
                  fontsize=style.TITLE_SIZE, color=style.PAYNES_GRAY,
                  loc='left', fontweight='bold')
    ax4.set_xticks(range(len(scenarios)))
    ax4.set_xticklabels(scenarios, fontsize=style.TICK_SIZE)
    style.apply_style(ax4)
    add_value_labels(ax4, bars4, lambda x: f'€{x:.0f}K' if x > 0 else 'N/A',
                    fontsize=11)
    ax4.legend(loc='upper right', frameon=False, fontsize=style.LEGEND_SIZE)

    # Add overall title
    fig.suptitle('Treatment Scenario Comparison: Health Outcomes and Cost-Effectiveness',
                fontsize=18, fontweight='bold', color=style.PAYNES_GRAY, y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 2: eGFR TRAJECTORIES
# ============================================================================

def generate_egfr_trajectories(results: Dict, output_path: str):
    """
    Generate eGFR decline trajectories over time.

    Shows how kidney function declines under different scenarios.

    Args:
        results: Dictionary of scenario results from model
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure(figsize=(14, 8))

    # Plot each scenario
    for name, res in results.items():
        egfr_track = res.get('egfr_track', [])
        if len(egfr_track) == 0:
            continue

        # Determine color
        if 'Natural History' in name:
            color = style.SCENARIO_COLORS['Natural History']
            linewidth = 3
            linestyle = '--'
            label = 'Natural History (baseline)'
        elif 'Optimistic' in name or '1:' in name:
            color = style.SCENARIO_COLORS['Optimistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Optimistic'
        elif 'Realistic' in name or '2:' in name:
            color = style.SCENARIO_COLORS['Realistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Realistic'
        elif 'Conservative' in name or '3:' in name:
            color = style.SCENARIO_COLORS['Conservative']
            linewidth = 2.5
            linestyle = '-'
            label = 'Conservative'
        elif 'Pessimistic' in name or '4:' in name:
            color = style.SCENARIO_COLORS['Pessimistic']
            linewidth = 2
            linestyle = '-'
            label = 'Pessimistic'
        elif 'Waning' in name or '5:' in name:
            color = style.SCENARIO_COLORS['Waning']
            linewidth = 2
            linestyle = ':'
            label = 'Treatment Waning'
        else:
            continue

        # Plot trajectory
        years = np.arange(len(egfr_track))
        ax.plot(years, egfr_track, color=color, linewidth=linewidth,
               linestyle=linestyle, label=label, alpha=0.9)

    # Add CKD stage thresholds as gridlines (only at these values)
    ckd_thresholds = [90, 60, 45, 30, 15]
    for threshold in ckd_thresholds:
        ax.axhline(y=threshold, color=style.PAYNES_GRAY, linestyle='-',
                  linewidth=1, alpha=0.3, zorder=1)

    # Add stage labels
    ax.text(2, 95, 'Normal/CKD1', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.7, fontweight='bold')
    ax.text(2, 75, 'CKD Stage 2', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.6)
    ax.text(2, 52, 'CKD Stage 3a', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.6)
    ax.text(2, 37, 'CKD Stage 3b', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.6)
    ax.text(2, 22, 'CKD Stage 4', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.6)
    ax.text(2, 7, 'CKD Stage 5/ESKD', fontsize=10, color=style.PAYNES_GRAY,
           alpha=0.6)

    # Labels and title
    ax.set_xlabel('Years Since Treatment', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_ylabel('eGFR (ml/min/1.73m²)', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_title('Kidney Function Trajectories by Treatment Scenario',
                fontsize=18, color=style.PAYNES_GRAY, pad=20,
                fontweight='bold')

    # Styling - apply but turn off default gridlines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.tick_params(labelsize=style.TICK_SIZE, colors=style.PAYNES_GRAY)
    ax.grid(False)  # Turn off default grid - we added custom gridlines above

    # Add legend
    style.add_legend(ax, ncol=2)

    # Set limits
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 3: POPULATION HEALTH STATES OVER TIME
# ============================================================================

def generate_population_states(results: Dict, output_path: str,
                               scenario_name: str = 'Scenario 0: Natural History'):
    """
    Generate stacked area chart showing distribution across CKD stages.

    Args:
        results: Dictionary of scenario results
        output_path: Path to save figure
        scenario_name: Which scenario to visualize (default: Natural History)
    """
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure(figsize=(14, 8))

    # Get trace data
    trace = results[scenario_name]['trace']
    years = np.arange(len(trace))

    # State names (including Normal state now)
    states = ['Normal', 'CKD2', 'CKD3a', 'CKD3b', 'CKD4', 'ESKD', 'Death']

    # Colors for states (gradient from best to worst: light blue → orange → red)
    state_colors = [
        '#A8D5F7',           # Normal - very light blue (best)
        '#7AA5E8',           # CKD2 - light blue
        style.ULTRAMARINE_BLUE,  # CKD3a - ultramarine blue
        style.COLOR_3_MID_BLEND,  # CKD3b - blue-orange blend
        style.ORANGE_SHAKE,   # CKD4 - orange (getting worse)
        '#D9534F',           # ESKD - red (severe)
        style.PAYNES_GRAY    # Death - gray
    ]

    # Create stacked area plot
    ax.stackplot(years, trace.T, labels=states, colors=state_colors, alpha=0.8)

    # Labels and title
    ax.set_xlabel('Years Since Age 1', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_ylabel('Proportion of Cohort', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')

    scenario_display = scenario_name.replace('Scenario 0: ', '')
    ax.set_title(f'Disease Progression Over Time: {scenario_display}',
                fontsize=18, color=style.PAYNES_GRAY, pad=20,
                fontweight='bold')

    # Styling
    style.apply_style(ax)
    style.add_legend(ax, ncol=6, bbox_to_anchor=(0.5, -0.08))

    # Set limits
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 1)

    # Y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 4: CUMULATIVE COSTS OVER AGE (DUAL Y-AXIS)
# ============================================================================

def generate_cost_over_age(results: Dict, output_path: str):
    """
    Generate cumulative cost curves over patient age with dual y-axis.

    Left axis: Cumulative costs
    Right axis: Annual costs

    Args:
        results: Dictionary of scenario results
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax1 = style.setup_figure(figsize=(14, 8))

    # Create second y-axis
    ax2 = ax1.twinx()

    # Starting age (from model parameters)
    starting_age = 1  # Adjust if different in your model

    # Plot cumulative costs on left axis
    for name, res in results.items():
        costs_by_cycle = res.get('discounted_costs_by_cycle', [])
        if len(costs_by_cycle) == 0:
            continue

        # Calculate cumulative costs
        cumulative_costs = np.cumsum(costs_by_cycle) / 1e6  # Convert to millions
        ages = np.arange(len(cumulative_costs)) + starting_age

        # Determine style
        if 'Natural History' in name:
            color = style.SCENARIO_COLORS['Natural History']
            linewidth = 3
            linestyle = '--'
            label = 'Natural History'
        elif 'Optimistic' in name or '1:' in name:
            color = style.SCENARIO_COLORS['Optimistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Optimistic'
        elif 'Realistic' in name or '2:' in name:
            color = style.SCENARIO_COLORS['Realistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Realistic'
        else:
            continue  # Skip other scenarios for clarity

        # Plot cumulative costs
        ax1.plot(ages[:50], cumulative_costs[:50], color=color,
                linewidth=linewidth, linestyle=linestyle,
                label=label, alpha=0.9)

    # Plot annual costs on right axis (just for Natural History as reference)
    nat_hist = results.get('Scenario 0: Natural History', {})
    annual_costs = nat_hist.get('costs_by_cycle', [])
    if len(annual_costs) > 0:
        ages = np.arange(len(annual_costs)) + starting_age
        ax2.plot(ages[:50], np.array(annual_costs[:50])/1e3,
                color=style.ACCENT_BLUE_LIGHT, linewidth=2, linestyle=':',
                alpha=0.7, label='Annual cost (Natural History)')

    # Left y-axis (cumulative) - primary axis styling
    ax1.set_ylabel('Cumulative Discounted Costs (€ millions)',
                  fontsize=style.LABEL_SIZE, color=style.PAYNES_GRAY,
                  fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=style.PAYNES_GRAY, labelsize=style.TICK_SIZE)

    # Right y-axis (annual) - IDENTICAL formatting to primary axis
    ax2.set_ylabel('Annual Costs (€ thousands)',
                  fontsize=style.LABEL_SIZE, color=style.PAYNES_GRAY,
                  fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=style.PAYNES_GRAY, labelsize=style.TICK_SIZE)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(style.PAYNES_GRAY)
    ax2.spines['right'].set_linewidth(1.5)

    # X-axis
    ax1.set_xlabel('Patient Age (years)', fontsize=style.LABEL_SIZE,
                  color=style.PAYNES_GRAY, fontweight='bold')

    # Title
    ax1.set_title('Lifetime Cost Accumulation by Treatment Scenario',
                 fontsize=18, color=style.PAYNES_GRAY, pad=20,
                 fontweight='bold')

    # Styling
    style.apply_style(ax1, show_top_spine=False)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
              loc='upper center', bbox_to_anchor=(0.5, -0.08),
              ncol=4, frameon=False, fontsize=style.LEGEND_SIZE)

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 5: VALUE-BASED PRICING HEATMAP
# ============================================================================

def generate_pricing_heatmap(pricing_df: pd.DataFrame, output_path: str):
    """
    Generate heatmap showing max justified price by scenario and threshold.

    Args:
        pricing_df: DataFrame from value_based_pricing_analysis
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure(figsize=(12, 8))

    # Extract QALY-based pricing columns
    qaly_cols = [col for col in pricing_df.columns if 'QALY:' in col]

    # Prepare data matrix
    scenarios = pricing_df['Scenario'].values
    data = pricing_df[qaly_cols].values / 1e6  # Convert to millions

    # Create heatmap
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto', alpha=0.9)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label('Maximum Justified Price (€ millions)',
                  fontsize=style.LABEL_SIZE, color=style.PAYNES_GRAY)
    cbar.ax.tick_params(labelsize=style.TICK_SIZE, colors=style.PAYNES_GRAY)

    # Set ticks
    ax.set_xticks(np.arange(len(qaly_cols)))
    ax.set_yticks(np.arange(len(scenarios)))

    # Labels
    threshold_labels = [col.replace('QALY: ', '').replace('€', '€\n')
                       for col in qaly_cols]
    scenario_labels = [s.replace('Scenario ', 'S').replace(': ', '\n')
                      for s in scenarios]

    ax.set_xticklabels(threshold_labels, fontsize=style.TICK_SIZE)
    ax.set_yticklabels(scenario_labels, fontsize=style.TICK_SIZE)

    # Add value annotations
    for i in range(len(scenarios)):
        for j in range(len(qaly_cols)):
            value = data[i, j]
            text_color = 'white' if value > data.max() * 0.6 else style.PAYNES_GRAY
            ax.text(j, i, f'€{value:.1f}M',
                   ha="center", va="center",
                   fontsize=11, color=text_color, fontweight='bold')

    # Axis labels
    ax.set_xlabel('Cost-Effectiveness Threshold', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_ylabel('Treatment Scenario', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')

    # Title
    ax.set_title('Value-Based Pricing: Maximum Justified Gene Therapy Price',
                fontsize=18, color=style.PAYNES_GRAY, pad=20,
                fontweight='bold')

    # Remove spines for heatmap
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(colors=style.PAYNES_GRAY, labelsize=style.TICK_SIZE)

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 6: COST-EFFECTIVENESS PLANE
# ============================================================================

def generate_ce_plane(results: Dict, output_path: str):
    """
    Generate cost-effectiveness plane with WTP thresholds.

    Args:
        results: Dictionary of scenario results
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure(figsize=(12, 10))

    # Extract data
    scenarios = []
    inc_costs = []
    inc_qalys = []
    colors = []

    for name, res in results.items():
        if 'Natural History' in name:
            continue

        scenarios.append(name.replace('Scenario ', 'S').replace(': ', '\n'))
        inc_costs.append(res.get('incremental_costs', 0) / 1e6)  # Millions
        inc_qalys.append(res.get('incremental_qalys', 0))

        # Assign colors
        if 'Optimistic' in name or '1:' in name:
            colors.append(style.SCENARIO_COLORS['Optimistic'])
        elif 'Realistic' in name or '2:' in name:
            colors.append(style.SCENARIO_COLORS['Realistic'])
        elif 'Conservative' in name or '3:' in name:
            colors.append(style.SCENARIO_COLORS['Conservative'])
        elif 'Pessimistic' in name or '4:' in name:
            colors.append(style.SCENARIO_COLORS['Pessimistic'])
        elif 'Waning' in name or '5:' in name:
            colors.append(style.SCENARIO_COLORS['Waning'])
        else:
            colors.append(style.PAYNES_GRAY)

    # Plot scenarios with larger, more visible dots
    for i, (scenario, cost, qaly, color) in enumerate(zip(scenarios, inc_costs, inc_qalys, colors)):
        ax.scatter(qaly, cost, s=600, color=color, alpha=0.9,
                  edgecolors=style.PAYNES_GRAY, linewidth=3,
                  label=scenario, zorder=5)

        # Add labels
        ax.annotate(scenario, (qaly, cost), xytext=(10, 10),
                   textcoords='offset points', fontsize=10,
                   color=style.PAYNES_GRAY, fontweight='bold')

    # Add WTP threshold lines
    max_qaly = max(inc_qalys) * 1.1
    thresholds = [100000, 150000, 300000]
    threshold_labels = ['€100K/QALY\n(Conventional)',
                       '€150K/QALY\n(High-value)',
                       '€300K/QALY\n(Ultra-rare)']
    threshold_colors = [style.ULTRAMARINE_BLUE, style.COLOR_3_MID_BLEND, style.ORANGE_SHAKE]

    for threshold, label, color in zip(thresholds, threshold_labels, threshold_colors):
        qaly_range = np.linspace(0, max_qaly, 100)
        cost_line = (threshold * qaly_range) / 1e6  # Convert to millions
        ax.plot(qaly_range, cost_line, linestyle='--', linewidth=2,
               color=color, alpha=0.7, label=label)

    # Axes
    ax.set_xlabel('Incremental QALYs', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_ylabel('Incremental Costs (€ millions)', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')

    # Title
    ax.set_title('Cost-Effectiveness Plane: Gene Therapy vs Natural History',
                fontsize=18, color=style.PAYNES_GRAY, pad=20,
                fontweight='bold')

    # Styling
    style.apply_style(ax)

    # Set limits
    ax.set_xlim(0, max_qaly)
    ax.set_ylim(bottom=0)

    # Legend (scenarios only, not threshold lines for clarity)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
             ncol=3, frameon=False, fontsize=style.LEGEND_SIZE)

    # Add annotation about thresholds
    ax.text(0.98, 0.98, 'Dashed lines = WTP thresholds',
           transform=ax.transAxes, fontsize=11,
           verticalalignment='top', horizontalalignment='right',
           color=style.PAYNES_GRAY, style='italic',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 7: SURVIVAL CURVES
# ============================================================================

def generate_survival_curves(results: Dict, output_path: str):
    """
    Generate survival probability curves by scenario.

    Args:
        results: Dictionary of scenario results
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax = style.setup_figure(figsize=(14, 8))

    # Starting age
    starting_age = 1

    # Plot each scenario
    for name, res in results.items():
        trace = res.get('trace', np.array([]))
        if trace.size == 0:
            print(f"Warning: No trace data for scenario '{name}'")
            continue

        # Calculate survival (1 - proportion dead)
        death_idx = -1  # Assuming Death is last state
        survival = 1 - trace[:, death_idx]
        ages = np.arange(len(survival)) + starting_age

        # Determine style - check all treatment scenarios
        plot_scenario = False
        if 'Natural History' in name or '0:' in name:
            color = style.SCENARIO_COLORS['Natural History']
            linewidth = 3
            linestyle = '--'
            label = 'Natural History'
            plot_scenario = True
        elif 'Optimistic' in name or 'Scenario 1' in name:
            color = style.SCENARIO_COLORS['Optimistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Optimistic'
            plot_scenario = True
        elif 'Realistic' in name or 'Scenario 2' in name:
            color = style.SCENARIO_COLORS['Realistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Realistic'
            plot_scenario = True
        elif 'Conservative' in name or 'Scenario 3' in name:
            color = style.SCENARIO_COLORS['Conservative']
            linewidth = 2
            linestyle = '-'
            label = 'Conservative'
            plot_scenario = True
        elif 'Pessimistic' in name or 'Scenario 4' in name:
            color = style.SCENARIO_COLORS['Pessimistic']
            linewidth = 2
            linestyle = '-'
            label = 'Pessimistic'
            plot_scenario = True

        if not plot_scenario:
            print(f"Skipping scenario '{name}' (not in main scenarios)")
            continue

        # Plot survival curve
        ax.plot(ages[:60], survival[:60], color=color,
               linewidth=linewidth, linestyle=linestyle,
               label=label, alpha=0.9)

    # Reference lines
    ax.axhline(y=0.5, color=style.PAYNES_GRAY, linestyle=':',
              linewidth=1, alpha=0.4)
    ax.text(2, 0.52, 'Median Survival', fontsize=10,
           color=style.PAYNES_GRAY, alpha=0.6)

    # Axes
    ax.set_xlabel('Age (years)', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')
    ax.set_ylabel('Survival Probability', fontsize=style.LABEL_SIZE,
                 color=style.PAYNES_GRAY, fontweight='bold')

    # Title
    ax.set_title('Survival Curves by Treatment Scenario',
                fontsize=18, color=style.PAYNES_GRAY, pad=20,
                fontweight='bold')

    # Styling
    style.apply_style(ax)
    style.add_legend(ax, ncol=4)

    # Y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
    ax.set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# FIGURE 8: QALY ACCUMULATION OVER TIME (DUAL Y-AXIS)
# ============================================================================

def generate_qaly_accumulation(results: Dict, output_path: str):
    """
    Generate cumulative QALY/evLYG accumulation curves with dual y-axis.

    Args:
        results: Dictionary of scenario results
        output_path: Path to save figure
    """
    style = CureLoweBrandStyle()
    fig, ax1 = style.setup_figure(figsize=(14, 8))

    # Create second y-axis
    ax2 = ax1.twinx()

    starting_age = 1

    # Plot cumulative QALYs on left axis
    for name, res in results.items():
        qalys_by_cycle = res.get('discounted_qalys_by_cycle', [])
        if len(qalys_by_cycle) == 0:
            continue

        cumulative_qalys = np.cumsum(qalys_by_cycle)
        ages = np.arange(len(cumulative_qalys)) + starting_age

        # Determine style
        if 'Natural History' in name:
            color = style.SCENARIO_COLORS['Natural History']
            linewidth = 3
            linestyle = '--'
            label = 'Natural History'
        elif 'Optimistic' in name or '1:' in name:
            color = style.SCENARIO_COLORS['Optimistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Optimistic'
        elif 'Realistic' in name or '2:' in name:
            color = style.SCENARIO_COLORS['Realistic']
            linewidth = 2.5
            linestyle = '-'
            label = 'Realistic'
        else:
            continue

        # Plot cumulative QALYs
        ax1.plot(ages[:50], cumulative_qalys[:50], color=color,
                linewidth=linewidth, linestyle=linestyle,
                label=label, alpha=0.9)

    # Plot annual QALYs on right axis (Natural History as reference)
    nat_hist = results.get('Scenario 0: Natural History', {})
    annual_qalys = nat_hist.get('qalys_by_cycle', [])
    if len(annual_qalys) > 0:
        ages = np.arange(len(annual_qalys)) + starting_age
        ax2.plot(ages[:50], annual_qalys[:50],
                color=style.ACCENT_BLUE_LIGHT, linewidth=2, linestyle=':',
                alpha=0.7, label='Annual QALYs (Natural History)')

    # Left y-axis (cumulative) - primary axis styling
    ax1.set_ylabel('Cumulative Discounted QALYs',
                  fontsize=style.LABEL_SIZE, color=style.PAYNES_GRAY,
                  fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=style.PAYNES_GRAY, labelsize=style.TICK_SIZE)

    # Right y-axis (annual) - IDENTICAL formatting to primary axis
    ax2.set_ylabel('Annual QALYs',
                  fontsize=style.LABEL_SIZE, color=style.PAYNES_GRAY,
                  fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=style.PAYNES_GRAY, labelsize=style.TICK_SIZE)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(style.PAYNES_GRAY)
    ax2.spines['right'].set_linewidth(1.5)

    # X-axis
    ax1.set_xlabel('Patient Age (years)', fontsize=style.LABEL_SIZE,
                  color=style.PAYNES_GRAY, fontweight='bold')

    # Title
    ax1.set_title('Health Benefit Accumulation Over Patient Lifetime',
                 fontsize=18, color=style.PAYNES_GRAY, pad=20,
                 fontweight='bold')

    # Styling
    style.apply_style(ax1, show_top_spine=False)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
              loc='upper center', bbox_to_anchor=(0.5, -0.08),
              ncol=4, frameon=False, fontsize=style.LEGEND_SIZE)

    plt.tight_layout()
    plt.savefig(output_path, dpi=style.DPI, bbox_inches='tight',
                transparent=True, format='png')
    plt.close()

    print(f"✓ Generated: {output_path}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def generate_all_figures(results: Dict, pricing_df: pd.DataFrame, output_dir: str):
    """
    Generate all HTA report figures with consistent Cure Lowe branding.

    Args:
        results: Dictionary of scenario results from model
        pricing_df: DataFrame from value_based_pricing_analysis
        output_dir: Directory to save figures
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    print("="*70)
    print("GENERATING HTA REPORT FIGURES - CURE LOWE FOUNDATION")
    print("="*70)
    print()
    print("Style: Ultramarine Blue (#2F6CD6) | Ivory (#F1ECE2)")
    print("       Lime (#D9FBC8) | Orange Shake (#F3A87B)")
    print()

    # Figure 1: Scenario Comparison (4-panel)
    print("[1/8] Generating Scenario Comparison (4-panel)...")
    generate_scenario_comparison(
        results,
        f"{output_dir}/figure1_scenario_comparison.png"
    )

    # Figure 2: eGFR Trajectories
    print("[2/8] Generating eGFR Trajectories...")
    generate_egfr_trajectories(
        results,
        f"{output_dir}/figure2_egfr_trajectories.png"
    )

    # Figure 3: Population Health States (Natural History)
    print("[3/8] Generating Population Health States (Natural History)...")
    generate_population_states(
        results,
        f"{output_dir}/figure3a_population_natural_history.png",
        scenario_name='Scenario 0: Natural History'
    )

    # Figure 3b: Population States (Optimistic Treatment)
    print("[3/8] Generating Population Health States (Optimistic)...")
    generate_population_states(
        results,
        f"{output_dir}/figure3b_population_optimistic.png",
        scenario_name='Scenario 1: Optimistic'
    )

    # Figure 4: Cost Over Age (Dual Y-Axis)
    print("[4/8] Generating Cost Over Age (dual y-axis)...")
    generate_cost_over_age(
        results,
        f"{output_dir}/figure4_cost_over_age.png"
    )

    # Figure 5: Value-Based Pricing Heatmap
    print("[5/8] Generating Value-Based Pricing Heatmap...")
    generate_pricing_heatmap(
        pricing_df,
        f"{output_dir}/figure5_pricing_heatmap.png"
    )

    # Figure 6: Cost-Effectiveness Plane
    print("[6/8] Generating Cost-Effectiveness Plane...")
    generate_ce_plane(
        results,
        f"{output_dir}/figure6_ce_plane.png"
    )

    # Figure 7: Survival Curves
    print("[7/8] Generating Survival Curves...")
    generate_survival_curves(
        results,
        f"{output_dir}/figure7_survival_curves.png"
    )

    # Figure 8: QALY Accumulation (Dual Y-Axis)
    print("[8/8] Generating QALY Accumulation (dual y-axis)...")
    generate_qaly_accumulation(
        results,
        f"{output_dir}/figure8_qaly_accumulation.png"
    )

    print()
    print("="*70)
    print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"\nOutput directory: {output_dir}")
    print(f"Format: PNG, 300 DPI, transparent background")
    print()
    print("Figure List:")
    print("  1. Scenario Comparison (QALYs, evLYG, Costs, ICERs)")
    print("  2. eGFR Trajectories (kidney function decline)")
    print("  3a. Population States - Natural History")
    print("  3b. Population States - Optimistic Treatment")
    print("  4. Cost Over Age (cumulative & annual, dual y-axis)")
    print("  5. Value-Based Pricing Heatmap")
    print("  6. Cost-Effectiveness Plane")
    print("  7. Survival Curves")
    print("  8. QALY Accumulation (cumulative & annual, dual y-axis)")
    print()
    print("All figures use Cure Lowe Foundation brand colors")
    print("and consistent styling (font size 14, no top spine,")
    print("horizontal gridlines, legend at bottom)")
    print()


if __name__ == "__main__":
    """
    Example usage - requires running the model first.
    """
    print("="*70)
    print("HTA FIGURE GENERATION MODULE")
    print("="*70)
    print()
    print("This module must be imported and used with model results.")
    print()
    print("Example usage:")
    print("="*70)
    print()
    print("from markov_cua_model import run_full_analysis")
    print("from generate_hta_figures import generate_all_figures")
    print()
    print("# Run the economic model")
    print("results = run_full_analysis(save_results=True)")
    print()
    print("# Generate all figures")
    print("generate_all_figures(")
    print("    results['scenario_results'],")
    print("    results['value_based_pricing'],")
    print("    './figures'")
    print(")")
    print()
    print("="*70)
    print()
    print("Or use the provided integration script:")
    print("  python run_model_and_generate_figures.py")
    print()
    print("="*70)
