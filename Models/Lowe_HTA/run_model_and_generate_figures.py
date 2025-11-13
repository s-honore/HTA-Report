"""
Complete HTA Analysis: Run Model + Generate All Figures

This script runs the complete Lowe Syndrome HTA analysis:
1. Runs Markov model with all scenarios
2. Performs sensitivity analyses
3. Generates all publication-quality figures

Author: Sebastian Honoré
Date: November 2025
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from markov_cua_model import run_full_analysis
from generate_hta_figures import generate_all_figures

def main():
    """Run complete HTA analysis with figure generation."""

    print("="*80)
    print("LOWE SYNDROME GENE THERAPY HTA - COMPLETE ANALYSIS")
    print("="*80)
    print()
    print("This script will:")
    print("  1. Run Markov cost-utility model (all scenarios)")
    print("  2. Perform sensitivity analyses")
    print("  3. Calculate value-based pricing")
    print("  4. Generate 8 publication-quality figures")
    print()
    print("Estimated time: 2-5 minutes")
    print()
    input("Press Enter to start...")
    print()

    # Define output directory
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'outputs'
    )
    figures_dir = os.path.join(output_dir, 'figures')

    print("="*80)
    print("STEP 1: RUNNING MARKOV MODEL")
    print("="*80)
    print()

    # Run the full economic analysis
    try:
        results = run_full_analysis(
            output_dir=output_dir,
            save_results=True
        )
        print()
        print("✓ Model completed successfully")
        print()
    except Exception as e:
        print(f"✗ Error running model: {e}")
        print()
        print("Common issues:")
        print("  - Missing dependencies (numpy, pandas)")
        print("  - Missing life table data")
        print("  - Incorrect file paths")
        print()
        return

    print("="*80)
    print("STEP 2: GENERATING FIGURES")
    print("="*80)
    print()

    # Generate all figures
    try:
        generate_all_figures(
            results['scenario_results'],
            results['value_based_pricing'],
            figures_dir
        )
        print()
        print("✓ All figures generated successfully")
        print()
    except Exception as e:
        print(f"✗ Error generating figures: {e}")
        print()
        print("Common issues:")
        print("  - Missing matplotlib dependency")
        print("  - Insufficient disk space")
        print("  - Permission errors")
        print()
        return

    print("="*80)
    print("✓✓✓ ANALYSIS COMPLETE ✓✓✓")
    print("="*80)
    print()
    print("Outputs:")
    print(f"  CSV Results: {output_dir}/")
    print(f"  Figures: {figures_dir}/")
    print()
    print("Generated Files:")
    print("  CSV:")
    print("    - scenario_results.csv")
    print("    - value_based_pricing.csv")
    print("    - sensitivity_analysis.csv")
    print("    - threshold_analysis.csv")
    print("    - tornado_diagram_data.csv")
    print("    - ce_plane_data.csv")
    print()
    print("  Figures (300 DPI PNG):")
    print("    - figure1_scenario_comparison.png")
    print("    - figure2_egfr_trajectories.png")
    print("    - figure3a_population_natural_history.png")
    print("    - figure3b_population_optimistic.png")
    print("    - figure4_cost_over_age.png")
    print("    - figure5_pricing_heatmap.png")
    print("    - figure6_ce_plane.png")
    print("    - figure7_survival_curves.png")
    print("    - figure8_qaly_accumulation.png")
    print()
    print("All figures use Cure Lowe Foundation brand colors and styling.")
    print()
    print("="*80)
    print()


if __name__ == "__main__":
    """Execute main analysis when script is run directly."""
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("="*80)
        print("Analysis interrupted by user")
        print("="*80)
        print()
        sys.exit(0)
    except Exception as e:
        print()
        print()
        print("="*80)
        print("UNEXPECTED ERROR")
        print("="*80)
        print()
        print(f"Error: {e}")
        print()
        print("Please check:")
        print("  1. All dependencies installed (numpy, pandas, matplotlib)")
        print("  2. Life table data file exists")
        print("  3. Write permissions for output directory")
        print()
        print("For support, check:")
        print("  - README.md")
        print("  - QUICKSTART.md")
        print("  - CHANGES_NOVEMBER_2025.md")
        print()
        sys.exit(1)
