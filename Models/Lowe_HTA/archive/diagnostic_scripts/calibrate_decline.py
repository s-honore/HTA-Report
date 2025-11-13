"""
Calibrate eGFR decline rates to match observed ESKD age of 32 years.

Target: Median ESKD age = 32 years (27 years from starting age 5)
Constraint: Decline accelerates with age (early rate < late rate)
"""

def calculate_eskd_age(starting_egfr, early_rate, late_rate, transition_age=15, starting_age=5):
    """Calculate age at ESKD given decline rates."""
    eskd_threshold = 15

    # Phase 1: starting_age to transition_age
    years_phase1 = transition_age - starting_age
    egfr_at_transition = starting_egfr - (early_rate * years_phase1)

    if egfr_at_transition <= eskd_threshold:
        # Reached ESKD in phase 1
        years_to_eskd = (starting_egfr - eskd_threshold) / early_rate
        return starting_age + years_to_eskd

    # Phase 2: transition_age onward
    remaining_decline = egfr_at_transition - eskd_threshold
    years_phase2 = remaining_decline / late_rate
    eskd_age = transition_age + years_phase2

    return eskd_age

# Solve for rates that give ESKD at age 32
# Use ratio constraint: late_rate = acceleration_factor * early_rate

print("=" * 80)
print("eGFR DECLINE RATE CALIBRATION")
print("=" * 80)
print("\nTarget: ESKD at age 32 (27 years from age 5)")
print("Constraint: Decline accelerates after age 15")
print("Starting eGFR: 70 ml/min/1.73m²")
print("\n" + "-" * 80)

# Test different acceleration factors
starting_egfr = 70
starting_age = 5
transition_age = 15
target_eskd_age = 32

print(f"{'Early Rate':<12} {'Late Rate':<12} {'Acceleration':<15} {'ESKD Age':<12} {'Error':<12}")
print("-" * 80)

best_rates = None
best_error = float('inf')

# Try different early rates
for early_rate in [1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.5, 2.6, 2.8, 3.0]:
    # Try different acceleration factors
    for accel in [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0]:
        late_rate = early_rate * accel

        eskd_age = calculate_eskd_age(starting_egfr, early_rate, late_rate, transition_age, starting_age)
        error = abs(eskd_age - target_eskd_age)

        if error < best_error:
            best_error = error
            best_rates = (early_rate, late_rate, accel)

        if error < 0.5:  # Print close matches
            marker = " <-- BEST" if (early_rate, late_rate) == best_rates[:2] else ""
            print(f"{early_rate:<12.2f} {late_rate:<12.2f} {accel:<15.2f}x {eskd_age:<12.1f} {error:<12.2f}{marker}")

if best_rates:
    print("\n" + "=" * 80)
    print(f"RECOMMENDED RATES:")
    print(f"  Early decline (ages 5-15): {best_rates[0]:.2f} ml/min/1.73m²/year")
    print(f"  Late decline (ages 15+):   {best_rates[1]:.2f} ml/min/1.73m²/year")
    print(f"  Acceleration factor:       {best_rates[2]:.2f}x")

    final_age = calculate_eskd_age(starting_egfr, best_rates[0], best_rates[1], transition_age, starting_age)
    print(f"  Predicted ESKD age:        {final_age:.1f} years")
    print(f"  Error from target (32):    {abs(final_age - 32):.2f} years")
    print("=" * 80)
