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

Scenarios:
- Scenario 0: Natural history (baseline eGFR decline)
- Scenario 1: Stabilization (0% decline)
- Scenario 2: 70% reduction in decline rate
- Scenario 3: 40% reduction in decline rate

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
    starting_age: int = 5
    time_horizon_years: int = 100
    cycle_length: float = 1.0  # Annual cycles
    discount_rate: float = 0.035  # 3.5% base case

    # eGFR parameters
    starting_egfr: float = 70.0  # ml/min/1.73m² at age 5
    # Calibrated to achieve median ESKD age 32 years (Ando et al. 2024)
    # (70 - 15) / 27 years = 2.04 ml/min/year
    natural_decline_rate: float = 2.04  # ml/min/1.73m²/year natural history

    # Age-dependent decline rates (NOT CURRENTLY USED - disabled for simplicity)
    use_age_dependent_decline: bool = False  # Disabled: use constant decline
    decline_rate_early: float = 1.40  # ml/min/1.73m²/year for ages 5-15
    decline_rate_late: float = 2.38  # ml/min/1.73m²/year for ages 15+ (1.7x acceleration)
    decline_transition_age: int = 15  # Age at which decline accelerates

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
    # Calibrated to match observed median survival of 30-40 years (Ando et al. 2024)
    # Base rate of 0.8% per year achieves life expectancy of ~34 years
    base_mortality_rate: float = 0.008  # 0.8% base annual mortality
    mortality_multipliers: Dict[str, float] = field(default_factory=lambda: {
        'CKD2': 1.0,
        'CKD3a': 1.2,
        'CKD3b': 1.5,
        'CKD4': 2.0,
        'ESKD': 3.0,
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
        Calculate age-dependent eGFR decline rate.

        Args:
            age: Current age of patient
            base_decline: Base decline rate (used for treatment scenarios)

        Returns:
            Adjusted decline rate for current age
        """
        if not self.params.use_age_dependent_decline:
            # Use constant decline rate
            return base_decline

        # For natural history, use age-dependent rates
        # For treatment scenarios, scale the age-dependent rate by treatment effect
        if base_decline == self.params.natural_decline_rate:
            # Natural history: use actual age-dependent rates
            if age < self.params.decline_transition_age:
                return self.params.decline_rate_early
            else:
                return self.params.decline_rate_late
        else:
            # Treatment scenario: scale age-dependent decline by treatment effect
            # Calculate what the natural rate would be at this age
            if age < self.params.decline_transition_age:
                natural_rate = self.params.decline_rate_early
            else:
                natural_rate = self.params.decline_rate_late

            # Scale by treatment effect
            # treatment_effect = base_decline / self.params.natural_decline_rate
            # return natural_rate * treatment_effect
            # Actually, simpler: just use base_decline (it's already the treated rate)
            return base_decline

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

            # Build transition matrix using current state-specific eGFRs
            trans_matrix = self.build_transition_matrix(
                egfr_decline_rate,
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

        Scenarios:
        0. Natural history (baseline)
        1. Stabilization (0% decline)
        2. 70% reduction in decline
        3. 40% reduction in decline

        Returns:
            Dictionary with all scenario results
        """
        natural_decline = self.params.natural_decline_rate

        # Define scenarios
        scenarios = {
            'Scenario 0: Natural History': {
                'decline_rate': natural_decline,
                'include_gt_cost': False
            },
            'Scenario 1: Stabilization (0%)': {
                'decline_rate': 0.0,
                'include_gt_cost': True
            },
            'Scenario 2: 70% Reduction': {
                'decline_rate': natural_decline * 0.30,  # 70% reduction = 30% of baseline
                'include_gt_cost': True
            },
            'Scenario 3: 40% Reduction': {
                'decline_rate': natural_decline * 0.60,  # 40% reduction = 60% of baseline
                'include_gt_cost': True
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

    print("\nAll results are available in the 'results' dictionary:")
    print("  - results['scenario_results']: Detailed scenario results")
    print("  - results['summary_df']: Summary table (DataFrame)")
    print("  - results['sensitivity_results']: One-way sensitivity analysis")
    print("  - results['tornado_data']: Tornado diagram data")
    print("  - results['threshold_results']: Threshold analysis")
    print("  - results['ce_plane_data']: Cost-effectiveness plane data")
