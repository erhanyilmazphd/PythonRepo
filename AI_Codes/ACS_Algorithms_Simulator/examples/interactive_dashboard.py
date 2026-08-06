"""
Interactive ACS Simulator Dashboard
Demonstrates enhanced output formatting and visualization
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ptmp_acs_simulator import SimulationConfig, PTMPSimulator
from acs_output_formatter import ACSOutputFormatter
from enhanced_visualizer import EnhancedACSVisualizer
import matplotlib.pyplot as plt


def main():
    """Run interactive dashboard demo"""

    print("\n" + "="*100)
    print("PTMP ACS SIMULATOR - INTERACTIVE DASHBOARD".center(100))
    print("="*100)

    # Configuration
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.5,
        base_interference=[0.15, 0.35, 0.25, 0.10, 0.40],
        switch_threshold=0.08,
        min_dwell_time=10,
        ewma_factor=0.3,
    )

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time Steps: {config.n_time_steps}")
    print(f"  Fairness Parameter: {config.fairness_param}")
    print(f"  Base Interference: {config.base_interference}")

    # Create and run simulator
    print(f"\nRunning simulation...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    # Create output formatter
    formatter = ACSOutputFormatter(config, simulator)

    # Print summary report
    print("\n")
    formatter.print_summary_report()

    # Display sample decision tables at key time steps
    key_steps = [0, config.n_time_steps // 4, config.n_time_steps // 2,
                 3 * config.n_time_steps // 4, config.n_time_steps - 1]

    print("\n" + "="*100)
    print("SAMPLE DECISION TABLES AT KEY TIME STEPS".center(100))
    print("="*100)

    for step in key_steps:
        best_alg = max(simulator.algorithms.keys(),
                      key=lambda a: sum(simulator.environment.base_rates[
                          :, simulator.algorithms[a].current_channel
                      ]))

        print(formatter.generate_algorithm_comparison(step))
        print(formatter.generate_decision_table(best_alg, step))
        print(formatter.generate_station_rates_table(best_alg, step))

    # Generate waterfall summary
    print(formatter.generate_waterfall_summary(window_size=50))

    # Create visualizations
    print("\n" + "="*100)
    print("GENERATING VISUALIZATIONS".center(100))
    print("="*100)

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Create visualizer
    visualizer = EnhancedACSVisualizer(simulator, formatter)

    # Generate visualizations
    print("\nGenerating waterfall dashboard...")
    waterfall_file = os.path.join(output_dir, 'waterfall_dashboard.png')
    visualizer.create_waterfall_dashboard(filename=waterfall_file)
    print(f"✓ Saved: {waterfall_file}")

    print("Generating decision tree visualization (final time step)...")
    decision_file = os.path.join(output_dir, 'decision_tree_final.png')
    visualizer.create_decision_tree_visualization(
        time_step=config.n_time_steps - 1,
        filename=decision_file
    )
    print(f"✓ Saved: {decision_file}")

    print("Generating comparative summary...")
    summary_file = os.path.join(output_dir, 'comparative_summary.png')
    visualizer.create_comparative_summary(filename=summary_file)
    print(f"✓ Saved: {summary_file}")

    # Export to JSON
    print("Exporting detailed results to JSON...")
    json_file = os.path.join(output_dir, 'interactive_results.json')
    formatter.export_to_json(json_file)
    print(f"✓ Saved: {json_file}")

    print("\n" + "="*100)
    print("DASHBOARD GENERATION COMPLETE".center(100))
    print("="*100)

    print(f"\nGenerated Files:")
    print(f"  • {waterfall_file}")
    print(f"  • {decision_file}")
    print(f"  • {summary_file}")
    print(f"  • {json_file}")

    print("\nVisualization files are ready for viewing!")
    print("Open the PNG files to see detailed waterfall charts and decision analysis.")

    # Show interactive mode hint
    print("\n" + "-"*100)
    print("Interactive Features:")
    print("  • Clean decision tables showing all metrics for each channel")
    print("  • Waterfall charts showing algorithm performance over time")
    print("  • Station rate matrices for detailed rate analysis")
    print("  • Algorithm comparison tables")
    print("  • Interference progression tracking")
    print("-"*100 + "\n")


if __name__ == '__main__':
    main()
