"""
Generate Figure 1: Cost-Effectiveness Plane for Lowe Syndrome Gene Therapy

This script creates a publication-ready cost-effectiveness plane plotting
incremental costs against incremental QALYs for three treatment scenarios.

Requirements: matplotlib, pandas, numpy
Usage: python generate_figure1_ce_plane.py
Output: figure1_ce_plane.png (publication quality, 300 DPI)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data
data = pd.read_csv('ce_plane_data.csv')

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Plot each scenario
colors = ['#2E7D32', '#F57C00', '#C62828']  # Green, Orange, Red
markers = ['o', 's', '^']
labels = [
    'Scenario 1: 50% Enzyme\n(Carrier Analogy)',
    'Scenario 2: 30% Enzyme',
    'Scenario 3: 15% Enzyme\n(Minimal Benefit)'
]

for idx, row in data.iterrows():
    ax.scatter(
        row['Incremental_QALYs'],
        row['Incremental_Costs'] / 1000000,  # Convert to millions
        s=200,
        c=colors[idx],
        marker=markers[idx],
        label=labels[idx],
        edgecolors='black',
        linewidths=1.5,
        zorder=3
    )

    # Add ICER annotation
    icer_text = f"ICER: €{row['ICER']/1000:.0f}K/QALY"
    ax.annotate(
        icer_text,
        xy=(row['Incremental_QALYs'], row['Incremental_Costs'] / 1000000),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
    )

# Add willingness-to-pay threshold lines
wtp_thresholds = [100000, 150000, 300000]  # €/QALY
wtp_labels = ['€100K/QALY', '€150K/QALY', '€300K/QALY (HST)']
wtp_colors = ['#BDBDBD', '#9E9E9E', '#757575']
wtp_styles = ['--', '-.', ':']

x_max = data['Incremental_QALYs'].max() * 1.1
for threshold, label, color, style in zip(wtp_thresholds, wtp_labels, wtp_colors, wtp_styles):
    x_range = np.linspace(0, x_max, 100)
    y_range = threshold * x_range / 1000000  # Convert to millions
    ax.plot(x_range, y_range, color=color, linestyle=style, linewidth=1.5,
            label=label, alpha=0.7, zorder=1)

# Add origin point for natural history
ax.scatter(0, 0, s=150, c='black', marker='x', linewidths=2,
           label='Natural History (Origin)', zorder=3)

# Formatting
ax.set_xlabel('Incremental QALYs', fontsize=12, fontweight='bold')
ax.set_ylabel('Incremental Cost (€ Millions)', fontsize=12, fontweight='bold')
ax.set_title('Cost-Effectiveness Plane: Gene Therapy vs. Natural History\nLowe Syndrome (1.5% Discount Rate)',
             fontsize=14, fontweight='bold', pad=20)

# Set axis limits
ax.set_xlim(-0.5, x_max)
ax.set_ylim(-0.2, data['Incremental_Costs'].max() / 1000000 * 1.15)

# Grid
ax.grid(True, alpha=0.3, zorder=0)

# Legend
ax.legend(loc='upper left', fontsize=9, framealpha=0.95)

# Add note
note_text = ('Note: All scenarios are cost-effective relative to natural history (northeast quadrant).\n'
             'ICER = Incremental Cost-Effectiveness Ratio. HST = Highly Specialised Technologies.')
fig.text(0.12, 0.02, note_text, fontsize=8, style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.3))

# Tight layout
plt.tight_layout(rect=[0, 0.05, 1, 1])

# Save figure
plt.savefig('figure1_ce_plane.png', dpi=300, bbox_inches='tight')
plt.savefig('figure1_ce_plane.pdf', format='pdf', bbox_inches='tight')
print("Figure 1 saved: figure1_ce_plane.png (PNG) and figure1_ce_plane.pdf (PDF)")
print("Resolution: 300 DPI (publication quality)")
