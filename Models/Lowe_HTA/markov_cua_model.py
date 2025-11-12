"""
Markov Cohort Model for Lowe Syndrome Gene Therapy Cost-Utility Analysis

This module implements a Markov cohort model to evaluate the cost-effectiveness
of gene therapy for Lowe syndrome, tracking progression through CKD stages.

Model Structure:
- Health States: CKD Stage 2, 3a, 3b, 4, 5/ESKD, Death
- Annual cycles
- Lifetime horizon (100 years)
- Starting age: 5 years (median treatment age)
- Discounting: 3.5% (base case)

Scenarios (decomposed decline: D_total = D_age + (1-θ)×D_path):
- Scenario 0: Natural history (1.10 ml/min/yr)
- Scenario 1: Carrier-equivalent ≥50% enzyme (0.30 ml/min/yr, θ=1.0)
- Scenario 2: Subthreshold 25-40% enzyme (0.70 ml/min/yr, θ=0.5)
- Scenario 3: Minimal 10-20% enzyme (0.94 ml/min/yr, θ=0.2)

Author: HTA Analysis Team
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import warnings
warnings.filterwarnings('ignore')


@dataclass
class ModelParameters:
    """Container for all model parameters with defaults."""

    # Time parameters
    starting_age: int = 1  # Start from age 1 (not age 5)
    time_horizon_years: int = 100
    cycle_length: float = 1.0  # Annual cycles
    discount_rate: float = 0.015  # 1.5% base case (NICE non-reference case for curative therapies)

    # eGFR parameters
    # Calibrated to achieve ESKD at age 32 (Ando 2024) with age-varying decline
    # Monte Carlo validation shows: need 14 fewer years of decline (28 ml/min @ 2.0/year)
    # Adjusted from 111 to 83 to match Monte Carlo ESKD timing with natural history
    starting_egfr: float = 83.0  # ml/min/1.73m² at age 1

    # Age-dependent decline rates based on Ando et al. 2024 Figure 1B
    # THREE age groups with different decline rates
    use_age_dependent_decline: bool = True  # ENABLED for accurate modeling
    decline_rate_early: float = 1.0    # ml/min/1.73m²/year for ages 1-10
    decline_rate_middle: float = 3.5   # ml/min/1.73m²/year for ages 10-20 (steep!)
    decline_rate_late: float = 2.0     # ml/min/1.73m²/year for ages 20+
    decline_transition_age_1: int = 10  # Age at which decline accelerates
    decline_transition_age_2: int = 20  # Age at which decline moderates

    # For reference: time-averaged constant rate (NOT USED when age-varying enabled)
    natural_decline_rate: float = 1.80  # Approximate average over lifetime

    # CKD stage thresholds (eGFR ml/min/1.73m²)
    ckd_thresholds: Dict[str, Tuple[float, float]] = field(default_factory=lambda: {
        'CKD2': (60, 90),   # Stage 2: 60-89
        'CKD3a': (45, 60),  # Stage 3a: 45-59
        'CKD3b': (30, 45),  # Stage 3b: 30-44
        'CKD4': (15, 30),   # Stage 4: 15-29
        'ESKD': (0, 15),    # Stage 5/ESKD: <15
    })

    # Health state utilities (QALY weights)
    # Base utilities from general CKD populations (Wyld et al. 2012)
    base_utilities: Dict[str, float] = field(default_factory=lambda: {
        'CKD2': 0.72,
        'CKD3a': 0.68,
        'CKD3b': 0.61,
        'CKD4': 0.54,
        'ESKD': 0.40,
        'Death': 0.00
    })

    # Lowe syndrome adjustment multiplier
    # Accounts for intellectual disability (90%), visual impairment (100%),
    # and neurological manifestations (100%) not captured in CKD utilities
    lowe_utility_multiplier: float = 0.85  # 15% decrement from base CKD utilities

    # Final utilities (auto-calculated, do not set directly)
    utilities: Dict[str, float] = field(init=False)

    # Annual costs by CKD stage (USD)
    annual_costs: Dict[str, float] = field(default_factory=lambda: {
        'CKD2': 20000,
        'CKD3a': 25000,
        'CKD3b': 40000,
        'CKD4': 50000,
        'ESKD': 150000,
        'Death': 0
    })

    # Gene therapy costs (USD)
    gene_therapy_cost: float = 3000000  # $3.0M one-time cost
    monitoring_year1: float = 25000     # Year 1 monitoring
    monitoring_year2_5: float = 10000   # Years 2-5 monitoring
    monitoring_ongoing: float = 3000    # Years 6+ monitoring

    # Mortality parameters
    # Calibrated to match "2nd to 4th decade" survival (ages 20-40) per Murdock 2023
    # Starting from age 1, median death should occur around age 30 (midpoint of 20-40)
    # Base rate calibrated empirically to achieve this with CKD-stage multipliers
    base_mortality_rate: float = 0.010  # 1.0% base annual mortality (reduced to allow ESKD before death)
    mortality_multipliers: Dict[str, float] = field(default_factory=lambda: {
        'CKD2': 0.8,   # Lower risk in early stages
        'CKD3a': 1.0,
        'CKD3b': 1.5,
        'CKD4': 2.5,   # Increased risk in advanced CKD
        'ESKD': 4.0,   # Highest risk post-ESKD (renal failure, infections)
    })

    def __post_init__(self):
        """Calculate Lowe-adjusted utilities after initialization."""
        self.utilities = {
            state: base_util * self.lowe_utility_multiplier
            for state, base_util in self.base_utilities.items()
        }
        # Death always has utility 0
        self.utilities['Death'] = 0.00


class MarkovCohortModel:
    """
    Markov cohort model for Lowe syndrome gene therapy cost-effectiveness.

    This model tracks a cohort through CKD stages based on eGFR decline rates,
    calculating costs, QALYs, and cost-effectiveness outcomes.
    """

    def __init__(self, params: ModelParameters):
        """
        Initialize the Markov model with parameters.

        Args:
            params: ModelParameters object with all model inputs
        """
        self.params = params
        self.states = ['CKD2', 'CKD3a', 'CKD3b', 'CKD4', 'ESKD', 'Death']
        self.n_states = len(self.states)
        self.n_cycles = params.time_horizon_years

        # Initialize tracking matrices
        self.trace = None  # Cohort distribution over time
        self.costs = None  # Costs by cycle
        self.qalys = None  # QALYs by cycle

    def get_decline_rate(self, age: int, base_decline: float) -> float:
        """
        Calculate age-dependent eGFR decline rate based on Ando 2024 Figure 1B.

        Three age groups with different NATURAL decline rates:
        - Ages 1-10: Slow decline (1.0 ml/min/year)
        - Ages 10-20: Steep accelerated decline (3.5 ml/min/year)
        - Ages 20+: Moderate continued decline (2.0 ml/min/year)

        For TREATMENT scenarios, applies mathematical decomposition:
        D_treated = D_age + (1-θ)×D_path where D_path varies by age

        Args:
            age: Current age of patient
            base_decline: Treatment effect parameter (0.30, 0.70, 0.94) OR natural_decline_rate

        Returns:
            Age-adjusted decline rate for current age
        """
        # First, determine natural rate for this age
        if age < self.params.decline_transition_age_1:
            # Ages 1-10: Slow decline
            natural_rate = self.params.decline_rate_early
        elif age < self.params.decline_transition_age_2:
            # Ages 10-20: Steep decline (adolescent acceleration)
            natural_rate = self.params.decline_rate_middle
        else:
            # Ages 20+: Moderate decline
            natural_rate = self.params.decline_rate_late

        # Check if this is natural history scenario
        is_natural_history = abs(base_decline - self.params.natural_decline_rate) < 0.01

        if is_natural_history:
            # Natural history: return age-varying rate
            return natural_rate
        else:
            # Treatment scenario: Apply decomposition D_treated = D_age + (1-θ)×D_path
            # Where D_path = natural_rate - D_age
            D_age = 0.3  # Normal aging component (constant across ages)
            D_path = natural_rate - D_age  # Pathological component (age-varying!)

            # Treatment effect θ implied by base_decline:
            # base_decline ≈ 0.30 → θ=1.0 (100% pathological reduction)
            # base_decline ≈ 0.70 → θ=0.5 (50% pathological reduction)
            # base_decline ≈ 0.94 → θ=0.2 (20% pathological reduction)

            # Map base_decline to treatment effect θ
            if abs(base_decline - 0.30) < 0.05:
                theta = 1.0  # Carrier-equivalent
            elif abs(base_decline - 0.70) < 0.05:
                theta = 0.5  # Intermediate
            elif abs(base_decline - 0.94) < 0.05:
                theta = 0.2  # Minimal
            else:
                # Unknown scenario - use proportional scaling
                theta = (self.params.natural_decline_rate - base_decline) / self.params.natural_decline_rate

            # Calculate treated rate for this age
            treated_rate = D_age + (1 - theta) * D_path

            return treated_rate

    def egfr_to_state(self, egfr: float) -> str:
        """
        Convert eGFR value to CKD health state.

        Args:
            egfr: eGFR value in ml/min/1.73m²

        Returns:
            CKD stage as string
        """
        if egfr < 0:
            return 'ESKD'

        for state, (lower, upper) in self.params.ckd_thresholds.items():
            if lower <= egfr < upper:
                return state

        # If eGFR >= 90, still assign to CKD2 (best state in model)
        if egfr >= 90:
            return 'CKD2'

        return 'ESKD'  # Default to ESKD if no match

    def calculate_transition_probability(
        self,
        current_state: str,
        next_state: str,
        egfr_decline: float,
        current_egfr: float,
        age: int
    ) -> float:
        """
        Calculate annual transition probability between states.

        Args:
            current_state: Current CKD stage
            next_state: Potential next CKD stage
            egfr_decline: Annual eGFR decline rate (ml/min/1.73m²/year)
            current_egfr: Current eGFR value
            age: Current age of patient

        Returns:
            Transition probability (0-1)
        """
        # Can't transition from Death
        if current_state == 'Death':
            return 1.0 if next_state == 'Death' else 0.0

        # Death transitions - allocated after determining alive state
        if next_state == 'Death':
            return self.calculate_mortality_rate(current_state, age)

        # Calculate next year's eGFR based on current state's eGFR
        # Use midpoint of current state's eGFR range for calculation
        current_lower, current_upper = self.params.ckd_thresholds.get(
            current_state, (current_egfr, current_egfr)
        )

        # Use current eGFR if provided, otherwise use midpoint of current state
        if current_state == self.egfr_to_state(current_egfr):
            state_egfr = current_egfr
        else:
            state_egfr = (current_lower + current_upper) / 2

        # Calculate eGFR after one year of decline
        next_egfr = max(0, state_egfr - egfr_decline)
        predicted_state = self.egfr_to_state(next_egfr)

        # Calculate mortality
        mortality = self.calculate_mortality_rate(current_state, age)

        # Survival probability
        survival_prob = 1.0 - mortality

        # Assign transition probabilities
        if predicted_state == next_state:
            # Transition to predicted state (if survive)
            return survival_prob
        else:
            # No transition to this state
            return 0.0

    def calculate_mortality_rate(self, state: str, age: int) -> float:
        """
        Calculate age and state-specific mortality rate.

        Args:
            state: Current CKD stage
            age: Current age

        Returns:
            Annual mortality probability
        """
        if state == 'Death':
            return 0.0

        # Base mortality increases with age
        age_factor = 1.0 + (age - self.params.starting_age) * 0.01  # 1% increase per year

        # State-specific multiplier
        state_multiplier = self.params.mortality_multipliers.get(state, 1.0)

        # Combined mortality rate (capped at 1.0)
        mortality = min(
            self.params.base_mortality_rate * age_factor * state_multiplier,
            1.0
        )

        return mortality

    def build_transition_matrix(
        self,
        egfr_decline: float,
        age: int,
        state_egfrs: Dict[str, float] = None
    ) -> np.ndarray:
        """
        Build transition probability matrix for one cycle.

        Args:
            egfr_decline: Annual eGFR decline rate
            age: Current age
            state_egfrs: Optional dict mapping states to their current eGFR values

        Returns:
            Transition matrix (n_states x n_states)
        """
        matrix = np.zeros((self.n_states, self.n_states))

        # Use midpoint of each state's range if no specific eGFR provided
        if state_egfrs is None:
            state_egfrs = {}
            for state in self.states:
                if state == 'Death':
                    state_egfrs[state] = 0
                else:
                    lower, upper = self.params.ckd_thresholds[state]
                    state_egfrs[state] = (lower + upper) / 2

        for i, from_state in enumerate(self.states):
            current_egfr = state_egfrs.get(from_state, 0)

            for j, to_state in enumerate(self.states):
                matrix[i, j] = self.calculate_transition_probability(
                    from_state, to_state, egfr_decline, current_egfr, age
                )

        # Normalize rows to sum to 1 (accounting for rounding errors)
        row_sums = matrix.sum(axis=1, keepdims=True)
        matrix = np.divide(matrix, row_sums, where=row_sums != 0)

        return matrix

    def run_model(
        self,
        egfr_decline_rate: float,
        scenario_name: str = "Baseline",
        include_gene_therapy_cost: bool = False
    ) -> Dict:
        """
        Run the Markov model for one scenario.

        Args:
            egfr_decline_rate: Annual eGFR decline rate (ml/min/1.73m²/year)
            scenario_name: Name of scenario for tracking
            include_gene_therapy_cost: Whether to include gene therapy costs

        Returns:
            Dictionary with model results
        """
        # Initialize cohort trace matrix
        trace = np.zeros((self.n_cycles + 1, self.n_states))

        # Starting distribution - all in initial state based on starting eGFR
        initial_state = self.egfr_to_state(self.params.starting_egfr)
        initial_state_idx = self.states.index(initial_state)
        trace[0, initial_state_idx] = 1.0

        # Track eGFR over time for the cohort
        # We'll track average eGFR weighted by state occupancy
        egfr_track = np.zeros(self.n_cycles + 1)
        egfr_track[0] = self.params.starting_egfr

        # Cycle through time
        # Track eGFR for each state separately (tunnel state approach)
        state_egfrs = {state: 0.0 for state in self.states}
        state_egfrs[initial_state] = self.params.starting_egfr

        for cycle in range(1, self.n_cycles + 1):
            age = self.params.starting_age + cycle

            # Get age-dependent decline rate for this cycle
            current_decline_rate = self.get_decline_rate(age, egfr_decline_rate)

            # Update eGFR for each state based on occupancy in previous cycle
            new_state_egfrs = {}
            for i, state in enumerate(self.states):
                if state == 'Death':
                    new_state_egfrs[state] = 0
                elif trace[cycle - 1, i] > 0.001:  # If state is occupied
                    # Decline from previous cycle's eGFR for this state
                    prev_egfr = state_egfrs.get(state, 0)
                    if prev_egfr == 0:  # Initialize if needed
                        lower, upper = self.params.ckd_thresholds[state]
                        prev_egfr = (lower + upper) / 2
                    new_state_egfrs[state] = max(0, prev_egfr - current_decline_rate)
                else:
                    # Use midpoint if unoccupied
                    if state != 'Death':
                        lower, upper = self.params.ckd_thresholds[state]
                        new_state_egfrs[state] = (lower + upper) / 2

            # Calculate weighted average eGFR for tracking
            avg_egfr = 0
            for i, state in enumerate(self.states):
                if state != 'Death':
                    avg_egfr += trace[cycle - 1, i] * new_state_egfrs.get(state, 0)
            egfr_track[cycle] = avg_egfr

            # Build transition matrix using current state-specific eGFRs and age-adjusted decline rate
            trans_matrix = self.build_transition_matrix(
                current_decline_rate,  # Use age-adjusted rate, not base rate
                age,
                new_state_egfrs
            )

            # Apply transitions
            trace[cycle, :] = trace[cycle - 1, :] @ trans_matrix

            # Update state eGFRs for next cycle
            state_egfrs = new_state_egfrs

        # Calculate costs and QALYs for each cycle
        costs_by_cycle = np.zeros(self.n_cycles + 1)
        qalys_by_cycle = np.zeros(self.n_cycles + 1)

        for cycle in range(self.n_cycles + 1):
            # State-based costs and utilities
            for state_idx, state in enumerate(self.states):
                proportion = trace[cycle, state_idx]
                costs_by_cycle[cycle] += proportion * self.params.annual_costs[state]
                qalys_by_cycle[cycle] += proportion * self.params.utilities[state]

        # Add gene therapy costs if applicable
        if include_gene_therapy_cost:
            # One-time gene therapy cost at cycle 0
            costs_by_cycle[0] += self.params.gene_therapy_cost

            # Monitoring costs
            for cycle in range(min(6, self.n_cycles + 1)):
                if cycle == 0:
                    costs_by_cycle[cycle] += self.params.monitoring_year1
                elif cycle <= 4:
                    costs_by_cycle[cycle] += self.params.monitoring_year2_5
                else:
                    costs_by_cycle[cycle] += self.params.monitoring_ongoing

            # Ongoing monitoring for remaining cycles
            for cycle in range(6, self.n_cycles + 1):
                costs_by_cycle[cycle] += self.params.monitoring_ongoing

        # Apply discounting
        discount_factors = np.array([
            1 / (1 + self.params.discount_rate) ** cycle
            for cycle in range(self.n_cycles + 1)
        ])

        discounted_costs = costs_by_cycle * discount_factors
        discounted_qalys = qalys_by_cycle * discount_factors

        # Calculate time to ESKD
        eskd_idx = self.states.index('ESKD')
        time_to_eskd = None
        for cycle in range(self.n_cycles + 1):
            if trace[cycle, eskd_idx] > 0.5:  # >50% of cohort in ESKD
                time_to_eskd = cycle
                break

        # Calculate life years
        death_idx = self.states.index('Death')
        life_years = 0
        for cycle in range(self.n_cycles + 1):
            life_years += (1 - trace[cycle, death_idx])

        # Store results
        results = {
            'scenario': scenario_name,
            'egfr_decline_rate': egfr_decline_rate,
            'total_costs': np.sum(discounted_costs),
            'total_qalys': np.sum(discounted_qalys),
            'total_costs_undiscounted': np.sum(costs_by_cycle),
            'total_qalys_undiscounted': np.sum(qalys_by_cycle),
            'life_years': life_years,
            'time_to_eskd': time_to_eskd if time_to_eskd else self.n_cycles,
            'trace': trace,
            'costs_by_cycle': costs_by_cycle,
            'qalys_by_cycle': qalys_by_cycle,
            'discounted_costs_by_cycle': discounted_costs,
            'discounted_qalys_by_cycle': discounted_qalys,
            'egfr_track': egfr_track
        }

        return results

    def run_monte_carlo_validation(
        self,
        egfr_decline_rate: float,
        n_simulations: int = 1000,
        random_seed: int = 42
    ) -> Dict:
        """
        Run Monte Carlo simulation of individual patients to validate cohort model.

        Args:
            egfr_decline_rate: Annual eGFR decline rate for natural history
            n_simulations: Number of patient simulations to run
            random_seed: Random seed for reproducibility

        Returns:
            Dictionary with validation results including distributions
        """
        np.random.seed(random_seed)

        # Track outcomes for each patient
        times_to_eskd = []
        times_to_death = []
        final_states = []
        ckd_stage_durations = {state: [] for state in self.states if state != 'Death'}

        for sim in range(n_simulations):
            # Initialize patient
            egfr = self.params.starting_egfr
            age = self.params.starting_age
            state = self.egfr_to_state(egfr)
            is_alive = True
            eskd_age = None

            # Track time in each CKD stage
            stage_durations = {s: 0 for s in self.states if s != 'Death'}

            # Simulate until death or end of time horizon
            for year in range(self.n_cycles):
                age = self.params.starting_age + year + 1

                # Apply eGFR decline (age-dependent)
                decline = self.get_decline_rate(age, egfr_decline_rate)
                egfr = max(0, egfr - decline)

                # Update state based on new eGFR
                new_state = self.egfr_to_state(egfr)

                # Record ESKD timing
                if new_state == 'ESKD' and eskd_age is None:
                    eskd_age = age

                # Check for death (stochastic)
                if new_state != 'Death':
                    mortality_prob = self.calculate_mortality_rate(new_state, age)
                    if np.random.rand() < mortality_prob:
                        is_alive = False
                        times_to_death.append(age)
                        final_states.append(new_state)
                        break

                    # Track time in current state
                    stage_durations[new_state] += 1

                state = new_state

            # Record outcomes
            if eskd_age is not None:
                times_to_eskd.append(eskd_age)

            # If survived entire time horizon
            if is_alive:
                times_to_death.append(age)
                final_states.append(state)

            # Record stage durations for this patient
            for s in ckd_stage_durations:
                ckd_stage_durations[s].append(stage_durations[s])

        # Calculate summary statistics
        eskd_reached_pct = 100 * len(times_to_eskd) / n_simulations
        median_eskd = np.median(times_to_eskd) if times_to_eskd else None
        median_death = np.median(times_to_death)
        mean_death = np.mean(times_to_death)

        # Calculate percentiles
        eskd_percentiles = {
            '25th': np.percentile(times_to_eskd, 25) if times_to_eskd else None,
            '50th': median_eskd,
            '75th': np.percentile(times_to_eskd, 75) if times_to_eskd else None,
        }

        death_percentiles = {
            '25th': np.percentile(times_to_death, 25),
            '50th': median_death,
            '75th': np.percentile(times_to_death, 75),
        }

        # Calculate proportion of patients in each CKD stage (average across time)
        avg_stage_proportions = {}
        for stage in ckd_stage_durations:
            durations = ckd_stage_durations[stage]
            avg_stage_proportions[stage] = np.mean(durations) / self.n_cycles if durations else 0

        results = {
            'n_simulations': n_simulations,
            'eskd_reached_pct': eskd_reached_pct,
            'median_eskd_age': median_eskd,
            'median_death_age': median_death,
            'mean_death_age': mean_death,
            'eskd_percentiles': eskd_percentiles,
            'death_percentiles': death_percentiles,
            'times_to_eskd': times_to_eskd,
            'times_to_death': times_to_death,
            'final_states': final_states,
            'avg_stage_proportions': avg_stage_proportions,
        }

        return results


class ScenarioAnalysis:
    """
    Runs multiple scenarios and calculates incremental cost-effectiveness.
    """

    def __init__(self, params: ModelParameters):
        """
        Initialize scenario analysis.

        Args:
            params: ModelParameters object
        """
        self.params = params
        self.model = MarkovCohortModel(params)
        self.results = {}

    def run_all_scenarios(self) -> Dict:
        """
        Run all four scenarios and calculate ICERs.

        Scenarios model technical achievement of enzyme restoration with
        mathematically decomposed decline rates: D_total = D_age + (1-θ)×D_path
        where D_age ≈ 0.3 ml/min/yr (normal aging), D_path ≈ 0.8 ml/min/yr.

        0. Natural history (baseline) - no treatment (1.10 ml/min/yr)
        1. Carrier-equivalent (≥50% enzyme) - 100% pathological reduction (0.30 ml/min/yr)
        2. Subthreshold (25-40% enzyme) - 50% pathological reduction (0.70 ml/min/yr)
        3. Minimal benefit (10-20% enzyme) - 20% pathological reduction (0.94 ml/min/yr)

        Biological rationale: Female carriers with ~50% OCRL enzyme have no
        progressive kidney disease (Röschinger et al. 2000), therefore 50%
        enzyme should eliminate pathological decline, leaving only normal aging.

        Returns:
            Dictionary with all scenario results
        """
        natural_decline = self.params.natural_decline_rate

        # Define scenarios with mathematically decomposed decline rates
        # D_total = D_age + (1-θ)×D_path where D_age≈0.3, D_path≈0.8
        scenarios = {
            'Scenario 0: Natural History': {
                'decline_rate': natural_decline,  # 1.10 ml/min/yr
                'include_gt_cost': False,
                'description': 'No treatment - natural disease progression'
            },
            'Scenario 1: Carrier-Equivalent': {
                'decline_rate': 0.30,  # D_age + 0×D_path (θ=1.0: 100% pathological reduction)
                'include_gt_cost': True,
                'description': '≥50% enzyme - complete protection, normal aging only'
            },
            'Scenario 2: Subthreshold': {
                'decline_rate': 0.70,  # D_age + 0.5×D_path (θ=0.5: 50% pathological reduction)
                'include_gt_cost': True,
                'description': '25-40% enzyme - partial protection'
            },
            'Scenario 3: Minimal Benefit': {
                'decline_rate': 0.94,  # D_age + 0.8×D_path (θ=0.2: 20% pathological reduction)
                'include_gt_cost': True,
                'description': '10-20% enzyme - limited benefit'
            }
        }

        # Run each scenario
        for scenario_name, config in scenarios.items():
            print(f"Running {scenario_name}...")
            results = self.model.run_model(
                egfr_decline_rate=config['decline_rate'],
                scenario_name=scenario_name,
                include_gene_therapy_cost=config['include_gt_cost']
            )
            self.results[scenario_name] = results

        # Calculate incremental results vs natural history
        baseline = self.results['Scenario 0: Natural History']

        for scenario_name in scenarios.keys():
            if scenario_name != 'Scenario 0: Natural History':
                self._calculate_incremental_results(scenario_name, baseline)

        return self.results

    def _calculate_incremental_results(
        self,
        scenario_name: str,
        baseline: Dict
    ) -> None:
        """
        Calculate incremental costs, QALYs, and ICER vs baseline.

        Args:
            scenario_name: Name of intervention scenario
            baseline: Baseline (natural history) results
        """
        intervention = self.results[scenario_name]

        # Incremental calculations
        incremental_costs = intervention['total_costs'] - baseline['total_costs']
        incremental_qalys = intervention['total_qalys'] - baseline['total_qalys']

        # Calculate evLYG (equal-value life years gained)
        # Using average baseline utility as reference (weighted by time in each state)
        # For simplicity, use average of CKD utilities as reference
        reference_utility = sum([
            self.model.params.utilities['CKD2'],
            self.model.params.utilities['CKD3a'],
            self.model.params.utilities['CKD3b'],
            self.model.params.utilities['CKD4']
        ]) / 4  # Average across non-ESKD CKD states

        evlyg = incremental_qalys / reference_utility if reference_utility > 0 else 0

        # Calculate ICER
        if incremental_qalys > 0:
            icer = incremental_costs / incremental_qalys
        elif incremental_qalys == 0:
            icer = float('inf') if incremental_costs > 0 else 0
        else:
            icer = float('-inf')  # Dominated (worse outcomes, higher cost)

        # Add to results
        intervention['incremental_costs'] = incremental_costs
        intervention['incremental_qalys'] = incremental_qalys
        intervention['evlyg'] = evlyg
        intervention['icer'] = icer
        intervention['incremental_life_years'] = (
            intervention['life_years'] - baseline['life_years']
        )
        intervention['time_to_eskd_delay'] = (
            intervention['time_to_eskd'] - baseline['time_to_eskd']
        )

    def summarize_results(self) -> pd.DataFrame:
        """
        Create summary table of all scenario results.

        Returns:
            DataFrame with key results for all scenarios
        """
        summary_data = []

        for scenario_name, results in self.results.items():
            row = {
                'Scenario': scenario_name,
                'eGFR Decline Rate': f"{results['egfr_decline_rate']:.2f}",
                'Total Costs ($)': f"${results['total_costs']:,.0f}",
                'Total QALYs': f"{results['total_qalys']:.2f}",
                'Life Years': f"{results['life_years']:.2f}",
                'Time to ESKD (years)': f"{results['time_to_eskd']:.0f}",
            }

            # Add incremental results for intervention scenarios
            if 'incremental_costs' in results:
                row['Incremental Costs ($)'] = f"${results['incremental_costs']:,.0f}"
                row['Incremental QALYs'] = f"{results['incremental_qalys']:.3f}"
                row['ICER ($/QALY)'] = (
                    f"${results['icer']:,.0f}" if abs(results['icer']) < 1e10
                    else "Dominated" if results['icer'] < 0
                    else "Infinity"
                )
            else:
                row['Incremental Costs ($)'] = "Reference"
                row['Incremental QALYs'] = "Reference"
                row['ICER ($/QALY)'] = "Reference"

            summary_data.append(row)

        return pd.DataFrame(summary_data)

    def value_based_pricing_analysis(
        self,
        thresholds: List[float] = None
    ) -> pd.DataFrame:
        """
        Calculate maximum justifiable gene therapy price for each scenario at various
        cost-effectiveness thresholds.

        This is the PRIMARY economic analysis: rather than assuming a price and
        calculating ICER, we solve for the maximum price that achieves each threshold.

        Formula: Max Price = (Threshold × Incremental QALYs) - Incremental Costs (excl. GT)

        Args:
            thresholds: List of ICER thresholds ($/QALY). Default: [100K, 150K, 300K]

        Returns:
            DataFrame with columns:
            - Scenario name
            - Incremental QALYs
            - evLYG
            - Life Years Gained
            - Max price at each threshold
        """
        if thresholds is None:
            thresholds = [100000, 150000, 300000]  # Standard thresholds

        if not self.results:
            raise ValueError("Must run run_all_scenarios() first")

        baseline = self.results['Scenario 0: Natural History']
        pricing_data = []

        for scenario_name, results in self.results.items():
            # Skip natural history
            if scenario_name == 'Scenario 0: Natural History':
                continue

            # Get health outcomes
            inc_qalys = results.get('incremental_qalys', 0)
            evlyg = results.get('evlyg', 0)
            inc_life_years = results.get('incremental_life_years', 0)

            # Calculate costs excluding gene therapy price
            # Total costs include: GT acquisition + monitoring + CKD management
            # We need to subtract GT acquisition to get other costs
            gt_price = self.params.gene_therapy_cost
            total_costs = results['total_costs']
            baseline_costs = baseline['total_costs']

            # Incremental costs excluding gene therapy acquisition price
            # = (total intervention costs - GT price) - baseline costs
            costs_excl_gt = (total_costs - gt_price) - baseline_costs

            # For each threshold, solve for maximum price
            max_prices = {}
            for threshold in thresholds:
                # Max price = (threshold × inc_QALYs) - costs_excl_gt
                # This ensures: (costs_excl_gt + max_price) / inc_QALYs = threshold
                if inc_qalys > 0:
                    max_price = (threshold * inc_qalys) - costs_excl_gt
                    max_prices[f'${threshold/1000:.0f}K/QALY'] = max(0, max_price)
                else:
                    max_prices[f'${threshold/1000:.0f}K/QALY'] = 0

            row = {
                'Scenario': scenario_name,
                'Incremental QALYs': inc_qalys,
                'evLYG': evlyg,
                'Life Years Gained': inc_life_years,
                **max_prices
            }
            pricing_data.append(row)

        df = pd.DataFrame(pricing_data)
        return df


class SensitivityAnalysis:
    """
    Performs one-way and threshold sensitivity analyses.
    """

    def __init__(self, params: ModelParameters):
        """
        Initialize sensitivity analysis.

        Args:
            params: Base case ModelParameters
        """
        self.base_params = params
        self.model = MarkovCohortModel(params)

    def one_way_sensitivity(
        self,
        parameter_ranges: Dict[str, Tuple[float, float]],
        scenario_decline_rate: float = 0.0,  # Stabilization scenario
        include_gt_cost: bool = True
    ) -> pd.DataFrame:
        """
        Perform one-way sensitivity analysis on key parameters.

        Args:
            parameter_ranges: Dict mapping parameter names to (low, high) tuples
            scenario_decline_rate: eGFR decline rate for intervention scenario
            include_gt_cost: Whether to include gene therapy costs

        Returns:
            DataFrame with sensitivity analysis results
        """
        results_list = []

        # Get baseline results
        baseline_params = ModelParameters()
        baseline_model = MarkovCohortModel(baseline_params)
        baseline_results = baseline_model.run_model(
            egfr_decline_rate=baseline_params.natural_decline_rate,
            scenario_name="Baseline",
            include_gene_therapy_cost=False
        )

        for param_name, (low_value, high_value) in parameter_ranges.items():
            print(f"Analyzing parameter: {param_name}")

            # Test low value
            params_low = self._create_varied_params(param_name, low_value)
            model_low = MarkovCohortModel(params_low)
            intervention_low = model_low.run_model(
                egfr_decline_rate=scenario_decline_rate,
                scenario_name=f"{param_name}_low",
                include_gene_therapy_cost=include_gt_cost
            )

            # Recalculate baseline with same parameter change if it affects baseline
            if param_name in ['discount_rate', 'base_mortality_rate']:
                baseline_low = model_low.run_model(
                    egfr_decline_rate=params_low.natural_decline_rate,
                    scenario_name="Baseline_low",
                    include_gene_therapy_cost=False
                )
            else:
                baseline_low = baseline_results

            icer_low = self._calculate_icer(intervention_low, baseline_low)

            # Test high value
            params_high = self._create_varied_params(param_name, high_value)
            model_high = MarkovCohortModel(params_high)
            intervention_high = model_high.run_model(
                egfr_decline_rate=scenario_decline_rate,
                scenario_name=f"{param_name}_high",
                include_gene_therapy_cost=include_gt_cost
            )

            if param_name in ['discount_rate', 'base_mortality_rate']:
                baseline_high = model_high.run_model(
                    egfr_decline_rate=params_high.natural_decline_rate,
                    scenario_name="Baseline_high",
                    include_gene_therapy_cost=False
                )
            else:
                baseline_high = baseline_results

            icer_high = self._calculate_icer(intervention_high, baseline_high)

            # Calculate base case ICER for comparison
            intervention_base = self.model.run_model(
                egfr_decline_rate=scenario_decline_rate,
                scenario_name="Base",
                include_gene_therapy_cost=include_gt_cost
            )
            icer_base = self._calculate_icer(intervention_base, baseline_results)

            results_list.append({
                'Parameter': param_name,
                'Low Value': low_value,
                'High Value': high_value,
                'ICER at Low': icer_low,
                'ICER at Base': icer_base,
                'ICER at High': icer_high,
                'Range': abs(icer_high - icer_low),
                'Base to Low Change': abs(icer_low - icer_base),
                'Base to High Change': abs(icer_high - icer_base)
            })

        df = pd.DataFrame(results_list)
        df = df.sort_values('Range', ascending=False)  # Sort by impact

        return df

    def threshold_analysis(
        self,
        target_icer: float = 100000,  # £100K/QALY threshold
        decline_range: Tuple[float, float] = (0.0, 4.0),
        n_points: int = 50
    ) -> pd.DataFrame:
        """
        Find the eGFR decline reduction needed to meet ICER threshold.

        Args:
            target_icer: Target ICER threshold ($/QALY)
            decline_range: Range of decline rates to test (min, max)
            n_points: Number of points to test

        Returns:
            DataFrame with threshold analysis results
        """
        # Get baseline results
        baseline_results = self.model.run_model(
            egfr_decline_rate=self.base_params.natural_decline_rate,
            scenario_name="Baseline",
            include_gene_therapy_cost=False
        )

        decline_rates = np.linspace(decline_range[0], decline_range[1], n_points)
        results_list = []

        for decline_rate in decline_rates:
            intervention_results = self.model.run_model(
                egfr_decline_rate=decline_rate,
                scenario_name=f"Decline_{decline_rate:.2f}",
                include_gene_therapy_cost=True
            )

            icer = self._calculate_icer(intervention_results, baseline_results)

            # Calculate % reduction from natural decline
            pct_reduction = (
                (self.base_params.natural_decline_rate - decline_rate) /
                self.base_params.natural_decline_rate * 100
            )

            results_list.append({
                'eGFR Decline Rate': decline_rate,
                'Percent Reduction': pct_reduction,
                'Total Costs': intervention_results['total_costs'],
                'Total QALYs': intervention_results['total_qalys'],
                'Incremental Costs': (
                    intervention_results['total_costs'] - baseline_results['total_costs']
                ),
                'Incremental QALYs': (
                    intervention_results['total_qalys'] - baseline_results['total_qalys']
                ),
                'ICER': icer,
                'Below Threshold': icer <= target_icer if icer > 0 else False
            })

        df = pd.DataFrame(results_list)

        # Find threshold crossing point
        below_threshold = df[df['Below Threshold'] == True]
        if not below_threshold.empty:
            threshold_point = below_threshold.iloc[0]
            print(f"\nThreshold Analysis Results:")
            print(f"Target ICER: ${target_icer:,.0f}/QALY")
            print(f"Required eGFR decline rate: {threshold_point['eGFR Decline Rate']:.2f} ml/min/1.73m²/year")
            print(f"Required reduction: {threshold_point['Percent Reduction']:.1f}%")
        else:
            print(f"\nNo scenario meets the ${target_icer:,.0f}/QALY threshold in tested range.")

        return df

    def _create_varied_params(self, param_name: str, value: float) -> ModelParameters:
        """
        Create a new ModelParameters object with one parameter varied.

        Args:
            param_name: Name of parameter to vary
            value: New value for parameter

        Returns:
            New ModelParameters object
        """
        params = ModelParameters()

        # Handle different parameter types
        if param_name == 'discount_rate':
            params.discount_rate = value
        elif param_name == 'gene_therapy_cost':
            params.gene_therapy_cost = value
        elif param_name == 'natural_decline_rate':
            params.natural_decline_rate = value
        elif param_name == 'base_mortality_rate':
            params.base_mortality_rate = value
        elif param_name.startswith('utility_'):
            state = param_name.replace('utility_', '')
            params.utilities[state] = value
        elif param_name.startswith('cost_'):
            state = param_name.replace('cost_', '')
            params.annual_costs[state] = value

        return params

    def _calculate_icer(self, intervention: Dict, baseline: Dict) -> float:
        """
        Calculate ICER between intervention and baseline.

        Args:
            intervention: Intervention results dictionary
            baseline: Baseline results dictionary

        Returns:
            ICER value
        """
        inc_costs = intervention['total_costs'] - baseline['total_costs']
        inc_qalys = intervention['total_qalys'] - baseline['total_qalys']

        if inc_qalys > 0:
            return inc_costs / inc_qalys
        elif inc_qalys == 0:
            return float('inf') if inc_costs > 0 else 0
        else:
            return float('-inf')

    def generate_tornado_data(
        self,
        parameter_ranges: Dict[str, Tuple[float, float]],
        scenario_decline_rate: float = 0.0
    ) -> pd.DataFrame:
        """
        Generate data for tornado diagram (one-way sensitivity).

        Args:
            parameter_ranges: Parameter ranges for testing
            scenario_decline_rate: Decline rate for intervention

        Returns:
            DataFrame formatted for tornado diagram plotting
        """
        owa_results = self.one_way_sensitivity(
            parameter_ranges,
            scenario_decline_rate
        )

        tornado_data = []
        for _, row in owa_results.iterrows():
            # Calculate the spread from base case
            low_diff = row['ICER at Base'] - row['ICER at Low']
            high_diff = row['ICER at High'] - row['ICER at Base']

            tornado_data.append({
                'Parameter': row['Parameter'],
                'Base_ICER': row['ICER at Base'],
                'Low_Value': row['Low Value'],
                'High_Value': row['High Value'],
                'Low_ICER': row['ICER at Low'],
                'High_ICER': row['ICER at High'],
                'Low_Diff': low_diff,
                'High_Diff': high_diff,
                'Total_Range': row['Range']
            })

        df = pd.DataFrame(tornado_data)
        df = df.sort_values('Total_Range', ascending=True)  # Sort for tornado plot

        return df


def run_full_analysis(
    output_dir: str = '/home/user/HTA-Report/Models/Lowe_HTA',
    save_results: bool = True
) -> Dict:
    """
    Run complete cost-effectiveness analysis with all scenarios and sensitivity analyses.

    Args:
        output_dir: Directory to save output files
        save_results: Whether to save results to CSV files

    Returns:
        Dictionary containing all analysis results
    """
    print("=" * 80)
    print("LOWE SYNDROME GENE THERAPY COST-EFFECTIVENESS ANALYSIS")
    print("=" * 80)
    print()

    # Initialize parameters
    params = ModelParameters()

    print("Model Parameters:")
    print(f"  Starting age: {params.starting_age} years")
    print(f"  Starting eGFR: {params.starting_egfr} ml/min/1.73m²")
    print(f"  Time horizon: {params.time_horizon_years} years")
    print(f"  Discount rate: {params.discount_rate * 100}%")
    print(f"  Natural eGFR decline: {params.natural_decline_rate} ml/min/1.73m²/year")
    print(f"  Gene therapy cost: ${params.gene_therapy_cost:,.0f}")
    print()

    # Run scenario analysis
    print("-" * 80)
    print("SCENARIO ANALYSIS")
    print("-" * 80)
    scenario_analysis = ScenarioAnalysis(params)
    scenario_results = scenario_analysis.run_all_scenarios()

    # Get summary table
    summary_df = scenario_analysis.summarize_results()
    print("\nScenario Results Summary:")
    print(summary_df.to_string(index=False))
    print()

    # Save scenario results
    if save_results:
        summary_df.to_csv(f"{output_dir}/scenario_results.csv", index=False)
        print(f"Scenario results saved to: {output_dir}/scenario_results.csv")

    # Run value-based pricing analysis (PRIMARY ANALYSIS)
    print("\n" + "-" * 80)
    print("VALUE-BASED PRICING ANALYSIS (PRIMARY)")
    print("-" * 80)
    pricing_df = scenario_analysis.value_based_pricing_analysis(
        thresholds=[100000, 150000, 300000]
    )
    print("\nMaximum Justifiable Gene Therapy Prices by Scenario:")
    print(pricing_df.to_string(index=False))
    print()
    print("Interpretation:")
    print("  - $100K/QALY: Conventional US threshold")
    print("  - $150K/QALY: High-value threshold for severe conditions")
    print("  - $300K/QALY: Ultra-rare disease threshold (e.g., NICE HST)")
    print()

    if save_results:
        pricing_df.to_csv(f"{output_dir}/value_based_pricing.csv", index=False)
        print(f"Value-based pricing saved to: {output_dir}/value_based_pricing.csv")

    # Run one-way sensitivity analysis
    print("-" * 80)
    print("ONE-WAY SENSITIVITY ANALYSIS")
    print("-" * 80)

    # Define parameter ranges for sensitivity analysis
    param_ranges = {
        'discount_rate': (0.00, 0.07),  # 0% to 7%
        'gene_therapy_cost': (2000000, 4000000),  # $2M to $4M
        'utility_ESKD': (0.30, 0.50),  # ESKD utility
        'utility_CKD2': (0.65, 0.80),  # CKD2 utility
        'cost_ESKD': (100000, 200000),  # ESKD annual cost
        'natural_decline_rate': (3.0, 5.0),  # eGFR decline rate
    }

    sensitivity = SensitivityAnalysis(params)
    owa_results = sensitivity.one_way_sensitivity(
        param_ranges,
        scenario_decline_rate=0.0  # Stabilization scenario
    )

    print("\nOne-Way Sensitivity Analysis Results:")
    print(owa_results[['Parameter', 'ICER at Low', 'ICER at Base', 'ICER at High', 'Range']].to_string(index=False))
    print()

    if save_results:
        owa_results.to_csv(f"{output_dir}/sensitivity_analysis.csv", index=False)
        print(f"Sensitivity analysis saved to: {output_dir}/sensitivity_analysis.csv")

    # Generate tornado diagram data
    tornado_data = sensitivity.generate_tornado_data(param_ranges)
    if save_results:
        tornado_data.to_csv(f"{output_dir}/tornado_diagram_data.csv", index=False)
        print(f"Tornado diagram data saved to: {output_dir}/tornado_diagram_data.csv")

    # Run threshold analysis
    print("-" * 80)
    print("THRESHOLD ANALYSIS")
    print("-" * 80)

    threshold_results = sensitivity.threshold_analysis(
        target_icer=100000,  # $100K/QALY threshold
        decline_range=(0.0, 4.0),
        n_points=50
    )

    if save_results:
        threshold_results.to_csv(f"{output_dir}/threshold_analysis.csv", index=False)
        print(f"Threshold analysis saved to: {output_dir}/threshold_analysis.csv")

    # Prepare cost-effectiveness plane data
    print("\n" + "-" * 80)
    print("COST-EFFECTIVENESS PLANE DATA")
    print("-" * 80)

    ce_plane_data = []
    baseline = scenario_results['Scenario 0: Natural History']

    for scenario_name, results in scenario_results.items():
        if scenario_name != 'Scenario 0: Natural History':
            ce_plane_data.append({
                'Scenario': scenario_name.replace('Scenario ', ''),
                'Incremental_Costs': results['incremental_costs'],
                'Incremental_QALYs': results['incremental_qalys'],
                'ICER': results['icer']
            })

    ce_plane_df = pd.DataFrame(ce_plane_data)
    print("\nCost-Effectiveness Plane Data:")
    print(ce_plane_df.to_string(index=False))

    if save_results:
        ce_plane_df.to_csv(f"{output_dir}/ce_plane_data.csv", index=False)
        print(f"\nCE plane data saved to: {output_dir}/ce_plane_data.csv")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    # Return all results
    return {
        'scenario_results': scenario_results,
        'summary_df': summary_df,
        'value_based_pricing': pricing_df,  # PRIMARY ANALYSIS
        'sensitivity_results': owa_results,
        'tornado_data': tornado_data,
        'threshold_results': threshold_results,
        'ce_plane_data': ce_plane_df,
        'parameters': params
    }


if __name__ == "__main__":
    """
    Main execution block - runs when script is called directly.

    Usage:
        python markov_cua_model.py
    """
    # Run the full analysis
    results = run_full_analysis(
        output_dir='/home/user/HTA-Report/Models/Lowe_HTA',
        save_results=True
    )

    print("\n" + "="*80)
    print("MONTE CARLO VALIDATION (Natural History)")
    print("="*80)
    print("\nRunning 1,000 individual patient simulations to validate cohort model...")

    # Run Monte Carlo validation for natural history
    params = ModelParameters()
    model = MarkovCohortModel(params)
    mc_results = model.run_monte_carlo_validation(
        egfr_decline_rate=params.natural_decline_rate,
        n_simulations=1000,
        random_seed=42
    )

    print(f"\nMonte Carlo Results (n={mc_results['n_simulations']}):")
    print(f"  Patients reaching ESKD: {mc_results['eskd_reached_pct']:.1f}%")
    print(f"\n  ESKD Timing:")
    print(f"    - Median age: {mc_results['median_eskd_age']:.1f} years" if mc_results['median_eskd_age'] else "    - Median age: N/A (most patients die before ESKD)")
    if mc_results['eskd_percentiles']['25th']:
        print(f"    - 25th percentile: {mc_results['eskd_percentiles']['25th']:.1f} years")
        print(f"    - 75th percentile: {mc_results['eskd_percentiles']['75th']:.1f} years")

    print(f"\n  Survival:")
    print(f"    - Median age at death: {mc_results['median_death_age']:.1f} years")
    print(f"    - Mean age at death: {mc_results['mean_death_age']:.1f} years")
    print(f"    - 25th percentile: {mc_results['death_percentiles']['25th']:.1f} years")
    print(f"    - 75th percentile: {mc_results['death_percentiles']['75th']:.1f} years")

    print(f"\n  Average Time Spent in Each CKD Stage:")
    for stage, proportion in sorted(mc_results['avg_stage_proportions'].items()):
        if proportion > 0.01:  # Only show stages with >1% time
            print(f"    - {stage}: {proportion*100:.1f}% of lifespan")

    print(f"\n  Target Validation:")
    target_eskd = 32
    target_death_min = 20
    target_death_max = 40
    eskd_match = "✓" if mc_results['median_eskd_age'] and abs(mc_results['median_eskd_age'] - target_eskd) <= 2 else "✗"
    death_match = "✓" if target_death_min <= mc_results['median_death_age'] <= target_death_max else "✗"
    print(f"    {eskd_match} ESKD at age ~{target_eskd} (Ando 2024)")
    print(f"    {death_match} Survival in 2nd-4th decade (Murdock 2023)")

    print("\n" + "="*80)
    print("\nAll results are available in the 'results' dictionary:")
    print("  - results['scenario_results']: Detailed scenario results")
    print("  - results['summary_df']: Summary table (DataFrame)")
    print("  - results['sensitivity_results']: One-way sensitivity analysis")
    print("  - results['tornado_data']: Tornado diagram data")
    print("  - results['threshold_results']: Threshold analysis")
    print("  - results['ce_plane_data']: Cost-effectiveness plane data")
    print("  - results['mc_validation']: Monte Carlo validation results")

    # Store MC results
    results['mc_validation'] = mc_results
