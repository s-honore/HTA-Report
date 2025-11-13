# Archive Directory

This directory contains old and diagnostic files that are no longer actively used but are preserved for reference.

## Contents

### diagnostic_scripts/
Python scripts used during model development and calibration:
- `calibrate_*.py` - Calibration scripts for model parameters
- `debug_model.py` - Debugging utilities
- `diagnose_*.py` - Diagnostic scripts for troubleshooting
- `test_*.py` - Testing and validation scripts
- `example_custom_analysis.py` - Example custom analysis
- `realistic_parameter_optimization.py` - Parameter optimization script

### old_outputs/
CSV output files from previous model runs with outdated parameters/scenarios:
- `example*.csv` - Example outputs from older model versions
- `summary_all_scenarios.csv` - Old scenario summary (superseded by scenario_results.csv)

## Current Files
The main working directory contains:
- `markov_cua_model.py` - Main Markov model
- `generate_recalibrated_figures.py` - Figure generation script
- `plot_treatment_scenarios.py` - Scenario plotting script
- `validate_scenarios.py` - Scenario validation script
- Current CSV outputs (scenario_results.csv, value_based_pricing.csv, etc.)
