"""
Plot treatment scenarios for Lowe syndrome gene therapy
Recreates natural history progression and shows 3 treatment scenarios
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle

# Model parameters from markov_cua_model.py
starting_age = 5
starting_egfr = 70.0
natural_decline_rate = 1.10  # ml/min/1.73m²/year

# Treatment scenarios (decline reduction)
scenarios = {
    'Natural History': {
        'decline_rate': natural_decline_rate * 1.0,  # 100% (no reduction)
        'color': '#2E3440',  # Dark grey
        'linestyle': '-',
        'linewidth': 3,
        'label': 'Natural History (No treatment)'
    },
    'Scenario 1': {
        'decline_rate': natural_decline_rate * 0.15,  # 85% reduction
        'color': '#A3BE8C',  # Green
        'linestyle': '-',
        'linewidth': 2.5,
        'label': 'Scenario 1: 50% Enzyme (85% decline ↓)'
    },
    'Scenario 2': {
        'decline_rate': natural_decline_rate * 0.35,  # 65% reduction
        'color': '#EBCB8B',  # Yellow
        'linestyle': '-',
        'linewidth': 2.5,
        'label': 'Scenario 2: 30% Enzyme (65% decline ↓)'
    },
    'Scenario 3': {
        'decline_rate': natural_decline_rate * 0.65,  # 35% reduction
        'color': '#D08770',  # Orange
        'linestyle': '-',
        'linewidth': 2.5,
        'label': 'Scenario 3: 15% Enzyme (35% decline ↓)'
    }
}

# CKD stage thresholds
ckd_stages = {
    'CKD 1': (90, 120, '#A3BE8C', 0.15),
    'CKD 2': (60, 90, '#EBCB8B', 0.15),
    'CKD 3a': (45, 60, '#D08770', 0.15),
    'CKD 3b': (30, 45, '#BF616A', 0.15),
    'CKD 4': (15, 30, '#B48EAD', 0.15),
    'ESKD': (0, 15, '#5E81AC', 0.2)
}

# Time horizon
years = np.arange(0, 101)  # 0 to 100 years from treatment
ages = starting_age + years

# Calculate eGFR trajectories
fig, ax = plt.subplots(figsize=(14, 8))

# Add CKD stage background shading
for stage_name, (lower, upper, color, alpha) in ckd_stages.items():
    ax.axhspan(lower, upper, color=color, alpha=alpha, zorder=0)

# Plot each scenario
for scenario_name, config in scenarios.items():
    decline_rate = config['decline_rate']
    egfr_trajectory = starting_egfr - (decline_rate * years)
    egfr_trajectory = np.maximum(egfr_trajectory, 0)  # Floor at 0

    ax.plot(
        ages,
        egfr_trajectory,
        color=config['color'],
        linestyle=config['linestyle'],
        linewidth=config['linewidth'],
        label=config['label'],
        zorder=10
    )

# Add CKD stage labels on the right
stage_label_x = 107  # x-position for stage labels
for stage_name, (lower, upper, color, alpha) in ckd_stages.items():
    mid_y = (lower + upper) / 2
    ax.text(
        stage_label_x,
        mid_y,
        stage_name,
        fontsize=10,
        weight='bold',
        va='center',
        ha='left',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color, linewidth=2)
    )

# Add horizontal lines for key thresholds
ax.axhline(y=15, color='#5E81AC', linestyle='--', linewidth=1.5, alpha=0.6, label='ESKD threshold (eGFR<15)', zorder=5)
ax.axhline(y=60, color='#D08770', linestyle='--', linewidth=1.5, alpha=0.6, label='CKD Stage 3 threshold', zorder=5)

# Styling
ax.set_xlabel('Age (years)', fontsize=14, weight='bold')
ax.set_ylabel('eGFR (mL/min/1.73 m²)', fontsize=14, weight='bold')
ax.set_title(
    'Treatment Scenarios: eGFR Progression in Lowe Syndrome\nGene Therapy Impact on Kidney Function Decline',
    fontsize=16,
    weight='bold',
    pad=20
)

ax.set_xlim(5, 110)
ax.set_ylim(0, 120)
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

# Legend
ax.legend(
    loc='upper right',
    fontsize=11,
    frameon=True,
    fancybox=True,
    shadow=True,
    framealpha=0.95
)

# Add annotations for key events
# Natural history reaches ESKD
natural_eskd_age = starting_age + (starting_egfr - 15) / natural_decline_rate
ax.annotate(
    f'Natural history\nreaches ESKD\n~age {natural_eskd_age:.0f}',
    xy=(natural_eskd_age, 15),
    xytext=(natural_eskd_age + 5, 35),
    fontsize=10,
    ha='left',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#ECEFF4', edgecolor='#2E3440', linewidth=1.5),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', linewidth=2, color='#2E3440')
)

# Treatment start indicator
ax.axvline(x=starting_age, color='#8FBCBB', linestyle='-.', linewidth=2, alpha=0.7, zorder=5)
ax.text(
    starting_age,
    125,
    'Treatment at age 5',
    fontsize=11,
    weight='bold',
    ha='center',
    va='bottom',
    color='#8FBCBB',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#8FBCBB', linewidth=2)
)

# Add model note
fig.text(
    0.5,
    0.02,
    'Model: Starting eGFR 70 mL/min/1.73m² at age 5 | Natural decline 1.10 mL/min/year (calibrated to Ando et al. 2024)\n' +
    'Enzyme restoration levels based on carrier analogy (50% enzyme = asymptomatic carriers)',
    ha='center',
    fontsize=9,
    style='italic',
    color='#4C566A'
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.08, right=0.93)

# Save figure
output_path = '/home/user/HTA-Report/Models/Lowe_HTA/treatment_scenarios_figure.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figure saved to: {output_path}")

plt.show()
