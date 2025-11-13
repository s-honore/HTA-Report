"""
Calibrate mortality parameters to match observed natural history.

Target outcomes:
- Median survival: 30-40 years (death at age 35-45 from starting age 5)
- Median time to ESKD: ~27 years (reaching ESKD at age 32)
"""

from markov_cua_model import ModelParameters, MarkovCohortModel
import numpy as np

def test_mortality_rate(base_mort_rate, target_life_years=35):
    """Test a given mortality rate and return life expectancy."""
    params = ModelParameters()
    params.base_mortality_rate = base_mort_rate

    model = MarkovCohortModel(params)
    results = model.run_model(
        egfr_decline_rate=params.natural_decline_rate,
        scenario_name="Natural History",
        include_gene_therapy_cost=False
    )

    life_years = results['life_years']
    time_to_eskd = results['time_to_eskd']

    return life_years, time_to_eskd

print("=" * 80)
print("MORTALITY PARAMETER CALIBRATION")
print("=" * 80)
print("\nTarget: Life expectancy ~35 years (death at age 40)")
print("Target: Time to ESKD ~27 years (ESKD at age 32)")
print("\n" + "-" * 80)

# Test range of mortality rates
test_rates = [0.02, 0.01, 0.005, 0.003, 0.002, 0.001, 0.0005]

print(f"{'Base Mortality Rate':<25} {'Life Years':<15} {'Age at Death':<15} {'Time to ESKD':<15} {'ESKD Age':<15}")
print("-" * 80)

best_rate = None
best_diff = float('inf')

for rate in test_rates:
    life_years, time_to_eskd = test_mortality_rate(rate)
    age_at_death = 5 + life_years
    eskd_age = 5 + time_to_eskd

    # Calculate how close to target (35 years life expectancy)
    diff = abs(life_years - 35)
    if diff < best_diff:
        best_diff = diff
        best_rate = rate

    marker = " <-- BEST" if rate == best_rate else ""
    print(f"{rate:<25.4f} {life_years:<15.2f} {age_at_death:<15.1f} {time_to_eskd:<15.1f} {eskd_age:<15.1f}{marker}")

print("\n" + "=" * 80)
print(f"RECOMMENDED: base_mortality_rate = {best_rate:.4f}")
print(f"This produces life expectancy of {test_mortality_rate(best_rate)[0]:.1f} years")
print("=" * 80)
