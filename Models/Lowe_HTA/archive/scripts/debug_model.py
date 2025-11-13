"""Quick debug script to test transition logic"""
import numpy as np

# CKD stage thresholds
ckd_thresholds = {
    'CKD2': (60, 90),
    'CKD3a': (45, 60),
    'CKD3b': (30, 45),
    'CKD4': (15, 30),
    'ESKD': (0, 15),
}

def egfr_to_state(egfr):
    """Convert eGFR to state"""
    if egfr < 0:
        return 'ESKD'
    for state, (lower, upper) in ckd_thresholds.items():
        if lower <= egfr < upper:
            return state
    if egfr >= 90:
        return 'CKD2'
    return 'ESKD'

# Test transitions with different decline rates
print("Testing eGFR transitions:\n")

for decline_rate in [0.0, 1.2, 2.4, 4.0]:
    print(f"\nDecline rate: {decline_rate} ml/min/1.73m²/year")
    print("-" * 60)

    # Start at eGFR 70 (CKD2)
    current_egfr = 70.0
    current_state = egfr_to_state(current_egfr)

    print(f"Starting: eGFR={current_egfr:.1f}, State={current_state}")

    # Simulate 10 years
    for year in range(1, 11):
        current_egfr = max(0, current_egfr - decline_rate)
        current_state = egfr_to_state(current_egfr)
        print(f"Year {year}: eGFR={current_egfr:.1f}, State={current_state}")

# Now test state-based transitions
print("\n\n" + "=" * 80)
print("Testing state-based transitions (using state midpoints):\n")

for decline_rate in [0.0, 1.2, 2.4, 4.0]:
    print(f"\nDecline rate: {decline_rate} ml/min/1.73m²/year")
    print("-" * 60)

    states = ['CKD2', 'CKD3a', 'CKD3b', 'CKD4', 'ESKD']

    # Calculate midpoint for each state
    state_midpoints = {}
    for state in states:
        lower, upper = ckd_thresholds[state]
        state_midpoints[state] = (lower + upper) / 2

    print("State midpoints:", state_midpoints)
    print()

    # For each state, calculate where it transitions to
    for from_state in states:
        from_egfr = state_midpoints[from_state]
        next_egfr = max(0, from_egfr - decline_rate)
        to_state = egfr_to_state(next_egfr)
        print(f"  {from_state} (eGFR={from_egfr:.1f}) -> eGFR={next_egfr:.1f} -> {to_state}")
