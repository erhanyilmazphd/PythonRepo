"""
Example: Custom ACS Simulation Scenario
========================================

This example shows how to create a custom simulation scenario
with your own parameters and run the simulator programmatically.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ptmp_acs_simulator import SimulationConfig, PTMPSimulator
import json


def main():
    """Run a custom simulation scenario"""

    print("=" * 70)
    print("PTMP ACS Simulator - Custom Scenario Example")
    print("=" * 70)

    # Create custom configuration
    config = SimulationConfig(
        n_stations=12,                              # 12 clients
        n_channels=6,                               # 6 channels (e.g., WiFi 802.11a)
        n_time_steps=300,                           # 300 time steps

        # Rate parameters
        min_rate=10.0,                              # 10 Mbps minimum
        max_rate=150.0,                             # 150 Mbps maximum

        # Fairness: 0=random clients, 1=all same distance
        fairness_param=0.3,                         # Mostly random with some clustering

        # Channel interference levels (6 channels)
        base_interference=[0.15, 0.35, 0.25, 0.10, 0.40, 0.20],

        # Channel switching parameters
        switch_threshold=0.1,                       # 10% improvement threshold
        min_dwell_time=15,                          # Minimum 15 steps per channel
    )

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time steps: {config.n_time_steps}")
    print(f"  Rate range: {config.min_rate}-{config.max_rate} Mbps")
    print(f"  Fairness parameter: {config.fairness_param}")
    print(f"  Base interference: {config.base_interference}")

    # Create and run simulator
    print("\nRunning simulation...")
    simulator = PTMPSimulator(config)
    simulator.run()

    # Get summary statistics
    stats = simulator.get_summary_stats()

    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    for algo_name, algo_stats in stats.items():
        print(f"\n{algo_name}:")
        print(f"  Avg Throughput: {algo_stats['avg_throughput']:.2f} Mbps")
        print(f"  Avg Min Rate: {algo_stats['avg_min_rate']:.2f} Mbps")
        print(f"  Fairness Index: {algo_stats['avg_fairness']:.4f}")
        print(f"  Channel Switches: {algo_stats['switches']}")

    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'output',
        'custom_scenario_results.json'
    )

    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print("=" * 70)

    # Show best algorithm by throughput
    best_algo = max(stats.items(),
                   key=lambda x: x[1]['avg_throughput'])
    print(f"\nBest Algorithm (by throughput): {best_algo[0]}")
    print(f"  Throughput: {best_algo[1]['avg_throughput']:.2f} Mbps")

    # Show best algorithm by fairness
    best_fair = max(stats.items(),
                   key=lambda x: x[1]['avg_fairness'])
    print(f"\nBest Algorithm (by fairness): {best_fair[0]}")
    print(f"  Fairness Index: {best_fair[1]['avg_fairness']:.4f}")


if __name__ == '__main__':
    main()
