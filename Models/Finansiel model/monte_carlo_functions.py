import numpy as np
import pandas as pd
from scipy.stats import triang, uniform, bernoulli
import matplotlib.pyplot as plt
import seaborn as sns
import numpy_financial as npf
from tqdm.auto import tqdm
from multiprocessing import Pool

N_ITERATIONS = 1000 # Number of Monte Carlo iterations
CURRENT_YEAR = 2025
COMMERCIAL_LIFE_YEARS = 15 # Years of sales post-launch (peak + decline)
TREATMENT_AGE_LIMIT = 20 # Patients younger than this are eligible

# R&D Phase Parameters (durations in years, costs in USD millions)
# Using triangular distribution: (min, mode, max)
# R&D Phase Functions
def preclinical_duration():
    return triang.rvs(c=0.4, loc=1, scale=2)  # 1 to 3 years, mode 1.8

def preclinical_cost():
    return triang.rvs(c=0.33, loc=1, scale=2)  # 1 to 3M, mode 1.66M

def phase1_2_duration():
    return triang.rvs(c=0.4, loc=2, scale=3)  # 2 to 5 years, mode 3.2

def phase1_2_cost():
    return triang.rvs(c=0.33, loc=3, scale=5)  # 20 to 80M, mode 40M

def phase3_duration():
    return triang.rvs(c=0.5, loc=2, scale=3)  # 2 to 5 years, mode 3.5

def phase3_cost():
    return triang.rvs(c=0.4, loc=10, scale=10)  # 50 to 300M, mode 150M

def regulatory_duration():
    return triang.rvs(c=0.33, loc=0.75, scale=0.75)  # 0.75 to 1.5 years, mode 1

def regulatory_cost():
    return triang.rvs(c=0.5, loc=2, scale=3)  # 2 to 5M, mode 3.5M

# Commercial Functions
def price_usd_millions():
    return triang.rvs(c=0.5, loc=2.0, scale=1.5)  # 2.0M to 3.5M, mode 2.75M

def gt_net_factor():
    return np.random.uniform(0.80, 0.90)  # 10-20% discount band

def cogs_percent_revenue():
    return uniform.rvs(loc=0.15, scale=0.10)  # 15% to 25%

def sga_percent_revenue():
    return uniform.rvs(loc=0.20, scale=0.10)  # 20% to 30%

# Market Penetration Functions
def wave1_max_rate():
    return uniform.rvs(loc=0.4, scale=0.15)  # 40% to 55%

def wave1_steepness():
    return uniform.rvs(loc=0.3, scale=0.3)  # 0.3 to 0.5

def wave1_midpoint_years():
    return triang.rvs(c=0.6, loc=2, scale=3)  # 1 to 4 years, mode 5

def wave2_max_rate():
    return uniform.rvs(loc=0.25, scale=0.2)  # 25% to 45%

def wave2_steepness():
    return uniform.rvs(loc=0.3, scale=0.3)  # 0.3 to 0.5

def wave2_midpoint_years():
    return triang.rvs(c=0.6, loc=2, scale=3)  # 1 to 4 years, mode 5

def wave3_max_rate():
    return uniform.rvs(loc=0.15, scale=0.15)  # 15% to 30%

def wave3_steepness():
    return uniform.rvs(loc=0.3, scale=0.3)  # 0.3 to 0.5

def wave3_midpoint_years():
    return triang.rvs(c=0.6, loc=2, scale=3)  # 1 to 4 years, mode 5

def prv_sale_value_usd_millions():
    return triang.rvs(c=0.4, loc=80, scale=70)  # 80M to 150M, mode 108M

# Updated PARAMS dictionary with named functions
PARAMS = {
    'preclinical': {
        'duration': preclinical_duration,
        'cost': preclinical_cost,
        'pos': 0.85  # Probability of success
    },
    'phase1_2': {
        'duration': phase1_2_duration,
        'cost': phase1_2_cost,
        'pos': 0.82  # PoS for rare disease/gene therapy can be higher than general
    },
    'phase3': {
        'duration': phase3_duration,
        'cost': phase3_cost,
        'pos': 0.90
    },
    'regulatory': {
        'duration': regulatory_duration,
        'cost': regulatory_cost,
        'pos': 0.90
    },
    
    # Commercial Parameters
    'price_usd_millions': price_usd_millions,
    'gt_net_factor': gt_net_factor,
    'cogs_percent_revenue': cogs_percent_revenue,
    'sga_percent_revenue': sga_percent_revenue,
    
    # Market Penetration
    'penetration_wave1': {
        'max_rate': wave1_max_rate,
        'steepness': wave1_steepness,
        'midpoint_years': wave1_midpoint_years
    },
    'penetration_wave2': {
        'max_rate': wave2_max_rate,
        'steepness': wave2_steepness,
        'midpoint_years': wave2_midpoint_years
    },
    'penetration_wave3': {
        'max_rate': wave3_max_rate,
        'steepness': wave3_steepness,
        'midpoint_years': wave3_midpoint_years
    },
    
    # ODD & PRV
    'odd_obtaining_prob': 0.95,
    'odd_rd_tax_credit_rate': 0.25,  # % of clinical trial costs (Phase 1/2 & 3)
    'odd_market_exclusivity_years_us': 7,
    'odd_market_exclusivity_years_eu': 10,
    'pdufa_fee_waiver_usd_millions': 3.0,
    
    'prv_obtaining_prob': 0.50,  # If rare pediatric disease
    'prv_sale_value_usd_millions': prv_sale_value_usd_millions,
    'prv_review_time_reduction_years': 4/12,  # Approx 4 months
    
    # Financial
    'discount_rate': 0.2,  # 20%
    'tax_rate': 0.21,  # Corporate tax rate
}
# Approval Waves (from Population_model.ipynb, using ISO3 codes)
# Base launch year for Wave 1 is 2030 if R&D starts now and is successful on an average timeline.
# The simulation will determine the actual launch year.
BASE_LAUNCH_YEAR_WAVE1 = 2030 



WAVES = {
    'wave1': {
        'countries': ['USA'] + 
                    ['DEU', 'FRA', 'ITA', 'ESP', 'BEL', 'NLD', 'AUT', 'DNK', 'SWE', 'FIN', 'NOR', 'IRL', 'ISL', 'LIE',
                     'PRT', 'GRC', 'POL', 'CZE', 'HUN', 'SVK', 'SVN', 'EST', 'LVA', 'LTU', 'ROU', 'BGR', 'HRV', 'MLT', 'CYP', 'LUX'],  # All EU + EEA
        'launch_delay_from_base': 0  # US + EU (about 1 year difference, but we treat it as same wave)
    },
    'wave2': {
        'countries': ['AUS', 'CAN', 'BRA', 'KOR', 'TWN', 'JPN'],  # Combining previous Wave 3 & 4
        'launch_delay_from_base': 3  # ~3 years after US
    },
    'wave3': {
        'countries': ['SAU', 'ISR', 'ARE', 'CHE'],  # Saudi Arabia, Israel, UAE, Switzerland
        'launch_delay_from_base': 5  # ~5 years after US
    }
}


def sigmoid_penetration(t, max_rate, steepness, midpoint_years):
    """Calculates market penetration at time t using a sigmoid function."""
    return max_rate / (1 + np.exp(-steepness * (t - midpoint_years)))

def get_eligible_patients(timeline_df, year, countries, age_limit):
    """
    Gets the number of eligible patients for a given year and list of countries.
    """
    if timeline_df.empty or 'year' not in timeline_df.columns or 'iso3' not in timeline_df.columns:
        # print(f"Warning: timeline_df is empty or missing required columns for year {year}, countries {countries}")
        return 0 # Return 0 if timeline_df is empty or not properly structured
        
    eligible = timeline_df[
        (timeline_df['year'] == year) &
        (timeline_df['iso3'].isin(countries)) &
        (timeline_df['age'] < age_limit) &
        (timeline_df['alive'] == True)
    ]
    return len(eligible['patient_uuid'].unique())



def simulate_single_iteration(args):
    i, params, waves_config, base_launch_year_w1, timeline_df, current_year, commercial_life_years, treatment_age_limit = args
    
    # Create a copy of the timeline_df to avoid sharing state
    timeline_df = timeline_df.copy()
    # Rest of your simulation logic...
    iter_result = {}
    #for i in tqdm(range(n_iterations)):
    # --- R&D Phase Simulation ---
    iter_rd_costs = {}
    iter_rd_durations = {}
    total_rd_cost = 0
    total_rd_duration = 0
    project_succeeded_through_phase = {} # Tracks success up to end of phase
    
    project_overall_succeeded = True # Will be set to False if any phase fails
    phases = ['preclinical', 'phase1_2', 'phase3', 'regulatory']
    
    odd_obtained_this_run = bernoulli.rvs(params['odd_obtaining_prob'])
    prv_obtained_this_run = False 
    prv_value_this_run = 0

    phase_costs_for_tax_credit = {'phase1_2': 0, 'phase3': 0}
    annual_rd_costs_stream_M_iter = []

    for phase_name in phases:
        phase_duration = params[phase_name]['duration']()
        phase_cost = params[phase_name]['cost']() 
        
        if phase_name == 'regulatory' and odd_obtained_this_run:
            phase_cost = max(0, phase_cost - params['pdufa_fee_waiver_usd_millions'])

        iter_rd_durations[phase_name] = phase_duration
        iter_rd_costs[phase_name] = phase_cost # Store individual phase cost

        total_rd_duration += phase_duration
        total_rd_cost += phase_cost 

        if phase_duration > 0:
            cost_per_year_phase = phase_cost / phase_duration
            for _ in range(int(np.floor(phase_duration))):
                annual_rd_costs_stream_M_iter.append(-cost_per_year_phase)
            if phase_duration % 1 != 0: 
                annual_rd_costs_stream_M_iter.append(-cost_per_year_phase * (phase_duration % 1))
        elif phase_cost > 0 : 
                annual_rd_costs_stream_M_iter.append(-phase_cost)

        if phase_name in ['phase1_2', 'phase3']:
            phase_costs_for_tax_credit[phase_name] = phase_cost
        
        phase_pos_val = params[phase_name]['pos']
        success_outcome = bernoulli.rvs(phase_pos_val)
        project_succeeded_through_phase[phase_name] = success_outcome
        
        #if i < 5: # Debug print for first 5 iterations
        #   print(f"Iter {i}, Phase {phase_name}, PoS: {phase_pos_val}, Actual Cost: {phase_cost:.2f}M, Actual Duration: {phase_duration:.2f}yrs, Outcome: {'Success' if success_outcome else 'Failure'}")

        if not success_outcome: 
            project_overall_succeeded = False
            #if i < 5: 
            #     print(f"Iter {i}, Project FAILED in phase {phase_name}")
            break 
    
    if project_overall_succeeded: 
        if bernoulli.rvs(params['prv_obtaining_prob']):
            prv_obtained_this_run = True
            prv_value_this_run = params['prv_sale_value_usd_millions']()

    iter_result = {
        'iteration': i, 'project_succeeded': project_overall_succeeded,
        'total_rd_cost_millions': total_rd_cost, 'total_rd_duration_years': total_rd_duration,
        'prv_obtained': prv_obtained_this_run, 'prv_value_millions': prv_value_this_run,
        'odd_obtained': odd_obtained_this_run,
        'annual_rd_costs_stream_M': annual_rd_costs_stream_M_iter,
        'annual_commercial_revenues_M': [], 'annual_patients_treated': [],
        'annual_commercial_ebit_M': [], 'annual_commercial_net_cash_flow_M': [],
        'full_project_cash_flow_stream_M': [], 'npv_usd_millions': np.nan,
        'launch_year_w1': np.nan,
        'rnpv_at_preclinical_start': np.nan, 'rnpv_at_phase1_2_start': np.nan,
        'rnpv_at_phase3_start': np.nan, 'rnpv_at_regulatory_start': np.nan,
        'rnpv_at_launch': np.nan
    }
    # Add individual phase costs and durations to iter_result
    for phase_n in phases:
        iter_result[f'cost_{phase_n}_M'] = iter_rd_costs.get(phase_n, 0)
        iter_result[f'duration_{phase_n}_yrs'] = iter_rd_durations.get(phase_n, 0)
        
    if project_overall_succeeded:
        actual_launch_year_w1 = int(current_year + total_rd_duration)
        iter_result['launch_year_w1'] = actual_launch_year_w1

        odd_rd_tax_credit_value = 0
        if odd_obtained_this_run:
            clinical_costs_for_credit = phase_costs_for_tax_credit['phase1_2'] + phase_costs_for_tax_credit['phase3']
            odd_rd_tax_credit_value = clinical_costs_for_credit * params['odd_rd_tax_credit_rate']
        iter_result['odd_tax_credit_millions'] = odd_rd_tax_credit_value if odd_obtained_this_run else 0
        # --- PATIENT-LEVEL TREATMENT LOGIC ---
        # Make a copy of the timeline for this simulation
        timeline_sim = timeline_df.copy()
        timeline_sim['treated'] = False
        annual_commercial_revenues_M_iter = []
        annual_patients_treated_iter = []
        annual_commercial_ebit_M_iter = []
        annual_commercial_net_cash_flow_M_iter = []
        wave_annual_sales = {wave_name: [] for wave_name in waves_config}
        wave_annual_patients = {wave_name: [] for wave_name in waves_config}
        for year_offset in range(commercial_life_years):
            operational_year = actual_launch_year_w1 + year_offset
            annual_revenue_iter_yr = 0
            current_patients_treated_iter_yr = 0
            for wave_name, config in waves_config.items():
                actual_wave_launch_year = actual_launch_year_w1 + config['launch_delay_from_base']
                if operational_year >= actual_wave_launch_year:
                    years_since_wave_launch = operational_year - actual_wave_launch_year
                    # Only select untreated, eligible patients
                    eligible_patients = timeline_sim[(timeline_sim['year'] == operational_year) &
                                                    (timeline_sim['iso3'].isin(config['countries'])) &
                                                    (timeline_sim['age'] < treatment_age_limit) &
                                                    (timeline_sim['alive'] == True) &
                                                    (timeline_sim['treated'] == False)]
                    num_eligible_patients = len(eligible_patients)
                    penetration_params_wave = params[f'penetration_{wave_name}']
                    market_penetration = sigmoid_penetration(
                        t=years_since_wave_launch,
                        max_rate=penetration_params_wave['max_rate'](),
                        steepness=penetration_params_wave['steepness'](),
                        midpoint_years=penetration_params_wave['midpoint_years']()
                    )
                    #price = params['price_usd_millions']()
                    list_price = params['price_usd_millions']()
                    net_price  = list_price * params['gt_net_factor']() 
                    n_to_treat = int(round(num_eligible_patients * market_penetration))
                    n_to_treat = min(n_to_treat, num_eligible_patients)
                    # Randomly select patients to treat
                    if n_to_treat > 0 and num_eligible_patients > 0:
                        patients_to_treat = eligible_patients.sample(n=n_to_treat, replace=False)
                        # Mark ALL records for these patients as treated (across all years)
                        patient_ids_to_treat = patients_to_treat['patient_uuid'].values  # Assuming there's a patient_id column
                        timeline_sim.loc[timeline_sim['patient_uuid'].isin(patient_ids_to_treat), 'treated'] = True
        
                    patients_this_wave_year = n_to_treat
                    annual_revenue_iter_yr += patients_this_wave_year * net_price
                    current_patients_treated_iter_yr += patients_this_wave_year
                    wave_annual_sales[wave_name].append(patients_this_wave_year * net_price)
                    wave_annual_patients[wave_name].append(patients_this_wave_year)
                    #if num_eligible_patients > 0 and i < 5:
                    #   print(f"Iter {i}, OpYear {operational_year}, Wave {wave_name}, Countries {config['countries']}")
                    #   print(f"  Eligible Patients: {num_eligible_patients}, Market Pen: {market_penetration:.4f}, List Price: ${list_price:.2f}M, Net Price: ${net_price:.2f}M, Revenue this wave-yr: ${patients_this_wave_year * net_price:.2f}M")

            annual_commercial_revenues_M_iter.append(annual_revenue_iter_yr)
            annual_patients_treated_iter.append(current_patients_treated_iter_yr)
            cogs = annual_revenue_iter_yr * params['cogs_percent_revenue']()
            sga = annual_revenue_iter_yr * params['sga_percent_revenue']()
            ebit_iter = annual_revenue_iter_yr - cogs - sga
            if year_offset == 0 and prv_obtained_this_run: ebit_iter += prv_value_this_run
            if year_offset == 0 and odd_obtained_this_run: ebit_iter += odd_rd_tax_credit_value
            annual_commercial_ebit_M_iter.append(ebit_iter)
            tax = ebit_iter * params['tax_rate'] if ebit_iter > 0 else 0
            net_cash_flow_iter = ebit_iter - tax
            annual_commercial_net_cash_flow_M_iter.append(net_cash_flow_iter)
        
        #if i < 5:
        #    print(f"Iter {i}, First Full Commercial Year Revenue (annual_commercial_revenues_M_iter[0]): ${annual_commercial_revenues_M_iter[0] if annual_commercial_revenues_M_iter else 0:.2f}M")

        iter_result['annual_commercial_revenues_M'] = annual_commercial_revenues_M_iter
        iter_result['annual_patients_treated'] = annual_patients_treated_iter
        iter_result['annual_commercial_ebit_M'] = annual_commercial_ebit_M_iter
        iter_result['annual_commercial_net_cash_flow_M'] = annual_commercial_net_cash_flow_M_iter
        for wave_name in waves_config:
            iter_result[f"{wave_name}_annual_sales_M"] = wave_annual_sales[wave_name]
            iter_result[f"{wave_name}_annual_patients"] = wave_annual_patients[wave_name]
            iter_result[f"{wave_name}_launch_year"] = actual_launch_year_w1 + waves_config[wave_name]['launch_delay_from_base']
        
        num_rd_years_full = len(annual_rd_costs_stream_M_iter)
        start_commercial_relative_year = actual_launch_year_w1 - current_year
        padding_zeros_count = max(0, start_commercial_relative_year - num_rd_years_full)
        
        current_full_cash_flow_stream = annual_rd_costs_stream_M_iter + [0] * padding_zeros_count + annual_commercial_net_cash_flow_M_iter
        iter_result['full_project_cash_flow_stream_M'] = current_full_cash_flow_stream
        iter_result['npv_usd_millions'] = npf.npv(params['discount_rate'], current_full_cash_flow_stream)

        # Calculate rNPV at phase gates for successful runs
        # rNPV at Launch
        iter_result['rnpv_at_launch'] = npf.npv(params['discount_rate'], annual_commercial_net_cash_flow_M_iter)
        
        # rNPV at Start of Regulatory
        val_at_reg = iter_result['rnpv_at_launch'] * params['regulatory']['pos'] 
        val_at_reg_disc = val_at_reg / ((1 + params['discount_rate']) ** iter_rd_durations['regulatory'])
        iter_result['rnpv_at_regulatory_start'] = val_at_reg_disc - iter_rd_costs['regulatory']

        # rNPV at Start of Phase 3
        val_at_p3 = iter_result['rnpv_at_regulatory_start'] * params['phase3']['pos']
        val_at_p3_disc = val_at_p3 / ((1 + params['discount_rate']) ** iter_rd_durations['phase3'])
        iter_result['rnpv_at_phase3_start'] = val_at_p3_disc - iter_rd_costs['phase3']

        # rNPV at Start of Phase 1/2
        val_at_p12 = iter_result['rnpv_at_phase3_start'] * params['phase1_2']['pos']
        val_at_p12_disc = val_at_p12 / ((1 + params['discount_rate']) ** iter_rd_durations['phase1_2'])
        iter_result['rnpv_at_phase1_2_start'] = val_at_p12_disc - iter_rd_costs['phase1_2']
        
        # rNPV at Start of Preclinical (this is effectively the rNPV from t=0 if project starts preclinical)
        val_at_preclin = iter_result['rnpv_at_phase1_2_start'] * params['preclinical']['pos']
        val_at_preclin_disc = val_at_preclin / ((1 + params['discount_rate']) ** iter_rd_durations['preclinical'])
        iter_result['rnpv_at_preclinical_start'] = val_at_preclin_disc - iter_rd_costs['preclinical']
        # Note: This rnpv_at_preclinical_start is NOT the same as the overall project NPV from t=0,
        # as it doesn't include prior phase costs in its "cost" term, only its own phase cost.
        # The 'npv_usd_millions' is the true t=0 rNPV for the iteration.

    else: # Project failed
        iter_result['full_project_cash_flow_stream_M'] = annual_rd_costs_stream_M_iter
        iter_result['npv_usd_millions'] = npf.npv(params['discount_rate'], annual_rd_costs_stream_M_iter)
        # For failed projects, rNPV at phase gates leading to failure would be negative (cost of that phase)
        # and 0 for phases after failure. For simplicity, we leave them as NaN or handle in analysis.

    #results.append(iter_result)
            
    return iter_result


def run_monte_carlo_simulation(n_iterations, params, waves_config, base_launch_year_w1, 
                             timeline_df, current_year, commercial_life_years, 
                             treatment_age_limit, n_processes=None):
    """
    Run Monte Carlo simulation with multiprocessing and progress bar.
    """
    print(f"Starting Monte Carlo simulation with {n_iterations} iterations...")
    
    # Prepare arguments for each iteration
    args_list = [(i, params, waves_config, base_launch_year_w1, 
                  timeline_df, current_year, 
                  commercial_life_years, treatment_age_limit) 
                 for i in range(n_iterations)]
    
    # Create process pool and run simulations
    with Pool(processes=n_processes) as pool:
        # Use imap for progress bar support
        results = list(tqdm(
            pool.imap(simulate_single_iteration, args_list),
            total=n_iterations,
            desc="Running simulations"
        ))
    
    # Convert results to DataFrame
    return pd.DataFrame(results)
