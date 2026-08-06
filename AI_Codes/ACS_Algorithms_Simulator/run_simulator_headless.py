"""
PTMP ACS Simulator - Headless Mode
Runs simulation and generates PNG outputs for analysis
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt
import numpy as np
from ptmp_acs_simulator import (
    SimulationConfig, PTMPSimulator, SimulatorVisualizer
)
import json
from datetime import datetime


def run_experiment(config: SimulationConfig, experiment_name: str):
    """Run a single experiment and save results"""

    print(f"\n{'='*80}")
    print(f"Experiment: {experiment_name}")
    print(f"{'='*80}")
    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time steps: {config.n_time_steps}")
    print(f"  Rate range: {config.min_rate}-{config.max_rate} Mbps")
    print(f"  Fairness param: {config.fairness_param}")
    print(f"  Base interference: {config.base_interference}")

    # Run simulation
    print("\nRunning simulation...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    # Generate visualization
    print("Generating visualization...")
    visualizer = SimulatorVisualizer(simulator)
    visualizer.create_figure()
    visualizer.update()

    # Save figure
    filename = f"results_{experiment_name}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()

    # Get statistics
    stats = simulator.get_summary_stats()

    # Save statistics to JSON
    json_filename = f"stats_{experiment_name}.json"
    with open(json_filename, 'w') as f:
        # Convert deque to list for JSON serialization
        stats_serializable = {}
        for alg_name, alg_stats in stats.items():
            stats_serializable[simulator.algorithms[alg_name].name] = alg_stats

        json.dump(stats_serializable, f, indent=2)
    print(f"✓ Saved: {json_filename}")

    # Print statistics
    print("\nResults:")
    print("-" * 80)
    for alg_name, stat in stats.items():
        print(f"\n{simulator.algorithms[alg_name].name}:")
        print(f"  Avg Throughput: {stat['avg_throughput']:.2f} Mbps")
        print(f"  Min Throughput: {stat['min_throughput']:.2f} Mbps")
        print(f"  Throughput Std: {stat['std_throughput']:.2f} Mbps")
        print(f"  Avg Min Rate: {stat['avg_min_rate']:.2f} Mbps")
        print(f"  Worst Min Rate: {stat['min_min_rate']:.2f} Mbps")
        print(f"  Avg Fairness: {stat['avg_fairness']:.4f}")
        print(f"  Channel Switches: {stat['switches']}")

    return stats, simulator


def main():
    """Run multiple experiments"""

    print("\n" + "="*80)
    print("PTMP ACS Simulator - Comprehensive Benchmark")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    all_results = {}

    # ========================================================================
    # EXPERIMENT 1: Uniform Distribution (High Fairness)
    # ========================================================================
    config1 = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=10.0,
        max_rate=100.0,
        fairness_param=0.9,  # High: stations close together
        base_interference=[0.1, 0.3, 0.2, 0.15],
        switch_threshold=0.08,
        ewma_factor=0.3,
        min_dwell_time=10,
    )
    all_results['uniform'], sim1 = run_experiment(config1, "exp1_uniform")

    # ========================================================================
    # EXPERIMENT 2: Random Distribution (Low Fairness)
    # ========================================================================
    config2 = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.1,  # Low: stations spread out
        base_interference=[0.2, 0.4, 0.1, 0.3],
        switch_threshold=0.08,
        ewma_factor=0.3,
        min_dwell_time=10,
    )
    all_results['random'], sim2 = run_experiment(config2, "exp2_random")

    # ========================================================================
    # EXPERIMENT 3: High Interference Variability
    # ========================================================================
    config3 = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.5,
        base_interference=[0.5, 0.7, 0.3, 0.6],  # Higher base interference
        interference_noise_std_factor=0.2,  # Higher noise
        switch_threshold=0.08,
        ewma_factor=0.3,
        min_dwell_time=10,
    )
    all_results['high_interference'], sim3 = run_experiment(config3, "exp3_high_interference")

    # ========================================================================
    # EXPERIMENT 4: Conservative Switching (Low Volatility)
    # ========================================================================
    config4 = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.5,
        base_interference=[0.2, 0.4, 0.1, 0.3],
        switch_threshold=0.15,  # Higher threshold = more conservative
        min_dwell_time=20,  # Longer dwell time
        ewma_factor=0.3,
    )
    all_results['conservative'], sim4 = run_experiment(config4, "exp4_conservative")

    # ========================================================================
    # EXPERIMENT 5: Aggressive Switching (High Adaptability)
    # ========================================================================
    config5 = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.5,
        base_interference=[0.2, 0.4, 0.1, 0.3],
        switch_threshold=0.05,  # Lower threshold = more aggressive
        min_dwell_time=5,  # Short dwell time
        ewma_factor=0.5,  # Fast response
    )
    all_results['aggressive'], sim5 = run_experiment(config5, "exp5_aggressive")

    # ========================================================================
    # EXPERIMENT 6: Many Stations
    # ========================================================================
    config6 = SimulationConfig(
        n_stations=16,  # Double the stations
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.3,
        base_interference=[0.2, 0.4, 0.1, 0.3],
        switch_threshold=0.08,
        ewma_factor=0.3,
        min_dwell_time=10,
    )
    all_results['many_stations'], sim6 = run_experiment(config6, "exp6_many_stations")

    # ========================================================================
    # SUMMARY COMPARISON
    # ========================================================================
    print("\n" + "="*80)
    print("COMPARATIVE SUMMARY ACROSS ALL EXPERIMENTS")
    print("="*80)

    comparison_data = {}

    for exp_name, stats in all_results.items():
        print(f"\n{exp_name.upper()}:")
        print("-" * 80)

        for alg_name, stat in stats.items():
            alg_display = list(sim1.algorithms.values())[
                list(sim1.algorithms.keys()).index(alg_name)
            ].name

            if exp_name not in comparison_data:
                comparison_data[exp_name] = {}

            comparison_data[exp_name][alg_display] = {
                'throughput': stat['avg_throughput'],
                'fairness': stat['avg_fairness'],
                'min_rate': stat['avg_min_rate'],
                'switches': stat['switches'],
            }

            print(f"  {alg_display}:")
            print(f"    Throughput: {stat['avg_throughput']:.1f} Mbps | " +
                  f"Fairness: {stat['avg_fairness']:.3f} | " +
                  f"Min Rate: {stat['avg_min_rate']:.1f} | " +
                  f"Switches: {stat['switches']}")

    # Save comparison
    comparison_filename = "comparison_all_experiments.json"
    with open(comparison_filename, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    print(f"\n✓ Saved comparison: {comparison_filename}")

    print("\n" + "="*80)
    print("All experiments completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
