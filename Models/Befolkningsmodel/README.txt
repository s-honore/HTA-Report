# RARE DISEASE POPULATION MODEL & MARKET POTENTIAL ANALYSIS
## Walther Therapeutics
--------------------------------------------------------------------------

## INTRODUCTION

This model simulates the global incidence, prevalence, and market potential for Lowe Syndrome gene therapy. It provides detailed projections on:

1. Current and future disease prevalence across different regions
2. Regulatory approval pathways across different markets
3. Patient accessibility following market approvals
4. Revenue forecasts based on patient numbers and treatment costs

The model incorporates complex factors including:
- Disease incidence rates and detection probabilities
- Country-specific healthcare systems (using HDI as a proxy)
- Patient lifespans based on survival statistics (Weibull distribution)
- Regulatory approval waves across global markets
- Gradual market penetration post-approval

## SETUP INSTRUCTIONS

### Prerequisites
- Python 3.8 or higher
- Required Python packages: pandas, numpy, matplotlib, plotly, scipy, seaborn
- Approximately 4GB of free disk space for input datasets

### Installation
1. Create a project directory structure with the following folders:
   - `/input_data/` - For input datasets
   - `/output_data/` - For model outputs (created automatically if missing)

2. Download and place the following datasets in the `/input_data/` folder:
   - `WPP2024_POP_F01_1_POPULATION_SINGLE_AGE_BOTH_SEXES.xlsx` (UN Population data)
   - `HDR23-24_Composite_indices_complete_time_series.csv` (HDI data)
   - `WPP2024_Demographic_Indicators_Medium.csv` (Future population projections)
   - `iso_to_region.csv` (Country-region mapping)

3. Ensure Python and required packages are installed:
   ```
   pip install pandas numpy matplotlib plotly scipy seaborn uuid kaleido
   ```

### Running the Model
1. Open the Jupyter notebook `Population_model.ipynb` in Jupyter Lab or Jupyter Notebook
2. Run all cells sequentially from top to bottom
3. Results will be displayed inline in the notebook and saved to the `/output_data/` directory

## MODEL COMPONENTS & METHODOLOGY

### 1. HDI Integration & Projection
The model uses the Human Development Index (HDI) as a proxy for healthcare system capacity, affecting disease detection rates:
- Historical HDI data (1990-2022) forms the base
- Pre-1956 values set to 0 (before disease discovery)
- Future HDI projected using country-specific growth rates
- Missing data filled using regional averages

### 2. Disease Incidence Model
Using a Zero-Inflated Poisson (ZIP) distribution to account for:
- Base incidence of 1 in 500,000 births
- Underreporting in countries with lower HDI
- Complete absence of cases before disease discovery (1956)
- Higher detection rates in countries with better healthcare

### 3. Survival & Lifecycle Simulation
Patient lifespans modeled using Weibull distribution:
- Shape parameter: 2.0 (distribution curve shape)
- Scale parameter: 40.0 (average lifespan)
- Each simulated patient tracked individually through time

### 4. Regulatory Approval Waves
Treatment access modeled via regulatory approval waves:
- Wave 1 (2030): USA and EU/EEA countries
- Wave 2 (2033): Australia, Canada, Brazil, South Korea, Taiwan, Japan
- Wave 3 (2032): Saudi Arabia, Israel, UAE, Switzerland
- Patient numbers calculated for each wave based on age and geography

### 5. Market Potential Analysis
Revenue projections based on:
- Treatment cost assumptions
- Market penetration rates that increase over time
- Patient age restrictions (typically under 21 years)
- Country-specific market access timelines

## MODEL OUTPUTS & INTERPRETATION

The model generates several key outputs:
1. Current prevalence estimates by region and country
2. Future prevalence projections through 2060
3. Eligible patient population by approval wave
4. Annual and cumulative revenue projections
5. Patient distribution by age, region, and country

Key metrics to focus on:
- Peak year revenue estimates
- Cumulative patients treated by 2050
- Early-access markets (Wave 1) that drive initial uptake
- Countries with highest patient populations

## CUSTOMIZATION OPTIONS

The model can be customized by modifying parameters:
1. Disease incidence rates (currently 1/500,000)
2. Survival parameters (shape and scale for Weibull distribution)
3. Approval timelines for different geographic regions
4. Treatment cost assumptions
5. Market penetration rates over time

## DATA SOURCES

1. United Nations Population Division (demographic data)
2. UN Human Development Report (HDI data)
3. WHO and published literature (disease incidence estimates)
4. Regulatory agency trends (approval pathway projections)


## VERSION HISTORY

- v1.0 (April 2025) - Initial release
- v1.1 (Planned) - Enhanced market access modeling
- v1.2 (Planned) - Competitive landscape integration
